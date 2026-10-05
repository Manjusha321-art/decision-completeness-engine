"""
Precision Human-in-the-Loop (HITL) Orchestrator.
Step 6: When automated self-healing cannot locate a critical requirement,
this module generates an ultra-targeted micro-request asking a specific human
for ONLY the single missing item, rather than asking them to re-review the entire dossier.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from .models import (
    DecisionRequest,
    EvidenceRequirement,
    EvidenceItem,
    EvidenceStatus,
    SourceType,
    HITLRequest
)


class PrecisionHITL:
    """
    Step 6: Generates precision human requests for unresolved evidence gaps.
    """

    def generate_micro_request(
        self,
        request: DecisionRequest,
        remaining_missing: List[EvidenceRequirement],
        verified_items: List[EvidenceItem]
    ) -> Optional[HITLRequest]:
        if not remaining_missing:
            return None

        # Prioritize the most critical missing requirement
        target_req = remaining_missing[0]

        # Determine appropriate stakeholder role based on requirement category
        role, email = self._determine_stakeholder(request, target_req)

        # Build verified context summary
        verified_summary_parts = [
            f"✓ {item.requirement_name} ({item.source_type.value})"
            for item in verified_items
        ]
        verified_summary = "; ".join(verified_summary_parts) if verified_summary_parts else "No items pre-verified."

        specific_action = (
            f"Please review and confirm ONLY this item: '{target_req.name}'. "
            f"Criteria: {target_req.validation_rule or target_req.description}"
        )

        return HITLRequest(
            request_id=request.id,
            target_role=role,
            target_email=email,
            summary_context=(
                f"Intake '{request.title}' for {request.requester} ({request.department}) "
                f"has passed {len(verified_items)} automated evidence checks but requires human sign-off on 1 specific item."
            ),
            verified_summary=verified_summary,
            missing_item_name=target_req.name,
            missing_item_description=target_req.description,
            specific_action_required=specific_action,
            options=[
                f"Grant One-Click Approval for {target_req.name}",
                "Upload Signed Document / Evidence",
                "Reject Request / Deny Exception"
            ]
        )

    def _determine_stakeholder(self, request: DecisionRequest, req: EvidenceRequirement) -> tuple[str, str]:
        req_id = req.id.upper()
        if "SALES" in req_id or "TRAVEL" in req_id:
            return "VP of Global Enterprise Sales", "vp-sales@company.internal"
        elif "JUMBO" in req_id or "MORTGAGE" in req_id or "UNDERWRITER" in req_id:
            return "Chief Underwriting Officer (CUO)", "cuo@fintechmortgage.com"
        elif "FIREWALL" in req_id or "OVERRIDE" in req_id or "CISO" in req_id:
            return "Head of Information Security (CISO)", "ciso@company.internal"
        elif "BUDGET" in req_id or "FINANCE" in req_id:
            return "VP of Finance & Corporate Treasury", "vp-finance@company.internal"
        elif "SECURITY" in req_id or "COMPLIANCE" in req_id or "SOC2" in req_id:
            return "Head of Information Security (CISO)", "ciso@company.internal"
        elif "LEGAL" in req_id or "DPA" in req_id:
            return "General Counsel & Legal Affairs", "legal@company.internal"
        elif "CLINICAL" in req_id or "MEDICAL" in req_id:
            return "Chief Medical Director", "medical-director@healthcare.org"
        elif "CREDIT" in req_id or "TAX" in req_id:
            return "Chief Credit Underwriter", "underwriting@fintechbank.com"
        elif "COMPENSATION" in req_id or "HR" in req_id:
            return "Chief People Officer / Comp Committee", "cpo@company.internal"
        else:
            return "Department Operations Director", f"ops-director@{request.department.lower().replace(' ', '')}.internal"

    def resolve_gap(
        self,
        target_req: EvidenceRequirement,
        action_chosen: str,
        user_notes: str = "",
        user_identity: str = "Authorized Reviewer"
    ) -> Optional[EvidenceItem]:
        """
        Converts human resolution into an EvidenceItem that fulfills the requirement.
        """
        if "reject" in action_chosen.lower() or "deny" in action_chosen.lower():
            return EvidenceItem(
                requirement_id=target_req.id,
                requirement_name=target_req.name,
                status=EvidenceStatus.REJECTED,
                source_type=SourceType.HUMAN_INPUT,
                source_location=f"hitl://response/{user_identity}",
                summary=f"Human Reviewer ({user_identity}) explicitly denied/rejected this requirement: {user_notes or 'Declined by reviewer.'}",
                confidence=1.0,
                metadata={"action": action_chosen, "notes": user_notes, "reviewer": user_identity}
            )

        return EvidenceItem(
            requirement_id=target_req.id,
            requirement_name=target_req.name,
            status=EvidenceStatus.HUMAN_PROVIDED,
            source_type=SourceType.HUMAN_INPUT,
            source_location=f"hitl://signature/{user_identity}",
            summary=f"Direct sign-off granted by {user_identity}. Action: {action_chosen}. Notes: {user_notes or 'Verified and authorized.'}",
            confidence=1.0,
            metadata={"action": action_chosen, "notes": user_notes, "reviewer": user_identity}
        )
