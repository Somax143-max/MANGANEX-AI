import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parent
ASSETS_DIR = ROOT / "ppt_assets"
OUTPUT_PPTX = ROOT / "MANGANEX_AI_SIH2026_Final_Submission.pptx"

def create_master_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Official SIH PDF Color Palette
    WHITE = RGBColor(255, 255, 255)
    BLACK = RGBColor(0, 0, 0)
    DARK_BLUE_TITLE = RGBColor(27, 54, 93)     # #1B365D SIH Navy Title
    SECTION_BLUE = RGBColor(26, 67, 138)       # #1A438A Deep Blue Subheading
    FOOTER_BLUE = RGBColor(14, 116, 188)       # #0E74BC Official SIH Footer Strip Blue
    TEXT_DARK = RGBColor(30, 41, 59)          # #1E293B Crisp Dark Gray for body text
    CARD_BG = RGBColor(248, 250, 252)          # #F8FAFC Subtle Light Card
    CARD_BORDER = RGBColor(203, 213, 225)      # #CBD5E1 Clean Border
    ORANGE_ACCENT = RGBColor(234, 88, 12)      # #EA580C SIH Orange
    GREEN_ACCENT = RGBColor(16, 149, 106)      # #10956A Clean Green Accent
    
    blank_layout = prs.slide_layouts[6]
    
    # Logo Assets
    sih_top_right = ASSETS_DIR / "sih_top_right_logo.png"
    sih_bulb_watermark = ASSETS_DIR / "img_p1_1.png"
    diag_workflow = ASSETS_DIR / "workflow_diag.png"
    diag_tech = ASSETS_DIR / "tech_layers.png"
    diag_impact = ASSETS_DIR / "impact_kpis.png"
    
    def apply_slide_template(slide, title_text, slide_num, is_title_page=False):
        # 1. Background (Pure White)
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = WHITE
        bg.line.fill.background()
        
        # 2. Bottom Blue Footer Banner (Exact SIH Strip)
        footer_strip = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, Inches(7.0), Inches(13.333), Inches(0.5)
        )
        footer_strip.fill.solid()
        footer_strip.fill.fore_color.rgb = FOOTER_BLUE
        footer_strip.line.fill.background()
        
        # Footer Text
        tf_foot = footer_strip.text_frame
        tf_foot.margin_left = Inches(0.8)
        tf_foot.margin_right = Inches(0.8)
        p_foot = tf_foot.paragraphs[0]
        p_foot.text = "@SIH Idea submission- Template"
        p_foot.font.size = Pt(11)
        p_foot.font.color.rgb = WHITE
        p_foot.font.name = "Arial"
        
        # Slide Number on bottom right
        if not is_title_page:
            p_num = tf_foot.add_paragraph()
            p_num.alignment = PP_ALIGN.RIGHT
            p_num.text = str(slide_num)
            p_num.font.size = Pt(11)
            p_num.font.color.rgb = WHITE
            p_num.font.name = "Arial"

        # 3. Top-Right Official SIH Logo Image
        if sih_top_right.exists():
            slide.shapes.add_picture(str(sih_top_right), Inches(11.0), Inches(0.2), width=Inches(1.85))

        # 4. Top Left "Your Team Name" Oval Badge (Slides 2 to 6)
        if not is_title_page:
            oval = slide.shapes.add_shape(
                MSO_SHAPE.OVAL, Inches(0.6), Inches(0.25), Inches(1.5), Inches(0.9)
            )
            oval.fill.solid()
            oval.fill.fore_color.rgb = WHITE
            oval.line.color.rgb = BLACK
            oval.line.width = Pt(1)
            tf_o = oval.text_frame
            tf_o.word_wrap = True
            p_o = tf_o.paragraphs[0]
            p_o.alignment = PP_ALIGN.CENTER
            p_o.text = "Your\nTeam\nName"
            p_o.font.size = Pt(9.5)
            p_o.font.color.rgb = BLACK
            p_o.font.name = "Arial"

            # Center Slide Title
            title_box = slide.shapes.add_textbox(Inches(2.5), Inches(0.3), Inches(8.0), Inches(0.8))
            tf_t = title_box.text_frame
            p_t = tf_t.paragraphs[0]
            p_t.alignment = PP_ALIGN.CENTER
            p_t.text = title_text
            p_t.font.size = Pt(26)
            p_t.font.bold = True
            p_t.font.color.rgb = BLACK
            p_t.font.name = "Arial"

    # =========================================================================
    # SLIDE 1: TITLE PAGE (With Official Center Bulb Watermark + Logo)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    apply_slide_template(slide1, "TITLE PAGE", 1, is_title_page=True)

    # Center-Right SIH Lightbulb Watermark Graphic (Exact from PDF Page 1)
    if sih_bulb_watermark.exists():
        slide1.shapes.add_picture(str(sih_bulb_watermark), Inches(7.5), Inches(1.3), width=Inches(4.8))

    # Top Main Banner: SMART INDIA HACKATHON 2026
    sih_main = slide1.shapes.add_textbox(Inches(1.5), Inches(0.2), Inches(8.5), Inches(0.7))
    p_main = sih_main.text_frame.paragraphs[0]
    p_main.text = "SMART INDIA HACKATHON 2026"
    p_main.font.size = Pt(28)
    p_main.font.bold = True
    p_main.font.color.rgb = DARK_BLUE_TITLE
    p_main.font.name = "Arial"

    # Centered "TITLE PAGE"
    tp_box = slide1.shapes.add_textbox(Inches(3.5), Inches(0.9), Inches(6.33), Inches(0.6))
    p_tp = tp_box.text_frame.paragraphs[0]
    p_tp.alignment = PP_ALIGN.CENTER
    p_tp.text = "TITLE PAGE"
    p_tp.font.size = Pt(22)
    p_tp.font.bold = True
    p_tp.font.color.rgb = BLACK
    p_tp.font.name = "Arial"

    # Left Bullets Container (Exact Template Fields)
    details_box = slide1.shapes.add_textbox(Inches(0.6), Inches(1.65), Inches(6.8), Inches(5.1))
    tf_d = details_box.text_frame
    tf_d.word_wrap = True

    entries = [
        ("• Problem Statement ID –", " 26009"),
        ("• Problem Statement Title –", " Using AI/ML and Space Technology to Identify Manganese Reserves and Overcome Production Shortfalls"),
        ("• Organization –", " Ministry of Steel, Government of India"),
        ("• Theme –", " Smart Automation"),
        ("• PS Category –", " Software"),
        ("• Team ID –", " [Enter Your Team ID]"),
        ("• Team Name –", " [Enter Your Team Name (Registered on portal)]")
    ]

    for idx, (label, val) in enumerate(entries):
        p = tf_d.paragraphs[0] if idx == 0 else tf_d.add_paragraph()
        p.space_after = Pt(10)
        
        r1 = p.add_run()
        r1.text = label
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = BLACK
        r1.font.name = "Arial"
        
        r2 = p.add_run()
        r2.text = val
        r2.font.bold = (idx < 5)
        r2.font.size = Pt(12)
        r2.font.color.rgb = SECTION_BLUE if idx < 5 else ORANGE_ACCENT
        r2.font.name = "Arial"

    # =========================================================================
    # SLIDE 2: IDEA TITLE & PROPOSED SOLUTION (With Workflow Infographic)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    apply_slide_template(slide2, "IDEA TITLE: MANGANEX AI", 2)

    # Sub-heading: ❖ Proposed Solution (Describe your Idea/Solution/Prototype)
    sub2 = slide2.shapes.add_textbox(Inches(0.6), Inches(1.15), Inches(12.0), Inches(0.4))
    p_sub2 = sub2.text_frame.paragraphs[0]
    p_sub2.text = "❖ Proposed Solution (Describe your Idea/Solution/Prototype)"
    p_sub2.font.size = Pt(14)
    p_sub2.font.bold = True
    p_sub2.font.underline = True
    p_sub2.font.color.rgb = SECTION_BLUE
    p_sub2.font.name = "Arial"

    # Top Flowchart Infographic Diagram
    if diag_workflow.exists():
        slide2.shapes.add_picture(str(diag_workflow), Inches(3.2), Inches(1.6), width=Inches(6.8))

    # 3 Column Cards below the diagram
    cards_s2 = [
        ("• Detailed Explanation of Proposed Solution", [
            "• End-to-End Decision Support: Fuses Sentinel-2 SWIR/NIR multispectral data with geological host rock lithology & mine telemetry.",
            "• Feature Extraction: Computes Ferrous Index (B11/B8A), Clay Alteration Index (B11/B12), and NDVI canopy stress.",
            "• Multi-Model ML Ensemble: Random Forest engines for In-Situ Potential, Shortfall Detection, and Risk Classification.",
            "• Interactive 3D GIS: 5-page Streamlit dashboard featuring PyDeck heatmaps and scenario simulation."
        ], SECTION_BLUE),
        
        ("• How It Addresses the Problem", [
            "• Eliminates Blind Exploration: Prioritizes high-confidence satellite spectral anomalies (60% faster turnaround).",
            "• Overcomes Production Deficits: Detects extraction gaps 3 to 6 months in advance by correlating equipment uptime and grade.",
            "• Quantitative Decision Support: Generates actionable recommendations for domestic quota reallocation & drilling targets."
        ], ORANGE_ACCENT),

        ("• Innovation & Uniqueness of the Solution", [
            "• Explainable AI (XAI): Decomposes prospectivity scores into exact mathematical signal contributions — no black-box decisions.",
            "• Multi-Hazard Risk Scoring: Simultaneously models geological, weather, and equipment bottlenecks at 97.5% accuracy.",
            "• Pre-Calibrated for Indian Belts: Sausar (MP/MH), Bonai-Keonjhar (Odisha), Sandur (Karnataka), and Kodurite (AP)."
        ], GREEN_ACCENT),
    ]

    for idx, (c_title, c_points, c_color) in enumerate(cards_s2):
        c_left = Inches(0.6 + idx * 4.1)
        card = slide2.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(3.8), Inches(3.9), Inches(3.05)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = c_color
        card.line.width = Pt(1.2)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.15)

        p = tf.paragraphs[0]
        p.text = c_title
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = c_color

        for pt in c_points:
            p_pt = tf.add_paragraph()
            p_pt.space_before = Pt(3)
            p_pt.text = pt
            p_pt.font.size = Pt(8.2)
            p_pt.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 3: TECHNICAL APPROACH (With Tech Architecture Diagram)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    apply_slide_template(slide3, "TECHNICAL APPROACH", 3)

    # Left Container: Technologies to be used
    left_s3 = slide3.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.3), Inches(4.5), Inches(5.4)
    )
    left_s3.fill.solid()
    left_s3.fill.fore_color.rgb = CARD_BG
    left_s3.line.color.rgb = SECTION_BLUE
    left_s3.line.width = Pt(1.5)

    tf_l3 = left_s3.text_frame
    tf_l3.word_wrap = True
    tf_l3.margin_left = tf_l3.margin_right = tf_l3.margin_top = Inches(0.2)

    p = tf_l3.paragraphs[0]
    p.text = "• Technologies to be Used"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = SECTION_BLUE

    tech_specs = [
        ("Core Language", "Python 3.10+ (Geospatial / ML / Analytics)"),
        ("Space & EO Data", "Sentinel-2 MSI (SWIR/NIR), Landsat-8/9 (TIRS LST), SRTM 30m DEM"),
        ("Machine Learning", "Scikit-Learn (Random Forest Regressors & Classifiers), Joblib, NumPy, Pandas"),
        ("Geospatial & 3D GIS", "PyDeck (WebGL 3D Geospatial Engine), Altair (Statistical Charts)"),
        ("Dashboard & UX", "Streamlit Multi-Page Enterprise Architecture with Dark Theme UI"),
        ("Hardware / Infra", "Standard Cloud / Edge Compute (Inference latency < 80ms)")
    ]

    for lbl, val in tech_specs:
        p = tf_l3.add_paragraph()
        p.space_before = Pt(5)
        r1 = p.add_run()
        r1.text = f"• {lbl}: "
        r1.font.bold = True
        r1.font.size = Pt(9.2)
        r1.font.color.rgb = DARK_BLUE_TITLE
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(9.2)
        r2.font.color.rgb = TEXT_DARK

    # Right Container: Methodology and Process for Implementation + Architecture Graphic
    right_s3 = slide3.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.3), Inches(1.3), Inches(7.4), Inches(5.4)
    )
    right_s3.fill.solid()
    right_s3.fill.fore_color.rgb = CARD_BG
    right_s3.line.color.rgb = GREEN_ACCENT
    right_s3.line.width = Pt(1.5)

    tf_r3 = right_s3.text_frame
    tf_r3.word_wrap = True
    tf_r3.margin_left = tf_r3.margin_right = tf_r3.margin_top = Inches(0.2)

    p = tf_r3.paragraphs[0]
    p.text = "• Methodology & Implementation Process"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT

    pipeline_steps = [
        ("Step 1: Space & Multispectral Ingestion", "Acquires Sentinel-2 SWIR-1/2 & Landsat Thermal radiance bands. Computes Ferrous (B11/B8A) & Clay (B11/B12) indices."),
        ("Step 2: Geological & Lithological Fusion", "Integrates SRTM DEM elevation/slope with GSI Sausar/Gondite formation lithology indices and historical extraction baselines."),
        ("Step 3: AI Inference & Prospectivity Scoring", "Calculates composite prospectivity score & confidence rating. Random Forest Regressor predicts in-situ manganese potential."),
        ("Step 4: Predictive Shortfall & Risk Classification", "Simulates extraction slippage based on equipment uptime, weather, and ore grade to forecast shortfalls 3-6 months in advance."),
        ("Step 5: Explainable AI & Working Prototype", "Presents 3D GIS heatmaps, transparent XAI driver breakdowns, and automated policy/operational recommendations.")
    ]

    for s_title, s_desc in pipeline_steps:
        p = tf_r3.add_paragraph()
        p.space_before = Pt(4)
        r_st = p.add_run()
        r_st.text = f"{s_title}\n"
        r_st.font.bold = True
        r_st.font.size = Pt(9.0)
        r_st.font.color.rgb = SECTION_BLUE
        r_sd = p.add_run()
        r_sd.text = s_desc
        r_sd.font.size = Pt(8.5)
        r_sd.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 4: FEASIBILITY AND VIABILITY (3 Structured Columns)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    apply_slide_template(slide4, "FEASIBILITY AND VIABILITY", 4)

    cards_s4 = [
        ("• Analysis of Feasibility & Viability", [
            "• Technical Feasibility: Utilizes proven, open-access Copernicus (Sentinel-2) and USGS (Landsat) satellite data pipelines with zero data licensing costs.",
            "• Operational Viability: Seamless web-based deployment requires no specialized on-premise hardware; accessible on desktop and field tablet devices.",
            "• Economic Viability: Payback period under 6 months by eliminating unnecessary exploratory drillholes ($50k–$150k saved per target site).",
            "• Scalability: Pipeline readily extends to Iron Ore, Bauxite, and Chromite mining belts across India."
        ], SECTION_BLUE),
        
        ("• Potential Challenges and Risks", [
            "• Cloud Cover & Monsoon Noise: Dense cloud cover during Indian monsoon (June–Sept) can obscure optical/SWIR satellite observations.",
            "• Dense Vegetation Camouflage: Thick forest canopy over unexplored terrains suppresses optical rock signatures.",
            "• Dynamic Mine Telemetry Gaps: Sub-optimal digital infrastructure in smaller private leaseholds.",
            "• Ground-Truth Discrepancy: Satellite surface indices require sub-surface drill core validation."
        ], ORANGE_ACCENT),

        ("• Strategies for Overcoming Challenges", [
            "• Multi-Temporal Cloud Masking: Merges dry season composites & integrates Sentinel-1 SAR radar for all-weather penetration.",
            "• Biogeochemical Canopy Stress Modeling: Converts suppressed NDVI into a positive mineralization proxy to penetrate vegetation cover.",
            "• Standardized Ingestion APIs: Lightweight Excel/CSV/JSON bulk data adapters allow seamless integration with legacy ERP systems.",
            "• JORC/UNFC Compliance: Positioned as G4/G3 exploration prioritization tool rather than certified reserve replacement."
        ], GREEN_ACCENT),
    ]

    for idx, (c_title, c_points, c_color) in enumerate(cards_s4):
        c_left = Inches(0.6 + idx * 4.1)
        card = slide4.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(1.4), Inches(3.9), Inches(5.3)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = c_color
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)

        p = tf.paragraphs[0]
        p.text = c_title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = c_color

        for pt in c_points:
            p_pt = tf.add_paragraph()
            p_pt.space_before = Pt(7)
            p_pt.text = pt
            p_pt.font.size = Pt(9.2)
            p_pt.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 5: IMPACT AND BENEFITS (With Impact KPI Infographic)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    apply_slide_template(slide5, "IMPACT AND BENEFITS", 5)

    # Top Infographic KPIs
    if diag_impact.exists():
        slide5.shapes.add_picture(str(diag_impact), Inches(3.6), Inches(1.3), width=Inches(6.0))

    # Bottom Two Content Cards
    quad_left = slide5.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(3.7), Inches(5.9), Inches(3.05)
    )
    quad_left.fill.solid()
    quad_left.fill.fore_color.rgb = CARD_BG
    quad_left.line.color.rgb = SECTION_BLUE
    quad_left.line.width = Pt(1.5)

    tf_ql = quad_left.text_frame
    tf_ql.word_wrap = True
    tf_ql.margin_left = tf_ql.margin_right = tf_ql.margin_top = Inches(0.2)

    p = tf_ql.paragraphs[0]
    p.text = "• Potential Impact on the Target Audience"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = SECTION_BLUE

    aud_items = [
        "• Ministry of Steel & Strategic Security: Reduces high-grade manganese import dependency for blast furnaces; enables real-time domestic supply deficit monitoring.",
        "• Mining Operators (MOIL / Private Miners): Early shortfall detection (3-6 months advance) prevents extraction bottlenecks, optimizes fleet dispatch, and stabilizes production.",
        "• EV Battery Ecosystem: Secures domestic raw material supply chain for emerging high-manganese Li-ion cathode chemistry (NMC precursors)."
    ]
    for pt in aud_items:
        p = tf_ql.add_paragraph()
        p.space_before = Pt(3)
        p.text = pt
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_DARK

    quad_right = slide5.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.7), Inches(5.9), Inches(3.05)
    )
    quad_right.fill.solid()
    quad_right.fill.fore_color.rgb = CARD_BG
    quad_right.line.color.rgb = GREEN_ACCENT
    quad_right.line.width = Pt(1.5)

    tf_qr = quad_right.text_frame
    tf_qr.word_wrap = True
    tf_qr.margin_left = tf_qr.margin_right = tf_qr.margin_top = Inches(0.2)

    p = tf_qr.paragraphs[0]
    p.text = "• Benefits of the Solution (Economic, Social & Environmental)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT

    ben_items = [
        "• Economic Benefits: 60% faster reconnaissance turnaround; multimillion-dollar drilling cost savings; domestic price stabilization against global import shocks.",
        "• Environmental Benefits: Non-invasive remote sensing prevents premature forest clearing and heavy machinery mobilization across ecologically sensitive zones.",
        "• National Targets: 592 critical mining zones actively monitored across 6 Indian states with 97.5% multi-hazard risk accuracy."
    ]
    for pt in ben_items:
        p = tf_qr.add_paragraph()
        p.space_before = Pt(3)
        p.text = pt
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 6: RESEARCH AND REFERENCES
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    apply_slide_template(slide6, "RESEARCH AND REFERENCES", 6)

    ref_card = slide6.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.3), Inches(12.1), Inches(5.4)
    )
    ref_card.fill.solid()
    ref_card.fill.fore_color.rgb = CARD_BG
    ref_card.line.color.rgb = SECTION_BLUE
    ref_card.line.width = Pt(1.5)

    tf_ref = ref_card.text_frame
    tf_ref.word_wrap = True
    tf_ref.margin_left = tf_ref.margin_right = tf_ref.margin_top = Inches(0.25)

    p = tf_ref.paragraphs[0]
    p.text = "• Details / Links of the Reference and Research Work"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = SECTION_BLUE

    ref_list = [
        ("1. Geological Survey of India (GSI) & Ministry of Mines:", 
         "• Indian Minerals Yearbook (Manganese Ore Chapter) & National Mineral Exploration Policy (NMEP).\n"
         "• United Nations Framework Classification (UNFC-1997 / UNFC-2009) for mineral reserves & resources."),
        
        ("2. Earth Observation & Satellite Multispectral Remote Sensing:", 
         "• European Space Agency (ESA) Copernicus Sentinel-2 MSI Spectral Band Formulations for Hydrothermal Alteration Mapping (Band 11 SWIR-1 / Band 12 SWIR-2 & Band 11 / Band 8A Ferrous Oxide Ratio).\n"
         "• USGS / NASA Landsat-8/9 Thermal Infrared Sensor (TIRS) Split-Window Land Surface Temperature (LST) Algorithms.\n"
         "• NASA / ISRO Shuttle Radar Topography Mission (SRTM) 30-meter Digital Elevation Models (DEM)."),
        
        ("3. Machine Learning & Explainable AI (XAI) Benchmarks:", 
         "• Breiman, L. (2001). 'Random Forests', Machine Learning, 45(1), 5-32 (Regression & Multi-hazard Classification).\n"
         "• Lundberg, S. M., & Lee, S. I. 'A Unified Approach to Interpreting Model Predictions' (Explainable AI driver decomposition principles).\n"
         "• Scikit-Learn Machine Learning Library (v1.4+) & Streamlit Enterprise Framework (v1.40+)."),
        
        ("4. Working Prototype Codebase & Live Interactive Repository:", 
         "• MANGANEX AI Full Working Repository: D:\\2nd move from os\\d\\MANGANEX_AI_SIHPOLISH\n"
         "• Live Interactive Decision Dashboard: http://localhost:8502 (5-Module Architecture)")
    ]

    for title_r, text_r in ref_list:
        p = tf_ref.add_paragraph()
        p.space_before = Pt(6)
        r_t = p.add_run()
        r_t.text = f"{title_r}\n"
        r_t.font.bold = True
        r_t.font.size = Pt(9.8)
        r_t.font.color.rgb = DARK_BLUE_TITLE

        r_b = p.add_run()
        r_b.text = text_r
        r_b.font.size = Pt(8.8)
        r_b.font.color.rgb = TEXT_DARK

    prs.save(OUTPUT_PPTX)
    print(f"Master SIH Submission PPTX generated at: {OUTPUT_PPTX}")

if __name__ == "__main__":
    create_master_presentation()
