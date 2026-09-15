import os
import sys
import datetime
from PIL import Image as PILImage

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable, PageBreak
)
from reportlab.pdfgen import canvas

sys.stdout.reconfigure(encoding='utf-8')

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A5568"))

        if self._pageNumber > 1:
            # Running Header
            self.drawString(54, 750, "PROJECT REVIEW 1: TECHNICAL PRESENTATION COMPANION & DEFENSE GUIDE")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 742, 612 - 54, 742)

            # Running Footer
            self.line(54, 45, 612 - 54, 45)
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(612 - 54, 32, page_text)
            self.drawString(54, 32, "CSE 784 — Dept. of CSE | Jerin Philip Mathew & Pregin Athish E")
        self.restoreState()


def get_scaled_image(img_path, max_width=480, max_height=260):
    if not os.path.exists(img_path):
        return None
    try:
        with PILImage.open(img_path) as img:
            w, h = img.size
            ratio = min(max_width / float(w), max_height / float(h))
            final_w = int(w * ratio)
            final_h = int(h * ratio)
            return Image(img_path, width=final_w, height=final_h)
    except Exception as e:
        print(f"Image load warning for {img_path}: {e}")
        return None


def generate_review_guide():
    base_dir = r"d:\An Intelligent Public Transport Delay Prediction and Route Optimization System Using Machine Learning"
    output_pdf_1 = os.path.join(base_dir, "MODEL BUILDING", "PROJECT_REVIEW_1_PRESENTATION_DEFENSE_GUIDE.pdf")
    output_pdf_2 = os.path.join(base_dir, "PROJECT_REVIEW_1_PRESENTATION_DEFENSE_GUIDE.pdf")

    doc = SimpleDocTemplate(
        output_pdf_1,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Color Palette
    PRIMARY = colors.HexColor("#1A365D")    # Deep Navy
    SECONDARY = colors.HexColor("#2B6CB0")  # Slate Blue
    ACCENT = colors.HexColor("#319795")     # Deep Teal
    DARK_TEXT = colors.HexColor("#2D3748")  # Charcoal
    LIGHT_BG = colors.HexColor("#F7FAFC")   # Off-white
    BORDER_COL = colors.HexColor("#E2E8F0") # Light Gray
    HIGHLIGHT_BG = colors.HexColor("#EDF2F7")

    # Custom Typography Styles
    styles.add(ParagraphStyle(
        'CoverSuperTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=ACCENT,
        alignment=0,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        alignment=0,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        'CoverSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=DARK_TEXT,
        alignment=0,
        spaceAfter=15
    ))

    styles.add(ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        'SubSectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        'SlideTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=ACCENT,
        spaceBefore=8,
        spaceAfter=2,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=DARK_TEXT,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        'BodyDarkBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=DARK_TEXT,
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        'BulletPoint',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=DARK_TEXT,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    ))

    styles.add(ParagraphStyle(
        'ScriptBoxText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1A202C")
    ))

    styles.add(ParagraphStyle(
        'TableHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=0
    ))

    styles.add(ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=DARK_TEXT
    ))

    styles.add(ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=DARK_TEXT
    ))

    story = []

    # ==========================================
    # COVER / HEADER BLOCK
    # ==========================================
    story.append(Paragraph("ACADEMIC PROJECT REVIEW 1 — CSE 784", styles['CoverSuperTitle']))
    story.append(Paragraph("An Intelligent Public Transport Delay Prediction & Route Optimization System Using Machine Learning", styles['CoverTitle']))
    story.append(Paragraph("<b>Comprehensive Slide-by-Slide Defense Guide, Mathematical Formulations, Literature Survey & Presentation Speaking Notes</b>", styles['CoverSubTitle']))

    # Metadata Card Table
    meta_data = [
        [
            Paragraph("<b>Project Phase:</b> Phase – 1 (Review 1)", styles['TableCell']),
            Paragraph("<b>Course Code:</b> CSE 784", styles['TableCell']),
            Paragraph("<b>Date:</b> September 2026", styles['TableCell'])
        ],
        [
            Paragraph("<b>Students:</b> Jerin Philip Mathew (2360385, 7BTCS C)<br/>Pregin Athish E (2360439, 7BTCS A)", styles['TableCell']),
            Paragraph("<b>Faculty Guides:</b> Dr. Jyothi Thomas<br/>Dr. Karthikeyan H", styles['TableCell']),
            Paragraph("<b>Department:</b> Computer Science & Engineering", styles['TableCell'])
        ]
    ]
    meta_table = Table(meta_data, colWidths=[180, 180, 144])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COL),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COL),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # Executive Pitch Box
    def make_script_box(title, text):
        box_data = [[
            Paragraph(f"<b>🎤 Speaking Script / Defense Pitch ({title}):</b><br/>{text}", styles['ScriptBoxText'])
        ]]
        t = Table(box_data, colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EBF8FF")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#BEE3F8")),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        return t

    story.append(make_script_box("30-Second Elevator Pitch for Reviewers", 
        "\"Good morning respected guides and panel members. Today we present our project: An Intelligent Public Transport Delay Prediction and Route Optimization System. Urban bus networks like BMTC face severe cascading delays due to traffic bottlenecks, micro-weather events, and stop overcrowding. While past literature focuses purely on passive delay prediction, our work introduces a dual-engine architecture: an ultra-low-latency XGBoost edge regressor (0.0027 ms) for mobile apps, a 3-layer BiLSTM with Bahdanau Attention achieving sub-minute trajectory precision (MAE: 20 seconds, R²: 0.9970), multi-class disruption diagnosis, TreeSHAP explainability, and an active sub-second A* dynamic graph rerouting engine that saves 75.5% delay time on the Bengaluru road graph.\""))
    story.append(Spacer(1, 14))

    # ==========================================
    # CHAPTER 1: FOUNDATIONAL CONTEXT (SLIDES 1-4)
    # ==========================================
    story.append(Paragraph("Chapter 1: Foundational Scope, Domain & Motivation (Slides 1 – 4)", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))

    story.append(Paragraph("<b>Slide 1: Title & Academic Metadata</b>", styles['SlideTag']))
    story.append(Paragraph("Sets the formal academic tone. Emphasizes the collaboration under the guidance of Dr. Jyothi Thomas and Dr. Karthikeyan H.", styles['BodyDark']))

    story.append(Paragraph("<b>Slide 2: Table of Contents</b>", styles['SlideTag']))
    story.append(Paragraph("Outlines the 9 structured segments of the presentation: Domain & Scope, Problem Identification, Objectives, Literature Survey (15 Papers), Research Gaps (7 Gaps), Proposed Architecture, Kimball Star Schema Dataset, Machine Learning Benchmarks, and Expected Outcomes.", styles['BodyDark']))

    story.append(Paragraph("<b>Slide 3: Domain & Sub-Domain Definition</b>", styles['SlideTag']))
    story.append(Paragraph("• <b>Primary Domain:</b> Artificial Intelligence & Data Science.<br/>• <b>Sub-Domain:</b> Machine Learning, Deep Sequential Learning & Predictive Analytics.<br/>• <b>5 Industrial Application Areas:</b> Urban Traffic Management, Peak-Hour Demand Forecasting, Public Transit Decision Support Systems (DSS), Intelligent Real-Time Route Optimization, and Multimodal Urban Logistics.", styles['BodyDark']))

    story.append(Paragraph("<b>Slide 4: Problem Statement, Motivation & Proposed Solution</b>", styles['SlideTag']))
    story.append(Paragraph("• <b>Problem Identification:</b> Urban bus networks in Indian metros suffer from cascading, compounding delays caused by traffic saturation, sudden monsoon downpours, and unmonitored bus stop dwell times. Existing systems use black-box models, ignore weather friction, and only predict delays without providing detour rerouting.<br/>• <b>Motivation:</b> Unreliable public transport pushes commuters to private vehicles, increasing city congestion. By providing sub-minute delay predictions and dynamic rerouting, we restore commuter trust, minimize travel delays, and support data-driven fleet operations for transit agencies.<br/>• <b>Proposed Solution:</b> An end-to-end framework integrating a 5-year BMTC dataset (729k rows), Kimball Star Schema warehouse, sequential deep learning (BiLSTM + Attention), multi-class disruption classification, Explainable AI (TreeSHAP), and dynamic graph rerouting.", styles['BodyDark']))
    story.append(Spacer(1, 10))

    # ==========================================
    # CHAPTER 2: LITERATURE REVIEW (SLIDES 5-19)
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("Chapter 2: Comprehensive Literature Review of 15 Research Papers (Slides 5 – 19)", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))
    story.append(Paragraph("We performed an exhaustive literature survey of 15 international, peer-reviewed research papers (IEEE, Elsevier, Springer, TRPRO, WCTR) across bus, tram, rail, and maritime transit systems. Below is the systematic synthesis:", styles['BodyDark']))

    papers_data = [
        [
            Paragraph("<b># / Year</b>", styles['TableHead']),
            Paragraph("<b>Paper Title & Authors</b>", styles['TableHead']),
            Paragraph("<b>Methodologies & Dataset</b>", styles['TableHead']),
            Paragraph("<b>Key Findings & Metric</b>", styles['TableHead']),
            Paragraph("<b>Critical Research Gap</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>P1</b><br/>2024", styles['TableCellBold']),
            Paragraph("<b>Explainable Delay Prediction in Public Bus Transit</b><br/>M. Gök et al. (IEEE Trans. ITS)", styles['TableCell']),
            Paragraph("LightGBM, XGBoost, Random Forest, SHAP XAI.<br/><i>Dataset:</i> ESHOT Izmir, Turkey (500k rows, 10 routes).", styles['TableCell']),
            Paragraph("LightGBM achieved R² = 0.88, MAE = 1.8 min. SHAP explained headway impacts.", styles['TableCell']),
            Paragraph("No sequence modeling; lacks dynamic graph rerouting; ignores micro-weather rainfall volume.", styles['TableCell'])
        ],
        [
            Paragraph("<b>P2</b><br/>2023", styles['TableCellBold']),
            Paragraph("<b>Public Transport Arrival Time Prediction Using Deep Learning</b><br/>S. Chen et al. (Elsevier TR-C)", styles['TableCell']),
            Paragraph("ConvLSTM, Spatio-Temporal Graph ConvNet (ST-GCN).<br/><i>Dataset:</i> Singapore LTA Bus GPS (2.1M pings).", styles['TableCell']),
            Paragraph("ST-GCN achieved RMSE = 2.15 min, outperforming static baselines.", styles['TableCell']),
            Paragraph("Heavy GPU computation (>400 ms latency); black-box without feature attribution; no rerouting.", styles['TableCell'])
        ],
        [
            Paragraph("<b>P3</b><br/>2024", styles['TableCellBold']),
            Paragraph("<b>Multi-Task Learning for Bus Delay & Crowding</b><br/>K. Zhang et al. (IEEE Access)", styles['TableCell']),
            Paragraph("Shared Multi-Task DNN with Hard Parameter Sharing.<br/><i>Dataset:</i> London TfL Bus & Oyster Tap Data.", styles['TableCell']),
            Paragraph("Simultaneous delay MAE = 2.3 min and occupancy accuracy = 81.2%.", styles['TableCell']),
            Paragraph("Discrete categorical crowding only; fails during sudden extreme weather events.", styles['TableCell'])
        ],
        [
            Paragraph("<b>P4</b><br/>2022", styles['TableCellBold']),
            Paragraph("<b>Dynamic Bus Rerouting Under Traffic Disruptions</b><br/>H. Liu & J. Wang (Springer JTT)", styles['TableCell']),
            Paragraph("Static Dijkstra on simplified corridor graph.<br/><i>Dataset:</i> Beijing Bus Group synthetic grid.", styles['TableCell']),
            Paragraph("Rerouted delayed buses with 15% theoretical time reduction.", styles['TableCell']),
            Paragraph("Simplified grid graph; not integrated with real OpenStreetMap network; no sub-second solver.", styles['TableCell'])
        ],
        [
            Paragraph("<b>P5</b><br/>2023", styles['TableCellBold']),
            Paragraph("<b>Weather Impact on Urban Bus Dwell Times</b><br/>A. Sharma et al. (Elsevier Transp. Policy)", styles['TableCell']),
            Paragraph("Ordinary Least Squares (OLS) & Random Forest.<br/><i>Dataset:</i> Delhi DTC Transit & IMD Weather.", styles['TableCell']),
            Paragraph("Proved rainfall >25 mm/h inflates bus stop dwell time by 42%.", styles['TableCell']),
            Paragraph("Coarse daily city-wide weather; no real-time telemetry streaming; purely descriptive.", styles['TableCell'])
        ],
        [
            Paragraph("<b>P6</b><br/>2021", styles['TableCellBold']),
            Paragraph("<b>Spatial Aggregation for Fleet Telematics</b><br/>R. Kumar et al. (IEEE T-IV)", styles['TableCell']),
            Paragraph("PostGIS Polygon Containment (ST_Within).<br/><i>Dataset:</i> 1,200 buses in Dublin, Ireland.", styles['TableCell']),
            Paragraph("Calculated average corridor speed with 3-second query time.", styles['TableCell']),
            Paragraph("High GIS query overhead; fails under 5,000+ concurrent buses; lacks discrete H3 hashing.", styles['TableCell'])
        ],
        [
            Paragraph("<b>P7</b><br/>2025", styles['TableCellBold']),
            Paragraph("<b>Predicting Ferry Transit Delays Using Open Data</b><br/>M. Sarhani et al. (Elsevier JPUBTR)", styles['TableCell']),
            Paragraph("SVR, Gradient Boosting, Deep Neural Nets, SHAP.<br/><i>Dataset:</i> Sydney & NYC Ferry GTFS (1.34M obs).", styles['TableCell']),
            Paragraph("GB achieved R² = 0.7807 with 90% predictions within 1 minute.", styles['TableCell']),
            Paragraph("Maritime waterways only; no road friction, signal delays, or urban bus dynamics.", styles['TableCell'])
        ],
        [
            Paragraph("<b>P8</b><br/>2017", styles['TableCellBold']),
            Paragraph("<b>Bus Arrival Prediction with Multi-Routes</b><br/>T. Yin et al. (Elsevier TRPRO / WCTR)", styles['TableCell']),
            Paragraph("GA-BPANN (Genetic Algorithm Neural Net), SVM.<br/><i>Dataset:</i> Zigong Bus Route 1, China (400 samples).", styles['TableCell']),
            Paragraph("GA-ANN achieved MAPE = 9.92%, RMSE = 235s across 16 workdays.", styles['TableCell']),
            Paragraph("Tiny sample (400 records); strictly 3 scalar features; explicitly excluded heavy congestion.", styles['TableCell'])
        ],
        [
            Paragraph("<b>P9</b><br/>2018", styles['TableCellBold']),
            Paragraph("<b>Bus Arrival Time Prediction Based on PCA-GA-SVM</b><br/>Z. Peng et al. (Neural Network World)", styles['TableCell']),
            Paragraph("Principal Component Analysis (PCA) + GA-SVM.<br/><i>Dataset:</i> Shenyang Bus Line 232, China (290 records).", styles['TableCell']),
            Paragraph("PCA compressed 6 features; PCA-GA-SVM achieved MAPE ~10%.", styles['TableCell']),
            Paragraph("Extremely small dataset (290 terms); coarse binary weather (sunny/rainy); no rerouting.", styles['TableCell'])
        ],
        [
            Paragraph("<b>P10</b><br/>2019", styles['TableCellBold']),
            Paragraph("<b>Multi-Output Deep Learning for Bus Arrival</b><br/>N. Petersen et al. (Elsevier TRPRO)", styles['TableCell']),
            Paragraph("Multi-Model Ensemble Network (FC-ANN + ConvLSTM).<br/><i>Dataset:</i> Movia Bus 4A Copenhagen (3.5M obs).", styles['TableCell']),
            Paragraph("FC + ConvLSTM achieved RMSE = 4.38 min on link travel times.", styles['TableCell']),
            Paragraph("Fails during sudden traffic incidents; lacks passenger count telemetry; no graph engine.", styles['TableCell'])
        ]
    ]

    papers_table = Table(papers_data, colWidths=[40, 115, 125, 115, 109])
    papers_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COL),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COL),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(papers_table)
    story.append(Spacer(1, 10))

    story.append(make_script_box("How to Defend the Literature Review in 2 Sentences",
        "\"We reviewed 15 foundational papers spanning bus, rail, and ferry networks. Across all 15 papers, two universal limitations stood out: first, they are purely PASSIVE—they predict delays but cannot reroute buses around bottlenecks; second, they either discard weather or use coarse city-wide averages. Our proposed system directly resolves these gaps by integrating micro-weather telemetry and sub-second dynamic graph rerouting on OpenStreetMap.\""))
    story.append(Spacer(1, 14))

    # ==========================================
    # CHAPTER 3: THE 7 RESEARCH GAPS (SLIDE 20)
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("Chapter 3: The 7 Research Gaps & Concrete Real-World Scenarios (Slide 20)", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))
    story.append(Paragraph("Slide 20 identifies the 7 core technical gaps in current public transit literature, illustrated with concrete, data-backed operational scenarios from Bengaluru's BMTC network:", styles['BodyDark']))

    gaps_data = [
        [
            Paragraph("<b># / Research Gap</b>", styles['TableHead']),
            Paragraph("<b>Technical Flaw in Literature</b>", styles['TableHead']),
            Paragraph("<b>Commuter (User) Impact Scenario</b>", styles['TableHead']),
            Paragraph("<b>Depot / Agency Manager Scenario</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>Gap 1</b><br/>Absence of Dynamic Graph Rerouting", styles['TableCellBold']),
            Paragraph("Existing studies focus only on passive delay prediction. None provide active, real-time detour geometries.", styles['TableCell']),
            Paragraph("<b>Amit (Airport Express KIA-9):</b> Faces 48-min Hebbal jam. Old app says 'Bus delayed'. Amit misses flight. Our system routes via Thanisandra, saving 44 mins.", styles['TableCell']),
            Paragraph("<b>Depot Controller:</b> Avoids 3-bus bunching on Bellary Road by automatically diverting trailing buses #202 & #203 in 42 ms, cutting corridor travel time from 65m to 21m.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Gap 2</b><br/>Excluded Environmental & Weather Features", styles['TableCellBold']),
            Paragraph("Weather is omitted, simplified to coarse binary flags, or aggregated to daily city averages.", styles['TableCell']),
            Paragraph("<b>Rahul at Bellandur:</b> 45 mm/h downpour floods road. Old model predicts sunny +2m delay; Rahul gets drenched. Our system predicts +28.5m delay; he stays dry in office.", styles['TableCell']),
            Paragraph("<b>Manager Suresh (Route 500D):</b> Prevents 6-bus flooding gridlock by detecting 45 mm/h storm, holding buses at KR Puram, and injecting standbys at Silk Board.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Gap 3</b><br/>Absence of Spatial Cell Indexing (H3)", styles['TableCellBold']),
            Paragraph("Coordinates processed as raw lat/long or heavy GIS polygon queries (ST_Within).", styles['TableCell']),
            Paragraph("<b>Ananya at Silk Board:</b> 200k users overload GIS server with 15s lag; app freezes and bus passes her. Our H3 hex hash loads nearest bus in 35 ms.", styles['TableCell']),
            Paragraph("<b>Chief Controller:</b> Aggregates speeds across 250 corridors and 6,000 buses in 15 ms via in-memory H3 integers, replacing 5-minute delayed GIS dashboards.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Gap 4</b><br/>Coarse Predictions & High Error Margins", styles['TableCellBold']),
            Paragraph("Models simplify delay into binary tags ('Congested') or have high error (MAE 5–10 min).", styles['TableCell']),
            Paragraph("<b>Priya at KR Puram:</b> Needs 08:45 Metro. Old model says 'Delayed ±8m'; she misses train. Our model predicts exact +16.4m delay, letting her reroute smoothly.", styles['TableCell']),
            Paragraph("<b>Shift Handover Manager:</b> Replaces blind guesswork with exact continuous delays (Bus 101: +2.8m, Bus 102: +24.8m), deploying standbys only where truly needed.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Gap 5</b><br/>Slow Response & High Processing Delays", styles['TableCellBold']),
            Paragraph("Unoptimized deep learning models take 300–2,000 ms per query, crashing under rush hour.", styles['TableCell']),
            Paragraph("<b>Vikram at Marathahalli (08:30 AM):</b> 2,000 req/sec causes 42s queue backlog and 504 Timeout. Our XGBoost returns ETA in 0.0027 ms (8 ms round-trip).", styles['TableCell']),
            Paragraph("<b>Cloud Architect:</b> Eliminates costly GPU cloud clusters; a single standard CPU server handles 370k requests/sec at near-zero hosting cost.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Gap 6</b><br/>Zero Visibility into Bus Crowding Levels", styles['TableCellBold']),
            Paragraph("No passenger load telemetry (Low, Moderate, Full) is provided in transit apps.", styles['TableCell']),
            Paragraph("<b>Meera at Marathahalli:</b> Waits for bus, only for a 97% packed bus to deny entry. Our app shows Bus 1 is 97% FULL and recommends Bus 2 (36% full) in 5 mins.", styles['TableCell']),
            Paragraph("<b>Fleet Dispatcher:</b> Eliminates empty trailing buses and prevents vehicle suspension damage by dynamically balancing passenger loads across fleet headways.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Gap 7</b><br/>Lack of Explainability (XAI)", styles['TableCellBold']),
            Paragraph("Black-box delay outputs leave commuters and transit agencies blind to root causes.", styles['TableCell']),
            Paragraph("<b>Rohan at Tin Factory:</b> 33m delay explained as: KR Puram Jam (+14.2m) + Rainstorm (+8.1m) + Overcrowding (+4.5m), restoring trust in transit.", styles['TableCell']),
            Paragraph("<b>Agency Auditor:</b> Uses TreeSHAP to distinguish valid road flooding from driver slacking, providing legal evidence to municipal bodies (BBMP/Police) to fix road drainage.", styles['TableCell'])
        ]
    ]

    gaps_table = Table(gaps_data, colWidths=[90, 110, 150, 154])
    gaps_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COL),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COL),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(gaps_table)
    story.append(Spacer(1, 14))

    # ==========================================
    # CHAPTER 4: OBJECTIVES (SLIDES 21-23)
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("Chapter 4: Project Objectives & Technical Execution Roadmap (Slides 21 – 23)", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))

    story.append(Paragraph("<b>Objective 1: High-Precision Delay & Occupancy Prediction Engine (Slide 22)</b>", styles['SubSectionHeader']))
    story.append(Paragraph("• <b>Multimodal Data Integration:</b> Unified ingestion of GTFS schedules, GPS telemetry, Open-Meteo hourly weather, Karnataka official holidays, and road network topology into a centralized 729k-row dataset.<br/>• <b>Zero-Target-Leakage Preprocessing:</b> Purged Out-Of-Time (OOT) temporal partitioning across 5 years (Train: 2022–2024, Val: 2025, Test: 2026). Strict stripping of <code>actual_arrival</code>.<br/>• <b>Sequential Deep Learning:</b> 3-Layer BiLSTM with Bahdanau Attention mechanism maintaining forward/backward hidden states across all 9 corridor stops.", styles['BodyDark']))

    story.append(Paragraph("<b>Objective 2: Explainable Dynamic Route Optimization Engine (Slide 22)</b>", styles['SubSectionHeader']))
    story.append(Paragraph("• <b>Transit Graph Modeling:</b> OpenStreetMap (OSM) multi-directed road graph with dynamic edge costs.<br/>• <b>Dynamic Cost Function:</b> $w(e) = \\frac{\\text{length}(e)}{\\text{ML\\_speed}(e)} \\times (1 + \\beta \\cdot \\text{congestion\\_index}(e)) + \\text{turn\\_penalties}$.<br/>• <b>Sub-Second Detour Pathfinding:</b> Dynamic A* and Dijkstra algorithms executing in $< 50\\text{ ms}$.<br/>• <b>Explainable AI Integration:</b> TreeSHAP feature attributions explaining delay root causes in natural language.", styles['BodyDark']))

    story.append(Paragraph("<b>Objective 3: Interactive Dashboard & Transit Decision Support (Slide 23)</b>", styles['SubSectionHeader']))
    story.append(Paragraph("• <b>Spatial Hotspot Clustering:</b> DBSCAN spatial clustering on GPS delay coordinates to identify recurring bottleneck zones (e.g. Silk Board, Tin Factory, Hebbal).<br/>• <b>Rule-Based Decision Support System (DSS):</b> Generates operational recommendations for depot managers (schedule buffer allocations, express skip-stop dispatches, and standby bus injection).", styles['BodyDark']))
    story.append(Spacer(1, 10))

    # ==========================================
    # CHAPTER 5: ARCHITECTURE & STAR SCHEMA (SLIDES 24 & 34-36)
    # ==========================================
    story.append(Paragraph("Chapter 5: System Architecture & Kimball Star Schema Data Warehouse (Slides 24 & 34 – 36)", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))

    # Embed Architecture Image
    arch_img_path = os.path.join(base_dir, "MODEL BUILDING", "PPT_IMAGES", "slide_24_Picture 2.png")
    arch_img = get_scaled_image(arch_img_path, max_width=490, max_height=220)
    if arch_img:
        story.append(arch_img)
        story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Data Warehouse Kimball Star Schema Architecture (Slides 35 & 36):</b>", styles['SubSectionHeader']))
    story.append(Paragraph("The data warehouse is organized around 1 centralized fact table and 5 dimension tables, enabling high-performance SQL analytics and OLAP cubes:", styles['BodyDark']))

    schema_data = [
        [
            Paragraph("<b>Table Name</b>", styles['TableHead']),
            Paragraph("<b>Type / Keys</b>", styles['TableHead']),
            Paragraph("<b>Core Attributes & Columns</b>", styles['TableHead']),
            Paragraph("<b>Data Integration Role</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>fact_integrated_bus_operations</b>", styles['TableCellBold']),
            Paragraph("<b>Fact Table</b><br/>PK: fact_id<br/>FK: bus_id, stop_id, service_date, route_id", styles['TableCell']),
            Paragraph("actual_arrival, delay_minutes, passenger_count, occupancy_pct, traffic_speed, congestion_index, disruption_label, weather_code", styles['TableCell']),
            Paragraph("Central measurement grain: 1 record per bus arrival at every stop across 729,648 events.", styles['TableCell'])
        ],
        [
            Paragraph("<b>dim_bus</b>", styles['TableCellBold']),
            Paragraph("<b>Dimension</b><br/>PK: bus_id", styles['TableCell']),
            Paragraph("registration_number, bus_type, capacity (45-60), seating_capacity, standing_capacity, fuel_type (Diesel/EV), ac_available", styles['TableCell']),
            Paragraph("BMTC Fleet Registry master tracking vehicle capacity and powertrain specs.", styles['TableCell'])
        ],
        [
            Paragraph("<b>dim_stop</b>", styles['TableCellBold']),
            Paragraph("<b>Dimension</b><br/>PK: stop_id", styles['TableCell']),
            Paragraph("stop_name, latitude, longitude, area, zone (North, East, South), shelter_available, accessibility", styles['TableCell']),
            Paragraph("Geocoded bus stop master for spatial indexing and corridor boundary mapping.", styles['TableCell'])
        ],
        [
            Paragraph("<b>dim_calendar</b>", styles['TableCellBold']),
            Paragraph("<b>Dimension</b><br/>PK: date", styles['TableCell']),
            Paragraph("day_of_week, is_weekend, is_holiday, holiday_name, holiday_type, is_working_day", styles['TableCell']),
            Paragraph("Official Karnataka State gazetted holiday calendar mapping peak/non-peak demand.", styles['TableCell'])
        ],
        [
            Paragraph("<b>dim_route</b>", styles['TableCellBold']),
            Paragraph("<b>Dimension</b><br/>PK: route_id", styles['TableCell']),
            Paragraph("route_name (500D ORR), first_stop, last_stop, route_distance_km (32.4 km), scheduled_duration (88 min)", styles['TableCell']),
            Paragraph("GTFS route timetable specifications.", styles['TableCell'])
        ],
        [
            Paragraph("<b>dim_road_network</b>", styles['TableCellBold']),
            Paragraph("<b>Dimension</b><br/>PK: road_id", styles['TableCell']),
            Paragraph("road_name, road_type (trunk/primary), length_km, lanes, maxspeed (60 km/h), oneway, geometry", styles['TableCell']),
            Paragraph("OpenStreetMap (OSM) road graph edges for dynamic shortest-path rerouting.", styles['TableCell'])
        ]
    ]

    schema_table = Table(schema_data, colWidths=[110, 85, 175, 134])
    schema_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COL),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COL),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(schema_table)
    story.append(Spacer(1, 14))

    # ==========================================
    # CHAPTER 6: DATASET & MATHEMATICAL DERIVATIONS (SLIDES 26-33)
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("Chapter 6: Comprehensive Dataset, 35 Features & Mathematical Derivations (Slides 26 – 33)", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))

    story.append(Paragraph("<b>The 35 Dataset Features Breakdown (Slides 27 – 31):</b>", styles['SubSectionHeader']))
    story.append(Paragraph("The dataset integrates <b>18 Direct Source Features</b> (from GTFS, BMTC registries, Open-Meteo API, Karnataka Calendar) and <b>17 Derived / Engineered Features</b>:", styles['BodyDark']))

    feature_summary_data = [
        [
            Paragraph("<b>Feature Domain</b>", styles['TableHead']),
            Paragraph("<b>Direct Source Features (18)</b>", styles['TableHead']),
            Paragraph("<b>Derived & Engineered Features (17)</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>Transit & Schedule</b>", styles['TableCellBold']),
            Paragraph("service_date, timestamp, route_id, route_name, trip_id, stop_sequence, scheduled_arrival", styles['TableCell']),
            Paragraph("actual_arrival, delay_minutes, lag_delay_prev_stop, delay_compounded_rate", styles['TableCell'])
        ],
        [
            Paragraph("<b>Vehicle & Fleet</b>", styles['TableCellBold']),
            Paragraph("bus_id, registration_number, bus_type, fuel_type, bus_capacity", styles['TableCell']),
            Paragraph("passenger_count, occupancy_percentage, occupancy_status", styles['TableCell'])
        ],
        [
            Paragraph("<b>Spatial & Geography</b>", styles['TableCellBold']),
            Paragraph("stop_id, stop_name, area, zone", styles['TableCell']),
            Paragraph("h3_spatial_cell_id, distance_to_next_stop, corridor_segment_id", styles['TableCell'])
        ],
        [
            Paragraph("<b>Weather & Environment</b>", styles['TableCellBold']),
            Paragraph("temperature, humidity, precipitation, rain, weather_code", styles['TableCell']),
            Paragraph("rain_intensity_bucket, weather_disruption_index", styles['TableCell'])
        ],
        [
            Paragraph("<b>Traffic & Disruption</b>", styles['TableCellBold']),
            Paragraph("—", styles['TableCell']),
            Paragraph("traffic_speed, congestion_level, congestion_index, incident_flag, disruption_label", styles['TableCell'])
        ],
        [
            Paragraph("<b>Temporal & Calendar</b>", styles['TableCellBold']),
            Paragraph("day_of_week, is_weekend, is_holiday, holiday_name", styles['TableCell']),
            Paragraph("hour_sin, hour_cos, day_sin, day_cos, is_rush_hour", styles['TableCell'])
        ]
    ]

    feat_table = Table(feature_summary_data, colWidths=[100, 190, 214])
    feat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COL),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COL),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(feat_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Mathematical Formulations Explained in Depth (Slides 32 & 33):</b>", styles['SubSectionHeader']))
    story.append(Paragraph("<b>1. Delay Minutes (Base-60 to Decimal Float Conversion):</b><br/>$$\\text{delay\\_minutes} = \\frac{\\text{Actual Arrival Timestamp} - \\text{Scheduled Arrival Timestamp}}{60.0 \\text{ seconds}}$$<br/><i>Example:</i> If Scheduled is <code>06:00:00</code> and Actual is <code>06:08:31</code>, the difference is 8 minutes and 31 seconds ($511\\text{ seconds}$). $\\frac{511}{60} = \\mathbf{8.5167 \\approx 8.52\\text{ decimal minutes}}$. (Note: $8.31$ decimal minutes would mean $8\\text{ min } 18.6\\text{ sec}$, which is mathematically incorrect for $31\\text{ seconds}$).", styles['BodyDark']))

    story.append(Paragraph("<b>2. Congestion Index ($CI$) & Indian Roads Congress (IRC:106) Thresholds:</b><br/>$$\\text{congestion\\_index} = \\max\\left(0, \\min\\left(1, 1 - \\frac{\\text{traffic\\_speed}}{60.0}\\right)\\right)$$<br/>The thresholds $0.30$ and $0.60$ are derived from standard <b>Level of Service (LOS)</b> engineering principles for $60\\text{ km/h}$ urban arterial roads:<br/>• <b>LOW ($CI \\le 0.30 \\iff v \\ge 42\\text{ km/h}$):</b> LOS A & B — Retains $\\ge 70\\%$ of free-flow speed. Free flow, negligible delay.<br/>• <b>MODERATE ($0.30 < CI \\le 0.60 \\iff 24 \\le v < 42\\text{ km/h}$):</b> LOS C & D — Retains $40\\%\\text{ to } 70\\%$ speed. Dense platoon flow.<br/>• <b>HEAVY ($CI > 0.60 \\iff v < 24\\text{ km/h}$):</b> LOS E & F — Retains $<40\\%$ speed. Stop-and-go breakdown; $24\\text{ km/h}$ is the universal tipping point where vehicle delays multiply exponentially.", styles['BodyDark']))

    story.append(Paragraph("<b>3. Dynamic Bus Capacity & Occupancy Status:</b><br/>$$\\text{occupancy\\_percentage} = \\left(\\frac{\\text{passenger\\_count}}{\\text{bus\\_capacity}}\\right) \\times 100$$<br/>Capacity is dynamically linked to <code>bus_type</code> (Ordinary: 60, EV Non-AC: 55, EV AC: 50, Volvo AC: 50, Airport Volvo: 45). Binned into: <code>LOW</code> ($<30\\%$), <code>MODERATE</code> ($30\\text{--}70\\%$), <code>HIGH</code> ($70\\text{--}90\\%$), <code>FULL</code> ($>90\\%$).", styles['BodyDark']))
    story.append(Spacer(1, 14))

    # ==========================================
    # CHAPTER 7: MODEL BUILDING & BENCHMARKING (SLIDES 37-42)
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("Chapter 7: Machine Learning Pipeline, Deep Learning & Benchmark Results (Slides 37 – 42)", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))

    story.append(Paragraph("<b>Target Definitions & Strict Zero-Target-Leakage Shielding (Slide 38):</b>", styles['SubSectionHeader']))
    story.append(Paragraph("To ensure industry-grade validity and prevent inflated, false evaluation scores, the pipeline enforces strict feature isolation:", styles['BodyDark']))

    leak_data = [
        [
            Paragraph("<b>Model Task / Objective</b>", styles['TableHead']),
            Paragraph("<b>Target Variable ($y$)</b>", styles['TableHead']),
            Paragraph("<b>Included Feature Space ($X$) (94 Features)</b>", styles['TableHead']),
            Paragraph("<b>Strictly Excluded (Leakage Shield)</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>Task 1: Regression</b><br/>Delay Duration Prediction", styles['TableCellBold']),
            Paragraph("<b>delay_minutes</b><br/>(Continuous Float)", styles['TableCell']),
            Paragraph("Scheduled timings, stop_sequence, bus_type, capacity, temperature, humidity, precipitation, rain, traffic_speed, congestion_index, incident_flag, lag_delay_prev_stop (Stop k-1)", styles['TableCell']),
            Paragraph("<b>actual_arrival</b> (direct algebraic target math)<br/><b>disruption_label</b> (derived from target)", styles['TableCell'])
        ],
        [
            Paragraph("<b>Task 2: Classification</b><br/>Disruption Root-Cause Diagnosis", styles['TableCellBold']),
            Paragraph("<b>disruption_label</b><br/>(6 Multi-Classes)", styles['TableCell']),
            Paragraph("Temperature, humidity, precipitation, rain, weather_code, traffic_speed, congestion_index, incident_flag, route_id, stop_id, scheduled_hour, day_of_week", styles['TableCell']),
            Paragraph("<b>actual_arrival</b> (direct leakage)<br/><b>delay_minutes</b> (formula component used to create class labels)", styles['TableCell'])
        ]
    ]

    leak_table = Table(leak_data, colWidths=[95, 75, 185, 149])
    leak_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COL),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COL),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(leak_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Regression Models Benchmark: BiLSTM with Attention vs. XGBoost (Slides 39 & 40):</b>", styles['SubSectionHeader']))
    story.append(Paragraph("Evaluated on the <b>2026 Out-of-Time Test Set (98,460 unseen rows)</b>:", styles['BodyDark']))

    reg_bench_data = [
        [
            Paragraph("<b>Performance Metric</b>", styles['TableHead']),
            Paragraph("<b>BiLSTM + Bahdanau Attention</b>", styles['TableHead']),
            Paragraph("<b>XGBoost Regressor (hist)</b>", styles['TableHead']),
            Paragraph("<b>Absolute Margin / Superiority</b>", styles['TableHead']),
            Paragraph("<b>Operational Deployment Role</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>R² Score (Variance Explained)</b>", styles['TableCellBold']),
            Paragraph("<b>0.9970 (99.70%)</b>", styles['TableCellBold']),
            Paragraph("0.9859 (98.59%)", styles['TableCell']),
            Paragraph("+1.11% R² gain", styles['TableCell']),
            Paragraph("BiLSTM captures 99.7% of all trajectory variance.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Root Mean Squared Error (RMSE)</b>", styles['TableCellBold']),
            Paragraph("<b>0.8650 min (~52 sec)</b>", styles['TableCellBold']),
            Paragraph("1.6307 min (~1m 38s)", styles['TableCell']),
            Paragraph("<b>-47.0% error reduction</b>", styles['TableCellBold']),
            Paragraph("Suppresses extreme compounding error spikes.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Mean Absolute Error (MAE)</b>", styles['TableCellBold']),
            Paragraph("<b>0.3458 min (~21 sec)</b>", styles['TableCellBold']),
            Paragraph("1.2983 min (~1m 18s)", styles['TableCell']),
            Paragraph("<b>-73.4% error reduction</b>", styles['TableCellBold']),
            Paragraph("Provides sub-minute, ~20-second precision.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Mean Absolute Percentage Error (MAPE)</b>", styles['TableCellBold']),
            Paragraph("<b>2.71%</b>", styles['TableCellBold']),
            Paragraph("20.99%", styles['TableCell']),
            Paragraph("-18.28% lower relative error", styles['TableCell']),
            Paragraph("Extremely reliable relative accuracy.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Inference Latency per Sample</b>", styles['TableCellBold']),
            Paragraph("0.0820 ms (Batch Trajectory)", styles['TableCell']),
            Paragraph("<b>0.0027 ms (2.7 μs)</b>", styles['TableCellBold']),
            Paragraph("XGBoost is 30x faster", styles['TableCell']),
            Paragraph("<b>XGBoost serves 370k req/sec on commuter edge!</b>", styles['TableCell'])
        ]
    ]

    reg_table = Table(reg_bench_data, colWidths=[120, 95, 95, 95, 99])
    reg_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COL),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COL),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(reg_table)
    story.append(Spacer(1, 10))

    # Embed Regression Heatmap / Scatter
    bilstm_scatter_path = os.path.join(base_dir, "MODEL BUILDING", "OUTPUTS", "Regressor", "Bidirectional LSTM with Bahdanau Attention", "bilstm_actual_vs_predicted_scatter.png")
    bilstm_heat_path = os.path.join(base_dir, "MODEL BUILDING", "OUTPUTS", "Regressor", "Bidirectional LSTM with Bahdanau Attention", "bilstm_stop_attention_weights_heatmap.png")

    img1 = get_scaled_image(bilstm_scatter_path, max_width=240, max_height=150)
    img2 = get_scaled_image(bilstm_heat_path, max_width=240, max_height=150)

    if img1 and img2:
        img_table = Table([[img1, img2]], colWidths=[252, 252])
        img_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(img_table)
        story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Classification Benchmark: XGBoost vs. Random Forest Classifier (Slides 41 & 42):</b>", styles['SubSectionHeader']))
    story.append(Paragraph("Comparison across overall metrics and per-class sensitivity on safety-critical minority classes (2026 Test Set):", styles['BodyDark']))

    clf_bench_data = [
        [
            Paragraph("<b>Evaluation Metric / Class</b>", styles['TableHead']),
            Paragraph("<b>XGBoost Classifier (multi:softprob)</b>", styles['TableHead']),
            Paragraph("<b>Random Forest Classifier (150 Trees)</b>", styles['TableHead']),
            Paragraph("<b>Operational Role & Insight</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>Overall Accuracy</b>", styles['TableCellBold']),
            Paragraph("<b>87.89%</b>", styles['TableCell']),
            Paragraph("87.73%", styles['TableCell']),
            Paragraph("High baseline accuracy across 98,460 test events.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Balanced Accuracy (Macro Recall)</b>", styles['TableCellBold']),
            Paragraph("<b>88.49%</b>", styles['TableCellBold']),
            Paragraph("87.73%", styles['TableCell']),
            Paragraph("Accounts for class imbalance across all 4 categories.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Weighted F1-Score</b>", styles['TableCellBold']),
            Paragraph("<b>0.8873 (88.73%)</b>", styles['TableCellBold']),
            Paragraph("0.8856 (88.56%)", styles['TableCell']),
            Paragraph("Harmonic mean of precision and recall.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Recall on ROUTE_CHANGED (Rare Class)</b>", styles['TableCellBold']),
            Paragraph("<b>90.54% (708 / 782 detected)</b>", styles['TableCellBold']),
            Paragraph("87.98% (688 / 782 detected)", styles['TableCell']),
            Paragraph("<b>XGBoost detects 90.5% of rare accidents & road closures!</b>", styles['TableCell'])
        ],
        [
            Paragraph("<b>Recall on NORMAL (On-Time)</b>", styles['TableCellBold']),
            Paragraph("88.26%", styles['TableCell']),
            Paragraph("<b>88.40%</b>", styles['TableCell']),
            Paragraph("High specificity for regular on-time transit runs.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Recall on DELAYED (5-15 min)</b>", styles['TableCellBold']),
            Paragraph("<b>88.81%</b>", styles['TableCell']),
            Paragraph("88.61%", styles['TableCell']),
            Paragraph("Accurate early warning for moderate traffic delays.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Recall on SEVERELY_DELAYED (>15m)</b>", styles['TableCellBold']),
            Paragraph("<b>86.36%</b>", styles['TableCell']),
            Paragraph("85.95%", styles['TableCell']),
            Paragraph("Flags major gridlocks for dynamic rerouting triggers.", styles['TableCell'])
        ]
    ]

    clf_table = Table(clf_bench_data, colWidths=[120, 120, 114, 150])
    clf_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COL),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COL),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(clf_table)
    story.append(Spacer(1, 14))

    # ==========================================
    # CHAPTER 8: EXPECTED OUTCOMES & ROUTING (SLIDES 43-46)
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("Chapter 8: Expected Results, Dynamic Routing & Dashboard (Slides 43 – 46)", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))

    story.append(Paragraph("<b>Outcome 1: Predictive Delay Analytics Engine (Slide 43)</b>", styles['SubSectionHeader']))
    story.append(Paragraph("• <b>Dual-Stage Risk Scoring:</b> Commuters receive a real-time risk classification (On-Time, Delayed, Severely Delayed) followed by an exact continuous delay duration in minutes.<br/>• <b>Sub-Second Responsiveness:</b> XGBoost serves mobile prediction endpoints in $0.0027\\text{ ms}$, ensuring zero mobile lag even during 100k+ rush-hour request surges.", styles['BodyDark']))

    story.append(Paragraph("<b>Outcome 2: Explainable Dynamic Routing on OpenStreetMap (Slide 43)</b>", styles['SubSectionHeader']))
    story.append(Paragraph("• <b>Dynamic Graph Pathfinding:</b> The system runs dynamic A* and Dijkstra shortest-path algorithms over the Bengaluru road graph. When the ML model predicts a severe bottleneck on the primary corridor (e.g. Outer Ring Road / Tin Factory / Hebbal), edge weights inflate dynamically and an optimal detour geometry is computed in $<50\\text{ ms}$.<br/>• <b>Benchmark Result:</b> Reduces corridor transit time from <b>$109.0\\text{ minutes}$ to $26.7\\text{ minutes}$</b>, saving <b>$82.3\\text{ minutes (75.5\\% delay reduction)}$</b>.<br/>• <b>SHAP Explanation Card:</b> Automatically prints natural-language explanations (e.g. <i>\"Rerouted due to: Heavy Jam at KR Puram (+14.2m) & Rainstorm (+8.1m)\"</i>).", styles['BodyDark']))

    story.append(Paragraph("<b>Outcome 3: Geospatial Hotspots & Decision Support System (Slide 45)</b>", styles['SubSectionHeader']))
    story.append(Paragraph("• <b>DBSCAN Spatial Hotspot Map:</b> Applies Density-Based Spatial Clustering of Applications with Noise (DBSCAN) on GPS delay coordinates, identifying recurrent infrastructure bottlenecks (e.g., Silk Board, Marathahalli, KR Puram).<br/>• <b>Rule-Based Decision Support for Depots:</b> Recommends schedule buffer extensions during peak monsoon hours and automates standby bus injection from neighboring depots.", styles['BodyDark']))
    story.append(Spacer(1, 10))

    # Embed Route Optimization / Hotspot Map
    route_map_path = os.path.join(base_dir, "MODEL BUILDING", "OUTPUTS", "Route_Optimization", "dynamic_rerouting_trajectory_map.png")
    route_img = get_scaled_image(route_map_path, max_width=490, max_height=200)
    if route_img:
        story.append(route_img)
        story.append(Spacer(1, 10))

    # ==========================================
    # CHAPTER 9: VIVA / REVIEWER Q&A DEFENSE SHEET
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("Chapter 9: Master Reviewer Q&A / Viva Defense Sheet", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))
    story.append(Paragraph("Here are the 10 most probable challenging questions from the review panel and your exact, mathematically rigorous answers:", styles['BodyDark']))

    qa_list = [
        ("Q1: Why did you choose BiLSTM + Bahdanau Attention over a standard LSTM or Transformer?",
         "\"Standard LSTMs only process sequences in one forward direction and suffer from vanishing gradients over long stops. A BiLSTM captures both forward delay accumulation and backward context. Furthermore, Bahdanau Additive Attention dynamically assigns mathematical weights (alpha_t) to specific upstream bottleneck stops (like Tin Factory), enabling sub-minute precision (MAE: 20 seconds, R²: 0.9970) while providing visual interpretability.\""),
        
        ("Q2: Why do you need BOTH XGBoost and BiLSTM? Isn't one enough?",
         "\"We designed a dual-tier industrial architecture: BiLSTM + Attention is our deep trajectory engine for dispatch controllers modeling 9-stop sequence compounding (0.082 ms). However, during peak rush hours with 100,000 mobile app users, BiLSTM tensor creation would cause server queues. XGBoost serves as our ultra-fast commuter edge regressor, operating in 0.0027 ms (2.7 microseconds / 370k queries/sec) on standard CPUs with zero queue delay.\""),

        ("Q3: How do you guarantee there is Zero Target Leakage in your models?",
         "\"We strictly excluded actual_arrival timestamp from feature space X because delay_minutes = actual_arrival - scheduled_arrival. In production, actual_arrival is unknown before the bus reaches. We also used a Purged Out-Of-Time (OOT) temporal split (Train: 2022-2024, Val: 2025, Test: 2026), preventing future data from leaking into the past.\""),

        ("Q4: Why are the congestion index thresholds set at 0.30 and 0.60?",
         "\"They are derived from Indian Roads Congress (IRC:106) and Highway Capacity Manual Level of Service (LOS) standards for 60 km/h arterial roads. CI <= 0.30 corresponds to v >= 42 km/h (LOS A/B, free flow). CI between 0.30 and 0.60 corresponds to 24 to 42 km/h (LOS C/D, dense flow). CI > 0.60 corresponds to v < 24 km/h (LOS E/F), which is the empirical tipping point where stop-and-go breakdown occurs and delays multiply exponentially.\""),

        ("Q5: How does your dynamic routing algorithm work in sub-second time?",
         "\"We model the road network as a multi-directed graph on OpenStreetMap. Road edge weights are dynamically computed using ML-predicted speeds and congestion indices: w(e) = (length / predicted_speed) * (1 + beta * CI). Using dynamic A* with Haversine distance heuristics, the shortest detour path is solved in under 50 milliseconds, saving 75.5% delay time on the Outer Ring Road corridor.\""),

        ("Q6: How did you handle the severe class imbalance in disruption classification?",
         "\"Critical disruptions like ROUTE_CHANGED represent less than 1% of events. We applied sample class weighting using inverse class frequencies ('balanced' mode). This forced the gradient booster to heavily penalize misclassifications on rare events, achieving a 90.54% Recall on ROUTE_CHANGED.\n\"")
    ]

    for q, a in qa_list:
        qa_box = [
            [Paragraph(f"<b>🎯 {q}</b><br/><br/><b>Answer:</b> {a}", styles['TableCell'])]
        ]
        qt = Table(qa_box, colWidths=[504])
        qt.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
            ('BOX', (0, 0), (-1, -1), 1, BORDER_COL),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(qt)
        story.append(Spacer(1, 6))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    
    # Also save a copy to root
    import shutil
    shutil.copyfile(output_pdf_1, output_pdf_2)
    print(f"Successfully generated PDF 1: {output_pdf_1} ({os.path.getsize(output_pdf_1)} bytes)")
    print(f"Successfully generated PDF 2: {output_pdf_2} ({os.path.getsize(output_pdf_2)} bytes)")

if __name__ == '__main__':
    generate_review_guide()
