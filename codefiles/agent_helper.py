"""
Agent Helper - Microsoft Foundry agent interaction functions.
"""

import os
import shutil
import json
import re
import subprocess
from datetime import datetime, timezone
from azure.ai.agents import AgentsClient
from azure.core.credentials import AccessToken

_credential = None
_az_cmd = None


def _find_az_cmd():
    """Find the full path to az.cmd on this system."""
    global _az_cmd
    if _az_cmd:
        return _az_cmd

    # Check if az is already on PATH
    found = shutil.which("az")
    if found:
        _az_cmd = found
        return _az_cmd

    # Read full system + user PATH from the Windows registry
    try:
        import winreg
        for hive, subkey in [
            (winreg.HKEY_LOCAL_MACHINE,
             r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"),
            (winreg.HKEY_CURRENT_USER, r"Environment"),
        ]:
            try:
                with winreg.OpenKey(hive, subkey) as key:
                    val, _ = winreg.QueryValueEx(key, "Path")
                    for d in val.split(";"):
                        d = d.strip()
                        if d and os.path.isfile(os.path.join(d, "az.cmd")):
                            _az_cmd = os.path.join(d, "az.cmd")
                            return _az_cmd
            except OSError:
                pass
    except ImportError:
        pass

    # Fallback: scan common install locations
    candidates = [
        r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin",
        r"C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin",
        os.path.join(os.environ.get("LOCALAPPDATA", ""),
                     "Programs", "Microsoft SDKs", "Azure", "CLI2", "wbin"),
    ]
    for d in candidates:
        p = os.path.join(d, "az.cmd")
        if os.path.isfile(p):
            _az_cmd = p
            return _az_cmd

    raise FileNotFoundError(
        "Azure CLI (az.cmd) not found. Please install Azure CLI or run "
        "'Get-Command az' in PowerShell to verify the installation path."
    )


class _CliTokenCredential:
    """Token credential that calls az.cmd directly."""

    def get_token(self, *scopes, **kwargs):
        resource = scopes[0].replace("/.default", "") if scopes else "https://management.azure.com"
        az = _find_az_cmd()
        result = subprocess.run(
            [az, "account", "get-access-token", "--resource", resource, "--output", "json"],
            capture_output=True, text=True, timeout=30, shell=True,
        )
        if result.returncode != 0:
            raise Exception(f"az CLI error: {result.stderr.strip()}")
        token_data = json.loads(result.stdout)
        expires_on = int(datetime.strptime(
            token_data["expiresOn"], "%Y-%m-%d %H:%M:%S.%f"
        ).replace(tzinfo=timezone.utc).timestamp())
        return AccessToken(token_data["accessToken"], expires_on)


def _get_credential():
    """Return a credential for the AI Foundry agent."""
    global _credential
    if _credential is None:
        _credential = _CliTokenCredential()
    return _credential


def reset_credential():
    """Reset the cached credential (useful after az login)."""
    global _credential
    _credential = None


def get_agent_client(endpoint):
    """Create a Microsoft Foundry AgentsClient using Azure credentials."""
    return AgentsClient(endpoint=endpoint, credential=_get_credential())


def run_agent_analysis(endpoint, agent_id, prompt):
    """Send a prompt to the agent pipeline and return the response text."""
    try:
        client = get_agent_client(endpoint)
        thread = client.threads.create()
        client.messages.create(thread_id=thread.id, role="user", content=prompt)
        run = client.runs.create_and_process(thread_id=thread.id, agent_id=agent_id)

        if run.status == "failed":
            error_msg = run.last_error.message if run.last_error else "Unknown error"
            return f"Agent run failed: {error_msg}"

        # Collect ALL assistant message texts.  With connected agents the
        # intermediate responses may appear as separate messages.  We pick
        # the longest one (the final compiled response) so we don't miss
        # any section.
        messages = client.messages.list(thread_id=thread.id)
        assistant_texts = []
        for msg in messages:
            if msg.role == "assistant":
                for part in msg.content:
                    if hasattr(part, "text") and part.text.value:
                        assistant_texts.append(part.text.value)

        if not assistant_texts:
            return "No response from agent."

        # Return the longest assistant message (the final compiled output).
        return max(assistant_texts, key=len)
    except Exception as e:
        return f"Error communicating with agent: {str(e)}"


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------

def _is_metrics_obj(data):
    """Check if a dict looks like a metrics analysis output."""
    return any(
        k in data
        for k in (
            "cpu_analysis", "memory_analysis", "disk_analysis",
            "network_analysis", "overall_health", "metrics_analysis",
        )
    )


def _is_anomaly_obj(data):
    """Check if a dict looks like an anomaly detection output."""
    return any(
        k in data
        for k in (
            "anomalies", "anomaly_summary", "health_assessment",
            "anomaly_detection",
        )
    )


def _is_remediation_obj(data):
    """Check if a dict looks like a remediation output."""
    return any(
        k in data
        for k in (
            "remediation_actions", "remediation_summary",
            "monitoring_recommendations", "preventive_measures",
            "remediation", "remediation_recommendations",
        )
    )


def _categorize(data, result):
    """Sort a parsed JSON object into the appropriate result bucket."""
    if not isinstance(data, dict):
        return

    # Unwrap known wrapper keys so their nested contents are at top level.
    # The LLM may use various key names for each section.
    wrapper_keys = (
        "metrics_analysis", "metric_analysis",
        "anomaly_detection", "anomaly_analysis", "anomaly_results",
        "anomaly_detection_results", "detected_anomalies",
        "remediation_recommendations", "remediation", "remediation_plan",
    )
    for wk in wrapper_keys:
        if wk in data and isinstance(data[wk], dict):
            nested = data.pop(wk)
            data.update(nested)

    metrics_keys = {
        "cpu_analysis", "memory_analysis", "disk_analysis",
        "network_analysis", "overall_health", "vm_name", "analysis_timestamp",
    }
    anomaly_keys = {
        "anomalies", "anomaly_summary", "health_assessment",
    }
    remediation_keys = {
        "remediation_actions", "remediation_summary",
        "monitoring_recommendations", "preventive_measures",
    }

    has_metrics = any(k in data for k in metrics_keys)
    has_anomalies = any(k in data for k in anomaly_keys)
    has_remediation = any(k in data for k in remediation_keys)

    # Deep scan: if anomalies not found at top level, look inside any
    # remaining dict values for anomaly-like keys (handles extra nesting).
    if not has_anomalies:
        for k, v in list(data.items()):
            if isinstance(v, dict) and any(ak in v for ak in anomaly_keys):
                data.pop(k)
                data.update(v)
                has_anomalies = True
                break

    # Combined output with multiple sections
    if sum([has_metrics, has_anomalies, has_remediation]) >= 2:
        if has_metrics:
            result["metrics_analysis"] = {
                k: v for k, v in data.items() if k in metrics_keys
            }
        if has_anomalies:
            result["anomalies"] = {
                k: v for k, v in data.items() if k in anomaly_keys
            }
        if has_remediation:
            result["remediation"] = {
                k: v for k, v in data.items() if k in remediation_keys
            }
        return

    # Single-section objects
    if has_metrics and not result["metrics_analysis"]:
        result["metrics_analysis"] = data
    elif has_anomalies and not result["anomalies"]:
        result["anomalies"] = data
    elif has_remediation and not result["remediation"]:
        result["remediation"] = data


def parse_agent_response(response_text):
    """Parse the combined response from the 3-agent pipeline.

    Handles:
    - A single combined JSON with metrics_analysis, anomaly_detection, remediation keys
    - JSON inside ```json ... ``` code fences
    - Standalone JSON objects in the text
    """
    result = {
        "metrics_analysis": None,
        "anomalies": None,
        "remediation": None,
    }

    # Strategy 1: JSON code fences
    json_blocks = re.findall(r"```(?:json)?\s*\n?(.*?)```", response_text, re.DOTALL)
    for block in json_blocks:
        block = block.strip()
        if not block:
            continue
        try:
            data = json.loads(block)
            _categorize(data, result)
        except json.JSONDecodeError:
            continue

    # Strategy 2: Find standalone JSON objects outside code fences
    if not all(result.values()):
        cleaned = re.sub(r"```(?:json)?\s*\n?.*?```", "", response_text, flags=re.DOTALL)
        brace_depth = 0
        start = -1
        for i, ch in enumerate(cleaned):
            if ch == "{":
                if brace_depth == 0:
                    start = i
                brace_depth += 1
            elif ch == "}":
                brace_depth -= 1
                if brace_depth == 0 and start >= 0:
                    candidate = cleaned[start : i + 1]
                    try:
                        data = json.loads(candidate)
                        _categorize(data, result)
                    except json.JSONDecodeError:
                        pass
                    start = -1

    # Strategy 3: Try parsing the entire response as JSON (agent may return pure JSON)
    if not all(result.values()):
        stripped = response_text.strip()
        if stripped.startswith("{"):
            try:
                data = json.loads(stripped)
                _categorize(data, result)
            except json.JSONDecodeError:
                pass

    return result
