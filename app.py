"""
Flask Web Application & REST API for The Decision Completeness Engine (DCE).
Provides an interactive Visual Decision Studio, real-time pipeline execution,
precision HITL simulation, and process mining analytics.
"""

import os
import json
from flask import Flask, render_template, request, jsonify
from decision_engine import (
    DecisionCompletenessEngine,
    DecisionRequest,
    EvidenceItem,
    EvidenceStatus,
    SourceType,
    get_all_scenarios,
    get_scenario
)

app = Flask(__name__)
engine = DecisionCompletenessEngine()

# In-memory session state for active decision flow
active_state = {
    "current_scenario_id": "vendor_procurement",
    "request": None,
    "initial_evidence": [],
    "current_dossier": [],
    "requirements": [],
    "audit_report": None,
    "investigation_trace": [],
    "hitl_request": None,
    "decision_result": None,
    "pipeline_stage": "IDLE"
}


def load_scenario_into_state(scenario_id: str):
    scen = get_scenario(scenario_id)
    active_state["current_scenario_id"] = scenario_id
    active_state["request"] = scen["request"]
    active_state["initial_evidence"] = list(scen["initial_evidence"])
    active_state["current_dossier"] = list(scen["initial_evidence"])
    active_state["requirements"] = []
    active_state["audit_report"] = None
    active_state["investigation_trace"] = []
    active_state["hitl_request"] = None
    active_state["decision_result"] = None
    active_state["pipeline_stage"] = "LOADED"


# Initialize default scenario
load_scenario_into_state("vendor_procurement")


@app.after_request
def add_caching_headers(response):
    if request.path.startswith("/static"):
        response.headers["Cache-Control"] = "public, max-age=3600"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/scenarios", methods=["GET"])
def api_get_scenarios():
    scenarios = get_all_scenarios()
    summary = {}
    for sid, s in scenarios.items():
        summary[sid] = {
            "id": s["id"],
            "name": s["name"],
            "domain": s["domain"],
            "badge": s["badge"],
            "description": s["description"],
            "request_title": s["request"].title,
            "department": s["request"].department,
            "requester": s["request"].requester,
            "amount": s["request"].context_data.get("amount", 0)
        }
    return jsonify({"scenarios": summary, "current": active_state["current_scenario_id"]})


@app.route("/api/scenarios/select", methods=["POST"])
def api_select_scenario():
    data = request.json or {}
    scenario_id = data.get("scenario_id", "vendor_procurement")
    load_scenario_into_state(scenario_id)
    return jsonify({
        "status": "SUCCESS",
        "scenario_id": scenario_id,
        "request": active_state["request"].model_dump(),
        "initial_evidence_count": len(active_state["initial_evidence"])
    })


@app.route("/api/custom-request", methods=["POST"])
def api_custom_request():
    data = request.json or {}
    title = data.get("title", "Custom Vendor Approval")
    domain = data.get("domain", "procurement")
    requester = data.get("requester", "Operations Lead")
    department = data.get("department", "Corporate Operations")
    amount = float(data.get("amount", 50000))
    summary = data.get("summary", "Ad-hoc decision request requiring evidence completeness verification.")

    custom_req = DecisionRequest(
        id=f"REQ-CUSTOM-{os.urandom(3).hex().upper()}",
        title=title,
        domain=domain,
        requester=requester,
        department=department,
        summary=summary,
        urgency="NORMAL",
        context_data={"amount": amount}
    )

    active_state["current_scenario_id"] = "custom"
    active_state["request"] = custom_req
    active_state["initial_evidence"] = []
    active_state["current_dossier"] = []
    active_state["requirements"] = []
    active_state["audit_report"] = None
    active_state["investigation_trace"] = []
    active_state["hitl_request"] = None
    active_state["decision_result"] = None
    active_state["pipeline_stage"] = "LOADED"

    return jsonify({"status": "SUCCESS", "request": custom_req.model_dump()})


@app.route("/api/pipeline/run-full", methods=["POST"])
def api_run_full_pipeline():
    data = request.json or {}
    auto_hitl = data.get("auto_resolve_hitl", False)
    hitl_action = data.get("hitl_action", "Grant One-Click Approval")
    reviewer = data.get("reviewer_name", "Sarah Jenkins (VP Finance)")

    trace = engine.run_full_pipeline(
        request=active_state["request"],
        initial_evidence=active_state["initial_evidence"],
        auto_resolve_hitl=auto_hitl,
        hitl_action=hitl_action,
        reviewer_name=reviewer
    )

    return jsonify(trace)


@app.route("/api/pipeline/step", methods=["POST"])
def api_step_pipeline():
    """
    Executes a single step in the 8-step pipeline to allow step-by-step walkthrough.
    """
    data = request.json or {}
    target_step = data.get("step")

    req = active_state["request"]
    dossier = active_state["current_dossier"]

    if target_step == 2 or target_step == "plan":
        requirements = engine.planner.plan_requirements(req)
        active_state["requirements"] = requirements
        active_state["pipeline_stage"] = "PLANNED"
        return jsonify({
            "step": 2,
            "status": "COMPLETED",
            "requirements": [r.model_dump() for r in requirements]
        })

    elif target_step == 3 or target_step == "audit":
        if not active_state["requirements"]:
            active_state["requirements"] = engine.planner.plan_requirements(req)

        audit_report = engine.auditor.audit(active_state["requirements"], dossier)
        active_state["audit_report"] = audit_report
        active_state["pipeline_stage"] = "AUDITED"
        return jsonify({
            "step": 3,
            "status": "COMPLETED",
            "audit_report": audit_report.model_dump()
        })

    elif target_step == 5 or target_step == "self_heal":
        if not active_state["audit_report"]:
            audit_report = engine.auditor.audit(active_state["requirements"], dossier)
            active_state["audit_report"] = audit_report

        missing = active_state["audit_report"].missing_requirements
        recovered_items, investigation_trace = engine.retriever.investigate(req, missing)
        dossier.extend(recovered_items)
        active_state["current_dossier"] = dossier
        active_state["investigation_trace"] = investigation_trace

        # Post-heal audit
        post_audit = engine.auditor.audit(active_state["requirements"], dossier)
        active_state["audit_report"] = post_audit
        active_state["pipeline_stage"] = "SELF_HEALED"

        return jsonify({
            "step": 5,
            "status": "COMPLETED",
            "recovered_count": len(recovered_items),
            "recovered_items": [item.model_dump() for item in recovered_items],
            "investigation_trace": investigation_trace,
            "post_audit": post_audit.model_dump()
        })

    elif target_step == 6 or target_step == "hitl_prompt":
        missing = active_state["audit_report"].missing_requirements if active_state["audit_report"] else []
        hitl_prompt = engine.hitl.generate_micro_request(req, missing, dossier)
        active_state["hitl_request"] = hitl_prompt
        active_state["pipeline_stage"] = "HITL_PENDING" if hitl_prompt else "READY_FOR_VERDICT"

        return jsonify({
            "step": 6,
            "status": "PENDING_HUMAN" if hitl_prompt else "NOT_NEEDED",
            "hitl_prompt": hitl_prompt.model_dump() if hitl_prompt else None
        })

    elif target_step == 7 or target_step == "decide":
        decision_result = engine.decider.deliberate(
            req, active_state["requirements"], dossier
        )
        active_state["decision_result"] = decision_result
        active_state["pipeline_stage"] = "DECIDED"

        # Record telemetry
        initial_missing = [r.id for r in active_state["requirements"] if r.id not in [i.requirement_id for i in active_state["initial_evidence"]]]
        self_healed_ids = [i.requirement_id for i in dossier if i.status == EvidenceStatus.SELF_HEALED]
        hitl_ids = [i.requirement_id for i in dossier if i.status == EvidenceStatus.HUMAN_PROVIDED]

        engine.analytics.record_decision(
            request_id=req.id,
            domain=req.domain,
            title=req.title,
            initially_blocked=len(initial_missing) > 0,
            initial_missing=initial_missing,
            self_healed=self_healed_ids,
            required_hitl=hitl_ids
        )

        return jsonify({
            "step": 7,
            "status": "COMPLETED",
            "decision": decision_result.model_dump()
        })

    return jsonify({"error": f"Unknown step '{target_step}'"}), 400


@app.route("/api/hitl/respond", methods=["POST"])
def api_hitl_respond():
    """
    Submits a human response to the precision micro-request.
    """
    data = request.json or {}
    action = data.get("action", "Grant One-Click Approval")
    reviewer = data.get("reviewer_name", "Sarah Jenkins (VP Finance)")
    notes = data.get("notes", "Verified departmental funds availability and authorized expenditure.")

    if not active_state["audit_report"] or not active_state["audit_report"].missing_requirements:
        return jsonify({"error": "No pending missing requirements for HITL."}), 400

    target_req = active_state["audit_report"].missing_requirements[0]
    resolved_item = engine.hitl.resolve_gap(
        target_req=target_req,
        action_chosen=action,
        user_notes=notes,
        user_identity=reviewer
    )

    if resolved_item:
        active_state["current_dossier"].append(resolved_item)

    # Re-audit
    final_audit = engine.auditor.audit(active_state["requirements"], active_state["current_dossier"])
    active_state["audit_report"] = final_audit

    # Deliberate
    decision_result = engine.decider.deliberate(
        active_state["request"], active_state["requirements"], active_state["current_dossier"]
    )
    active_state["decision_result"] = decision_result

    return jsonify({
        "status": "RESOLVED",
        "resolved_item": resolved_item.model_dump() if resolved_item else None,
        "final_audit": final_audit.model_dump(),
        "decision": decision_result.model_dump()
    })


@app.route("/api/analytics", methods=["GET"])
def api_get_analytics():
    metrics = engine.analytics.get_summary_metrics()
    recommendations = [rec.model_dump() for rec in engine.analytics.generate_recommendations()]
    history = engine.analytics.decision_history
    return jsonify({
        "metrics": metrics,
        "recommendations": recommendations,
        "history": history
    })


@app.route("/api/sources", methods=["GET"])
def api_get_sources():
    sources = []
    for connector in engine.retriever.connectors:
        items = []
        if hasattr(connector, "documents"):
            items = connector.documents
        elif hasattr(connector, "emails"):
            items = connector.emails
        elif hasattr(connector, "records"):
            items = connector.records
        elif hasattr(connector, "registries"):
            items = connector.registries

        sources.append({
            "name": connector.name,
            "type": connector.source_type,
            "item_count": len(items),
            "sample_items": items[:3]
        })
    return jsonify({"sources": sources})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("=" * 60)
    print("  The Decision Completeness Engine (DCE) Visual Studio")
    print(f"  Running on http://0.0.0.0:{port}")
    print("=" * 60)
    app.run(host="0.0.0.0", port=port, debug=False)
