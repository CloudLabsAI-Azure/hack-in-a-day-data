"""
Intelligent Infrastructure Operations Assistant
Streamlit Dashboard Application
"""

import streamlit as st
import json
import os
from dotenv import load_dotenv
from datetime import datetime
import re
import time
import pandas as pd

from monitor_helper import get_logs_client, query_cpu, query_memory, query_disk, query_network, build_metrics_prompt
from monitor_helper import reset_credential as reset_monitor_credential
from agent_helper import run_agent_analysis, parse_agent_response, reset_credential as reset_agent_credential
from event_grid_helper import publish_anomalies

load_dotenv()

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="InfraOps Assistant",
    page_icon="wrench",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Configuration validation
# ---------------------------------------------------------------------------
def validate_configuration():
    required_vars = {
        "AGENT_API_ENDPOINT": os.getenv("AGENT_API_ENDPOINT"),
        "AGENT_ID": os.getenv("AGENT_ID"),
        "LOG_ANALYTICS_WORKSPACE_ID": os.getenv("LOG_ANALYTICS_WORKSPACE_ID"),
    }
    missing = [k for k, v in required_vars.items() if not v or v.strip() == ""]
    return missing


def show_setup_guide(missing):
    st.error("Configuration Required")
    st.markdown("""
    ### Setup Guide

    Edit the `.env` file in the codefiles folder with your credentials.
    """)
    st.warning(f"**Missing required variables:** {', '.join(missing)}")
    st.stop()


missing = validate_configuration()
if missing:
    show_setup_guide(missing)

# ---------------------------------------------------------------------------
# CSS Styling
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .main-header {
        background: linear-gradient(-45deg, #0F62FE, #14B8A6, #0F62FE, #6366F1);
        background-size: 400% 400%;
        animation: gradientShift 10s ease infinite;
        padding: 2rem 2.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(15,98,254,0.18);
    }
    .main-header h1 { color: #fff; margin: 0; font-size: 2.2rem; font-weight: 700; letter-spacing: -0.5px; }
    .main-header p  { color: rgba(255,255,255,0.85); margin: 0.4rem 0 0; font-size: 1.05rem; }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(18px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .fade-in { animation: fadeInUp 0.5s ease-out; }

    @keyframes statusPulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(16,185,129,0.35); }
        50%      { box-shadow: 0 0 0 8px rgba(16,185,129,0); }
    }
    .status-dot-ok {
        display: inline-block; width: 10px; height: 10px; border-radius: 50%;
        background: #10B981; animation: statusPulse 2s infinite; margin-right: 6px;
    }
    .status-dot-off {
        display: inline-block; width: 10px; height: 10px; border-radius: 50%;
        background: #EF4444; margin-right: 6px;
    }

    .metric-card {
        background: #fff; border-radius: 10px; padding: 1.2rem 1.5rem;
        border: 1px solid #E5E7EB; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        animation: fadeInUp 0.5s ease-out;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.10);
    }
    .metric-card .label { font-size: 0.82rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.3rem; }
    .metric-card .value { font-size: 1.8rem; font-weight: 700; color: #111827; }

    .sev-critical { border-left: 4px solid #EF4444; }
    .sev-high     { border-left: 4px solid #F97316; }
    .sev-medium   { border-left: 4px solid #F59E0B; }
    .sev-low      { border-left: 4px solid #10B981; }

    .badge {
        display: inline-block; padding: 3px 10px; border-radius: 6px;
        font-size: 0.75rem; font-weight: 600; color: #fff; letter-spacing: 0.3px;
    }
    .badge-critical { background: #EF4444; }
    .badge-high     { background: #F97316; }
    .badge-medium   { background: #F59E0B; color: #111; }
    .badge-low      { background: #10B981; }

    .completion-banner {
        padding: 1.2rem; border-radius: 10px; text-align: center; margin: 1rem 0;
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        box-shadow: 0 4px 16px rgba(16,185,129,0.25);
        animation: fadeInUp 0.5s ease-out;
    }
    .completion-banner h3 { margin: 0; color: #fff; font-size: 1.15rem; }
    .completion-banner p  { margin: 0.3rem 0 0; color: rgba(255,255,255,0.9); font-size: 0.92rem; }

    .stButton>button {
        background: linear-gradient(135deg, #0F62FE 0%, #14B8A6 100%);
        color: #fff; font-weight: 600; border: none; padding: 0.7rem 1.8rem;
        border-radius: 8px; transition: all 0.25s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(15,98,254,0.3);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
    }
    [data-testid="stSidebar"] * { color: #E2E8F0 !important; }

    .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
    .stTabs [data-baseweb="tab"] {
        background: #F3F4F6; border-radius: 8px 8px 0 0;
        padding: 0.8rem 1.4rem; font-weight: 600; font-size: 0.9rem;
    }
    .stTabs [aria-selected="true"] {
        background: #fff; border-bottom: 3px solid #0F62FE;
    }

    .stProgress > div > div > div {
        background: linear-gradient(90deg, #0F62FE 0%, #14B8A6 100%);
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>Infrastructure Operations Assistant</h1>
    <p>AI-powered infrastructure health monitoring, anomaly detection, and remediation guidance</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
workspace_id = os.getenv("LOG_ANALYTICS_WORKSPACE_ID")
agent_endpoint = os.getenv("AGENT_API_ENDPOINT")
agent_id = os.getenv("AGENT_ID")
eg_endpoint = os.getenv("EVENT_GRID_ENDPOINT", "").strip()
eg_key = os.getenv("EVENT_GRID_KEY", "").strip()

with st.sidebar:
    st.markdown("### Connection Status")

    agent_ok = bool(agent_endpoint) and bool(agent_id)
    workspace_ok = bool(workspace_id)
    eg_ok = bool(eg_endpoint) and bool(eg_key)

    dot_agent = "ok" if agent_ok else "off"
    dot_law = "ok" if workspace_ok else "off"
    dot_eg = "ok" if eg_ok else "off"
    st.markdown(f'<span class="status-dot-{dot_agent}"></span> Agent', unsafe_allow_html=True)
    st.markdown(f'<span class="status-dot-{dot_law}"></span> Log Analytics', unsafe_allow_html=True)
    st.markdown(f'<span class="status-dot-{dot_eg}"></span> Event Grid Alerts', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Settings")
    vm_name = st.text_input("VM Name (display only)", value="Hack-VM")
    timespan = st.selectbox(
        "Time Range",
        [1, 2, 4, 6, 12, 24],
        index=0,
        format_func=lambda x: f"Last {x} hour(s)",
    )

    st.markdown("---")
    if st.button("Reset Credentials"):
        reset_monitor_credential()
        reset_agent_credential()
        st.success("Credentials reset. Run az login in your terminal, then click Analyze.")

# ---------------------------------------------------------------------------
# Anomaly synthesis helper — fills anomaly list from metrics/remediation
# when the anomaly detection agent returns an empty list despite issues.
# ---------------------------------------------------------------------------
def _ensure_anomalies(parsed_result):
    """If anomaly agent returned no anomalies but metrics/remediation show issues, synthesize entries."""
    anomalies_data = parsed_result.get("anomalies") or {}
    anomaly_list = anomalies_data.get("anomalies", [])
    # Filter out non-dict items (agent may return strings instead of objects)
    anomaly_list = [a for a in anomaly_list if isinstance(a, dict)]
    anomalies_data["anomalies"] = anomaly_list
    if anomaly_list:
        return  # Agent already provided anomalies — nothing to do

    metrics = parsed_result.get("metrics_analysis") or {}
    remediation = parsed_result.get("remediation") or {}
    overall = (metrics.get("overall_health") or {}).get("status", "").upper()
    actions = remediation.get("remediation_actions", [])

    if overall not in ("CRITICAL", "WARNING") and not actions:
        return  # Truly healthy — leave anomalies empty

    synth = []
    for cat_key, cat_label in [
        ("cpu_analysis", "CPU"), ("memory_analysis", "Memory"),
        ("disk_analysis", "Disk"), ("network_analysis", "Network"),
    ]:
        cat_data = metrics.get(cat_key, {})
        if isinstance(cat_data, list):
            cat_data = cat_data[0] if cat_data else {}
        cat_status = (cat_data.get("status") or "").upper()
        if cat_status in ("CRITICAL", "WARNING"):
            synth.append({
                "severity": cat_status,
                "category": cat_label,
                "title": f"{cat_label} {cat_status.title()}",
                "description": cat_data.get("summary", f"{cat_label} is in {cat_status} state"),
                "evidence": f"Status: {cat_status}, Average: {cat_data.get('average_percent', cat_data.get('average_available_mb', 'N/A'))}",
                "impact": next(
                    (a.get("expected_outcome", "") for a in actions
                     if cat_label.lower() in (a.get("action") or "").lower()
                     or cat_label.lower() in (a.get("category") or "").lower()),
                    f"{cat_label} issue requires attention"
                ),
            })

    # Last resort: create from remediation actions themselves
    if not synth and actions:
        for act in actions:
            prio = (act.get("priority") or "").lower()
            sev = "CRITICAL" if prio == "immediate" else "WARNING" if prio == "short-term" else "INFO"
            synth.append({
                "severity": sev,
                "category": act.get("category", "general"),
                "title": act.get("action", "Detected Issue"),
                "description": act.get("implementation", ""),
                "evidence": "Identified by AI remediation analysis",
                "impact": act.get("expected_outcome", ""),
            })

    if synth:
        if not parsed_result.get("anomalies"):
            parsed_result["anomalies"] = {}
        parsed_result["anomalies"]["anomalies"] = synth
        crit = sum(1 for a in synth if a["severity"] == "CRITICAL")
        warn = sum(1 for a in synth if a["severity"] == "WARNING")
        info_c = sum(1 for a in synth if a["severity"] == "INFO")
        parsed_result["anomalies"]["anomaly_summary"] = {
            "critical": crit, "warning": warn, "info": info_c,
            "total_anomalies": len(synth),
            "overall_status": "CRITICAL" if crit else "WARNING" if warn else "INFO",
        }


# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab_analyze, tab_metrics, tab_anomalies, tab_remediation, tab_alerts = st.tabs(
    ["Analyze Infrastructure", "Metrics Overview", "Anomaly Detection", "Remediation", "Alert History"]
)

# ---------------------------------------------------------------------------
# Tab 1: Analyze
# ---------------------------------------------------------------------------
with tab_analyze:
    st.subheader("Run Infrastructure Analysis")
    st.markdown(
        "Click the button below to query live metrics from Log Analytics and send them "
        "to the AI agent pipeline for analysis."
    )

    if st.button("Analyze Infrastructure Health", type="primary"):
        with st.status("Running infrastructure analysis...", expanded=True) as status:
            try:
                st.write("Querying Log Analytics for CPU metrics...")
                logs_client = get_logs_client()
                cpu_df = query_cpu(logs_client, workspace_id, timespan)

                st.write("Querying Log Analytics for memory metrics...")
                memory_df = query_memory(logs_client, workspace_id, timespan)

                st.write("Querying Log Analytics for disk metrics...")
                disk_df = query_disk(logs_client, workspace_id, timespan)

                st.write("Querying Log Analytics for network metrics...")
                network_df = query_network(logs_client, workspace_id, timespan)
            except Exception as e:
                status.update(label="Authentication error", state="error")
                err_str = str(e)
                if "credential" in err_str.lower() or "authentication" in err_str.lower() or "token" in err_str.lower():
                    st.error(
                        f"**Authentication failed.** Run `az login` in your terminal and restart Streamlit.\n\n"
                        f"If running on an Azure VM, make sure a Managed Identity is assigned and has "
                        f"'Log Analytics Reader' + 'Cognitive Services User' roles.\n\n"
                        f"Error: {err_str}"
                    )
                else:
                    st.error(f"Failed to query Log Analytics: {err_str}")
                cpu_df = memory_df = disk_df = network_df = None
                st.stop()

            if cpu_df is None and memory_df is None and disk_df is None:
                status.update(label="No metrics found", state="error")
                st.error(
                    "No metrics data found in Log Analytics. "
                    "Make sure the VM has Azure Monitor Agent installed and the Data Collection Rule is active. "
                    "Try increasing the time range."
                )
            else:
                data_summary = []
                if cpu_df is not None:
                    data_summary.append(f"CPU: {len(cpu_df)} data points")
                if memory_df is not None:
                    data_summary.append(f"Memory: {len(memory_df)} data points")
                if disk_df is not None:
                    data_summary.append(f"Disk: {len(disk_df)} data points")
                if network_df is not None:
                    data_summary.append(f"Network: {len(network_df)} data points")
                st.write(f"Metrics retrieved: {', '.join(data_summary)}")

                st.write("Building analysis prompt...")
                prompt = build_metrics_prompt(cpu_df, memory_df, disk_df, vm_name, timespan, network_df)

                st.write("Sending to AI agent pipeline for analysis...")
                response = run_agent_analysis(agent_endpoint, agent_id, prompt)

                if response and not response.startswith("Error") and not response.startswith("Agent run failed"):
                    st.session_state["last_response"] = response
                    parsed_result = parse_agent_response(response)

                    # --- Ensure anomalies exist when metrics indicate issues ---
                    _ensure_anomalies(parsed_result)

                    st.session_state["last_parsed"] = parsed_result
                    st.session_state["last_cpu_df"] = cpu_df
                    st.session_state["last_memory_df"] = memory_df
                    st.session_state["last_disk_df"] = disk_df
                    st.session_state["last_network_df"] = network_df

                    # Check if parsing extracted any structured data
                    has_structured = any(parsed_result.get(k) for k in ("metrics_analysis", "anomalies", "remediation"))
                    if not has_structured:
                        st.warning(
                            "The agent returned a response but it could not be parsed into structured sections. "
                            "Check the raw response in the expander below."
                        )

                    # Publish CRITICAL/WARNING anomalies to Event Grid
                    if eg_ok:
                        st.write("Publishing alerts to Event Grid...")
                        pub_count, total_alerts, eg_error = publish_anomalies(
                            st.session_state["last_parsed"], vm_name
                        )
                        if eg_error:
                            st.warning(f"Event Grid: {eg_error}")
                        elif pub_count > 0:
                            st.write(f"Published {pub_count} alert(s) to Event Grid.")
                            if "alert_history" not in st.session_state:
                                st.session_state["alert_history"] = []
                            st.session_state["alert_history"].append({
                                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "count": pub_count,
                                "vm": vm_name,
                            })
                        else:
                            st.write("No CRITICAL or WARNING anomalies to publish.")

                    status.update(label="Analysis complete!", state="complete")
                    st.markdown("""
                    <div class="completion-banner">
                        <h3>Analysis Complete</h3>
                        <p>Check the other tabs for detailed results.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    status.update(label="Agent error", state="error")
                    st.error(f"Agent response: {response}")

    if "last_response" in st.session_state:
        with st.expander("View Raw Agent Response"):
            st.text_area("Agent Response", st.session_state["last_response"], height=400)

# ---------------------------------------------------------------------------
# Tab 2: Metrics Overview
# ---------------------------------------------------------------------------
with tab_metrics:
    st.subheader("Metrics Overview")
    parsed = st.session_state.get("last_parsed", {})
    metrics = parsed.get("metrics_analysis") if parsed else None

    if metrics:
        cpu = metrics.get("cpu_analysis", {})
        mem = metrics.get("memory_analysis", {})
        health = metrics.get("overall_health", {})

        cols = st.columns(4)
        with cols[0]:
            status_val = cpu.get("status", "unknown")
            sev = "sev-critical" if status_val == "critical" else "sev-medium" if status_val == "warning" else "sev-low"
            st.markdown(
                f'<div class="metric-card {sev}"><div class="label">CPU Avg</div>'
                f'<div class="value">{cpu.get("average_percent", "N/A")}%</div></div>',
                unsafe_allow_html=True,
            )
        with cols[1]:
            status_val = mem.get("status", "unknown")
            sev = "sev-critical" if status_val == "critical" else "sev-medium" if status_val == "warning" else "sev-low"
            st.markdown(
                f'<div class="metric-card {sev}"><div class="label">Memory Available</div>'
                f'<div class="value">{mem.get("average_available_mb", "N/A")} MB</div></div>',
                unsafe_allow_html=True,
            )
        with cols[2]:
            score = health.get("score", "N/A")
            sev = (
                "sev-critical" if isinstance(score, (int, float)) and score < 50
                else "sev-medium" if isinstance(score, (int, float)) and score < 75
                else "sev-low"
            )
            st.markdown(
                f'<div class="metric-card {sev}"><div class="label">Health Score</div>'
                f'<div class="value">{score}</div></div>',
                unsafe_allow_html=True,
            )
        with cols[3]:
            overall = health.get("status", "unknown").upper()
            badge = (
                "badge-critical" if overall == "CRITICAL"
                else "badge-high" if overall == "WARNING"
                else "badge-low"
            )
            st.markdown(
                f'<div class="metric-card"><div class="label">Overall Status</div>'
                f'<div class="value"><span class="badge {badge}">{overall}</span></div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")

        if cpu.get("summary"):
            st.markdown(f"**CPU:** {cpu['summary']}")
        if mem.get("summary"):
            st.markdown(f"**Memory:** {mem['summary']}")

        disk_list = metrics.get("disk_analysis", [])
        if isinstance(disk_list, list) and disk_list:
            st.markdown("**Disk Analysis:**")
            for d in disk_list:
                d_status = d.get("status", "unknown")
                st.markdown(
                    f"- Drive {d.get('drive', '?')}: {d.get('average_free_percent', '?')}% free "
                    f"({d_status}) - {d.get('summary', '')}"
                )
        elif isinstance(disk_list, dict):
            st.markdown("**Disk Analysis:**")
            d_status = disk_list.get("status", "unknown")
            st.markdown(
                f"- {disk_list.get('summary', d_status)}"
            )

        net = metrics.get("network_analysis", {})
        if isinstance(net, dict) and net.get("summary"):
            st.markdown(f"**Network:** {net['summary']}")

        if health.get("summary"):
            st.markdown(f"**Overall:** {health['summary']}")

        # CPU chart from raw data
        cpu_df = st.session_state.get("last_cpu_df")
        if cpu_df is not None and not cpu_df.empty:
            st.markdown("### CPU Utilization Over Time")
            chart_df = cpu_df.copy()
            chart_df["TimeGenerated"] = pd.to_datetime(chart_df["TimeGenerated"])
            chart_df = chart_df.set_index("TimeGenerated")
            st.line_chart(chart_df["CounterValue"], use_container_width=True)

        # Memory chart
        memory_df = st.session_state.get("last_memory_df")
        if memory_df is not None and not memory_df.empty:
            st.markdown("### Available Memory Over Time")
            chart_df = memory_df.copy()
            chart_df["TimeGenerated"] = pd.to_datetime(chart_df["TimeGenerated"])
            chart_df = chart_df.set_index("TimeGenerated")
            st.line_chart(chart_df["CounterValue"], use_container_width=True)

        # Disk chart
        disk_df = st.session_state.get("last_disk_df")
        if disk_df is not None and not disk_df.empty:
            st.markdown("### Disk Metrics Over Time")
            chart_df = disk_df.copy()
            chart_df["TimeGenerated"] = pd.to_datetime(chart_df["TimeGenerated"])
            chart_df = chart_df.set_index("TimeGenerated")
            st.line_chart(chart_df["CounterValue"], use_container_width=True)

        # Network chart
        network_df = st.session_state.get("last_network_df")
        if network_df is not None and not network_df.empty:
            st.markdown("### Network Throughput Over Time")
            chart_df = network_df.copy()
            chart_df["TimeGenerated"] = pd.to_datetime(chart_df["TimeGenerated"])
            chart_df = chart_df.set_index("TimeGenerated")
            st.line_chart(chart_df["CounterValue"], use_container_width=True)
    else:
        st.info("Run an analysis from the first tab to see metrics here.")

# ---------------------------------------------------------------------------
# Tab 3: Anomaly Detection
# ---------------------------------------------------------------------------
with tab_anomalies:
    st.subheader("Anomaly Detection")
    parsed = st.session_state.get("last_parsed", {})
    anomalies = parsed.get("anomalies") if parsed else None

    if anomalies:
        summary = anomalies.get("anomaly_summary", {})

        # Recalculate counts from the actual anomaly list if summary is empty/zero
        anomaly_list = anomalies.get("anomalies", [])

        if anomaly_list and not summary.get("total_anomalies"):
            crit = sum(1 for a in anomaly_list if a.get("severity", "").upper() == "CRITICAL")
            warn = sum(1 for a in anomaly_list if a.get("severity", "").upper() == "WARNING")
            info = sum(1 for a in anomaly_list if a.get("severity", "").upper() == "INFO")
            summary = {"critical": crit, "warning": warn, "info": info, "total_anomalies": len(anomaly_list)}

        cols = st.columns(4)
        with cols[0]:
            st.markdown(
                f'<div class="metric-card sev-critical"><div class="label">Critical</div>'
                f'<div class="value">{summary.get("critical", 0)}</div></div>',
                unsafe_allow_html=True,
            )
        with cols[1]:
            st.markdown(
                f'<div class="metric-card sev-high"><div class="label">Warning</div>'
                f'<div class="value">{summary.get("warning", 0)}</div></div>',
                unsafe_allow_html=True,
            )
        with cols[2]:
            st.markdown(
                f'<div class="metric-card sev-medium"><div class="label">Info</div>'
                f'<div class="value">{summary.get("info", 0)}</div></div>',
                unsafe_allow_html=True,
            )
        with cols[3]:
            total = summary.get("total_anomalies", 0)
            st.markdown(
                f'<div class="metric-card"><div class="label">Total</div>'
                f'<div class="value">{total}</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # Health assessment
        ha = anomalies.get("health_assessment", {})
        if ha:
            ha_cols = st.columns(4)
            for i, (key, label) in enumerate(
                [("cpu_status", "CPU"), ("memory_status", "Memory"), ("disk_status", "Disk"), ("network_status", "Network")]
            ):
                val = ha.get(key, "UNKNOWN").upper()
                badge = (
                    "badge-critical" if val == "CRITICAL"
                    else "badge-high" if val == "WARNING"
                    else "badge-low" if val == "HEALTHY"
                    else "badge-medium"
                )
                with ha_cols[i]:
                    st.markdown(
                        f'<span class="badge {badge}">{label}: {val}</span>',
                        unsafe_allow_html=True,
                    )
            if ha.get("overall_risk"):
                st.markdown(f"**Overall Risk:** {ha['overall_risk']}")

        st.markdown("---")

        # Anomaly list
        anomaly_list = [a for a in anomalies.get("anomalies", []) if isinstance(a, dict)]
        if anomaly_list:
            for a in anomaly_list:
                sev = a.get("severity", "INFO").upper()
                sev_css = "critical" if sev == "CRITICAL" else "high" if sev == "WARNING" else "medium"
                badge_css = f"badge-{sev_css}"

                # Extract fields with fallbacks for different key names the LLM may use
                a_title = (a.get("title") or a.get("name") or a.get("anomaly_type")
                           or a.get("type") or a.get("anomaly") or "Anomaly")
                a_desc = (a.get("description") or a.get("details") or a.get("detail")
                          or a.get("summary") or a.get("message") or "")
                a_evidence = (a.get("evidence") or a.get("data") or a.get("metric_value")
                              or a.get("observed_value") or a.get("current_value") or "")
                a_impact = (a.get("impact") or a.get("risk") or a.get("consequence")
                            or a.get("recommendation") or "")

                # If still empty, build from all available keys in the anomaly dict
                if not a_desc:
                    skip_keys = {"severity", "category", "id", "first_detected"}
                    parts = [f"{k}: {v}" for k, v in a.items()
                             if k not in skip_keys and v and k != "severity"]
                    a_desc = "; ".join(parts) if parts else ""

                st.markdown(
                    f"""<div class="metric-card sev-{sev_css}" style="margin-bottom: 0.8rem;">
                    <span class="badge {badge_css}">{sev}</span>
                    &nbsp;<strong>{a_title}</strong>
                    <span class="badge badge-medium">{a.get("category", "")}</span>
                    <p style="margin-top:0.5rem;">{a_desc}</p>
                    <p><em>Evidence:</em> {a_evidence or "N/A"}</p>
                    <p><em>Impact:</em> {a_impact or "N/A"}</p>
                    </div>""",
                    unsafe_allow_html=True,
                )
        else:
            st.success("No anomalies detected. Infrastructure is healthy.")
    else:
        st.info("Run an analysis from the first tab to see anomaly detection results here.")

# ---------------------------------------------------------------------------
# Tab 4: Remediation
# ---------------------------------------------------------------------------
with tab_remediation:
    st.subheader("Remediation Recommendations")
    parsed = st.session_state.get("last_parsed", {})
    remediation = parsed.get("remediation") if parsed else None

    if remediation:
        summary = remediation.get("remediation_summary", {})

        cols = st.columns(4)
        with cols[0]:
            st.markdown(
                f'<div class="metric-card sev-critical"><div class="label">Immediate</div>'
                f'<div class="value">{summary.get("immediate", 0)}</div></div>',
                unsafe_allow_html=True,
            )
        with cols[1]:
            st.markdown(
                f'<div class="metric-card sev-medium"><div class="label">Short-term</div>'
                f'<div class="value">{summary.get("short_term", 0)}</div></div>',
                unsafe_allow_html=True,
            )
        with cols[2]:
            st.markdown(
                f'<div class="metric-card sev-low"><div class="label">Medium-term</div>'
                f'<div class="value">{summary.get("medium_term", 0)}</div></div>',
                unsafe_allow_html=True,
            )
        with cols[3]:
            st.markdown(
                f'<div class="metric-card"><div class="label">Total Actions</div>'
                f'<div class="value">{summary.get("total_actions", 0)}</div></div>',
                unsafe_allow_html=True,
            )

        if summary.get("estimated_resolution_time"):
            st.markdown(f"**Estimated resolution time for immediate actions:** {summary['estimated_resolution_time']}")

        st.markdown("---")

        # Remediation actions
        actions = remediation.get("remediation_actions", [])
        if actions:
            st.markdown("### Corrective Actions")
            for action in actions:
                priority = action.get("priority", "Medium-term")
                sev = "critical" if priority == "Immediate" else "medium" if priority == "Short-term" else "low"
                badge = f"badge-{'critical' if sev == 'critical' else 'high' if sev == 'medium' else 'low'}"
                risk = action.get("risk", "LOW")
                st.markdown(
                    f"""<div class="metric-card sev-{sev}" style="margin-bottom: 0.8rem;">
                    <span class="badge {badge}">{priority}</span>
                    &nbsp;<strong>{action.get("action", "")}</strong>
                    <span class="badge badge-medium">{action.get("category", "")}</span>
                    <p style="margin-top:0.5rem;"><em>Implementation:</em> {action.get("implementation", "")}</p>
                    <p><em>Azure Service:</em> {action.get("azure_service", "N/A")}
                    &nbsp;|&nbsp;<em>Effort:</em> {action.get("estimated_effort", "N/A")}
                    &nbsp;|&nbsp;<em>Risk:</em> {risk}</p>
                    <p><em>Expected Outcome:</em> {action.get("expected_outcome", "N/A")}</p>
                    </div>""",
                    unsafe_allow_html=True,
                )

        # Monitoring recommendations
        monitoring = remediation.get("monitoring_recommendations", [])
        if monitoring:
            st.markdown("### Monitoring Recommendations")
            for m in monitoring:
                st.markdown(
                    f"- **{m.get('metric', '')}**: Threshold {m.get('threshold', 'N/A')}, "
                    f"Check every {m.get('frequency', 'N/A')}, "
                    f"Notify {m.get('action_group', 'N/A')}"
                )

        # Preventive measures
        preventive = remediation.get("preventive_measures", [])
        if preventive:
            st.markdown("### Preventive Measures")
            for p in preventive:
                st.markdown(f"- {p}")
    else:
        st.info("Run an analysis from the first tab to see remediation recommendations here.")

# ---------------------------------------------------------------------------
# Tab 5: Alert History
# ---------------------------------------------------------------------------
with tab_alerts:
    st.subheader("Alert History")

    if not eg_ok:
        st.warning(
            "Event Grid is not configured. Add EVENT_GRID_ENDPOINT and EVENT_GRID_KEY "
            "to your .env file to enable automated alerting."
        )
    else:
        st.markdown(
            "When the analysis detects CRITICAL or WARNING anomalies, they are automatically "
            "published to Azure Event Grid. A Logic App subscribes to these events and sends "
            "email notifications with the AI-generated insights."
        )

    history = st.session_state.get("alert_history", [])
    if history:
        st.markdown("### Published Alerts (This Session)")
        for entry in reversed(history):
            st.markdown(
                f'<div class="metric-card" style="margin-bottom: 0.6rem;">'
                f'<strong>{entry["time"]}</strong> - Published <strong>{entry["count"]}</strong> '
                f'alert(s) for VM <strong>{entry["vm"]}</strong></div>',
                unsafe_allow_html=True,
            )
    else:
        st.info("No alerts have been published yet. Run an analysis that detects CRITICAL or WARNING anomalies.")
