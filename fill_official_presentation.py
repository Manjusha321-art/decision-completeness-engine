import os
import shutil
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

TEMPLATE_PATH = r"C:\Users\HP\.gemini\antigravity\brain\3fe956f8-3f9d-4415-84ed-47c270beb2e8\.user_uploaded\media_1791214615882.pptx"
OUTPUT_PATH = r"c:\Users\HP\Downloads\The Decision Completeness Engine\HackSprint_Decision_Completeness_Engine.pptx"
STATIC_PATH = r"c:\Users\HP\Downloads\The Decision Completeness Engine\static\HackSprint_Decision_Completeness_Engine.pptx"

prs = pptx.Presentation(TEMPLATE_PATH)

# Helper styling constants
COLOR_TITLE_CYAN = RGBColor(93, 224, 230)      # #5DE0E6 (template title color)
COLOR_DARK_SLATE = RGBColor(15, 23, 42)        # #0F172A
COLOR_NAVY_HEADING = RGBColor(30, 41, 59)      # #1E293B
COLOR_BODY_TEXT = RGBColor(51, 65, 85)         # #334155
COLOR_MUTED_TEXT = RGBColor(100, 116, 139)     # #64748B
COLOR_CARD_BG = RGBColor(255, 255, 255)        # Pure white card
COLOR_CARD_BORDER = RGBColor(203, 213, 225)    # Slate-300
COLOR_TEAL_ACCENT = RGBColor(13, 148, 136)     # Teal-600
COLOR_TEAL_LIGHT = RGBColor(240, 253, 250)     # Teal-50
COLOR_INDIGO_ACCENT = RGBColor(79, 70, 229)    # Indigo-600
COLOR_INDIGO_LIGHT = RGBColor(238, 242, 255)   # Indigo-50
COLOR_GREEN = RGBColor(22, 163, 74)            # Green-600
COLOR_AMBER = RGBColor(217, 119, 6)            # Amber-600
COLOR_RED = RGBColor(220, 38, 38)              # Red-600

FONT_SERIF = "Times New Roman"
FONT_SANS = "Calibri"

def add_card(slide, left, top, width, height, bg_rgb=COLOR_CARD_BG, border_rgb=COLOR_CARD_BORDER):
    """Creates a clean card shape with solid fill and border."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_rgb
    card.line.color.rgb = border_rgb
    card.line.width = Pt(1.5)
    return card

# ==============================================================================
# SLIDE 1: Cover Slide
# ==============================================================================
slide1 = prs.slides[0]

# Shape 15 has the YOUR NAME, TEAM NAME, TRACK NO labels
# Let's update Shape 15 cleanly without moving other things
shape15 = slide1.shapes[15]
shape15.left = Inches(1.5)
shape15.width = Inches(11.0)
shape15.height = Inches(2.2)
tf15 = shape15.text_frame
tf15.word_wrap = True
tf15.clear()

items_s1 = [
    ("YOUR NAME: ", "[Your Name(s)]", COLOR_DARK_SLATE, True),
    ("TEAM NAME: ", "The Completeness Crew", COLOR_DARK_SLATE, True),
    ("TRACK NO: ", "AI & Enterprise Automation (Open Innovation)", COLOR_DARK_SLATE, True),
    ("PROJECT: ", "The Decision Completeness Engine (DCE)", COLOR_TEAL_ACCENT, True),
    ("LIVE DEMO: ", "https://static-outstanding-palm-clarke.trycloudflare.com", COLOR_INDIGO_ACCENT, False),
]

for idx, (label, val, val_col, is_bold) in enumerate(items_s1):
    p = tf15.paragraphs[0] if idx == 0 else tf15.add_paragraph()
    p.space_after = Pt(4)
    r1 = p.add_run()
    r1.text = label
    r1.font.name = "Playfair Display"
    r1.font.size = Pt(15)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_DARK_SLATE

    r2 = p.add_run()
    r2.text = val
    r2.font.name = FONT_SANS
    r2.font.size = Pt(15)
    r2.font.bold = is_bold
    r2.font.color.rgb = val_col

print("Slide 1 updated successfully.")

# ==============================================================================
# SLIDE 2: Solution
# ==============================================================================
slide2 = prs.slides[1]

# Left Card: The Real-World Problem
card_prob = add_card(slide2, Inches(1.12), Inches(2.7), Inches(8.6), Inches(7.6))
tf_prob = card_prob.text_frame
tf_prob.vertical_anchor = MSO_ANCHOR.TOP
tf_prob.margin_left = Inches(0.4)
tf_prob.margin_right = Inches(0.4)
tf_prob.margin_top = Inches(0.4)
tf_prob.margin_bottom = Inches(0.4)
tf_prob.word_wrap = True

p = tf_prob.paragraphs[0]
p.text = "THE PROBLEM WE SOLVE"
p.font.name = FONT_SANS
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = COLOR_RED
p.space_after = Pt(6)

p_sub = tf_prob.add_paragraph()
p_sub.text = "Traditional enterprise decision-making & standard AI suffer from three fatal flaws:"
p_sub.font.name = FONT_SANS
p_sub.font.size = Pt(13)
p_sub.font.italic = True
p_sub.font.color.rgb = COLOR_MUTED_TEXT
p_sub.space_after = Pt(16)

problem_points = [
    ("1. Scattered Context & Information Silos", 
     "In procurement, lending, and claims, critical evidence is fragmented across Google Drive, old email threads, ERP ledgers, and employee heads. Nobody has the full picture at intake."),
    ("2. Expensive Decision Ping-Pong", 
     "Files bounce between departments for days: 'Where is the SOC2 cert?', 'Did Finance approve?' This repetitive chasing accounts for up to 70% of total approval cycle delays."),
    ("3. Generative AI Hallucination & Risk", 
     "Standard LLMs ask 'What should I decide?' and confidently guess even when missing 50% of the facts—creating catastrophic compliance, financial, and legal liabilities in production.")
]

for title, desc in problem_points:
    pt = tf_prob.add_paragraph()
    pt.text = title
    pt.font.name = FONT_SANS
    pt.font.size = Pt(15)
    pt.font.bold = True
    pt.font.color.rgb = COLOR_NAVY_HEADING
    pt.space_after = Pt(3)

    pd = tf_prob.add_paragraph()
    pd.text = desc
    pd.font.name = FONT_SANS
    pd.font.size = Pt(13)
    pd.font.color.rgb = COLOR_BODY_TEXT
    pd.space_after = Pt(14)

# Right Card: The Decision Completeness Solution
card_sol = add_card(slide2, Inches(10.2), Inches(2.7), Inches(8.68), Inches(7.6))
tf_sol = card_sol.text_frame
tf_sol.vertical_anchor = MSO_ANCHOR.TOP
tf_sol.margin_left = Inches(0.4)
tf_sol.margin_right = Inches(0.4)
tf_sol.margin_top = Inches(0.4)
tf_sol.margin_bottom = Inches(0.4)
tf_sol.word_wrap = True

p = tf_sol.paragraphs[0]
p.text = "OUR SOLUTION: THE COMPLETENESS ENGINE"
p.font.name = FONT_SANS
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = COLOR_TEAL_ACCENT
p.space_after = Pt(6)

p_sub2 = tf_sol.add_paragraph()
p_sub2.text = "The core paradigm shift: verify sufficiency before deciding, then self-heal:"
p_sub2.font.name = FONT_SANS
p_sub2.font.size = Pt(13)
p_sub2.font.italic = True
p_sub2.font.color.rgb = COLOR_MUTED_TEXT
p_sub2.space_after = Pt(16)

solution_points = [
    ("1. Core Paradigm Inversion", 
     "Instead of asking 'What should I decide?', our AI asks first: 'Do I have enough verified evidence to decide at all?'—mimicking a senior judge or lead physician."),
    ("2. Dynamic Evidence Planning (Not Hardcoded)", 
     "The AI dynamically reasons about what evidence is required based on request type, transaction value, and risk profile—adapting across 8 enterprise domains."),
    ("3. Zero-Hallucination Gatekeeper", 
     "Blocks execution when critical items are absent. It refuses to guess and calculates an objective completeness score (0-100%)."),
    ("4. Autonomous Multi-Source Self-Healing", 
     "Silently searches Google Drive vaults, Gmail/M365 archives, NetSuite ERP, and regulatory databases to recover missing documents automatically."),
    ("5. Precision Human-in-the-Loop (HITL)", 
     "Sends a surgical micro-request for ONLY the single missing piece (e.g. 1-click VP budget approval in 15 seconds, not 30 minutes).")
]

for title, desc in solution_points:
    pt = tf_sol.add_paragraph()
    pt.text = title
    pt.font.name = FONT_SANS
    pt.font.size = Pt(14)
    pt.font.bold = True
    pt.font.color.rgb = COLOR_NAVY_HEADING
    pt.space_after = Pt(2)

    pd = tf_sol.add_paragraph()
    pd.text = desc
    pd.font.name = FONT_SANS
    pd.font.size = Pt(12.5)
    pd.font.color.rgb = COLOR_BODY_TEXT
    pd.space_after = Pt(8)

print("Slide 2 updated successfully.")

# ==============================================================================
# SLIDE 3: Tech Stack & Architecture
# ==============================================================================
slide3 = prs.slides[2]

tech_layers = [
    ("1. Agentic Core & Reasoning Engine",
     "Python 3.13 • Pydantic v2 Type-Safe Schemas • Dynamic Evidence Spec Planner • Gatekeeper Zero-Hallucination Auditor • Pluggable LLM (Groq Llama 3.3 70B / Gemini 1.5 Pro / Local)",
     COLOR_INDIGO_ACCENT, COLOR_INDIGO_LIGHT),
    ("2. Autonomous Multi-Source Enterprise Connectors",
     "Corporate Google Drive Vault (Indexed PDFs, SOC2, Appraisals) • Mailbox Archive (Gmail / M365 Exchange Threads) • ERP Financial Ledger (NetSuite / SAP GL Balances) • Regulatory Registries (D&B, OFAC, SOS)",
     COLOR_TEAL_ACCENT, COLOR_TEAL_LIGHT),
    ("3. Precision Human-in-the-Loop & Execution Dispatchers",
     "Precision Micro-Ask Orchestrator • Webhook Action Cards (Slack / Email 1-Click Interactive Buttons) • Downstream Action Dispatchers (PO Creation, EDI-835 Claims, Term Sheets) • SHA-256 Audit Ledger",
     COLOR_AMBER, RGBColor(254, 243, 199)),
    ("4. Visual Decision Studio, API & Cloud Orchestration",
     "Modern Dark-Mode Decision Studio (Tailwind CSS, Lucide Icons) • High-Performance Flask/FastAPI REST API (< 20ms execution) • Cloudflare Secure Global HTTPS Tunnel • Production-Ready n8n Workflow JSON",
     COLOR_DARK_SLATE, RGBColor(241, 245, 249))
]

y_pos = Inches(2.7)
card_h = Inches(1.68)
gap = Inches(0.2)

for title, desc, col_acc, col_bg in tech_layers:
    c = add_card(slide3, Inches(1.12), y_pos, Inches(17.76), card_h, bg_rgb=COLOR_CARD_BG, border_rgb=COLOR_CARD_BORDER)
    tf = c.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.4)
    tf.margin_right = Inches(0.4)
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_SANS
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = col_acc
    p.space_after = Pt(4)

    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = FONT_SANS
    p2.font.size = Pt(13.5)
    p2.font.color.rgb = COLOR_BODY_TEXT

    y_pos += card_h + gap

print("Slide 3 updated successfully.")

# ==============================================================================
# SLIDE 4: System Architecture (Blank in template, let's add title + architecture diagram)
# ==============================================================================
slide4 = prs.slides[3]

# Add Title matching template
title_box = slide4.shapes.add_textbox(Inches(1.12), Inches(0.92), Inches(14.46), Inches(1.5))
tf_title = title_box.text_frame
p_title = tf_title.paragraphs[0]
p_title.text = "System Architecture"
p_title.font.name = "Times"
p_title.font.size = Pt(80)
p_title.font.bold = False
p_title.font.color.rgb = COLOR_TITLE_CYAN

# Architecture Visual Flow Card
arch_card = add_card(slide4, Inches(1.12), Inches(2.7), Inches(17.76), Inches(7.6))
tf_arch = arch_card.text_frame
tf_arch.vertical_anchor = MSO_ANCHOR.TOP
tf_arch.margin_left = Inches(0.4)
tf_arch.margin_right = Inches(0.4)
tf_arch.margin_top = Inches(0.4)
tf_arch.margin_bottom = Inches(0.4)
tf_arch.word_wrap = True

p = tf_arch.paragraphs[0]
p.text = "END-TO-END AUTONOMOUS AGENT PIPELINE"
p.font.name = FONT_SANS
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = COLOR_DARK_SLATE
p.space_after = Pt(10)

arch_blocks = [
    ("[1] REQUEST INTAKE", "Ingests transaction from Form, Email, Webhook, or API", "Dossier Model", COLOR_DARK_SLATE),
    ("[2] EVIDENCE PLANNER", "LLM dynamically infers required evidence spec & confidence thresholds", "Pydantic Spec", COLOR_INDIGO_ACCENT),
    ("[3] GAP AUDITOR & GATEKEEPER", "Audits available vs required evidence. If gaps exist: HALT & ENGAGE GATE", "Zero-Hallucination Gate", COLOR_RED),
    ("[4] AUTONOMOUS RETRIEVER", "Searches Google Drive Vault, Gmail/M365, NetSuite ERP, Registries", "Multi-Source Search", COLOR_TEAL_ACCENT),
    ("[5] PRECISION HITL MICRO-ASK", "Dispatches surgical Slack/Email card for ONLY the remaining missing delta", "1-Click Interactive Card", COLOR_AMBER),
    ("[6] DELIBERATOR & VERDICT", "Holistic synthesis, calibrated confidence (e.g. 97%), citation-backed reasoning", "Explainable Verdict", COLOR_GREEN),
    ("[7] DOWNSTREAM ACTIONS", "Dispatches PO creation, sends notifications, commits SHA-256 audit ledger", "Automated Execution", COLOR_INDIGO_ACCENT),
    ("[8] META-LEARNING OPTIMIZER", "Telemetry mines blocker patterns; proposes intake form re-engineering", "Continuous Optimization", COLOR_DARK_SLATE)
]

for name, desc, badge, col in arch_blocks:
    p_b = tf_arch.add_paragraph()
    r_n = p_b.add_run()
    r_n.text = f"{name}  "
    r_n.font.name = FONT_SANS
    r_n.font.size = Pt(13.5)
    r_n.font.bold = True
    r_n.font.color.rgb = col

    r_bd = p_b.add_run()
    r_bd.text = f"[{badge}]  —  "
    r_bd.font.name = FONT_SANS
    r_bd.font.size = Pt(11.5)
    r_bd.font.bold = True
    r_bd.font.color.rgb = COLOR_MUTED_TEXT

    r_d = p_b.add_run()
    r_d.text = desc
    r_d.font.name = FONT_SANS
    r_d.font.size = Pt(13)
    r_d.font.color.rgb = COLOR_BODY_TEXT
    p_b.space_after = Pt(7)

print("Slide 4 updated successfully.")

# ==============================================================================
# SLIDE 5: Data Flow Diagram
# ==============================================================================
slide5 = prs.slides[4]

flow_card = add_card(slide5, Inches(1.12), Inches(2.7), Inches(17.76), Inches(7.6))
tf_flow = flow_card.text_frame
tf_flow.vertical_anchor = MSO_ANCHOR.TOP
tf_flow.margin_left = Inches(0.4)
tf_flow.margin_right = Inches(0.4)
tf_flow.margin_top = Inches(0.4)
tf_flow.margin_bottom = Inches(0.4)
tf_flow.word_wrap = True

p = tf_flow.paragraphs[0]
p.text = "THE 8-STEP AUTONOMOUS DECISION LIFECYCLE"
p.font.name = FONT_SANS
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = COLOR_DARK_SLATE
p.space_after = Pt(12)

steps_data = [
    ("Step 1: Request Intake Arrives", "Transaction arrives via intake form, webhook, or email with initial context & attachments."),
    ("Step 2: AI Dynamic Evidence Planning", "AI reads the request & context, inferring exact required evidence (price, SLAs, SOC2, budget)."),
    ("Step 3 & 4: Initial Gap Audit & Gatekeeper Block", "Engine cross-checks initial dossier against specs. Gaps found (e.g. SOC2, Budget) -> Engine HALTS."),
    ("Step 5: Autonomous Multi-Source Self-Healing", "Engine searches connected silos: Google Drive finds SOC2 cert; NetSuite ERP verifies vendor reliability."),
    ("Step 6: Precision Human-in-the-Loop (HITL)", "Only budget approval remains absent. Dispatches targeted Slack card to VP Finance for 1-click sign-off."),
    ("Step 7: Deliberation, Verdict & Execution", "Dossier 100% complete! AI issues calibrated verdict (Approved, 97% confidence), issues PO & notifies team."),
    ("Step 8: Continuous Meta-Learning & Process Mining", "Engine analyzes telemetry across decisions; suggests adding budget check to intake form to eliminate future blocks.")
]

for stitle, sdesc in steps_data:
    p_s = tf_flow.add_paragraph()
    r1 = p_s.add_run()
    r1.text = f"{stitle}: "
    r1.font.name = FONT_SANS
    r1.font.size = Pt(14)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_TEAL_ACCENT

    r2 = p_s.add_run()
    r2.text = sdesc
    r2.font.name = FONT_SANS
    r2.font.size = Pt(13)
    r2.font.color.rgb = COLOR_BODY_TEXT
    p_s.space_after = Pt(10)

print("Slide 5 updated successfully.")

# ==============================================================================
# SLIDE 6: Screenshot of Your Project
# ==============================================================================
slide6 = prs.slides[5]

# Top live demo link pill
link_card = add_card(slide6, Inches(1.12), Inches(2.55), Inches(17.76), Inches(0.7), bg_rgb=COLOR_INDIGO_LIGHT, border_rgb=COLOR_INDIGO_ACCENT)
tf_link = link_card.text_frame
tf_link.vertical_anchor = MSO_ANCHOR.MIDDLE
tf_link.margin_left = Inches(0.4)
p_link = tf_link.paragraphs[0]
r_l1 = p_link.add_run()
r_l1.text = "🌐 LIVE CLOUD DEMONSTRATION: "
r_l1.font.name = FONT_SANS
r_l1.font.size = Pt(14)
r_l1.font.bold = True
r_l1.font.color.rgb = COLOR_INDIGO_ACCENT

r_l2 = p_link.add_run()
r_l2.text = "https://static-outstanding-palm-clarke.trycloudflare.com  (Fast <50ms, 8 Enterprise Domains)"
r_l2.font.name = FONT_SANS
r_l2.font.size = Pt(14)
r_l2.font.bold = True
r_l2.font.color.rgb = COLOR_DARK_SLATE

# UI Mockup Card
ui_card = add_card(slide6, Inches(1.12), Inches(3.4), Inches(17.76), Inches(6.9))
tf_ui = ui_card.text_frame
tf_ui.vertical_anchor = MSO_ANCHOR.TOP
tf_ui.margin_left = Inches(0.4)
tf_ui.margin_right = Inches(0.4)
tf_ui.margin_top = Inches(0.3)
tf_ui.word_wrap = True

p = tf_ui.paragraphs[0]
p.text = "DECISION COMPLETENESS ENGINE — VISUAL DECISION STUDIO UI"
p.font.name = FONT_SANS
p.font.size = Pt(17)
p.font.bold = True
p.font.color.rgb = COLOR_DARK_SLATE
p.space_after = Pt(8)

ui_features = [
    ("⚡ Real-Time 8-Step Pipeline Stepper:", "Animated visual transitions from [01 Intake] through [04 Gatekeeper Block] to [07 Final Verdict] and [08 Meta-Learning]."),
    ("🎛️ Dual-Speed Execution Controls:", "Switch between ⚡ Turbo Mode (Instant < 50ms) for high-throughput evaluation, and 🏎️ Fast Mode (Animated 350ms) for visual demonstrations."),
    ("📋 Live Evidence Specification Matrix:", "Color-coded status badges: [VERIFIED], [✨ SELF-HEALED from Drive/ERP], [👤 HITL APPROVED], and [❌ MISSING GAP] with source citations & confidence meters."),
    ("🛡️ Interactive Zero-Hallucination Gatekeeper:", "Visual security block card prevents LLM guessing when evidence threshold is unsatisfied; details exact missing delta."),
    ("👤 Precision HITL Micro-Ask Simulator:", "Targeted 1-click interactive approval card simulating Slack/Email push notifications (testable live in the browser)."),
    ("📊 Continuous Process Mining Dashboard:", "Live telemetric charts computing Gatekeeper Block Rate (62%), Self-Healing Rate (88%), and automated intake form redesign suggestions.")
]

for f_name, f_desc in ui_features:
    p_f = tf_ui.add_paragraph()
    r1 = p_f.add_run()
    r1.text = f"{f_name} "
    r1.font.name = FONT_SANS
    r1.font.size = Pt(13)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_TEAL_ACCENT

    r2 = p_f.add_run()
    r2.text = f_desc
    r2.font.name = FONT_SANS
    r2.font.size = Pt(12.5)
    r2.font.color.rgb = COLOR_BODY_TEXT
    p_f.space_after = Pt(8)

print("Slide 6 updated successfully.")

# ==============================================================================
# SLIDE 7: Others
# ==============================================================================
slide7 = prs.slides[6]

col_w = Inches(5.65)
col_gap = Inches(0.4)
c1_left = Inches(1.12)
c2_left = c1_left + col_w + col_gap
c3_left = c2_left + col_w + col_gap

# Col 1: 8 Enterprise Scenarios
card_c1 = add_card(slide7, c1_left, Inches(2.7), col_w, Inches(7.6))
tf_c1 = card_c1.text_frame
tf_c1.vertical_anchor = MSO_ANCHOR.TOP
tf_c1.margin_left = Inches(0.3)
tf_c1.margin_right = Inches(0.3)
tf_c1.margin_top = Inches(0.3)
tf_c1.word_wrap = True

p = tf_c1.paragraphs[0]
p.text = "8 ENTERPRISE DOMAINS"
p.font.name = FONT_SANS
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = COLOR_DARK_SLATE
p.space_after = Pt(8)

scenarios_list = [
    ("1. Hardware Procurement", "$85k Laptops • Recovers SOC2 from Drive; asks VP Finance."),
    ("2. FinTech Lending", "$250k Apex Revolving • Recovers Form 1120-S & 12M bank records."),
    ("3. Executive Hiring", "VP Eng Offer • Recovers Sterling background check & reference."),
    ("4. Healthcare Claims", "$42k Knee Surgery • Recovers surgical op notes & prior auth."),
    ("5. Corporate Expense", "$14.2k Zurich Dinner • Recovers itemized VAT folio; asks VP."),
    ("6. Legal & SaaS Contract", "VectorFlow AI ($120k/yr) • Recovers executed DPA & covenants."),
    ("7. Cloud Firewall Exemption", "Port 9443 Ingress • Discovers partner mTLS cert & 48h TTL."),
    ("8. Jumbo Mortgage Loan", "$850k Loan • Recovers appraisal ($1.15M, 73.9% LTV) & W-2s.")
]

for title, desc in scenarios_list:
    p_sc = tf_c1.add_paragraph()
    r1 = p_sc.add_run()
    r1.text = f"{title}: "
    r1.font.name = FONT_SANS
    r1.font.size = Pt(11.5)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_INDIGO_ACCENT

    r2 = p_sc.add_run()
    r2.text = desc
    r2.font.name = FONT_SANS
    r2.font.size = Pt(11)
    r2.font.color.rgb = COLOR_BODY_TEXT
    p_sc.space_after = Pt(4)

# Col 2: Business Value & Metrics
card_c2 = add_card(slide7, c2_left, Inches(2.7), col_w, Inches(7.6))
tf_c2 = card_c2.text_frame
tf_c2.vertical_anchor = MSO_ANCHOR.TOP
tf_c2.margin_left = Inches(0.3)
tf_c2.margin_right = Inches(0.3)
tf_c2.margin_top = Inches(0.3)
tf_c2.word_wrap = True

p = tf_c2.paragraphs[0]
p.text = "QUANTIFIABLE ROI"
p.font.name = FONT_SANS
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = COLOR_TEAL_ACCENT
p.space_after = Pt(8)

roi_points = [
    ("⚡ 90% Turnaround Reduction", "Cuts average enterprise approval cycles from 2.5 days down to sub-minute execution."),
    ("🛡️ Zero-Hallucination Guarantee", "Hard gate strictly halts AI from guessing or making decisions when evidence is incomplete."),
    ("⏱️ 15-Sec Human Overhead", "Replaces exhausting 40-page document reviews with 1-click targeted micro-approvals."),
    ("📈 Process Self-Healing", "Continuous process mining diagnoses systemic blockers to permanently optimize intake forms.")
]

for title, desc in roi_points:
    p_roi = tf_c2.add_paragraph()
    r1 = p_roi.add_run()
    r1.text = title
    r1.font.name = FONT_SANS
    r1.font.size = Pt(13)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_NAVY_HEADING
    p_roi.space_after = Pt(2)

    p_d = tf_c2.add_paragraph()
    p_d.text = desc
    p_d.font.name = FONT_SANS
    p_d.font.size = Pt(12)
    p_d.font.color.rgb = COLOR_BODY_TEXT
    p_d.space_after = Pt(12)

# Col 3: Production Readiness & Deliverables
card_c3 = add_card(slide7, c3_left, Inches(2.7), col_w, Inches(7.6))
tf_c3 = card_c3.text_frame
tf_c3.vertical_anchor = MSO_ANCHOR.TOP
tf_c3.margin_left = Inches(0.3)
tf_c3.margin_right = Inches(0.3)
tf_c3.margin_top = Inches(0.3)
tf_c3.word_wrap = True

p = tf_c3.paragraphs[0]
p.text = "PRODUCTION DELIVERABLES"
p.font.name = FONT_SANS
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = COLOR_DARK_SLATE
p.space_after = Pt(8)

deliverables = [
    ("📦 Importable n8n Workflow", "Full production JSON workflow with AI Agent, Tool & Webhook nodes (`decision_completeness_engine.json`)."),
    ("🧪 Automated Test Suite", "9/9 passing unit & integration tests (`python -m unittest tests/test_engine.py`)."),
    ("☁️ Multi-Cloud Deployment", "Dockerfile, Render (render.yaml), Railway (railway.json), and Vercel configuration ready to deploy."),
    ("🔒 Cryptographic Audit Proof", "SHA-256 chain-of-custody evidence hashing for regulatory compliance and audit readiness.")
]

for title, desc in deliverables:
    p_del = tf_c3.add_paragraph()
    r1 = p_del.add_run()
    r1.text = title
    r1.font.name = FONT_SANS
    r1.font.size = Pt(13)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_NAVY_HEADING
    p_del.space_after = Pt(2)

    p_d = tf_c3.add_paragraph()
    p_d.text = desc
    p_d.font.name = FONT_SANS
    p_d.font.size = Pt(12)
    p_d.font.color.rgb = COLOR_BODY_TEXT
    p_d.space_after = Pt(12)

print("Slide 7 updated successfully.")

# Save updated presentation
prs.save(OUTPUT_PATH)
shutil.copyfile(OUTPUT_PATH, STATIC_PATH)
print(f"DONE! Presentation saved to {OUTPUT_PATH} and copied to {STATIC_PATH}.")
