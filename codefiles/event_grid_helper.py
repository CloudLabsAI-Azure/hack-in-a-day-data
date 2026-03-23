"""
Event Grid Helper
Publishes CRITICAL and WARNING anomalies from the AI agent analysis
to an Azure Event Grid Topic. A Logic App subscribes to this topic
and sends emails containing the AI-generated insights.
"""

import os
import json
import uuid
from datetime import datetime, timezone
from azure.eventgrid import EventGridPublisherClient, EventGridEvent
from azure.core.credentials import AzureKeyCredential


def get_event_grid_client():
    """Create and return an Event Grid publisher client."""
    endpoint = os.getenv("EVENT_GRID_ENDPOINT", "").strip()
    key = os.getenv("EVENT_GRID_KEY", "").strip()

    if not endpoint or not key:
        return None

    credential = AzureKeyCredential(key)
    return EventGridPublisherClient(endpoint, credential)


def build_alert_events(parsed_response, vm_name="Hack-VM"):
    """
    Extract CRITICAL and WARNING anomalies from the parsed agent response
    and build Event Grid events that include the AI analysis content.
    """
    events = []
    anomalies_data = parsed_response.get("anomalies") or {}
    remediation_data = parsed_response.get("remediation") or {}

    anomaly_list = anomalies_data.get("anomalies", [])
    action_list = remediation_data.get("remediation_actions", [])

    # Build a lookup of remediation actions by category
    remediation_by_category = {}
    for action in action_list:
        cat = action.get("category", "").lower()
        if cat not in remediation_by_category:
            remediation_by_category[cat] = []
        remediation_by_category[cat].append(action)

    for anomaly in anomaly_list:
        severity = anomaly.get("severity", "INFO").upper()
        if severity not in ("CRITICAL", "WARNING"):
            continue

        category = anomaly.get("category", "general").lower()

        # Find matching remediation actions for this anomaly
        matched_actions = remediation_by_category.get(category, [])
        remediation_text = ""
        if matched_actions:
            parts = []
            for act in matched_actions:
                parts.append(
                    f"- [{act.get('priority', 'N/A')}] {act.get('action', 'N/A')}: "
                    f"{act.get('implementation', 'N/A')}"
                )
            remediation_text = "\n".join(parts)

        # Health assessment context
        health = anomalies_data.get("health_assessment") or {}

        event_data = {
            "alert_id": f"ALERT-{uuid.uuid4().hex[:8].upper()}",
            "severity": severity,
            "vm_name": vm_name,
            "title": anomaly.get("title", "Infrastructure Anomaly"),
            "category": anomaly.get("category", "general"),
            "description": anomaly.get("description", ""),
            "evidence": anomaly.get("evidence", ""),
            "impact": anomaly.get("impact", ""),
            "remediation": remediation_text,
            "health_assessment": {
                "cpu_status": health.get("cpu_status", "UNKNOWN"),
                "memory_status": health.get("memory_status", "UNKNOWN"),
                "disk_status": health.get("disk_status", "UNKNOWN"),
                "network_status": health.get("network_status", "UNKNOWN"),
                "overall_risk": health.get("overall_risk", "UNKNOWN"),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        event = EventGridEvent(
            event_type="InfraOps.Anomaly.Detected",
            subject=f"/infraops/{vm_name}/anomaly/{category}",
            data=event_data,
            data_version="1.0",
        )
        events.append(event)

    return events


def publish_anomalies(parsed_response, vm_name="Hack-VM"):
    """
    Publish CRITICAL/WARNING anomalies to Event Grid.
    Returns tuple: (published_count, total_critical_warning, error_message)
    """
    client = get_event_grid_client()
    if client is None:
        return 0, 0, "Event Grid not configured (missing endpoint or key)"

    events = build_alert_events(parsed_response, vm_name)
    if not events:
        return 0, 0, None

    try:
        client.send(events)
        return len(events), len(events), None
    except Exception as e:
        return 0, len(events), str(e)
