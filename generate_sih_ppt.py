import collections.abc
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parent
OUTPUT_PPTX = ROOT / "MANGANEX_AI_SIH2026_Official_Presentation.pptx"

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Professional Color Palette matching Ministry of Steel & Space Tech
    NAVY_DARK = RGBColor(11, 19, 43)        # #0B132B
    STEEL_BLUE = RGBColor(28, 42, 74)       # #1C2A4A
    CYAN_ACCENT = RGBColor(0, 168, 232)     # #00A8E8
    ORANGE_ACCENT = RGBColor(247, 127, 0)   # #F77F00
    WHITE = RGBColor(255, 255, 255)
    TEXT_LIGHT = RGBColor(226, 232, 240)    # #E2E8F0
    TEXT_MUTED = RGBColor(148, 163, 184)    # #94A3B8
    CARD_BG = RGBColor(19, 29, 49)          # #131D31
    CARD_BORDER = RGBColor(41, 58, 88)      # #293A58
    GREEN_ACCENT = RGBColor(16, 185, 129)   # #10B981

    blank_layout = prs.slide_layouts[6]
    
    def add_header_footer(slide, title_text, slide_num):
        # Header banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(9.5), Inches(0.8))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT
        p.font.name = "Arial"
        
        # SIH Logo Header Tag on Top Right
        sih_box = slide.shapes.add_textbox(Inches(10.5), Inches(0.35), Inches(2.2), Inches(0.8))
        tf_sih = sih_box.text_frame
        tf_sih.word_wrap = True
        p_sih = tf_sih.paragraphs[0]
        p_sih.alignment = PP_ALIGN.RIGHT
        p_sih.text = "SMART INDIA HACKATHON 2026"
        p_sih.font.size = Pt(9)
        p_sih.font.bold = True
        p_sih.font.color.rgb = ORANGE_ACCENT
        p_sih.font.name = "Arial"
        
        # Sub-header line
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.15), Inches(11.73), Inches(0.02)
        )
        line.fill.solid()
        line.fill.fore_color.rgb = CARD_BORDER
        line.line.color.rgb = CARD_BORDER

        # Footer
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.73), Inches(0.35))
        tf_f = footer_box.text_frame
        p_f = tf_f.paragraphs[0]
        p_f.text = f"@SIH Idea submission- Template | PS 26009: Ministry of Steel | Slide {slide_num}"
        p_f.font.size = Pt(9)
        p_f.font.color.rgb = TEXT_MUTED
        p_f.font.name = "Arial"

    # =========================================================================
    # SLIDE 1: TITLE PAGE
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY_DARK
    bg1.line.fill.background()

    # Top Tag
    top_tag = slide1.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.5))
    p_tag = top_tag.text_frame.paragraphs[0]
    p_tag.text = "SMART INDIA HACKATHON 2026 — IDEA SUBMISSION"
    p_tag.font.size = Pt(13)
    p_tag.font.bold = True
    p_tag.font.color.rgb = ORANGE_ACCENT
    p_tag.font.name = "Arial"

    # Main Project Title
    proj_title = slide1.shapes.add_textbox(Inches(0.8), Inches(1.0), Inches(11.7), Inches(1.1))
    p_t = proj_title.text_frame.paragraphs[0]
    p_t.text = "MANGANEX AI"
    p_t.font.size = Pt(36)
    p_t.font.bold = True
    p_t.font.color.rgb = CYAN_ACCENT
    p_t.font.name = "Arial"

    p_sub = proj_title.text_frame.add_paragraph()
    p_sub.text = "AI/ML & Space Technology Platform for Manganese Exploration & Production Shortfall Forecasting"
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = TEXT_LIGHT
    p_sub.font.name = "Arial"

    # Details Card (Left Container)
    details_card = slide1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.3), Inches(7.0), Inches(4.5)
    )
    details_card.fill.solid()
    details_card.fill.fore_color.rgb = CARD_BG
    details_card.line.color.rgb = CARD_BORDER

    tf_d = details_card.text_frame
    tf_d.word_wrap = True
    tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = Inches(0.35)

    entries = [
        ("• Problem Statement ID –", "26009"),
        ("• Problem Statement Title –", "Using AI/ML and Space Technology to Identify Manganese Reserves and Overcome Production Shortfalls"),
        ("• Organization –", "Ministry of Steel, Government of India"),
        ("• Theme –", "Smart Automation"),
        ("• PS Category –", "Software"),
        ("• Team ID –", "[Enter Your Team ID]"),
        ("• Team Name –", "[Enter Your Team Name]")
    ]

    for idx, (label, val) in enumerate(entries):
        p = tf_d.paragraphs[0] if idx == 0 else tf_d.add_paragraph()
        p.space_after = Pt(8)
        run_l = p.add_run()
        run_l.text = f"{label} "
        run_l.font.bold = True
        run_l.font.size = Pt(11)
        run_l.font.color.rgb = CYAN_ACCENT
        run_l.font.name = "Arial"

        run_v = p.add_run()
        run_v.text = val
        run_v.font.bold = (idx < 5)
        run_v.font.size = Pt(11)
        run_v.font.color.rgb = WHITE if idx < 5 else ORANGE_ACCENT
        run_v.font.name = "Arial"

    # Right Highlights Card
    right_card = slide1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.1), Inches(2.3), Inches(4.4), Inches(4.5)
    )
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = STEEL_BLUE
    right_card.line.color.rgb = CYAN_ACCENT

    tf_r = right_card.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = Inches(0.35)

    p_rh = tf_r.paragraphs[0]
    p_rh.text = "EXECUTIVE SUMMARY"
    p_rh.font.size = Pt(13)
    p_rh.font.bold = True
    p_rh.font.color.rgb = ORANGE_ACCENT

    highlights = [
        "🛰️ Space Tech Integration: Ingests Sentinel-2 MSI SWIR-1/2 & Landsat-8/9 Thermal LST bands.",
        "🤖 AI/ML Predictive Models: Random Forest Regressors & Classifiers trained on 592 verified Indian mining zones.",
        "📊 Dual Core Objectives: Accelerated greenfield manganese deposit discovery + Early-warning production shortfall mitigation.",
        "🏛️ National Impact: Directly addresses India's mineral security & import substitution for steel & EV battery industries."
    ]

    for h in highlights:
        p = tf_r.add_paragraph()
        p.space_before = Pt(10)
        p.text = h
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 2: PROPOSED SOLUTION
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    bg2 = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg2.fill.solid()
    bg2.fill.fore_color.rgb = NAVY_DARK
    bg2.line.fill.background()
    add_header_footer(slide2, "PROPOSED SOLUTION: MANGANEX AI", 2)

    # 3 Strategic Solution Pillars (Cards)
    pillar_data = [
        ("1. Detailed Explanation of Proposed Solution", [
            "• End-to-End Decision Support System: Fuses Earth Observation (EO) satellite multispectral data with geological host rock lithology and historical operational data.",
            "• Space Tech Feature Extraction: Real-time calculation of Sentinel-2 Ferrous Oxide (B11/B8A), Hydrothermal Clay Index (B11/B12), NDVI Canopy Stress, and Landsat Thermal LST.",
            "• Predictive Multi-Model ML Ensemble: Dedicated Random Forest engines for In-situ Potential Estimation, Extraction Shortfall Detection, and Multi-hazard Risk Classification.",
            "• Interactive 3D GIS Command Center: 5-page decision dashboard featuring PyDeck spatial heatmaps and scenario simulation for mine managers."
        ], CYAN_ACCENT),
        ("2. How It Addresses Problem Statement 26009", [
            "• Eliminates Blind Exploration: Replaces high-cost random grid-drilling by prioritizing high-confidence satellite spectral anomaly clusters (60% faster turnaround).",
            "• Overcomes Production Deficits: Detects mine-level extraction gaps 3 to 6 months in advance by correlating equipment efficiency, rainfall, and grade depletion.",
            "• Quantitative Decision Support: Generates actionable recommendations for domestic quota reallocation, equipment overhaul, and GSI/MOIL drilling targets."
        ], ORANGE_ACCENT),
        ("3. Innovation & Uniqueness of Solution", [
            "• Transparent Explainable AI (XAI): Decomposes composite prospectivity scores into exact mathematical signal contributions—no 'black-box' decisions.",
            "• Multi-Hazard Risk Scoring: Simultaneously models geological, weather-induced, and mechanical bottlenecks at 97.5% classification accuracy.",
            "• Indian Manganese Belts Calibration: Pre-calibrated for Sausar (MP/MH), Bonai-Keonjhar (Odisha), Sandur (Karnataka), and Kodurite (AP) series."
        ], GREEN_ACCENT),
    ]

    for idx, (p_title, p_points, border_col) in enumerate(pillar_data):
        c_left = Inches(0.8 + idx * 4.0)
        card = slide2.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(1.5), Inches(3.75), Inches(5.2)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = border_col
        card.line.width = Pt(1.5)

        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = Inches(0.25)

        p_h = tf_c.paragraphs[0]
        p_h.text = p_title
        p_h.font.size = Pt(12)
        p_h.font.bold = True
        p_h.font.color.rgb = border_col

        for pt in p_points:
            p_b = tf_c.add_paragraph()
            p_b.space_before = Pt(8)
            p_b.text = pt
            p_b.font.size = Pt(9.5)
            p_b.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 3: TECHNICAL APPROACH
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    bg3 = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg3.fill.solid()
    bg3.fill.fore_color.rgb = NAVY_DARK
    bg3.line.fill.background()
    add_header_footer(slide3, "TECHNICAL APPROACH & SYSTEM ARCHITECTURE", 3)

    # Left Container: Tech Stack
    tech_card = slide3.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(4.3), Inches(5.2)
    )
    tech_card.fill.solid()
    tech_card.fill.fore_color.rgb = CARD_BG
    tech_card.line.color.rgb = CARD_BORDER

    tf_t = tech_card.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = Inches(0.25)

    p_th = tf_t.paragraphs[0]
    p_th.text = "TECHNOLOGIES & FRAMEWORKS"
    p_th.font.size = Pt(12)
    p_th.font.bold = True
    p_th.font.color.rgb = CYAN_ACCENT

    tech_items = [
        ("Core Language", "Python 3.10+ (Data Science / Geospatial / ML)"),
        ("Space & EO Data", "Sentinel-2 MSI (SWIR/NIR), Landsat-8/9 (TIRS LST), SRTM 30m DEM"),
        ("Machine Learning", "Scikit-Learn (Random Forest Regressors & Classifiers), Joblib, NumPy, Pandas"),
        ("Geospatial & 3D GIS", "PyDeck (WebGL 3D Geospatial Engine), Altair (Declarative Statistical Visualizations)"),
        ("Dashboard & UX", "Streamlit Multi-Page Enterprise Architecture with Dark Theme UI"),
        ("Hardware Needs", "Standard Cloud / Edge Compute (Lightweight inference < 80ms latency)")
    ]

    for lbl, val in tech_items:
        p = tf_t.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = f"• {lbl}: "
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = ORANGE_ACCENT
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = TEXT_LIGHT

    # Right Container: Architecture Flow & Methodology
    arch_card = slide3.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.3), Inches(1.5), Inches(7.23), Inches(5.2)
    )
    arch_card.fill.solid()
    arch_card.fill.fore_color.rgb = CARD_BG
    arch_card.line.color.rgb = CYAN_ACCENT

    tf_a = arch_card.text_frame
    tf_a.word_wrap = True
    tf_a.margin_left = tf_a.margin_right = tf_a.margin_top = Inches(0.25)

    p_ah = tf_a.paragraphs[0]
    p_ah.text = "METHODOLOGY & PIPELINE PROCESS"
    p_ah.font.size = Pt(12)
    p_ah.font.bold = True
    p_ah.font.color.rgb = CYAN_ACCENT

    steps = [
        ("Step 1: Space & Multispectral Ingestion", "Acquires Sentinel-2 SWIR-1/2 & Landsat Thermal radiance bands over Indian manganese belts. Computes Ferrous Index (B11/B8A), Clay Index (B11/B12), and NDVI."),
        ("Step 2: Geological & Lithological Fusion", "Integrates SRTM DEM elevation/slope with GSI Sausar/Gondite formation lithology indices and historical extraction baselines."),
        ("Step 3: AI Inference & Prospectivity Scoring", "Calculates composite prospectivity score & confidence rating. Random Forest Regressor predicts in-situ manganese potential tonnage."),
        ("Step 4: Predictive Shortfall & Risk Classification", "Simulates extraction slippage based on equipment uptime, weather, and ore grade to forecast shortfalls 3-6 months in advance."),
        ("Step 5: Explainable AI & Decision Dashboard", "Presents 3D GIS heatmaps, transparent XAI driver breakdowns, and automated policy/operational recommendations for Ministry & Mine Managers.")
    ]

    for s_title, s_desc in steps:
        p = tf_a.add_paragraph()
        p.space_before = Pt(6)
        r_st = p.add_run()
        r_st.text = f"{s_title}\n"
        r_st.font.bold = True
        r_st.font.size = Pt(9.5)
        r_st.font.color.rgb = GREEN_ACCENT
        r_sd = p.add_run()
        r_sd.text = s_desc
        r_sd.font.size = Pt(8.8)
        r_sd.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 4: FEASIBILITY AND VIABILITY
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    bg4 = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg4.fill.solid()
    bg4.fill.fore_color.rgb = NAVY_DARK
    bg4.line.fill.background()
    add_header_footer(slide4, "FEASIBILITY AND VIABILITY ANALYSIS", 4)

    # 3 Structured Columns
    col_w = Inches(3.75)
    
    # 1. Feasibility
    feas_card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), col_w, Inches(5.2))
    feas_card.fill.solid()
    feas_card.fill.fore_color.rgb = CARD_BG
    feas_card.line.color.rgb = CYAN_ACCENT
    tf_f1 = feas_card.text_frame
    tf_f1.word_wrap = True
    tf_f1.margin_left = tf_f1.margin_right = tf_f1.margin_top = Inches(0.25)
    
    p = tf_f1.paragraphs[0]
    p.text = "1. Feasibility Analysis"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    
    f_pts = [
        "• Technical Feasibility: Utilizes proven, open-access Copernicus (Sentinel-2) and USGS (Landsat) satellite data pipelines with zero licensing costs.",
        "• Operational Viability: Seamless web-based deployment requires no specialized on-premise hardware; accessible on desktop and tablet devices.",
        "• Economic Viability: Payback period under 6 months by eliminating unnecessary exploratory exploratory drillholes ($50k–$150k saved per site).",
        "• Scalability: Pipeline readily extends to Iron Ore, Bauxite, and Chromite belts across India."
    ]
    for pt in f_pts:
        p = tf_f1.add_paragraph()
        p.space_before = Pt(8)
        p.text = pt
        p.font.size = Pt(9.3)
        p.font.color.rgb = TEXT_LIGHT

    # 2. Challenges & Risks
    risk_card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.5), col_w, Inches(5.2))
    risk_card.fill.solid()
    risk_card.fill.fore_color.rgb = CARD_BG
    risk_card.line.color.rgb = ORANGE_ACCENT
    tf_f2 = risk_card.text_frame
    tf_f2.word_wrap = True
    tf_f2.margin_left = tf_f2.margin_right = tf_f2.margin_top = Inches(0.25)
    
    p = tf_f2.paragraphs[0]
    p.text = "2. Potential Challenges & Risks"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ORANGE_ACCENT
    
    r_pts = [
        "• Cloud Cover & Monsoon Noise: Dense cloud cover during Indian monsoon (June–Sept) can obscure optical/SWIR satellite observations.",
        "• Dense Vegetation Camouflage: Thick forest canopy over unexplored terrains (e.g. Eastern Ghats) suppresses optical rock signatures.",
        "• Dynamic Mine Telemetry Gaps: Sub-optimal digital infrastructure or missing telemetry in smaller private mine leaseholds.",
        "• Geological Ground-Truth Discrepancy: Satellite surface indices require sub-surface drill core validation."
    ]
    for pt in r_pts:
        p = tf_f2.add_paragraph()
        p.space_before = Pt(8)
        p.text = pt
        p.font.size = Pt(9.3)
        p.font.color.rgb = TEXT_LIGHT

    # 3. Mitigation Strategies
    strat_card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.5), col_w, Inches(5.2))
    strat_card.fill.solid()
    strat_card.fill.fore_color.rgb = CARD_BG
    strat_card.line.color.rgb = GREEN_ACCENT
    tf_f3 = strat_card.text_frame
    tf_f3.word_wrap = True
    tf_f3.margin_left = tf_f3.margin_right = tf_f3.margin_top = Inches(0.25)
    
    p = tf_f3.paragraphs[0]
    p.text = "3. Mitigation Strategies"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT
    
    s_pts = [
        "• Multi-Temporal Cloud Masking: Merges cloud-free dry season composites and integrates Sentinel-1 SAR (Synthetic Aperture Radar) for all-weather penetration.",
        "• Biogeochemical Canopy Stress Modeling: Converts suppressed NDVI into a positive mineralization proxy to penetrate vegetation cover.",
        "• Standardized Ingestion APIs: Lightweight Excel/CSV/JSON bulk data adapters allow seamless integration with legacy ERP and mine dispatch logs.",
        "• JORC/UNFC Compliance Positioning: Positioned as G4/G3 exploration prioritization tool rather than certified reserve replacement."
    ]
    for pt in s_pts:
        p = tf_f3.add_paragraph()
        p.space_before = Pt(8)
        p.text = pt
        p.font.size = Pt(9.3)
        p.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 5: IMPACT AND BENEFITS
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    bg5 = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg5.fill.solid()
    bg5.fill.fore_color.rgb = NAVY_DARK
    bg5.line.fill.background()
    add_header_footer(slide5, "IMPACT AND BENEFITS TO THE NATION", 5)

    # 4 Impact Quadrants
    quads = [
        ("🏛️ Ministry of Steel & Strategic Security", [
            "• Import Substitution: Reduces high-grade manganese import dependency for domestic blast furnaces and specialized steel mills.",
            "• National Reserve Buffering: Provides real-time visibility into domestic supply deficits to trigger strategic stockpiling.",
            "• Electric Vehicle (EV) Ecosystem: Safeguards domestic raw material security for emerging Manganese-rich Li-ion cathode precursors (NMC)."
        ], CYAN_ACCENT, Inches(0.8), Inches(1.5)),
        
        ("💰 Economic & Industrial Benefits", [
            "• 60% Faster Exploration Cycle: Accelerates mineral reconnaissance from years to weeks, speeding up commercial mining lease auctions.",
            "• Multimillion-Dollar Cost Savings: Minimizes exploratory drilling capital waste by targeting pre-screened satellite alteration zones.",
            "• Optimized Mine Fleet Output: Early shortfall alerts prevent production bottlenecks and stabilize domestic supply prices."
        ], GREEN_ACCENT, Inches(6.8), Inches(1.5)),

        ("🌱 Environmental & Social Benefits", [
            "• Non-Invasive Mineral Reconnaissance: Reduces destructive surface trenching and premature forest clearing during initial exploration phases.",
            "• Carbon Footprint Reduction: Minimizes heavy exploration rig mobilization across sensitive ecological regions.",
            "• Regional Job Creation: Fosters sustainable mining downstream industries and high-tech geospatial employment in mining districts."
        ], ORANGE_ACCENT, Inches(0.8), Inches(4.2)),

        ("🎯 Quantitative Impact Targets", [
            "• > 60% Reduction in greenfield mineral discovery turnaround time.",
            "• 3-6 Months early warning for mine-level production deficits.",
            "• 97.5% Accuracy in multi-hazard operational risk classification.",
            "• 592 Critical mining zones actively monitored across 6 Indian states."
        ], RGBColor(168, 85, 247), Inches(6.8), Inches(4.2)),
    ]

    for title_q, pts_q, border_q, l_q, t_q in quads:
        q_card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l_q, t_q, Inches(5.75), Inches(2.5))
        q_card.fill.solid()
        q_card.fill.fore_color.rgb = CARD_BG
        q_card.line.color.rgb = border_q
        q_card.line.width = Pt(1.5)
        
        tf_q = q_card.text_frame
        tf_q.word_wrap = True
        tf_q.margin_left = tf_q.margin_right = tf_q.margin_top = Inches(0.2)

        p = tf_q.paragraphs[0]
        p.text = title_q
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = border_q

        for pt in pts_q:
            p_b = tf_q.add_paragraph()
            p_b.space_before = Pt(4)
            p_b.text = pt
            p_b.font.size = Pt(9.0)
            p_b.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 6: RESEARCH AND REFERENCES
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    bg6 = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg6.fill.solid()
    bg6.fill.fore_color.rgb = NAVY_DARK
    bg6.line.fill.background()
    add_header_footer(slide6, "RESEARCH, REFERENCES AND DATA SOURCES", 6)

    ref_card = slide6.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.73), Inches(5.2)
    )
    ref_card.fill.solid()
    ref_card.fill.fore_color.rgb = CARD_BG
    ref_card.line.color.rgb = CARD_BORDER

    tf_ref = ref_card.text_frame
    tf_ref.word_wrap = True
    tf_ref.margin_left = tf_ref.margin_right = tf_ref.margin_top = Inches(0.3)

    p_rh = tf_ref.paragraphs[0]
    p_rh.text = "ACADEMIC, GEOLOGICAL & SATELLITE REFERENCES"
    p_rh.font.size = Pt(13)
    p_rh.font.bold = True
    p_rh.font.color.rgb = CYAN_ACCENT

    references = [
        ("1. Geological Survey of India (GSI) & Ministry of Mines:", 
         "• Indian Minerals Yearbook (Manganese Ore Chapter) & National Mineral Exploration Policy (NMEP).\n"
         "• United Nations Framework Classification (UNFC-1997 / UNFC-2009) for mineral reserves & resources."),
        
        ("2. Earth Observation & Satellite Multispectral Remote Sensing:", 
         "• European Space Agency (ESA) Copernicus Sentinel-2 MSI Spectral Band Formulations for Hydrothermal Alteration Mapping (Band 11 SWIR-1 / Band 12 SWIR-2 & Band 11 / Band 8A Ferrous Oxide Ratio).\n"
         "• USGS / NASA Landsat-8/9 Thermal Infrared Sensor (TIRS) Split-Window Land Surface Temperature (LST) Algorithms.\n"
         "• NASA / ISRO Shuttle Radar Topography Mission (SRTM) 30-meter Digital Elevation Models (DEM)."),
        
        ("3. Machine Learning & Explainable AI (XAI) Benchmarks:", 
         "• Breiman, L. (2001). 'Random Forests', Machine Learning, 45(1), 5-32 (Applied for Regression & Multi-hazard Classification).\n"
         "• Lundberg, S. M., & Lee, S. I. 'A Unified Approach to Interpreting Model Predictions' (Explainable AI driver decomposition principles).\n"
         "• Scikit-Learn Machine Learning Library (v1.4+) & Streamlit Enterprise Framework (v1.40+)."),
        
        ("4. Working Prototype Codebase & Live Interactive Repository:", 
         "• MANGANEX AI Full Working Repository: D:\\2nd move from os\\d\\MANGANEX_AI_SIHPOLISH\n"
         "• Live Interactive Decision Dashboard: http://localhost:8502 (5-Module Architecture)")
    ]

    for title_r, text_r in references:
        p = tf_ref.add_paragraph()
        p.space_before = Pt(8)
        r_t = p.add_run()
        r_t.text = f"{title_r}\n"
        r_t.font.bold = True
        r_t.font.size = Pt(10)
        r_t.font.color.rgb = ORANGE_ACCENT

        r_b = p.add_run()
        r_b.text = text_r
        r_b.font.size = Pt(9.0)
        r_b.font.color.rgb = TEXT_LIGHT

    # Save presentation
    prs.save(OUTPUT_PPTX)
    print(f"SIH 2026 Presentation generated successfully at: {OUTPUT_PPTX}")

if __name__ == "__main__":
    create_presentation()
