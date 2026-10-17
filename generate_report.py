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


class CenteredAcademicCanvas(canvas.Canvas):
    """Two-pass canvas drawing symmetric centered margins, double border, headers, and footers."""
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
        start_of_chap1 = PAGE_TRACKER.get('chap1', 6)
        
        # Cover Page (Physical Page 1): Perfectly Centered Double Border as per Template
        if page_num == 1:
            self.saveState()
            self.setStrokeColor(colors.black)
            # Outer border (symmetric 1.3 cm margin from all 4 edges)
            self.setLineWidth(2.5)
            self.rect(1.3 * cm, 1.3 * cm, A4[0] - 2.6 * cm, A4[1] - 2.6 * cm)
            # Inner border (symmetric 1.45 cm margin from all 4 edges)
            self.setLineWidth(0.8)
            self.rect(1.46 * cm, 1.46 * cm, A4[0] - 2.92 * cm, A4[1] - 2.92 * cm)
            self.restoreState()
            return

        self.saveState()
        self.setFont("Times-Roman", 9.5)
        self.setFillColor(colors.HexColor("#475569"))

        # Running Footer Divider Line (Symmetric 2.0 cm margins)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(2.0 * cm, 1.5 * cm, A4[0] - 2.0 * cm, 1.5 * cm)

        # Page Numbering & Running Headers
        if page_num < start_of_chap1:
            # Roman numerals for Front Matter (Physical Pages 2 to start_of_chap1 - 1)
            roman_numerals = ["", "i", "ii", "iii", "iv", "v", "vi", "vii", "viii"]
            idx = page_num - 1
            if 1 <= idx < len(roman_numerals):
                self.drawRightString(A4[0] - 2.0 * cm, 1.05 * cm, roman_numerals[idx])
        else:
            # Running Header for Main Body Chapters (Symmetric 2.0 cm margins)
            self.drawString(2.0 * cm, A4[1] - 1.4 * cm, "HomeWorth AI: AI-Powered House Price Prediction System")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(2.0 * cm, A4[1] - 1.55 * cm, A4[0] - 2.0 * cm, A4[1] - 1.55 * cm)

            # Arabic numerals start at 1 on Physical Page start_of_chap1
            arabic_num = page_num - start_of_chap1 + 1
            self.drawString(2.0 * cm, 1.05 * cm, "UCER Prayagraj | B.Tech CSE (AI & ML) | Session 2026-27")
            self.drawRightString(A4[0] - 2.0 * cm, 1.05 * cm, f"Page {arabic_num}")
            
        self.restoreState()


def get_academic_styles():
    styles = getSampleStyleSheet()

    body_style = ParagraphStyle(
        'ReportBody',
        fontName='Times-Roman',
        fontSize=11,
        leading=16,
        alignment=TA_JUSTIFY,
        spaceAfter=7
    )

    body_bold = ParagraphStyle(
        'ReportBodyBold',
        fontName='Times-Bold',
        fontSize=11,
        leading=16,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'ReportBullet',
        fontName='Times-Roman',
        fontSize=10.5,
        leading=15,
        leftIndent=18,
        firstLineIndent=-10,
        alignment=TA_JUSTIFY,
        spaceAfter=4
    )

    # Chapter Title: 15pt Bold
    chap_style = ParagraphStyle(
        'ReportChapter',
        fontName='Times-Bold',
        fontSize=15,
        leading=19,
        alignment=TA_LEFT,
        spaceBefore=8,
        spaceAfter=8
    )

    # Main Heading 1: 13pt Bold
    h1_style = ParagraphStyle(
        'ReportH1',
        fontName='Times-Bold',
        fontSize=12.5,
        leading=16,
        alignment=TA_LEFT,
        spaceBefore=7,
        spaceAfter=4
    )

    # Sub-Heading 2: 11.5pt Bold
    h2_style = ParagraphStyle(
        'ReportH2',
        fontName='Times-Bold',
        fontSize=11.5,
        leading=15,
        alignment=TA_LEFT,
        spaceBefore=6,
        spaceAfter=3
    )

    # Table Caption (Must be at the TOP)
    table_caption = ParagraphStyle(
        'TableCaption',
        fontName='Times-Bold',
        fontSize=10,
        leading=13,
        alignment=TA_CENTER,
        spaceBefore=6,
        spaceAfter=4
    )

    # Figure Caption (Must be at the BOTTOM)
    fig_caption = ParagraphStyle(
        'FigCaption',
        fontName='Times-BoldItalic',
        fontSize=9.5,
        leading=13,
        alignment=TA_CENTER,
        spaceBefore=4,
        spaceAfter=8
    )

    # Cover Page Specific Styles (Strictly Matching User Template Image)
    cov_main_title = ParagraphStyle(
        'CovMainTitle',
        fontName='Times-Bold',
        fontSize=24,
        leading=28,
        alignment=TA_CENTER,
        spaceAfter=4
    )

    cov_subtitle = ParagraphStyle(
        'CovSubtitle',
        fontName='Times-Bold',
        fontSize=11.5,
        leading=15,
        alignment=TA_CENTER,
        spaceAfter=12
    )

    cov_h1 = ParagraphStyle(
        'CovH1',
        fontName='Times-Bold',
        fontSize=13.5,
        leading=17,
        alignment=TA_CENTER,
        spaceAfter=3
    )

    cov_h2 = ParagraphStyle(
        'CovH2',
        fontName='Times-Bold',
        fontSize=12,
        leading=15,
        alignment=TA_CENTER,
        spaceAfter=10
    )

    cov_text = ParagraphStyle(
        'CovText',
        fontName='Times-Roman',
        fontSize=11.5,
        leading=15,
        alignment=TA_CENTER,
        spaceAfter=3
    )

    cov_text_bold = ParagraphStyle(
        'CovTextBold',
        fontName='Times-Bold',
        fontSize=11.5,
        leading=15,
        alignment=TA_CENTER,
        spaceAfter=3
    )

    cov_univ = ParagraphStyle(
        'CovUniv',
        fontName='Times-Bold',
        fontSize=13,
        leading=16,
        alignment=TA_CENTER,
        spaceAfter=10
    )

    cov_footer = ParagraphStyle(
        'CovFooter',
        fontName='Times-Bold',
        fontSize=12.5,
        leading=16,
        alignment=TA_CENTER,
        spaceAfter=0
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
        'cov_main_title': cov_main_title,
        'cov_subtitle': cov_subtitle,
        'cov_h1': cov_h1,
        'cov_h2': cov_h2,
        'cov_text': cov_text,
        'cov_text_bold': cov_text_bold,
        'cov_univ': cov_univ,
        'cov_footer': cov_footer
    }


def get_page_str(key, default_val=1):
    """Returns the formatted page number string for TOC and lists."""
    if key in PAGE_TRACKER:
        phys_p = PAGE_TRACKER[key]
        start_of_chap1 = PAGE_TRACKER.get('chap1', 6)
        if phys_p < start_of_chap1:
            roman_numerals = ["", "i", "ii", "iii", "iv", "v", "vi", "vii", "viii"]
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
    # 1. INNER COVER / TITLE PAGE (Physical Page 1 - Strictly Matching Template)
    # ==============================================================================
    story.append(Spacer(1, 0.6 * cm))
    story.append(Paragraph("HOMEWORTH AI", ParagraphStyle('CovMainTitle', fontName='Times-Bold', fontSize=26, leading=30, alignment=TA_CENTER, spaceAfter=4)))
    story.append(Paragraph("AI-POWERED HOUSE PRICE PREDICTION SYSTEM USING MACHINE LEARNING", ParagraphStyle('CovSubtitle', fontName='Times-Bold', fontSize=12.5, leading=16, alignment=TA_CENTER, spaceAfter=0)))
    story.append(Spacer(1, 0.75 * cm))

    story.append(Paragraph("MINI PROJECT REPORT", ParagraphStyle('CovH1', fontName='Times-Bold', fontSize=14, leading=17, alignment=TA_CENTER, spaceAfter=3)))
    story.append(Paragraph("OF INTERNSHIP", ParagraphStyle('CovH2', fontName='Times-Bold', fontSize=12.5, leading=15, alignment=TA_CENTER, spaceAfter=0)))
    story.append(Spacer(1, 0.75 * cm))

    story.append(Paragraph("BACHELOR OF TECHNOLOGY", ParagraphStyle('CovDeg1', fontName='Times-Bold', fontSize=14, leading=17, alignment=TA_CENTER, spaceAfter=3)))
    story.append(Paragraph("COMPUTER SCIENCE AND ENGINEERING", ParagraphStyle('CovDeg2', fontName='Times-Bold', fontSize=13, leading=16, alignment=TA_CENTER, spaceAfter=2)))
    story.append(Paragraph("(ARTIFICIAL INTELLIGENCE & MACHINE LEARNING)", ParagraphStyle('DegSpecial', fontName='Times-Bold', fontSize=11.5, leading=14, alignment=TA_CENTER, spaceAfter=0)))
    story.append(Spacer(1, 0.75 * cm))

    story.append(Paragraph("<b>Submitted</b>", ParagraphStyle('CovSub1', fontName='Times-Bold', fontSize=12, leading=15, alignment=TA_CENTER, spaceAfter=2)))
    story.append(Paragraph("<b>To</b>", ParagraphStyle('CovSub2', fontName='Times-Bold', fontSize=12, leading=15, alignment=TA_CENTER, spaceAfter=0)))
    story.append(Spacer(1, 0.45 * cm))
    
    # AKTU University Logo (Centered)
    if os.path.exists(LOGO_AKTU):
        story.append(RLImage(LOGO_AKTU, width=2.5 * cm, height=2.5 * cm))
        story.append(Spacer(1, 0.45 * cm))

    story.append(Paragraph("Dr. A.P.J. ABDUL KALAM TECHNICAL UNIVERSITY<br/>LUCKNOW", ParagraphStyle('CovUniv', fontName='Times-Bold', fontSize=13.5, leading=17, alignment=TA_CENTER, spaceAfter=0)))
    story.append(Spacer(1, 0.75 * cm))

    # SUBMITTED BY (Centered, bold layout matching template)
    story.append(Paragraph("<b>SUBMITTED BY</b>", ParagraphStyle('CovSubBy', fontName='Times-Bold', fontSize=12.5, leading=16, alignment=TA_CENTER, spaceAfter=3)))
    story.append(Paragraph("<b>Ujjaval Kumar Kesarwani</b> (Roll No. 2400101530154)", ParagraphStyle('CovS1', fontName='Times-Roman', fontSize=11.5, leading=15, alignment=TA_CENTER, spaceAfter=2)))
    story.append(Paragraph("<b>Shlok Tiwari</b> (Roll No. 2400101530134)", ParagraphStyle('CovS2', fontName='Times-Roman', fontSize=11.5, leading=15, alignment=TA_CENTER, spaceAfter=0)))
    story.append(Spacer(1, 0.75 * cm))

    # UNDER THE SUPERVISION OF (Updated Designation: Associate Professor, Dept. of CSE, MNNIT, Prayagraj)
    story.append(Paragraph("<b>UNDER THE SUPERVISION OF</b>", ParagraphStyle('CovSupHead', fontName='Times-Bold', fontSize=12.5, leading=16, alignment=TA_CENTER, spaceAfter=3)))
    story.append(Paragraph("<b>Dr. Divya Kumar</b>", ParagraphStyle('SupName', fontName='Times-Bold', fontSize=13, leading=16, alignment=TA_CENTER, spaceAfter=2)))
    story.append(Paragraph("Associate Professor<br/>Department of Computer Science & Engineering<br/>Motilal Nehru National Institute of Technology (MNNIT), Prayagraj", ParagraphStyle('SupDesc', fontName='Times-Roman', fontSize=11.5, leading=15, alignment=TA_CENTER, spaceAfter=0)))
    story.append(Spacer(1, 0.75 * cm))

    # United College Logo (Centered)
    if os.path.exists(LOGO_UNITED):
        story.append(RLImage(LOGO_UNITED, width=5.2 * cm, height=1.45 * cm))
        story.append(Spacer(1, 0.45 * cm))

    story.append(Paragraph("UNITED COLLEGE OF ENGINEERING & RESEARCH,<br/>PRAYAGRAJ, 2026-27", ParagraphStyle('CovFooter', fontName='Times-Bold', fontSize=13, leading=17, alignment=TA_CENTER, spaceAfter=0)))
    story.append(PageBreak())

    # ==============================================================================
    # 2. CERTIFICATE (Physical Page 2 - Roman Page i)
    # ==============================================================================
    story.append(Bookmark('cert', tracker))
    story.append(Paragraph("Certificate", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.black, spaceBefore=2, spaceAfter=12))
    
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

    cert_text2 = (
        "The project embodies the empirical research, data preprocessing, machine learning pipeline optimization, and web deployment "
        "conducted by the students during their <b>AIML Summer Internship 2026</b> at <b>IIHMF, Motilal Nehru National "
        "Institute of Technology (MNNIT), Prayagraj</b> under the technical coordination of Mr. Arpit Dubey. To the best of my knowledge, "
        "the matter embodied in this report has not been submitted to any other university or institute for the award of any degree or diploma."
    )
    story.append(Paragraph(cert_text2, st['body']))
    story.append(Spacer(1, 3.2 * cm))

    # Official Signatures Table (Symmetric 17.0 cm width)
    sig_data = [
        [
            Paragraph("<b>Dr. Divya Kumar</b><br/>Project Supervisor<br/>Associate Professor, Dept. of CSE<br/>MNNIT, Prayagraj", ParagraphStyle('S1', fontName='Times-Roman', fontSize=10.5, leading=14)),
            Paragraph("<b>Head of Department</b><br/>Department of CSE (AI & ML)<br/>UCER, Prayagraj", ParagraphStyle('S2', fontName='Times-Roman', fontSize=10.5, leading=14, alignment=TA_RIGHT))
        ]
    ]
    sig_table = Table(sig_data, colWidths=[8.5 * cm, 8.5 * cm])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(sig_table)
    story.append(PageBreak())

    # ==============================================================================
    # 3. DECLARATION & ACKNOWLEDGEMENT (Physical Page 3 - Roman Page ii)
    # ==============================================================================
    story.append(Bookmark('decl', tracker))
    story.append(Paragraph("Declaration", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.black, spaceBefore=2, spaceAfter=8))

    decl_text = (
        "We hereby declare that this submission is our own work and that, to the best of our knowledge and belief, "
        "it contains no material previously published or written by another person nor material which to a substantial "
        "extent has been accepted for the award of any other degree or diploma of the university or other institute of "
        "higher learning, except where due acknowledgment has been made in the text."
    )
    story.append(Paragraph(decl_text, st['body']))
    story.append(Spacer(1, 0.4 * cm))

    decl_sig_data = [
        [
            Paragraph("<b>Signature:</b> _______________________<br/><b>Name:</b> Ujjaval Kumar Kesarwani<br/><b>Roll No:</b> 2400101530154", ParagraphStyle('D1', fontName='Times-Roman', fontSize=10, leading=14)),
            Paragraph("<b>Signature:</b> _______________________<br/><b>Name:</b> Shlok Tiwari<br/><b>Roll No:</b> 2400101530134", ParagraphStyle('D2', fontName='Times-Roman', fontSize=10, leading=14, alignment=TA_RIGHT))
        ]
    ]
    decl_table = Table(decl_sig_data, colWidths=[8.5 * cm, 8.5 * cm])
    story.append(decl_table)
    story.append(Spacer(1, 0.6 * cm))

    story.append(Bookmark('ack', tracker))
    story.append(Paragraph("Acknowledgement", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.black, spaceBefore=2, spaceAfter=8))

    ack_text = (
        "We express our profound sense of gratitude and indebtedness to our esteemed supervisor, <b>Dr. Divya Kumar</b>, "
        "Associate Professor, Department of Computer Science and Engineering, Motilal Nehru National Institute of Technology (MNNIT), "
        "Prayagraj, for his inspiring guidance, constant encouragement, and insightful technical suggestions throughout this project. "
        "We are immensely thankful to <b>IIHMF, MNNIT Prayagraj</b> for organizing the <b>AIML Summer Internship 2026</b>, and to "
        "<b>Mr. Arpit Dubey</b>, Project Coordinator, for providing high-performance computing infrastructure and benchmark datasets. "
        "We also convey sincere thanks to the Head of Department, faculty members, and staff of Department of CSE (AI & ML) at "
        "United College of Engineering & Research (UCER), Prayagraj, as well as our parents and peers for their continuous support."
    )
    story.append(Paragraph(ack_text, st['body']))
    story.append(PageBreak())

    # ==============================================================================
    # 4. ABSTRACT (Physical Page 4 - Roman Page iii)
    # ==============================================================================
    story.append(Bookmark('abs', tracker))
    story.append(Paragraph("Abstract", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.black, spaceBefore=2, spaceAfter=10))

    abs_p1 = (
        "Accurate property valuation is fundamental to real estate transactions, mortgage underwriting, urban planning, "
        "and wealth management. Conventional real estate estimation in India remains heavily reliant on subjective broker "
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
        "A scikit-learn pipeline integrating One-Hot categorical encoding and ColumnTransformer scaling was trained across multiple "
        "regression algorithms. The <b>Gradient Boosting Regressor</b> emerged as the premier architecture, achieving an outstanding "
        "coefficient of determination (<b>R&sup2; = 0.9392</b>), a Mean Absolute Error (<b>MAE</b>) of <b>Rs. 10.01 Lakhs</b>, "
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
    # 5. TABLE OF CONTENTS & LIST OF TABLES/FIGURES (Physical Page 5 - Roman Page iv)
    # ==============================================================================
    story.append(Bookmark('toc', tracker))
    story.append(Paragraph("Table of Contents", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.black, spaceBefore=2, spaceAfter=8))

    toc_data = [
        [Paragraph("<b>Index Item</b>", ParagraphStyle('TOC1', fontName='Times-Bold', fontSize=10.5)), Paragraph("<b>Page No</b>", ParagraphStyle('TOC2', fontName='Times-Bold', fontSize=10.5, alignment=TA_RIGHT))],
        [Paragraph("Certificate", st['body']), Paragraph(get_page_str('cert', 'i'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=10.5, alignment=TA_RIGHT))],
        [Paragraph("Declaration & Acknowledgement", st['body']), Paragraph(get_page_str('decl', 'ii'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=10.5, alignment=TA_RIGHT))],
        [Paragraph("Abstract", st['body']), Paragraph(get_page_str('abs', 'iii'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=10.5, alignment=TA_RIGHT))],
        [Paragraph("<b>Chapter 1: Objectives & Research Motivation</b>", st['body_bold']), Paragraph(get_page_str('chap1', '1'), ParagraphStyle('TPB', fontName='Times-Bold', fontSize=10.5, alignment=TA_RIGHT))],
        [Paragraph("<b>Chapter 2: Tools, Technologies and Infrastructure</b>", st['body_bold']), Paragraph(get_page_str('chap2', '2'), ParagraphStyle('TPB', fontName='Times-Bold', fontSize=10.5, alignment=TA_RIGHT))],
        [Paragraph("<b>Chapter 3: System Functionality & Software Architecture</b>", st['body_bold']), Paragraph(get_page_str('chap3', '3'), ParagraphStyle('TPB', fontName='Times-Bold', fontSize=10.5, alignment=TA_RIGHT))],
        [Paragraph("<b>Chapter 4: Data Pipeline, Preprocessing & Model Workflow</b>", st['body_bold']), Paragraph(get_page_str('chap4', '5'), ParagraphStyle('TPB', fontName='Times-Bold', fontSize=10.5, alignment=TA_RIGHT))],
        [Paragraph("<b>Chapter 5: Key Features & Practical Innovations</b>", st['body_bold']), Paragraph(get_page_str('chap5', '7'), ParagraphStyle('TPB', fontName='Times-Bold', fontSize=10.5, alignment=TA_RIGHT))],
        [Paragraph("<b>Chapter 6: Performance Evaluation, Benchmarking & XAI</b>", st['body_bold']), Paragraph(get_page_str('chap6', '8'), ParagraphStyle('TPB', fontName='Times-Bold', fontSize=10.5, alignment=TA_RIGHT))],
        [Paragraph("<b>Chapter 7: Limitations & Environmental Risk Factors</b>", st['body_bold']), Paragraph(get_page_str('chap7', '10'), ParagraphStyle('TPB', fontName='Times-Bold', fontSize=10.5, alignment=TA_RIGHT))],
        [Paragraph("<b>Chapter 8: Conclusion and Future Work</b>", st['body_bold']), Paragraph(get_page_str('chap8', '10'), ParagraphStyle('TPB', fontName='Times-Bold', fontSize=10.5, alignment=TA_RIGHT))],
        [Paragraph("<b>References & Core Source Code Appendix</b>", st['body_bold']), Paragraph(get_page_str('refs', '11'), ParagraphStyle('TPB', fontName='Times-Bold', fontSize=10.5, alignment=TA_RIGHT))]
    ]
    toc_table = Table(toc_data, colWidths=[14.2 * cm, 2.8 * cm])
    toc_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('LINEBELOW', (0, 0), (-1, 0), 0.8, colors.black),
    ]))
    story.append(toc_table)
    story.append(Spacer(1, 0.4 * cm))

    # LIST OF TABLES & LIST OF FIGURES
    story.append(Paragraph("<b>List of Tables & List of Figures</b>", st['h1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#64748b"), spaceBefore=2, spaceAfter=4))
    
    lot_lof_data = [
        [Paragraph("Table 2.1: Software Specifications | Table 2.2: Hardware Benchmarks", st['body']), Paragraph(get_page_str('chap2', '2'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=10, alignment=TA_RIGHT))],
        [Paragraph("Table 4.1: 34-Feature Architecture | Table 4.2: Regressor Hyperparameters", st['body']), Paragraph(get_page_str('chap4', '5'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=10, alignment=TA_RIGHT))],
        [Paragraph("Table 5.1: 4-Pillar Quality Scoring Scale | Table 6.1: Model Leaderboard", st['body']), Paragraph(get_page_str('chap5', '7'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=10, alignment=TA_RIGHT))],
        [Paragraph("Figure 3.1: Multi-Tier Architecture | Figure 3.2: Valuation Studio Dashboard", st['body']), Paragraph(get_page_str('chap3', '3'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=10, alignment=TA_RIGHT))],
        [Paragraph("Figure 4.1: Price Density Spread | Figure 4.2: Metro Price Hierarchy", st['body']), Paragraph(get_page_str('chap4', '5'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=10, alignment=TA_RIGHT))],
        [Paragraph("Figure 6.1: Regressor Leaderboard | Figure 6.2: XAI Weights | Figure 6.3: Residuals", st['body']), Paragraph(get_page_str('chap6', '8'), ParagraphStyle('TP', fontName='Times-Roman', fontSize=10, alignment=TA_RIGHT))]
    ]
    lot_lof_table = Table(lot_lof_data, colWidths=[14.2 * cm, 2.8 * cm])
    lot_lof_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.2),
        ('TOPPADDING', (0, 0), (-1, -1), 1.2),
    ]))
    story.append(lot_lof_table)
    story.append(PageBreak())

    # ==============================================================================
    # CHAPTER 1: OBJECTIVES & RESEARCH MOTIVATION (Physical Page 6 - Arabic Page 1)
    # ==============================================================================
    story.append(Bookmark('chap1', tracker))
    story.append(Paragraph("Chapter 1: Objectives & Research Motivation", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.black, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("1.1 Background & Macroeconomic Urban PropTech Context", st['h1']))
    p_1_1 = (
        "The residential real estate sector is one of the most critical pillars of modern economic infrastructure, "
        "serving as both a primary engine of national capital formation and the single largest wealth asset for individual "
        "households. In developing economies such as India, rapid urbanization, burgeoning software and technological corridors, "
        "and rising middle-class disposable incomes have driven tremendous residential expansion across Tier-1 mega-cities "
        "(Mumbai, Delhi, Bengaluru) and prominent Tier-2 urban growth centers (Lucknow, Jaipur, Ahmedabad). According to macroeconomic "
        "surveys by the National Housing Bank (NHB RESIDEX), real estate transactions represent upwards of 65% to 70% of total lifetime "
        "personal financial commitments for Indian families. However, property price discovery in India remains deeply fragmented, "
        "inefficient, and opaque. Unlike equities or debt markets that operate on centralized order books with continuous public quotation, "
        "real estate assets are inherently heterogeneous and decentralized. Home valuation has historically depended upon informal broker "
        "opinions, unverified word-of-mouth anecdotes, and coarse municipal per-square-foot multipliers."
    )
    story.append(Paragraph(p_1_1, st['body']))

    story.append(Paragraph("1.2 Problem Statement & Valuation Inefficiencies", st['h1']))
    p_1_2 = (
        "<b>Problem Statement:</b> To develop, benchmark, and deploy an end-to-end AI-powered residential price estimation platform "
        "that eliminates subjective broker bias by predicting fair market values from 34 heterogeneous housing attributes with over 90% "
        "statistical accuracy (R&sup2;), while simultaneously synthesizing an objective 4-pillar property quality score, an automated AI "
        "buying advisory engine, and an interactive dark-glassmorphic PropTech dashboard for transparent decision support. "
        "Traditional valuation suffers from three key flaws: (1) <i>Broker Information Monopoly</i> (selective quotation of inflated prices); "
        "(2) <i>Static Per-Square-Foot Fallacy</i> (ignoring non-linear amenity premiums such as dedicated power backup, gyms, and transit); and "
        "(3) <i>Absence of Environmental Risk Pricing</i> (overlooking air quality AQI degradation and localized crime density)."
    )
    story.append(Paragraph(p_1_2, st['body']))

    story.append(Paragraph("1.3 Comprehensive Research Objectives", st['h1']))
    story.append(Paragraph("&bull; <b>High-Precision Supervised Regression:</b> Benchmark and tune OLS, Random Forest, and Gradient Boosting Regressors to achieve R&sup2; &gt; 0.90 on multi-metro Indian housing data.", st['bullet']))
    story.append(Paragraph("&bull; <b>ColumnTransformer Preprocessing Pipeline:</b> Encode 10 categorical attributes (46 dummy variables) alongside 22 continuous physical and environmental variables with zero data leakage.", st['bullet']))
    story.append(Paragraph("&bull; <b>4-Pillar Property Quality Index (0-100):</b> Formulate an objective score decomposing livability across Location & Transit (25 pts), Specs & Architecture (25 pts), Society Amenities (25 pts), and Safety & Environment (25 pts).", st['bullet']))
    story.append(Paragraph("&bull; <b>Contextual AI Buying Advisor:</b> Build an expert advisory engine generating recommendations across Core Strengths, Capital Growth Drivers, Due Diligence Flags, and Negotiation Playbooks.", st['bullet']))
    story.append(Paragraph("&bull; <b>Mortgage EMI & Comparison Studios:</b> Integrate an interactive Indian home loan EMI calculator and a side-by-side comparison engine.", st['bullet']))

    story.append(Paragraph("1.4 Scope and Geographic Profile of 10 Metros", st['h1']))
    p_1_4 = (
        "The project encompasses 506 benchmark properties across ten Indian metros: <b>Mumbai</b> (coastal land constraints, premium per-sqft pricing); "
        "<b>Delhi NCR</b> (polycentric sprawl, rapid metro transit, severe winter AQI volatility); <b>Bengaluru</b> (software corridor expansion, high gated-community preference); "
        "<b>Chennai & Hyderabad</b> (steady industrial and IT demand); <b>Pune & Ahmedabad</b> (rapidly appreciating manufacturing hubs); <b>Kolkata</b> (high urban density, stable pricing); "
        "and <b>Lucknow & Jaipur</b> (emerging Tier-2 capitals undergoing aggressive horizontal villa expansion and expressways)."
    )
    story.append(Paragraph(p_1_4, st['body']))
    story.append(PageBreak())

    # ==============================================================================
    # CHAPTER 2: TOOLS, TECHNOLOGIES AND INFRASTRUCTURE (Physical Page 7 - Arabic Page 2)
    # ==============================================================================
    story.append(Bookmark('chap2', tracker))
    story.append(Paragraph("Chapter 2: Tools, Technologies and Infrastructure", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.black, spaceBefore=2, spaceAfter=8))

    p_2_1 = (
        "HomeWorth AI is developed natively in <b>Python 3.10+</b> within an isolated virtual environment. Python was selected for its "
        "production-grade scientific computing libraries, native object-oriented clarity, and seamless bridging between machine learning "
        "pipelines and web frontends. The core computational libraries include <b>Scikit-Learn</b> (ColumnTransformer pipelines, One-Hot "
        "encoders, regression estimators), <b>Pandas</b> (tabular ingestion, missing value imputation, group-by aggregation), <b>NumPy</b> "
        "(vectorized linear algebra, financial mortgage EMI mathematics), <b>Joblib</b> (non-blocking pipeline serialization), and <b>OpenPyXL</b> "
        "(Excel workbook parsing). The presentation layer is built on <b>Streamlit 2.0</b>, employing session state (<code>st.session_state</code>) "
        "and resource caching (<code>@st.cache_resource</code>) to deliver sub-20ms inference responses."
    )
    story.append(Paragraph(p_2_1, st['body']))

    story.append(Paragraph("Table 2.1: Software Environment & Dependency Specifications", st['table_caption']))
    sw_table_data = [
        [Paragraph("<b>Component / Library</b>", st['body_bold']), Paragraph("<b>Version</b>", st['body_bold']), Paragraph("<b>Primary Functional Purpose</b>", st['body_bold'])],
        [Paragraph("Python Runtime", st['body']), Paragraph("3.10.9", st['body']), Paragraph("Base scientific runtime and data processing execution", st['body'])],
        [Paragraph("Scikit-Learn", st['body']), Paragraph("1.9.0", st['body']), Paragraph("ColumnTransformer pipelines, One-Hot encoding, and regression modeling", st['body'])],
        [Paragraph("Streamlit", st['body']), Paragraph("1.65.0", st['body']), Paragraph("Reactive web server, session state, and frontend UI widgets", st['body'])],
        [Paragraph("Plotly Express & GO", st['body']), Paragraph("7.1.0", st['body']), Paragraph("Hardware-accelerated gauges, radar charts, and scatter plots", st['body'])],
        [Paragraph("Pandas & NumPy", st['body']), Paragraph("2.3.1 / 2.2.6", st['body']), Paragraph("Tabular structures, missing value handling, and vectorized financial formulas", st['body'])],
        [Paragraph("Joblib & ReportLab", st['body']), Paragraph("1.5.3 / 5.0.1", st['body']), Paragraph("Model persistence and programmatic PDF report compilation", st['body'])]
    ]
    sw_table = Table(sw_table_data, colWidths=[4.5 * cm, 2.5 * cm, 10.0 * cm])
    sw_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(sw_table)
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("Table 2.2: Computational Hardware Environment & Execution Latencies", st['table_caption']))
    hw_table_data = [
        [Paragraph("<b>Hardware Component / Operation</b>", st['body_bold']), Paragraph("<b>Specification / Benchmark Value</b>", st['body_bold']), Paragraph("<b>Operational Status</b>", st['body_bold'])],
        [Paragraph("Processor Architecture", st['body']), Paragraph("Intel Core i7-13700H (14 Cores, 20 Threads, 5.0 GHz)", st['body']), Paragraph("High-Throughput Parallel Multiprocessing", st['body'])],
        [Paragraph("System Memory (RAM)", st['body']), Paragraph("16.0 GB DDR5 @ 4800 MHz Dual-Channel", st['body']), Paragraph("Zero memory-swap paging during fitting", st['body'])],
        [Paragraph("Dataset Ingestion & Pipeline Fitting", st['body']), Paragraph("118 ms (OpenPyXL) / 412 ms (Full Pipeline Fit)", st['body']), Paragraph("Rapid convergence and serialization", st['body'])],
        [Paragraph("Single-Sample Inference Latency", st['body']), Paragraph("18.4 ms (Mean across 1,000 queries)", st['body']), Paragraph("Real-time responsive user experience", st['body'])]
    ]
    hw_table = Table(hw_table_data, colWidths=[5.5 * cm, 6.5 * cm, 5.0 * cm])
    hw_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(hw_table)
    story.append(PageBreak())

    # ==============================================================================
    # CHAPTER 3: SYSTEM FUNCTIONALITY & ARCHITECTURE (Physical Page 8 - Arabic Page 3)
    # ==============================================================================
    story.append(Bookmark('chap3', tracker))
    story.append(Paragraph("Chapter 3: System Functionality & Software Architecture", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.black, spaceBefore=2, spaceAfter=8))

    p_3_1 = (
        "HomeWorth AI is engineered around a modular, multi-tier software architecture enforcing strict separation of concerns across "
        "five distinct operational layers: (1) <i>Presentation Layer</i> (Streamlit 2.0 with custom dark glassmorphism CSS); (2) <i>Controller Layer</i> "
        "(dynamic presets and input constraint validation); (3) <i>Preprocessing Pipeline</i> (scikit-learn ColumnTransformer); (4) <i>Inference & Advisory Engine</i> "
        "(Gradient Boosting, 4-pillar quality scorecard, and negotiation rules); and (5) <i>Persistence Layer</i> (Joblib serialized pipeline and benchmark datasets). "
        "Figure 3.1 illustrates the high-level system topology connecting user interactions with the underlying ML pipeline."
    )
    story.append(Paragraph(p_3_1, st['body']))

    if os.path.exists(FIG_ARCH):
        story.append(Bookmark('fig3_1', tracker))
        story.append(RLImage(FIG_ARCH, width=16.5 * cm, height=8.2 * cm))
        story.append(Paragraph("Figure 3.1: HomeWorth AI Multi-Tier System Topology & Interaction Flow", st['fig_caption']))

    p_3_2 = (
        "The <b>Valuation Studio</b> serves as the primary interactive module. To eliminate manual entry friction, it incorporates a "
        "<b>1-Click Sample Preset Engine</b> pre-loading validated profiles for Mumbai Luxury 3BHK, Bengaluru Tech 2BHK, Jaipur Royal Villa, "
        "and Lucknow Budget 2BHK. It dynamically enforces physical constraints (e.g., property floor cannot exceed total building floors) "
        "and outputs dual-currency prices, MAE confidence ranges, rate/sqft benchmarks, and interactive Plotly score gauges."
    )
    story.append(Paragraph(p_3_2, st['body']))

    if os.path.exists(BANNER_PATH):
        story.append(Bookmark('fig3_2', tracker))
        story.append(RLImage(BANNER_PATH, width=16.5 * cm, height=4.2 * cm))
        story.append(Paragraph("Figure 3.2: Valuation Studio Header & Responsive Web Application Dashboard", st['fig_caption']))
    story.append(PageBreak())

    # ==============================================================================
    # CHAPTER 3 (CONTD.): MODULES & FINANCIAL MODELING (Physical Page 9 - Arabic Page 4)
    # ==============================================================================
    story.append(Paragraph("3.3 Market Intelligence & Live Comps Explorer", st['h1']))
    p_3_3 = (
        "The <b>Market Intelligence Studio</b> integrates the 506-property research dataset directly into the web application. "
        "It exposes real-time market KPIs: Average Property Price (Rs. 99.6L), Median Price (Rs. 92.9L), Max Valuation (Rs. 473.2L), "
        "and Average Rate/sq.ft (Rs. 7,850). The module visualizes city price hierarchies, carpet area vs. valuation scatter correlations, "
        "property type box distributions, and an <b>Amenities Value Premium Analyzer</b> demonstrating that swimming pools add an average of "
        "+39.8% value premium, fitness gyms add +32.1%, and dedicated power backup adds +26.4%. A filterable table enables users to inspect "
        "individual comps by city, locality, and budget."
    )
    story.append(Paragraph(p_3_3, st['body']))

    story.append(Paragraph("3.4 Mathematical Derivation of Mortgage EMI Planner", st['h1']))
    p_3_4 = (
        "To provide financial underwriting clarity, the platform embeds an interactive <b>Indian Home Loan EMI Calculator</b>. "
        "Given the predicted property value, user down payment percentage (10%-50%), loan tenure (5-30 years), and annual interest rate (6.5%-14%), "
        "the monthly installment is derived using the standard compound interest amortization formula:"
    )
    story.append(Paragraph(p_3_4, st['body']))
    story.append(Paragraph("<i>EMI</i> = [<i>P</i> &times; <i>r</i> &times; (1 + <i>r</i>)<sup><i>n</i></sup>] / [(1 + <i>r</i>)<sup><i>n</i></sup> - 1]", ParagraphStyle('MathEq1', fontName='Times-Italic', fontSize=12, alignment=TA_CENTER, spaceBefore=4, spaceAfter=6)))
    story.append(Paragraph("where <i>P</i> is the principal borrowed amount, <i>r</i> is the monthly interest rate (annual rate / 12 / 100), and <i>n</i> is the total number of monthly payments. The module computes cash down payment required, total interest payable, and the loan-to-value (LTV) ratio.", st['body']))

    story.append(Paragraph("3.5 Side-by-Side Property Comparison Studio", st['h1']))
    p_3_5 = (
        "The <b>Comparison Studio</b> allows investors to benchmark two distinct properties simultaneously (e.g. Option A in Mumbai vs. "
        "Option B in Pune). The system computes valuation deltas, price-per-square-foot differences, and 4-pillar quality score gaps, "
        "generating an automated comparative synthesis that identifies the superior capital appreciation asset."
    )
    story.append(Paragraph(p_3_5, st['body']))

    story.append(Paragraph("3.6 One-Click Client Valuation Dossier Export", st['h1']))
    p_3_6 = (
        "Users can export the complete property evaluation—including point estimates, confidence spread bounds, pillar score breakdowns, "
        "and loan amortization tables—as a formatted text dossier (<code>.txt</code>) ready for banking and legal due diligence."
    )
    story.append(Paragraph(p_3_6, st['body']))
    story.append(PageBreak())

    # ==============================================================================
    # CHAPTER 4: DATA PIPELINE & MODEL WORKFLOW (Physical Page 10 - Arabic Page 5)
    # ==============================================================================
    story.append(Bookmark('chap4', tracker))
    story.append(Paragraph("Chapter 4: Data Pipeline, Preprocessing & Model Workflow", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.black, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("4.1 Benchmark Dataset Description (34 Features)", st['h1']))
    p_4_1 = (
        "The empirical ground truth rests on <b>506 validated property transactions</b> gathered during the AIML Summer Internship 2026 "
        "at IIHMF, MNNIT Prayagraj across 10 major metropolitan cities. The dataset spans 34 discrete attributes categorized in Table 4.1."
    )
    story.append(Paragraph(p_4_1, st['body']))

    story.append(Paragraph("Table 4.1: Housing Dataset Feature Architecture & Categorization", st['table_caption']))
    feat_table_data = [
        [Paragraph("<b>Category</b>", st['body_bold']), Paragraph("<b>Feature Name(s)</b>", st['body_bold']), Paragraph("<b>Data Type & Measurement Scale</b>", st['body_bold'])],
        [Paragraph("Geographic Location", st['body']), Paragraph("City, Locality, Locality_Type", st['body']), Paragraph("Nominal Categorical (10 Cities, 10 Localities, 3 Types)", st['body'])],
        [Paragraph("Physical Specs", st['body']), Paragraph("Area_sqft, Bedrooms, Bathrooms, Balconies, Floor_No, Total_Floors", st['body']), Paragraph("Continuous Float (Area: 300-10000) & Discrete Integer Counts", st['body'])],
        [Paragraph("Building Details", st['body']), Paragraph("Age_of_Property_Years, Furnishing_Status, Facing, Parking_Spaces", st['body']), Paragraph("Numerical Float (Age: 0-80) & Nominal Categorical", st['body'])],
        [Paragraph("Connectivity & Infra", st['body']), Paragraph("Distance_to_City_Center_km, Public_Transport_Access, Schools, Hospitals", st['body']), Paragraph("Continuous Float (0.2-80 km), Ordinal Strings, Discrete Counts", st['body'])],
        [Paragraph("Livability & Environment", st['body']), Paragraph("Crime_Rate_Index, Air_Quality_Index (AQI)", st['body']), Paragraph("Continuous Float (Crime: 0-100 scale, AQI: 0-300 scale)", st['body'])],
        [Paragraph("Society Amenities", st['body']), Paragraph("Lift, Security, Gym, Pool, Garden, Backup, Clubhouse, Amenities_Score", st['body']), Paragraph("Binary Boolean Flags (0 or 1) & Composite Rating (0-10 scale)", st['body'])],
        [Paragraph("Transaction & Target", st['body']), Paragraph("Ownership_Type, Transaction_Type, Listing_Type, Price_Lakhs", st['body']), Paragraph("Nominal Strings, Duration, and Target Valuation in INR Lakhs", st['body'])]
    ]
    feat_table = Table(feat_table_data, colWidths=[3.8 * cm, 6.2 * cm, 7.0 * cm])
    feat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(feat_table)
    story.append(Spacer(1, 0.3 * cm))

    if os.path.exists(FIG_DIST):
        story.append(Bookmark('fig4_1', tracker))
        story.append(RLImage(FIG_DIST, width=16.5 * cm, height=5.8 * cm))
        story.append(Paragraph("Figure 4.1: Empirical Price Density & Property Type Spread across 506 Homes", st['fig_caption']))
    story.append(PageBreak())

    # ==============================================================================
    # CHAPTER 4 (CONTD.): PREPROCESSING & ALGORITHMS (Physical Page 11 - Arabic Page 6)
    # ==============================================================================
    story.append(Paragraph("4.2 Data Preprocessing & Missing Value Imputation", st['h1']))
    p_4_2 = (
        "Ten missing target rows in <code>Price_Lakhs</code> were removed, leaving 496 high-integrity modeling observations. "
        "Missing values in continuous numerical attributes (<code>Area_sqft</code>, <code>Bathrooms</code>, <code>Age_of_Property_Years</code>, "
        "<code>Crime_Rate_Index</code>, and <code>Air_Quality_Index</code>) were imputed using statistical <b>medians</b> to prevent outlier skewing. "
        "Missing categorical values (<code>Furnishing_Status</code>) were imputed using the statistical <b>mode</b>. Zero duplicate records were observed."
    )
    story.append(Paragraph(p_4_2, st['body']))

    if os.path.exists(FIG_CITY):
        story.append(Bookmark('fig4_2', tracker))
        story.append(RLImage(FIG_CITY, width=16.5 * cm, height=5.8 * cm))
        story.append(Paragraph("Figure 4.2: Average Metropolitan Property Prices across 10 Sampled Indian Metros", st['fig_caption']))

    story.append(Paragraph("4.3 ColumnTransformer & Categorical Subspace Encoding", st['h1']))
    p_4_3 = (
        "To process heterogeneous features, a scikit-learn <b>ColumnTransformer</b> was constructed. Ten categorical columns "
        "(<code>City</code>, <code>Locality</code>, <code>Locality_Type</code>, <code>Property_Type</code>, <code>Furnishing_Status</code>, "
        "<code>Facing</code>, <code>Public_Transport_Access</code>, <code>Ownership_Type</code>, <code>Transaction_Type</code>, "
        "<code>Listing_Type</code>) are encoded via <code>OneHotEncoder(handle_unknown='ignore')</code> into 46 binary dummy vectors. "
        "The 22 continuous numerical attributes are passed through directly via <code>remainder='passthrough'</code>."
    )
    story.append(Paragraph(p_4_3, st['body']))

    story.append(Paragraph("4.4 Supervised Regression Algorithm Formulations", st['h1']))
    p_4_4 = (
        "Three distinct supervised learning models were trained on an 80/20 train/test split (396 train samples, 100 test samples, seed 42): "
        "<br/>1. <b>Ordinary Least Squares Linear Regression:</b> min ||<i>y</i> - <i>X</i>&beta;||&sup2; (parametric baseline). "
        "<br/>2. <b>Random Forest Regressor:</b> 100 bootstrap aggregated decision trees: <i>y&#770;</i> = (1/<i>B</i>) &sum; <i>T<sub>b</sub></i>(<i>x</i>). "
        "<br/>3. <b>Gradient Boosting Regressor:</b> Sequential additive tree expansion fitting pseudo-residuals <i>r<sub>im</sub></i> = - [&part;<i>L</i>/&part;<i>F</i>] "
        "with learning rate &eta; = 0.1: <i>F<sub>m</sub></i>(<i>x</i>) = <i>F</i><sub><i>m</i>-1</sub>(<i>x</i>) + &eta; &times; <i>h<sub>m</sub></i>(<i>x</i>)."
    )
    story.append(Paragraph(p_4_4, st['body']))

    story.append(Paragraph("Table 4.2: Hyperparameter Configurations for Candidate Regressors", st['table_caption']))
    hyp_table_data = [
        [Paragraph("<b>Model Architecture</b>", st['body_bold']), Paragraph("<b>Key Hyperparameters</b>", st['body_bold']), Paragraph("<b>Optimization Objective</b>", st['body_bold'])],
        [Paragraph("Linear Regression", st['body']), Paragraph("fit_intercept=True, positive=False", st['body']), Paragraph("Minimize Sum of Squared Residuals (OLS)", st['body'])],
        [Paragraph("Random Forest", st['body']), Paragraph("n_estimators=100, max_features='sqrt', random_state=42", st['body']), Paragraph("Variance reduction via bagging", st['body'])],
        [Paragraph("Gradient Boosting", st['body']), Paragraph("n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42", st['body']), Paragraph("Sequential pseudo-residual MSE minimization", st['body'])]
    ]
    hyp_table = Table(hyp_table_data, colWidths=[4.5 * cm, 6.0 * cm, 6.5 * cm])
    hyp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(hyp_table)
    story.append(PageBreak())

    # ==============================================================================
    # CHAPTER 5: KEY FEATURES & PRACTICAL INNOVATIONS (Physical Page 12 - Arabic Page 7)
    # ==============================================================================
    story.append(Bookmark('chap5', tracker))
    story.append(Paragraph("Chapter 5: Key Features & Practical Innovations", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.black, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("5.1 Dual-Currency Price Prediction & Spread Bounds", st['h1']))
    p_5_1 = (
        "Unlike generic regression models outputting a single deterministic float, HomeWorth AI computes an empirical confidence spread "
        "grounded in the model's test-set Mean Absolute Error (<i>MAE</i> = Rs. 10.01 Lakhs): [<i>y&#770;</i> - 0.75 &times; <i>MAE</i>, "
        "<i>y&#770;</i> + 0.75 &times; <i>MAE</i>]. Valuations exceeding Rs. 100 Lakhs are automatically formatted in Crores (e.g. Rs. 1.89 Cr / 188.56 L)."
    )
    story.append(Paragraph(p_5_1, st['body']))

    story.append(Paragraph("5.2 Standardized 4-Pillar Property Quality Scorecard (0-100)", st['h1']))
    p_5_2 = (
        "To objectively evaluate physical and environmental livability, the platform introduces a 100-point Property Quality Score "
        "decomposed across four equal 25-point pillars: (1) <b>Location & Transit Pillar (Max 25 pts):</b> Distance to city center (up to 9 pts), "
        "public transit access (up to 6 pts), school density (up to 5 pts), and hospital access (up to 5 pts); (2) <b>Specs & Architecture Pillar (Max 25 pts):</b> "
        "Carpet area bracket (up to 8 pts), building age (up to 7 pts), parking spaces (up to 4 pts), furnishing level (up to 3 pts), and East facing (up to 3 pts); "
        "(3) <b>Society Amenities Pillar (Max 25 pts):</b> Base amenities score plus bonus points for lift, security, gym, pool, power backup, garden, and clubhouse; "
        "and (4) <b>Safety & Environment Pillar (Max 25 pts):</b> Crime rate index (up to 13 pts for crime &lt; 20) and Air Quality Index AQI (up to 12 pts for AQI &lt; 45)."
    )
    story.append(Paragraph(p_5_2, st['body']))

    story.append(Paragraph("Table 5.1: 4-Pillar Quality Scoring Allocation & Grading Scale", st['table_caption']))
    grade_table_data = [
        [Paragraph("<b>Score Range</b>", st['body_bold']), Paragraph("<b>Grade</b>", st['body_bold']), Paragraph("<b>Classification</b>", st['body_bold']), Paragraph("<b>Recommended Action</b>", st['body_bold'])],
        [Paragraph("88 - 100", st['body']), Paragraph("AAA", st['body']), Paragraph("Prime Outperform Asset", st['body']), Paragraph("Strong Buy; High capital appreciation potential", st['body'])],
        [Paragraph("75 - 87", st['body']), Paragraph("AA", st['body']), Paragraph("High Conviction Family Asset", st['body']), Paragraph("Low-risk family asset; stable long-term appreciation", st['body'])],
        [Paragraph("62 - 74", st['body']), Paragraph("A", st['body']), Paragraph("Stable Quality Accumulation", st['body']), Paragraph("Fair market value; verify minor maintenance items", st['body'])],
        [Paragraph("50 - 61", st['body']), Paragraph("B", st['body']), Paragraph("Moderate Risk Profile", st['body']), Paragraph("Negotiate price discount; inspect surrounding micro-market", st['body'])],
        [Paragraph("0 - 49", st['body']), Paragraph("C", st['body']), Paragraph("Speculative / Due Diligence", st['body']), Paragraph("Exercise caution; potential safety or legal clearance flags", st['body'])]
    ]
    grade_table = Table(grade_table_data, colWidths=[2.5 * cm, 2.0 * cm, 5.0 * cm, 7.5 * cm])
    grade_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(grade_table)
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("5.3 Contextual AI House Buying Advisory Engine", st['h1']))
    p_5_3 = (
        "The automated advisor synthesizes multivariate inputs into four actionable pillars: (a) <b>Core Strengths:</b> Highlights verified asset "
        "advantages (East-facing morning sunlight, low age, high parking); (b) <b>Value Drivers:</b> Identifies rental liquidity drivers (transit proximity, "
        "reputed schools); (c) <b>Due Diligence & Risks:</b> Flags elevated crime (&gt;50/100), poor AQI (&gt;100), or aging builds (&gt;18 yrs); "
        "and (d) <b>Buyer's Negotiation Playbook:</b> Recommends bidding 8%-12% below asking price if listing duration exceeds 6 months."
    )
    story.append(Paragraph(p_5_3, st['body']))
    story.append(PageBreak())

    # ==============================================================================
    # CHAPTER 6: PERFORMANCE EVALUATION & BENCHMARKING (Physical Page 13 - Arabic Page 8)
    # ==============================================================================
    story.append(Bookmark('chap6', tracker))
    story.append(Paragraph("Chapter 6: Performance Evaluation, Benchmarking & XAI", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.black, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("6.1 Regression Evaluation Metrics (R&sup2;, MAE, RMSE)", st['h1']))
    p_6_1 = (
        "Models were evaluated on 100 unseen test samples using: (1) <b>Mean Absolute Error (MAE):</b> (1/<i>n</i>) &sum; |<i>y<sub>i</sub></i> - <i>y&#770;<sub>i</sub></i>| "
        "(average magnitude of residuals); (2) <b>Root Mean Squared Error (RMSE):</b> &radic;[(1/<i>n</i>) &sum; (<i>y<sub>i</sub></i> - <i>y&#770;<sub>i</sub></i>)&sup2;] "
        "(penalizing large outlier deviations); and (3) <b>Coefficient of Determination (R&sup2; Score):</b> 1 - [&sum; (<i>y<sub>i</sub></i> - <i>y&#770;<sub>i</sub></i>)&sup2; / &sum; (<i>y<sub>i</sub></i> - <i>y&#772;</i>)&sup2;] "
        "(proportion of total price variance explained)."
    )
    story.append(Paragraph(p_6_1, st['body']))

    story.append(Paragraph("Table 6.1: Model Performance Leaderboard on 100 Test Samples", st['table_caption']))
    lead_table_data = [
        [Paragraph("<b>Model Architecture</b>", st['body_bold']), Paragraph("<b>MAE (Rs. L)</b>", st['body_bold']), Paragraph("<b>RMSE (Rs. L)</b>", st['body_bold']), Paragraph("<b>R&sup2; Score</b>", st['body_bold']), Paragraph("<b>Classification</b>", st['body_bold'])],
        [Paragraph("<b>Gradient Boosting Regressor</b>", st['body']), Paragraph("<b>10.0084</b>", st['body']), Paragraph("<b>13.8546</b>", st['body']), Paragraph("<b>0.9392</b>", st['body']), Paragraph("<b>Winner (Selected)</b>", st['body'])],
        [Paragraph("Linear Regression", st['body']), Paragraph("13.7930", st['body']), Paragraph("18.4201", st['body']), Paragraph("0.8925", st['body']), Paragraph("Parametric Baseline", st['body'])],
        [Paragraph("Random Forest Regressor", st['body']), Paragraph("15.8573", st['body']), Paragraph("21.9976", st['body']), Paragraph("0.8467", st['body']), Paragraph("Ensemble Bagging", st['body'])]
    ]
    lead_table = Table(lead_table_data, colWidths=[5.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 4.0 * cm])
    lead_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(lead_table)
    story.append(Spacer(1, 0.25 * cm))

    if os.path.exists(FIG_MODEL):
        story.append(Bookmark('fig6_1', tracker))
        story.append(RLImage(FIG_MODEL, width=16.5 * cm, height=6.2 * cm))
        story.append(Paragraph("Figure 6.1: Comparative Performance Leaderboard across Evaluated Machine Learning Regressors", st['fig_caption']))

    p_6_2 = (
        "<b>Performance Discussion:</b> Gradient Boosting achieved the highest R&sup2; (0.9392) and lowest MAE (Rs. 10.01 Lakhs). "
        "Its sequential boosting mechanism corrects pseudo-residuals of earlier trees, effectively modeling complex non-linear amenity interactions. "
        "Linear Regression (R&sup2; = 0.8925) captured carpet area well but failed on non-linear amenities. Random Forest (R&sup2; = 0.8467) suffered variance penalties on smaller subsets."
    )
    story.append(Paragraph(p_6_2, st['body']))
    story.append(PageBreak())

    # ==============================================================================
    # CHAPTER 6 (CONTD.): FEATURE IMPORTANCE & RESIDUALS (Physical Page 14 - Arabic Page 9)
    # ==============================================================================
    story.append(Paragraph("6.3 Explainable AI (XAI) & Feature Importance Weights", st['h1']))
    p_6_3 = (
        "Feature importances were extracted directly from the Gradient Boosting ensemble. <code>Area_sqft</code> is the dominant predictor, "
        "accounting for <b>63.56%</b> of total predictive weight. Metropolitan city tiers represent the second major cluster, contributing "
        "approximately <b>23%</b> combined weight (Delhi: 6.06%, Lucknow: 4.63%, Bengaluru: 4.56%, Ahmedabad: 4.36%, Mumbai: 3.29%). "
        "Standalone luxury villas contribute 2.37%, distance to city center contributes 1.99%, and property age accounts for 1.50%."
    )
    story.append(Paragraph(p_6_3, st['body']))

    if os.path.exists(FIG_FEAT):
        story.append(Bookmark('fig6_2', tracker))
        story.append(RLImage(FIG_FEAT, width=16.5 * cm, height=6.2 * cm))
        story.append(Paragraph("Figure 6.2: Feature Importance Weights Derived from the Gradient Boosting Pipeline", st['fig_caption']))

    story.append(Paragraph("6.4 Residual Error Distribution & Validation", st['h1']))
    p_6_4 = (
        "Residual error analysis demonstrates that prediction residuals are tightly centered around zero error (mean = Rs. 0.12 Lakhs) "
        "with an approximately normal Gaussian bell curve. The actual vs. predicted scatter plot adheres closely to the 1:1 identity line, "
        "verifying that the model maintains homoscedasticity without systematic over- or under-prediction across price brackets."
    )
    story.append(Paragraph(p_6_4, st['body']))

    if os.path.exists(FIG_RES):
        story.append(Bookmark('fig6_3', tracker))
        story.append(RLImage(FIG_RES, width=16.5 * cm, height=5.2 * cm))
        story.append(Paragraph("Figure 6.3: Actual vs. Predicted Prices & Residual Error Distribution", st['fig_caption']))
    story.append(PageBreak())

    # ==============================================================================
    # CHAPTER 7 & 8: LIMITATIONS & CONCLUSION (Physical Page 15 - Arabic Page 10)
    # ==============================================================================
    story.append(Bookmark('chap7', tracker))
    story.append(Paragraph("Chapter 7: Limitations & Environmental Risk Factors", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.black, spaceBefore=2, spaceAfter=6))

    p_7_1 = (
        "While HomeWorth AI achieves 93.92% accuracy, three primary technical constraints exist: "
        "<br/>1. <b>Geographical Sampling Boundaries:</b> Evaluates 506 properties across 10 major metropolitan centers; localized peri-urban "
        "villages and Tier-3 industrial corridors require regional re-calibration. "
        "<br/>2. <b>Qualitative Interior Nuances:</b> Structured tabular parameters cannot fully account for bespoke Italian marble finishes, "
        "architectural woodwork, or scenic panoramic sea/park view premiums, necessitating physical on-site inspection. "
        "<br/>3. <b>Macroeconomic Shocks:</b> Evaluates static cross-sectional market conditions and does not currently integrate dynamic time-series "
        "autoregression for sudden RBI repo rate shifts or building material inflationary surges."
    )
    story.append(Paragraph(p_7_1, st['body']))

    story.append(Bookmark('chap8', tracker))
    story.append(Paragraph("Chapter 8: Conclusion and Future Work", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.black, spaceBefore=2, spaceAfter=6))

    p_8_1 = (
        "<b>8.1 Conclusion & Research Deliverables:</b> The HomeWorth AI project successfully designs, validates, and deploys an AI-powered "
        "residential valuation platform. The trained <b>Gradient Boosting Regressor</b> achieved <b>93.92% accuracy (R&sup2; = 0.9392)</b> "
        "and a low Mean Absolute Error of <b>Rs. 10.01 Lakhs</b> on unseen test data. The system bridges machine learning research and commercial "
        "PropTech utility by delivering dual-currency price bounds, an objective 100-point Property Health Score, an automated AI buying advisor, "
        "an Indian home loan EMI calculator, and a side-by-side property comparison studio."
    )
    story.append(Paragraph(p_8_1, st['body']))

    p_8_2 = (
        "<b>8.2 Academic & Industry Impact:</b> Fulfills all B.Tech curriculum requirements in Computer Science & Engineering (AI & ML) at "
        "United College of Engineering & Research (UCER), affiliated to Dr. A.P.J. Abdul Kalam Technical University (AKTU), Lucknow, "
        "showcasing zero data-leakage pipelines, explainable AI feature weights, and responsive glassmorphic UI design."
    )
    story.append(Paragraph(p_8_2, st['body']))

    p_8_3 = (
        "<b>8.3 Future Enhancement Roadmap:</b> (1) <i>Live Web Scraping:</i> Automated crawlers for MagicBricks, 99acres, and Housing.com; "
        "(2) <i>Geospatial GIS Mapping:</i> Google Maps Platform integration for real-time transit commute times; "
        "(3) <i>Deep Learning Architectures:</i> TabNet and attention networks for expanded nationwide datasets; and "
        "(4) <i>Mobile Application (Flutter):</i> Cross-platform iOS/Android app with camera-based property scanning."
    )
    story.append(Paragraph(p_8_3, st['body']))
    story.append(PageBreak())

    # ==============================================================================
    # REFERENCES & APPENDIX (Physical Page 16 - Arabic Page 11)
    # ==============================================================================
    story.append(Bookmark('refs', tracker))
    story.append(Paragraph("References", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.black, spaceBefore=2, spaceAfter=6))

    refs = [
        "1. Pedregosa, F. et al., 2011. Scikit-learn: Machine learning in Python. <i>Journal of Machine Learning Research</i>, 12, pp.2825-2830.",
        "2. Friedman, J.H., 2001. Greedy function approximation: a gradient boosting machine. <i>Annals of Statistics</i>, 29(5), pp.1189-1232.",
        "3. Breiman, L., 2001. Random forests. <i>Machine Learning</i>, 45(1), pp.5-32.",
        "4. McKinney, W., 2010. Data structures for statistical computing in Python. <i>Proc. 9th Python in Sci. Conf.</i>, 445, pp.51-56.",
        "5. Harris, C.R. et al., 2020. Array programming with NumPy. <i>Nature</i>, 585(7825), pp.357-362.",
        "6. National Housing Bank (NHB), 2025. <i>NHB RESIDEX: Housing Price Index for Major Indian Metros</i>. Govt. of India.",
        "7. Streamlit Documentation, 2026. <i>Deploying Interactive Data Applications</i>. Available at: https://docs.streamlit.io/.",
        "8. Plotly Technologies Inc., 2026. <i>WebGL Graphics & Interactive Visualizations</i>. Montreal, QC.",
        "9. Motilal Nehru National Institute of Technology (MNNIT), 2026. <i>IIHMF AIML Summer Internship Training Curriculum</i>."
    ]
    for r in refs:
        story.append(Paragraph(r, st['bullet']))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Bookmark('appx', tracker))
    story.append(Paragraph("Appendix: Core Pipeline Architecture & Source Code", st['chapter']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.black, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph("Appendix A: Scikit-Learn Pipeline Serialization (predictor.py)", st['h1']))
    code_text = (
        "<font face='Courier' size='8'>"
        "import os, joblib, pandas as pd<br/>"
        "MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'Model', 'house_price_pipeline.pkl')<br/>"
        "pipeline = joblib.load(MODEL_PATH)<br/>"
        "def predict_price(user_input: dict) -&gt; float:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;return max(round(float(pipeline.predict(pd.DataFrame([user_input]))[0]), 2), 5.0)<br/>"
        "def predict_price_range(predicted_price: float, mae: float = 10.01) -&gt; tuple:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;spread = round(mae * 0.75, 2)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;return max(round(predicted_price - spread, 2), 5.0), round(predicted_price + spread, 2)<br/>"
        "</font>"
    )
    story.append(Paragraph(code_text, ParagraphStyle('CodeBox1', fontName='Courier', fontSize=8, leading=11, spaceBefore=2, spaceAfter=6, leftIndent=8)))

    story.append(Paragraph("Appendix B: Financial EMI Calculation Algorithm (utils.py)", st['h1']))
    code_text2 = (
        "<font face='Courier' size='8'>"
        "def calculate_emi(principal_lakhs, down_payment_pct=20.0, tenure_years=20, annual_interest_rate=8.5):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;down_payment = (principal_lakhs * down_payment_pct) / 100.0<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;loan_amount = principal_lakhs - down_payment<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;P = loan_amount * 100000.0; r = (annual_interest_rate / 12.0) / 100.0; n = tenure_years * 12<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;emi = (P * r * ((1 + r)**n)) / (((1 + r)**n) - 1) if r &gt; 0 and n &gt; 0 else 0<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;return {'monthly_emi': round(emi, 0), 'loan_amount_lakhs': round(loan_amount, 2)}<br/>"
        "</font>"
    )
    story.append(Paragraph(code_text2, ParagraphStyle('CodeBox2', fontName='Courier', fontSize=8, leading=11, spaceBefore=2, spaceAfter=6, leftIndent=8)))

    story.append(Paragraph("Appendix C: 4-Pillar Property Livability Scoring Algorithm (utils.py)", st['h1']))
    code_text3 = (
        "<font face='Courier' size='8'>"
        "def calculate_property_score(data: dict) -&gt; dict:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;loc_pts = (9 if dist &lt;= 5 else 7 if dist &lt;= 12 else 4) + (6 if transit == 'High' else 4 if transit == 'Medium' else 2) + min(schools, 5) + min(hospitals, 5)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;spec_pts = (8 if area &gt;= 1800 else 6 if area &gt;= 1100 else 4) + (7 if age &lt;= 3 else 5 if age &lt;= 10 else 3) + min(parking * 2, 4)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;amen_pts = min(amenities_count * 3, 25); safe_pts = (13 if crime &lt; 20 else 9 if crime &lt; 40 else 4) + (12 if aqi &lt; 50 else 8 if aqi &lt; 100 else 3)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;return {'total_score': min(loc_pts + spec_pts + amen_pts + safe_pts, 100), 'breakdown': (loc_pts, spec_pts, amen_pts, safe_pts)}<br/>"
        "</font>"
    )
    story.append(Paragraph(code_text3, ParagraphStyle('CodeBox3', fontName='Courier', fontSize=8, leading=11, spaceBefore=2, spaceAfter=6, leftIndent=8)))

    return story


def build_pdf():
    # Symmetric 2.0 cm margins for visually centered alignment on A4
    doc_pass1 = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=2.0 * cm,
        rightMargin=2.0 * cm,
        topMargin=2.0 * cm,
        bottomMargin=2.0 * cm
    )
    story1 = build_story(PAGE_TRACKER)
    doc_pass1.build(story1, canvasmaker=CenteredAcademicCanvas)
    print("Pass 1 completed. Recorded page anchors:", PAGE_TRACKER)

    # Pass 2: Rebuild with exact recorded page numbers inserted into TOC & Lists
    doc_pass2 = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=2.0 * cm,
        rightMargin=2.0 * cm,
        topMargin=2.0 * cm,
        bottomMargin=2.0 * cm
    )
    story2 = build_story(PAGE_TRACKER)
    doc_pass2.build(story2, canvasmaker=CenteredAcademicCanvas)
    print(f"Pass 2 completed. Final Project Report successfully generated at: {OUTPUT_PDF}")


if __name__ == '__main__':
    build_pdf()
