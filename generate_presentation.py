import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRATCH_DIR = r"C:\Users\ujjav\.gemini\antigravity\brain\54b1e0af-2f7a-4222-8817-cb66512bb3b9\scratch"
PPT_LOGOS_DIR = os.path.join(SCRATCH_DIR, "ppt_logos")
FIGS_DIR = os.path.join(SCRATCH_DIR, "doc_figures")
BANNER_PATH = os.path.join(BASE_DIR, "Streamlit_App", "assets", "hero_banner.png")
OUTPUT_PPTX = os.path.join(BASE_DIR, "HomeWorth_AI_Presentation.pptx")

# Logo files
LOGO_UNITED = os.path.join(PPT_LOGOS_DIR, "img_p1_0.png")
LOGO_AKTU = os.path.join(PPT_LOGOS_DIR, "img_p1_1.png")

# Palette
DARK_NAVY = RGBColor(15, 23, 42)
ROYAL_BLUE = RGBColor(30, 58, 138)
ACCENT_BLUE = RGBColor(37, 99, 235)
LIGHT_BLUE = RGBColor(239, 246, 255)
TEXT_DARK = RGBColor(30, 41, 59)
TEXT_MUTED = RGBColor(100, 116, 139)
WHITE = RGBColor(255, 255, 255)
GREEN_ACCENT = RGBColor(16, 185, 129)
LINE_COLOR = RGBColor(59, 130, 246)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def add_header(slide, title_text=""):
    # Header container
    header_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    header_box.fill.solid()
    header_box.fill.fore_color.rgb = WHITE
    header_box.line.color.rgb = WHITE
    
    # United Logo
    if os.path.exists(LOGO_UNITED):
        slide.shapes.add_picture(LOGO_UNITED, Inches(0.5), Inches(0.18), height=Inches(0.75))
    
    # AKTU Logo
    if os.path.exists(LOGO_AKTU):
        slide.shapes.add_picture(LOGO_AKTU, Inches(11.8), Inches(0.12), height=Inches(0.9))
        
    # Blue separator line matching template
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.04))
    line.fill.solid()
    line.fill.fore_color.rgb = LINE_COLOR
    line.line.color.rgb = LINE_COLOR
    
    # Slide Title
    if title_text:
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.28), Inches(11.7), Inches(0.75))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Times New Roman"
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = DARK_NAVY

# ============================================================
# SLIDE 1: Title Slide (Strictly Matching Attachment 2 Template)
# ============================================================
s1 = prs.slides.add_slide(blank_layout)
add_header(s1)

# "Summer Training Presentation" (at top center, as per template)
top_sub = s1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.333), Inches(0.8))
tf_sub = top_sub.text_frame
p_sub = tf_sub.paragraphs[0]
p_sub.text = "Summer Training Presentation"
p_sub.font.name = "Times New Roman"
p_sub.font.size = Pt(36)
p_sub.font.bold = True
p_sub.font.color.rgb = DARK_NAVY
p_sub.alignment = PP_ALIGN.CENTER

# Project Title Card (Center)
title_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(2.55), Inches(10.933), Inches(1.9))
title_box.fill.solid()
title_box.fill.fore_color.rgb = LIGHT_BLUE
title_box.line.color.rgb = ACCENT_BLUE
title_box.line.width = Pt(1.5)

tf_title = title_box.text_frame
tf_title.word_wrap = True
p_t1 = tf_title.paragraphs[0]
p_t1.text = "HOMEWORTH AI"
p_t1.font.name = "Times New Roman"
p_t1.font.size = Pt(32)
p_t1.font.bold = True
p_t1.font.color.rgb = ROYAL_BLUE
p_t1.alignment = PP_ALIGN.CENTER

p_t2 = tf_title.add_paragraph()
p_t2.text = "AI-Powered House Price Prediction & Real Estate Valuation System"
p_t2.font.name = "Times New Roman"
p_t2.font.size = Pt(20)
p_t2.font.bold = True
p_t2.font.color.rgb = TEXT_DARK
p_t2.alignment = PP_ALIGN.CENTER

p_t3 = tf_title.add_paragraph()
p_t3.text = "Carried out at: IIHMF, Motilal Nehru National Institute of Technology (MNNIT), Prayagraj"
p_t3.font.name = "Times New Roman"
p_t3.font.size = Pt(13)
p_t3.font.italic = True
p_t3.font.color.rgb = TEXT_MUTED
p_t3.alignment = PP_ALIGN.CENTER

# Bottom Info Columns (Left: Student Names & AKTU Roll Numbers, Right: Supervisor & Institution)
left_box = s1.shapes.add_textbox(Inches(1.2), Inches(4.7), Inches(5.3), Inches(2.2))
tf_left = left_box.text_frame
tf_left.word_wrap = True

p_l0 = tf_left.paragraphs[0]
p_l0.text = "SUBMITTED BY:"
p_l0.font.name = "Times New Roman"
p_l0.font.size = Pt(14)
p_l0.font.bold = True
p_l0.font.color.rgb = ROYAL_BLUE

students = [
    ("Ujjaval Kumar Kesarwani", "AKTU Roll No: 2400101530154"),
    ("Shlok Tiwari", "AKTU Roll No: 2400101530134")
]
for name, roll in students:
    p_name = tf_left.add_paragraph()
    p_name.text = f"• {name}"
    p_name.font.name = "Times New Roman"
    p_name.font.size = Pt(15)
    p_name.font.bold = True
    p_name.font.color.rgb = TEXT_DARK
    
    p_roll = tf_left.add_paragraph()
    p_roll.text = f"   {roll}"
    p_roll.font.name = "Times New Roman"
    p_roll.font.size = Pt(13)
    p_roll.font.color.rgb = TEXT_MUTED

right_box = s1.shapes.add_textbox(Inches(6.8), Inches(4.7), Inches(5.3), Inches(2.2))
tf_right = right_box.text_frame
tf_right.word_wrap = True

p_r0 = tf_right.paragraphs[0]
p_r0.text = "UNDER THE SUPERVISION OF:"
p_r0.font.name = "Times New Roman"
p_r0.font.size = Pt(14)
p_r0.font.bold = True
p_r0.font.color.rgb = ROYAL_BLUE

p_sup = tf_right.add_paragraph()
p_sup.text = "Dr. Divya Kumar"
p_sup.font.name = "Times New Roman"
p_sup.font.size = Pt(16)
p_sup.font.bold = True
p_sup.font.color.rgb = TEXT_DARK

p_dept = tf_right.add_paragraph()
p_dept.text = "Associate Professor\nDepartment of Computer Science & Engineering\nMotilal Nehru National Institute of Technology (MNNIT), Prayagraj"
p_dept.font.name = "Times New Roman"
p_dept.font.size = Pt(12)
p_dept.font.color.rgb = TEXT_MUTED

# ============================================================
# SLIDE 2: Outline (Strictly Matching Attachment 2 Template)
# ============================================================
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "Presentation Outline")

outline_items = [
    ("01", "Introduction & Problem Statement", "The valuation gap, broker subjectivity, and real estate market opacity."),
    ("02", "Project Objectives", "Predictive modeling, composite quality scoring, automated AI buying advisor."),
    ("03", "Methodology & Architecture", "506 benchmark properties, 34 attributes, 10 Indian metropolitan cities."),
    ("04", "Machine Learning Pipeline", "Preprocessing, One-Hot Encoding, ColumnTransformer, and regression training."),
    ("05", "Model Evaluation & Results", "Gradient Boosting (93.92% R²) vs. Random Forest vs. Linear Regression."),
    ("06", "Explainable AI (XAI)", "Feature importance weights driving fair market value estimation."),
    ("07", "Implementation & Web Dashboard", "Production Streamlit application, financial EMI planner, property comparison."),
    ("08", "Conclusion & Future Work", "Summary of internship outcomes, practical impact, and future extensions.")
]

y_start = 2.15
for idx, (num, title, desc) in enumerate(outline_items):
    col = idx % 2
    row = idx // 2
    x = 0.8 + (col * 6.0)
    y = y_start + (row * 1.22)
    
    card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(5.7), Inches(1.05))
    card.fill.solid()
    card.fill.fore_color.rgb = LIGHT_BLUE
    card.line.color.rgb = RGBColor(219, 234, 254)
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.18)
    tf.margin_top = Inches(0.12)
    
    p = tf.paragraphs[0]
    p.text = f"{num}  {title}"
    p.font.name = "Times New Roman"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ROYAL_BLUE
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = "Times New Roman"
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = TEXT_DARK

# ============================================================
# SLIDE 3: Introduction & The PropTech Challenge
# ============================================================
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "Introduction: The Real Estate Valuation Gap")

def add_bullet_card(slide, x, y, w, h, title, bullets, border_color=ACCENT_BLUE):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    card.fill.solid()
    card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.2)
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Times New Roman"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ROYAL_BLUE
    
    for b in bullets:
        p_b = tf.add_paragraph()
        p_b.text = f"•  {b}"
        p_b.font.name = "Times New Roman"
        p_b.font.size = Pt(13)
        p_b.font.color.rgb = TEXT_DARK
        p_b.space_before = Pt(8)

add_bullet_card(
    s3, 0.8, 2.2, 5.7, 4.7,
    "⚠️ The Traditional Valuation Dilemma",
    [
        "Subjective & Biased Estimates: Traditional home pricing heavily depends on middleman / broker opinions and anecdotal neighborhood pricing.",
        "Market Opacity: Buyers frequently overpay due to artificial inflation, while sellers face stagnant listings when overpriced.",
        "Static Calculators Lack Context: Generic price calculators solely evaluate area, ignoring air quality (AQI), crime rates, and transit.",
        "High Financial Risk: Real estate represents the largest single lifetime investment for Indian families; inaccurate valuation causes severe financial distress."
    ],
    border_color=RGBColor(239, 68, 68)
)

add_bullet_card(
    s3, 6.8, 2.2, 5.7, 4.7,
    "💡 The HomeWorth AI Solution",
    [
        "Data-Driven Machine Learning: Replaces guesswork with empirical regression models trained on multi-metro Indian transaction records.",
        "Holistic Multi-Factor Pricing: Incorporates 34 structural, environmental, transit, security, and society amenities parameters.",
        "Composite Property Quality Score: An objective 0–100 index evaluating Location, Architecture, Amenities, and Safety.",
        "Actionable Advisory Engine: Contextual recommendations on negotiation leverage, asset strengths, and due diligence checks.",
        "Production-Grade Web Application: Interactive Streamlit interface with integrated mortgage/EMI planner."
    ],
    border_color=GREEN_ACCENT
)

# ============================================================
# SLIDE 4: Project Objectives
# ============================================================
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "Project Objectives & Scope")

objs = [
    ("🎯 High-Precision Valuation", "Develop and tune robust supervised regression models to predict residential prices with >90% R² accuracy, minimizing MAE on unseen test data."),
    ("📐 Multi-Dimensional Feature Modeling", "Engineer comprehensive feature transformers that account for physical carpet area, age, facing, society amenities, and transit corridors."),
    ("🏆 4-Pillar Livability Index", "Construct a standardized 100-point Property Health Score assessing Location, Physical Construction, Lifestyle Amenities, and Environmental Safety."),
    ("🤖 Explainable AI & Buyer Advisory", "Deliver transparent feature importance rankings and automated real estate advice detailing growth drivers, risk flags, and negotiation tactics."),
    ("🏦 Integrated Financial Planning", "Equip users with built-in mortgage / EMI calculations, loan-to-value ratios, and downloadable official property valuation reports."),
    ("🌐 Production Web Deployment", "Deploy a responsive, enterprise-grade dark-glassmorphism Streamlit platform accessible to home buyers, sellers, and evaluators.")
]

for idx, (title, desc) in enumerate(objs):
    col = idx % 2
    row = idx // 2
    x = 0.8 + (col * 6.0)
    y = 2.2 + (row * 1.6)
    
    box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(5.7), Inches(1.4))
    box.fill.solid()
    box.fill.fore_color.rgb = LIGHT_BLUE
    box.line.color.rgb = ACCENT_BLUE
    box.line.width = Pt(1)
    
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.15)
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Times New Roman"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ROYAL_BLUE
    
    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.name = "Times New Roman"
    p_d.font.size = Pt(12)
    p_d.font.color.rgb = TEXT_DARK
    p_d.space_before = Pt(4)

# ============================================================
# SLIDE 5: Dataset Architecture & Exploratory Data Analysis
# ============================================================
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "Dataset Architecture & Geographic Scope")

# Left Column: Dataset Details
add_bullet_card(
    s5, 0.8, 2.2, 5.7, 4.7,
    "📊 Dataset Overview (506 Benchmark Homes)",
    [
        "Scope & Dimensions: 506 validated property transactions across 10 top Indian metropolitan centers, containing 34 detailed attributes.",
        "Geographic Coverage: Mumbai, Delhi, Bengaluru, Pune, Chennai, Hyderabad, Kolkata, Ahmedabad, Lucknow, and Jaipur.",
        "Property Types: High-rise Apartments (54.7%), Luxury Villas (16.0%), Independent Houses (17.2%), and Builder Floors (10.1%).",
        "Target Variable: Price_Lakhs (INR) ranging from ₹ 10.0 Lakhs to ₹ 473.21 Lakhs (Mean: ₹ 99.61 L, Median: ₹ 92.90 L).",
        "Data Hygiene: Missing values in numerical attributes imputed via median; categorical features imputed with mode; zero target nulls."
    ]
)

# Right Column: City Prices Chart
if os.path.exists(os.path.join(FIGS_DIR, "fig_city_prices.png")):
    s5.shapes.add_picture(os.path.join(FIGS_DIR, "fig_city_prices.png"), Inches(6.8), Inches(2.2), width=Inches(5.7))

# ============================================================
# SLIDE 6: Machine Learning Pipeline & Methodology
# ============================================================
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, "Machine Learning Methodology & Pipeline")

steps = [
    ("Step 1: Data Ingestion & Cleaning", "Load 506 raw records from Excel. Drop House_ID unique identifier. Impute missing values with statistical medians and modes."),
    ("Step 2: ColumnTransformer Architecture", "10 Categorical Features (City, Locality, Property Type, Facing, Furnishing, etc.) processed via OneHotEncoder(handle_unknown='ignore') -> 46 dummy variables.\n22 Numerical Features passed through without data leakage."),
    ("Step 3: 80/20 Train-Test Partitioning", "Split data into Training Set (396 samples, 32 raw features) and Testing Set (100 samples, 32 raw features) with fixed random state 42 for reproducible benchmarking."),
    ("Step 4: Regression Algorithm Training", "Train candidate models (Linear Regression, Random Forest, Gradient Boosting Regressor) inside scikit-learn Pipeline objects combining preprocessing and estimators."),
    ("Step 5: Model Serialization & Deployment", "Serialize the best-performing pipeline using Joblib into house_price_pipeline.pkl for real-time inference in Streamlit.")
]

for idx, (title, desc) in enumerate(steps):
    y = 2.2 + (idx * 0.96)
    box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(y), Inches(11.7), Inches(0.85))
    box.fill.solid()
    box.fill.fore_color.rgb = LIGHT_BLUE
    box.line.color.rgb = ACCENT_BLUE
    
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_top = Inches(0.1)
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Times New Roman"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ROYAL_BLUE
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = "Times New Roman"
    p2.font.size = Pt(11)
    p2.font.color.rgb = TEXT_DARK

# ============================================================
# SLIDE 7: Model Comparison & Evaluation Leaderboard
# ============================================================
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "Model Evaluation & Performance Leaderboard")

# Left: Performance Table & Key Findings
add_bullet_card(
    s7, 0.8, 2.2, 5.7, 4.7,
    "🏆 Model Benchmark Results",
    [
        "Gradient Boosting Regressor (Winner):\n  • R² Score: 0.9392 (93.92% variance explained)\n  • MAE: ₹ 10.01 Lakhs (Lowest test error)\n  • RMSE: ₹ 13.85 Lakhs",
        "Linear Regression (Baseline):\n  • R² Score: 0.8925 | MAE: ₹ 13.79 Lakhs | RMSE: ₹ 18.42 Lakhs\n  • Solid baseline but struggles with non-linear amenity interactions.",
        "Random Forest Regressor (Ensemble):\n  • R² Score: 0.8467 | MAE: ₹ 15.86 Lakhs | RMSE: ₹ 22.00 Lakhs\n  • Suffered slight variance penalties on smaller sample subsets.",
        "Deployment Decision: Gradient Boosting selected for superior convergence and lowest residual errors."
    ]
)

# Right: Embedded Comparison Chart
if os.path.exists(os.path.join(FIGS_DIR, "fig_model_comparison.png")):
    s7.shapes.add_picture(os.path.join(FIGS_DIR, "fig_model_comparison.png"), Inches(6.8), Inches(2.2), width=Inches(5.7))

# ============================================================
# SLIDE 8: Explainable AI & Feature Importance
# ============================================================
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, "Explainable AI (XAI): Key Feature Weights")

# Left: Feature Importance Chart
if os.path.exists(os.path.join(FIGS_DIR, "fig_feature_importance.png")):
    s8.shapes.add_picture(os.path.join(FIGS_DIR, "fig_feature_importance.png"), Inches(0.8), Inches(2.2), width=Inches(5.7))

# Right: Analysis
add_bullet_card(
    s8, 6.8, 2.2, 5.7, 4.7,
    "🔍 Feature Contribution Insights",
    [
        "Carpet Area (63.56%): The dominant physical valuation driver; unit price scales strongly with square footage.",
        "Metropolitan City Tier (~23% Combined):\n  • Delhi (6.06%), Lucknow (4.63%), Bengaluru (4.56%), Ahmedabad (4.36%), Mumbai (3.29%).\n  • Metro economic status creates massive baseline price differentials.",
        "Property Classification (Villa: 2.37%):\n  • Standalone land ownership and luxury villas command premium pricing over standard high-rise apartments.",
        "Distance to City Center (1.99%):\n  • Peripheral properties trade at a noticeable discount due to commute overhead.",
        "Age of Property (1.50%):\n  • Newer builds trade at premiums; properties >18 years face maintenance discounts."
    ]
)

# ============================================================
# SLIDE 9: System Architecture & Technology Stack
# ============================================================
s9 = prs.slides.add_slide(blank_layout)
add_header(s9, "System Implementation & Technology Stack")

tech_cards = [
    ("Python 3.10+", "Core Language", "High-performance scripting, data handling, and native scientific libraries."),
    ("Scikit-Learn", "Machine Learning", "Pipelines, ColumnTransformer, OneHotEncoder, and GradientBoostingRegressor."),
    ("Streamlit 2.0", "Web Framework", "Interactive reactive dashboard, session-state management, and instant execution."),
    ("Plotly Express", "Interactive Graphics", "Hardware-accelerated gauges, polar radar charts, box plots, and histograms."),
    ("Pandas & NumPy", "Data Manipulation", "Dataset filtering, aggregation, and mathematical vector calculations."),
    ("Custom CSS3", "Design System", "Dark-mode glassmorphic theme, responsive cards, and refined typography.")
]

for idx, (title, cat, desc) in enumerate(tech_cards):
    col = idx % 3
    row = idx // 3
    x = 0.8 + (col * 3.9)
    y = 2.2 + (row * 2.35)
    
    card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(3.7), Inches(2.1))
    card.fill.solid()
    card.fill.fore_color.rgb = LIGHT_BLUE
    card.line.color.rgb = ACCENT_BLUE
    card.line.width = Pt(1.5)
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Times New Roman"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = ROYAL_BLUE
    
    p_c = tf.add_paragraph()
    p_c.text = cat.upper()
    p_c.font.name = "Times New Roman"
    p_c.font.size = Pt(10.5)
    p_c.font.bold = True
    p_c.font.color.rgb = ACCENT_BLUE
    p_c.space_before = Pt(2)
    
    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.name = "Times New Roman"
    p_d.font.size = Pt(12)
    p_d.font.color.rgb = TEXT_DARK
    p_d.space_before = Pt(6)

# ============================================================
# SLIDE 10: Real-World Dashboard: Valuation Studio
# ============================================================
s10 = prs.slides.add_slide(blank_layout)
add_header(s10, "Valuation Studio: Interactive Production Features")

add_bullet_card(
    s10, 0.8, 2.2, 5.7, 4.7,
    "🏠 Valuation Studio Capabilities",
    [
        "1-Click Sample Presets: Load realistic configurations for Mumbai Luxury 3BHK, Bengaluru Tech 2BHK, Jaipur Villa, and Lucknow Budget in one click.",
        "Dual Currency Valuation: Automatically displays market estimates in Lakhs and Crores (e.g., ₹ 1.89 Cr / 188.56 L).",
        "High-Confidence Spread: Computes empirical price bands (±8.5%) based on regression mean absolute error.",
        "Rate per Square Foot: Dynamically benchmarks per-sqft pricing against municipal locality comps.",
        "Input Validation: Enforces physical constraints (e.g., floor number cannot exceed total building floors)."
    ]
)

# Right: UI Banner or Overview
if os.path.exists(BANNER_PATH):
    s10.shapes.add_picture(BANNER_PATH, Inches(6.8), Inches(2.2), width=Inches(5.7))

# ============================================================
# SLIDE 11: Market Intelligence & EDA Studio
# ============================================================
s11 = prs.slides.add_slide(blank_layout)
add_header(s11, "Market Intelligence: Real-Time Data Exploration")

add_bullet_card(
    s11, 0.8, 2.2, 5.7, 4.7,
    "📊 Empirical Market Analytics",
    [
        "Integrated 506-Home Dataset: Exposes full internship dataset directly within the Streamlit web application.",
        "Live Market KPIs: Real-time calculation of Average Market Price (₹ 99.6L), Median (₹ 92.9L), and Max Asset Value (₹ 473.2L).",
        "Amenities Value Premium: Visual bar charts quantifying the price premium added by Swimming Pools, Gyms, Clubhouses, and Power Backups.",
        "Interactive Comp Explorer: Filterable tabular viewer allowing buyers to cross-filter by City, Property Type, and Budget."
    ]
)

add_bullet_card(
    s11, 6.8, 2.2, 5.7, 4.7,
    "⭐ Amenities Valuation Premium",
    [
        "Swimming Pool: Adds an average of +₹ 36.4 Lakhs (+39.8% value premium) in high-density metro communities.",
        "Fitness Gym: Adds +₹ 28.2 Lakhs (+32.1% premium) due to younger demographic tenant demand.",
        "Power Backup: Crucial livability requirement adding +₹ 22.5 Lakhs (+26.4% premium).",
        "Gated 24x7 Security: Standard expectation in Tier-1 cities; non-gated properties face severe illiquidity."
    ]
)

# ============================================================
# SLIDE 12: Key Innovations: AI Advisor & Comparison Studio
# ============================================================
s12 = prs.slides.add_slide(blank_layout)
add_header(s12, "Key Innovations: AI Advisory & Comparison Tool")

add_bullet_card(
    s12, 0.8, 2.2, 5.7, 4.7,
    "🤖 Intelligent AI Buying Advisor",
    [
        "Four Actionable Advice Pillars:\n  1. Core Strengths: Highlights prime location, security, and daylighting.\n  2. Growth Drivers: Identifies metro transit and school corridors.\n  3. Due Diligence Cautions: Flags high crime, elevated AQI, or aging builds.\n  4. Buyer's Negotiation Playbook: Recommends 5–10% discount bids if property has spent >6 months on market.",
        "Target Persona Matching: Automatically assigns recommended investor profile (First-time Buyer, Family End-User, HNW Luxury Seeker)."
    ]
)

add_bullet_card(
    s12, 6.8, 2.2, 5.7, 4.7,
    "⚖️ Side-by-Side Property Comparator",
    [
        "Direct Comps Matching: Evaluate Property Option A vs. Property Option B side-by-side on one screen.",
        "Delta Comparison Metrics: Instant computation of price delta, rate/sqft gap, and property score differential.",
        "Automated Verdict: Data-backed synthesis declaring the higher-value option for long-term capital preservation.",
        "Financial EMI Planner: Interactive mortgage calculator computing down payment, monthly EMI, and total interest outlay."
    ]
)

# ============================================================
# SLIDE 13: Project Limitations & Future Scope
# ============================================================
s13 = prs.slides.add_slide(blank_layout)
add_header(s13, "Limitations & Future Roadmap")

add_bullet_card(
    s13, 0.8, 2.2, 5.7, 4.7,
    "⚠️ Current Project Limitations",
    [
        "Geographic Boundary: Sampled across 10 major Indian metros; expansion needed for Tier-2 and Tier-3 emerging hubs.",
        "Static Transaction Dataset: Relies on periodic batch updates rather than real-time live MLS streaming.",
        "Macroeconomic Rates: Does not currently ingest live RBI repo rate shifts or changing home loan interest cycles automatically.",
        "Physical Inspection Variance: Models cannot evaluate internal interior quality, marble finishes, or woodwork condition."
    ],
    border_color=RGBColor(245, 158, 11)
)

add_bullet_card(
    s13, 6.8, 2.2, 5.7, 4.7,
    "🚀 Future Enhancement Roadmap",
    [
        "Live Real Estate Portal APIs: Integrate real-time scrapers and listing feeds from MagicBricks, 99acres, and Housing.com.",
        "GIS & Satellite Mapping: Incorporate Google Maps Platform APIs for micro-distance routing and topological mapping.",
        "Deep Learning Models: Experiment with Deep Neural Networks and TabNet for complex non-linear feature interactions.",
        "Mobile Application (Flutter): Package into cross-platform iOS & Android mobile apps with camera-based property scanning."
    ],
    border_color=GREEN_ACCENT
)

# ============================================================
# SLIDE 14: Conclusion
# ============================================================
s14 = prs.slides.add_slide(blank_layout)
add_header(s14, "Conclusion & Project Achievements")

concl_box = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.2), Inches(11.7), Inches(4.7))
concl_box.fill.solid()
concl_box.fill.fore_color.rgb = LIGHT_BLUE
concl_box.line.color.rgb = ACCENT_BLUE
concl_box.line.width = Pt(1.5)

tf_c = concl_box.text_frame
tf_c.word_wrap = True
tf_c.margin_left = tf_c.margin_right = Inches(0.35)
tf_c.margin_top = Inches(0.3)

p_c0 = tf_c.paragraphs[0]
p_c0.text = "Summary of Internship Outcomes:"
p_c0.font.name = "Times New Roman"
p_c0.font.size = Pt(18)
p_c0.font.bold = True
p_c0.font.color.rgb = ROYAL_BLUE

points = [
    "High-Precision ML Predictive Engine: Built and validated a Gradient Boosting Regressor achieving 93.92% R² accuracy, significantly outperforming Linear Regression and Random Forest baselines.",
    "Comprehensive 34-Feature Domain Modeling: Bridged physical dimensions with societal, environmental, and connectivity indicators to eliminate subjective broker bias.",
    "Objective Property Health Scoring: Invented a 4-pillar 100-point livability index providing actionable clarity to home buyers.",
    "Commercial-Grade User Experience: Transformed raw research into an interactive, multi-tab, glassmorphic Streamlit application with live mortgage planning and report export.",
    "Academic Fulfillment: Successfully met all curriculum and research deliverables for the AIML Summer Internship 2026 at IIHMF, MNNIT Prayagraj and UCER AKTU."
]

for pt in points:
    p = tf_c.add_paragraph()
    p.text = f"✅  {pt}"
    p.font.name = "Times New Roman"
    p.font.size = Pt(14)
    p.font.color.rgb = TEXT_DARK
    p.space_before = Pt(14)

# ============================================================
# SLIDE 15: References & Acknowledgments
# ============================================================
s15 = prs.slides.add_slide(blank_layout)
add_header(s15, "References & Acknowledgments")

add_bullet_card(
    s15, 0.8, 2.2, 5.7, 4.7,
    "📚 Academic & Technical References",
    [
        "Scikit-Learn: Machine Learning in Python, Pedregosa et al., JMLR 12, pp. 2825-2830, 2011.",
        "Gradient Boosting Machines, Jerome H. Friedman, The Annals of Statistics, Vol. 29, No. 5, 2001.",
        "Streamlit Open-Source Framework: Deploying Machine Learning Applications, 2026.",
        "Plotly Technologies Inc.: Collaborative Data Visualization, Montreal, QC, 2026.",
        "Housing Price Indices in Indian Metros: National Housing Bank (NHB RESIDEX) Reports."
    ]
)

add_bullet_card(
    s15, 6.8, 2.2, 5.7, 4.7,
    "🙏 Institutional Acknowledgments",
    [
        "IIHMF, MNNIT Prayagraj: For hosting the AIML Summer Internship 2026 and providing technical guidance under Project Coordinator Arpit Dubey.",
        "Dr. Divya Kumar (Project Supervisor, MNNIT Prayagraj): For invaluable mentorship, architectural feedback, and rigorous academic oversight.",
        "United College of Engineering & Research (UCER), Prayagraj: Department of Computer Science & Engineering (AI & ML).",
        "Dr. A.P.J. Abdul Kalam Technical University (AKTU), Lucknow: For the comprehensive B.Tech engineering curriculum."
    ]
)

# Save Presentation
prs.save(OUTPUT_PPTX)
print(f"Presentation saved successfully to: {OUTPUT_PPTX}")
