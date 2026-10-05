"""
ERP & Financial Ledger Connector.
Simulates querying enterprise databases (SAP, NetSuite, Workday, QuickBooks)
for transaction history, remaining budget pools, and supplier fulfillment metrics.
"""

from typing import List, Dict, Any
from .base import BaseConnector


class ERPConnector(BaseConnector):
    def __init__(self):
        super().__init__(name="Enterprise ERP & Financial Ledger (NetSuite/SAP)", source_type="ERP_LEDGER")
        self.records = [
            {
                "id": "erp-vendor-bytecraft",
                "entity": "ByteCraft Solutions",
                "table": "vendors_master",
                "keywords": ["vendor history", "on-time delivery", "dispute count", "duns", "paydex", "fulfillment rate", "vendor reliability"],
                "data": {
                    "vendor_id": "VEND-8109",
                    "status": "APPROVED_TIER_2",
                    "historical_orders_count": 8,
                    "total_spend_ytd": "$142,500",
                    "on_time_delivery_rate": "98.4%",
                    "defect_rate": "0.12%",
                    "payment_terms": "Net 30",
                    "dispute_count": 0
                },
                "summary": "ByteCraft Solutions (VEND-8109): 8 completed historical POs totaling $142,500. On-time delivery rate 98.4%, defect rate 0.12%, zero active disputes.",
                "confidence": 0.99
            },
            {
                "id": "erp-borrower-apex",
                "entity": "Apex Retail LLC",
                "table": "commercial_borrowers",
                "keywords": ["credit history", "prior loans", "dpd max", "internal rating", "delinquency"],
                "data": {
                    "account_id": "COMM-7721",
                    "prior_loans_count": 2,
                    "repaid_in_full": True,
                    "days_past_due_max": 0,
                    "internal_credit_score": "A- (740 eq)"
                },
                "summary": "Apex Retail LLC: 2 previous credit facilities fully settled with 0 days past due. Internal rating A-.",
                "confidence": 0.98
            }
        ]

    def search(self, queries: List[str], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []
        clean_queries = [q.lower().strip() for q in queries if q]

        for record in self.records:
            rec_text = (record["entity"] + " " + record["summary"] + " " + " ".join(record["keywords"])).lower()
            keyword_match = False

            for q in clean_queries:
                q_words = [w for w in q.split() if len(w) > 2]
                matched_words = [w for w in q_words if w in rec_text]
                if len(matched_words) >= 1:
                    keyword_match = True
                    break

            if not keyword_match:
                continue

            context_boost = 0.0
            for k, v in context.items():
                if isinstance(v, str) and len(v) > 3 and v.lower() in rec_text:
                    context_boost += 0.1

            score = min(0.99, record["confidence"] + context_boost)
            results.append({
                "source_name": self.name,
                "source_type": self.source_type,
                "source_location": f"erp://{record['table']}/{record['id']}",
                "title": f"ERP Record: {record['entity']} ({record['table']})",
                "content_snippet": record["summary"],
                "confidence": round(score, 2),
                "metadata": record["data"]
            })

        return sorted(results, key=lambda x: x["confidence"], reverse=True)
