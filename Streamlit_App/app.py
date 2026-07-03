# ============================================================
#               HomeWorth AI v1.0
#        Smart House Price Prediction Platform
# ============================================================

import streamlit as st
import os
import base64

# Backend
from predictor import predict_price
from advisor import generate_advice
from utils import (
    format_price,
    property_score,
    investment_rating,
    market_category,
    confidence_score
)

# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="HomeWorth AI",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# Load CSS
# ============================================================

CURRENT_DIR = os.path.dirname(__file__)

css_path = os.path.join(CURRENT_DIR, "style.css")

with open(css_path) as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ============================================================
# Helper Function
# ============================================================

def image_to_base64(path):
    with open(path, "rb") as image:
        return base64.b64encode(image.read()).decode()

# ============================================================
# Load Hero Banner
# ============================================================

banner_path = os.path.join(
    CURRENT_DIR,
    "assets",
    "hero_banner.png"
)

banner = image_to_base64(banner_path)

# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.markdown("# 🏡 HomeWorth AI")

    st.markdown("---")

    st.success("🟢 Model Ready")

    st.metric(
        "Model Accuracy",
        "93.91%"
    )

    st.metric(
        "Algorithm",
        "Gradient Boosting"
    )

    st.markdown("---")

    st.markdown(
        """
### 🚀 Features

- AI Price Prediction

- Investment Analysis

- Property Score

- AI Buying Advisor

- Premium Dashboard
"""
    )

    st.markdown("---")

    st.caption("Version 1.0")

# ============================================================
# HERO SECTION
# ============================================================

left, right = st.columns([1.2,1])

with left:

    st.markdown(
        """
<div class="badge">
🤖 AI Powered
</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="main-title">

Home<span class="gradient">Worth</span> AI

</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="subtitle">

Predict accurate house prices using Machine Learning.

Get intelligent investment insights, property evaluation,
and AI-powered buying recommendations instantly.

</div>
""",
        unsafe_allow_html=True
    )

    st.markdown("")

    c1,c2,c3 = st.columns(3)

    with c1:
        st.markdown(
            '<div class="pill">🎯 Accurate Prediction</div>',
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            '<div class="pill">📈 Investment Analysis</div>',
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            '<div class="pill">🤖 AI Advisor</div>',
            unsafe_allow_html=True
        )

with right:

    st.markdown(
        f"""
<div class="hero glow">

<img
src="data:image/png;base64,{banner}"
style="width:100%;
border-radius:18px;">

</div>
""",
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# DASHBOARD OVERVIEW
# ============================================================

st.markdown(
    """
<h2 class="section-title">
📊 Dashboard Overview
</h2>
""",
    unsafe_allow_html=True
)

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.markdown("""
<div class="metric-card glow">
<h3>🏙️</h3>
<h2>10</h2>
<p>Cities</p>
</div>
""", unsafe_allow_html=True)

with metric2:
    st.markdown("""
<div class="metric-card glow">
<h3>🏠</h3>
<h2>4</h2>
<p>Property Types</p>
</div>
""", unsafe_allow_html=True)

with metric3:
    st.markdown("""
<div class="metric-card glow">
<h3>🎯</h3>
<h2>93.91%</h2>
<p>Accuracy</p>
</div>
""", unsafe_allow_html=True)

with metric4:
    st.markdown("""
<div class="metric-card glow">
<h3>🤖</h3>
<h2>AI</h2>
<p>Powered</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# PROPERTY LOCATION
# ============================================================

st.markdown("""
<div class="glass">
<h2 class="section-title">
📍 Property Location
</h2>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:

    city = st.selectbox(
        "City",
        [
            "Ahmedabad",
            "Bengaluru",
            "Chennai",
            "Delhi",
            "Hyderabad",
            "Jaipur",
            "Kolkata",
            "Lucknow",
            "Mumbai",
            "Pune"
        ]
    )

    locality = st.selectbox(
        "Locality",
        [
            "Civil Lines",
            "Green Park",
            "Hill View",
            "Lake View",
            "MG Road",
            "New Extension",
            "Old Town",
            "Riverside",
            "Sector 12",
            "Tech Park Road"
        ]
    )

with col2:

    locality_type = st.selectbox(
        "Locality Type",
        [
            "Urban",
            "Suburban",
            "Rural"
        ]
    )

    property_type = st.selectbox(
        "Property Type",
        [
            "Apartment",
            "Builder Floor",
            "Independent House",
            "Villa"
        ]
    )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# PROPERTY DETAILS
# ============================================================

st.markdown("""
<div class="glass">
<h2 class="section-title">
🏠 Property Details
</h2>
""", unsafe_allow_html=True)

left_col, right_col = st.columns(2)

with left_col:

    area = st.number_input(
        "📐 Area (sq.ft.)",
        min_value=300,
        max_value=10000,
        value=1200,
        step=50
    )

    bedrooms = st.number_input(
        "🛏 Bedrooms",
        min_value=1,
        max_value=10,
        value=3
    )

    bathrooms = st.number_input(
        "🚿 Bathrooms",
        min_value=1,
        max_value=10,
        value=2
    )

    balconies = st.number_input(
        "🌅 Balconies",
        min_value=0,
        max_value=5,
        value=1
    )

with right_col:

    floor = st.number_input(
        "🏢 Preferred Floor",
        min_value=0,
        max_value=60,
        value=3
    )

    total_floors = st.number_input(
        "🏗 Total Floors",
        min_value=1,
        max_value=60,
        value=10
    )

    age = st.number_input(
        "🏚 Property Age",
        min_value=0,
        max_value=100,
        value=5
    )

    furnishing = st.selectbox(
        "🛋 Furnishing",
        [
            "Fully-Furnished",
            "Semi-Furnished",
            "Unfurnished"
        ]
    )

    facing = st.selectbox(
        "🧭 House Facing",
        [
            "East",
            "North",
            "North-East",
            "South",
            "South-West",
            "West"
        ]
    )

    parking = st.number_input(
        "🚗 Parking Spaces",
        min_value=0,
        max_value=5,
        value=1
    )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# NEIGHBOURHOOD DETAILS
# ============================================================

st.markdown(
    """
<h2 class="section-title">
🌍 Neighbourhood & Environment
</h2>
""",
    unsafe_allow_html=True,
)

with st.container():

    left_col, right_col = st.columns(2)

    with left_col:

        distance = st.number_input(
            "📍 Distance to City Center (km)",
            min_value=0.0,
            max_value=100.0,
            value=6.0,
            step=0.5,
        )

        schools = st.number_input(
            "🏫 Nearby Schools",
            min_value=0,
            max_value=20,
            value=4,
        )

        hospitals = st.number_input(
            "🏥 Nearby Hospitals",
            min_value=0,
            max_value=20,
            value=3,
        )

    with right_col:

        transport = st.selectbox(
            "🚌 Public Transport",
            [
                "High",
                "Medium",
                "Low",
            ],
        )

        crime = st.slider(
            "🚔 Crime Rate Index",
            0,
            100,
            25,
        )

        air_quality = st.slider(
            "🌿 Air Quality Index",
            0,
            300,
            60,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# AMENITIES
# ============================================================

st.markdown(
    """
<h2 class="section-title">
⭐ Property Amenities
</h2>
""",
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3)

with c1:

    has_lift = st.checkbox("🛗 Lift", value=True)

    has_security = st.checkbox("🛡 Security", value=True)

    has_gym = st.checkbox("🏋 Gym", value=True)

with c2:

    has_pool = st.checkbox("🏊 Swimming Pool")

    has_garden = st.checkbox("🌳 Garden", value=True)

with c3:

    has_backup = st.checkbox("⚡ Power Backup", value=True)

    has_clubhouse = st.checkbox("🏛 Clubhouse")

amenities_score = st.slider(
    "⭐ Overall Amenities Score",
    0,
    10,
    8,
)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# PREDICT BUTTON
# ============================================================

predict_clicked = st.button(
    "✨ Predict House Price",
    use_container_width=True,
)

# ============================================================
# BUILD USER INPUT
# ============================================================

user_input = {

    "City": city,

    "Locality": locality,

    "Locality_Type": locality_type,

    "Property_Type": property_type,

    "Area_sqft": area,

    "Bedrooms": bedrooms,

    "Bathrooms": bathrooms,

    "Balconies": balconies,

    "Floor_No": floor,

    "Total_Floors": total_floors,

    "Age_of_Property_Years": age,

    "Furnishing_Status": furnishing,

    "Parking_Spaces": parking,

    "Facing": facing,

    "Distance_to_City_Center_km": distance,

    "Nearby_Schools_Count": schools,

    "Nearby_Hospitals_Count": hospitals,

    "Public_Transport_Access": transport,

    "Crime_Rate_Index": crime,

    "Air_Quality_Index": air_quality,

    "Has_Lift": int(has_lift),

    "Has_Security": int(has_security),

    "Has_Gym": int(has_gym),

    "Has_Swimming_Pool": int(has_pool),

    "Has_Garden": int(has_garden),

    "Has_Power_Backup": int(has_backup),

    "Has_Clubhouse": int(has_clubhouse),

    "Amenities_Score": amenities_score,

    "Ownership_Type": "Freehold",

    "Transaction_Type": "Resale",

    "Listing_Type": "Broker",

    "Months_on_Market": 2
}

# ============================================================
# PREDICTION ENGINE
# ============================================================

prediction = None
score = None
rating = None
category = None
advice = None

if predict_clicked:

    with st.spinner("🤖 HomeWorth AI is analysing your property..."):

        status = st.empty()

        status.info("📍 Analysing location...")
        prediction = predict_price(user_input)

        status.info("📊 Calculating property score...")
        score = property_score(user_input)

        status.info("📈 Evaluating investment quality...")
        rating = investment_rating(score)

        status.info("🏷 Classifying market category...")
        category = market_category(prediction)

        status.info("🤖 Generating AI recommendations...")
        advice = generate_advice(
            user_input,
            prediction
        )

        status.success("✅ Analysis Completed Successfully!")

    st.balloons()

    st.markdown("<br>", unsafe_allow_html=True)



# ============================================================
# RESULT HEADER
# ============================================================

if prediction is not None:

    st.markdown(
        """
<h2 class="section-title">
📊 Prediction Result
</h2>
""",
        unsafe_allow_html=True,
    )

# ============================================================
# MAIN RESULT CARD
# ============================================================

st.markdown(
    f"""
<div class="result-card">

<div class="result-title">
Estimated Market Value
</div>

<div class="result-price">
{format_price(prediction)}
</div>

</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# METRICS
# ============================================================

m1, m2, m3 = st.columns(3)

with m1:

    st.metric(
        "⭐ Property Score",
        f"{score}/100"
    )

with m2:

    st.metric(
        "📈 Investment Rating",
        rating
    )

with m3:

    st.metric(
        "🏷 Market Category",
        category
    )

confidence = confidence_score(score)

st.markdown("### 🎯 Prediction Confidence")

st.progress(confidence / 100)

st.success(f"Model Confidence: {confidence}%")

st.markdown("### 🏆 Property Highlights")

highlights = []

if amenities_score >= 8:
    highlights.append("⭐ Premium Amenities")

if crime <= 30:
    highlights.append("🛡 Safe Locality")

if air_quality <= 80:
    highlights.append("🌿 Healthy Environment")

if schools >= 4:
    highlights.append("🏫 Excellent Schools Nearby")

if hospitals >= 3:
    highlights.append("🏥 Good Healthcare Access")

if distance <= 8:
    highlights.append("📍 Close to City Center")

if parking >= 2:
    highlights.append("🚗 Spacious Parking")

if has_security:
    highlights.append("🔒 24×7 Security")

if has_lift:
    highlights.append("🛗 Lift Available")

col1, col2 = st.columns(2)

for i, item in enumerate(highlights):
    if i % 2 == 0:
        col1.success(item)
    else:
        col2.success(item)



st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# AI ADVISOR
# ============================================================

st.markdown(
    """
<h2 class="section-title">
🤖 AI House Buying Advisor
</h2>
""",
    unsafe_allow_html=True,
)

for tip in advice:

    st.markdown(
        f"""
<div class="ai-card">

{tip}

</div>
""",
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# PROPERTY SUMMARY
# ============================================================

st.markdown(
    """
<h2 class="section-title">
🏡 Property Summary
</h2>
""",
    unsafe_allow_html=True,
)

summary1, summary2 = st.columns(2)

with summary1:

    st.info(f"📍 Location : {city}, {locality}")

    st.info(f"🏠 Property Type : {property_type}")

    st.info(f"🧭 Facing : {facing}")

    st.info(f"📐 Area : {area} sqft")

with summary2:

    st.info(f"🛏 Bedrooms : {bedrooms}")

    st.info(f"🚿 Bathrooms : {bathrooms}")

    st.info(f"🚗 Parking : {parking}")

    st.info(f"⭐ Amenities Score : {amenities_score}/10")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
"""
<div class="footer">

🏡 <b>HomeWorth AI v1.0</b>

<br><br>

Developed using

Python • Streamlit • Scikit-Learn • Gradient Boosting

<br><br>

AIML Summer Internship Project 2026

</div>
""",
unsafe_allow_html=True
)