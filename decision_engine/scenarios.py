"""
Pre-configured realistic enterprise scenarios for demonstrating The Decision Completeness Engine.
Includes the canonical Laptop Vendor approval from the core concept document, plus lending, hiring, and healthcare.
"""

from typing import Dict, Any, List
from .models import DecisionRequest, EvidenceItem, EvidenceStatus, SourceType


def get_all_scenarios() -> Dict[str, Dict[str, Any]]:
    return {
        "vendor_procurement": {
            "id": "vendor_procurement",
            "name": "Vendor Approval: 50 Developer Laptops ($85,000)",
            "domain": "procurement",
            "badge": "Canonical Example",
            "description": "Approve ByteCraft Solutions for supplying 50 high-performance engineering laptops. Request has basic pricing and delivery info, but lacks security certification and executive budget signoff.",
            "request": DecisionRequest(
                id="REQ-PROC-8842",
                title="Approve ByteCraft Solutions for 50 Developer Laptops ($85,000)",
                domain="procurement",
                requester="Marcus Sterling (Lead Systems Architect)",
                department="Engineering Infrastructure",
                summary="Urgent Q4 hardware refresh for 50 high-performance developer laptops. Vendor quote is $85,000 ($1,700/unit) with 3-year warranty.",
                urgency="HIGH",
                context_data={
                    "vendor_name": "ByteCraft Solutions",
                    "amount": 85000,
                    "item_category": "Laptops & Developer Hardware",
                    "units": 50,
                    "cost_center": "CC-4010-IT-INFRA"
                },
                initial_documents=[
                    {"name": "ByteCraft_Dell_Hardware_Quote_Q4.pdf", "type": "quote"},
                    {"name": "Delivery_Schedule_Commitment.pdf", "type": "sla"}
                ]
            ),
            "initial_evidence": [
                EvidenceItem(
                    requirement_id="PRICE_BENCHMARK",
                    requirement_name="Competitive Price Benchmarking",
                    status=EvidenceStatus.VERIFIED,
                    source_type=SourceType.INITIAL_DOSSIER,
                    source_location="intake://attachments/ByteCraft_Dell_Hardware_Quote_Q4.pdf",
                    summary="Formal quote of $1,700/unit verified against standard catalog rate ($1,850/unit), demonstrating 8.2% cost reduction under enterprise bulk pricing tier.",
                    confidence=0.95
                ),
                EvidenceItem(
                    requirement_id="DELIVERY_SLA",
                    requirement_name="Delivery Timeline & SLA Commitment",
                    status=EvidenceStatus.VERIFIED,
                    source_type=SourceType.INITIAL_DOSSIER,
                    source_location="intake://attachments/Delivery_Schedule_Commitment.pdf",
                    summary="Committed delivery SLA of 10 business days from PO receipt with 3-year next-business-day on-site replacement warranty.",
                    confidence=0.92
                )
            ]
        },
        "commercial_lending": {
            "id": "commercial_lending",
            "name": "Commercial Credit Facility: Apex Retail ($250,000)",
            "domain": "lending",
            "badge": "FinTech / Banking",
            "description": "Commercial revolving credit line application. Missing certified tax returns and operating bank records. Engine searches Drive and Email archives to locate IRS Form 1120-S and 12-month deposit statements.",
            "request": DecisionRequest(
                id="REQ-LEND-4921",
                title="Apex Retail LLC - $250k Revolving Inventory Credit Line",
                domain="lending",
                requester="David Cho (Senior Commercial Loan Officer)",
                department="Commercial Underwriting",
                summary="Merchant credit line request for holiday inventory build-up. Applicant is a multi-unit specialty retailer operating across Texas.",
                urgency="NORMAL",
                context_data={
                    "borrower_name": "Apex Retail LLC",
                    "amount": 250000,
                    "facility_type": "Revolving Line of Credit",
                    "term_months": 24
                },
                initial_documents=[
                    {"name": "Apex_Credit_Application_Form.pdf", "type": "application"}
                ]
            ),
            "initial_evidence": [
                EvidenceItem(
                    requirement_id="CREDIT_BORROWER_HISTORY",
                    requirement_name="Historical Credit Performance & DPD Records",
                    status=EvidenceStatus.VERIFIED,
                    source_type=SourceType.INITIAL_DOSSIER,
                    source_location="intake://attachments/Apex_Credit_Application_Form.pdf",
                    summary="Clean historical credit record verified via internal ledger: 2 prior loans fully paid off with zero late payments (0 DPD).",
                    confidence=0.96
                )
            ]
        },
        "executive_hiring": {
            "id": "executive_hiring",
            "name": "Executive Offer: VP of Engineering ($220,000 + Equity)",
            "domain": "hiring",
            "badge": "Talent & HR",
            "description": "Executive hiring decision for Dr. Elena Rostova. Interview scores are present, but background screening and supervisory references are missing from candidate folder.",
            "request": DecisionRequest(
                id="REQ-HIRE-1092",
                title="Extend VP Engineering Offer to Dr. Elena Rostova",
                domain="hiring",
                requester="Priya Nair (VP of Talent Acquisition)",
                department="People & Executive Recruiting",
                summary="Proposed offer for VP Engineering: $220k base + 0.8% equity grant. Hiring team completed loop with stellar marks.",
                urgency="HIGH",
                context_data={
                    "candidate_name": "Dr. Elena Rostova",
                    "role": "VP of Engineering",
                    "base_salary": 220000,
                    "level": "Executive (E9)"
                },
                initial_documents=[
                    {"name": "Interview_Loop_Scorecard_Summary.pdf", "type": "evaluation"}
                ]
            ),
            "initial_evidence": [
                EvidenceItem(
                    requirement_id="TECHNICAL_PORTFOLIO_ASSESSMENT",
                    requirement_name="Structured Leadership & Technical Assessment",
                    status=EvidenceStatus.VERIFIED,
                    source_type=SourceType.INITIAL_DOSSIER,
                    source_location="intake://attachments/Interview_Loop_Scorecard_Summary.pdf",
                    summary="Unanimous 4.8 / 5.0 score across 5-panel executive interview loop (Architecture, Culture, Scaled Org Leadership, Strategy).",
                    confidence=0.98
                )
            ]
        },
        "healthcare_claim": {
            "id": "healthcare_claim",
            "name": "Insurance Claim: Knee Arthroplasty Reimbursement ($42,000)",
            "domain": "healthcare",
            "badge": "Healthcare & Claims",
            "description": "High-value inpatient orthopedic surgery claim. Billing code submitted, but operative clinical notes and prior authorization are missing from the claim intake file.",
            "request": DecisionRequest(
                id="REQ-CLAIM-7712",
                title="St. Jude Hospital - TKA Surgery Claim Reimbursement ($42,000)",
                domain="healthcare",
                requester="Claims Processing Specialist #402",
                department="Claims Adjudication",
                summary="Hospital inpatient claim for Total Knee Arthroplasty (CPT 27447) with modular implant system. Patient ID #49102.",
                urgency="NORMAL",
                context_data={
                    "provider": "Dr. Robert Mercer, MD",
                    "facility": "St. Jude Orthopedic Center",
                    "amount": 42000,
                    "cpt_code": "27447",
                    "patient_id": "49102"
                },
                initial_documents=[
                    {"name": "UB04_Hospital_Billing_Form.pdf", "type": "invoice"}
                ]
            ),
            "initial_evidence": []
        },
        "corporate_expense": {
            "id": "corporate_expense",
            "name": "Expense Reimbursement: Zurich Executive Dinner ($14,200)",
            "domain": "expense",
            "badge": "Finance & Audit",
            "description": "Executive travel & client dinner reimbursement. Missing itemized Swiss VAT folio and client attendee list. Engine recovers folio and client roster from Drive & Email archives.",
            "request": DecisionRequest(
                id="REQ-EXP-9912",
                title="Jordan Bell - Zurich Client Roundtable & Hotel Reimbursement ($14,200)",
                domain="expense",
                requester="Jordan Bell (VP Enterprise Sales)",
                department="Global Sales & Field Operations",
                summary="Multi-day client briefing dinners in Zurich with UBS and Swisscom enterprise delegates. Total claim: $14,200 (CHF 13,193).",
                urgency="NORMAL",
                context_data={
                    "claimant": "Jordan Bell",
                    "amount": 14200,
                    "currency": "USD",
                    "destination": "Zurich, Switzerland",
                    "trip_type": "Executive Client Development"
                },
                initial_documents=[
                    {"name": "Amex_Monthly_Statement_Summary.pdf", "type": "statement"}
                ]
            ),
            "initial_evidence": [
                EvidenceItem(
                    requirement_id="PER_DIEM_POLICY_CHECK",
                    requirement_name="Corporate Travel & Per-Diem Compliance Audit",
                    status=EvidenceStatus.VERIFIED,
                    source_type=SourceType.INITIAL_DOSSIER,
                    source_location="intake://attachments/Amex_Monthly_Statement_Summary.pdf",
                    summary="Lodging and executive dining verified in line with high-cost tier city allowance; flagged for secondary approval due to exceeding $10,000 threshold.",
                    confidence=0.94
                )
            ]
        },
        "legal_contract": {
            "id": "legal_contract",
            "name": "AI SaaS Contract: VectorFlow Enterprise DPA ($120,000/yr)",
            "domain": "legal",
            "badge": "Legal & Privacy",
            "description": "Third-party customer service AI platform agreement. Missing cross-border Data Processing Addendum and AI Zero-Retention guarantee. Engine recovers signed DPA and model opt-out covenant from Email archives.",
            "request": DecisionRequest(
                id="REQ-LEGAL-3810",
                title="VectorFlow AI - Enterprise Customer AI Platform SaaS ($120k/yr)",
                domain="legal",
                requester="Maya Lin (VP of Customer Success)",
                department="Customer Experience & AI Ops",
                summary="Procurement of customer support AI agent platform. Annual recurring license of $120,000 with SLA guarantees.",
                urgency="HIGH",
                context_data={
                    "vendor": "VectorFlow AI Technologies Inc.",
                    "amount": 120000,
                    "contract_type": "Enterprise SaaS & DPA",
                    "data_classification": "Restricted Customer PII"
                },
                initial_documents=[
                    {"name": "VectorFlow_Master_Services_Agreement_Draft.pdf", "type": "contract"}
                ]
            ),
            "initial_evidence": [
                EvidenceItem(
                    requirement_id="CYBER_INSURANCE_CERTIFICATE",
                    requirement_name="Certificate of Cyber Liability Insurance ($5M+)",
                    status=EvidenceStatus.VERIFIED,
                    source_type=SourceType.INITIAL_DOSSIER,
                    source_location="intake://attachments/VectorFlow_Master_Services_Agreement_Draft.pdf",
                    summary="ACORD certificate confirms $10,000,000 technology E&O and Cyber risk liability policy active through Dec 2027.",
                    confidence=0.97
                )
            ]
        },
        "firewall_exemption": {
            "id": "firewall_exemption",
            "name": "Cloud Security: Core Banking Port 9443 Ingress Exception",
            "domain": "infra",
            "badge": "DevOps & SecOps",
            "description": "Production firewall rule exemption to allow external migration partner access on Port 9443. Engine discovers mutual TLS client certificate and automated 48-hour EventBridge rollback script.",
            "request": DecisionRequest(
                id="REQ-SEC-5501",
                title="Temporary Ingress Rule: Open Port 9443 for Core Banking Bridge",
                domain="infra",
                requester="Tariq Mansoor (Principal DevOps Engineer)",
                department="Cloud Platform & SRE",
                summary="Emergency 48-hour ingress allowance from dedicated partner datacenter to migration cluster on Port 9443.",
                urgency="CRITICAL",
                context_data={
                    "port": 9443,
                    "protocol": "TCP / mTLS",
                    "target_cluster": "k8s-prod-banking-core",
                    "max_duration_hours": 48
                },
                initial_documents=[
                    {"name": "Partner_Network_CIDR_Specification.pdf", "type": "network_spec"}
                ]
            ),
            "initial_evidence": [
                EvidenceItem(
                    requirement_id="STATIC_CIDR_WHITELIST",
                    requirement_name="Static Partner CIDR / IP Whitelist Validation",
                    status=EvidenceStatus.VERIFIED,
                    source_type=SourceType.INITIAL_DOSSIER,
                    source_location="intake://attachments/Partner_Network_CIDR_Specification.pdf",
                    summary="Source IP confirmed restricted to single dedicated static corporate partner /29 subnet (198.51.100.32/29).",
                    confidence=0.99
                )
            ]
        },
        "jumbo_mortgage": {
            "id": "jumbo_mortgage",
            "name": "Jumbo Real Estate Loan: $850k (Dr. Aris Thorne)",
            "domain": "mortgage",
            "badge": "Real Estate & Lending",
            "description": "Non-conforming residential home loan ($850,000). Missing independent property appraisal and trailing W-2 transcripts. Engine searches Drive & Email to recover Fannie Mae Form 1004 ($1.15M valuation, 73.9% LTV) and 2-year IRS transcripts.",
            "request": DecisionRequest(
                id="REQ-MORT-8819",
                title="Dr. Aris Thorne - $850k Jumbo Residential Purchase Financing",
                domain="mortgage",
                requester="Laura Chen (Senior Underwriting Specialist)",
                department="Mortgage Credit Underwriting",
                summary="30-year fixed jumbo residential purchase loan for property in Austin TX. Purchase price $1,150,000, loan amount $850,000.",
                urgency="NORMAL",
                context_data={
                    "borrower": "Dr. Aris Thorne",
                    "amount": 850000,
                    "property_value": 1150000,
                    "property_type": "Single Family Residence",
                    "loan_type": "30-Year Fixed Jumbo"
                },
                initial_documents=[
                    {"name": "Preliminary_Title_Commitment_Binder.pdf", "type": "title"}
                ]
            ),
            "initial_evidence": [
                EvidenceItem(
                    requirement_id="TITLE_INSURANCE_COMMITMENT",
                    requirement_name="Preliminary Title Report & Clean Title Commitment",
                    status=EvidenceStatus.VERIFIED,
                    source_type=SourceType.INITIAL_DOSSIER,
                    source_location="intake://attachments/Preliminary_Title_Commitment_Binder.pdf",
                    summary="First American Title binder confirms fee simple title with clean ownership history and zero adverse encumbrances or judicial liens.",
                    confidence=0.98
                )
            ]
        }
    }


def get_scenario(scenario_id: str) -> Dict[str, Any]:
    scenarios = get_all_scenarios()
    return scenarios.get(scenario_id, scenarios["vendor_procurement"])
