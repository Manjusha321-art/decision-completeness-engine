"""
Gap Auditor and Completeness Gatekeeper.
Step 3 & Step 4: Audits what evidence exists, computes completeness score,
and explicitly blocks decisions when critical evidence is missing.
"""

from typing import List, Dict, Any, Tuple
from .models import (
    EvidenceRequirement,
    EvidenceItem,
    EvidenceStatus,
    ImportanceLevel,
    CompletenessAuditReport
)


class EvidenceAuditor:
    """
    Audits the current dossier against the inferred requirements.
    Calculates completeness score and enforces the decision gate:
    Refuses to decide if any critical or mandatory evidence is absent.
    """

    def audit(
        self,
        requirements: List[EvidenceRequirement],
        dossier: List[EvidenceItem]
    ) -> CompletenessAuditReport:
        items_map: Dict[str, EvidenceItem] = {
            item.requirement_id: item for item in dossier if item.status != EvidenceStatus.REJECTED
        }

        audit_items = []
        missing_requirements = []
        verified_count = 0
        critical_missing_count = 0

        # Weighted scoring based on importance
        weight_sum = 0.0
        earned_sum = 0.0

        weight_table = {
            ImportanceLevel.CRITICAL: 3.0,
            ImportanceLevel.MANDATORY: 2.0,
            ImportanceLevel.RECOMMENDED: 1.0,
            ImportanceLevel.OPTIONAL: 0.5,
        }

        for req in requirements:
            w = weight_table.get(req.importance, 1.0)
            weight_sum += w

            matched_item = items_map.get(req.id)
            if matched_item:
                verified_count += 1
                earned_sum += w * matched_item.confidence
                audit_items.append({
                    "requirement_id": req.id,
                    "requirement_name": req.name,
                    "category": req.category,
                    "importance": req.importance.value,
                    "status": matched_item.status.value,
                    "found": True,
                    "source": matched_item.source_type.value,
                    "source_location": matched_item.source_location,
                    "summary": matched_item.summary,
                    "confidence": matched_item.confidence,
                })
            else:
                audit_items.append({
                    "requirement_id": req.id,
                    "requirement_name": req.name,
                    "category": req.category,
                    "importance": req.importance.value,
                    "status": EvidenceStatus.MISSING.value,
                    "found": False,
                    "source": None,
                    "source_location": None,
                    "summary": "Evidence not located in initial dossier.",
                    "confidence": 0.0,
                })
                missing_requirements.append(req)
                if req.importance in (ImportanceLevel.CRITICAL, ImportanceLevel.MANDATORY):
                    critical_missing_count += 1

        completeness_pct = (earned_sum / weight_sum * 100.0) if weight_sum > 0 else 0.0
        completeness_pct = round(completeness_pct, 1)

        is_complete = (critical_missing_count == 0)

        blocking_reason = None
        if not is_complete:
            missing_names = [f"'{r.name}' ({r.importance.value})" for r in missing_requirements if r.importance in (ImportanceLevel.CRITICAL, ImportanceLevel.MANDATORY)]
            blocking_reason = (
                f"DECISION GATE ENGAGED: Blocked from proceeding to verdict. "
                f"{critical_missing_count} required evidence item(s) absent: {', '.join(missing_names)}. "
                f"Autonomous self-healing search initiated."
            )

        return CompletenessAuditReport(
            is_complete=is_complete,
            completeness_score=completeness_pct,
            total_requirements=len(requirements),
            verified_count=verified_count,
            missing_count=len(missing_requirements),
            critical_missing_count=critical_missing_count,
            items=audit_items,
            missing_requirements=missing_requirements,
            blocking_reason=blocking_reason
        )
