"""
Data models and schemas for The Decision Completeness Engine (DCE).
Enforces structured evidence tracking, gatekeeping, and audit trails.
"""

from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field


class ImportanceLevel(str, Enum):
    CRITICAL = "CRITICAL"      # Cannot proceed without this; non-negotiable
    MANDATORY = "MANDATORY"    # Required for positive approval
    RECOMMENDED = "RECOMMENDED" # Strengthens confidence; human can override
    OPTIONAL = "OPTIONAL"      # Nice to have


class EvidenceStatus(str, Enum):
    VERIFIED = "VERIFIED"          # Verified in initial dossier
    SELF_HEALED = "SELF_HEALED"    # Recovered autonomously from sources
    HUMAN_PROVIDED = "HUMAN_PROVIDED" # Supplied via precision HITL
    MISSING = "MISSING"            # Not found anywhere
    REJECTED = "REJECTED"          # Found but invalid / expired / failed check


class DecisionVerdict(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ESCALATED = "ESCALATED"
    BLOCKED = "BLOCKED"            # Incomplete evidence; halted at gate


class SourceType(str, Enum):
    INITIAL_DOSSIER = "INITIAL_DOSSIER"
    GOOGLE_DRIVE = "GOOGLE_DRIVE"
    EMAIL_ARCHIVE = "EMAIL_ARCHIVE"
    ERP_LEDGER = "ERP_LEDGER"
    WEB_REGISTRY = "WEB_REGISTRY"
    HUMAN_INPUT = "HUMAN_INPUT"


class EvidenceRequirement(BaseModel):
    """Specification of a single required piece of evidence inferred dynamically by the AI."""
    id: str = Field(..., description="Unique identifier for this requirement (e.g. SOC2_COMPLIANCE)")
    name: str = Field(..., description="Human readable title")
    description: str = Field(..., description="Detailed description of what constitutes valid evidence")
    category: str = Field("General", description="Category: Financial, Compliance, Operational, Security, Legal")
    importance: ImportanceLevel = Field(ImportanceLevel.MANDATORY, description="Criticality of requirement")
    query_hints: List[str] = Field(default_factory=list, description="Keywords and queries to locate this item in sources")
    validation_rule: Optional[str] = Field(None, description="Criteria for valid evidence (e.g., valid until > 2026, signed by VP)")


class EvidenceItem(BaseModel):
    """An actual verified piece of evidence collected by the engine."""
    requirement_id: str
    requirement_name: str
    status: EvidenceStatus = EvidenceStatus.VERIFIED
    source_type: SourceType = SourceType.INITIAL_DOSSIER
    source_location: str = Field(..., description="Pointer to source (e.g., 'email://thread-9821' or 'drive://docs/soc2.pdf')")
    summary: str = Field(..., description="Extracted facts and verified payload")
    confidence: float = Field(1.0, ge=0.0, le=1.0, description="Confidence in authenticity and relevance (0.0 to 1.0)")
    verified_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DecisionRequest(BaseModel):
    """The incoming decision request payload."""
    id: str
    title: str
    domain: str = Field(..., description="Domain: procurement, lending, hiring, healthcare, compliance")
    requester: str
    department: str
    summary: str
    urgency: str = "NORMAL"
    context_data: Dict[str, Any] = Field(default_factory=dict)
    initial_documents: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class CompletenessAuditReport(BaseModel):
    """Gap analysis produced after auditing evidence against requirements."""
    is_complete: bool
    completeness_score: float = Field(..., ge=0.0, le=100.0, description="Percentage score 0-100%")
    total_requirements: int
    verified_count: int
    missing_count: int
    critical_missing_count: int
    items: List[Dict[str, Any]] = Field(default_factory=list)
    missing_requirements: List[EvidenceRequirement] = Field(default_factory=list)
    blocking_reason: Optional[str] = None


class HITLRequest(BaseModel):
    """Precision Human-in-the-Loop targeted request."""
    request_id: str
    target_role: str
    target_email: str
    summary_context: str
    verified_summary: str
    missing_item_name: str
    missing_item_description: str
    specific_action_required: str
    options: List[str] = Field(default_factory=lambda: ["Approve / Confirm", "Upload Document", "Reject Request"])
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class DecisionExecutionResult(BaseModel):
    """Final decision outcome and execution trace."""
    decision_id: str
    request_id: str
    verdict: DecisionVerdict
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    recommendation: str
    executive_summary: str
    reasoning_chain: List[str] = Field(default_factory=list)
    risk_assessment: Dict[str, Any] = Field(default_factory=dict)
    evidence_dossier: List[EvidenceItem] = Field(default_factory=list)
    actions_executed: List[Dict[str, Any]] = Field(default_factory=list)
    audit_trail: List[Dict[str, Any]] = Field(default_factory=list)
    completed_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class ProcessImprovementInsight(BaseModel):
    """Meta-learning insight to fix systemic intake bottlenecks."""
    insight_id: str
    domain: str
    pattern_observed: str
    block_frequency_pct: float
    impact_level: str  # HIGH, MEDIUM, LOW
    root_cause: str
    suggested_action: str
    estimated_turnaround_improvement: str
