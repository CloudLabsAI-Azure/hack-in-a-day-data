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

    # Build a lookup of remediation actions by category (try multiple key aliases)
    remediation_by_category = {}
    for action in action_list:
        cat = (action.get("category") or action.get("type") or "").lower().strip()
        if cat not in remediation_by_category:
            remediation_by_category[cat] = []
        remediation_by_category[cat].append(action)

    for anomaly in anomaly_list:
        if not isinstance(anomaly, dict):
            continue
        severity = anomaly.get("severity", "INFO").upper()
        if severity not in ("CRITICAL", "WARNING"):
            continue

        category = anomaly.get("category", "general").lower()

        # Build description/evidence/impact from whatever keys the anomaly has.
        # The LLM may use different key names or omit some fields.
        title = anomaly.get("title", "Infrastructure Anomaly")
        description = anomaly.get("description", "")
        evidence = anomaly.get("evidence", "")
        impact = anomaly.get("impact", "")

        if not description:
            description = anomaly.get("details", "") or anomaly.get("summary", "") or title
        if not evidence:
            # Build evidence from any numeric/data fields in the anomaly
            ev_parts = []
            for ek in ("metric_value", "threshold", "value", "current_value", "first_detected"):
                if anomaly.get(ek):
                    ev_parts.append(f"{ek}: {anomaly[ek]}")
            evidence = ", ".join(ev_parts) if ev_parts else f"{severity} {category} anomaly detected"
        if not impact:
            impact = anomaly.get("recommendation", "") or f"{severity} level {category} issue requires attention"

        # Find matching remediation actions for this anomaly
        # Try exact category match first, then partial match, then all actions
        matched_actions = remediation_by_category.get(category, [])
        if not matched_actions:
            # Try partial/fuzzy match on category names
            for cat_key, cat_actions in remediation_by_category.items():
                if category in cat_key or cat_key in category:
                    matched_actions.extend(cat_actions)
        if not matched_actions:
            # No category match at all — include all remediation actions
            matched_actions = action_list
        remediation_text = ""
        if matched_actions:
            parts = []
            for act in matched_actions:
                act_name = act.get("action") or act.get("title") or act.get("name") or "N/A"
                act_impl = act.get("implementation") or act.get("description") or act.get("details") or "N/A"
                act_prio = act.get("priority") or act.get("urgency") or "N/A"
                parts.append(f"- [{act_prio}] {act_name}: {act_impl}")
            remediation_text = "\n".join(parts)

        event_data = {
            "alert_id": f"ALERT-{uuid.uuid4().hex[:8].upper()}",
            "severity": severity,
            "vm_name": vm_name,
            "title": title,
            "category": anomaly.get("category", "general"),
            "description": description,
            "evidence": evidence,
            "impact": impact,
            "remediation": remediation_text,
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
