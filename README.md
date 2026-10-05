# The Decision Completeness Engine (DCE)

> **"An AI that checks whether it has enough information to make a decision *before* making it, and goes to find whatever is missing."**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Status: Production-Grade](https://img.shields.io/badge/status-production--ready-emerald.svg)]()
[![Zero-Hallucination Gate](https://img.shields.io/badge/gatekeeper-zero--hallucination-purple.svg)]()
[![n8n Ready](https://img.shields.io/badge/n8n-workflow--included-orange.svg)](file:///c:/Users/HP/Downloads/The%20Decision%20Completeness%20Engine/n8n/decision_completeness_engine.json)

---

## The Problem It Solves

Most enterprise AI systems ask: *"What should I decide?"*

If someone submits an approval request missing half the facts, standard generative AI will **confidently answer anyway**—hallucinating compliance, speculating on missing variables, and creating severe governance risk. Meanwhile, human teams waste days playing email ping-pong: *"Where's the certificate?"*, *"Did the VP sign off?"*

**The Decision Completeness Engine flips the paradigm:**
It asks first: ***"Do I have enough evidence to decide at all?"***

Like an expert physician who orders tests before diagnosing, the engine enforces a strict zero-hallucination decision gate, autonomously searches company repositories for missing records, and contacts humans only for the exact missing delta.

```
Request arrives
      ↓
[Step 2] AI infers required evidence dynamically (Not hardcoded)
      ↓
[Step 3 & 4] Audit dossier → Complete? ──No──→ 🚫 DECISION BLOCKED AT GATE!
      │                                                ↓
      │                                    [Step 5] Autonomous Search (Drive, Email, ERP)
      │                                                ↓
      │                                         Found? ──No──→ [Step 6] Precision HITL
      │                                                ↓ Yes            (Targeted Micro-Ask)
      └──Yes───────────────────────────────────────────┴───────────────────────┘
      ↓
[Step 7] AI deliberates verdict + calibrated confidence score + dispatches actions
      ↓
[Step 8] Meta-Learning: Analyzes telemetry → Identifies bottlenecks → Fixes intake process
```

---

## What Makes It Special (Core Superpowers)

1. **It Knows When NOT to Decide:** Refuses to guess or hallucinate when critical evidence is absent.
2. **Requirements Are Inferred, Not Hardcoded:** Understands domain, risk, policy, and financial scale to formulate dynamic evidence specifications.
3. **Autonomous Self-Healing:** Traverses Google Drive, email archives, ERP ledgers, and public registries to locate and verify missing documents on its own.
4. **Precision Human-in-the-Loop:** Never asks humans to *"re-review the whole 40-page dossier"*. Asks only the specific person for the exact missing item (e.g. *“Sarah: 4/5 items verified. Missing ONLY VP Finance budget sign-off. Click to approve.”*).
5. **Calibrated Confidence & Chain-of-Custody:** Every decision comes with a composite confidence score (0-100%) and an auditable reasoning chain linking to source citations.
6. **Continuous Meta-Learning:** Aggregates blocker patterns (e.g. *“71% of requests get blocked on budget approval”*) and generates concrete workflow re-engineering proposals.

---

## Repository Structure

```
The Decision Completeness Engine/
├── app.py                     # Interactive Flask Web Studio & REST API
├── cli.py                     # High-performance Command Line Interface
├── DEMO_SCRIPT.md             # 3-Minute High-Impact Pitch & Demo Script
├── N8N_GUIDE.md               # Node-by-Node n8n Implementation Guide
├── README.md                  # Comprehensive Documentation & Architecture
│
├── decision_engine/           # Core Modular Engine Package
│   ├── __init__.py
│   ├── models.py              # Pydantic Schemas (Requests, EvidenceSpecs, Dossiers, Verdicts)
│   ├── planner.py             # Step 2: Dynamic Evidence Planner
│   ├── auditor.py             # Step 3 & 4: Gap Auditor & Gatekeeper
│   ├── retriever.py           # Step 5: Multi-Source Autonomous Investigation Agent
│   ├── hitl.py                # Step 6: Precision Human-in-the-Loop Coordinator
│   ├── decider.py             # Step 7: Deliberation, Reasoning & Action Dispatcher
│   ├── analytics.py           # Step 8: Telemetry, Pattern Mining & Meta-Learning
│   ├── scenarios.py           # Pre-loaded Enterprise Scenarios
│   ├── orchestrator.py        # Master 8-Step Pipeline Orchestrator
│   └── connectors/            # Pluggable Enterprise Source Connectors
│       ├── base.py
│       ├── drive_connector.py # Google Drive Document Vault
│       ├── email_connector.py # Corporate Gmail / Exchange Threads
│       ├── erp_connector.py   # NetSuite / SAP / GL Financial Ledger
│       └── registry_connector.py # D&B, OFAC Sanctions, Secretary of State
│
├── templates/
│   └── index.html             # Sleek Dark-Mode Single Page Visual Studio
│
├── static/
│   ├── css/custom.css         # Glassmorphism, animations & status badges
│   ├── js/app.js              # Interactive UI controller & live stepper runner
│   └── n8n/                   # Downloadable workflow assets
│
├── n8n/                       # Production-Ready n8n Workflow Assets
│   ├── decision_completeness_engine.json # Importable n8n Workflow JSON
│   └── prompts/               # Production-Tuned LLM Prompts
│       ├── evidence_planner.prompt.txt
│       ├── gap_auditor.prompt.txt
│       └── verdict_synthesizer.prompt.txt
│
└── tests/
    └── test_engine.py         # Comprehensive Unit & Integration Test Suite
```

---

## Quickstart Guide

### 1. Launch the Visual Decision Studio
Run the web application:
```bash
python app.py
```
Open your browser at **`http://localhost:5000`**.
- Switch between real-world scenarios with 1 click.
- Click **Run Pipeline** to watch the 8-step execution live.
- Test the interactive **Precision HITL Modal** to approve, upload memos, or reject.
- Explore the **Knowledge Vault** and **Process Mining Dashboard**.

### 2. Run via Command Line Interface (CLI)
Execute full decision pipelines directly in your terminal:
```bash
# Run the canonical Laptop Fleet Procurement scenario
python cli.py run --scenario vendor_procurement --auto-approve

# Run commercial credit underwriting
python cli.py run --scenario commercial_lending --auto-approve

# View meta-learning analytics and process optimization recommendations
python cli.py analytics

# List all available scenarios
python cli.py scenarios
```

### 3. Run the Automated Test Suite
Verify that all 8 steps and gatekeeper mechanisms are operating flawlessly:
```bash
python -m unittest tests/test_engine.py
```

### 4. Deploy into n8n
Import [`n8n/decision_completeness_engine.json`](file:///c:/Users/HP/Downloads/The%20Decision%20Completeness%20Engine/n8n/decision_completeness_engine.json) directly into any n8n instance. See [`N8N_GUIDE.md`](file:///c:/Users/HP/Downloads/The%20Decision%20Completeness%20Engine/N8N_GUIDE.md) for full configuration details.

---

## Pre-Configured Enterprise Scenarios (8 Built-In Domains)

| Scenario | Domain | Context & Gaps | Autonomous Recovery |
|---|---|---|---|
| **Vendor Onboarding** *(Canonical)* | Procurement | 50 Developer Laptops ($85k). Has quotes & SLA, missing SOC2 & budget sign-off. | Recovers SOC2 Type II from Drive & delivery record from ERP. Triggers HITL for VP Finance sign-off. |
| **Merchant Credit Line** | FinTech / Lending | $250k revolving facility. Missing certified tax returns & 12M cash flow records. | Recovers Form 1120-S from Drive & 12-month deposit records from Email thread. |
| **VP of Engineering Offer** | Talent / HR | Executive hiring offer ($220k + equity). Missing background check & supervisory reference. | Recovers Sterling screening from Drive & former CTO reference letter from Email. |
| **Surgical Claim Adjudication** | Healthcare | $42k Knee Arthroplasty claim. Missing surgeon operative notes & prior authorization code. | Recovers operative clinical report from Drive & prior auth letter #PA-9938210 from Email. |
| **Executive Expense Reimbursement** | Finance & Audit | $14.2k Zurich client roundtable. Missing itemized VAT hotel folio & attendee list. | Recovers Dolder Grand hotel folio from Drive & verified client guest list from Email. |
| **AI SaaS Contract & DPA Review** | Legal & Privacy | $120k/yr customer support AI. Missing cross-border DPA & zero-retention guarantee. | Recovers countersigned EU SCCs DPA and model opt-out covenant from Email. |
| **Cloud Firewall Port Exemption** | DevOps & SecOps | Emergency 48h Port 9443 ingress for banking bridge. Missing mTLS cert & teardown alarm. | Recovers X.509 client certificate and automated 48-hour EventBridge rollback script. |
| **Jumbo Real Estate Mortgage** | Real Estate Lending | $850k residential purchase. Missing certified appraisal & trailing 2Y W-2 transcripts. | Recovers Fannie Mae Form 1004 appraisal ($1.15M valuation, 73.9% LTV) and IRS W-2 transcripts. |

---

## The 3-Minute Demo Script

Preparing to present to executives or investors? Check out [`DEMO_SCRIPT.md`](file:///c:/Users/HP/Downloads/The%20Decision%20Completeness%20Engine/DEMO_SCRIPT.md) for a word-for-word, timed walkthrough designed to create an instant "Aha!" moment.
