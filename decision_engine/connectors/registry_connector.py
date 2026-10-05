"""
External Registry & Regulatory Connector.
Simulates public corporate registries (Secretary of State, Companies House),
OFAC/Sanctions databases, Dun & Bradstreet risk reports, and state licensing boards.
"""

from typing import List, Dict, Any
from .base import BaseConnector


class RegistryConnector(BaseConnector):
    def __init__(self):
        super().__init__(name="External Regulatory & Registry API (D&B / OFAC / State Registry)", source_type="WEB_REGISTRY")
        self.registries = [
            {
                "id": "reg-bytecraft",
                "entity": "ByteCraft Solutions Inc.",
                "keywords": ["corporate status", "sanctions", "ofac", "good standing", "tax id", "duns", "paydex"],
                "data": {
                    "jurisdiction": "Delaware, USA (File #589210)",
                    "status": "ACTIVE_GOOD_STANDING",
                    "ofac_sanctions_check": "CLEARED_NO_MATCHES",
                    "duns_number": "08-992-1204",
                    "dnb_paydex_score": 84,
                    "last_verified": "2026-09-01"
                },
                "summary": "State of Delaware Corp Division: ByteCraft Solutions Inc. is in Good Standing. OFAC/SAM.gov Sanctions List: Cleared (Zero hits). Dun & Bradstreet Paydex: 84/100 (Low risk).",
                "confidence": 0.99
            },
            {
                "id": "reg-apex",
                "entity": "Apex Retail LLC",
                "keywords": ["secretary of state", "good standing", "ucc liens", "sanctions", "corporate status", "tax forfeiture"],
                "data": {
                    "jurisdiction": "Texas SOS (File #8023194)",
                    "status": "ACTIVE_IN_GOOD_STANDING",
                    "tax_forfeiture_check": "CLEARED",
                    "active_ucc_liens": "None outstanding against operating assets"
                },
                "summary": "Texas Secretary of State: Apex Retail LLC Active & Good Standing. No outstanding judicial liens or tax forfeitures recorded.",
                "confidence": 0.98
            },
            {
                "id": "reg-dr-mercer",
                "entity": "Dr. Robert Mercer, MD",
                "keywords": ["medical board", "npi", "physician license", "abos certification", "state board"],
                "data": {
                    "npi": "1942801923",
                    "state_board": "California Medical Board (#A14892)",
                    "board_certification": "American Board of Orthopaedic Surgery (ABOS)",
                    "disciplinary_actions": "NONE",
                    "expiration_date": "2027-11-30"
                },
                "summary": "National Provider Identifier (NPI 1942801923): Dr. Robert Mercer holds Active unrestricted license (CA Board #A14892) & ABOS Board Certification. Zero disciplinary sanctions.",
                "confidence": 0.99
            }
        ]

    def search(self, queries: List[str], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []
        clean_queries = [q.lower().strip() for q in queries if q]

        for reg in self.registries:
            reg_text = (reg["entity"] + " " + reg["summary"] + " " + " ".join(reg["keywords"])).lower()
            keyword_match = False

            for q in clean_queries:
                q_words = [w for w in q.split() if len(w) > 2]
                matched_words = [w for w in q_words if w in reg_text]
                if len(matched_words) >= 1:
                    keyword_match = True
                    break

            if not keyword_match:
                continue

            context_boost = 0.0
            for k, v in context.items():
                if isinstance(v, str) and len(v) > 3 and v.lower() in reg_text:
                    context_boost += 0.1

            score = min(0.99, reg["confidence"] + context_boost)
            results.append({
                "source_name": self.name,
                "source_type": self.source_type,
                "source_location": f"registry://sec_state/{reg['id']}",
                "title": f"Official Registry Verification: {reg['entity']}",
                "content_snippet": reg["summary"],
                "confidence": round(score, 2),
                "metadata": reg["data"]
            })

        return sorted(results, key=lambda x: x["confidence"], reverse=True)
