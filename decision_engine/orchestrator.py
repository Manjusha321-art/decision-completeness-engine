"""
Master Orchestrator for The Decision Completeness Engine.
Executes the full 8-step lifecycle with state tracking, callbacks,
and precision human-in-the-loop interception.
"""

from typing import Dict, Any, List, Optional, Callable
from .models import (
    DecisionRequest,
    EvidenceRequirement,
    EvidenceItem,
    EvidenceStatus,
    CompletenessAuditReport,
    HITLRequest,
    DecisionExecutionResult,
    DecisionVerdict
)
from .planner import EvidencePlanner
from .auditor import EvidenceAuditor
from .retriever import AutonomousRetriever
from .hitl import PrecisionHITL
from .decider import DecisionDeliberator
from .analytics import ProcessAnalyticsEngine
from .scenarios import get_scenario


class DecisionCompletenessEngine:
    """
    Main Engine Class orchestrating the 8 core steps.
    """

    def __init__(self):
        self.planner = EvidencePlanner()
        self.auditor = EvidenceAuditor()
        self.retriever = AutonomousRetriever()
        self.hitl = PrecisionHITL()
        self.decider = DecisionDeliberator()
        self.analytics = ProcessAnalyticsEngine()

    def run_full_pipeline(
        self,
        request: DecisionRequest,
        initial_evidence: List[EvidenceItem] = None,
        auto_resolve_hitl: bool = False,
        hitl_action: str = "Grant One-Click Approval",
        reviewer_name: str = "Sarah Jenkins (VP Finance)"
    ) -> Dict[str, Any]:
        """
        Executes all steps of the Decision Completeness Engine.
        Returns a rich execution trace containing data and outcomes at every step.
        """
        trace: Dict[str, Any] = {
            "request_id": request.id,
            "title": request.title,
            "domain": request.domain,
            "steps": {}
        }

        # Step 1: Request Ingested
        dossier: List[EvidenceItem] = list(initial_evidence or [])
        trace["steps"]["step1_intake"] = {
            "status": "COMPLETED",
            "request": request.model_dump(),
            "initial_dossier_count": len(dossier)
        }

        # Step 2: Evidence Planning
        requirements: List[EvidenceRequirement] = self.planner.plan_requirements(request)
        trace["steps"]["step2_planning"] = {
            "status": "COMPLETED",
            "requirements_count": len(requirements),
            "requirements": [r.model_dump() for r in requirements]
        }

        # Step 3: Initial Audit & Completeness Check
        initial_audit: CompletenessAuditReport = self.auditor.audit(requirements, dossier)
        trace["steps"]["step3_initial_audit"] = {
            "status": "COMPLETED",
            "completeness_score": initial_audit.completeness_score,
            "is_complete": initial_audit.is_complete,
            "verified_count": initial_audit.verified_count,
            "missing_count": initial_audit.missing_count,
            "audit_items": initial_audit.items
        }

        # Step 4: Gatekeeper Evaluation
        initially_blocked = not initial_audit.is_complete
        initial_missing_ids = [r.id for r in initial_audit.missing_requirements]
        trace["steps"]["step4_gatekeeper"] = {
            "status": "ENGAGED" if initially_blocked else "PASSED",
            "is_blocked": initially_blocked,
            "blocking_reason": initial_audit.blocking_reason,
            "missing_critical_count": initial_audit.critical_missing_count
        }

        # Step 5: Autonomous Self-Healing Retrieval
        self_healed_items: List[EvidenceItem] = []
        investigation_trace = []
        if initially_blocked and initial_audit.missing_requirements:
            self_healed_items, investigation_trace = self.retriever.investigate(
                request, initial_audit.missing_requirements
            )
            dossier.extend(self_healed_items)

        trace["steps"]["step5_self_healing"] = {
            "status": "COMPLETED",
            "self_healed_count": len(self_healed_items),
            "self_healed_items": [item.model_dump() for item in self_healed_items],
            "investigation_trace": investigation_trace
        }

        # Re-audit after self-healing
        post_heal_audit: CompletenessAuditReport = self.auditor.audit(requirements, dossier)
        trace["steps"]["post_heal_audit"] = {
            "completeness_score": post_heal_audit.completeness_score,
            "is_complete": post_heal_audit.is_complete,
            "missing_count": post_heal_audit.missing_count,
            "audit_items": post_heal_audit.items
        }

        # Step 6: Precision Human-in-the-Loop
        hitl_prompt: Optional[HITLRequest] = None
        human_provided_items: List[EvidenceItem] = []

        if not post_heal_audit.is_complete:
            hitl_prompt = self.hitl.generate_micro_request(
                request, post_heal_audit.missing_requirements, dossier
            )

            if hitl_prompt and auto_resolve_hitl:
                # Fulfill the human request
                target_req = post_heal_audit.missing_requirements[0]
                resolved_item = self.hitl.resolve_gap(
                    target_req=target_req,
                    action_chosen=hitl_action,
                    user_notes=f"Authorized under enterprise delegation of authority policy.",
                    user_identity=reviewer_name
                )
                if resolved_item:
                    human_provided_items.append(resolved_item)
                    dossier.append(resolved_item)

        trace["steps"]["step6_hitl"] = {
            "status": "RESOLVED" if human_provided_items else ("PENDING_HUMAN" if hitl_prompt else "NOT_NEEDED"),
            "hitl_prompt": hitl_prompt.model_dump() if hitl_prompt else None,
            "human_resolved": len(human_provided_items) > 0,
            "human_items": [item.model_dump() for item in human_provided_items]
        }

        # Re-audit final dossier
        final_audit: CompletenessAuditReport = self.auditor.audit(requirements, dossier)
        trace["final_completeness"] = {
            "completeness_score": final_audit.completeness_score,
            "is_complete": final_audit.is_complete,
            "audit_items": final_audit.items
        }

        # Step 7: Deliberation & Action Execution
        decision_result: DecisionExecutionResult = self.decider.deliberate(
            request, requirements, dossier
        )
        trace["steps"]["step7_verdict"] = {
            "status": "COMPLETED",
            "verdict": decision_result.verdict.value,
            "confidence_score": decision_result.confidence_score,
            "recommendation": decision_result.recommendation,
            "executive_summary": decision_result.executive_summary,
            "reasoning_chain": decision_result.reasoning_chain,
            "risk_assessment": decision_result.risk_assessment,
            "actions_executed": decision_result.actions_executed,
            "audit_trail": decision_result.audit_trail
        }

        # Step 8: Telemetry & Meta-Learning
        self_healed_ids = [item.requirement_id for item in self_healed_items]
        hitl_ids = [item.requirement_id for item in human_provided_items]
        self.analytics.record_decision(
            request_id=request.id,
            domain=request.domain,
            title=request.title,
            initially_blocked=initially_blocked,
            initial_missing=initial_missing_ids,
            self_healed=self_healed_ids,
            required_hitl=hitl_ids
        )

        metrics = self.analytics.get_summary_metrics()
        recommendations = self.analytics.generate_recommendations()

        trace["steps"]["step8_meta_learning"] = {
            "status": "COMPLETED",
            "metrics": metrics,
            "insights": [rec.model_dump() for rec in recommendations]
        }

        return trace
