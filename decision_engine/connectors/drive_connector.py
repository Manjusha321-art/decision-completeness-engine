"""
Corporate Google Drive / Document Vault Connector.
Simulates enterprise cloud storage with indexed PDF reports, certificates, and compliance filings.
"""

from typing import List, Dict, Any
from .base import BaseConnector


class DriveConnector(BaseConnector):
    def __init__(self):
        super().__init__(name="Corporate Google Drive Vault", source_type="GOOGLE_DRIVE")
        self.documents = [
            {
                "id": "doc-001",
                "title": "ByteCraft Solutions - SOC2 Type II Independent Audit Report.pdf",
                "folder": "Drive > Security & Compliance > Vendor Audits > 2025",
                "location": "gdrive://compliance/vendor_audits/ByteCraft_SOC2_Type2_2025.pdf",
                "keywords": ["soc2", "security", "bytecraft", "certification", "compliance", "type ii", "audit"],
                "content": "Independent Service Auditor's Report on Controls Relevant to Security, Availability, and Confidentiality. ByteCraft Solutions Inc. Period: Jan 1 2025 - Dec 31 2025. Verdict: Unqualified / Clean Opinion. Controls operating effectively. Valid through Dec 31, 2026.",
                "confidence": 0.96,
                "metadata": {
                    "auditor": "Deloitte & Touche LLP",
                    "valid_until": "2026-12-31",
                    "file_size": "2.4 MB",
                    "uploaded_by": "secops@company.internal"
                }
            },
            {
                "id": "doc-002",
                "title": "Apex Retail LLC - 2024 Corporate Tax Returns Form 1120-S.pdf",
                "folder": "Drive > Commercial Lending > Financial Dossiers > Apex",
                "location": "gdrive://finance/lending/Apex_Retail_TaxReturns_2024.pdf",
                "keywords": ["tax returns", "apex retail", "1120-s", "irs", "revenue", "cpa signed", "tax return"],
                "content": "IRS Form 1120-S U.S. Income Tax Return for an S Corporation. Tax Year 2024. Apex Retail LLC. Gross receipts: $4,210,000. Ordinary business income: $580,000. Verified signed by CPA Ronald Vance.",
                "confidence": 0.98,
                "metadata": {
                    "cpa": "Vance & Associates CPAs",
                    "tax_year": "2024",
                    "gross_revenue": "$4,210,000"
                }
            },
            {
                "id": "doc-003",
                "title": "Dr. Elena Rostova - Executive Background & Credential Verification Report.pdf",
                "folder": "Drive > Human Resources > Executive Search > Engineering",
                "location": "gdrive://hr/background_checks/Rostova_Elena_Sterling_Check.pdf",
                "keywords": ["background check", "criminal record", "degree verification", "sterling", "hirecheck", "rostova"],
                "content": "Sterling Executive Background Screening Report for Dr. Elena Rostova. Criminal Record: Clear. Employment Verification: 12 years verified (Senior Director at CloudScale). Degree Verification: PhD Computer Science, Carnegie Mellon verified.",
                "confidence": 0.99,
                "metadata": {
                    "agency": "Sterling Talent Solutions",
                    "status": "CLEAR_NO_RECORDS",
                    "completed_date": "2026-08-15"
                }
            },
            {
                "id": "doc-004",
                "title": "Orthopedic Surgery - Operative Notes & Surgeon Detailed Log.pdf",
                "folder": "Drive > Claims Administration > Clinical Records > 2026",
                "location": "gdrive://clinical/claims/surgery_op_notes_patient_49102.pdf",
                "keywords": ["operative notes", "surgeon log", "cpt 27447", "clinical notes", "implant", "mercer"],
                "content": "Operative Report: Total Knee Arthroplasty (CPT 27447). Surgeon: Dr. Robert Mercer, MD. Detailed implant ledger: Zimmer NexGen LPS Flex system. Pre-op diagnosis confirmed, intraoperative complications: none. Estimated blood loss: 120cc.",
                "confidence": 0.95,
                "metadata": {
                    "hospital": "St. Jude Orthopedic Center",
                    "physician": "Dr. Robert Mercer, MD",
                    "cpt_code": "27447"
                }
            },
            {
                "id": "doc-005",
                "title": "Global Cloud SLA & ISO 27001 Certificate - ByteCraft.pdf",
                "folder": "Drive > Procurement > Master Service Agreements",
                "location": "gdrive://procurement/msa/ByteCraft_ISO27001_2025.pdf",
                "keywords": ["iso27001", "iso 27001", "bytecraft", "sla", "certificate", "quality"],
                "content": "ISO/IEC 27001:2022 Certification granted to ByteCraft Solutions for Information Security Management Systems. Accredited by UKAS. Certificate valid until October 2027.",
                "confidence": 0.94,
                "metadata": {
                    "cert_authority": "BSI Group",
                    "expiry": "2027-10-15"
                }
            },
            {
                "id": "doc-006",
                "title": "The Dolder Grand Hotel Zurich - Itemized Folio & VAT Receipt.pdf",
                "folder": "Drive > Sales & Field Operations > Expense Receipts > 2026",
                "location": "gdrive://expenses/travel/Zurich_DolderGrand_ItemizedFolio_99182.pdf",
                "keywords": ["hotel folio", "itemized invoice", "vat receipt", "tax invoice", "zurich hotel"],
                "content": "Official Itemized Hotel Folio: The Dolder Grand, Zurich. Guest: Jordan Bell. Dates: Sept 12-16, 2026. Itemized breakdown: Executive Suite CHF 8,400, Private Salon Client Dinner CHF 3,850, VAT 7.7% CHF 943. Total: CHF 13,193 (USD $14,200 equivalent). Clean payment settled via Amex.",
                "confidence": 0.98,
                "metadata": {
                    "hotel": "The Dolder Grand Zurich",
                    "vat_verified": "7.7% Swiss MwSt verified",
                    "total_usd": "$14,200.00"
                }
            },
            {
                "id": "doc-007",
                "title": "VectorFlow AI - Certificate of Cyber Liability Insurance ($10M).pdf",
                "folder": "Drive > Legal & Compliance > Vendor Insurance Binders",
                "location": "gdrive://legal/insurance/VectorFlow_ACORD_Cyber_10M.pdf",
                "keywords": ["certificate of insurance", "cyber liability", "errors and omissions", "coi", "acord"],
                "content": "ACORD Certificate of Liability Insurance. Insured: VectorFlow AI Technologies Inc. Carrier: Chubb National Insurance. Coverage: Technology Errors & Omissions $10,000,000 Aggregate; Cyber Security & Privacy Breach $10,000,000. Customer named as Additional Insured. Policy period: Active through Dec 2027.",
                "confidence": 0.97,
                "metadata": {
                    "insurer": "Chubb National Insurance",
                    "aggregate_limit": "$10,000,000",
                    "status": "ACTIVE_ADDITIONAL_INSURED"
                }
            },
            {
                "id": "doc-008",
                "title": "Core Banking Ingress - Mutual TLS 1.3 Partner Client Certificate.crt",
                "folder": "Drive > Security Operations > PKI & Cryptographic Assets",
                "location": "gdrive://secops/pki/partner_core_banking_mtls_2026.crt",
                "keywords": ["mtls", "tls 1.3", "x509 certificate", "client cert", "mutual tls"],
                "content": "X.509 v3 Client Certificate issued by Enterprise Internal Root CA #2. Subject: CN=partner-banking-bridge.fintechcore.internal. Public Key: ECC prime256v1. Key Usage: Digital Signature, Key Encipherment, Client Authentication. Validity: Active through Oct 2027.",
                "confidence": 0.99,
                "metadata": {
                    "issuer": "Enterprise Internal PKI",
                    "algorithm": "ECDSA / TLS 1.3",
                    "fingerprint": "9A:7F:32:E1:8B:20"
                }
            },
            {
                "id": "doc-009",
                "title": "Dr. Aris Thorne - Uniform Residential Appraisal Report Form 1004.pdf",
                "folder": "Drive > Residential Lending > Collateral Files > Thorne",
                "location": "gdrive://underwriting/appraisals/Thorne_FannieMae_1004_Appraisal.pdf",
                "keywords": ["appraisal report", "form 1004", "property valuation", "fair market value", "ltv"],
                "content": "Uniform Residential Appraisal Report (Fannie Mae Form 1004). Subject Property: 742 Evergreen Ridge Way, Austin TX. Certified Appraiser: Robert Sterling, SRA. Determined Fair Market Value: $1,150,000. Loan amount requested: $850,000, yielding LTV ratio of 73.9% (well below 80.0% jumbo threshold).",
                "confidence": 0.98,
                "metadata": {
                    "appraised_value": "$1,150,000",
                    "loan_amount": "$850,000",
                    "computed_ltv": "73.9%"
                }
            }
        ]

    def search(self, queries: List[str], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []
        clean_queries = [q.lower().strip() for q in queries if q]

        for doc in self.documents:
            doc_text = (doc["title"] + " " + doc["content"] + " " + " ".join(doc["keywords"])).lower()
            keyword_match = False
            match_count = 0

            for q in clean_queries:
                if q in doc_text:
                    keyword_match = True
                    match_count += 2
                    break
                q_words = [w for w in q.split() if len(w) > 2]
                matched_words = [w for w in q_words if w in doc_text]
                required_words = len(q_words) if len(q_words) <= 2 else int(len(q_words) * 0.6)
                if len(matched_words) >= required_words and len(matched_words) > 0:
                    keyword_match = True
                    match_count += len(matched_words)
                    break

            if not keyword_match:
                continue

            # Context boost
            context_boost = 0.0
            for k, v in context.items():
                if isinstance(v, str) and len(v) > 3 and v.lower() in doc_text:
                    context_boost += 0.1

            score = min(0.99, doc["confidence"] + context_boost)
            results.append({
                "source_name": self.name,
                "source_type": self.source_type,
                "source_location": doc["location"],
                "title": doc["title"],
                "content_snippet": doc["content"],
                "confidence": round(score, 2),
                "metadata": doc["metadata"]
            })

        return sorted(results, key=lambda x: x["confidence"], reverse=True)
