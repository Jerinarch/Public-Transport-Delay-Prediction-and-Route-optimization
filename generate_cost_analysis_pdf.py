import os
import sys
import re
import html
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfgen import canvas

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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#718096"))

        if self._pageNumber > 1:
            self.drawString(36, 810, "CLOUD ENGINEERING & FINANCIAL FEASIBILITY ANALYSIS")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(36, 802, 559, 802)

        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(36, 38, 559, 38)

        self.setFont("Helvetica", 8)
        self.drawString(36, 26, "Intelligent Public Transport Delay Prediction System")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(559, 26, page_text)
        self.restoreState()

def clean_markdown_inline(text):
    if not text: return ""
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    return text

def parse_markdown_to_flowables(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    PRIMARY = colors.HexColor("#1A365D")
    SECONDARY = colors.HexColor("#2B6CB0")
    TEXT_DARK = colors.HexColor("#2D3748")
    BORDER_COLOR = colors.HexColor("#E2E8F0")

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('DocTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=PRIMARY, spaceAfter=6, spaceBefore=0)
    h1_style = ParagraphStyle('Heading1_Custom', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, leading=17, textColor=PRIMARY, spaceBefore=12, spaceAfter=5, keepWithNext=True)
    h2_style = ParagraphStyle('Heading2_Custom', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=SECONDARY, spaceBefore=9, spaceAfter=4, keepWithNext=True)
    h3_style = ParagraphStyle('Heading3_Custom', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=SECONDARY, spaceBefore=7, spaceAfter=3, keepWithNext=True)
    body_style = ParagraphStyle('Body_Custom', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=TEXT_DARK, spaceAfter=6)
    bullet_style = ParagraphStyle('Bullet_Custom', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=TEXT_DARK, leftIndent=12, spaceAfter=4)

    flowables = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i].rstrip('\r\n')
        
        if not line.strip():
            i += 1
            continue
            
        if line.strip() in ['---', '***', '___']:
            flowables.append(Spacer(1, 6))
            flowables.append(HRFlowable(width="100%", thickness=0.75, color=BORDER_COLOR, spaceBefore=3, spaceAfter=6))
            i += 1
            continue

        if line.startswith("# "):
            text = clean_markdown_inline(line[2:].strip())
            flowables.append(Paragraph(text, title_style))
            flowables.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=4, spaceAfter=10))
        elif line.startswith("## "):
            text = clean_markdown_inline(line[3:].strip())
            flowables.append(Paragraph(text, h1_style))
        elif line.startswith("### "):
            text = clean_markdown_inline(line[4:].strip())
            flowables.append(Paragraph(text, h2_style))
        elif line.startswith("> "):
            quote_text = clean_markdown_inline(line[2:].strip())
            p_quote = Paragraph(quote_text, body_style)
            t_quote = Table([[p_quote]], colWidths=[523.27])
            t_quote.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
                ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#3182CE")),
                ('LEFTPADDING', (0,0), (-1,-1), 10),
                ('RIGHTPADDING', (0,0), (-1,-1), 10),
                ('TOPPADDING', (0,0), (-1,-1), 8),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ]))
            flowables.append(Spacer(1, 4))
            flowables.append(t_quote)
            flowables.append(Spacer(1, 4))
        elif line.strip().startswith("* ") or line.strip().startswith("- "):
            item_text = line.strip()[2:].strip()
            bullet_p = Paragraph(f"&bull; &nbsp; {clean_markdown_inline(item_text)}", bullet_style)
            flowables.append(bullet_p)
        elif re.match(r'^(\d+)\.\s+(.*)$', line.strip()):
            m_num = re.match(r'^(\d+)\.\s+(.*)$', line.strip())
            num_str = m_num.group(1)
            item_text = m_num.group(2)
            bullet_p = Paragraph(f"<b>{num_str}.</b> &nbsp; {clean_markdown_inline(item_text)}", bullet_style)
            flowables.append(bullet_p)
        else:
            cleaned_text = clean_markdown_inline(line.strip())
            if cleaned_text:
                flowables.append(Paragraph(cleaned_text, body_style))
        i += 1

    return flowables

def generate_pdf_document(md_path, pdf_path):
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=40, bottomMargin=40)
    flowables = parse_markdown_to_flowables(md_path)
    doc.build(flowables, canvasmaker=NumberedCanvas)

if __name__ == "__main__":
    md_filepath = r"D:\An Intelligent Public Transport Delay Prediction and Route Optimization System Using Machine Learning\CLOUD_ENGINEERING_AND_COST_ANALYSIS.md"
    pdf_filepath = r"D:\An Intelligent Public Transport Delay Prediction and Route Optimization System Using Machine Learning\CLOUD_ENGINEERING_AND_COST_ANALYSIS.pdf"
    generate_pdf_document(md_filepath, pdf_filepath)
