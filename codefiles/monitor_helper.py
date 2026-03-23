"""
Monitor Helper - Log Analytics query functions for infrastructure telemetry.
"""

import os
import shutil
import json
import subprocess
from datetime import timedelta, datetime, timezone
import pandas as pd
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
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
    """Return a credential for Log Analytics queries."""
    global _credential
    if _credential is None:
        _credential = _CliTokenCredential()
    return _credential


def reset_credential():
    """Reset the cached credential (useful after az login)."""
    global _credential
    _credential = None


def get_logs_client():
    """Create a Log Analytics query client using Azure credentials."""
    return LogsQueryClient(_get_credential())


def query_metrics(client, workspace_id, query, timespan_hours=1):
    """Execute a KQL query against Log Analytics and return a DataFrame.

    Raises on authentication/authorization errors so callers can surface them.
    Returns None only when the query succeeds but produces no rows.
    """
    response = client.query_workspace(
        workspace_id=workspace_id,
        query=query,
        timespan=timedelta(hours=timespan_hours),
    )
    if response.status == LogsQueryStatus.SUCCESS:
        if response.tables and response.tables[0].rows:
            raw_cols = response.tables[0].columns
            columns = [c.name if hasattr(c, "name") else str(c) for c in raw_cols]
            rows = response.tables[0].rows
            return pd.DataFrame(rows, columns=columns)
    return None


# ---------------------------------------------------------------------------
# Predefined KQL queries
# ---------------------------------------------------------------------------

CPU_QUERY = """
Perf
| where ObjectName in ("Processor", "Processor Information") and CounterName == "% Processor Time" and InstanceName == "_Total"
| project TimeGenerated, Computer, CounterValue
| order by TimeGenerated asc
"""

CPU_FALLBACK_QUERY = """
Perf
| where ObjectName in ("Processor", "Processor Information") and CounterName in ("% Processor Time", "% User Time")
| where InstanceName == "_Total"
| project TimeGenerated, Computer, CounterValue
| order by TimeGenerated asc
"""

MEMORY_QUERY = """
Perf
| where ObjectName == "Memory" and CounterName == "Available MBytes"
| project TimeGenerated, Computer, CounterValue
| order by TimeGenerated asc
"""

MEMORY_FALLBACK_QUERY = """
Perf
| where ObjectName == "Memory" and CounterName in ("% Committed Bytes In Use", "Committed Bytes")
| extend CounterValue = iif(CounterName == "Committed Bytes", CounterValue / 1048576.0, CounterValue)
| project TimeGenerated, Computer, CounterName, CounterValue
| order by TimeGenerated asc
"""

DISK_QUERY = """
Perf
| where ObjectName == "LogicalDisk" and CounterName == "% Free Space"
| where InstanceName != "_Total"
| project TimeGenerated, Computer, InstanceName, CounterValue
| order by TimeGenerated asc
"""

DISK_FALLBACK_QUERY = """
Perf
| where ObjectName == "LogicalDisk" and CounterName in ("% Disk Read Time", "Disk Bytes/sec", "% Idle Time")
| project TimeGenerated, Computer, InstanceName, CounterValue
| order by TimeGenerated asc
"""

NETWORK_QUERY = """
Perf
| where ObjectName has "Network" and CounterName == "Bytes Total/sec"
| project TimeGenerated, Computer, InstanceName, CounterValue
| order by TimeGenerated asc
"""

NETWORK_FALLBACK_QUERY = """
Perf
| where ObjectName has "Network" and CounterName in ("Bytes Total/sec", "Packets Sent/sec", "Packets Received/sec")
| project TimeGenerated, Computer, InstanceName, CounterValue
| order by TimeGenerated asc
"""


def query_cpu(client, workspace_id, timespan_hours=1):
    """Query CPU utilization metrics. Falls back to % Idle Time if % Processor Time is not available."""
    result = query_metrics(client, workspace_id, CPU_QUERY, timespan_hours)
    if result is None or result.empty:
        result = query_metrics(client, workspace_id, CPU_FALLBACK_QUERY, timespan_hours)
    return result


def query_memory(client, workspace_id, timespan_hours=1):
    """Query memory metrics. Falls back to Committed Bytes (converted to MB) if Available MBytes is not available."""
    result = query_metrics(client, workspace_id, MEMORY_QUERY, timespan_hours)
    if result is None or result.empty:
        result = query_metrics(client, workspace_id, MEMORY_FALLBACK_QUERY, timespan_hours)
    return result


def query_disk(client, workspace_id, timespan_hours=1):
    """Query disk metrics. Falls back to % Idle Time if % Free Space is not available."""
    result = query_metrics(client, workspace_id, DISK_QUERY, timespan_hours)
    if result is None or result.empty:
        result = query_metrics(client, workspace_id, DISK_FALLBACK_QUERY, timespan_hours)
    return result


def query_network(client, workspace_id, timespan_hours=1):
    """Query network metrics. Falls back to Packets Sent/sec if Bytes Total/sec is not available."""
    result = query_metrics(client, workspace_id, NETWORK_QUERY, timespan_hours)
    if result is None or result.empty:
        result = query_metrics(client, workspace_id, NETWORK_FALLBACK_QUERY, timespan_hours)
    return result


def build_metrics_prompt(cpu_df, memory_df, disk_df, vm_name="Hack-VM", timespan_hours=1, network_df=None):
    """Build a text prompt from metrics DataFrames for the AI agent."""
    from datetime import datetime, timezone

    prompt = f"""Analyze the following infrastructure telemetry from an Azure Windows Virtual Machine:

VM NAME: {vm_name}
TIME RANGE: Last {timespan_hours} hour(s)
COLLECTION DATE: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}

CPU METRICS (% Processor Time - _Total):
"""
    if cpu_df is not None and not cpu_df.empty:
        # Limit to last 60 data points to keep prompt manageable
        for _, row in cpu_df.tail(60).iterrows():
            prompt += f"  {row['TimeGenerated']} | CPU: {row['CounterValue']:.1f}%\n"
    else:
        prompt += "  No data available\n"

    prompt += "\nMEMORY METRICS:\n"
    if memory_df is not None and not memory_df.empty:
        counter_col = memory_df.get("CounterName")
        for _, row in memory_df.tail(60).iterrows():
            cname = row.get("CounterName", "Available MBytes")
            if cname == "% Committed Bytes In Use":
                prompt += f"  {row['TimeGenerated']} | Committed: {row['CounterValue']:.1f}%\n"
            else:
                prompt += f"  {row['TimeGenerated']} | Available: {row['CounterValue']:.0f} MB\n"
    else:
        prompt += "  No data available\n"

    prompt += "\nDISK METRICS:\n"
    if disk_df is not None and not disk_df.empty:
        for _, row in disk_df.tail(60).iterrows():
            instance = row.get("InstanceName", "Unknown")
            prompt += f"  {row['TimeGenerated']} | Drive: {instance} | Value: {row['CounterValue']:.1f}\n"
    else:
        prompt += "  No data available\n"

    prompt += "\nNETWORK METRICS:\n"
    if network_df is not None and not network_df.empty:
        for _, row in network_df.tail(60).iterrows():
            instance = row.get("InstanceName", "Unknown")
            prompt += f"  {row['TimeGenerated']} | Interface: {instance} | Bytes/sec: {row['CounterValue']:.1f}\n"
    else:
        prompt += "  No data available\n"

    return prompt
