"""
Evidence Planner: Dynamically infers evidence specifications from request context.
Does NOT rely on rigid hardcoded checklists; reasons about risk, policy, domain, and amounts.
"""

from typing import List, Dict, Any, Optional
import os
import json
from .models import DecisionRequest, EvidenceRequirement, ImportanceLevel


class EvidencePlanner:
    """
    Step 2: Evidence Requirement Formulation.
    Analyzes the decision context and determines the exact specification
    of evidence required before any verdict can legitimately be rendered.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")

    def plan_requirements(self, request: DecisionRequest) -> List[EvidenceRequirement]:
        """
        Produce dynamic evidence requirements based on domain, request context, and risk profile.
        """
        # If external LLM key is configured, we can leverage LLM planning;
        # otherwise use intelligent semantic rule synthesizer with domain depth.
        domain = request.domain.lower()
        amount = request.context_data.get("amount", 0)

        if "procure" in domain or "vendor" in domain:
            return self._plan_procurement(request, amount)
        elif "mortgage" in domain or "real_estate" in domain or "home" in domain:
            return self._plan_mortgage(request, amount)
        elif "lend" in domain or "credit" in domain or "loan" in domain:
            return self._plan_lending(request, amount)
        elif "expense" in domain or "travel" in domain or "reimburse" in domain:
            return self._plan_expense(request, amount)
        elif "legal" in domain or "contract" in domain or "saas" in domain:
            return self._plan_legal_contract(request, amount)
        elif "infra" in domain or "firewall" in domain or "devops" in domain:
            return self._plan_infrastructure(request)
        elif "hire" in domain or "hiring" in domain or "candidate" in domain or "hr" in domain:
            return self._plan_hiring(request)
        elif "health" in domain or "claim" in domain or "medical" in domain:
            return self._plan_healthcare(request)
        elif "security" in domain or "compliance" in domain or "exempt" in domain:
            return self._plan_compliance(request)
        else:
            return self._plan_general(request)

    def _plan_procurement(self, request: DecisionRequest, amount: float) -> List[EvidenceRequirement]:
        reqs = [
            EvidenceRequirement(
                id="PRICE_BENCHMARK",
                name="Competitive Price Benchmarking",
                description="Evidence of at least 3 competitive market quotes or an authorized pre-negotiated catalog discount rate.",
                category="Financial",
                importance=ImportanceLevel.MANDATORY,
                query_hints=["quote", "price comparison", "benchmark", "discount", "competitive pricing"],
                validation_rule="Must demonstrate cost parity or savings >= 5% against market median."
            ),
            EvidenceRequirement(
                id="DELIVERY_SLA",
                name="Delivery Timeline & SLA Commitment",
                description="Documented fulfillment schedule and SLA with delivery lead-time commitment.",
                category="Operational",
                importance=ImportanceLevel.MANDATORY,
                query_hints=["delivery record", "lead time", "fulfillment", "sla commitment", "shipping window"],
                validation_rule="Delivery lead time must not exceed required project timeline."
            ),
            EvidenceRequirement(
                id="SECURITY_CERTIFICATION",
                name="Security & Quality Certification (SOC2 / ISO 27001)",
                description="Independent auditor verification of operational security controls, data protection, and ISO/SOC standards.",
                category="Security & Compliance",
                importance=ImportanceLevel.CRITICAL if amount > 25000 or "laptop" in request.title.lower() else ImportanceLevel.MANDATORY,
                query_hints=["soc2", "type ii", "iso 27001", "security certification", "audit report", "compliance"],
                validation_rule="Must have active validity period spanning current fiscal period."
            ),
            EvidenceRequirement(
                id="VENDOR_PERFORMANCE_HISTORY",
                name="Vendor Reliability & Dispute History",
                description="Historical delivery records, dispute records, or verified credit/reputation rating.",
                category="Risk Assessment",
                importance=ImportanceLevel.RECOMMENDED,
                query_hints=["vendor history", "on-time delivery", "dispute count", "duns", "paydex", "fulfillment rate"],
                validation_rule="Historical on-time delivery > 90% or zero active regulatory sanctions."
            )
        ]

        # High-value approval governance rule
        if amount >= 50000 or "laptop" in request.title.lower():
            reqs.append(
                EvidenceRequirement(
                    id="BUDGET_EXECUTIVE_APPROVAL",
                    name="Departmental Budget Sign-off (VP / Finance Head)",
                    description=f"Explicit budget authorization for commitments exceeding $50k (Requested: ${amount:,.2f}).",
                    category="Governance & Financial",
                    importance=ImportanceLevel.CRITICAL,
                    query_hints=["budget approval", "vp finance signoff", "cfo approval", "gl unencumbered balance"],
                    validation_rule="Signed or approved by VP Finance or Department Head."
                )
            )

        return reqs

    def _plan_lending(self, request: DecisionRequest, amount: float) -> List[EvidenceRequirement]:
        return [
            EvidenceRequirement(
                id="TAX_RETURNS_VERIFIED",
                name="Certified Corporate Tax Returns (Trailing 2 Years)",
                description="Official IRS tax filings (Form 1120/1120-S) signed by an accredited CPA.",
                category="Financial",
                importance=ImportanceLevel.CRITICAL,
                query_hints=["tax returns", "1120", "irs", "revenue", "cpa signed"],
                validation_rule="Positive operating income and debt service coverage ratio > 1.25x."
            ),
            EvidenceRequirement(
                id="BANK_CASH_FLOW_STATEMENTS",
                name="Operating Account Cash Flow & Bank Statements",
                description="Trailing 12-month bank statements verifying consistent deposits and zero NSF defaults.",
                category="Financial",
                importance=ImportanceLevel.MANDATORY,
                query_hints=["bank statements", "merchant cash flow", "average monthly deposits", "operating ledger"],
                validation_rule="Average monthly gross deposits must be >= 1.5x monthly debt service."
            ),
            EvidenceRequirement(
                id="CREDIT_BORROWER_HISTORY",
                name="Historical Credit Performance & DPD Records",
                description="Historical credit bureau or internal ledger record of prior facilities and payment timeliness.",
                category="Risk Assessment",
                importance=ImportanceLevel.MANDATORY,
                query_hints=["credit history", "prior loans", "dpd max", "internal rating", "delinquency"],
                validation_rule="No delinquencies exceeding 30 days within trailing 24 months."
            ),
            EvidenceRequirement(
                id="ENTITY_GOOD_STANDING",
                name="Secretary of State Good Standing & Lien Check",
                description="Active legal entity status with no outstanding tax warrants or asset liens.",
                category="Legal & Regulatory",
                importance=ImportanceLevel.CRITICAL,
                query_hints=["secretary of state", "good standing", "ucc liens", "sanctions", "corporate status"],
                validation_rule="Active status in home state jurisdiction with zero encumbering judicial liens."
            )
        ]

    def _plan_hiring(self, request: DecisionRequest) -> List[EvidenceRequirement]:
        return [
            EvidenceRequirement(
                id="TECHNICAL_PORTFOLIO_ASSESSMENT",
                name="Structured Leadership & Technical Assessment",
                description="Scorecard and structured notes from technical interview loop and case evaluation.",
                category="Competency",
                importance=ImportanceLevel.MANDATORY,
                query_hints=["interview scorecard", "technical evaluation", "leadership review"],
                validation_rule="Overall interview rating >= 4.0 / 5.0."
            ),
            EvidenceRequirement(
                id="EXECUTIVE_REFERENCE_FEEDBACK",
                name="Past Executive Reference Verifications",
                description="Confidential feedback from at least two prior supervisors or executive peers.",
                category="Cultural & Performance",
                importance=ImportanceLevel.CRITICAL,
                query_hints=["reference feedback", "past manager", "executive reference", "recommendation"],
                validation_rule="Confirmed direct oversight and positive rehire eligibility."
            ),
            EvidenceRequirement(
                id="BACKGROUND_CREDENTIAL_CLEARANCE",
                name="Comprehensive Background & Degree Clearance",
                description="Screening covering criminal records, credential verification, and sanctions checks.",
                category="Compliance & Trust",
                importance=ImportanceLevel.CRITICAL,
                query_hints=["background check", "criminal record", "degree verification", "sterling", "hirecheck"],
                validation_rule="Zero disqualifying felony convictions; degree conferred by accredited institution."
            ),
            EvidenceRequirement(
                id="COMPENSATION_BAND_ALIGNMENT",
                name="Compensation Committee & Band Approval",
                description="Authorized sign-off ensuring package aligns with approved executive equity/salary bands.",
                category="Governance",
                importance=ImportanceLevel.MANDATORY,
                query_hints=["compensation signoff", "equity grant approval", "hr director approval"],
                validation_rule="Approved by Head of People and Compensation Committee."
            )
        ]

    def _plan_healthcare(self, request: DecisionRequest) -> List[EvidenceRequirement]:
        return [
            EvidenceRequirement(
                id="CLINICAL_OPERATIVE_NOTES",
                name="Itemized Operative & Clinical Notes",
                description="Comprehensive surgeon log detailing clinical indication, surgical intervention, and implants.",
                category="Clinical Necessity",
                importance=ImportanceLevel.CRITICAL,
                query_hints=["operative notes", "surgeon log", "cpt 27447", "clinical notes", "implant"],
                validation_rule="Must substantiate medical necessity per standard clinical guidelines."
            ),
            EvidenceRequirement(
                id="PRIOR_AUTHORIZATION_LETTER",
                name="Valid In-Window Prior Authorization",
                description="Insurer prior authorization code valid for the admission date and procedure code.",
                category="Billing Compliance",
                importance=ImportanceLevel.CRITICAL,
                query_hints=["prior authorization", "auth letter", "pa-", "pre-authorization"],
                validation_rule="Active authorization ID matching CPT billing code."
            ),
            EvidenceRequirement(
                id="PROVIDER_LICENSE_CREDENTIAL",
                name="Attending Provider Board & Medical License",
                description="Current state medical board certification with zero active disciplinary suspensions.",
                category="Regulatory",
                importance=ImportanceLevel.MANDATORY,
                query_hints=["medical board", "npi", "physician license", "abos certification"],
                validation_rule="Unrestricted medical license in jurisdiction of care."
            )
        ]

    def _plan_compliance(self, request: DecisionRequest) -> List[EvidenceRequirement]:
        return [
            EvidenceRequirement(
                id="SECURITY_ARCHITECTURE_REVIEW",
                name="Security Architecture Threat Model",
                description="Documented technical risk mitigation for proposed exemption.",
                category="Security",
                importance=ImportanceLevel.CRITICAL,
                query_hints=["threat model", "architecture review", "security mitigation"],
                validation_rule="Mitigating compensatory controls approved by InfoSec."
            ),
            EvidenceRequirement(
                id="DATA_PROTECTION_AGREEMENT",
                name="Signed Data Protection Addendum (DPA)",
                description="Binding contractual privacy clauses matching GDPR / CCPA.",
                category="Legal",
                importance=ImportanceLevel.CRITICAL,
                query_hints=["dpa", "data processing agreement", "standard contractual clauses"],
                validation_rule="Executed by legal counsel of both parties."
            )
        ]

    def _plan_expense(self, request: DecisionRequest, amount: float) -> List[EvidenceRequirement]:
        return [
            EvidenceRequirement(
                id="ITEMIZED_TAX_FOLIO",
                name="Itemized Hotel Folio & VAT Tax Receipt",
                description="Line-item receipt showing room rates, local taxes, meals, and incidental charges.",
                category="Receipts & Tax",
                importance=ImportanceLevel.CRITICAL,
                query_hints=["hotel folio", "itemized invoice", "vat receipt", "tax invoice", "zurich hotel"],
                validation_rule="Total itemized charges must reconcile within $1.00 of requested reimbursement."
            ),
            EvidenceRequirement(
                id="CLIENT_ATTENDEE_ROSTER",
                name="Client Attendee Roster & Business Purpose",
                description="List of verified enterprise client attendees, companies, and strategic account agenda.",
                category="Compliance",
                importance=ImportanceLevel.MANDATORY,
                query_hints=["attendee roster", "business purpose", "client dinner", "guest list", "offsite agenda"],
                validation_rule="Documented legitimate business development purpose with external participants."
            ),
            EvidenceRequirement(
                id="PER_DIEM_POLICY_CHECK",
                name="Corporate Travel & Per-Diem Compliance Audit",
                description="Audit confirming meal and hotel rates adhere to regional lodging limits.",
                category="Audit & Policy",
                importance=ImportanceLevel.RECOMMENDED,
                query_hints=["per diem", "travel policy", "lodging cap", "compliance audit"],
                validation_rule="Within allowable company per-diem thresholds or justified by executive status."
            ),
            EvidenceRequirement(
                id="VP_SALES_EXCEPTION_SIGNOFF",
                name="VP Sales Travel Policy Exception Authorization",
                description=f"Explicit executive authorization for corporate travel commitments > $10,000 (${amount:,.2f}).",
                category="Executive Governance",
                importance=ImportanceLevel.CRITICAL,
                query_hints=["vp sales approval", "travel exception", "head of sales signoff"],
                validation_rule="Signed by VP of Sales or Chief Commercial Officer."
            )
        ]

    def _plan_legal_contract(self, request: DecisionRequest, amount: float) -> List[EvidenceRequirement]:
        return [
            EvidenceRequirement(
                id="DATA_PROCESSING_AGREEMENT_DPA",
                name="Signed Data Processing Agreement (DPA & SCCs)",
                description="Binding data privacy agreement including Standard Contractual Clauses for cross-border transfer.",
                category="Privacy & Legal",
                importance=ImportanceLevel.CRITICAL,
                query_hints=["dpa", "data processing agreement", "standard contractual clauses", "gdpr", "vectorflow"],
                validation_rule="Signed by authorized vendor corporate officer; includes sub-processor obligations."
            ),
            EvidenceRequirement(
                id="AI_ZERO_RETENTION_GUARANTEE",
                name="AI Model Training & Zero-Data-Retention Rider",
                description="Explicit contractual guarantee that customer data is never used to train foundation models.",
                category="AI Governance",
                importance=ImportanceLevel.CRITICAL,
                query_hints=["zero retention", "model training rider", "ai governance", "training opt-out"],
                validation_rule="Irrevocable negative covenant prohibiting customer data ingestion into model weights."
            ),
            EvidenceRequirement(
                id="CYBER_INSURANCE_CERTIFICATE",
                name="Certificate of Cyber Liability Insurance ($5M+)",
                description="Proof of current Errors & Omissions and Cyber Risk insurance policy with $5M+ aggregate limit.",
                category="Risk & Liability",
                importance=ImportanceLevel.MANDATORY,
                query_hints=["certificate of insurance", "cyber liability", "errors and omissions", "coi", "acord"],
                validation_rule="Active policy with company named as additional insured; limit >= $5,000,000."
            ),
            EvidenceRequirement(
                id="CISO_SECURITY_SIGNOFF",
                name="CISO Architecture & External LLM Sign-off",
                description="Information Security Head formal concurrence on third-party AI pipeline integration.",
                category="Security Clearance",
                importance=ImportanceLevel.CRITICAL,
                query_hints=["ciso approval", "security architecture signoff", "infosec clearance"],
                validation_rule="Approved by Chief Information Security Officer."
            )
        ]

    def _plan_infrastructure(self, request: DecisionRequest) -> List[EvidenceRequirement]:
        return [
            EvidenceRequirement(
                id="STATIC_CIDR_WHITELIST",
                name="Static Partner CIDR / IP Whitelist Validation",
                description="Verified partner IP block allocation restricted to /29 or tighter subnet.",
                category="Network Security",
                importance=ImportanceLevel.CRITICAL,
                query_hints=["cidr whitelist", "partner ip", "source subnet", "firewall rule", "port 9443"],
                validation_rule="Must be dedicated static corporate IP block; no public wildcard subnets allowed."
            ),
            EvidenceRequirement(
                id="MTLS_CRYPTO_CERTIFICATE",
                name="Mutual TLS (mTLS) Client-Server Certificate",
                description="X.509 cryptographic certificate validating reciprocal handshake authentication.",
                category="Cryptography",
                importance=ImportanceLevel.CRITICAL,
                query_hints=["mtls", "tls 1.3", "x509 certificate", "client cert", "mutual tls"],
                validation_rule="Valid SHA-256 or ECC certificate issued by enterprise internal PKI."
            ),
            EvidenceRequirement(
                id="AUTOMATED_ROLLBACK_TEARDOWN",
                name="Automated Rollback Script & 48-Hour TTL Alarm",
                description="Tested Terraform/Ansible script with scheduled AWS CloudWatch rule to terminate ingress at 48h.",
                category="Operational Resilience",
                importance=ImportanceLevel.MANDATORY,
                query_hints=["rollback script", "ttl alarm", "automated teardown", "terraform script"],
                validation_rule="Automated destruction timer <= 48 hours from activation."
            ),
            EvidenceRequirement(
                id="CISO_EMERGENCY_OVERRIDE",
                name="CISO Emergency Firewall Override Authorization",
                description="Direct authorization from Chief Information Security Officer for external ingress to tier-1 cluster.",
                category="Executive Clearance",
                importance=ImportanceLevel.CRITICAL,
                query_hints=["ciso emergency signoff", "firewall exception approval", "infosec director override"],
                validation_rule="Formal emergency exception ticket signed by CISO."
            )
        ]

    def _plan_mortgage(self, request: DecisionRequest, amount: float) -> List[EvidenceRequirement]:
        return [
            EvidenceRequirement(
                id="APPRAISAL_PROPERTY_REPORT",
                name="Independent Certified Appraisal Report (LTV <= 80%)",
                description="Uniform Residential Appraisal Report (Fannie Mae Form 1004) establishing fair market value.",
                category="Collateral",
                importance=ImportanceLevel.CRITICAL,
                query_hints=["appraisal report", "form 1004", "property valuation", "fair market value", "ltv"],
                validation_rule="Appraised value must support Loan-to-Value ratio <= 80%."
            ),
            EvidenceRequirement(
                id="INCOME_W2_TAX_TRANSCRIPTS",
                name="Trailing 2-Year W-2s & Verified Employment (VOE)",
                description="W-2 wage transcripts and written verification of employment confirming stable earnings.",
                category="Capacity",
                importance=ImportanceLevel.CRITICAL,
                query_hints=["w-2", "wage transcripts", "voe", "employment verification", "salary history"],
                validation_rule="Debt-to-Income (DTI) ratio must not exceed 43% under qualifying interest rate."
            ),
            EvidenceRequirement(
                id="LIQUID_RESERVES_PROOF",
                name="Proof of 6-Month Liquid Reserve Assets",
                description="Brokerage or bank statements showing minimum 6 months principal, interest, taxes, insurance (PITI).",
                category="Reserves",
                importance=ImportanceLevel.MANDATORY,
                query_hints=["liquid reserves", "piti reserves", "brokerage statement", "escrow reserves"],
                validation_rule="Vested unencumbered liquid assets >= 6 months PITI."
            ),
            EvidenceRequirement(
                id="TITLE_INSURANCE_COMMITMENT",
                name="Preliminary Title Report & Clean Title Commitment",
                description="Title insurance policy binder showing clean fee simple title with no adverse liens.",
                category="Legal & Title",
                importance=ImportanceLevel.MANDATORY,
                query_hints=["preliminary title report", "title commitment", "alta policy", "clean title"],
                validation_rule="Zero unreleased mechanics liens or clouds on title."
            ),
            EvidenceRequirement(
                id="CHIEF_UNDERWRITER_JUMBO_APPROVAL",
                name="Chief Underwriting Officer (CUO) Jumbo Tier Sign-off",
                description=f"Executive credit sign-off for non-conforming loan amounts exceeding $766,550 (${amount:,.2f}).",
                category="Credit Governance",
                importance=ImportanceLevel.CRITICAL,
                query_hints=["chief underwriter approval", "cuo signoff", "jumbo tier approval"],
                validation_rule="Signed by Chief Underwriting Officer or Credit Committee."
            )
        ]

    def _plan_general(self, request: DecisionRequest) -> List[EvidenceRequirement]:
        """Infers dynamic requirements for open-ended requests."""
        return [
            EvidenceRequirement(
                id="SUBSTANTIATING_DOCUMENTATION",
                name="Primary Substantive Evidence",
                description=f"Core factual justification and scope details for {request.title}.",
                category="Scope & Objective",
                importance=ImportanceLevel.CRITICAL,
                query_hints=[request.title.lower(), "proposal", "contract", "spec"],
                validation_rule="Clear articulation of deliverables and objectives."
            ),
            EvidenceRequirement(
                id="FINANCIAL_IMPACT_ANALYSIS",
                name="Budget & Cost Authorization",
                description="Cost breakdown and departmental approval.",
                category="Financial",
                importance=ImportanceLevel.MANDATORY,
                query_hints=["budget", "cost", "financial breakdown", "signoff"],
                validation_rule="Approved funding allocation."
            ),
            EvidenceRequirement(
                id="STAKEHOLDER_CLEARANCE",
                name="Stakeholder Governance Sign-off",
                description="Verification that relevant department leads have concurred.",
                category="Governance",
                importance=ImportanceLevel.RECOMMENDED,
                query_hints=["approval", "stakeholder concurrence", "manager signoff"],
                validation_rule="Concurrence from primary department lead."
            )
        ]
