"""
Autonomous Multi-Source Investigation & Self-Healing Agent.
Step 5: When a decision is blocked due to missing evidence, this agent
autonomously traverses corporate repositories (Drive, Email, ERP, Registry)
to locate, extract, and verify missing documents and records.
"""

from typing import List, Dict, Any, Tuple
from .models import (
    EvidenceRequirement,
    EvidenceItem,
    EvidenceStatus,
    SourceType,
    DecisionRequest
)
from .connectors import BaseConnector, get_default_connectors


class AutonomousRetriever:
    """
    Step 5: Investigates connected data sources to self-heal evidence gaps.
    """

    def __init__(self, connectors: List[BaseConnector] = None):
        self.connectors = connectors or get_default_connectors()

    def investigate(
        self,
        request: DecisionRequest,
        missing_requirements: List[EvidenceRequirement]
    ) -> Tuple[List[EvidenceItem], List[Dict[str, Any]]]:
        """
        Attempts to discover evidence for each missing requirement.
        Returns:
          - recovered_items: List of new EvidenceItem objects
          - investigation_trace: Detailed log of searches and discoveries
        """
        recovered_items: List[EvidenceItem] = []
        investigation_trace: List[Dict[str, Any]] = []

        context_hints = {
            "title": request.title,
            "department": request.department,
            "requester": request.requester,
            **request.context_data
        }

        for req in missing_requirements:
            req_trace = {
                "requirement_id": req.id,
                "requirement_name": req.name,
                "importance": req.importance.value,
                "queries_executed": req.query_hints,
                "sources_searched": [],
                "recovered": False,
                "discovered_item": None
            }

            best_candidate = None
            best_connector = None

            for connector in self.connectors:
                search_log = {
                    "source_name": connector.name,
                    "source_type": connector.source_type,
                    "hits_found": 0
                }

                candidates = connector.search(req.query_hints, context_hints)
                search_log["hits_found"] = len(candidates)
                req_trace["sources_searched"].append(search_log)

                if candidates:
                    top_hit = candidates[0]
                    if best_candidate is None or top_hit["confidence"] > best_candidate["confidence"]:
                        best_candidate = top_hit
                        best_connector = connector

            # If candidate satisfies confidence threshold (>= 0.70)
            if best_candidate and best_candidate["confidence"] >= 0.70:
                recovered_item = EvidenceItem(
                    requirement_id=req.id,
                    requirement_name=req.name,
                    status=EvidenceStatus.SELF_HEALED,
                    source_type=SourceType(best_candidate["source_type"]),
                    source_location=best_candidate["source_location"],
                    summary=f"Autonomously recovered via {best_candidate['source_name']}: {best_candidate['content_snippet']}",
                    confidence=round(best_candidate["confidence"], 2),
                    metadata=best_candidate.get("metadata", {})
                )
                recovered_items.append(recovered_item)
                req_trace["recovered"] = True
                req_trace["discovered_item"] = {
                    "source_name": best_candidate["source_name"],
                    "source_location": best_candidate["source_location"],
                    "title": best_candidate["title"],
                    "snippet": best_candidate["content_snippet"],
                    "confidence": best_candidate["confidence"]
                }

            investigation_trace.append(req_trace)

        return recovered_items, investigation_trace
