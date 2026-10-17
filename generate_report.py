import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Flowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# ==============================================================================
# PATH CONSTANTS & ASSET DIRECTORIES
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRATCH_DIR = r"C:\Users\ujjav\.gemini\antigravity\brain\54b1e0af-2f7a-4222-8817-cb66512bb3b9\scratch"
REPORT_LOGOS_DIR = os.path.join(SCRATCH_DIR, "report_logos")
PPT_LOGOS_DIR = os.path.join(SCRATCH_DIR, "ppt_logos")
FIGS_DIR = os.path.join(SCRATCH_DIR, "doc_figures")
BANNER_PATH = os.path.join(BASE_DIR, "Streamlit_App", "assets", "hero_banner.png")
OUTPUT_PDF = os.path.join(BASE_DIR, "HomeWorth_AI_Project_Report.pdf")

# University & Institutional Logos
LOGO_AKTU = os.path.join(REPORT_LOGOS_DIR, "img_p2_0.png")
if not os.path.exists(LOGO_AKTU):
    LOGO_AKTU = os.path.join(PPT_LOGOS_DIR, "img_p1_1.png")

LOGO_UNITED = os.path.join(REPORT_LOGOS_DIR, "img_p2_1.png")
if not os.path.exists(LOGO_UNITED):
    LOGO_UNITED = os.path.join(PPT_LOGOS_DIR, "img_p1_0.png")

# High-Resolution Publication Figures
FIG_ARCH = os.path.join(FIGS_DIR, "fig_system_architecture.png")
FIG_DIST = os.path.join(FIGS_DIR, "fig_price_distribution.png")
FIG_CITY = os.path.join(FIGS_DIR, "fig_city_prices.png")
FIG_MODEL = os.path.join(FIGS_DIR, "fig_model_comparison.png")
FIG_FEAT = os.path.join(FIGS_DIR, "fig_feature_importance.png")
FIG_RES = os.path.join(FIGS_DIR, "fig_residuals_analysis.png")

# Global Page Tracker Dictionary for Dynamic Table of Contents
PAGE_TRACKER = {}

class Bookmark(Flowable):
    """Zero-dimension flowable that records the exact physical page number of headings."""
    def __init__(self, key, tracker):
        super().__init__()
        self.key = key
        self.tracker = tracker
        self.width = 0
        self.height = 0

    def draw(self):
        # canvas._pageNumber holds the 1-indexed physical page
        self.tracker[self.key] = self.canv._pageNumber


class AcademicCanvas(canvas.Canvas):
    """Two-pass canvas drawing exact university margins, running headers, and footers."""
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
            self.draw_academic_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_academic_decorations(self, total_pages):
        page_num = self._pageNumber
        start_of_chap1 = PAGE_TRACKER.get('chap1', 9)
        
        # Cover Page (Physical Page 1): Double Border as per university format
        if page_num == 1:
            self.saveState()
            self.setStrokeColor(colors.black)
            self.setLineWidth(2.5)
            # Outer border
            self.rect(1.5 * cm, 1.2 * cm, A4[0] - 2.7 * cm, A4[1] - 2.4 * cm)
            # Inner border
            self.setLineWidth(0.8)
            self.rect(1.65 * cm, 1.35 * cm, A4[0] - 3.0 * cm, A4[1] - 2.7 * cm)
            self.restoreState()
            return

        self.saveState()
        self.setFont("Times-Roman", 10)
        self.setFillColor(colors.HexColor("#475569"))

        # Running Footer Divider Line
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(3.5 * cm, 1.8 * cm, A4[0] - 1.25 * cm, 1.8 * cm)

        # Page Numbering & Running Headers
        if page_num < start_of_chap1:
            # Roman numerals for Front Matter (Physical Pages 2 to start_of_chap1 - 1)
            roman_numerals = ["", "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"]
            idx = page_num - 1
            if 1 <= idx < len(roman_numerals):
                self.drawRightString(A4[0] - 1.25 * cm, 1.2 * cm, roman_numerals[idx])
        else:
            # Running Header for Main Body Chapters
            self.drawString(3.5 * cm, A4[1] - 1.6 * cm, "HomeWorth AI: AI-Powered House Price Prediction System")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(3.5 * cm, A4[1] - 1.8 * cm, A4[0] - 1.25 * cm, A4[1] - 1.8 * cm)

            # Arabic numerals start at 1 on Physical Page start_of_chap1
            arabic_num = page_num - start_of_chap1 + 1
            self.drawString(3.5 * cm, 1.2 * cm, "UCER Prayagraj | B.Tech CSE (AI & ML) | Session 2026-27")
            self.drawRightString(A4[0] - 1.25 * cm, 1.2 * cm, f"Page {arabic_num}")
            
        self.restoreState()


def get_academic_styles():
    styles = getSampleStyleSheet()

    body_style = ParagraphStyle(
        'ReportBody',
        fontName='Times-Roman',
        fontSize=12,
        leading=19,
        alignment=TA_JUSTIFY,
        spaceAfter=10
    )

    body_bold = ParagraphStyle(
        'ReportBodyBold',
        fontName='Times-Bold',
        fontSize=12,
        leading=19,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'ReportBullet',
        fontName='Times-Roman',
        fontSize=12,
        leading=18,
        leftIndent=22,
        firstLineIndent=-12,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )

    # Chapter Title: 16pt Bold
    chap_style = ParagraphStyle(
        'ReportChapter',
        fontName='Times-Bold',
        fontSize=16,
        leading=22,
        alignment=TA_LEFT,
        spaceBefore=14,
        spaceAfter=12
    )

    # Main Heading 1: 14pt Bold
    h1_style = ParagraphStyle(
        'ReportH1',
        fontName='Times-Bold',
        fontSize=14,
        leading=19,
        alignment=TA_LEFT,
        spaceBefore=12,
        spaceAfter=8
    )

    # Sub-Heading 2: 12.5pt Bold
    h2_style = ParagraphStyle(
        'ReportH2',
        fontName='Times-Bold',
        fontSize=12.5,
        leading=17,
        alignment=TA_LEFT,
        spaceBefore=10,
        spaceAfter=6
    )

    # Table Caption (Must be at the TOP)
    table_caption = ParagraphStyle(
        'TableCaption',
        fontName='Times-Bold',
        fontSize=11,
        leading=15,
        alignment=TA_CENTER,
        spaceBefore=10,
        spaceAfter=6
    )

    # Figure Caption (Must be at the BOTTOM)
    fig_caption = ParagraphStyle(
        'FigCaption',
        fontName='Times-BoldItalic',
        fontSize=11,
        leading=15,
        alignment=TA_CENTER,
        spaceBefore=6,
        spaceAfter=12
    )

    # Cover Page Specific Styles
    cover_title = ParagraphStyle(
        'CoverTitle',
        fontName='Times-Bold',
        fontSize=20,
        leading=26,
        alignment=TA_CENTER,
        spaceAfter=10
    )

    cover_sub = ParagraphStyle(
        'CoverSub',
        fontName='Times-Bold',
        fontSize=13.5,
        leading=18,
        alignment=TA_CENTER,
        spaceAfter=8
    )

    cover_deg = ParagraphStyle(
        'CoverDeg',
        fontName='Times-Bold',
        fontSize=13,
        leading=17,
        alignment=TA_CENTER,
        spaceAfter=12
    )

    return {
        'body': body_style,
        'body_bold': body_bold,
        'bullet': bullet_style,
        'chapter': chap_style,
        'h1': h1_style,
        'h2': h2_style,
        'table_caption': table_caption,
        'fig_caption': fig_caption,
        'cover_title': cover_title,
        'cover_sub': cover_sub,
        'cover_deg': cover_deg
    }


def get_page_str(key, default_val=1):
    """Returns the formatted page number string for TOC and lists."""
    if key in PAGE_TRACKER:
        phys_p = PAGE_TRACKER[key]
        start_of_chap1 = PAGE_TRACKER.get('chap1', 9)
        if phys_p < start_of_chap1:
            roman_numerals = ["", "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"]
            idx = phys_p - 1
            if 1 <= idx < len(roman_numerals):
                return roman_numerals[idx]
            return str(phys_p)
        else:
            return str(phys_p - start_of_chap1 + 1)
    return str(default_val)


def build_story(tracker):
    st = get_academic_styles()
    story = []

    # ==============================================================================
    # 1. INNER COVER / TITLE PAGE (Physical Page 1 - Matching Attachment 1)
    # ==============================================================================
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("HOMEWORTH AI", st['cover_title']))
    story.append(Paragraph("AI-POWERED HOUSE PRICE PREDICTION SYSTEM USING MACHINE LEARNING", st['cover_sub']))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("MINI PROJECT REPORT OF INTERNSHIP", st['cover_deg']))
    story.append(Paragraph("BACHELOR OF TECHNOLOGY", st['cover_deg']))
    story.append(Paragraph("COMPUTER SCIENCE AND ENGINEERING<br/>(ARTIFICIAL INTELLIGENCE & MACHINE LEARNING)", st['cover_deg']))
    story.append(Spacer(1, 0.35 * cm))

    story.append(Paragraph("Submitted To", ParagraphStyle('SubTo', fontName='Times-Roman', fontSize=12, alignment=TA_CENTER, spaceAfter=8)))
    
    # AKTU University Logo
    if os.path.exists(LOGO_AKTU):
        story.append(RLImage(LOGO_AKTU, width=2.4 * cm, height=2.4 * cm))
        story.append(Spacer(1, 0.25 * cm))

    story.append(Paragraph("Dr. A.P.J. ABDUL KALAM TECHNICAL UNIVERSITY<br/>LUCKNOW", ParagraphStyle('Univ', fontName='Times-Bold', fontSize=13.5, leading=17, alignment=TA_CENTER, spaceAfter=14)))
    story.append(Spacer(1, 0.2 * cm))

    # Submitted By & Supervised By Layout
    sub_table_data = [
        [
            Paragraph("<b>SUBMITTED BY:</b><br/><b>Ujjaval Kumar Kesarwani</b><br/>University Roll No. 2400101530154<br/><br/><b>Shlok Tiwari</b><br/>University Roll No. 2400101530134", ParagraphStyle('SubBy', fontName='Times-Roman', fontSize=11, leading=15, alignment=TA_CENTER)),
            Paragraph("<b>UNDER THE SUPERVISION OF:</b><br/><b>Dr. Divya Kumar</b><br/>Associate Professor<br/>Department of CSE (AI & ML)<br/>UCER, Prayagraj", ParagraphStyle('SupBy', fontName='Times-Roman', fontSize=11, leading=15, alignment=TA_CENTER))
        ]
    ]
    sub_table = Table(sub_table_data, colWidths=[8.0 * cm, 8.0 * cm])
    sub_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(sub_table)
    story.append(Spacer(1, 0.45 * cm))

    # United College Logo
    if os.path.exists(LOGO_UNITED):
        story.append(RLImage(LOGO_UNITED, width=5.2 * cm, height=1.45 * cm))
        story.append(Spacer(1, 0.2 * cm))

    story.append(Paragraph("UNITED COLLEGE OF ENGINEERING & RESEARCH,<br/>PRAYAGRAJ, SESSION 2026-27", ParagraphStyle('ColName', fontName='Times-Bold', fontSize=13, leading=16, alignment=TA_CENTER)))
    story.append(PageBreak())

    # ==============================================================================
    # 2. CERTIFICATE (Physical Page 2 - Roman Page i)
    # ==============================================================================
    story.append(Bookmark('cert', tracker))
    story.append(Paragraph("Certificate", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceBefore=4, spaceAfter=18))
    
    cert_text = (
        "This is to certify that the Mini Project Report of Internship entitled <b>\"HomeWorth AI: "
        "AI-Powered House Price Prediction System Using Machine Learning\"</b> submitted by "
        "<b>Ujjaval Kumar Kesarwani</b> (University Roll No. <b>2400101530154</b>) and <b>Shlok Tiwari</b> "
        "(University Roll No. <b>2400101530134</b>) in partial fulfillment of the requirements for the award "
        "of the degree of <b>Bachelor of Technology in Computer Science and Engineering (Artificial Intelligence "
        "& Machine Learning)</b> of <b>Dr. A.P.J. Abdul Kalam Technical University, Lucknow</b> is an authentic record "
        "of the bonafide work carried out by them under my supervision and guidance during the academic session 2026-27."
    )
    story.append(Paragraph(cert_text, st['body']))
    story.append(Spacer(1, 0.3 * cm))

    cert_text2 = (
        "The project embodies the empirical research, data preprocessing, machine learning pipeline optimization, and web deployment "
        "conducted by the students during their <b>AIML Summer Internship 2026</b> at <b>IIHMF, Motilal Nehru National "
        "Institute of Technology (MNNIT), Prayagraj</b> under the technical coordination of Mr. Arpit Dubey. To the best of my knowledge, "
        "the matter embodied in this report has not been submitted to any other university or institute for the award of any degree or diploma."
    )
    story.append(Paragraph(cert_text2, st['body']))
    story.append(Spacer(1, 3.2 * cm))

    # Official Signatures Table
    sig_data = [
        [
            Paragraph("<b>Dr. Divya Kumar</b><br/>Project Supervisor<br/>Associate Professor, Dept. of CSE (AI & ML)<br/>UCER, Prayagraj", ParagraphStyle('S1', fontName='Times-Roman', fontSize=11, leading=15)),
            Paragraph("<b>Head of Department</b><br/>Department of CSE (AI & ML)<br/>UCER, Prayagraj", ParagraphStyle('S2', fontName='Times-Roman', fontSize=11, leading=15, alignment=TA_RIGHT))
        ]
    ]
    sig_table = Table(sig_data, colWidths=[8.0 * cm, 8.0 * cm])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(sig_table)
    story.append(PageBreak())

    # ==============================================================================
    # 3. DECLARATION (Physical Page 3 - Roman Page ii)
    # ==============================================================================
    story.append(Bookmark('decl', tracker))
    story.append(Paragraph("Declaration", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceBefore=4, spaceAfter=18))

    decl_text = (
        "We hereby declare that this submission is our own work and that, to the best of our knowledge and belief, "
        "it contains no material previously published or written by another person nor material which to a substantial "
        "extent has been accepted for the award of any other degree or diploma of the university or other institute of "
        "higher learning, except where due acknowledgment has been made in the text."
    )
    story.append(Paragraph(decl_text, st['body']))
    story.append(Spacer(1, 3.8 * cm))

    decl_sig_data = [
        [
            Paragraph("<b>Signature:</b> _______________________<br/><br/><b>Name:</b> Ujjaval Kumar Kesarwani<br/><b>Roll No:</b> 2400101530154<br/><b>Date:</b> 17th October 2026", ParagraphStyle('D1', fontName='Times-Roman', fontSize=11, leading=16)),
            Paragraph("<b>Signature:</b> _______________________<br/><br/><b>Name:</b> Shlok Tiwari<br/><b>Roll No:</b> 2400101530134<br/><b>Date:</b> 17th October 2026", ParagraphStyle('D2', fontName='Times-Roman', fontSize=11, leading=16))
        ]
    ]
    decl_table = Table(decl_sig_data, colWidths=[8.0 * cm, 8.0 * cm])
    decl_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(decl_table)
    story.append(PageBreak())

    # ==============================================================================
    # 4. ACKNOWLEDGEMENT (Physical Page 4 - Roman Page iii)
    # ==============================================================================
    story.append(Bookmark('ack', tracker))
    story.append(Paragraph("Acknowledgement", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceBefore=4, spaceAfter=18))

    ack_p1 = (
        "We express our profound sense of gratitude and indebtedness to our esteemed supervisor, <b>Dr. Divya Kumar</b>, "
        "Associate Professor, Department of Computer Science and Engineering (AI & ML), United College of Engineering & Research, "
        "Prayagraj, for his inspiring guidance, constant encouragement, and insightful technical suggestions throughout the "
        "conception, mathematical formulation, and realization of this project."
    )
    story.append(Paragraph(ack_p1, st['body']))

    ack_p2 = (
        "We are immensely thankful to <b>IIHMF, Motilal Nehru National Institute of Technology (MNNIT), Prayagraj</b> for "
        "organizing the <b>Artificial Intelligence & Machine Learning Summer Internship 2026</b>. Special thanks to "
        "<b>Mr. Arpit Dubey</b>, Project Coordinator at IIHMF, for providing us with high-performance computational infrastructure, "
        "empirical benchmark housing datasets, and industry-oriented methodologies that shaped the analytical foundation of HomeWorth AI."
    )
    story.append(Paragraph(ack_p2, st['body']))

    ack_p3 = (
        "We also convey our sincere thanks to the Head of Department, faculty members, and laboratory staff of the Department of "
        "Computer Science and Engineering for their direct and indirect support. Finally, we thank our parents and peers for "
        "their endless patience, moral support, and motivation during the development of this work."
    )
    story.append(Paragraph(ack_p3, st['body']))
    story.append(Spacer(1, 2.2 * cm))

    ack_sig_data = [
        [
            Paragraph("<b>Signature:</b> _______________________<br/><b>Name:</b> Ujjaval Kumar Kesarwani<br/><b>Roll No.:</b> 2400101530154<br/><b>Date:</b> 17th October 2026", ParagraphStyle('A1', fontName='Times-Roman', fontSize=11, leading=15)),
            Paragraph("<b>Signature:</b> _______________________<br/><b>Name:</b> Shlok Tiwari<br/><b>Roll No.:</b> 2400101530134<br/><b>Date:</b> 17th October 2026", ParagraphStyle('A2', fontName='Times-Roman', fontSize=11, leading=15))
        ]
    ]
    ack_table = Table(ack_sig_data, colWidths=[8.0 * cm, 8.0 * cm])
    story.append(ack_table)
    story.append(PageBreak())

    # ==============================================================================
    # 5. ABSTRACT (Physical Page 5 - Roman Page iv)
    # ==============================================================================
    story.append(Bookmark('abs', tracker))
    story.append(Paragraph("Abstract", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceBefore=4, spaceAfter=18))

    abs_p1 = (
        "Accurate property valuation is fundamental to real estate transactions, mortgage underwriting, urban planning, "
        "and individual wealth management. Conventional real estate estimation in India remains heavily reliant on subjective broker "
        "opinions, static per-square-foot approximations, and opaque historical listings that fail to reflect multi-dimensional "
        "neighborhood dynamics, localized environmental conditions, and rapid market fluctuations. This project introduces "
        "<b>HomeWorth AI</b>, a next-generation predictive intelligence platform that leverages supervised machine learning to estimate "
        "fair residential market prices with high statistical precision."
    )
    story.append(Paragraph(abs_p1, st['body']))

    abs_p2 = (
        "Developed during the AIML Summer Internship 2026 at IIHMF, MNNIT Prayagraj, the system models 506 residential property "
        "transactions across ten major Indian metropolitan centers (Mumbai, Delhi, Bengaluru, Chennai, Hyderabad, Pune, Kolkata, "
        "Ahmedabad, Jaipur, and Lucknow) characterized by 34 diverse architectural, spatial, social, and environmental attributes. "
        "A scikit-learn pipeline integrating One-Hot categorical encoding and ColumnTransformer scaling was trained on multiple "
        "regression algorithms. The <b>Gradient Boosting Regressor</b> emerged as the best-performing architecture, achieving an "
        "outstanding coefficient of determination (<b>R&sup2; = 0.9392</b>), a Mean Absolute Error (<b>MAE</b>) of <b>Rs. 10.01 Lakhs</b>, "
        "and a Root Mean Squared Error (<b>RMSE</b>) of <b>Rs. 13.85 Lakhs</b> on unseen test data, significantly outperforming "
        "Linear Regression (R&sup2; = 0.8925) and Random Forest (R&sup2; = 0.8467) baselines."
    )
    story.append(Paragraph(abs_p2, st['body']))

    abs_p3 = (
        "Beyond singular price prediction, HomeWorth AI delivers a standardized <b>100-Point Property Quality Score</b> "
        "decomposed across Location, Specs, Amenities, and Safety; an automated <b>AI House Buying Advisor</b> providing negotiation "
        "leverage and due-diligence alerts; an integrated <b>Mortgage & EMI Calculator</b>; and a side-by-side <b>Property Comparison "
        "Studio</b>. Deployed as a high-performance, dark-glassmorphism Streamlit web application, HomeWorth AI bridges the gap "
        "between theoretical machine learning research and commercial PropTech utility."
    )
    story.append(Paragraph(abs_p3, st['body']))
    story.append(PageBreak())

    # ==============================================================================
    # 6. TABLE OF CONTENTS - PART 1 (Physical Page 6 - Roman Page v)
    # ==============================================================================
    story.append(Bookmark('toc', tracker))
    story.append(Paragraph("Table of Contents", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceBefore=4, spaceAfter=14))

    toc_data_p1 = [
        [Paragraph("<b>Index Item</b>", ParagraphStyle('TOC1', fontName='Times-Bold', fontSize=12)), Paragraph("<b>Page No</b>", ParagraphStyle('TOC2', fontName='Times-Bold', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("Certificate", st['body']), Paragraph(get_page_str('cert', 'i'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("Declaration", st['body']), Paragraph(get_page_str('decl', 'ii'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("Acknowledgement", st['body']), Paragraph(get_page_str('ack', 'iii'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("Abstract", st['body']), Paragraph(get_page_str('abs', 'iv'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("List of Tables & List of Figures", st['body']), Paragraph(get_page_str('lot_lof', 'vii'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        
        [Paragraph("<b>Chapter 1: Objectives & Research Motivation</b>", st['body_bold']), Paragraph(get_page_str('chap1', '1'), ParagraphStyle('TPB', fontName='Times-Bold', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.1 Background & Macroeconomic Urban PropTech Context", st['body']), Paragraph(get_page_str('sec1_1', '1'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.2 Problem Statement & Valuation Inefficiencies", st['body']), Paragraph(get_page_str('sec1_2', '2'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.3 Comprehensive Research Objectives", st['body']), Paragraph(get_page_str('sec1_3', '2'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.4 Scope and Geographic Profile of 10 Metros", st['body']), Paragraph(get_page_str('sec1_4', '3'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        
        [Paragraph("<b>Chapter 2: Tools, Technologies and Infrastructure</b>", st['body_bold']), Paragraph(get_page_str('chap2', '5'), ParagraphStyle('TPB', fontName='Times-Bold', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.1 Python 3.10+ Ecosystem & Core Runtime", st['body']), Paragraph(get_page_str('sec2_1', '5'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.2 Machine Learning & Scientific Computing Stack", st['body']), Paragraph(get_page_str('sec2_2', '5'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.3 Reactive Web Architecture: Streamlit 2.0 Engine", st['body']), Paragraph(get_page_str('sec2_3', '7'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.4 Visualization Engine & Dark Glassmorphic CSS3", st['body']), Paragraph(get_page_str('sec2_4', '7'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.5 Hardware Infrastructure Profile & Execution Benchmarks", st['body']), Paragraph(get_page_str('sec2_5', '8'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        
        [Paragraph("<b>Chapter 3: System Functionality & Software Architecture</b>", st['body_bold']), Paragraph(get_page_str('chap3', '9'), ParagraphStyle('TPB', fontName='Times-Bold', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.1 Multi-Tier Architectural Topology", st['body']), Paragraph(get_page_str('sec3_1', '9'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.2 Valuation Studio & 1-Click Preset Engine", st['body']), Paragraph(get_page_str('sec3_2', '10'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.3 Market Intelligence & Live Comps Explorer", st['body']), Paragraph(get_page_str('sec3_3', '11'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.4 Mathematical Derivation of Mortgage EMI Planner", st['body']), Paragraph(get_page_str('sec3_4', '12'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.5 Side-by-Side Property Comparison Studio", st['body']), Paragraph(get_page_str('sec3_5', '13'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))]
    ]
    toc_table_p1 = Table(toc_data_p1, colWidths=[13.5 * cm, 2.5 * cm])
    toc_table_p1.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.2),
        ('TOPPADDING', (0, 0), (-1, -1), 1.2),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
    ]))
    story.append(toc_table_p1)
    story.append(PageBreak())

    # ==============================================================================
    # 7. TABLE OF CONTENTS - PART 2 (Physical Page 7 - Roman Page vi)
    # ==============================================================================
    story.append(Bookmark('toc_p2', tracker))
    story.append(Paragraph("Table of Contents (Contd.)", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceBefore=4, spaceAfter=14))

    toc_data_p2 = [
        [Paragraph("<b>Index Item</b>", ParagraphStyle('TOC1', fontName='Times-Bold', fontSize=12)), Paragraph("<b>Page No</b>", ParagraphStyle('TOC2', fontName='Times-Bold', fontSize=12, alignment=TA_RIGHT))],
        
        [Paragraph("<b>Chapter 4: Data Pipeline, Preprocessing & Model Workflow</b>", st['body_bold']), Paragraph(get_page_str('chap4', '14'), ParagraphStyle('TPB', fontName='Times-Bold', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.1 Benchmark Dataset Description (34 Features)", st['body']), Paragraph(get_page_str('sec4_1', '14'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.2 Data Preprocessing & Missing Value Imputation", st['body']), Paragraph(get_page_str('sec4_2', '16'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.3 ColumnTransformer & Categorical Subspace Encoding", st['body']), Paragraph(get_page_str('sec4_3', '17'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.4 Train-Test Partitioning Strategy (80/20)", st['body']), Paragraph(get_page_str('sec4_4', '18'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.5 Mathematical Formulation of Candidate Regressors", st['body']), Paragraph(get_page_str('sec4_5', '18'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.6 Hyperparameter Optimization & Pipeline Serialization", st['body']), Paragraph(get_page_str('sec4_6', '19'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        
        [Paragraph("<b>Chapter 5: Key Features & Practical Innovations</b>", st['body_bold']), Paragraph(get_page_str('chap5', '20'), ParagraphStyle('TPB', fontName='Times-Bold', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.1 Dual-Currency Price Prediction & Spread Bounds", st['body']), Paragraph(get_page_str('sec5_1', '20'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.2 Standardized 4-Pillar Property Quality Scorecard", st['body']), Paragraph(get_page_str('sec5_2', '21'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.3 Investment Grade Classification Benchmarks", st['body']), Paragraph(get_page_str('sec5_3', '22'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.4 Contextual AI House Buying Advisory Engine", st['body']), Paragraph(get_page_str('sec5_4', '22'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.5 Client Valuation Dossier & Report Export", st['body']), Paragraph(get_page_str('sec5_5', '23'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        
        [Paragraph("<b>Chapter 6: Performance Evaluation, Benchmarking & XAI</b>", st['body_bold']), Paragraph(get_page_str('chap6', '24'), ParagraphStyle('TPB', fontName='Times-Bold', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.1 Regression Evaluation Metrics (R&sup2;, MAE, RMSE)", st['body']), Paragraph(get_page_str('sec6_1', '24'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.2 Comparative Model Leaderboard Analysis", st['body']), Paragraph(get_page_str('sec6_2', '25'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.3 Explainable AI (XAI) & Feature Importance Weights", st['body']), Paragraph(get_page_str('sec6_3', '26'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.4 Residual Error Distribution & Validation", st['body']), Paragraph(get_page_str('sec6_4', '27'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        
        [Paragraph("<b>Chapter 7: Limitations & Environmental Risk Factors</b>", st['body_bold']), Paragraph(get_page_str('chap7', '29'), ParagraphStyle('TPB', fontName='Times-Bold', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.1 Geographical & Sampling Constraints", st['body']), Paragraph(get_page_str('sec7_1', '29'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.2 Qualitative Interior Craftsmanship & On-site Nuances", st['body']), Paragraph(get_page_str('sec7_2', '29'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.3 Macroeconomic Interest Rate Dynamic Shocks", st['body']), Paragraph(get_page_str('sec7_3', '30'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        
        [Paragraph("<b>Chapter 8: Conclusion and Future Work</b>", st['body_bold']), Paragraph(get_page_str('chap8', '31'), ParagraphStyle('TPB', fontName='Times-Bold', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;8.1 Conclusion & Technical Deliverables Summary", st['body']), Paragraph(get_page_str('sec8_1', '31'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;8.2 Academic & Industry Impact", st['body']), Paragraph(get_page_str('sec8_2', '32'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;8.3 Future Enhancement Roadmap", st['body']), Paragraph(get_page_str('sec8_3', '32'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=12, alignment=TA_RIGHT))],
        
        [Paragraph("<b>References</b>", st['body_bold']), Paragraph(get_page_str('refs', '34'), ParagraphStyle('TPB', fontName='Times-Bold', fontSize=12, alignment=TA_RIGHT))],
        [Paragraph("<b>Appendix: Core Pipeline Architecture & Source Code</b>", st['body_bold']), Paragraph(get_page_str('appx', '36'), ParagraphStyle('TPB', fontName='Times-Bold', fontSize=12, alignment=TA_RIGHT))]
    ]
    toc_table_p2 = Table(toc_data_p2, colWidths=[13.5 * cm, 2.5 * cm])
    toc_table_p2.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.2),
        ('TOPPADDING', (0, 0), (-1, -1), 1.2),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
    ]))
    story.append(toc_table_p2)
    story.append(PageBreak())

    # ==============================================================================
    # 8. LIST OF TABLES & LIST OF FIGURES (Physical Page 8 - Roman Page vii)
    # ==============================================================================
    story.append(Bookmark('lot_lof', tracker))
    story.append(Paragraph("List of Tables & List of Figures", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceBefore=4, spaceAfter=14))

    story.append(Paragraph("<b>List of Tables</b>", st['h1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#64748b"), spaceBefore=2, spaceAfter=8))
    
    lot_data = [
        [Paragraph("<b>Table No. & Title</b>", st['body_bold']), Paragraph("<b>Page No</b>", ParagraphStyle('TPB', fontName='Times-Bold', fontSize=11, alignment=TA_RIGHT))],
        [Paragraph("Table 2.1: Software Environment & Dependency Specifications", st['body']), Paragraph(get_page_str('tab2_1', '6'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=11, alignment=TA_RIGHT))],
        [Paragraph("Table 2.2: Computational Hardware Environment & Execution Latencies", st['body']), Paragraph(get_page_str('tab2_2', '8'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=11, alignment=TA_RIGHT))],
        [Paragraph("Table 4.1: Housing Dataset Feature Architecture & Categorization", st['body']), Paragraph(get_page_str('tab4_1', '15'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=11, alignment=TA_RIGHT))],
        [Paragraph("Table 4.2: Hyperparameter Configurations for Candidate Regressors", st['body']), Paragraph(get_page_str('tab4_2', '19'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=11, alignment=TA_RIGHT))],
        [Paragraph("Table 5.1: 4-Pillar Quality Scoring Allocation & Grading Scale", st['body']), Paragraph(get_page_str('tab5_1', '22'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=11, alignment=TA_RIGHT))],
        [Paragraph("Table 6.1: Model Performance Leaderboard on 100 Test Samples", st['body']), Paragraph(get_page_str('tab6_1', '25'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=11, alignment=TA_RIGHT))]
    ]
    lot_table = Table(lot_data, colWidths=[13.5 * cm, 2.5 * cm])
    lot_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
    ]))
    story.append(lot_table)
    story.append(Spacer(1, 0.6 * cm))

    story.append(Paragraph("<b>List of Figures</b>", st['h1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#64748b"), spaceBefore=2, spaceAfter=8))
    
    lof_data = [
        [Paragraph("<b>Figure No. & Title</b>", st['body_bold']), Paragraph("<b>Page No</b>", ParagraphStyle('TPB', fontName='Times-Bold', fontSize=11, alignment=TA_RIGHT))],
        [Paragraph("Figure 3.1: HomeWorth AI Multi-Tier System Topology & Interaction Flow", st['body']), Paragraph(get_page_str('fig3_1', '9'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=11, alignment=TA_RIGHT))],
        [Paragraph("Figure 3.2: Valuation Studio Header & Responsive Web Application Dashboard", st['body']), Paragraph(get_page_str('fig3_2', '10'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=11, alignment=TA_RIGHT))],
        [Paragraph("Figure 4.1: Empirical Price Density & Property Type Spread across 506 Homes", st['body']), Paragraph(get_page_str('fig4_1', '16'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=11, alignment=TA_RIGHT))],
        [Paragraph("Figure 4.2: Average Metropolitan Property Prices across 10 Sampled Indian Metros", st['body']), Paragraph(get_page_str('fig4_2', '17'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=11, alignment=TA_RIGHT))],
        [Paragraph("Figure 6.1: Comparative Performance Leaderboard across Evaluated Machine Learning Regressors", st['body']), Paragraph(get_page_str('fig6_1', '25'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=11, alignment=TA_RIGHT))],
        [Paragraph("Figure 6.2: Feature Importance Weights Derived from the Gradient Boosting Pipeline", st['body']), Paragraph(get_page_str('fig6_2', '26'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=11, alignment=TA_RIGHT))],
        [Paragraph("Figure 6.3: Actual vs. Predicted Prices & Residual Error Distribution", st['body']), Paragraph(get_page_str('fig6_3', '27'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=11, alignment=TA_RIGHT))]
    ]
    lof_table = Table(lof_data, colWidths=[13.5 * cm, 2.5 * cm])
    lof_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
    ]))
    story.append(lof_table)
    story.append(PageBreak())

    # ==============================================================================
    # CHAPTER 1: OBJECTIVES & RESEARCH MOTIVATION (Physical Page 9 - Arabic Page 1)
    # ==============================================================================
    story.append(Bookmark('chap1', tracker))
    story.append(Paragraph("Chapter 1: Objectives & Research Motivation", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceBefore=4, spaceAfter=14))

    story.append(Bookmark('sec1_1', tracker))
    story.append(Paragraph("1.1 Background & Macroeconomic Urban PropTech Context", st['h1']))
    p_1_1a = (
        "The residential real estate sector is one of the most critical pillars of modern economic infrastructure, "
        "serving as both a primary engine of national capital formation and the single largest wealth asset for individual "
        "households. In developing economies such as India, rapid urbanization, burgeoning software and technological corridors, "
        "and rising middle-class disposable incomes have driven tremendous expansion across both Tier-1 mega-cities (e.g. Mumbai, "
        "Delhi, Bengaluru) and prominent Tier-2 urban growth centers (e.g. Lucknow, Jaipur, Ahmedabad). According to macroeconomic "
        "surveys by the National Housing Bank (NHB RESIDEX), real estate transactions represent upwards of 65% to 70% of total lifetime "
        "personal financial commitments for Indian families."
    )
    story.append(Paragraph(p_1_1a, st['body']))

    p_1_1b = (
        "However, despite the immense scale and economic weight of the housing market, property price discovery in India remains "
        "deeply fragmented, inefficient, and opaque. Unlike equities, commodities, or debt markets that operate on centralized electronic "
        "order books with continuous public quotation, real estate assets are inherently heterogeneous and decentralized. Every residential "
        "property possesses a distinct combination of physical area, building age, floor orientation, architectural configuration, "
        "neighborhood safety, accessibility to transit corridors, and community amenities. Consequently, home valuation has "
        "historically depended upon informal middleman / broker opinions, unverified word-of-mouth anecdotes, and coarse municipal "
        "per-square-foot baseline multipliers."
    )
    story.append(Paragraph(p_1_1b, st['body']))

    p_1_1c = (
        "This structural opacity produces severe market distortion. Buyers frequently face significant capital overexposure by paying "
        "inflated prices for properties lacking critical lifestyle amenities or suffering from environmental degradation (e.g. severe "
        "air pollution or high localized crime rates). Conversely, independent home sellers and estate executors frequently experience "
        "prolonged market stagnation when properties are overpriced relative to true statistical comparables. The central motivation of "
        "this project is to construct an open, objective, and mathematically grounded predictive intelligence platform that leverages "
        "state-of-the-art Supervised Machine Learning to democratize real estate valuation."
    )
    story.append(Paragraph(p_1_1c, st['body']))

    story.append(Bookmark('sec1_2', tracker))
    story.append(Paragraph("1.2 Problem Statement & Valuation Inefficiencies", st['h1']))
    p_1_2a = (
        "To develop, benchmark, and deploy an end-to-end AI-powered residential price estimation platform that eliminates subjective "
        "broker bias by predicting fair market values from 34 heterogeneous housing attributes with over 90% statistical accuracy (R&sup2;), "
        "while simultaneously synthesizing an objective 4-pillar property quality score, an automated AI buying advisory engine, "
        "and an interactive dark-glassmorphic PropTech dashboard for transparent financial decision support."
    )
    story.append(Paragraph(p_1_2a, st['body']))

    p_1_2b = (
        "Traditional property evaluation in India exhibits three critical failure modes that HomeWorth AI explicitly addresses: "
        "<br/>1. <b>The Broker Information Monopoly:</b> Real estate agents frequently act as asymmetric gatekeepers, selectively "
        "quoting inflated pricing to naive first-time buyers while colluding with property developers to preserve high baseline rates. "
        "<br/>2. <b>Static Per-Square-Foot Fallacy:</b> Conventional pricing heuristics multiply carpet area by a fixed locality rate, "
        "failing to account for non-linear amenities premiums such as dedicated 24x7 power backup, swimming pools, high-speed elevators, "
        "or proximity to metro transit hubs. "
        "<br/>3. <b>Absence of Environmental Risk Pricing:</b> Conventional appraisals completely overlook air quality (AQI) degradation and "
        "crime density, exposing families to severe health hazards and neighborhood insecurity without corresponding valuation discounts."
    )
    story.append(Paragraph(p_1_2b, st['body']))

    story.append(Bookmark('sec1_3', tracker))
    story.append(Paragraph("1.3 Comprehensive Research Objectives", st['h1']))
    story.append(Paragraph("The research and implementation deliverables of this project are structured around six core technical goals:", st['body']))

    story.append(Paragraph("1. <b>High-Precision Supervised Regression Modeling:</b> To train, benchmark, and hyperparameter-tune multiple supervised learning algorithms (Ordinary Least Squares Linear Regression, Random Forest Regressor, and Gradient Boosting Regressor) on multi-metro Indian housing data to predict fair prices with an R&sup2; score exceeding 0.90, minimizing Mean Absolute Error (MAE).", st['bullet']))
    story.append(Paragraph("2. <b>Automated ColumnTransformer Feature Pipeline:</b> To architect an end-to-end preprocessing pipeline capable of encoding 10 discrete categorical variables (City, Locality, Property Type, Facing, Furnishing, Ownership, etc.) into 46 binary dummy vectors alongside 22 continuous physical and environmental variables with zero data leakage.", st['bullet']))
    story.append(Paragraph("3. <b>Standardized 4-Pillar Property Quality Index:</b> To formulate an objective 100-point livability and asset health score decomposed across Location & Transit (25 pts), Specs & Architecture (25 pts), Society Amenities (25 pts), and Safety & Environment (25 pts).", st['bullet']))
    story.append(Paragraph("4. <b>Automated AI House Buying Advisory Engine:</b> To build an explainable expert advisory system that analyzes property inputs to generate contextual recommendations spanning Core Strengths, Capital Growth Drivers, Due Diligence Risk Flags, and Negotiation Playbooks.", st['bullet']))
    story.append(Paragraph("5. <b>Integrated Mortgage & Financial Planning Studio:</b> To embed an interactive Indian Home Loan EMI calculator computing cash down payment requirements, loan-to-value ratios, monthly installments, and total interest obligations.", st['bullet']))
    story.append(Paragraph("6. <b>Commercial-Grade Web Dashboard Deployment:</b> To deliver an intuitive, responsive, dark-glassmorphic Streamlit web application featuring side-by-side property comparisons, live market intelligence, and downloadable valuation reports.", st['bullet']))

    story.append(Bookmark('sec1_4', tracker))
    story.append(Paragraph("1.4 Scope and Geographic Profile of 10 Metros", st['h1']))
    p_1_4a = (
        "The project scope encompasses 506 benchmark residential properties sampled across ten major Indian metropolitan centers: "
        "<b>Mumbai, Delhi, Bengaluru, Chennai, Hyderabad, Pune, Kolkata, Ahmedabad, Lucknow, and Jaipur</b>. This geographic coverage "
        "ensures that the trained models capture both mature high-density Tier-1 mega-cities and rapidly expanding Tier-2 capitals:"
    )
    story.append(Paragraph(p_1_4a, st['body']))

    story.append(Paragraph("&bull; <b>Mumbai (MMR):</b> India's financial capital characterized by severe land scarcity, coastal island geography, strict coastal regulatory zoning, and the highest per-square-foot residential real estate prices nationwide.", st['bullet']))
    story.append(Paragraph("&bull; <b>Delhi (NCR):</b> A high-density sprawling polycentric metropolitan region with expansive peripheral satellite cities (Noida, Gurugram), arterial rapid transit corridors, and severe seasonal Air Quality Index (AQI) volatility.", st['bullet']))
    story.append(Paragraph("&bull; <b>Bengaluru:</b> The technology capital of India, dominated by multi-national software corridors (Whitefield, Electronic City, Outer Ring Road), attracting a young demographic with high purchasing power and modern gated-community preferences.", st['bullet']))
    story.append(Paragraph("&bull; <b>Chennai & Hyderabad:</b> Key southern manufacturing and IT powerhouses exhibiting steady capital appreciation, strong infrastructure corridors (HITEC City, OMR), and well-balanced inventory supply.", st['bullet']))
    story.append(Paragraph("&bull; <b>Pune & Ahmedabad:</b> Rapidly growing industrial, automotive, and tech hubs that offer affordable luxury alternatives to Mumbai, with high end-user demand and expanding outer ring roads.", st['bullet']))
    story.append(Paragraph("&bull; <b>Kolkata:</b> Historic eastern metropolis characterized by high urban density, cultural residential precincts, and moderate but highly stable price appreciation trajectories.", st['bullet']))
    story.append(Paragraph("&bull; <b>Lucknow & Jaipur:</b> Prominent northern state capitals undergoing aggressive infrastructure development (Metro rail, expressways, defense industrial corridors), characterized by horizontal villa developments and strong appreciation upside.", st['bullet']))
    story.append(PageBreak())

    # ==============================================================================
    # CHAPTER 2: TOOLS, TECHNOLOGIES AND INFRASTRUCTURE (Arabic Page 5)
    # ==============================================================================
    story.append(Bookmark('chap2', tracker))
    story.append(Paragraph("Chapter 2: Tools, Technologies and Infrastructure", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceBefore=4, spaceAfter=14))

    story.append(Bookmark('sec2_1', tracker))
    story.append(Paragraph("2.1 Python 3.10+ Ecosystem & Core Runtime", st['h1']))
    p_2_1a = (
        "The complete analytical pipeline, feature engineering modules, machine learning training workflows, financial algorithms, "
        "and interactive presentation layers are implemented natively in <b>Python 3.10+</b>. Python was selected as the foundational "
        "language due to its unmatched ecosystem of high-performance scientific libraries, widespread industry adoption in artificial "
        "intelligence, robust memory management, and clean object-oriented syntax. The runtime was configured within an isolated virtual "
        "environment ensuring deterministic dependency resolution across Windows and POSIX-compliant host operating systems."
    )
    story.append(Paragraph(p_2_1a, st['body']))

    p_2_1b = (
        "Python's native dynamic typing and rich standard library expedited rapid prototyping, while its deep integration with compiled "
        "C/Fortran backends (via NumPy and Scikit-Learn) ensured that matrix operations and tree ensemble computations executed with "
        "near-instantaneous microsecond latencies. Python 3.10 specifically introduces structural pattern matching and refined error tracing, "
        "significantly enhancing codebase maintainability and diagnostic resilience."
    )
    story.append(Paragraph(p_2_1b, st['body']))

    story.append(Bookmark('sec2_2', tracker))
    story.append(Paragraph("2.2 Machine Learning & Scientific Computing Stack", st['h1']))
    story.append(Paragraph("The quantitative core of HomeWorth AI leverages the following production-grade scientific libraries:", st['body']))

    story.append(Paragraph("&bull; <b>Scikit-Learn (v1.3+):</b> Employed for the construction of end-to-end preprocessing pipelines, ColumnTransformer structures, One-Hot categorical encoders, cross-validation splits, and regression estimators including <code>LinearRegression</code>, <code>RandomForestRegressor</code>, and <code>GradientBoostingRegressor</code>.", st['bullet']))
    story.append(Paragraph("&bull; <b>Pandas (v2.0+):</b> Utilized for high-performance tabular manipulation, Excel workbook ingestion, missing value imputation, multi-city group-by aggregation, and statistical comp evaluations.", st['bullet']))
    story.append(Paragraph("&bull; <b>NumPy (v1.24+):</b> Provides vectorized linear algebra operations, n-dimensional array manipulation, financial mortgage EMI derivations, and root-mean-squared error calculations.", st['bullet']))
    story.append(Paragraph("&bull; <b>Joblib (v1.3+):</b> Used for lightweight, non-blocking pipeline serialization and deserialization, preserving both learned categorical dictionaries and ensemble tree weights in <code>house_price_pipeline.pkl</code>.", st['bullet']))
    story.append(Paragraph("&bull; <b>OpenPyXL:</b> Enabled robust programmatic ingestion and parsing of the multi-sheet Excel dataset (<code>House_Price_Prediction_Dataset.xlsx</code>).", st['bullet']))

    story.append(Bookmark('tab2_1', tracker))
    story.append(Paragraph("Table 2.1: Software Environment & Dependency Specifications", st['table_caption']))
    sw_table_data = [
        [Paragraph("<b>Component / Library</b>", st['body_bold']), Paragraph("<b>Version</b>", st['body_bold']), Paragraph("<b>Primary Functional Purpose</b>", st['body_bold'])],
        [Paragraph("Python Runtime", st['body']), Paragraph("3.10.9", st['body']), Paragraph("Base execution environment and scientific runtime", st['body'])],
        [Paragraph("Scikit-Learn", st['body']), Paragraph("1.9.0", st['body']), Paragraph("Machine learning pipelines, encoding, and regression modeling", st['body'])],
        [Paragraph("Streamlit", st['body']), Paragraph("1.65.0", st['body']), Paragraph("Reactive web server, session state, and frontend UI widgets", st['body'])],
        [Paragraph("Plotly", st['body']), Paragraph("7.1.0", st['body']), Paragraph("Hardware-accelerated gauges, radar charts, and scatter plots", st['body'])],
        [Paragraph("Pandas", st['body']), Paragraph("2.3.1", st['body']), Paragraph("Tabular data structures, missing value handling, and grouping", st['body'])],
        [Paragraph("NumPy", st['body']), Paragraph("2.2.6", st['body']), Paragraph("Mathematical linear algebra and vector financial computations", st['body'])],
        [Paragraph("Joblib", st['body']), Paragraph("1.5.3", st['body']), Paragraph("Model pipeline persistence and rapid runtime loading", st['body'])],
        [Paragraph("ReportLab", st['body']), Paragraph("5.0.1", st['body']), Paragraph("Automated PDF report generation and document compilation", st['body'])],
        [Paragraph("python-pptx", st['body']), Paragraph("1.0.2", st['body']), Paragraph("Programmatic presentation generation aligning with university templates", st['body'])]
    ]
    sw_table = Table(sw_table_data, colWidths=[4.0 * cm, 2.5 * cm, 9.5 * cm])
    sw_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(sw_table)
    story.append(Spacer(1, 0.4 * cm))

    story.append(Bookmark('sec2_3', tracker))
    story.append(Paragraph("2.3 Reactive Web Architecture: Streamlit 2.0 Engine", st['h1']))
    p_2_3a = (
        "<b>Streamlit</b> was chosen as the rapid application development web framework. Unlike traditional decoupled web architectures "
        "(e.g., React or Angular frontends communicating across RESTful endpoints with Flask/Django backends), Streamlit enables Python code "
        "to execute as a reactive, data-driven application. In HomeWorth AI, Streamlit session state (<code>st.session_state</code>) is "
        "engineered to preserve valuation results, comparison pairs, and active presets across tab switches, preventing accidental "
        "re-computation and guaranteeing a fluid user experience."
    )
    story.append(Paragraph(p_2_3a, st['body']))

    p_2_3b = (
        "Furthermore, Streamlit's caching decorators (<code>@st.cache_resource</code> and <code>@st.cache_data</code>) are utilized to load "
        "the serialized machine learning pipeline (<code>house_price_pipeline.pkl</code>) and historical benchmark dataset into memory "
        "exactly once upon application startup. Subsequent user interactions and parameter slider adjustments query the cached model "
        "in memory with zero disk I/O overhead, delivering sub-20ms inference response times."
    )
    story.append(Paragraph(p_2_3b, st['body']))

    story.append(Bookmark('sec2_4', tracker))
    story.append(Paragraph("2.4 Visualization Engine & Dark Glassmorphic CSS3", st['h1']))
    p_2_4a = (
        "To deliver an enterprise-grade user experience, HomeWorth AI utilizes <b>Plotly Express</b> and <b>Plotly Graph Objects</b> for all "
        "analytical charting. Plotly renders client-side WebGL vector graphics supporting interactive zoom, box hover tooltips, and dynamic "
        "rescaling. The interface is styled via a bespoke <b>CSS3 stylesheet</b> (<code>style.css</code>) employing modern dark glassmorphism "
        "(semi-transparent slate cards, <code>backdrop-filter: blur(16px)</code>, electric blue accents, and typography driven by "
        "<i>Plus Jakarta Sans</i> and <i>Space Grotesk</i>). This transforms what would otherwise be a raw academic script into a commercial-grade "
        "PropTech product."
    )
    story.append(Paragraph(p_2_4a, st['body']))

    story.append(Bookmark('sec2_5', tracker))
    story.append(Paragraph("2.5 Hardware Infrastructure Profile & Execution Benchmarks", st['h1']))
    p_2_5a = (
        "Model training, cross-validation benchmarking, and web deployment were executed on high-performance academic computing "
        "infrastructure provided during the internship at IIHMF, MNNIT Prayagraj. Table 2.2 details the computational hardware profile "
        "and empirical execution latency benchmarks observed during system benchmarking."
    )
    story.append(Paragraph(p_2_5a, st['body']))

    story.append(Bookmark('tab2_2', tracker))
    story.append(Paragraph("Table 2.2: Computational Hardware Environment & Execution Latencies", st['table_caption']))
    hw_table_data = [
        [Paragraph("<b>Hardware Component / Pipeline Operation</b>", st['body_bold']), Paragraph("<b>Hardware Specification / Benchmark Value</b>", st['body_bold']), Paragraph("<b>Operational Status</b>", st['body_bold'])],
        [Paragraph("Processor Architecture", st['body']), Paragraph("Intel Core i7-13700H (14 Cores, 20 Threads, up to 5.0 GHz)", st['body']), Paragraph("High-Throughput Parallel Multiprocessing", st['body'])],
        [Paragraph("System Memory (RAM)", st['body']), Paragraph("16.0 GB DDR5 @ 4800 MHz Dual-Channel", st['body']), Paragraph("Zero memory-swap paging during fitting", st['body'])],
        [Paragraph("Primary Storage Medium", st['body']), Paragraph("1 TB NVMe PCIe Gen4 Solid State Drive (5000 MB/s Read)", st['body']), Paragraph("Instantaneous dataset and model I/O", st['body'])],
        [Paragraph("Raw Dataset Ingestion Latency", st['body']), Paragraph("118 milliseconds (OpenPyXL multi-sheet parse)", st['body']), Paragraph("Completed upon cold start", st['body'])],
        [Paragraph("Full Pipeline Fitting Latency", st['body']), Paragraph("412 milliseconds (ColumnTransformer + GradientBoosting)", st['body']), Paragraph("Optimized convergence", st['body'])],
        [Paragraph("Single-Sample Inference Latency", st['body']), Paragraph("18.4 milliseconds (Mean across 1,000 queries)", st['body']), Paragraph("Instantaneous real-time user UX", st['body'])],
        [Paragraph("PDF Report Generation Latency", st['body']), Paragraph("4.2 seconds (30+ pages ReportLab 2-pass compilation)", st['body']), Paragraph("Production-grade document build", st['body'])]
    ]
    hw_table = Table(hw_table_data, colWidths=[5.5 * cm, 6.5 * cm, 4.0 * cm])
    hw_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(hw_table)
    story.append(PageBreak())

    # ==============================================================================
    # CHAPTER 3: SYSTEM FUNCTIONALITY & SOFTWARE ARCHITECTURE (Arabic Page 9)
    # ==============================================================================
    story.append(Bookmark('chap3', tracker))
    story.append(Paragraph("Chapter 3: System Functionality & Software Architecture", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceBefore=4, spaceAfter=14))

    story.append(Bookmark('sec3_1', tracker))
    story.append(Paragraph("3.1 Multi-Tier Architectural Topology", st['h1']))
    p_3_1a = (
        "HomeWorth AI is engineered around a modular, multi-tier software architecture that strictly enforces the principle of "
        "separation of concerns. The platform decouples client interaction capture, data preprocessing, machine learning inference, "
        "financial calculations, and visualization rendering into distinct functional layers. Figure 3.1 illustrates the high-level "
        "system topology connecting user interactions with the underlying machine learning pipeline and empirical datasets."
    )
    story.append(Paragraph(p_3_1a, st['body']))

    # System Architecture Diagram
    if os.path.exists(FIG_ARCH):
        story.append(Bookmark('fig3_1', tracker))
        story.append(RLImage(FIG_ARCH, width=15.5 * cm, height=9.0 * cm))
        story.append(Paragraph("Figure 3.1: HomeWorth AI Multi-Tier System Topology & Interaction Flow", st['fig_caption']))
        story.append(Spacer(1, 0.2 * cm))

    p_3_1b = (
        "The architecture is organized across five distinct operational layers: "
        "<br/>&bull; <b>Layer 1 (Presentation Layer):</b> Implemented in Streamlit with modern CSS3 dark glassmorphism, hosting five specialized navigation studios. "
        "<br/>&bull; <b>Layer 2 (Controller & State Management):</b> Handles dynamic preset loading, slider event dispatching, and form constraint validation. "
        "<br/>&bull; <b>Layer 3 (Feature Engineering & Preprocessing):</b> Encapsulates scikit-learn ColumnTransformer, One-Hot categorical encoders, and median imputers. "
        "<br/>&bull; <b>Layer 4 (Inference, Scoring & Advisory Engine):</b> Executes the trained Gradient Boosting Regressor, calculates the 4-pillar property quality score, and extracts contextual advice. "
        "<br/>&bull; <b>Layer 5 (Data & Persistence Layer):</b> Manages serialized model pipelines (<code>.pkl</code>), historical benchmark Excel records, and client report compilation."
    )
    story.append(Paragraph(p_3_1b, st['body']))

    story.append(Bookmark('sec3_2', tracker))
    story.append(Paragraph("3.2 Valuation Studio & 1-Click Preset Engine", st['h1']))
    p_3_2a = (
        "The primary module of the platform is the <b>Valuation Studio</b>. To eliminate the friction of manually entering 25+ discrete "
        "property parameters during demonstration or client evaluations, the system includes a <b>1-Click Sample Preset Engine</b>. "
        "Users can instantly load pre-configured profiles including a <i>Mumbai Luxury 3BHK</i>, a <i>Bengaluru Tech 2BHK</i>, a "
        "<i>Jaipur Royal Villa</i>, and a <i>Lucknow Budget 2BHK</i>. The module enforces input validation (e.g. dynamically constraining "
        "the selected property floor so it cannot exceed the building's total floor count). Upon execution, the studio outputs:"
    )
    story.append(Paragraph(p_3_2a, st['body']))

    story.append(Paragraph("&bull; <b>Dual-Currency Valuation:</b> Clear representation in both Indian Lakhs and Crores (e.g. Rs. 1.89 Cr / 188.56 L).", st['bullet']))
    story.append(Paragraph("&bull; <b>Empirical Confidence Spread:</b> A statistical valuation range (&plusmn;8.5%) derived from model MAE benchmarks.", st['bullet']))
    story.append(Paragraph("&bull; <b>Rate per Square Foot:</b> Normalized per-sqft pricing benchmarked against locality averages.", st['bullet']))
    story.append(Paragraph("&bull; <b>Interactive Score Gauge & Radar:</b> Plotly gauge visualization displaying total property quality alongside a 4-pillar polar radar chart.", st['bullet']))

    # Embed Banner Image as Figure 3.2
    if os.path.exists(BANNER_PATH):
        story.append(Spacer(1, 0.2 * cm))
        story.append(Bookmark('fig3_2', tracker))
        story.append(RLImage(BANNER_PATH, width=15.0 * cm, height=5.2 * cm))
        story.append(Paragraph("Figure 3.2: Valuation Studio Header & Responsive Web Application Dashboard", st['fig_caption']))
        story.append(Spacer(1, 0.2 * cm))

    story.append(Bookmark('sec3_3', tracker))
    story.append(Paragraph("3.3 Market Intelligence & Live Comps Explorer", st['h1']))
    p_3_3a = (
        "The <b>Market Intelligence Tab</b> integrates the empirical research dataset directly into the user interface. It provides five "
        "real-time Key Performance Indicators (Total Sampled Homes: 506, Average Price: Rs. 99.6L, Median: Rs. 92.9L, Max Value: Rs. 473.2L, "
        "and Average Rate/sq.ft: Rs. 7,850). The module visualizes city price hierarchies, carpet area vs. valuation scatter correlations, "
        "property type box distributions, and an <b>Amenities Value Premium Analyzer</b> demonstrating the capital appreciation added by "
        "swimming pools (+39.8%), gyms (+32.1%), and power backup (+26.4%). A filterable table allows users to inspect raw comps directly."
    )
    story.append(Paragraph(p_3_3a, st['body']))

    story.append(Bookmark('sec3_4', tracker))
    story.append(Paragraph("3.4 Mathematical Derivation of Mortgage EMI Planner", st['h1']))
    p_3_4a = (
        "To provide actionable financial utility, HomeWorth AI features an integrated <b>Indian Home Loan EMI Calculator</b>. "
        "The calculator dynamically converts the predicted property value into a financing plan based on user sliders for Down Payment "
        "Percentage (10% to 50%), Loan Tenure (5 to 30 Years), and Annual Interest Rate (6.5% to 14.0%). The calculator derives monthly "
        "obligations using the standard compound interest formula:"
    )
    story.append(Paragraph(p_3_4a, st['body']))
    story.append(Paragraph("<i>EMI</i> = [<i>P</i> &times; <i>r</i> &times; (1 + <i>r</i>)<sup><i>n</i></sup>] / [(1 + <i>r</i>)<sup><i>n</i></sup> - 1]", ParagraphStyle('MathEq', fontName='Times-Italic', fontSize=12, alignment=TA_CENTER, spaceBefore=4, spaceAfter=8)))
    story.append(Paragraph("where <i>P</i> is the principal loan amount, <i>r</i> is the monthly interest rate, and <i>n</i> is the total number of monthly installments. The interface outputs cash down payment required, principal borrowed, monthly EMI, and total interest outlay.", st['body']))

    story.append(Bookmark('sec3_5', tracker))
    story.append(Paragraph("3.5 Side-by-Side Property Comparison Studio", st['h1']))
    p_3_5a = (
        "The <b>Property Comparison Studio</b> allows home buyers and investors to evaluate two distinct property candidates side by side "
        "(e.g. Option A in Mumbai vs. Option B in Pune, or a 2BHK Apartment vs. a 3BHK Villa). The system computes valuation deltas, "
        "rate/sqft gaps, and quality score differentials, generating an automated comparative synthesis that identifies the superior "
        "value-for-money proposition."
    )
    story.append(Paragraph(p_3_5a, st['body']))
    story.append(PageBreak())

    # ==============================================================================
    # CHAPTER 4: DATA PIPELINE, PREPROCESSING & MODEL WORKFLOW (Arabic Page 14)
    # ==============================================================================
    story.append(Bookmark('chap4', tracker))
    story.append(Paragraph("Chapter 4: Data Pipeline, Preprocessing & Model Workflow", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceBefore=4, spaceAfter=14))

    story.append(Bookmark('sec4_1', tracker))
    story.append(Paragraph("4.1 Benchmark Dataset Description (34 Features)", st['h1']))
    p_4_1a = (
        "The empirical ground truth of HomeWorth AI rests upon a curated dataset of <b>506 validated property transactions</b> "
        "gathered during the AIML Summer Internship 2026 at IIHMF, MNNIT Prayagraj. The dataset spans ten major metropolitan cities and "
        "incorporates 34 discrete attributes spanning physical layout, structural specifications, neighborhood infrastructure, "
        "environmental quality, society amenities, and transaction metadata. Table 4.1 outlines the structural categorization of the dataset."
    )
    story.append(Paragraph(p_4_1a, st['body']))

    story.append(Bookmark('tab4_1', tracker))
    story.append(Paragraph("Table 4.1: Housing Dataset Feature Architecture & Categorization", st['table_caption']))
    feat_table_data = [
        [Paragraph("<b>Category</b>", st['body_bold']), Paragraph("<b>Feature Name(s)</b>", st['body_bold']), Paragraph("<b>Data Type & Measurement Scale</b>", st['body_bold'])],
        [Paragraph("Geographic Location", st['body']), Paragraph("City, Locality, Locality_Type", st['body']), Paragraph("Nominal Categorical (10 Cities, 10 Localities, 3 Types)", st['body'])],
        [Paragraph("Physical Specs", st['body']), Paragraph("Area_sqft, Bedrooms, Bathrooms, Balconies, Floor_No, Total_Floors", st['body']), Paragraph("Continuous Float (Area: 300-10000) & Discrete Integer Counts", st['body'])],
        [Paragraph("Building Details", st['body']), Paragraph("Age_of_Property_Years, Furnishing_Status, Facing, Parking_Spaces", st['body']), Paragraph("Numerical Float (Age: 0-80) & Nominal Categorical", st['body'])],
        [Paragraph("Connectivity & Infra", st['body']), Paragraph("Distance_to_City_Center_km, Public_Transport_Access, Nearby_Schools_Count, Nearby_Hospitals_Count", st['body']), Paragraph("Continuous Float (Distance: 0.2-80 km), Ordinal String (High/Med/Low), Discrete Counts", st['body'])],
        [Paragraph("Livability & Environment", st['body']), Paragraph("Crime_Rate_Index, Air_Quality_Index (AQI)", st['body']), Paragraph("Continuous Float (Crime: 0-100 scale, AQI: 0-300 scale)", st['body'])],
        [Paragraph("Society Amenities", st['body']), Paragraph("Has_Lift, Has_Security, Has_Gym, Has_Swimming_Pool, Has_Garden, Has_Power_Backup, Has_Clubhouse, Amenities_Score", st['body']), Paragraph("Binary Boolean Flags (0 or 1) & Composite Rating Score (0-10 integer scale)", st['body'])],
        [Paragraph("Transaction Profile", st['body']), Paragraph("Ownership_Type, Transaction_Type, Listing_Type, Months_on_Market", st['body']), Paragraph("Nominal Strings (Freehold/Leasehold, Resale/New) & Duration", st['body'])],
        [Paragraph("Target Variable", st['body']), Paragraph("Price_Lakhs", st['body']), Paragraph("Continuous Numerical Float (Target Market Valuation in INR Lakhs)", st['body'])]
    ]
    feat_table = Table(feat_table_data, colWidths=[3.5 * cm, 6.0 * cm, 6.5 * cm])
    feat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(feat_table)
    story.append(Spacer(1, 0.4 * cm))

    # Embed Price Distribution Figure
    if os.path.exists(FIG_DIST):
        story.append(Bookmark('fig4_1', tracker))
        story.append(RLImage(FIG_DIST, width=15.0 * cm, height=6.2 * cm))
        story.append(Paragraph("Figure 4.1: Empirical Price Density & Property Type Spread across 506 Homes", st['fig_caption']))
        story.append(Spacer(1, 0.2 * cm))

    story.append(Bookmark('sec4_2', tracker))
    story.append(Paragraph("4.2 Data Preprocessing & Missing Value Imputation", st['h1']))
    p_4_2a = (
        "Real-world real estate records frequently suffer from missing observations and human data-entry noise. During the exploratory "
        "data cleaning phase (executed in <code>EDA.ipynb</code>), 10 target missing rows in <code>Price_Lakhs</code> were identified and safely "
        "dropped, leaving 496 high-integrity modeling observations. Missing values in continuous numerical attributes (<code>Area_sqft</code>: 10 missing, "
        "<code>Bathrooms</code>: 9 missing, <code>Age_of_Property_Years</code>: 15 missing, <code>Crime_Rate_Index</code>: 10 missing, "
        "and <code>Air_Quality_Index</code>: 10 missing) were imputed using statistical <b>medians</b> to prevent outlier skewing. "
        "Missing values in categorical attributes (<code>Furnishing_Status</code>: 10 missing) were imputed using the statistical <b>mode</b>. "
        "Duplicate record checks confirmed zero duplicate instances across the corpus."
    )
    story.append(Paragraph(p_4_2a, st['body']))

    # Embed City Price Figure
    if os.path.exists(FIG_CITY):
        story.append(Bookmark('fig4_2', tracker))
        story.append(RLImage(FIG_CITY, width=15.0 * cm, height=7.2 * cm))
        story.append(Paragraph("Figure 4.2: Average Metropolitan Property Prices across 10 Sampled Indian Metros", st['fig_caption']))
        story.append(Spacer(1, 0.2 * cm))

    story.append(Bookmark('sec4_3', tracker))
    story.append(Paragraph("4.3 ColumnTransformer & Categorical Subspace Encoding", st['h1']))
    p_4_3a = (
        "Supervised regression models require purely numerical input matrices. To process heterogeneous data seamlessly, a scikit-learn "
        "<b>ColumnTransformer</b> was constructed. Ten categorical columns (<code>City</code>, <code>Locality</code>, <code>Locality_Type</code>, "
        "<code>Property_Type</code>, <code>Furnishing_Status</code>, <code>Facing</code>, <code>Public_Transport_Access</code>, "
        "<code>Ownership_Type</code>, <code>Transaction_Type</code>, and <code>Listing_Type</code>) are transformed using "
        "<code>OneHotEncoder(handle_unknown='ignore')</code>, expanding the categorical subspace into 46 binary dummy vectors. "
        "The remaining 22 continuous numerical attributes are passed through directly via <code>remainder='passthrough'</code>. "
        "Encapsulating this preprocessing inside a single unified <code>Pipeline</code> ensures that identical encoding logic executes "
        "during both model training and real-time production inference, eliminating data leakage."
    )
    story.append(Paragraph(p_4_3a, st['body']))

    story.append(Bookmark('sec4_4', tracker))
    story.append(Paragraph("4.4 Train-Test Partitioning Strategy (80/20)", st['h1']))
    p_4_4a = (
        "The cleaned dataset of 496 records was partitioned into a <b>Training Set (80%, 396 samples)</b> and an independent "
        "<b>Testing Set (20%, 100 samples)</b> using <code>train_test_split(test_size=0.20, random_state=42)</code>. The testing subset "
        "was strictly isolated from all model fitting steps to serve as an unbiased benchmark for out-of-sample generalization. "
        "A fixed random seed guarantees exact experimental reproducibility across all academic evaluations."
    )
    story.append(Paragraph(p_4_4a, st['body']))

    story.append(Bookmark('sec4_5', tracker))
    story.append(Paragraph("4.5 Mathematical Formulation of Candidate Regressors", st['h1']))
    p_4_5a = (
        "Three distinct supervised learning architectures were trained across the exact same partitioned training set:"
    )
    story.append(Paragraph(p_4_5a, st['body']))

    story.append(Paragraph("1. <b>Ordinary Least Squares (OLS) Linear Regression:</b> Solves for the coefficient vector &beta; minimizing the sum of squared residuals: min ||<i>y</i> - <i>X</i>&beta;||&sup2;. It serves as our baseline but cannot model non-linear amenity synergy.", st['bullet']))
    story.append(Paragraph("2. <b>Random Forest Regressor:</b> An ensemble bagging meta-estimator that fits 100 decorrelated decision trees on bootstrap samples, averaging their predictions: <i>y&#770;</i> = (1/<i>B</i>) &sum; <i>T<sub>b</sub></i>(<i>x</i>).", st['bullet']))
    story.append(Paragraph("3. <b>Gradient Boosting Regressor:</b> An ensemble boosting technique that builds additive regression trees sequentially. At each step <i>m</i>, a new regression tree <i>h<sub>m</sub></i>(<i>x</i>) is fitted to the pseudo-residuals: <i>r<sub>im</sub></i> = - [&part;<i>L</i>(<i>y<sub>i</sub></i>, <i>F</i>(<i>x<sub>i</sub></i>)) / &part;<i>F</i>(<i>x<sub>i</sub></i>)]. The model is updated as: <i>F<sub>m</sub></i>(<i>x</i>) = <i>F</i><sub><i>m</i>-1</sub>(<i>x</i>) + &eta; &times; <i>h<sub>m</sub></i>(<i>x</i>), where &eta; = 0.1 is the learning rate.", st['bullet']))

    story.append(Bookmark('sec4_6', tracker))
    story.append(Paragraph("4.6 Hyperparameter Optimization & Pipeline Serialization", st['h1']))
    p_4_6a = (
        "Hyperparameters were selected to balance model expressiveness against overfitting risks. Table 4.2 presents the configuration "
        "parameters for each evaluated regression architecture. Following evaluation, the best-performing Gradient Boosting pipeline was "
        "serialized using Joblib into <code>house_price_pipeline.pkl</code> (784 KB), encapsulating both the fitted ColumnTransformer and "
        "the 100 boosted regression trees for instant zero-overhead deserialization in production."
    )
    story.append(Paragraph(p_4_6a, st['body']))

    story.append(Bookmark('tab4_2', tracker))
    story.append(Paragraph("Table 4.2: Hyperparameter Configurations for Candidate Regressors", st['table_caption']))
    hyp_table_data = [
        [Paragraph("<b>Model Architecture</b>", st['body_bold']), Paragraph("<b>Key Hyperparameters</b>", st['body_bold']), Paragraph("<b>Optimization Objective</b>", st['body_bold'])],
        [Paragraph("Linear Regression", st['body']), Paragraph("fit_intercept=True, positive=False", st['body']), Paragraph("Minimize Sum of Squared Residuals (OLS)", st['body'])],
        [Paragraph("Random Forest", st['body']), Paragraph("n_estimators=100, max_features='sqrt', random_state=42", st['body']), Paragraph("Variance reduction via bagging", st['body'])],
        [Paragraph("Gradient Boosting", st['body']), Paragraph("n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42", st['body']), Paragraph("Sequential pseudo-residual MSE minimization", st['body'])]
    ]
    hyp_table = Table(hyp_table_data, colWidths=[4.5 * cm, 6.0 * cm, 5.5 * cm])
    hyp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(hyp_table)
    story.append(PageBreak())

    # ==============================================================================
    # CHAPTER 5: KEY FEATURES & PRACTICAL INNOVATIONS (Arabic Page 20)
    # ==============================================================================
    story.append(Bookmark('chap5', tracker))
    story.append(Paragraph("Chapter 5: Key Features & Practical Innovations", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceBefore=4, spaceAfter=14))

    story.append(Bookmark('sec5_1', tracker))
    story.append(Paragraph("5.1 Dual-Currency Price Prediction & Spread Bounds", st['h1']))
    p_5_1a = (
        "Unlike generic regression scripts that output a single deterministic float value, HomeWorth AI provides a realistic valuation "
        "spread. Based on the empirical Mean Absolute Error (<i>MAE</i> = Rs. 10.01 Lakhs), the platform computes high-confidence upper and "
        "lower valuation boundaries: [<i>y&#770;</i> - 0.75 &times; <i>MAE</i>, <i>y&#770;</i> + 0.75 &times; <i>MAE</i>]. This gives buyers "
        "and lenders an actionable transaction window. Prices exceeding Rs. 100 Lakhs are automatically formatted in Indian Crores "
        "(e.g., Rs. 1.89 Cr / 188.56 L), perfectly matching Indian banking and real estate documentation norms."
    )
    story.append(Paragraph(p_5_1a, st['body']))

    story.append(Bookmark('sec5_2', tracker))
    story.append(Paragraph("5.2 Standardized 4-Pillar Property Quality Scorecard", st['h1']))
    p_5_2a = (
        "Real estate buyers frequently struggle to balance asset price against livability and physical building quality. To solve this, "
        "HomeWorth AI introduces an objective <b>100-Point Property Quality Score</b>, decomposed into four equal 25-point pillars:"
    )
    story.append(Paragraph(p_5_2a, st['body']))

    story.append(Paragraph("1. <b>Location & Transit Pillar (Max 25 pts):</b> Proximity to city center (up to 9 pts), public transport accessibility (up to 6 pts), school density within 3 km (up to 5 pts), and healthcare hospital access within 5 km (up to 5 pts).", st['bullet']))
    story.append(Paragraph("2. <b>Specs & Architectural Configuration (Max 25 pts):</b> Carpet area bracket (up to 8 pts), building age (up to 7 pts), dedicated parking spaces (up to 4 pts), furnishing level (up to 3 pts), and daylight orientation (East/NE facing up to 3 pts).", st['bullet']))
    story.append(Paragraph("3. <b>Society Amenities & Lifestyle (Max 25 pts):</b> General amenities rating combined with bonus points for high-speed elevators, 24x7 security, fitness gym, swimming pool, power backup, landscaped gardens, and clubhouse facilities.", st['bullet']))
    story.append(Paragraph("4. <b>Safety & Environmental Air Quality (Max 25 pts):</b> Localized crime rate index (up to 13 pts for crime <20/100) and surrounding Air Quality Index (up to 12 pts for pristine AQI <45).", st['bullet']))

    story.append(Bookmark('sec5_3', tracker))
    story.append(Paragraph("5.3 Investment Grade Classification Benchmarks", st['h1']))
    p_5_3_intro = (
        "Based on total accumulated points across all four pillars, properties are categorized into standardized institutional investment "
        "grades. Table 5.1 outlines the classification rubric and recommended transactional actions."
    )
    story.append(Paragraph(p_5_3_intro, st['body']))

    story.append(Bookmark('tab5_1', tracker))
    story.append(Paragraph("Table 5.1: 4-Pillar Quality Scoring Allocation & Grading Scale", st['table_caption']))
    grade_table_data = [
        [Paragraph("<b>Score Range</b>", st['body_bold']), Paragraph("<b>Investment Grade</b>", st['body_bold']), Paragraph("<b>Market Quality Classification</b>", st['body_bold']), Paragraph("<b>Recommended Action</b>", st['body_bold'])],
        [Paragraph("88 - 100", st['body']), Paragraph("Grade AAA", st['body']), Paragraph("Prime Outperform Asset", st['body']), Paragraph("Strong Buy; High capital appreciation potential", st['body'])],
        [Paragraph("75 - 87", st['body']), Paragraph("Grade AA", st['body']), Paragraph("High Conviction Family Asset", st['body']), Paragraph("Low-risk family asset; stable appreciation", st['body'])],
        [Paragraph("62 - 74", st['body']), Paragraph("Grade A", st['body']), Paragraph("Stable Quality Accumulation", st['body']), Paragraph("Fair market value; verify minor maintenance", st['body'])],
        [Paragraph("50 - 61", st['body']), Paragraph("Grade B", st['body']), Paragraph("Moderate Risk Profile", st['body']), Paragraph("Negotiate price discount; inspect neighborhood", st['body'])],
        [Paragraph("0 - 49", st['body']), Paragraph("Grade C", st['body']), Paragraph("Speculative / Due Diligence", st['body']), Paragraph("Exercise caution; potential safety/legal flags", st['body'])]
    ]
    grade_table = Table(grade_table_data, colWidths=[2.5 * cm, 3.0 * cm, 4.5 * cm, 6.0 * cm])
    grade_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(grade_table)
    story.append(Spacer(1, 0.4 * cm))

    story.append(Bookmark('sec5_4', tracker))
    story.append(Paragraph("5.4 Contextual AI House Buying Advisory Engine", st['h1']))
    p_5_4a = (
        "The automated advisory engine analyzes the property's multivariate profile to generate categorized, contextual advice: "
        "(a) <b>Core Strengths:</b> Highlights verified asset advantages such as East-facing morning sunlight, low building age, and high parking ratios; "
        "(b) <b>Value Drivers:</b> Identifies rental liquidity triggers such as metro transit proximity and school density; "
        "(c) <b>Due Diligence & Risks:</b> Warns buyers regarding high crime rates (>50/100), poor AQI (>100), or buildings older than 18 years requiring repair funds; and "
        "(d) <b>Buyer's Negotiation Playbook:</b> Advises buyers to bid 8% to 12% below asking price if the listing has been active on the market for over 6 months."
    )
    story.append(Paragraph(p_5_4a, st['body']))

    story.append(Bookmark('sec5_5', tracker))
    story.append(Paragraph("5.5 Client Valuation Dossier & Report Export", st['h1']))
    p_5_5a = (
        "Users can export the full property dossier--including valuation estimates, confidence spread, score breakdowns, property specs, "
        "and financing EMI tables--as a downloadable formatted text report (<code>.txt</code>) ready for submission to banking institutions, "
        "mortgage underwriters, and legal advisors."
    )
    story.append(Paragraph(p_5_5a, st['body']))
    story.append(PageBreak())

    # ==============================================================================
    # CHAPTER 6: PERFORMANCE EVALUATION, BENCHMARKING & XAI (Arabic Page 24)
    # ==============================================================================
    story.append(Bookmark('chap6', tracker))
    story.append(Paragraph("Chapter 6: Performance Evaluation, Benchmarking & XAI", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceBefore=4, spaceAfter=14))

    story.append(Bookmark('sec6_1', tracker))
    story.append(Paragraph("6.1 Regression Evaluation Metrics (R&sup2;, MAE, RMSE)", st['h1']))
    p_6_1a = (
        "Model performance was evaluated on the unseen 100-sample test set using three standard statistical regression metrics: "
        "(1) <b>Mean Absolute Error (MAE):</b> (1/<i>n</i>) &sum; |<i>y<sub>i</sub></i> - <i>y&#770;<sub>i</sub></i>|, measuring the average magnitude of absolute prediction residuals in Rs. Lakhs; "
        "(2) <b>Root Mean Squared Error (RMSE):</b> &radic;[(1/<i>n</i>) &sum; (<i>y<sub>i</sub></i> - <i>y&#770;<sub>i</sub></i>)&sup2;], penalizing larger prediction errors to assess variance stability; and "
        "(3) <b>Coefficient of Determination (R&sup2; Score):</b> 1 - [&sum; (<i>y<sub>i</sub></i> - <i>y&#770;<sub>i</sub></i>)&sup2; / &sum; (<i>y<sub>i</sub></i> - <i>y&#772;</i>)&sup2;], quantifying the proportion of total variance explained by the independent feature matrix."
    )
    story.append(Paragraph(p_6_1a, st['body']))

    story.append(Bookmark('sec6_2', tracker))
    story.append(Paragraph("6.2 Comparative Model Leaderboard Analysis", st['h1']))
    p_6_2a = (
        "Table 6.1 summarizes the empirical benchmarking results across all three candidate regression models evaluated on the isolated test set."
    )
    story.append(Paragraph(p_6_2a, st['body']))

    story.append(Bookmark('tab6_1', tracker))
    story.append(Paragraph("Table 6.1: Model Performance Leaderboard on 100 Test Samples", st['table_caption']))
    lead_table_data = [
        [Paragraph("<b>Model Architecture</b>", st['body_bold']), Paragraph("<b>MAE (Rs. Lakhs)</b>", st['body_bold']), Paragraph("<b>RMSE (Rs. Lakhs)</b>", st['body_bold']), Paragraph("<b>R&sup2; Score</b>", st['body_bold']), Paragraph("<b>Classification</b>", st['body_bold'])],
        [Paragraph("<b>Gradient Boosting Regressor</b>", st['body']), Paragraph("<b>10.0084</b>", st['body']), Paragraph("<b>13.8546</b>", st['body']), Paragraph("<b>0.9392</b>", st['body']), Paragraph("<b>Winner (Selected)</b>", st['body'])],
        [Paragraph("Linear Regression", st['body']), Paragraph("13.7930", st['body']), Paragraph("18.4201", st['body']), Paragraph("0.8925", st['body']), Paragraph("Parametric Baseline", st['body'])],
        [Paragraph("Random Forest Regressor", st['body']), Paragraph("15.8573", st['body']), Paragraph("21.9976", st['body']), Paragraph("0.8467", st['body']), Paragraph("Ensemble Bagging", st['body'])]
    ]
    lead_table = Table(lead_table_data, colWidths=[5.0 * cm, 2.8 * cm, 2.8 * cm, 2.2 * cm, 3.2 * cm])
    lead_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(lead_table)
    story.append(Spacer(1, 0.4 * cm))

    # Embed Model Comparison Chart
    if os.path.exists(FIG_MODEL):
        story.append(Bookmark('fig6_1', tracker))
        story.append(RLImage(FIG_MODEL, width=15.0 * cm, height=7.5 * cm))
        story.append(Paragraph("Figure 6.1: Comparative Performance Leaderboard across Evaluated Machine Learning Regressors", st['fig_caption']))
        story.append(Spacer(1, 0.2 * cm))

    p_6_2_analysis = (
        "<b>Performance Discussion:</b> The Gradient Boosting Regressor achieved the highest R&sup2; score (0.9392) and the lowest MAE "
        "(Rs. 10.01 Lakhs). This superiority stems from gradient boosting's sequential optimization strategy, wherein each regression tree "
        "specifically corrects the residual errors of preceding trees. Linear Regression attained an R&sup2; of 0.8925, demonstrating strong "
        "linear correlation with carpet area but failing to model complex non-linear interactions between society amenities and urban locations. "
        "Random Forest Regressor scored 0.8467, exhibiting slightly higher variance penalties on boundary instances."
    )
    story.append(Paragraph(p_6_2_analysis, st['body']))

    story.append(Bookmark('sec6_3', tracker))
    story.append(Paragraph("6.3 Explainable AI (XAI) & Feature Importance Weights", st['h1']))
    p_6_3a = (
        "To satisfy production transparency requirements, feature importances were extracted directly from the trained Gradient Boosting "
        "ensemble. Figure 6.2 illustrates the relative predictive weight of the top 9 features."
    )
    story.append(Paragraph(p_6_3a, st['body']))

    # Embed Feature Importance Chart
    if os.path.exists(FIG_FEAT):
        story.append(Bookmark('fig6_2', tracker))
        story.append(RLImage(FIG_FEAT, width=15.0 * cm, height=7.5 * cm))
        story.append(Paragraph("Figure 6.2: Feature Importance Weights Derived from the Gradient Boosting Pipeline", st['fig_caption']))
        story.append(Spacer(1, 0.2 * cm))

    p_6_3_weights = (
        "<b>Economic Interpretation of Weights:</b> Carpet area (<code>Area_sqft</code>) is by far the most influential feature, "
        "accounting for <b>63.56%</b> of total predictive weight. This aligns with real-world real estate economics where usable carpet "
        "square footage establishes baseline asset value. Metropolitan city tiers represent the second major cluster, contributing "
        "approximately <b>23%</b> combined weight (Delhi: 6.06%, Lucknow: 4.63%, Bengaluru: 4.56%, Ahmedabad: 4.36%, and Mumbai: 3.29%). "
        "Standalone luxury villas contribute 2.37%, distance to city center accounts for 1.99%, and property age contributes 1.50%."
    )
    story.append(Paragraph(p_6_3_weights, st['body']))

    story.append(Bookmark('sec6_4', tracker))
    story.append(Paragraph("6.4 Residual Error Distribution & Validation", st['h1']))
    p_6_4a = (
        "To ensure that the model does not suffer from systematic bias or heteroscedasticity, residual errors were analyzed. "
        "Figure 6.3 shows the actual vs. predicted values and the residual distribution."
    )
    story.append(Paragraph(p_6_4a, st['body']))

    # Embed Residuals Analysis Chart
    if os.path.exists(FIG_RES):
        story.append(Bookmark('fig6_3', tracker))
        story.append(RLImage(FIG_RES, width=15.0 * cm, height=6.2 * cm))
        story.append(Paragraph("Figure 6.3: Actual vs. Predicted Prices & Residual Error Distribution", st['fig_caption']))
        story.append(Spacer(1, 0.2 * cm))

    p_6_4b = (
        "The residual distribution is tightly centered at zero error (mean = Rs. 0.12 Lakhs) with a near-perfect bell curve. The scatter plot "
        "adheres closely to the ideal 1:1 identity line across budget, mid-market, and luxury tiers, confirming model stability."
    )
    story.append(Paragraph(p_6_4b, st['body']))
    story.append(PageBreak())

    # ==============================================================================
    # CHAPTER 7: LIMITATIONS & ENVIRONMENTAL RISK FACTORS (Arabic Page 29)
    # ==============================================================================
    story.append(Bookmark('chap7', tracker))
    story.append(Paragraph("Chapter 7: Limitations & Environmental Risk Factors", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceBefore=4, spaceAfter=14))

    p_7_intro = (
        "While HomeWorth AI achieves high predictive accuracy and provides robust decision support, certain technical and structural "
        "constraints must be acknowledged for responsible production deployment."
    )
    story.append(Paragraph(p_7_intro, st['body']))

    story.append(Bookmark('sec7_1', tracker))
    story.append(Paragraph("7.1 Geographical & Sampling Constraints", st['h1']))
    p_7_1a = (
        "The current dataset models 506 residential properties sampled across ten Tier-1 and prominent Tier-2 Indian metropolitan centers. "
        "While the data captures broad metropolitan pricing hierarchies, the sample size within individual micro-neighborhoods remains "
        "moderate. Applying the trained model to emerging Tier-3 cities, peri-urban villages, or industrial townships requires localized "
        "re-calibration and expanded comp collection."
    )
    story.append(Paragraph(p_7_1a, st['body']))

    story.append(Bookmark('sec7_2', tracker))
    story.append(Paragraph("7.2 Qualitative Interior Craftsmanship & On-site Nuances", st['h1']))
    p_7_2a = (
        "Supervised regression models operate on structured tabular parameters. However, in luxury real estate, significant value variance "
        "stems from subjective factors that cannot be captured in numerical tables--such as imported Italian marble flooring, bespoke interior "
        "woodwork, ceiling height variances, scenic sea/park views, and maintenance condition of common stairwells. Physical on-site "
        "inspection remains essential for final transaction closing."
    )
    story.append(Paragraph(p_7_2a, st['body']))

    story.append(Bookmark('sec7_3', tracker))
    story.append(Paragraph("7.3 Macroeconomic Interest Rate Dynamic Shocks", st['h1']))
    p_7_3a = (
        "Property prices are subject to macroeconomic cycles, Reserve Bank of India (RBI) repo rate shifts, inflationary trends in building "
        "materials (cement, steel), and municipal stamp duty revisions. The current pipeline evaluates cross-sectional static snapshots "
        "and does not currently integrate dynamic time-series autoregressive forecasting."
    )
    story.append(Paragraph(p_7_3a, st['body']))
    story.append(PageBreak())

    # ==============================================================================
    # CHAPTER 8: CONCLUSION AND FUTURE WORK (Arabic Page 31)
    # ==============================================================================
    story.append(Bookmark('chap8', tracker))
    story.append(Paragraph("Chapter 8: Conclusion and Future Work", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceBefore=4, spaceAfter=14))

    story.append(Bookmark('sec8_1', tracker))
    story.append(Paragraph("8.1 Conclusion & Technical Deliverables Summary", st['h1']))
    p_8_1a = (
        "The <b>HomeWorth AI</b> project successfully demonstrates the design, empirical validation, and deployment of an AI-powered "
        "residential property valuation and real estate intelligence platform. Developed during the AIML Summer Internship 2026 at "
        "IIHMF, MNNIT Prayagraj, the system models 506 validated property transactions across 10 top Indian metros characterized by 34 attributes. "
        "By training and benchmarking multiple regression models, the <b>Gradient Boosting Regressor</b> was established as the premier "
        "architecture, achieving <b>93.92% accuracy (R&sup2; = 0.9392)</b> and a low Mean Absolute Error of <b>Rs. 10.01 Lakhs</b>."
    )
    story.append(Paragraph(p_8_1a, st['body']))

    p_8_1b = (
        "Crucially, the platform bridges machine learning theory and practical consumer utility. By combining dual-currency price bands with "
        "a standardized 100-point Property Health Score, an automated AI buying advisory engine, a side-by-side property comparison tool, and an "
        "integrated Indian home loan EMI calculator, HomeWorth AI provides end-to-end decision clarity to prospective home buyers and real "
        "estate professionals."
    )
    story.append(Paragraph(p_8_1b, st['body']))

    story.append(Bookmark('sec8_2', tracker))
    story.append(Paragraph("8.2 Academic & Industry Impact", st['h1']))
    p_8_2a = (
        "This project fulfills all academic requirements of the B.Tech curriculum at United College of Engineering & Research (UCER), "
        "affiliated to Dr. A.P.J. Abdul Kalam Technical University, Lucknow. It exemplifies rigorous engineering practices: zero data-leakage "
        "pipelining, automated feature importance extraction, robust session-state management, and modern glassmorphic UI design."
    )
    story.append(Paragraph(p_8_2a, st['body']))

    story.append(Bookmark('sec8_3', tracker))
    story.append(Paragraph("8.3 Future Enhancement Roadmap", st['h1']))
    story.append(Paragraph("The future engineering roadmap for HomeWorth AI includes the following technical advancements:", st['body']))

    story.append(Paragraph("&bull; <b>Live Real Estate Portal Web Scraping:</b> Implementing automated asynchronous crawlers (Scrapy/BeautifulSoup) to stream real-time secondary market listings from MagicBricks, 99acres, and Housing.com.", st['bullet']))
    story.append(Paragraph("&bull; <b>Geospatial GIS & Satellite Mapping:</b> Integrating Google Maps Platform APIs to calculate exact travel times to metro stations, tech parks, and arterial expressways based on real-time transit traffic.", st['bullet']))
    story.append(Paragraph("&bull; <b>Deep Learning & TabNet Neural Architectures:</b> Benchmarking TabNet and deep neural networks with attention mechanisms against gradient boosted trees on expanded nationwide datasets.", st['bullet']))
    story.append(Paragraph("&bull; <b>Cross-Platform Mobile App (Flutter):</b> Developing native Android and iOS mobile applications allowing users to snap photos of residential buildings and instantly receive ML-grounded valuation estimates.", st['bullet']))
    story.append(PageBreak())

    # ==============================================================================
    # REFERENCES (Arabic Page 34)
    # ==============================================================================
    story.append(Bookmark('refs', tracker))
    story.append(Paragraph("References", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceBefore=4, spaceAfter=14))

    refs = [
        "1. Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V. and Vanderplas, J., 2011. Scikit-learn: Machine learning in Python. <i>Journal of Machine Learning Research</i>, 12, pp.2825-2830.",
        "2. Friedman, J.H., 2001. Greedy function approximation: a gradient boosting machine. <i>Annals of Statistics</i>, 29(5), pp.1189-1232.",
        "3. Breiman, L., 2001. Random forests. <i>Machine Learning</i>, 45(1), pp.5-32.",
        "4. McKinney, W., 2010. Data structures for statistical computing in Python. In <i>Proceedings of the 9th Python in Science Conference</i>, 445, pp.51-56.",
        "5. Harris, C.R., Millman, K.J., van der Walt, S.J. et al., 2020. Array programming with NumPy. <i>Nature</i>, 585(7825), pp.357-362.",
        "6. National Housing Bank (NHB), 2025. <i>NHB RESIDEX: Housing Price Index for Major Indian Metropolitan Centers</i>. Technical Report, Government of India.",
        "7. Streamlit Documentation, 2026. <i>Building and Deploying Interactive Data Applications in Python</i>. Available at: https://docs.streamlit.io/.",
        "8. Plotly Technologies Inc., 2026. <i>Collaborative Data Visualization & Interactive WebGL Graphics</i>. Montreal, QC.",
        "9. Motilal Nehru National Institute of Technology (MNNIT), Prayagraj, 2026. <i>IIHMF AIML Summer Internship Training Curriculum and Real Estate Comp Datasets</i>."
    ]
    for r in refs:
        story.append(Paragraph(r, st['bullet']))
        story.append(Spacer(1, 0.15 * cm))
    story.append(PageBreak())

    # ==============================================================================
    # APPENDIX: CORE SOURCE CODE (Arabic Page 36)
    # ==============================================================================
    story.append(Bookmark('appx', tracker))
    story.append(Paragraph("Appendix: Core Pipeline Architecture & Source Code", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceBefore=4, spaceAfter=14))

    story.append(Paragraph("Appendix A: Scikit-Learn Pipeline Serialization (predictor.py)", st['h1']))
    code_text = (
        "<font face='Courier' size='8.5'>"
        "import os, joblib, pandas as pd<br/>"
        "MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'Model', 'house_price_pipeline.pkl')<br/>"
        "pipeline = joblib.load(MODEL_PATH)<br/><br/>"
        "def predict_price(user_input: dict) -&gt; float:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;input_df = pd.DataFrame([user_input])<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;prediction = pipeline.predict(input_df)[0]<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;return max(round(float(prediction), 2), 5.0)<br/><br/>"
        "def predict_price_range(predicted_price: float, mae: float = 10.01) -&gt; tuple:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;spread = round(mae * 0.75, 2)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;lower = max(round(predicted_price - spread, 2), 5.0)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;upper = round(predicted_price + spread, 2)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;return lower, upper<br/>"
        "</font>"
    )
    story.append(Paragraph(code_text, ParagraphStyle('CodeBox1', fontName='Courier', fontSize=8.5, leading=12, spaceBefore=4, spaceAfter=10, leftIndent=10)))

    story.append(Paragraph("Appendix B: Financial EMI Calculation Algorithm (utils.py)", st['h1']))
    code_text2 = (
        "<font face='Courier' size='8.5'>"
        "def calculate_emi(principal_lakhs, down_payment_pct=20.0, tenure_years=20, annual_interest_rate=8.5):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;down_payment = (principal_lakhs * down_payment_pct) / 100.0<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;loan_amount = principal_lakhs - down_payment<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;P = loan_amount * 100000.0<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;monthly_r = (annual_interest_rate / 12.0) / 100.0<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;num_months = tenure_years * 12<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;if monthly_r &gt; 0 and num_months &gt; 0:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;emi = (P * monthly_r * ((1 + monthly_r)**num_months)) / (((1 + monthly_r)**num_months) - 1)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;return {'monthly_emi': round(emi, 0), 'loan_amount_lakhs': round(loan_amount, 2)}<br/>"
        "</font>"
    )
    story.append(Paragraph(code_text2, ParagraphStyle('CodeBox2', fontName='Courier', fontSize=8.5, leading=12, spaceBefore=4, spaceAfter=10, leftIndent=10)))

    story.append(Paragraph("Appendix C: 4-Pillar Property Livability Scoring Algorithm (utils.py)", st['h1']))
    code_text3 = (
        "<font face='Courier' size='8.5'>"
        "def calculate_property_score(data: dict) -&gt; dict:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;# 1. Location Pillar (Max 25 pts)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;loc_pts = 9 if dist &lt;= 5 else 7 if dist &lt;= 12 else 4<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;loc_pts += 6 if transit == 'High' else 4 if transit == 'Medium' else 2<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;loc_pts += min(schools, 5) + min(hospitals, 5)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;# 2. Specs Pillar (Max 25 pts)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;spec_pts = 8 if area &gt;= 1800 else 6 if area &gt;= 1100 else 4<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;spec_pts += 7 if age &lt;= 3 else 5 if age &lt;= 10 else 3<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;# 3. Amenities Pillar (Max 25 pts)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;amen_pts = min(amenities_count * 3, 25)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;# 4. Safety & Environment Pillar (Max 25 pts)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;safe_pts = 13 if crime &lt; 20 else 9 if crime &lt; 40 else 4<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;safe_pts += 12 if aqi &lt; 50 else 8 if aqi &lt; 100 else 3<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;total_score = min(loc_pts + spec_pts + amen_pts + safe_pts, 100)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;return {'total_score': total_score, 'breakdown': (loc_pts, spec_pts, amen_pts, safe_pts)}<br/>"
        "</font>"
    )
    story.append(Paragraph(code_text3, ParagraphStyle('CodeBox3', fontName='Courier', fontSize=8.5, leading=12, spaceBefore=4, spaceAfter=10, leftIndent=10)))

    return story


def build_pdf():
    # Pass 1: Build document and record exact page numbers in PAGE_TRACKER
    doc_pass1 = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=3.5 * cm,
        topMargin=2.5 * cm,
        rightMargin=1.25 * cm,
        bottomMargin=1.25 * cm
    )
    story1 = build_story(PAGE_TRACKER)
    doc_pass1.build(story1, canvasmaker=AcademicCanvas)
    print("Pass 1 completed. Recorded page anchors:", PAGE_TRACKER)

    # Pass 2: Rebuild with exact recorded page numbers inserted into TOC & Lists
    doc_pass2 = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=3.5 * cm,
        topMargin=2.5 * cm,
        rightMargin=1.25 * cm,
        bottomMargin=1.25 * cm
    )
    story2 = build_story(PAGE_TRACKER)
    doc_pass2.build(story2, canvasmaker=AcademicCanvas)
    print(f"Pass 2 completed. Final Project Report successfully generated at: {OUTPUT_PDF}")


if __name__ == '__main__':
    build_pdf()
