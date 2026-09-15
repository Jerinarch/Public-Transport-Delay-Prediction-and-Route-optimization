import os
import sys
import re
import html
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable, Preformatted
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to add running headers and footers with accurate total page count.
    """
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

        # Running Header (pages 2 and later)
        if self._pageNumber > 1:
            self.drawString(36, 810, "DATASET COMPARISON, FEATURE MAPPING & SOURCE CITATION SPECIFICATION")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(36, 802, 559, 802)

        # Running Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(36, 38, 559, 38)

        self.setFont("Helvetica", 8)
        self.drawString(36, 26, "Intelligent Public Transport Delay Prediction & Route Optimization System")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(559, 26, page_text)
        self.restoreState()


def clean_markdown_inline(text):
    """
    Convert markdown inline formatting (**bold**, *italic*, `code`, [links]) into HTML tags for ReportLab Paragraph safely.
    """
    if not text:
        return ""
    
    # 1. Escape raw HTML special characters safely except existing entities
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    # 2. Extract inline backtick code snippets into placeholders first
    code_snippets = []
    def repl_code(match):
        idx = len(code_snippets)
        code_content = match.group(1)
        code_snippets.append(f'<font face="Courier" size="8" color="#1A365D"><b>{code_content}</b></font>')
        return f"___CODE_PH_{idx}___"
    
    text = re.sub(r'`(.*?)`', repl_code, text)
    
    # 3. Convert bold **text** or __text__
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    
    # 4. Convert italic *text*
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    
    # 5. Convert links [text](url) -> text with blue underline
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<font color="#2B6CB0"><u>\1</u></font>', text)
    
    # 6. Restore inline code placeholders
    for idx, snippet in enumerate(code_snippets):
        text = text.replace(f"___CODE_PH_{idx}___", snippet)
        
    return text


def parse_markdown_to_flowables(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Color Palette
    PRIMARY = colors.HexColor("#1A365D")      # Deep Navy Blue
    SECONDARY = colors.HexColor("#2B6CB0")    # Slate Blue
    ACCENT = colors.HexColor("#0D9488")       # Teal Accent
    TEXT_DARK = colors.HexColor("#2D3748")    # Charcoal body text
    BG_LIGHT = colors.HexColor("#F8FAFC")     # Soft light background
    BORDER_COLOR = colors.HexColor("#E2E8F0") # Border gray
    CODE_BG = colors.HexColor("#1E293B")      # Dark slate for code

    styles = getSampleStyleSheet()

    # Define Paragraph Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceAfter=6,
        spaceBefore=0
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=14.5,
        textColor=PRIMARY,
        spaceBefore=11,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=SECONDARY,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11.5,
        textColor=ACCENT,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11,
        textColor=TEXT_DARK,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=TEXT_DARK,
        leftIndent=12,
        spaceAfter=2
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.8,
        textColor=TEXT_DARK
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.white
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.5,
        leading=8.5,
        textColor=colors.HexColor("#E2E8F0")
    )

    flowables = []
    
    i = 0
    n = len(lines)
    
    in_code_block = False
    code_block_lines = []

    while i < n:
        line = lines[i].rstrip('\r\n')
        
        # Check Code Block Toggle
        if line.strip().startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_block_lines = []
            else:
                in_code_block = False
                
                # Truncate lines that exceed 115 characters to prevent overflow
                wrapped_code_lines = []
                for cl in code_block_lines:
                    if len(cl) > 115:
                        wrapped_code_lines.append(cl[:115] + "...")
                    else:
                        wrapped_code_lines.append(cl)

                # Split code lines into chunks of at most 25 lines
                chunk_size = 25
                for chunk_idx in range(0, len(wrapped_code_lines), chunk_size):
                    sub_lines = wrapped_code_lines[chunk_idx:chunk_idx+chunk_size]
                    code_chunk_text = "\n".join(sub_lines)
                    
                    p_code = Preformatted(code_chunk_text, code_style)
                    t_code = Table([[p_code]], colWidths=[523.27])
                    t_code.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
                        ('BOX', (0,0), (-1,-1), 0.75, PRIMARY),
                        ('TOPPADDING', (0,0), (-1,-1), 4),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                        ('LEFTPADDING', (0,0), (-1,-1), 6),
                        ('RIGHTPADDING', (0,0), (-1,-1), 6),
                    ]))
                    
                    flowables.append(Spacer(1, 2))
                    flowables.append(t_code)
                    flowables.append(Spacer(1, 2))
                
                flowables.append(Spacer(1, 4))
            i += 1
            continue

        if in_code_block:
            code_block_lines.append(line)
            i += 1
            continue

        # Blank line
        if not line.strip():
            i += 1
            continue

        # Horizontal Rule `---`
        if line.strip() in ['---', '***', '___']:
            flowables.append(Spacer(1, 3))
            flowables.append(HRFlowable(width="100%", thickness=0.75, color=BORDER_COLOR, spaceBefore=3, spaceAfter=5))
            i += 1
            continue

        # Markdown Table Detection
        if '|' in line and i + 1 < n and '|' in lines[i+1] and '-' in lines[i+1]:
            table_lines = []
            while i < n and '|' in lines[i]:
                table_lines.append(lines[i].strip())
                i += 1
            
            # Parse table_lines
            header_line = table_lines[0]
            data_lines = table_lines[2:] if len(table_lines) > 2 else []

            headers = [c.strip() for c in header_line.split('|')[1:-1]]
            num_cols = len(headers)

            if num_cols > 0:
                table_data = []
                
                # Header row
                header_row = [Paragraph(clean_markdown_inline(h), table_header_style) for h in headers]
                table_data.append(header_row)

                # Data rows
                for d_line in data_lines:
                    cols = [c.strip() for c in d_line.split('|')[1:-1]]
                    while len(cols) < num_cols:
                        cols.append("")
                    row = [Paragraph(clean_markdown_inline(cols[idx]), table_cell_style) for idx in range(num_cols)]
                    table_data.append(row)

                # Calculate Column Widths proportionally to fit usable_width = 523.27
                usable_width = 523.27
                if num_cols == 4:
                    col_widths = [usable_width * 0.22, usable_width * 0.25, usable_width * 0.25, usable_width * 0.28]
                elif num_cols == 5:
                    col_widths = [usable_width * 0.05, usable_width * 0.22, usable_width * 0.20, usable_width * 0.23, usable_width * 0.30]
                elif num_cols == 6:
                    col_widths = [usable_width * 0.05, usable_width * 0.18, usable_width * 0.15, usable_width * 0.15, usable_width * 0.14, usable_width * 0.33]
                elif num_cols == 7:
                    col_widths = [usable_width * 0.04, usable_width * 0.14, usable_width * 0.12, usable_width * 0.14, usable_width * 0.08, usable_width * 0.08, usable_width * 0.40]
                else:
                    col_widths = [usable_width / num_cols] * num_cols

                t = Table(table_data, colWidths=col_widths, repeatRows=1)
                t_style = [
                    ('BACKGROUND', (0,0), (-1,0), PRIMARY),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('TOPPADDING', (0,0), (-1,-1), 2.5),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
                    ('LEFTPADDING', (0,0), (-1,-1), 3.5),
                    ('RIGHTPADDING', (0,0), (-1,-1), 3.5),
                    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
                ]
                
                # Alternating row background
                for r_idx in range(1, len(table_data)):
                    if r_idx % 2 == 0:
                        t_style.append(('BACKGROUND', (0, r_idx), (-1, r_idx), BG_LIGHT))
                
                t.setStyle(TableStyle(t_style))
                flowables.append(Spacer(1, 3))
                flowables.append(t)
                flowables.append(Spacer(1, 4))
            continue

        # Headings
        if line.startswith("# "):
            text = clean_markdown_inline(line[2:].strip())
            flowables.append(Paragraph(text, title_style))
            flowables.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=5))
            i += 1
            continue
        elif line.startswith("## "):
            text = clean_markdown_inline(line[3:].strip())
            flowables.append(Paragraph(text, h1_style))
            i += 1
            continue
        elif line.startswith("### "):
            text = clean_markdown_inline(line[4:].strip())
            flowables.append(Paragraph(text, h2_style))
            i += 1
            continue
        elif line.startswith("#### "):
            text = clean_markdown_inline(line[5:].strip())
            flowables.append(Paragraph(text, h3_style))
            i += 1
            continue

        # Blockquote / Alert
        if line.startswith("> "):
            quote_text = clean_markdown_inline(line[2:].strip())
            p_quote = Paragraph(quote_text, body_style)
            t_quote = Table([[p_quote]], colWidths=[523.27])
            t_quote.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
                ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#3182CE")),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
                ('RIGHTPADDING', (0,0), (-1,-1), 8),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ]))
            flowables.append(Spacer(1, 2))
            flowables.append(t_quote)
            flowables.append(Spacer(1, 3))
            i += 1
            continue

        # Bullet List Items
        if line.strip().startswith("* ") or line.strip().startswith("- "):
            item_text = line.strip()[2:].strip()
            bullet_p = Paragraph(f"&bull; &nbsp; {clean_markdown_inline(item_text)}", bullet_style)
            flowables.append(bullet_p)
            i += 1
            continue

        # Numbered List Items
        m_num = re.match(r'^(\d+)\.\s+(.*)$', line.strip())
        if m_num:
            num_str = m_num.group(1)
            item_text = m_num.group(2)
            bullet_p = Paragraph(f"<b>{num_str}.</b> &nbsp; {clean_markdown_inline(item_text)}", bullet_style)
            flowables.append(bullet_p)
            i += 1
            continue

        # Normal Paragraph Text
        cleaned_text = clean_markdown_inline(line.strip())
        if cleaned_text:
            flowables.append(Paragraph(cleaned_text, body_style))

        i += 1

    return flowables


def generate_pdf_document(md_path, pdf_path):
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=40
    )

    print(f"Parsing Markdown file: {md_path}")
    flowables = parse_markdown_to_flowables(md_path)
    
    print(f"Building PDF document: {pdf_path}")
    doc.build(flowables, canvasmaker=NumberedCanvas)
    print(f"PDF Successfully generated at: {pdf_path}")


if __name__ == "__main__":
    base_dir = r"d:\An Intelligent Public Transport Delay Prediction and Route Optimization System Using Machine Learning"
    md_filepath = os.path.join(base_dir, "COMPREHENSIVE_OLD_VS_NEW_DATASET_COMPARISON_REPORT.md")
    pdf_filepath = os.path.join(base_dir, "Comprehensive_Dataset_Comparison_and_Feature_Mapping_Report.pdf")
    generate_pdf_document(md_filepath, pdf_filepath)
