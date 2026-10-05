"""
The Decision Completeness Engine (DCE) Package.
An AI framework that checks whether it has enough information to make a decision
before making it, and goes to find whatever is missing.
"""

from .models import (
    DecisionRequest,
    EvidenceRequirement,
    EvidenceItem,
    EvidenceStatus,
    ImportanceLevel,
    DecisionVerdict,
    SourceType,
    CompletenessAuditReport,
    HITLRequest,
    DecisionExecutionResult,
    ProcessImprovementInsight
)
from .planner import EvidencePlanner
from .auditor import EvidenceAuditor
from .retriever import AutonomousRetriever
from .hitl import PrecisionHITL
from .decider import DecisionDeliberator
from .analytics import ProcessAnalyticsEngine
from .orchestrator import DecisionCompletenessEngine
from .scenarios import get_all_scenarios, get_scenario

__version__ = "1.0.0"

__all__ = [
    "DecisionCompletenessEngine",
    "DecisionRequest",
    "EvidenceRequirement",
    "EvidenceItem",
    "EvidenceStatus",
    "ImportanceLevel",
    "DecisionVerdict",
    "SourceType",
    "CompletenessAuditReport",
    "HITLRequest",
    "DecisionExecutionResult",
    "ProcessImprovementInsight",
    "EvidencePlanner",
    "EvidenceAuditor",
    "AutonomousRetriever",
    "PrecisionHITL",
    "DecisionDeliberator",
    "ProcessAnalyticsEngine",
    "get_all_scenarios",
    "get_scenario",
]
