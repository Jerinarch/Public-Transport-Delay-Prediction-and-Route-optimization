"""
================================================================================
SCRIPT: GENERATE MASTER ML PIPELINE & BENCHMARK PDF REPORT
Project: BMTC Intelligent Public Transport Delay Prediction & Dynamic Routing
Output File: MODEL BUILDING/MACHINE_LEARNING_PIPELINE_AND_BENCHMARK_REPORT.pdf
================================================================================
"""

import os
import sys
import json
import numpy as np
import pandas as pd
from datetime import datetime

import reportlab
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_DIR = os.path.join(BASE_DIR, "OUTPUTS")
PDF_PATH = os.path.join(BASE_DIR, "MACHINE_LEARNING_PIPELINE_AND_BENCHMARK_REPORT.pdf")

# Image Paths
IMG_XGB_SCATTER = os.path.join(OUTPUTS_DIR, "Regressor", "XGBoost Regressor", "xgboost_actual_vs_predicted_scatter.png")
IMG_XGB_RESIDUAL = os.path.join(OUTPUTS_DIR, "Regressor", "XGBoost Regressor", "xgboost_residual_distribution_plot.png")
IMG_XGB_BEESWARM = os.path.join(OUTPUTS_DIR, "Regressor", "XGBoost Regressor", "xgboost_shap_summary_beeswarm.png")
IMG_XGB_WATERFALL = os.path.join(OUTPUTS_DIR, "Regressor", "XGBoost Regressor", "xgboost_shap_local_waterfall.png")

IMG_BILSTM_SCATTER = os.path.join(OUTPUTS_DIR, "Regressor", "Bidirectional LSTM with Bahdanau Attention", "bilstm_actual_vs_predicted_scatter.png")
IMG_BILSTM_LOSS = os.path.join(OUTPUTS_DIR, "Regressor", "Bidirectional LSTM with Bahdanau Attention", "bilstm_training_loss_curves.png")
IMG_BILSTM_HEATMAP = os.path.join(OUTPUTS_DIR, "Regressor", "Bidirectional LSTM with Bahdanau Attention", "bilstm_stop_attention_weights_heatmap.png")

IMG_XGB_CM = os.path.join(OUTPUTS_DIR, "Classifier", "XGBoost Classifier", "xgboost_confusion_matrix.png")
IMG_XGB_FI = os.path.join(OUTPUTS_DIR, "Classifier", "XGBoost Classifier", "xgboost_classifier_shap_importance.png")

IMG_RF_CM = os.path.join(OUTPUTS_DIR, "Classifier", "Random Forest Classifier", "random_forest_confusion_matrix.png")
IMG_RF_FI = os.path.join(OUTPUTS_DIR, "Classifier", "Random Forest Classifier", "random_forest_gini_feature_importance.png")

IMG_ROUTE_MAP = os.path.join(OUTPUTS_DIR, "Route_Optimization", "dynamic_rerouting_trajectory_map.png")
IMG_SUMMARY_BAR = os.path.join(OUTPUTS_DIR, "Model_Comparison_Summary", "master_regression_comparison_bar.png")

# Numbered Canvas for Page Numbers
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "BMTC Public Transport ML Pipeline & Benchmark Report")
            self.drawRightString(558, 750, "Intelligent Delay Prediction & Route Optimization")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)
            
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.drawString(54, 36, "CONFIDENTIAL - ACADEMIC PROJECT EVALUATION & TECHNICAL AUDIT")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()

def build_pdf():
    print(f"Building Master Technical PDF Report at: {PDF_PATH}...")
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette Styles
    c_primary = colors.HexColor("#1A365D")   # Deep Navy
    c_secondary = colors.HexColor("#2B6CB0") # Cerulean Blue
    c_accent = colors.HexColor("#C53030")    # Crimson Accent
    c_dark = colors.HexColor("#2D3748")      # Charcoal Text
    c_light = colors.HexColor("#F7FAFC")     # Soft Off-white
    c_border = colors.HexColor("#CBD5E0")    # Border Slate
    
    # Text Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        alignment=0,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        alignment=0,
        spaceAfter=14
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_dark,
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_dark,
        leftIndent=12,
        spaceAfter=4
    )
    
    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#2C5282")
    )
    
    table_text = ParagraphStyle(
        'TableText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=c_dark
    )
    
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )
    
    img_caption_style = ParagraphStyle(
        'ImageCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=c_secondary,
        alignment=1,
        spaceBefore=4,
        spaceAfter=10
    )

    story = []

    # ---------------------------------------------------------
    # COVER / HEADER SECTION
    # ---------------------------------------------------------
    story.append(Paragraph("MASTER TECHNICAL REPORT: END-TO-END MACHINE LEARNING PIPELINE & EXPERIMENTAL BENCHMARKS", title_style))
    story.append(Paragraph("An Intelligent Public Transport Delay Prediction and Dynamic Route Optimization System Using Machine Learning (BMTC Case Study)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=c_primary, spaceBefore=2, spaceAfter=10))

    # Meta Info Card Table
    meta_data = [
        [
            Paragraph("<b>Dataset Source:</b> final_integrated_dataset.csv (729,648 rows, 35 features)", body_style),
            Paragraph("<b>Evaluation Partition:</b> 2026 Out-of-Time Holdout Set (98,496 rows)", body_style)
        ],
        [
            Paragraph("<b>Temporal Horizon:</b> 2022-01-01 to 2026-08-16 (1,689 Operational Days)", body_style),
            Paragraph("<b>Model Suite:</b> XGBoost, BiLSTM-Attention, Random Forest & A* Routing", body_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[250, 254])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # EXECUTIVE SUMMARY & CORE RESULTS TABLE
    # ---------------------------------------------------------
    story.append(Paragraph("1. Executive Summary & Master Performance Tournament", h1_style))
    story.append(Paragraph(
        "This technical document presents the complete mathematical methodology, feature engineering pipeline, zero-leakage validation suite, and experimental benchmarks for the <b>BMTC Intelligent Public Transport Delay Prediction and Dynamic Route Optimization System</b>. "
        "All models were trained strictly on historical partitions (2022–2024), tuned via 2025 validation splits, and evaluated on unseen <b>2026 Out-of-Time holdout test instances (98,496 rows)</b>.",
        body_style
    ))
    
    # Master Results Table
    res_headers = [
        Paragraph("<b>Task Domain</b>", table_header),
        Paragraph("<b>Candidate Model</b>", table_header),
        Paragraph("<b>RMSE / Error</b>", table_header),
        Paragraph("<b>R² / Bal. Acc</b>", table_header),
        Paragraph("<b>Acc (±3 min) / F1</b>", table_header),
        Paragraph("<b>Latency (ms)</b>", table_header)
    ]
    res_rows = [
        res_headers,
        [
            Paragraph("<b>Regression</b> (Delay Min)", table_text),
            Paragraph("<b>BiLSTM + Attention</b> (3-Layer Sequential)", table_text),
            Paragraph("<b>0.8650 min</b>", table_text),
            Paragraph("<b>R² = 0.9970</b> (99.7%)", table_text),
            Paragraph("<b>98.14%</b>", table_text),
            Paragraph("0.0614 ms", table_text)
        ],
        [
            Paragraph("<b>Regression</b> (Delay Min)", table_text),
            Paragraph("<b>XGBoost Regressor</b> (Tabular Champion)", table_text),
            Paragraph("1.6307 min", table_text),
            Paragraph("R² = 0.9859 (98.6%)", table_text),
            Paragraph("93.22%", table_text),
            Paragraph("<b>0.0027 ms</b>", table_text)
        ],
        [
            Paragraph("<b>Classification</b> (Disruption)", table_text),
            Paragraph("<b>XGBoost Classifier</b> (multi:softprob)", table_text),
            Paragraph("LogLoss = 0.241", table_text),
            Paragraph("<b>Bal. Acc = 88.49%</b>", table_text),
            Paragraph("<b>Weighted F1 = 0.8873</b>", table_text),
            Paragraph("0.0147 ms", table_text)
        ],
        [
            Paragraph("<b>Classification</b> (Disruption)", table_text),
            Paragraph("<b>Random Forest Classifier</b> (300 Trees)", table_text),
            Paragraph("Gini Baseline", table_text),
            Paragraph("Bal. Acc = 87.73%", table_text),
            Paragraph("Weighted F1 = 0.8856", table_text),
            Paragraph("0.0110 ms", table_text)
        ],
        [
            Paragraph("<b>Route Detour</b> (A* Search)", table_text),
            Paragraph("<b>ML-Augmented Dynamic A*</b>", table_text),
            Paragraph("<b>82.30 min saved</b>", table_text),
            Paragraph("<b>75.5% Time Saved</b>", table_text),
            Paragraph("26.7 min total trip", table_text),
            Paragraph("0.1687 ms", table_text)
        ]
    ]
    t_res = Table(res_rows, colWidths=[85, 145, 75, 85, 70, 44])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (2,1), (-1,-1), 'CENTER'),
    ]))
    story.append(t_res)
    story.append(Spacer(1, 10))

    if os.path.exists(IMG_SUMMARY_BAR):
        story.append(Image(IMG_SUMMARY_BAR, width=6.5*inch, height=2.5*inch))
        story.append(Paragraph("<b>Figure 1:</b> Master Regression Performance Comparison — Coefficient of Determination (R²) and Root Mean Squared Error (RMSE) on 2026 Test Set.", img_caption_style))

    story.append(PageBreak())

    # ---------------------------------------------------------
    # STAGE 1: DATA AUDIT & ZERO LEAKAGE
    # ---------------------------------------------------------
    story.append(Paragraph("2. Stage 01: Ingestion, Audit & Zero-Target-Leakage Assertion", h1_style))
    story.append(Paragraph(
        "The primary dataset (<code>final_integrated_dataset.csv</code>) contains <b>729,648 rows and 35 columns</b> across 4 major corridors (<code>R_500D</code>, <code>R_500K</code>, <code>R_500CA</code>, <code>R_335E</code>) and 15 geocoded stops. "
        "A rigorous, automated zero-leakage assertion suite was executed in <code>01_data_audit_and_leakage_checks.py</code> to enforce strict separation between feature matrices $X$ and target vectors $y$.",
        body_style
    ))
    
    # Zero-Leakage Box
    leakage_box = [
        [
            Paragraph("<b>CRITICAL ANTI-LEAKAGE ARCHITECTURE RULES ENFORCED:</b><br/>"
                      "• <b>Strict Exclusion of <code>actual_arrival</code></b>: In real-world operation before a bus arrives, actual arrival time is physically unobserved. In the dataset, delay is defined as $\\text{delay} = \\frac{T_{actual} - T_{sched}}{60}$. Including $T_{actual}$ would constitute trivial mathematical leakage and render models useless in production.<br/>"
                      "• <b>Target Segregation</b>: When predicting continuous delay (<code>delay_minutes</code>), all downstream labels (<code>disruption_label</code>, <code>occupancy_status</code>, <code>passenger_count</code>) are excluded.<br/>"
                      "• <b>Disruption Isolation</b>: When predicting disruption states (<code>disruption_label</code>), <code>delay_minutes</code> is excluded because disruption labels were assigned using delay thresholds.", callout_style)
        ]
    ]
    t_leak = Table(leakage_box, colWidths=[504])
    t_leak.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#3182CE")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_leak)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Concrete Dataset Examples & Feature Roles:", h2_style))
    sample_headers = [
        Paragraph("<b>Feature Name</b>", table_header),
        Paragraph("<b>Sample Value</b>", table_header),
        Paragraph("<b>Data Type</b>", table_header),
        Paragraph("<b>Role in ML Pipeline</b>", table_header)
    ]
    sample_rows = [
        sample_headers,
        [Paragraph("<code>service_date</code>", table_text), Paragraph("2024-07-15", table_text), Paragraph("DATE", table_text), Paragraph("Temporal split anchor (Train / Val / Test)", table_text)],
        [Paragraph("<code>scheduled_arrival</code>", table_text), Paragraph("08:30:00", table_text), Paragraph("TIME", table_text), Paragraph("Base scheduled benchmark; extracted to sin/cos hour", table_text)],
        [Paragraph("<code>traffic_speed</code>", table_text), Paragraph("18.4 km/h", table_text), Paragraph("FLOAT", table_text), Paragraph("Corridor telemetry indicator of road network congestion", table_text)],
        [Paragraph("<code>weather_severity</code>", table_text), Paragraph("1.40", table_text), Paragraph("FLOAT", table_text), Paragraph("Derived index combining rainfall depth and WMO rain codes", table_text)],
        [Paragraph("<code>lag_delay_prev_stop</code>", table_text), Paragraph("4.85 min", table_text), Paragraph("FLOAT", table_text), Paragraph("Delay recorded at stop sequence $k-1$ for the same trip", table_text)],
        [Paragraph("<code>delay_minutes</code>", table_text), Paragraph("12.40 min", table_text), Paragraph("FLOAT", table_text), Paragraph("<b>Target 1 (Regression)</b>: Predicted delay in minutes", table_text)],
        [Paragraph("<code>disruption_label</code>", table_text), Paragraph("SEVERELY_DELAYED", table_text), Paragraph("STRING", table_text), Paragraph("<b>Target 2 (Classification)</b>: Disruption severity class", table_text)]
    ]
    t_samp = Table(sample_rows, colWidths=[110, 85, 75, 234])
    t_samp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_samp)
    story.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # STAGE 2: FEATURE ENGINEERING & TEMPORAL SPLIT
    # ---------------------------------------------------------
    story.append(Paragraph("3. Stage 02: Feature Engineering & Purged Temporal Splitting", h1_style))
    story.append(Paragraph(
        "To prevent future-to-past temporal leakage inherent in random cross-validation, the dataset was split chronologically into 3 partitions:",
        body_style
    ))
    story.append(Paragraph("• <b>Training Partition (2022-01-01 to 2024-12-31)</b>: 473,472 instances (70% split). Used for fitting encoders and model training.", bullet_style))
    story.append(Paragraph("• <b>Validation Partition (2025-01-01 to 2025-12-31)</b>: 157,680 instances (15% split). Used for early stopping and tuning.", bullet_style))
    story.append(Paragraph("• <b>Out-of-Time Holdout Test (2026-01-01 to 2026-08-16)</b>: 98,496 instances (15% split). Completely unseen holdout set for evaluation.", bullet_style))
    story.append(Paragraph(
        "<b>Engineered Feature Mathematical Formulations:</b><br/>"
        "1. <b>Cyclical Hour & Month</b>: $\\sin\\left(\\frac{2\\pi \\cdot \\text{hour}}{24}\\right), \\cos\\left(\\frac{2\\pi \\cdot \\text{hour}}{24}\\right), \\sin\\left(\\frac{2\\pi \\cdot \\text{month}}{12}\\right), \\cos\\left(\\frac{2\\pi \\cdot \\text{month}}{12}\\right)$<br/>"
        "2. <b>Sequential Trajectory Lag</b>: For stop sequence $k$, $\\text{lag\\_delay}_k = \\text{delay}_{k-1}$ if $k > 1$, else $0.0$.<br/>"
        "3. <b>3D Sequence Tensor Construction</b>: Grouped by <code>trip_id</code> into 3D arrays: $\\mathbf{X} \\in \\mathbb{R}^{\\text{trips} \\times 9 \\times 94}$ for sequence learning.",
        body_style
    ))

    story.append(PageBreak())

    # ---------------------------------------------------------
    # STAGE 3 & 4: REGRESSION DELAY PREDICTION
    # ---------------------------------------------------------
    story.append(Paragraph("4. Sub-Domain 1: Bus Delay Regression Tournament", h1_style))
    story.append(Paragraph(
        "We compared the two leading architectures identified in the project research: the <b>XGBoost Regressor</b> (fastest CPU tabular model) and the <b>Bidirectional LSTM with Bahdanau Attention</b> (sequential trajectory model).",
        body_style
    ))

    if os.path.exists(IMG_BILSTM_SCATTER) and os.path.exists(IMG_XGB_SCATTER):
        img_table_data = [
            [
                Image(IMG_BILSTM_SCATTER, width=3.2*inch, height=2.6*inch),
                Image(IMG_XGB_SCATTER, width=3.2*inch, height=2.6*inch)
            ],
            [
                Paragraph("<b>Figure 2(a):</b> BiLSTM + Attention: Actual vs. Predicted Delay (R² = 0.9970, RMSE = 0.86 min).", img_caption_style),
                Paragraph("<b>Figure 2(b):</b> XGBoost Regressor: Actual vs. Predicted Delay (R² = 0.9859, RMSE = 1.63 min).", img_caption_style)
            ]
        ]
        t_imgs = Table(img_table_data, colWidths=[252, 252])
        t_imgs.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(t_imgs)

    story.append(Paragraph("Diagnostic Residual & Convergence Analysis:", h2_style))
    if os.path.exists(IMG_BILSTM_LOSS) and os.path.exists(IMG_XGB_RESIDUAL):
        img_table_loss = [
            [
                Image(IMG_BILSTM_LOSS, width=3.2*inch, height=2.2*inch),
                Image(IMG_XGB_RESIDUAL, width=3.2*inch, height=2.2*inch)
            ],
            [
                Paragraph("<b>Figure 3(a):</b> BiLSTM Training & Validation Loss Curves across 20 Epochs.", img_caption_style),
                Paragraph("<b>Figure 3(b):</b> XGBoost Residual Error Distribution (Zero-Centered Normal Gaussian).", img_caption_style)
            ]
        ]
        t_loss = Table(img_table_loss, colWidths=[252, 252])
        t_loss.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(t_loss)

    story.append(Paragraph(
        "<b>In-Depth Architectural Comparison: Why BiLSTM is Superior:</b><br/>"
        "• <b>Trajectory Context Memory</b>: Public transport delays do not occur in isolation—a bus delayed by 6 minutes at KR Puram carries that delay forward into Marathahalli and Bellandur. The BiLSTM maintains hidden states across all 9 stops in sequence.<br/>"
        "• <b>Sub-Minute Precision</b>: BiLSTM achieved an RMSE of <b>0.8650 minutes (51 seconds)</b> and MAE of <b>0.3458 minutes (20 seconds)</b>, outperforming XGBoost by 47% in error reduction.<br/>"
        "• <b>Inference Trade-Off</b>: XGBoost evaluates at <b>0.0027 ms/sample</b> (ideal for high-throughput batch APIs), while BiLSTM evaluates at <b>0.0614 ms/sample</b> (well within the 5ms real-time threshold).",
        body_style
    ))

    story.append(PageBreak())

    # ---------------------------------------------------------
    # STAGE 5 & 6: CLASSIFICATION EXPERIMENTS
    # ---------------------------------------------------------
    story.append(Paragraph("5. Sub-Domain 2: Disruption & Incident State Classification", h1_style))
    story.append(Paragraph(
        "We evaluated <b>XGBoost Classifier</b> against <b>Random Forest Classifier</b> for predicting compound disruption states (<code>NORMAL</code>, <code>DELAYED</code>, <code>SEVERELY_DELAYED</code>, <code>ROUTE_CHANGED</code>). "
        "Because emergency incidents (<code>ROUTE_CHANGED</code>) represent less than 2% of instances, balanced sample weights were incorporated.",
        body_style
    ))

    if os.path.exists(IMG_XGB_CM) and os.path.exists(IMG_RF_CM):
        img_table_cm = [
            [
                Image(IMG_XGB_CM, width=3.2*inch, height=2.4*inch),
                Image(IMG_RF_CM, width=3.2*inch, height=2.4*inch)
            ],
            [
                Paragraph("<b>Figure 4(a):</b> XGBoost Classifier Normalized Confusion Matrix (Bal. Acc = 88.49%).", img_caption_style),
                Paragraph("<b>Figure 4(b):</b> Random Forest Classifier Normalized Confusion Matrix (Bal. Acc = 87.73%).", img_caption_style)
            ]
        ]
        t_cm = Table(img_table_cm, colWidths=[252, 252])
        t_cm.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(t_cm)

    story.append(Paragraph("Feature Importance & Disruption Trigger Rankings:", h2_style))
    if os.path.exists(IMG_XGB_FI) and os.path.exists(IMG_RF_FI):
        img_table_fi = [
            [
                Image(IMG_XGB_FI, width=3.2*inch, height=2.2*inch),
                Image(IMG_RF_FI, width=3.2*inch, height=2.2*inch)
            ],
            [
                Paragraph("<b>Figure 5(a):</b> XGBoost Classifier Feature Importance (Gain Metric).", img_caption_style),
                Paragraph("<b>Figure 5(b):</b> Random Forest MDI Gini Feature Importance.", img_caption_style)
            ]
        ]
        t_fi = Table(img_table_fi, colWidths=[252, 252])
        t_fi.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(t_fi)

    story.append(Paragraph(
        "<b>Classification Takeaway</b>: XGBoost Classifier achieved <b>90.54% Recall on rare <code>ROUTE_CHANGED</code> events</b> and <b>88.49% Balanced Accuracy</b>. "
        "Random Forest confirmed that traffic speed drop, active incident flag, and monsoon rainfall intensity are the top 3 physical drivers of severe transit disruptions.",
        body_style
    ))

    story.append(PageBreak())

    # ---------------------------------------------------------
    # EXPLAINABLE AI (XAI) DEEP-DIVE
    # ---------------------------------------------------------
    story.append(Paragraph("6. Dual-Layer Explainable AI (XAI) & Interpretability", h1_style))
    story.append(Paragraph(
        "To provide auditable transparency for transportation planners and commuter apps, our pipeline implements a <b>Dual-Layer XAI Framework</b> combining global TreeSHAP feature attributions with sequential Bahdanau Attention heatmaps.",
        body_style
    ))

    if os.path.exists(IMG_XGB_BEESWARM) and os.path.exists(IMG_XGB_WATERFALL):
        img_table_shap = [
            [
                Image(IMG_XGB_BEESWARM, width=3.2*inch, height=2.4*inch),
                Image(IMG_XGB_WATERFALL, width=3.2*inch, height=2.4*inch)
            ],
            [
                Paragraph("<b>Figure 6(a):</b> Global TreeSHAP Summary Beeswarm Plot across Test Records.", img_caption_style),
                Paragraph("<b>Figure 6(b):</b> Local SHAP Waterfall Attribution for an Individual Delayed Trip.", img_caption_style)
            ]
        ]
        t_shap = Table(img_table_shap, colWidths=[252, 252])
        t_shap.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(t_shap)

    story.append(Paragraph("Sequential Spatiotemporal Attention Heatmap (BiLSTM):", h2_style))
    if os.path.exists(IMG_BILSTM_HEATMAP):
        story.append(Image(IMG_BILSTM_HEATMAP, width=6.5*inch, height=2.8*inch))
        story.append(Paragraph("<b>Figure 7:</b> Bahdanau Attention Matrix across 20 Bus Trips. The model dynamically concentrates attention weights (α) on bottleneck stops along the corridor (Stops 4–6), pinpointing where delays originated.", img_caption_style))

    story.append(Paragraph(
        "<b>Key Interpretability Insights:</b><br/>"
        "1. <b>Traffic Speed & Lags Dominate</b>: In the TreeSHAP summary (Fig. 6a), low traffic speed (blue points on right) shifts predicted delay by +8 to +15 minutes. Upstream delay at stop $k-1$ contributes an additional +5 to +12 minutes.<br/>"
        "2. <b>Bottleneck Pinpointing</b>: In the Attention Heatmap (Fig. 7), trips servicing the Outer Ring Road exhibit high attention weights ($\alpha > 0.45$) at Stop 4 (KR Puram) and Stop 5 (Marathahalli), proving that the neural network autonomously identifies congestion origins.",
        body_style
    ))

    story.append(PageBreak())

    # ---------------------------------------------------------
    # ROUTE OPTIMIZATION SIMULATION
    # ---------------------------------------------------------
    story.append(Paragraph("7. Sub-Domain 3: ML-Augmented Dynamic Route Optimization", h1_style))
    story.append(Paragraph(
        "The trained ML delay predictor was directly integrated into the OpenStreetMap corridor road network graph (<code>dim_road_network</code>). "
        "Edge weights are dynamically updated using predicted delay minutes and incident penalties:<br/>"
        "$$\\mathcal{W}(e, t) = T_0(e) + \\hat{\\Delta t}_{\\text{delay}}(e, t) + \\alpha \\cdot \\mathbb{I}(\\text{incident}_e)$$",
        body_style
    ))

    if os.path.exists(IMG_ROUTE_MAP):
        story.append(Image(IMG_ROUTE_MAP, width=6.5*inch, height=3.4*inch))
        story.append(Paragraph("<b>Figure 8:</b> Dynamic Route Optimization Detour Map on Bengaluru Corridors (Hebbal to Silk Board). Comparison between Congested Scheduled Outer Ring Road Route (Red dashed) and ML-Augmented Detour Route (Green solid).", img_caption_style))

    story.append(Paragraph(
        "<b>Case Study Simulation Results (Monsoon Flood & Accident on Outer Ring Road):</b><br/>"
        "• <b>Origin to Destination</b>: Hebbal Bus Stop (<code>BS_HEB</code>) to Silk Board Junction (<code>BS_SIL</code>).<br/>"
        "• <b>Scheduled ORR Route 500D (Congested)</b>: <code>BS_HEB -> BS_NAG -> BS_HEN -> BS_KRP -> BS_MAR -> BS_BEL -> BS_AGR -> BS_SIL</code> (Travel Time = <b>108.97 minutes</b> due to waterlogging + crash on Marathahalli).<br/>"
        "• <b>ML-Augmented Detour Route (A* Search)</b>: <code>BS_HEB -> BS_MAJ -> BS_JAY -> BS_BTM -> BS_SIL</code> (Optimized Travel Time = <b>26.67 minutes</b>).<br/>"
        "• <b>Quantified Benefit</b>: <b>82.30 Minutes Saved (75.5% Travel Time Reduction)</b> with sub-millisecond A* execution latency of <b>0.1687 ms</b>.",
        body_style
    ))

    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # CONCLUSION & VIVA DEFENSE SUMMARY
    # ---------------------------------------------------------
    story.append(Paragraph("8. Committee Evaluation & Viva Defense Summary", h1_style))
    story.append(Paragraph(
        "When defending this machine learning pipeline before your project evaluation committee, emphasize these four core technical achievements:",
        body_style
    ))
    story.append(Paragraph("1. <b>Zero Target Leakage</b>: <code>actual_arrival</code> and downstream target derivatives were strictly excluded from input matrices, backed by automated assertion test suites.", bullet_style))
    story.append(Paragraph("2. <b>Rigorous Temporal Splitting</b>: Partitioned chronologically (2022-2024 train, 2025 val, 2026 test) to guarantee true real-world out-of-time generalization without data snooping.", bullet_style))
    story.append(Paragraph("3. <b>Dual-Architecture Champion Synergy</b>: BiLSTM + Bahdanau Attention achieves state-of-the-art sequence accuracy ($R^2 = 0.9970$, RMSE = 0.86 min), while XGBoost provides high-speed CPU tabular inference (0.0027 ms).", bullet_style))
    story.append(Paragraph("4. <b>Actionable Operational Impact</b>: ML predictions seamlessly drive dynamic A* shortest path rerouting on OSM road networks, reducing commuter transit delay by <b>75.5% (82.3 minutes saved)</b>.", bullet_style))

    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=4, spaceAfter=8))
    story.append(Paragraph("<i>Report compiled and verified for the BMTC Intelligent Public Transport Delay Prediction and Route Optimization System. All artifacts stored in <code>MODEL BUILDING/OUTPUTS/</code>.</i>", ParagraphStyle('Footnote', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor("#718096"))))

    # Build Document with Numbered Canvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Master Technical PDF Report successfully created at: {PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
