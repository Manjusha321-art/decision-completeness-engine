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

# Palette
COLOR_TITLE_CYAN = RGBColor(93, 224, 230)      # #5DE0E6 (Template Title)
COLOR_DARK_SLATE = RGBColor(15, 23, 42)        # #0F172A
COLOR_NAVY_HEADING = RGBColor(30, 41, 59)      # #1E293B
COLOR_BODY_TEXT = RGBColor(51, 65, 85)         # #334155
COLOR_MUTED_TEXT = RGBColor(100, 116, 139)     # #64748B
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_CARD_BORDER = RGBColor(203, 213, 225)    # Slate-300
COLOR_TEAL_ACCENT = RGBColor(13, 148, 136)     # Teal-600
COLOR_TEAL_BG = RGBColor(240, 253, 250)        # Teal-50
COLOR_TEAL_BORDER = RGBColor(94, 234, 212)     # Teal-300
COLOR_INDIGO_ACCENT = RGBColor(79, 70, 229)    # Indigo-600
COLOR_INDIGO_BG = RGBColor(238, 242, 255)      # Indigo-50
COLOR_INDIGO_BORDER = RGBColor(199, 210, 254)  # Indigo-300
COLOR_GREEN = RGBColor(22, 163, 74)            # Green-600
COLOR_GREEN_BG = RGBColor(240, 253, 244)       # Green-50
COLOR_GREEN_BORDER = RGBColor(134, 239, 172)   # Green-300
COLOR_AMBER = RGBColor(217, 119, 6)            # Amber-600
COLOR_AMBER_BG = RGBColor(254, 243, 199)       # Amber-50
COLOR_AMBER_BORDER = RGBColor(252, 211, 77)    # Amber-300
COLOR_RED = RGBColor(220, 38, 38)              # Red-600
COLOR_RED_BG = RGBColor(254, 242, 242)         # Red-50
COLOR_RED_BORDER = RGBColor(252, 165, 165)     # Red-300
COLOR_GRAY_BG = RGBColor(248, 250, 252)        # Slate-50

FONT_SANS = "Calibri"
FONT_TITLE = "Times"

def add_rounded_box(slide, left, top, width, height, bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER, border_width=1.5):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(border_width)
    else:
        shape.line.fill.background()
    return shape

def add_arrow(slide, left, top, width, height, color=COLOR_TEAL_ACCENT):
    arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, left, top, width, height)
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = color
    arrow.line.fill.background()
    return arrow

def add_down_arrow(slide, left, top, width, height, color=COLOR_TEAL_ACCENT):
    arrow = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, left, top, width, height)
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = color
    arrow.line.fill.background()
    return arrow

# ==============================================================================
# SLIDE 1: Cover Slide
# ==============================================================================
slide1 = prs.slides[0]
shape15 = slide1.shapes[15]
shape15.left = Inches(1.5)
shape15.top = Inches(6.8)
shape15.width = Inches(11.2)
shape15.height = Inches(2.5)
tf15 = shape15.text_frame
tf15.word_wrap = True
tf15.clear()

items_s1 = [
    ("NAME: ", "Manjusha Varikuppala", COLOR_DARK_SLATE, True),
    ("TEAM NAME: ", "Hackhustlers", COLOR_INDIGO_ACCENT, True),
    ("TRACK: ", "Track 01: AI & Enterprise Automation (Open Innovation)", COLOR_DARK_SLATE, True),
    ("PROJECT: ", "The Decision Completeness Engine (DCE)", COLOR_TEAL_ACCENT, True),
    ("LIVE DEMO: ", "https://static-outstanding-palm-clarke.trycloudflare.com", COLOR_DARK_SLATE, False),
]

for idx, (label, val, val_col, is_bold) in enumerate(items_s1):
    p = tf15.paragraphs[0] if idx == 0 else tf15.add_paragraph()
    p.space_after = Pt(4)
    r1 = p.add_run()
    r1.text = label
    r1.font.name = "Playfair Display"
    r1.font.size = Pt(16)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_DARK_SLATE

    r2 = p.add_run()
    r2.text = val
    r2.font.name = FONT_SANS
    r2.font.size = Pt(16)
    r2.font.bold = is_bold
    r2.font.color.rgb = val_col

print("Slide 1 updated with Manjusha Varikuppala & Hackhustlers.")

# ==============================================================================
# SLIDE 2: Solution (Visual Comparison & Diagram)
# ==============================================================================
slide2 = prs.slides[1]

# Clear any previous content shapes on slide 2 (keep 0, 1 background, 2 title)
while len(slide2.shapes) > 3:
    sp = slide2.shapes[len(slide2.shapes)-1]._element
    sp.getparent().remove(sp)

# Left Column: THE PROBLEM (Visual breakdown of the failure loop)
card_prob = add_rounded_box(slide2, Inches(1.12), Inches(2.7), Inches(8.6), Inches(7.6), bg_color=COLOR_WHITE, border_color=COLOR_RED_BORDER)
tf_p = card_prob.text_frame
tf_p.margin_left = Inches(0.4)
tf_p.margin_right = Inches(0.4)
tf_p.margin_top = Inches(0.35)
p = tf_p.paragraphs[0]
p.text = "THE PROBLEM: WHY ENTERPRISE DECISIONS FAIL"
p.font.name = FONT_SANS
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = COLOR_RED
p.space_after = Pt(14)

prob_flow = [
    ("1. Scattered Context & Silos", "Drive, Email, NetSuite ERP, Spreadsheets", "Information is never in one place at intake. Gaps are discovered late.", COLOR_RED_BG, COLOR_RED_BORDER, COLOR_RED),
    ("2. Endless Approval Ping-Pong", "2.5 Days Wasted Per Approval", "'You forgot the SOC2 cert', 'Where is budget approval?' Bouncing files wastes 70% of time.", COLOR_AMBER_BG, COLOR_AMBER_BORDER, COLOR_AMBER),
    ("3. Dangerous GenAI Hallucination", "Standard LLMs Confidently Guess", "Most AI asks 'What should I decide?' and hallucinates when missing 50% of the facts.", COLOR_RED_BG, COLOR_RED_BORDER, COLOR_RED)
]

y_step = Inches(3.4)
for title, badge, desc, bg_c, bdr_c, acc_c in prob_flow:
    box = add_rounded_box(slide2, Inches(1.4), y_step, Inches(8.0), Inches(1.7), bg_color=bg_c, border_color=bdr_c)
    tf = box.text_frame
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.2)
    tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    r_t = p1.add_run()
    r_t.text = f"{title}  "
    r_t.font.name = FONT_SANS
    r_t.font.size = Pt(14)
    r_t.font.bold = True
    r_t.font.color.rgb = acc_c
    
    r_b = p1.add_run()
    r_b.text = f"[{badge}]"
    r_b.font.name = FONT_SANS
    r_b.font.size = Pt(11)
    r_b.font.bold = True
    r_b.font.color.rgb = COLOR_NAVY_HEADING
    p1.space_after = Pt(4)
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = FONT_SANS
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_BODY_TEXT
    
    y_step += Inches(1.85)

# Down arrow connecting problem to the hallucination callout
callout_p = add_rounded_box(slide2, Inches(1.4), Inches(9.0), Inches(8.0), Inches(0.95), bg_color=COLOR_DARK_SLATE, border_color=None)
tf_cp = callout_p.text_frame
tf_cp.vertical_anchor = MSO_ANCHOR.MIDDLE
tf_cp.margin_left = Inches(0.3)
tf_cp.margin_right = Inches(0.3)
p_cp = tf_cp.paragraphs[0]
p_cp.text = "Result: Decisions are either paralyzed for days or made blindly with missing facts."
p_cp.font.name = FONT_SANS
p_cp.font.size = Pt(12.5)
p_cp.font.bold = True
p_cp.font.color.rgb = COLOR_WHITE

# Right Column: THE SOLUTION (Decision Completeness Engine)
card_sol = add_rounded_box(slide2, Inches(10.2), Inches(2.7), Inches(8.68), Inches(7.6), bg_color=COLOR_WHITE, border_color=COLOR_TEAL_BORDER)
tf_s = card_sol.text_frame
tf_s.margin_left = Inches(0.4)
tf_s.margin_right = Inches(0.4)
tf_s.margin_top = Inches(0.35)
p = tf_s.paragraphs[0]
p.text = "THE SOLUTION: DECISION COMPLETENESS ENGINE"
p.font.name = FONT_SANS
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = COLOR_TEAL_ACCENT
p.space_after = Pt(14)

sol_flow = [
    ("1. Core Inversion", "Do I have enough evidence to decide?", "Like a lead doctor ordering tests before diagnosing, we verify completeness first.", COLOR_TEAL_BG, COLOR_TEAL_BORDER, COLOR_TEAL_ACCENT),
    ("2. Dynamic Planning", "Inferred Evidence Specs (Not Checklists)", "AI dynamically deduces what evidence is needed based on transaction amount, domain, and risk tier.", COLOR_INDIGO_BG, COLOR_INDIGO_BORDER, COLOR_INDIGO_ACCENT),
    ("3. Zero-Hallucination Gate", "Halts & Calculates 0-100% Score", "Guaranteed zero speculation: if critical evidence is absent, the engine blocks decision execution.", COLOR_RED_BG, COLOR_RED_BORDER, COLOR_RED),
    ("4. Autonomous Self-Healing", "Searches Drive, Mail, ERP, Web", "Silently recovers missing proof from connected enterprise silos before bothering humans.", COLOR_GREEN_BG, COLOR_GREEN_BORDER, COLOR_GREEN),
    ("5. Precision Human-in-the-Loop", "15-Sec Targeted Micro-Ask", "Sends a surgical Slack/Email card for ONLY the remaining missing delta (e.g. 1-click VP budget approval).", COLOR_AMBER_BG, COLOR_AMBER_BORDER, COLOR_AMBER)
]

y_step = Inches(3.4)
for title, badge, desc, bg_c, bdr_c, acc_c in sol_flow:
    box = add_rounded_box(slide2, Inches(10.5), y_step, Inches(8.08), Inches(1.15), bg_color=bg_c, border_color=bdr_c)
    tf = box.text_frame
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.12)
    tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    r_t = p1.add_run()
    r_t.text = f"{title}  "
    r_t.font.name = FONT_SANS
    r_t.font.size = Pt(13)
    r_t.font.bold = True
    r_t.font.color.rgb = acc_c
    
    r_b = p1.add_run()
    r_b.text = f"[{badge}]"
    r_b.font.name = FONT_SANS
    r_b.font.size = Pt(11)
    r_b.font.bold = True
    r_b.font.color.rgb = COLOR_NAVY_HEADING
    p1.space_after = Pt(2)
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = FONT_SANS
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = COLOR_BODY_TEXT
    
    y_step += Inches(1.23)

print("Slide 2 updated with visual comparison cards.")

# ==============================================================================
# SLIDE 3: Tech Stack & Architecture (4-Tier Layered Architecture Diagram)
# ==============================================================================
slide3 = prs.slides[2]

while len(slide3.shapes) > 3:
    sp = slide3.shapes[len(slide3.shapes)-1]._element
    sp.getparent().remove(sp)

layers = [
    ("LAYER 1: AGENTIC CORE & REASONING ENGINE",
     "Dynamic Evidence Specification Planner • Gap Auditor & Completeness Scorer (0-100%) • Zero-Hallucination Gatekeeper • Deliberator & Confidence Calibration",
     "Python 3.13 • Pydantic v2 Type-Safe Contracts • Groq Llama 3.3 70B / Gemini 1.5 Pro",
     COLOR_INDIGO_ACCENT, COLOR_INDIGO_BG, COLOR_INDIGO_BORDER),
    ("LAYER 2: AUTONOMOUS MULTI-SOURCE ENTERPRISE CONNECTORS",
     "Corporate Google Drive Vault (Indexed PDFs, SOC2, Appraisals) • Mailbox Archive (Gmail / M365 Exchange Threads) • ERP Financial Ledger (NetSuite / SAP GL Balances) • Regulatory Registries (D&B, OFAC, SOS)",
     "Vector Embeddings • Fuzzy Matcher • REST APIs • Pluggable BaseConnector Abstraction",
     COLOR_TEAL_ACCENT, COLOR_TEAL_BG, COLOR_TEAL_BORDER),
    ("LAYER 3: PRECISION HUMAN-IN-THE-LOOP & ACTION DISPATCHERS",
     "Precision Micro-Ask Engine (Role-Targeted Asks) • Interactive Slack & Email Cards with 1-Click Approval • Downstream Action Execution (PO Generation, Claim Remittance EDI-835, Term Sheet)",
     "Slack Webhooks • Action Dispatcher Subsystem • SHA-256 Chain-of-Custody Audit Ledger",
     COLOR_AMBER, COLOR_AMBER_BG, COLOR_AMBER_BORDER),
    ("LAYER 4: VISUAL DECISION STUDIO & CLOUD ORCHESTRATION",
     "Dark-Mode Visual Studio UI • 8-Step Interactive Pipeline Stepper • Turbo (<50ms) & Animated Execution Modes • Continuous Meta-Learning & Process Mining Dashboard",
     "FastAPI / Flask Single-Roundtrip API • Tailwind CSS • n8n Workflow (`decision_completeness.json`) • Cloudflare Live Tunnel",
     COLOR_DARK_SLATE, COLOR_GRAY_BG, COLOR_CARD_BORDER)
]

y_pos = Inches(2.7)
card_h = Inches(1.72)
gap = Inches(0.18)

for l_title, l_desc, l_tech, acc_c, bg_c, bdr_c in layers:
    card = add_rounded_box(slide3, Inches(1.12), y_pos, Inches(17.76), card_h, bg_color=bg_c, border_color=bdr_c)
    tf = card.text_frame
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.4)
    tf.margin_right = Inches(0.4)
    tf.margin_top = Inches(0.2)
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = l_title
    p.font.name = FONT_SANS
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = acc_c
    p.space_after = Pt(3)

    p2 = tf.add_paragraph()
    p2.text = l_desc
    p2.font.name = FONT_SANS
    p2.font.size = Pt(13)
    p2.font.color.rgb = COLOR_BODY_TEXT
    p2.space_after = Pt(4)

    p3 = tf.add_paragraph()
    r_tech_lbl = p3.add_run()
    r_tech_lbl.text = "Tech Stack: "
    r_tech_lbl.font.name = FONT_SANS
    r_tech_lbl.font.size = Pt(12)
    r_tech_lbl.font.bold = True
    r_tech_lbl.font.color.rgb = COLOR_NAVY_HEADING

    r_tech_val = p3.add_run()
    r_tech_val.text = l_tech
    r_tech_val.font.name = FONT_SANS
    r_tech_val.font.size = Pt(12)
    r_tech_val.font.color.rgb = acc_c

    y_pos += card_h + gap

print("Slide 3 updated with layered tech stack.")

# ==============================================================================
# SLIDE 4: System Architecture (End-to-End Visual Flowchart Pipeline)
# ==============================================================================
slide4 = prs.slides[3]

while len(slide4.shapes) > 2:
    sp = slide4.shapes[len(slide4.shapes)-1]._element
    sp.getparent().remove(sp)

# Add Title
title_box = slide4.shapes.add_textbox(Inches(1.12), Inches(0.92), Inches(14.46), Inches(1.5))
tf_title = title_box.text_frame
p_title = tf_title.paragraphs[0]
p_title.text = "System Architecture"
p_title.font.name = FONT_TITLE
p_title.font.size = Pt(80)
p_title.font.color.rgb = COLOR_TITLE_CYAN

# Outer container card
main_card = add_rounded_box(slide4, Inches(1.12), Inches(2.7), Inches(17.76), Inches(7.6), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)

# Top subtitle
tf_m = main_card.text_frame
tf_m.margin_left = Inches(0.4)
tf_m.margin_top = Inches(0.25)
p = tf_m.paragraphs[0]
p.text = "AUTONOMOUS MULTI-AGENT DECISION PIPELINE & FEEDBACK LOOP"
p.font.name = FONT_SANS
p.font.size = Pt(17)
p.font.bold = True
p.font.color.rgb = COLOR_DARK_SLATE

# Row 1: 5 Pipeline Process Blocks with Arrows
blocks_r1 = [
    ("Step 1\nINTAKE", "Request Arrives\n(Form / Email / API)", COLOR_DARK_SLATE, COLOR_GRAY_BG, COLOR_CARD_BORDER),
    ("Step 2\nPLANNER", "Dynamic Spec\nInference (Pydantic)", COLOR_INDIGO_ACCENT, COLOR_INDIGO_BG, COLOR_INDIGO_BORDER),
    ("Step 3 & 4\nAUDITOR", "Gap Audit &\nGatekeeper Block", COLOR_RED, COLOR_RED_BG, COLOR_RED_BORDER),
    ("Step 5\nRETRIEVER", "Autonomous Search\n(Drive/Mail/ERP)", COLOR_TEAL_ACCENT, COLOR_TEAL_BG, COLOR_TEAL_BORDER),
    ("Step 6\nHITL MICRO-ASK", "Targeted 1-Click\nSlack Approval", COLOR_AMBER, COLOR_AMBER_BG, COLOR_AMBER_BORDER),
]

b_w = Inches(2.65)
b_h = Inches(1.85)
b_y = Inches(3.4)
arr_w = Inches(0.55)
arr_h = Inches(0.35)
arr_y = b_y + Inches(0.75)

x = Inches(1.4)
for i, (b_title, b_sub, acc_c, bg_c, bdr_c) in enumerate(blocks_r1):
    box = add_rounded_box(slide4, x, b_y, b_w, b_h, bg_color=bg_c, border_color=bdr_c)
    tf = box.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    p1.text = b_title
    p1.font.name = FONT_SANS
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = acc_c
    p1.space_after = Pt(4)
    
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.text = b_sub
    p2.font.name = FONT_SANS
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_BODY_TEXT
    
    x += b_w
    if i < len(blocks_r1) - 1:
        add_arrow(slide4, x + Inches(0.1), arr_y, arr_w, arr_h, color=COLOR_TEAL_ACCENT)
        x += arr_w + Inches(0.2)

# Row 2: Downstream Deliberation, Verdict, and Action Execution (Width 11.0) + Telemetry Feedback (Width 6.0)
y_r2 = Inches(5.6)
card_dec = add_rounded_box(slide4, Inches(1.4), y_r2, Inches(10.8), Inches(2.3), bg_color=COLOR_GREEN_BG, border_color=COLOR_GREEN_BORDER)
tf_dec = card_dec.text_frame
tf_dec.margin_left = Inches(0.35)
tf_dec.margin_right = Inches(0.35)
tf_dec.margin_top = Inches(0.25)
tf_dec.word_wrap = True

p = tf_dec.paragraphs[0]
p.text = "Step 7: DELIBERATION, CONFIDENCE SCORING & EXECUTION"
p.font.name = FONT_SANS
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = COLOR_GREEN
p.space_after = Pt(4)

dec_details = [
    ("✓ Calibrated Verdict: ", "Computes evidence-grounded confidence (e.g. 97%) and generates citation-backed explanation."),
    ("✓ Automated Actions: ", "Generates Purchase Order PO-88421, updates NetSuite ERP, and dispatches Slack notifications."),
    ("✓ Proof of Compliance: ", "Commits SHA-256 cryptographic chain-of-custody audit log for zero-tamper auditability.")
]
for lbl, val in dec_details:
    pd = tf_dec.add_paragraph()
    r1 = pd.add_run()
    r1.text = lbl
    r1.font.name = FONT_SANS
    r1.font.size = Pt(12)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_DARK_SLATE
    r2 = pd.add_run()
    r2.text = val
    r2.font.name = FONT_SANS
    r2.font.size = Pt(12)
    r2.font.color.rgb = COLOR_BODY_TEXT
    pd.space_after = Pt(3)

# Meta-Learning Box (Right of Row 2)
card_meta = add_rounded_box(slide4, Inches(12.6), y_r2, Inches(5.9), Inches(2.3), bg_color=COLOR_INDIGO_BG, border_color=COLOR_INDIGO_BORDER)
tf_meta = card_meta.text_frame
tf_meta.margin_left = Inches(0.3)
tf_meta.margin_right = Inches(0.3)
tf_meta.margin_top = Inches(0.25)
tf_meta.word_wrap = True

p = tf_meta.paragraphs[0]
p.text = "Step 8: META-LEARNING ENGINE"
p.font.name = FONT_SANS
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = COLOR_INDIGO_ACCENT
p.space_after = Pt(4)

meta_bullets = [
    ("• Telemetry Mining: ", "Aggregates recurring missing evidence patterns across all past decisions."),
    ("• Intake Optimization: ", "Suggests: '70% of delays are missing budget sign-off. Add budget check at intake form.'"),
    ("• Continuous ROI: ", "Turns organizational decision bottlenecks into permanent process upgrades.")
]
for lbl, val in meta_bullets:
    pm = tf_meta.add_paragraph()
    r1 = pm.add_run()
    r1.text = lbl
    r1.font.name = FONT_SANS
    r1.font.size = Pt(11.5)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_DARK_SLATE
    r2 = pm.add_run()
    r2.text = val
    r2.font.name = FONT_SANS
    r2.font.size = Pt(11.5)
    r2.font.color.rgb = COLOR_BODY_TEXT
    pm.space_after = Pt(3)

# Bottom Architecture Security & Compliance Banner
card_banner = add_rounded_box(slide4, Inches(1.4), Inches(8.2), Inches(17.1), Inches(1.5), bg_color=COLOR_DARK_SLATE, border_color=None)
tf_b = card_banner.text_frame
tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
tf_b.margin_left = Inches(0.4)
tf_b.margin_right = Inches(0.4)
p = tf_b.paragraphs[0]
p.text = "ENTERPRISE SECURITY & COMPLIANCE ARCHITECTURE"
p.font.name = FONT_SANS
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_TITLE_CYAN
p.space_after = Pt(2)
p2 = tf_b.add_paragraph()
p2.text = "• Zero Data Retention Covenant • SOC2 Type II Encrypted Connectors • Least-Privilege Role-Based Access Control (RBAC) • SHA-256 Cryptographic Audit Ledger"
p2.font.name = FONT_SANS
p2.font.size = Pt(12)
p2.font.color.rgb = COLOR_WHITE

print("Slide 4 updated with interactive flowchart pipeline.")

# ==============================================================================
# SLIDE 5: Data Flow Diagram (DFD) — Real Visual Flowchart
# ==============================================================================
slide5 = prs.slides[4]

while len(slide5.shapes) > 3:
    sp = slide5.shapes[len(slide5.shapes)-1]._element
    sp.getparent().remove(sp)

# Outer Card
card_dfd = add_rounded_box(slide5, Inches(1.12), Inches(2.7), Inches(17.76), Inches(7.6), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
tf_dfd = card_dfd.text_frame
tf_dfd.margin_left = Inches(0.4)
tf_dfd.margin_top = Inches(0.2)
p = tf_dfd.paragraphs[0]
p.text = "DATA FLOW DIAGRAM (DFD LEVEL-1): EVIDENCE COMPLETENESS LIFECYCLE"
p.font.name = FONT_SANS
p.font.size = Pt(17)
p.font.bold = True
p.font.color.rgb = COLOR_DARK_SLATE

# DFD Entities & Flow Boxes
# 1. External Entity: Requester / Intake
ent_box = add_rounded_box(slide5, Inches(1.4), Inches(3.6), Inches(3.0), Inches(1.5), bg_color=COLOR_DARK_SLATE, border_color=None)
tf_e = ent_box.text_frame
tf_e.vertical_anchor = MSO_ANCHOR.MIDDLE
tf_e.word_wrap = True
pe = tf_e.paragraphs[0]
pe.alignment = PP_ALIGN.CENTER
pe.text = "EXTERNAL ENTITY\nRequester / Webhook"
pe.font.name = FONT_SANS
pe.font.size = Pt(14)
pe.font.bold = True
pe.font.color.rgb = COLOR_WHITE

add_arrow(slide5, Inches(4.5), Inches(4.15), Inches(0.6), Inches(0.4), color=COLOR_TEAL_ACCENT)

# 2. Process 1: Evidence Spec Planner
proc1 = add_rounded_box(slide5, Inches(5.2), Inches(3.4), Inches(3.4), Inches(1.9), bg_color=COLOR_INDIGO_BG, border_color=COLOR_INDIGO_BORDER)
tf_p1 = proc1.text_frame
tf_p1.vertical_anchor = MSO_ANCHOR.MIDDLE
tf_p1.word_wrap = True
p1 = tf_p1.paragraphs[0]
p1.alignment = PP_ALIGN.CENTER
p1.text = "Process 1.0\nEVIDENCE SPEC PLANNER\n(Infers Required Spec Items)"
p1.font.name = FONT_SANS
p1.font.size = Pt(13)
p1.font.bold = True
p1.font.color.rgb = COLOR_INDIGO_ACCENT

add_arrow(slide5, Inches(8.7), Inches(4.15), Inches(0.6), Inches(0.4), color=COLOR_TEAL_ACCENT)

# 3. Process 2: Gap Auditor & Gatekeeper
proc2 = add_rounded_box(slide5, Inches(9.4), Inches(3.4), Inches(3.6), Inches(1.9), bg_color=COLOR_RED_BG, border_color=COLOR_RED_BORDER)
tf_p2 = proc2.text_frame
tf_p2.vertical_anchor = MSO_ANCHOR.MIDDLE
tf_p2.word_wrap = True
p2 = tf_p2.paragraphs[0]
p2.alignment = PP_ALIGN.CENTER
p2.text = "Process 2.0\nZERO-HALLUCINATION GATE\n(Cross-checks Gaps & Blocks)"
p2.font.name = FONT_SANS
p2.font.size = Pt(13)
p2.font.bold = True
p2.font.color.rgb = COLOR_RED

# Branch: Complete -> Green Arrow to Decision
add_arrow(slide5, Inches(13.1), Inches(4.15), Inches(0.6), Inches(0.4), color=COLOR_GREEN)

# 4. Process 5: Deliberator & Execution
proc5 = add_rounded_box(slide5, Inches(13.8), Inches(3.4), Inches(4.5), Inches(1.9), bg_color=COLOR_GREEN_BG, border_color=COLOR_GREEN_BORDER)
tf_p5 = proc5.text_frame
tf_p5.vertical_anchor = MSO_ANCHOR.MIDDLE
tf_p5.word_wrap = True
p5 = tf_p5.paragraphs[0]
p5.alignment = PP_ALIGN.CENTER
p5.text = "Process 5.0\nDELIBERATION & ACTION DISPATCH\n(Approved • PO Created • Ledger Committed)"
p5.font.name = FONT_SANS
p5.font.size = Pt(13)
p5.font.bold = True
p5.font.color.rgb = COLOR_GREEN

# Down Arrow from Process 2 to Self-Healing
add_down_arrow(slide5, Inches(11.0), Inches(5.4), Inches(0.4), Inches(0.5), color=COLOR_AMBER)

# 5. Process 3: Autonomous Multi-Source Self-Healing (Lower Row)
proc3 = add_rounded_box(slide5, Inches(8.5), Inches(6.0), Inches(5.4), Inches(1.9), bg_color=COLOR_TEAL_BG, border_color=COLOR_TEAL_BORDER)
tf_p3 = proc3.text_frame
tf_p3.margin_left = Inches(0.25)
tf_p3.margin_top = Inches(0.15)
tf_p3.word_wrap = True
p3 = tf_p3.paragraphs[0]
p3.text = "Process 3.0: AUTONOMOUS SELF-HEALING RETRIEVAL"
p3.font.name = FONT_SANS
p3.font.size = Pt(13)
p3.font.bold = True
p3.font.color.rgb = COLOR_TEAL_ACCENT
p3.space_after = Pt(2)

ds_items = [
    "• D1: Google Drive Vault (Indexed PDFs, SOC2, Appraisals)",
    "• D2: Corporate Mailbox (Gmail / M365 Exchange Threads)",
    "• D3: NetSuite ERP Ledger (Vendor Reliability & Financials)",
    "• D4: External Registries (D&B, OFAC Sanctions, SEC Edgar)"
]
for ds in ds_items:
    pds = tf_p3.add_paragraph()
    pds.text = ds
    pds.font.name = FONT_SANS
    pds.font.size = Pt(11)
    pds.font.color.rgb = COLOR_BODY_TEXT

# Left Arrow to Process 4: Precision HITL
arrow_left = slide5.shapes.add_shape(MSO_SHAPE.LEFT_ARROW, Inches(7.8), Inches(6.8), Inches(0.6), Inches(0.4))
arrow_left.fill.solid()
arrow_left.fill.fore_color.rgb = COLOR_AMBER
arrow_left.line.fill.background()

# 6. Process 4: Precision Human-in-the-Loop Micro-Ask
proc4 = add_rounded_box(slide5, Inches(1.4), Inches(6.0), Inches(6.3), Inches(1.9), bg_color=COLOR_AMBER_BG, border_color=COLOR_AMBER_BORDER)
tf_p4 = proc4.text_frame
tf_p4.margin_left = Inches(0.3)
tf_p4.margin_top = Inches(0.15)
tf_p4.word_wrap = True
p4 = tf_p4.paragraphs[0]
p4.text = "Process 4.0: PRECISION HITL MICRO-REQUEST"
p4.font.name = FONT_SANS
p4.font.size = Pt(13)
p4.font.bold = True
p4.font.color.rgb = COLOR_AMBER
p4.space_after = Pt(3)

p4_b1 = tf_p4.add_paragraph()
p4_b1.text = "• Identifies EXACT missing item (e.g. Budget Sign-Off from VP Finance)"
p4_b1.font.name = FONT_SANS
p4_b1.font.size = Pt(11.5)
p4_b1.font.color.rgb = COLOR_BODY_TEXT

p4_b2 = tf_p4.add_paragraph()
p4_b2.text = "• Dispatches targeted Slack card with 1-click Approve/Reject button"
p4_b2.font.name = FONT_SANS
p4_b2.font.size = Pt(11.5)
p4_b2.font.color.rgb = COLOR_BODY_TEXT

p4_b3 = tf_p4.add_paragraph()
p4_b3.text = "• Takes 15 seconds instead of traditional 30-minute review cycles"
p4_b3.font.name = FONT_SANS
p4_b3.font.size = Pt(11.5)
p4_b3.font.color.rgb = COLOR_BODY_TEXT

# Bottom Process 6: Telemetry & Process Mining
proc6 = add_rounded_box(slide5, Inches(1.4), Inches(8.2), Inches(16.9), Inches(1.6), bg_color=COLOR_DARK_SLATE, border_color=None)
tf_p6 = proc6.text_frame
tf_p6.vertical_anchor = MSO_ANCHOR.MIDDLE
tf_p6.margin_left = Inches(0.4)
tf_p6.margin_right = Inches(0.4)
p = tf_p6.paragraphs[0]
p.text = "Process 6.0: TELEMETRY MINING & CONTINUOUS PROCESS OPTIMIZATION"
p.font.name = FONT_SANS
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_TITLE_CYAN
p.space_after = Pt(2)

p2 = tf_p6.add_paragraph()
p2.text = "Every blocked gate, retrieved document, and human micro-interaction is logged. Telemetry detects organizational patterns (e.g. '70% of delays are missing budget sign-off') and proposes automatic intake form redesign to prevent future blocks."
p2.font.name = FONT_SANS
p2.font.size = Pt(12)
p2.font.color.rgb = COLOR_WHITE

print("Slide 5 updated with professional Data Flow Diagram.")

# ==============================================================================
# SLIDE 6: Screenshot of Your Project & Visual UI Studio
# ==============================================================================
slide6 = prs.slides[5]

while len(slide6.shapes) > 3:
    sp = slide6.shapes[len(slide6.shapes)-1]._element
    sp.getparent().remove(sp)

# Top Live Demo Link Pill
link_card = add_rounded_box(slide6, Inches(1.12), Inches(2.55), Inches(17.76), Inches(0.65), bg_color=COLOR_INDIGO_BG, border_color=COLOR_INDIGO_ACCENT)
tf_link = link_card.text_frame
tf_link.vertical_anchor = MSO_ANCHOR.MIDDLE
tf_link.margin_left = Inches(0.4)
p_link = tf_link.paragraphs[0]
r_l1 = p_link.add_run()
r_l1.text = "🌐 LIVE CLOUD APPLICATION: "
r_l1.font.name = FONT_SANS
r_l1.font.size = Pt(14)
r_l1.font.bold = True
r_l1.font.color.rgb = COLOR_INDIGO_ACCENT

r_l2 = p_link.add_run()
r_l2.text = "https://static-outstanding-palm-clarke.trycloudflare.com  [⚡ Fast <50ms | 8 Domains | Zero Hallucination]"
r_l2.font.name = FONT_SANS
r_l2.font.size = Pt(14)
r_l2.font.bold = True
r_l2.font.color.rgb = COLOR_DARK_SLATE

# Browser Frame Outer Mockup
frame = add_rounded_box(slide6, Inches(1.12), Inches(3.35), Inches(17.76), Inches(6.9), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)

# Browser top bar
topbar = add_rounded_box(slide6, Inches(1.12), Inches(3.35), Inches(17.76), Inches(0.55), bg_color=COLOR_DARK_SLATE, border_color=None)
tf_tb = topbar.text_frame
tf_tb.vertical_anchor = MSO_ANCHOR.MIDDLE
tf_tb.margin_left = Inches(0.4)
p = tf_tb.paragraphs[0]
p.text = "🔴 🟡 🟢   https://static-outstanding-palm-clarke.trycloudflare.com  —  Decision Completeness Engine Visual Studio"
p.font.name = FONT_SANS
p.font.size = Pt(12)
p.font.color.rgb = RGBColor(226, 232, 240)

# Pipeline Stepper Mockup
stepper = add_rounded_box(slide6, Inches(1.3), Inches(4.05), Inches(17.4), Inches(0.75), bg_color=COLOR_GRAY_BG, border_color=COLOR_CARD_BORDER)
tf_step = stepper.text_frame
tf_step.vertical_anchor = MSO_ANCHOR.MIDDLE
tf_step.word_wrap = True
ps = tf_step.paragraphs[0]
ps.alignment = PP_ALIGN.CENTER
steps_str = "[01 Intake ✓]  ➜  [02 Plan ✓]  ➜  [03 Audit ✓]  ➜  [04 Gate Block ⛔]  ➜  [05 Self-Heal ✨]  ➜  [06 HITL 👤]  ➜  [07 Verdict 🎯]  ➜  [08 Learn 📊]"
ps.text = steps_str
ps.font.name = FONT_SANS
ps.font.size = Pt(12.5)
ps.font.bold = True
ps.font.color.rgb = COLOR_INDIGO_ACCENT

# UI Columns: Left = Evidence Dossier Matrix; Right = Gatekeeper & Verdict Card
# Left Card: Evidence Matrix
col_mat = add_rounded_box(slide6, Inches(1.3), Inches(4.95), Inches(8.5), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
tf_cm = col_mat.text_frame
tf_cm.margin_left = Inches(0.3)
tf_cm.margin_right = Inches(0.3)
tf_cm.margin_top = Inches(0.2)
tf_cm.word_wrap = True

p = tf_cm.paragraphs[0]
p.text = "EVIDENCE SPECIFICATION MATRIX (LIVE DOSSIER)"
p.font.name = FONT_SANS
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_DARK_SLATE
p.space_after = Pt(8)

evidence_ui = [
    ("Competitive Price Benchmark", "VERIFIED (95%)", "Direct vendor quotation comparison", COLOR_GREEN_BG, COLOR_GREEN),
    ("Delivery Timeline SLA Commitment", "VERIFIED (92%)", "14-day turnaround SLA verified", COLOR_GREEN_BG, COLOR_GREEN),
    ("SOC2 Type II Security Certificate", "✨ SELF-HEALED", "Retrieved from Corporate Drive Vault", COLOR_TEAL_BG, COLOR_TEAL_ACCENT),
    ("Past Delivery Track Record (98%)", "✨ SELF-HEALED", "Retrieved from NetSuite ERP Ledger", COLOR_TEAL_BG, COLOR_TEAL_ACCENT),
    ("Budget Sign-Off (VP Finance)", "👤 HITL SIGNED", "Approved in 15s via targeted Slack card", COLOR_AMBER_BG, COLOR_AMBER)
]

for title, status, src, bg_c, acc_c in evidence_ui:
    p_e = tf_cm.add_paragraph()
    r_t = p_e.add_run()
    r_t.text = f"{title}\n"
    r_t.font.name = FONT_SANS
    r_t.font.size = Pt(11.5)
    r_t.font.bold = True
    r_t.font.color.rgb = COLOR_NAVY_HEADING

    r_s = p_e.add_run()
    r_s.text = f"  [{status}] — {src}"
    r_s.font.name = FONT_SANS
    r_s.font.size = Pt(10.5)
    r_s.font.bold = True
    r_s.font.color.rgb = acc_c
    p_e.space_after = Pt(6)

# Right Card: Verdict, Confidence & Downstream Execution
col_ver = add_rounded_box(slide6, Inches(10.1), Inches(4.95), Inches(8.6), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_GREEN_BORDER)
tf_cv = col_ver.text_frame
tf_cv.margin_left = Inches(0.3)
tf_cv.margin_right = Inches(0.3)
tf_cv.margin_top = Inches(0.2)
tf_cv.word_wrap = True

p = tf_cv.paragraphs[0]
p.text = "GATEKEEPER VERDICT & DOWNSTREAM ACTIONS"
p.font.name = FONT_SANS
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_GREEN
p.space_after = Pt(6)

p_score = tf_cv.add_paragraph()
p_score.text = "Completeness Score: 100% (All Critical Requirements Met)\nVerdict: APPROVED  |  Confidence Score: 97%"
p_score.font.name = FONT_SANS
p_score.font.size = Pt(12)
p_score.font.bold = True
p_score.font.color.rgb = COLOR_DARK_SLATE
p_score.space_after = Pt(10)

actions_ui = [
    ("⚡ Action 1: ERP Purchase Order Dispatched", "PO #PO-88421 committed to NetSuite with line-item schedule."),
    ("💬 Action 2: Precision Slack Alert Sent", "Requester and procurement channel notified in real-time."),
    ("🔒 Action 3: Cryptographic Audit Ledger", "SHA-256 chain-of-custody hash committed: `0x7f8a9...b34c`.")
]
for title, desc in actions_ui:
    pa = tf_cv.add_paragraph()
    r_t = pa.add_run()
    r_t.text = f"{title}\n"
    r_t.font.name = FONT_SANS
    r_t.font.size = Pt(11.5)
    r_t.font.bold = True
    r_t.font.color.rgb = COLOR_INDIGO_ACCENT
    r_d = pa.add_run()
    r_d.text = f"  {desc}"
    r_d.font.name = FONT_SANS
    r_d.font.size = Pt(10.5)
    r_d.font.color.rgb = COLOR_BODY_TEXT
    pa.space_after = Pt(8)

print("Slide 6 updated with visual browser mockup.")

# ==============================================================================
# SLIDE 7: Others (8 Enterprise Scenarios, Quantifiable ROI & Deliverables)
# ==============================================================================
slide7 = prs.slides[6]

while len(slide7.shapes) > 3:
    sp = slide7.shapes[len(slide7.shapes)-1]._element
    sp.getparent().remove(sp)

col_w = Inches(5.65)
col_gap = Inches(0.4)
c1_l = Inches(1.12)
c2_l = c1_l + col_w + col_gap
c3_l = c2_l + col_w + col_gap

# Col 1: 8 Enterprise Scenarios
card_c1 = add_rounded_box(slide7, c1_l, Inches(2.7), col_w, Inches(7.6), bg_color=COLOR_WHITE, border_color=COLOR_INDIGO_BORDER)
tf_c1 = card_c1.text_frame
tf_c1.margin_left = Inches(0.3)
tf_c1.margin_right = Inches(0.3)
tf_c1.margin_top = Inches(0.3)
tf_c1.word_wrap = True

p = tf_c1.paragraphs[0]
p.text = "8 ENTERPRISE DOMAINS (READY-TO-DEMO)"
p.font.name = FONT_SANS
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_INDIGO_ACCENT
p.space_after = Pt(8)

scenarios = [
    ("1. Hardware Procurement", "$85k Laptops • Recovers SOC2; asks VP."),
    ("2. Commercial Lending", "$250k Apex Revolving • Recovers Form 1120-S."),
    ("3. Executive Hiring", "VP Eng Offer • Recovers Sterling & references."),
    ("4. Healthcare Claims", "$42k Knee Surgery • Recovers op notes & auth."),
    ("5. Corporate Expense", "$14.2k Zurich Dinner • Recovers itemized folio."),
    ("6. Legal SaaS Contract", "VectorFlow AI • Recovers DPA & covenants."),
    ("7. Cloud Firewall Exemption", "Port 9443 Ingress • Recovers partner mTLS cert."),
    ("8. Jumbo Real Estate Mortgage", "$850k Loan • Recovers $1.15M appraisal & W-2s.")
]

for title, desc in scenarios:
    ps = tf_c1.add_paragraph()
    r1 = ps.add_run()
    r1.text = f"{title}: "
    r1.font.name = FONT_SANS
    r1.font.size = Pt(11)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_DARK_SLATE
    r2 = ps.add_run()
    r2.text = desc
    r2.font.name = FONT_SANS
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = COLOR_BODY_TEXT
    ps.space_after = Pt(4)

# Col 2: Big ROI Metrics
card_c2 = add_rounded_box(slide7, c2_l, Inches(2.7), col_w, Inches(7.6), bg_color=COLOR_WHITE, border_color=COLOR_TEAL_BORDER)
tf_c2 = card_c2.text_frame
tf_c2.margin_left = Inches(0.3)
tf_c2.margin_right = Inches(0.3)
tf_c2.margin_top = Inches(0.3)
tf_c2.word_wrap = True

p = tf_c2.paragraphs[0]
p.text = "QUANTIFIABLE BUSINESS VALUE"
p.font.name = FONT_SANS
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_TEAL_ACCENT
p.space_after = Pt(8)

roi_stats = [
    ("90% Turnaround Reduction", "Drops average approval cycles from 2.5 days down to seconds.", COLOR_TEAL_ACCENT),
    ("0% Hallucination Rate", "Zero speculation: strictly halts AI from guessing when data is incomplete.", COLOR_RED),
    ("15s Human Micro-Ask", "Executives never read 40 pages; they answer a 1-click micro-question.", COLOR_AMBER),
    ("88% Autonomous Healing", "Self-heals gaps by searching Drive, Email, and ERP ledgers.", COLOR_GREEN)
]

for stat, desc, col in roi_stats:
    p_st = tf_c2.add_paragraph()
    r_st = p_st.add_run()
    r_st.text = f"{stat}\n"
    r_st.font.name = FONT_SANS
    r_st.font.size = Pt(14)
    r_st.font.bold = True
    r_st.font.color.rgb = col
    
    r_desc = p_st.add_run()
    r_desc.text = desc
    r_desc.font.name = FONT_SANS
    r_desc.font.size = Pt(11)
    r_desc.font.color.rgb = COLOR_BODY_TEXT
    p_st.space_after = Pt(10)

# Col 3: Deliverables & Production Readiness
card_c3 = add_rounded_box(slide7, c3_l, Inches(2.7), col_w, Inches(7.6), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
tf_c3 = card_c3.text_frame
tf_c3.margin_left = Inches(0.3)
tf_c3.margin_right = Inches(0.3)
tf_c3.margin_top = Inches(0.3)
tf_c3.word_wrap = True

p = tf_c3.paragraphs[0]
p.text = "PRODUCTION DELIVERABLES"
p.font.name = FONT_SANS
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_DARK_SLATE
p.space_after = Pt(8)

deliverables_list = [
    ("📦 Importable n8n Workflow", "Full production JSON workflow with AI Agent, Tool & Webhook nodes (`decision_completeness_engine.json`)."),
    ("🧪 Automated Test Suite", "9/9 passing unit & integration tests (`python -m unittest tests/test_engine.py`)."),
    ("☁️ Multi-Cloud Deployment", "Dockerfile, Render (render.yaml), Railway (railway.json), and Vercel configuration ready to deploy."),
    ("🔒 Cryptographic Audit Proof", "SHA-256 chain-of-custody evidence hashing for regulatory compliance and audit readiness.")
]

for title, desc in deliverables_list:
    pd = tf_c3.add_paragraph()
    r1 = pd.add_run()
    r1.text = f"{title}\n"
    r1.font.name = FONT_SANS
    r1.font.size = Pt(12)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_NAVY_HEADING
    r2 = pd.add_run()
    r2.text = desc
    r2.font.name = FONT_SANS
    r2.font.size = Pt(11)
    r2.font.color.rgb = COLOR_BODY_TEXT
    pd.space_after = Pt(10)

print("Slide 7 updated with 3-column visual layout.")

# Save presentation
prs.save(OUTPUT_PATH)
shutil.copyfile(OUTPUT_PATH, STATIC_PATH)
print(f"ALL DONE! Saved to {OUTPUT_PATH} and {STATIC_PATH}.")
