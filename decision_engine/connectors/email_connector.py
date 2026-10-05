"""
Email Archive & Mailbox Connector.
Simulates searching Gmail and Microsoft 365 Exchange mailboxes for quotes,
supplier correspondences, executive approvals, and references.
"""

from typing import List, Dict, Any
from .base import BaseConnector


class EmailConnector(BaseConnector):
    def __init__(self):
        super().__init__(name="Corporate Mailbox Archive (Gmail/M365)", source_type="EMAIL_ARCHIVE")
        self.emails = [
            {
                "id": "email-8821",
                "thread_id": "thread-procure-laptop-q4",
                "subject": "Re: Competitive Quotations - Laptop Hardware Refresh (50 Units)",
                "sender": "r.chen@hardware-distribution.com",
                "to": "procurement@company.internal",
                "date": "2026-09-28T14:32:00Z",
                "keywords": ["quote", "price comparison", "benchmark", "discount", "competitive pricing"],
                "body": "Hi Procurement Team, Attached is our formal benchmark sheet comparing ByteCraft Dell XPS-15 packages ($1,700/unit), Lenovo ThinkPad T16 ($1,780/unit), and HP EliteBook ($1,850/unit). ByteCraft includes 3-year on-site next-business-day warranty, yielding an 8.2% cost advantage under bulk threshold.",
                "has_attachment": True,
                "attachment_name": "Q4_Enterprise_Hardware_Benchmark_Matrix.xlsx",
                "confidence": 0.95
            },
            {
                "id": "email-9014",
                "thread_id": "thread-exec-hiring-rostova",
                "subject": "Executive Reference Feedback: Dr. Elena Rostova",
                "sender": "marcus.vance@former-employer-cloudscale.io",
                "to": "talent-leadership@company.internal",
                "date": "2026-09-18T10:15:00Z",
                "keywords": ["reference feedback", "past manager", "executive reference", "recommendation"],
                "body": "Elena was our VP of Cloud Infrastructure for 4 years. She scaled our Kubernetes fleet to 15,000 nodes with 99.995% uptime and reduced AWS spending by $4.2M. Strong cultural leader, zero reservations in re-hiring her for any top engineering post.",
                "has_attachment": False,
                "confidence": 0.97
            },
            {
                "id": "email-7731",
                "thread_id": "thread-claim-auth-ortho",
                "subject": "Pre-Authorization Confirmation: Patient ID #49102 - TKA Surgery",
                "sender": "approvals@national-health-care.org",
                "to": "billing@stjude-hospital.org",
                "date": "2026-08-30T11:00:00Z",
                "keywords": ["prior authorization", "auth letter", "pa-", "pre-authorization"],
                "body": "Prior authorization #PA-9938210 approved for Total Knee Arthroplasty (CPT 27447) with in-network prosthetic devices. Valid for admission window Sept 1 - Sept 30, 2026.",
                "has_attachment": True,
                "attachment_name": "Auth_Letter_PA9938210.pdf",
                "confidence": 0.98
            },
            {
                "id": "email-5512",
                "thread_id": "thread-apex-credit-wire",
                "subject": "Apex Retail LLC - Commercial Merchant Statement & Cash Flow",
                "sender": "treasury@apexretailgroup.com",
                "to": "commercial-lending@fintechbank.com",
                "date": "2026-09-10T16:20:00Z",
                "keywords": ["bank statements", "merchant cash flow", "average monthly deposits", "operating ledger"],
                "body": "Dear Credit Underwriting, Attached find our trailing 12-month merchant processing statements and operating bank records verifying average monthly gross deposits of $350,000+ with zero overdraft events.",
                "has_attachment": True,
                "attachment_name": "Apex_Operating_Ledger_12M.pdf",
                "confidence": 0.94
            },
            {
                "id": "email-6102",
                "thread_id": "thread-zurich-exec-dinner",
                "subject": "Zurich Strategic Client Briefing & Executive Dinner Attendee Roster",
                "sender": "jordan.bell@company.internal",
                "to": "field-finance@company.internal",
                "date": "2026-09-17T18:00:00Z",
                "keywords": ["attendee roster", "business purpose", "client dinner", "guest list", "offsite agenda"],
                "body": "Attached is the confirmed client dinner roster for Sept 14 at The Dolder Grand: 8 verified enterprise delegates from UBS, Credit Suisse/UBS Group, and Swisscom attending the Q4 AI core banking modernization roundtable.",
                "has_attachment": True,
                "attachment_name": "Zurich_Client_Roster_Signed.pdf",
                "confidence": 0.96
            },
            {
                "id": "email-6103",
                "thread_id": "thread-vectorflow-contract",
                "subject": "Executed VectorFlow DPA & Signed Zero-Model-Training Guarantee",
                "sender": "legal@vectorflow.ai",
                "to": "legal-contracts@company.internal",
                "date": "2026-09-22T11:45:00Z",
                "keywords": ["dpa", "data processing agreement", "standard contractual clauses", "gdpr", "zero retention", "model training rider"],
                "body": "Dear Legal Counsel, Attached please find our countersigned Data Processing Addendum (EU SCCs 2021/914) along with Schedule B guaranteeing zero retention of customer queries and binding covenant that customer prompt data is permanently excluded from model fine-tuning.",
                "has_attachment": True,
                "attachment_name": "VectorFlow_DPA_ZeroRetention_Executed.pdf",
                "confidence": 0.98
            },
            {
                "id": "email-6104",
                "thread_id": "thread-firewall-rollback",
                "subject": "Security Review: Automated Rollback Script & 48h TTL Rule for Port 9443",
                "sender": "devops-automation@company.internal",
                "to": "secops-alerts@company.internal",
                "date": "2026-09-29T14:10:00Z",
                "keywords": ["rollback script", "ttl alarm", "automated teardown", "terraform script"],
                "body": "Terraform change PR #4092 merged and dry-run verified. Contains AWS EventBridge rule 'banking-ingress-ttl-48h' that automatically revokes ingress security group rule on Port 9443 at 48:00:00 without requiring manual intervention.",
                "has_attachment": False,
                "confidence": 0.97
            },
            {
                "id": "email-6105",
                "thread_id": "thread-thorne-mortgage",
                "subject": "Dr. Aris Thorne - 2024 & 2025 W-2 Transcripts + Employer VOE",
                "sender": "underwriting-docs@mortgageflow.org",
                "to": "jumbo-processing@fintechbank.com",
                "date": "2026-09-25T09:30:00Z",
                "keywords": ["w-2", "wage transcripts", "voe", "employment verification", "salary history"],
                "body": "Attached find borrower verified IRS W-2 transcripts for 2024 ($385,000) and 2025 ($420,000), plus written Verification of Employment from Dell Medical Center confirming tenure as Chief of Neuroradiology.",
                "has_attachment": True,
                "attachment_name": "Thorne_W2_Transcripts_VOE.pdf",
                "confidence": 0.98
            }
        ]

    def search(self, queries: List[str], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []
        clean_queries = [q.lower().strip() for q in queries if q]

        for email in self.emails:
            email_text = (email["subject"] + " " + email["body"] + " " + " ".join(email["keywords"])).lower()
            keyword_match = False

            for q in clean_queries:
                if q in email_text:
                    keyword_match = True
                    break
                q_words = [w for w in q.split() if len(w) > 2]
                matched_words = [w for w in q_words if w in email_text]
                required_words = len(q_words) if len(q_words) <= 2 else int(len(q_words) * 0.6)
                if len(matched_words) >= required_words and len(matched_words) > 0:
                    keyword_match = True
                    break

            if not keyword_match:
                continue

            # Context boost
            context_boost = 0.0
            for k, v in context.items():
                if isinstance(v, str) and len(v) > 3 and v.lower() in email_text:
                    context_boost += 0.1

            score = min(0.99, email["confidence"] + context_boost)
            results.append({
                "source_name": self.name,
                "source_type": self.source_type,
                "source_location": f"email://threads/{email['thread_id']}#{email['id']}",
                "title": email["subject"],
                "content_snippet": email["body"][:250] + ("..." if len(email["body"]) > 250 else ""),
                "confidence": round(score, 2),
                "metadata": {
                    "from": email["sender"],
                    "date": email["date"],
                    "attachment": email.get("attachment_name")
                }
            })

        return sorted(results, key=lambda x: x["confidence"], reverse=True)
