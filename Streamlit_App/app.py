# ============================================================
#               HomeWorth AI - Production Edition
#     Next-Gen AI Residential Valuation & Real Estate Analytics
#      AIML Summer Internship Project 2026 @ IIHMF, MNNIT Prayagraj
# ============================================================

import os
import base64
import json
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Local Modules
from predictor import (
    predict_price,
    predict_price_range,
    get_model_benchmark_metrics,
    get_feature_importances
)
from advisor import generate_structured_advice
from utils import (
    format_price,
    property_score,
    get_property_subscores,
    investment_rating,
    market_category,
    confidence_score,
    calculate_emi,
    load_market_dataset,
    generate_property_report_text
)

# ============================================================
# Page Configuration
# ============================================================
st.set_page_config(
    page_title="HomeWorth AI — Smart Property Valuation & Analytics",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# Load Custom Stylesheet
# ============================================================
CURRENT_DIR = os.path.dirname(__file__)
css_path = os.path.join(CURRENT_DIR, "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Helper: image to base64
def image_to_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image:
            return base64.b64encode(image.read()).decode()
    return ""

banner_path = os.path.join(CURRENT_DIR, "assets", "hero_banner.png")
banner_b64 = image_to_base64(banner_path)

# ============================================================
# Pre-defined Presets for 1-Click Evaluation
# ============================================================
PRESETS = {
    "Custom": None,
    "🌆 Mumbai Luxury 3BHK (South)": {
        "City": "Mumbai", "Locality": "Green Park", "Locality_Type": "Urban", "Property_Type": "Apartment",
        "Area_sqft": 1850, "Bedrooms": 3, "Bathrooms": 3, "Balconies": 2, "Floor_No": 12, "Total_Floors": 25,
        "Age_of_Property_Years": 3, "Furnishing_Status": "Fully-Furnished", "Facing": "North-East", "Parking_Spaces": 2,
        "Distance_to_City_Center_km": 4.5, "Nearby_Schools_Count": 5, "Nearby_Hospitals_Count": 4,
        "Public_Transport_Access": "High", "Crime_Rate_Index": 20, "Air_Quality_Index": 55,
        "Has_Lift": 1, "Has_Security": 1, "Has_Gym": 1, "Has_Swimming_Pool": 1, "Has_Garden": 1,
        "Has_Power_Backup": 1, "Has_Clubhouse": 1, "Amenities_Score": 9,
        "Ownership_Type": "Freehold", "Transaction_Type": "Resale", "Listing_Type": "Broker", "Months_on_Market": 1
    },
    "🚀 Bengaluru Tech 2BHK (Whitefield)": {
        "City": "Bengaluru", "Locality": "Tech Park Road", "Locality_Type": "Urban", "Property_Type": "Apartment",
        "Area_sqft": 1250, "Bedrooms": 2, "Bathrooms": 2, "Balconies": 1, "Floor_No": 6, "Total_Floors": 14,
        "Age_of_Property_Years": 2, "Furnishing_Status": "Semi-Furnished", "Facing": "East", "Parking_Spaces": 1,
        "Distance_to_City_Center_km": 8.0, "Nearby_Schools_Count": 4, "Nearby_Hospitals_Count": 3,
        "Public_Transport_Access": "High", "Crime_Rate_Index": 22, "Air_Quality_Index": 48,
        "Has_Lift": 1, "Has_Security": 1, "Has_Gym": 1, "Has_Swimming_Pool": 0, "Has_Garden": 1,
        "Has_Power_Backup": 1, "Has_Clubhouse": 1, "Amenities_Score": 8,
        "Ownership_Type": "Freehold", "Transaction_Type": "New Booking", "Listing_Type": "Owner", "Months_on_Market": 2
    },
    "🏰 Jaipur Royal 4BHK Villa": {
        "City": "Jaipur", "Locality": "Hill View", "Locality_Type": "Suburban", "Property_Type": "Villa",
        "Area_sqft": 3100, "Bedrooms": 4, "Bathrooms": 4, "Balconies": 3, "Floor_No": 2, "Total_Floors": 2,
        "Age_of_Property_Years": 1, "Furnishing_Status": "Fully-Furnished", "Facing": "North-East", "Parking_Spaces": 3,
        "Distance_to_City_Center_km": 11.0, "Nearby_Schools_Count": 3, "Nearby_Hospitals_Count": 2,
        "Public_Transport_Access": "Medium", "Crime_Rate_Index": 18, "Air_Quality_Index": 40,
        "Has_Lift": 0, "Has_Security": 1, "Has_Gym": 1, "Has_Swimming_Pool": 1, "Has_Garden": 1,
        "Has_Power_Backup": 1, "Has_Clubhouse": 1, "Amenities_Score": 9,
        "Ownership_Type": "Freehold", "Transaction_Type": "New Booking", "Listing_Type": "Owner", "Months_on_Market": 3
    },
    "💚 Lucknow Budget 2BHK (Gomti Nagar)": {
        "City": "Lucknow", "Locality": "Riverside", "Locality_Type": "Urban", "Property_Type": "Apartment",
        "Area_sqft": 950, "Bedrooms": 2, "Bathrooms": 2, "Balconies": 1, "Floor_No": 4, "Total_Floors": 8,
        "Age_of_Property_Years": 6, "Furnishing_Status": "Semi-Furnished", "Facing": "East", "Parking_Spaces": 1,
        "Distance_to_City_Center_km": 6.5, "Nearby_Schools_Count": 3, "Nearby_Hospitals_Count": 2,
        "Public_Transport_Access": "Medium", "Crime_Rate_Index": 30, "Air_Quality_Index": 72,
        "Has_Lift": 1, "Has_Security": 1, "Has_Gym": 0, "Has_Swimming_Pool": 0, "Has_Garden": 1,
        "Has_Power_Backup": 1, "Has_Clubhouse": 0, "Amenities_Score": 6,
        "Ownership_Type": "Freehold", "Transaction_Type": "Resale", "Listing_Type": "Owner", "Months_on_Market": 4
    }
}

# ============================================================
# Session State Initialization
# ============================================================
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

if "preset_selected" not in st.session_state:
    st.session_state.preset_selected = "Custom"

# ============================================================
# Sidebar Configuration & Brand Context
# ============================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        🏡 <span>HomeWorth AI</span>
    </div>
    <div class="sidebar-badge">Production v2.0 • AI ML</div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-card">
        <div style="font-size:12px; color:#94a3b8; text-transform:uppercase; font-weight:600;">Engine Status</div>
        <div style="font-size:16px; font-weight:700; color:#10b981; margin-top:2px;">🟢 Production Ready</div>
        <div style="font-size:13px; color:#cbd5e1; margin-top:6px;"><b>Algorithm:</b> Gradient Boosting</div>
        <div style="font-size:13px; color:#cbd5e1;"><b>Model R²:</b> 93.92%</div>
        <div style="font-size:13px; color:#cbd5e1;"><b>MAE:</b> ₹ 10.01 Lakhs</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚡ Quick Presets")
    preset_choice = st.selectbox(
        "Load Sample Property:",
        options=list(PRESETS.keys()),
        index=list(PRESETS.keys()).index(st.session_state.preset_selected),
        key="sidebar_preset_selector"
    )
    if preset_choice != st.session_state.preset_selected:
        st.session_state.preset_selected = preset_choice
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="font-size:13px; color:#94a3b8; line-height:1.6;">
        <b>Internship Project 2026</b><br>
        IIHMF, MNNIT Prayagraj<br>
        Developed by:<br>
        • <b>Ujjaval Kumar Kesarwani</b><br>
        • <b>Shlok Tiwari</b>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# MAIN APPLICATION INTERFACE (Tabs Navigation)
# ============================================================
tab_val, tab_market, tab_compare, tab_xai, tab_about = st.tabs([
    "🏠 Valuation Studio",
    "📊 Market Intelligence & EDA",
    "⚖️ Property Comparison",
    "🧠 Model Intelligence & XAI",
    "ℹ️ Documentation & Team"
])

# Load preset defaults if active
current_preset = PRESETS.get(st.session_state.preset_selected)

# ============================================================
# TAB 1: VALUATION STUDIO
# ============================================================
with tab_val:
    # Hero Showcase
    hero_img_html = ""
    if banner_b64:
        hero_img_html = f"""
        <div style="text-align:center;">
            <img src="data:image/png;base64,{banner_b64}" style="width:100%; max-height:220px; object-fit:cover; border-radius:18px; box-shadow:0 12px 30px rgba(0,0,0,0.5);">
        </div>
        """

    st.markdown(f"""
    <div class="hero-wrapper">
        <div class="hero-tag">✨ AI-Powered Real Estate Valuation • 93.92% Accuracy</div>
        <div class="hero-title">Home<span class="gradient-text">Worth</span> AI Studio</div>
        <div class="hero-desc">
            Instantly evaluate residential market value, price per square foot, investment quality grade, and actionable buyer negotiation advice using trained machine learning models.
        </div>
        <div class="hero-stats-row">
            <span class="hero-pill">🏙️ 10 Major Indian Metros</span>
            <span class="hero-pill">🎯 Gradient Boosting Regressor</span>
            <span class="hero-pill">⭐ Multi-Pillar Livability Score</span>
            <span class="hero-pill">🤖 Automated Buying Advisor</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Input Form Layout in Grid Containers
    st.markdown("### 📝 Enter Property Specifications")

    col_loc, col_spec = st.columns([1, 1], gap="medium")

    # Column 1: Location & Property Profile
    with col_loc:
        st.markdown("""<div class="glass-card"><div class="card-title">📍 Location & Profile</div>""", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        cities = ["Ahmedabad", "Bengaluru", "Chennai", "Delhi", "Hyderabad", "Jaipur", "Kolkata", "Lucknow", "Mumbai", "Pune"]
        def_city = current_preset["City"] if current_preset else "Mumbai"
        city = c1.selectbox("City", cities, index=cities.index(def_city) if def_city in cities else 0)

        localities = ["Civil Lines", "Green Park", "Hill View", "Lake View", "MG Road", "New Extension", "Old Town", "Riverside", "Sector 12", "Tech Park Road"]
        def_loc = current_preset["Locality"] if current_preset else "Green Park"
        locality = c2.selectbox("Locality", localities, index=localities.index(def_loc) if def_loc in localities else 0)

        c3, c4 = st.columns(2)
        loc_types = ["Urban", "Suburban", "Rural"]
        def_loctype = current_preset["Locality_Type"] if current_preset else "Urban"
        locality_type = c3.selectbox("Locality Classification", loc_types, index=loc_types.index(def_loctype) if def_loctype in loc_types else 0)

        prop_types = ["Apartment", "Builder Floor", "Independent House", "Villa"]
        def_proptype = current_preset["Property_Type"] if current_preset else "Apartment"
        property_type = c4.selectbox("Property Type", prop_types, index=prop_types.index(def_proptype) if def_proptype in prop_types else 0)

        c5, c6 = st.columns(2)
        own_types = ["Freehold", "Leasehold", "Co-operative Society"]
        def_own = current_preset["Ownership_Type"] if current_preset else "Freehold"
        ownership_type = c5.selectbox("Ownership Title", own_types, index=own_types.index(def_own) if def_own in own_types else 0)

        trans_types = ["Resale", "New Booking"]
        def_trans = current_preset["Transaction_Type"] if current_preset else "Resale"
        transaction_type = c6.selectbox("Transaction Type", trans_types, index=trans_types.index(def_trans) if def_trans in trans_types else 0)

        st.markdown("</div>", unsafe_allow_html=True)

    # Column 2: Physical Layout & Architecture
    with col_spec:
        st.markdown("""<div class="glass-card"><div class="card-title">📐 Physical Dimensions & Structure</div>""", unsafe_allow_html=True)

        c7, c8 = st.columns(2)
        def_area = current_preset["Area_sqft"] if current_preset else 1250
        area = c7.number_input("Carpet Area (sq.ft.)", min_value=300, max_value=12000, value=def_area, step=50)

        def_bhk = current_preset["Bedrooms"] if current_preset else 3
        bedrooms = c8.number_input("Bedrooms (BHK)", min_value=1, max_value=10, value=def_bhk)

        c9, c10 = st.columns(2)
        def_baths = current_preset["Bathrooms"] if current_preset else 2
        bathrooms = c9.number_input("Bathrooms", min_value=1, max_value=8, value=def_baths)

        def_balc = current_preset["Balconies"] if current_preset else 1
        balconies = c10.number_input("Balconies", min_value=0, max_value=6, value=def_balc)

        c11, c12 = st.columns(2)
        def_totfloors = current_preset["Total_Floors"] if current_preset else 12
        total_floors = c12.number_input("Building Total Floors", min_value=1, max_value=60, value=def_totfloors)

        def_floor = current_preset["Floor_No"] if current_preset else 3
        floor = c11.number_input("Property Floor", min_value=0, max_value=int(total_floors), value=min(def_floor, int(total_floors)))

        c13, c14 = st.columns(2)
        def_age = current_preset["Age_of_Property_Years"] if current_preset else 4
        age = c13.number_input("Age of Property (Years)", min_value=0, max_value=80, value=def_age)

        furnish_opts = ["Fully-Furnished", "Semi-Furnished", "Unfurnished"]
        def_furnish = current_preset["Furnishing_Status"] if current_preset else "Semi-Furnished"
        furnishing = c14.selectbox("Furnishing Status", furnish_opts, index=furnish_opts.index(def_furnish) if def_furnish in furnish_opts else 1)

        c15, c16 = st.columns(2)
        facing_opts = ["East", "North-East", "North", "West", "South", "South-West"]
        def_facing = current_preset["Facing"] if current_preset else "East"
        facing = c15.selectbox("House Facing Orientation", facing_opts, index=facing_opts.index(def_facing) if def_facing in facing_opts else 0)

        def_parking = current_preset["Parking_Spaces"] if current_preset else 1
        parking = c16.number_input("Reserved Parking Spots", min_value=0, max_value=5, value=def_parking)

        st.markdown("</div>", unsafe_allow_html=True)

    # Row 2: Environment, Infrastructure & Amenities
    col_env, col_amen = st.columns([1, 1], gap="medium")

    with col_env:
        st.markdown("""<div class="glass-card"><div class="card-title">🌍 Neighbourhood & Environment</div>""", unsafe_allow_html=True)
        
        e1, e2 = st.columns(2)
        def_dist = float(current_preset["Distance_to_City_Center_km"]) if current_preset else 6.0
        distance = e1.number_input("Distance to City Center (km)", min_value=0.2, max_value=80.0, value=def_dist, step=0.5)

        transit_opts = ["High", "Medium", "Low"]
        def_transit = current_preset["Public_Transport_Access"] if current_preset else "High"
        transport = e2.selectbox("Public Transport Connectivity", transit_opts, index=transit_opts.index(def_transit) if def_transit in transit_opts else 0)

        e3, e4 = st.columns(2)
        def_schools = current_preset["Nearby_Schools_Count"] if current_preset else 4
        schools = e3.number_input("Schools Within 3 km", min_value=0, max_value=20, value=def_schools)

        def_hosp = current_preset["Nearby_Hospitals_Count"] if current_preset else 3
        hospitals = e4.number_input("Hospitals Within 5 km", min_value=0, max_value=20, value=def_hosp)

        e5, e6 = st.columns(2)
        def_crime = current_preset["Crime_Rate_Index"] if current_preset else 25
        crime = e5.slider("Local Crime Rate Index (0-100)", min_value=0, max_value=100, value=def_crime, help="Lower index indicates higher security")

        def_aqi = current_preset["Air_Quality_Index"] if current_preset else 55
        air_quality = e6.slider("Air Quality Index (AQI)", min_value=0, max_value=300, value=def_aqi, help="Lower values mean cleaner air")

        def_months = current_preset["Months_on_Market"] if current_preset else 2
        months_market = st.slider("Listing Duration (Months on Market)", min_value=1, max_value=24, value=def_months)

        st.markdown("</div>", unsafe_allow_html=True)

    with col_amen:
        st.markdown("""<div class="glass-card"><div class="card-title">⭐ Society Amenities & Infrastructure</div>""", unsafe_allow_html=True)

        a1, a2, a3 = st.columns(3)
        def_lift = bool(current_preset["Has_Lift"]) if current_preset else True
        has_lift = a1.checkbox("🛗 High-Speed Lift", value=def_lift)

        def_sec = bool(current_preset["Has_Security"]) if current_preset else True
        has_security = a2.checkbox("🛡️ 24x7 Security", value=def_sec)

        def_gym = bool(current_preset["Has_Gym"]) if current_preset else True
        has_gym = a3.checkbox("🏋️ Fitness Gym", value=def_gym)

        a4, a5, a6 = st.columns(3)
        def_pool = bool(current_preset["Has_Swimming_Pool"]) if current_preset else False
        has_pool = a4.checkbox("🏊 Swimming Pool", value=def_pool)

        def_garden = bool(current_preset["Has_Garden"]) if current_preset else True
        has_garden = a5.checkbox("🌳 Landscaped Park", value=def_garden)

        def_backup = bool(current_preset["Has_Power_Backup"]) if current_preset else True
        has_backup = a6.checkbox("⚡ 100% Power Backup", value=def_backup)

        has_clubhouse = st.checkbox("🏛️ Residents Clubhouse & Lounge", value=bool(current_preset["Has_Clubhouse"]) if current_preset else False)

        def_amscore = current_preset["Amenities_Score"] if current_preset else 8
        amenities_score = st.slider("Overall Amenities Rating (0-10)", min_value=0, max_value=10, value=def_amscore)

        st.markdown("</div>", unsafe_allow_html=True)

    # Build input payload
    user_payload = {
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
        "Ownership_Type": ownership_type,
        "Transaction_Type": transaction_type,
        "Listing_Type": "Broker",
        "Months_on_Market": months_market
    }

    # Action Trigger
    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("✨ Calculate Instant AI Valuation & Full Investment Report", use_container_width=True)

    if predict_btn:
        with st.spinner("🤖 HomeWorth AI engine is analyzing market comparables & estimating value..."):
            pred_val = predict_price(user_payload)
            low_val, high_val = predict_price_range(pred_val)
            score_val = property_score(user_payload)
            subscores = get_property_subscores(user_payload)
            rating_val = investment_rating(score_val)
            cat_val = market_category(pred_val)
            conf_val = confidence_score(score_val)
            advice_dict = generate_structured_advice(user_payload, pred_val)
            
            # Save to session state
            st.session_state.prediction_result = {
                "user_payload": user_payload,
                "price": pred_val,
                "range": (low_val, high_val),
                "score": score_val,
                "subscores": subscores,
                "rating": rating_val,
                "category": cat_val,
                "confidence": conf_val,
                "advice": advice_dict
            }
        st.toast("✅ Property valuation generated successfully!", icon="🏡")

    # ============================================================
    # RENDER PREDICTION RESULTS (CRITICAL FIX: Check State!)
    # ============================================================
    if st.session_state.prediction_result is not None:
        res = st.session_state.prediction_result
        price = res["price"]
        low, high = res["range"]
        score = res["score"]
        rating = res["rating"]
        cat = res["category"]
        conf = res["confidence"]
        sub = res["subscores"]
        advice = res["advice"]
        payload = res["user_payload"]
        
        area_sq = payload["Area_sqft"]
        rate_sqft = round((price * 100000.0) / area_sq, 0) if area_sq > 0 else 0

        st.markdown("---")
        st.markdown("## 📊 Valuation & Investment Analysis Results")

        # Top Hero Card
        st.markdown(f"""
        <div class="result-hero">
            <div class="result-eyebrow">AI-Estimated Fair Market Value</div>
            <div class="result-main-price">{format_price(price)}</div>
            <div class="result-range-badge">
                🎯 Expected Valuation Range: <b>₹ {low:,.2f} L</b> – <b>₹ {high:,.2f} L</b> (±8.5% Confidence)
            </div>
            <div style="margin-top:14px; font-size:15px; color:#dbeafe;">
                Benchmark Rate: <b>₹ {rate_sqft:,.0f} / sq.ft.</b> • {payload['City']} ({payload['Locality']})
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 4 Key Metrics Bar
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">🏆</div>
                <div class="kpi-value">{score}<span style="font-size:16px; color:#94a3b8;">/100</span></div>
                <div class="kpi-label">Property Score</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">📈</div>
                <div class="kpi-value" style="font-size:20px; padding-top:6px;">{rating.split(' ')[1]}</div>
                <div class="kpi-label">{rating.split(' ')[0]} Grade</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">🏷️</div>
                <div class="kpi-value" style="font-size:18px; padding-top:8px;">{cat.split(' ')[0]}</div>
                <div class="kpi-label">Market Bracket</div>
            </div>
            """, unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">🎯</div>
                <div class="kpi-value">{conf}%</div>
                <div class="kpi-label">Algorithm Confidence</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Visual Scorecard & Health Radar
        vis_col1, vis_col2 = st.columns([1, 1], gap="medium")

        with vis_col1:
            st.markdown("""<div class="glass-card"><div class="card-title">📈 Property Quality Score Breakdown</div>""", unsafe_allow_html=True)
            
            # Gauge chart for overall score
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Composite Property Score", 'font': {'size': 18, 'color': '#ffffff'}},
                number={'suffix': "/100", 'font': {'size': 26, 'color': '#ffffff'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94a3b8"},
                    'bar': {'color': "#3b82f6", 'thickness': 0.28},
                    'bgcolor': "rgba(15, 23, 42, 0.6)",
                    'borderwidth': 1,
                    'bordercolor': "rgba(255,255,255,0.1)",
                    'steps': [
                        {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.25)'},
                        {'range': [50, 75], 'color': 'rgba(245, 158, 11, 0.25)'},
                        {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.25)'}
                    ]
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=260,
                margin=dict(l=20, r=20, t=40, b=10)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with vis_col2:
            st.markdown("""<div class="glass-card"><div class="card-title">🕸️ 4-Pillar Real Estate Radar</div>""", unsafe_allow_html=True)
            
            categories = ['Location & Transit', 'Specs & Layout', 'Society Amenities', 'Safety & Environment']
            values = [sub['location'], sub['specs'], sub['amenities'], sub['environment']]
            # Close the radar loop
            categories_closed = categories + [categories[0]]
            values_closed = values + [values[0]]

            fig_radar = go.Figure(data=go.Scatterpolar(
                r=values_closed,
                theta=categories_closed,
                fill='toself',
                fillcolor='rgba(99, 102, 241, 0.35)',
                line=dict(color='#818cf8', width=2),
                marker=dict(size=6, color='#38bdf8')
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 25], color='#94a3b8', gridcolor='rgba(255,255,255,0.1)'),
                    angularaxis=dict(color='#ffffff', gridcolor='rgba(255,255,255,0.1)')
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=260,
                margin=dict(l=30, r=30, t=20, b=20)
            )
            st.plotly_chart(fig_radar, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # AI Buying Advisor Module
        st.markdown("### 🤖 Intelligent AI House Buying Advisor")
        
        target_info = advice["target_profile"]
        st.info(f"🎯 **Target Buyer Persona:** **{target_info['title']}** — {target_info['rationale']}")

        adv_tab1, adv_tab2, adv_tab3, adv_tab4 = st.tabs([
            "🌟 Core Strengths",
            "💡 Value Drivers",
            "⚠️ Due Diligence & Risks",
            "🤝 Buyer's Negotiation Playbook"
        ])

        with adv_tab1:
            for s in advice["strengths"]:
                st.markdown(f"""
                <div class="advisory-item strength">
                    <div class="advisory-header">{s['icon']} {s['title']}</div>
                    <div class="advisory-body">{s['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

        with adv_tab2:
            for op in advice["opportunities"]:
                st.markdown(f"""
                <div class="advisory-item opportunity">
                    <div class="advisory-header">{op['icon']} {op['title']}</div>
                    <div class="advisory-body">{op['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

        with adv_tab3:
            if advice["cautions"]:
                for c in advice["cautions"]:
                    st.markdown(f"""
                    <div class="advisory-item caution">
                        <div class="advisory-header">{c['icon']} {c['title']}</div>
                        <div class="advisory-body">{c['desc']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✨ Zero major risk flags detected in this property profile!")

        with adv_tab4:
            for n in advice["negotiation"]:
                st.markdown(f"""
                <div class="advisory-item negotiation">
                    <div class="advisory-header">{n['icon']} {n['title']}</div>
                    <div class="advisory-body">{n['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

        # Integrated Mortgage & EMI Calculator
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🏦 Financing & Monthly EMI Planner")
        
        with st.container():
            st.markdown("""<div class="glass-card">""", unsafe_allow_html=True)
            
            f1, f2, f3 = st.columns(3)
            down_pct = f1.slider("Down Payment (%)", min_value=10, max_value=50, value=20, step=5)
            loan_tenure = f2.slider("Loan Tenure (Years)", min_value=5, max_value=30, value=20, step=1)
            interest_rate = f3.slider("Annual Interest Rate (%)", min_value=6.5, max_value=14.0, value=8.5, step=0.1)

            emi_data = calculate_emi(price, down_pct, loan_tenure, interest_rate)

            ec1, ec2, ec3, ec4 = st.columns(4)
            ec1.metric("Down Payment", f"₹ {emi_data['down_payment_lakhs']} L")
            ec2.metric("Total Loan Amount", f"₹ {emi_data['loan_amount_lakhs']} L")
            ec3.metric("Estimated Monthly EMI", f"₹ {emi_data['monthly_emi']:,.0f}")
            ec4.metric("Total Interest Paid", f"₹ {emi_data['total_interest_lakhs']} L")

            st.markdown("</div>", unsafe_allow_html=True)

        # Export & Download Valuation Report
        report_text = generate_property_report_text(payload, price, score, rating, emi_data)
        st.download_button(
            label="📄 Download Official Valuation & Investment Report (.txt)",
            data=report_text,
            file_name=f"HomeWorth_Valuation_{payload['City']}_{payload['Locality']}.txt",
            mime="text/plain",
            use_container_width=True
        )

# ============================================================
# TAB 2: MARKET INTELLIGENCE & EDA
# ============================================================
with tab_market:
    st.markdown("""
    <div class="hero-wrapper">
        <div class="hero-tag">📊 Exploratory Data Analysis & Empirical Intelligence</div>
        <div class="hero-title">Real Estate <span class="gradient-text">Market Intelligence</span></div>
        <div class="hero-desc">
            Explore pricing distributions, locality trends, and amenities premiums derived from 506 validated property transactions across 10 top Indian metros analyzed during our research internship.
        </div>
    </div>
    """, unsafe_allow_html=True)

    df_market = load_market_dataset()

    if not df_market.empty:
        # High level market KPIs
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Sampled Properties", f"{len(df_market)}")
        k2.metric("Average Market Price", f"₹ {df_market['Price_Lakhs'].mean():,.1f} L")
        k3.metric("Median Property Price", f"₹ {df_market['Price_Lakhs'].median():,.1f} L")
        k4.metric("Max Asset Price", f"₹ {df_market['Price_Lakhs'].max():,.1f} L")
        k5.metric("Avg Rate / sq.ft", f"₹ {df_market['Price_per_sqft'].mean():,.0f}")

        st.markdown("<br>", unsafe_allow_html=True)

        # Plot 1: City-wise Average Prices
        st.markdown("""<div class="glass-card"><div class="card-title">🏙️ Metro Pricing Hierarchy (Average vs Median Price)</div>""", unsafe_allow_html=True)
        city_stats = df_market.groupby("City")["Price_Lakhs"].agg(["mean", "median", "count"]).reset_index()
        city_stats = city_stats.sort_values(by="mean", ascending=False)
        
        fig_city = px.bar(
            city_stats,
            x="City",
            y=["mean", "median"],
            barmode="group",
            labels={"value": "Price (₹ Lakhs)", "variable": "Metric"},
            color_discrete_sequence=["#3b82f6", "#8b5cf6"],
            template="plotly_dark"
        )
        fig_city.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_city, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Plot 2 & 3: Scatter Area vs Price and Box Plot
        sc_col1, sc_col2 = st.columns(2, gap="medium")

        with sc_col1:
            st.markdown("""<div class="glass-card"><div class="card-title">📐 Carpet Area vs Property Valuation</div>""", unsafe_allow_html=True)
            fig_scatter = px.scatter(
                df_market,
                x="Area_sqft",
                y="Price_Lakhs",
                color="Property_Type",
                hover_data=["City", "Locality", "Bedrooms"],
                labels={"Area_sqft": "Area (sq.ft.)", "Price_Lakhs": "Price (₹ Lakhs)"},
                template="plotly_dark"
            )
            fig_scatter.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=360,
                margin=dict(t=20, b=20, l=20, r=20)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with sc_col2:
            st.markdown("""<div class="glass-card"><div class="card-title">🏠 Property Type Price Ranges & Outliers</div>""", unsafe_allow_html=True)
            fig_box = px.box(
                df_market,
                x="Property_Type",
                y="Price_Lakhs",
                color="Property_Type",
                labels={"Property_Type": "Property Category", "Price_Lakhs": "Price (₹ Lakhs)"},
                template="plotly_dark"
            )
            fig_box.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=360,
                margin=dict(t=20, b=20, l=20, r=20)
            )
            st.plotly_chart(fig_box, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Plot 4: Amenities Premium Breakdown
        st.markdown("""<div class="glass-card"><div class="card-title">⭐ Value Premium of Critical Society Amenities</div>""", unsafe_allow_html=True)
        amenity_comparison = []
        amenities_list = [
            ("Has_Swimming_Pool", "Swimming Pool"),
            ("Has_Gym", "Fitness Gym"),
            ("Has_Clubhouse", "Clubhouse"),
            ("Has_Lift", "Elevator / Lift"),
            ("Has_Power_Backup", "Power Backup")
        ]
        for col_name, label in amenities_list:
            avg_with = df_market[df_market[col_name] == 1]["Price_Lakhs"].mean()
            avg_without = df_market[df_market[col_name] == 0]["Price_Lakhs"].mean()
            amenity_comparison.append({
                "Amenity": label,
                "With Amenity (₹ L)": round(avg_with, 2),
                "Without Amenity (₹ L)": round(avg_without, 2),
                "Premium (%)": round(((avg_with - avg_without) / avg_without) * 100, 1)
            })
        df_amenity_comp = pd.DataFrame(amenity_comparison)

        fig_amenity = px.bar(
            df_amenity_comp,
            x="Amenity",
            y=["With Amenity (₹ L)", "Without Amenity (₹ L)"],
            barmode="group",
            color_discrete_sequence=["#10b981", "#64748b"],
            template="plotly_dark"
        )
        fig_amenity.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=340,
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_amenity, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Interactive Data Filter
        st.markdown("### 🔍 Benchmark Dataset Explorer")
        with st.expander("Filter and Inspect Sample Records"):
            filt_c1, filt_c2 = st.columns(2)
            sel_cities = filt_c1.multiselect("Filter by City", options=df_market["City"].unique(), default=["Mumbai", "Delhi", "Bengaluru"])
            sel_types = filt_c2.multiselect("Filter by Type", options=df_market["Property_Type"].unique(), default=df_market["Property_Type"].unique())
            
            filtered_df = df_market[
                (df_market["City"].isin(sel_cities)) &
                (df_market["Property_Type"].isin(sel_types))
            ]
            st.dataframe(
                filtered_df[["City", "Locality", "Property_Type", "Area_sqft", "Bedrooms", "Bathrooms", "Floor_No", "Price_Lakhs", "Price_per_sqft"]].head(25),
                use_container_width=True
            )
    else:
        st.warning("⚠️ Market dataset file not found at Dataset/House_Price_Prediction_Dataset.xlsx.")

# ============================================================
# TAB 3: PROPERTY COMPARISON STUDIO
# ============================================================
with tab_compare:
    st.markdown("""
    <div class="hero-wrapper">
        <div class="hero-tag">⚖️ Side-by-Side Investment Decision Support</div>
        <div class="hero-title">Property <span class="gradient-text">Comparison Studio</span></div>
        <div class="hero-desc">
            Compare two properties across pricing, square footage valuation, society amenities, and property score to make data-backed purchasing choices.
        </div>
    </div>
    """, unsafe_allow_html=True)

    cmp_c1, cmp_c2 = st.columns(2, gap="large")

    with cmp_c1:
        st.markdown("#### 🏢 Property Option A")
        city_a = st.selectbox("City (A)", ["Mumbai", "Bengaluru", "Delhi", "Pune", "Hyderabad", "Jaipur", "Lucknow"], index=0, key="city_a")
        area_a = st.number_input("Area sq.ft (A)", min_value=400, max_value=8000, value=1400, step=50, key="area_a")
        bhk_a = st.number_input("Bedrooms (A)", min_value=1, max_value=6, value=3, key="bhk_a")
        prop_a = st.selectbox("Type (A)", ["Apartment", "Builder Floor", "Independent House", "Villa"], index=0, key="prop_a")
        amenities_a = st.slider("Amenities Score (A)", 0, 10, 8, key="amen_a")
        crime_a = st.slider("Crime Rate Index (A)", 0, 100, 20, key="crime_a")

    with cmp_c2:
        st.markdown("#### 🏡 Property Option B")
        city_b = st.selectbox("City (B)", ["Mumbai", "Bengaluru", "Delhi", "Pune", "Hyderabad", "Jaipur", "Lucknow"], index=1, key="city_b")
        area_b = st.number_input("Area sq.ft (B)", min_value=400, max_value=8000, value=1600, step=50, key="area_b")
        bhk_b = st.number_input("Bedrooms (B)", min_value=1, max_value=6, value=3, key="bhk_b")
        prop_b = st.selectbox("Type (B)", ["Apartment", "Builder Floor", "Independent House", "Villa"], index=0, key="prop_b")
        amenities_b = st.slider("Amenities Score (B)", 0, 10, 7, key="amen_b")
        crime_b = st.slider("Crime Rate Index (B)", 0, 100, 35, key="crime_b")

    if st.button("⚖️ Compare These Two Properties", use_container_width=True):
        # Quick synthesize full payloads
        mock_a = {
            "City": city_a, "Locality": "Green Park", "Locality_Type": "Urban", "Property_Type": prop_a,
            "Area_sqft": area_a, "Bedrooms": bhk_a, "Bathrooms": 2, "Balconies": 1, "Floor_No": 4, "Total_Floors": 10,
            "Age_of_Property_Years": 4, "Furnishing_Status": "Semi-Furnished", "Facing": "East", "Parking_Spaces": 1,
            "Distance_to_City_Center_km": 6.0, "Nearby_Schools_Count": 4, "Nearby_Hospitals_Count": 3,
            "Public_Transport_Access": "High", "Crime_Rate_Index": crime_a, "Air_Quality_Index": 55,
            "Has_Lift": 1, "Has_Security": 1, "Has_Gym": 1, "Has_Swimming_Pool": 0, "Has_Garden": 1,
            "Has_Power_Backup": 1, "Has_Clubhouse": 1, "Amenities_Score": amenities_a,
            "Ownership_Type": "Freehold", "Transaction_Type": "Resale", "Listing_Type": "Broker", "Months_on_Market": 2
        }
        mock_b = {
            "City": city_b, "Locality": "Riverside", "Locality_Type": "Urban", "Property_Type": prop_b,
            "Area_sqft": area_b, "Bedrooms": bhk_b, "Bathrooms": 2, "Balconies": 1, "Floor_No": 3, "Total_Floors": 12,
            "Age_of_Property_Years": 3, "Furnishing_Status": "Semi-Furnished", "Facing": "North", "Parking_Spaces": 1,
            "Distance_to_City_Center_km": 7.0, "Nearby_Schools_Count": 3, "Nearby_Hospitals_Count": 2,
            "Public_Transport_Access": "Medium", "Crime_Rate_Index": crime_b, "Air_Quality_Index": 60,
            "Has_Lift": 1, "Has_Security": 1, "Has_Gym": 1, "Has_Swimming_Pool": 1, "Has_Garden": 1,
            "Has_Power_Backup": 1, "Has_Clubhouse": 0, "Amenities_Score": amenities_b,
            "Ownership_Type": "Freehold", "Transaction_Type": "Resale", "Listing_Type": "Broker", "Months_on_Market": 2
        }

        price_a = predict_price(mock_a)
        price_b = predict_price(mock_b)
        score_a = property_score(mock_a)
        score_b = property_score(mock_b)

        rate_a = round((price_a * 100000) / area_a, 0)
        rate_b = round((price_b * 100000) / area_b, 0)

        st.markdown("<br>", unsafe_allow_html=True)
        rc1, rc2 = st.columns(2)
        with rc1:
            st.markdown(f"""
            <div class="glass-card" style="border-top:4px solid #3b82f6;">
                <h3>🏢 Property A ({city_a})</h3>
                <h1 style="color:#60a5fa;">{format_price(price_a)}</h1>
                <p><b>Rate:</b> ₹ {rate_a:,.0f} / sq.ft.</p>
                <p><b>Property Score:</b> {score_a}/100</p>
                <p><b>Investment Grade:</b> {investment_rating(score_a)}</p>
            </div>
            """, unsafe_allow_html=True)

        with rc2:
            st.markdown(f"""
            <div class="glass-card" style="border-top:4px solid #10b981;">
                <h3>🏡 Property B ({city_b})</h3>
                <h1 style="color:#34d399;">{format_price(price_b)}</h1>
                <p><b>Rate:</b> ₹ {rate_b:,.0f} / sq.ft.</p>
                <p><b>Property Score:</b> {score_b}/100</p>
                <p><b>Investment Grade:</b> {investment_rating(score_b)}</p>
            </div>
            """, unsafe_allow_html=True)

        # Comparative Verdict
        diff_price = abs(price_a - price_b)
        cheaper = "Property A" if price_a < price_b else "Property B"
        higher_score = "Property A" if score_a > score_b else "Property B"
        st.info(f"💡 **Comparative Analysis:** **{cheaper}** is more cost-efficient by ₹ {diff_price:,.2f} Lakhs. Meanwhile, **{higher_score}** achieves the higher composite livability and investment score.")

# ============================================================
# TAB 4: MODEL INTELLIGENCE & XAI
# ============================================================
with tab_xai:
    st.markdown("""
    <div class="hero-wrapper">
        <div class="hero-tag">🧠 Explainable AI & Algorithm Transparency</div>
        <div class="hero-title">Model <span class="gradient-text">Performance & Architecture</span></div>
        <div class="hero-desc">
            Empirical benchmark metrics, algorithm leaderboard, and feature importance rankings generated during model selection in the MNNIT Prayagraj AIML Internship.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🏆 Algorithm Leaderboard")
    metrics_data = get_model_benchmark_metrics()
    st.table(pd.DataFrame(metrics_data))

    # Leaderboard visual chart
    df_metrics = pd.DataFrame(metrics_data)
    fig_metrics = px.bar(
        df_metrics,
        x="Model",
        y="R2 Score",
        color="Model",
        text="Accuracy",
        labels={"R2 Score": "R² Variance Explained (0-1)"},
        template="plotly_dark",
        color_discrete_sequence=["#10b981", "#3b82f6", "#8b5cf6"]
    )
    fig_metrics.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(t=20, b=20, l=20, r=20)
    )
    st.plotly_chart(fig_metrics, use_container_width=True)

    # Feature Importance
    st.markdown("### 🔍 Top Predictive Features (Gradient Boosting Weights)")
    st.markdown("How much each housing attribute drives the final valuation estimate:")
    
    fi_df = get_feature_importances(12)
    fig_fi = px.bar(
        fi_df.sort_values(by="Importance_Pct", ascending=True),
        x="Importance_Pct",
        y="Display_Name",
        orientation="h",
        labels={"Importance_Pct": "Importance Weight (%)", "Display_Name": "Feature"},
        template="plotly_dark",
        color="Importance_Pct",
        color_continuous_scale="Viridis"
    )
    fig_fi.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420,
        margin=dict(t=20, b=20, l=20, r=20)
    )
    st.plotly_chart(fig_fi, use_container_width=True)

    st.markdown("""
    <div class="glass-card">
        <div class="card-title">⚙️ Machine Learning Pipeline Architecture</div>
        <p style="color:#94a3b8; font-size:14px; line-height:1.7;">
            <b>1. One-Hot Encoding:</b> 10 categorical attributes (City, Locality, Property Type, Facing, Furnishing, etc.) are converted into 46 numerical dummy vectors with <code>handle_unknown='ignore'</code>.<br>
            <b>2. ColumnTransformer:</b> Passthrough for 22 continuous numerical dimensions (Area, Bedrooms, Distance, AQI, Crime Index, Amenities).<br>
            <b>3. Gradient Boosting Regressor:</b> Fitted on 80% split with 100 estimators, minimizing squared error loss without overfitting.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# TAB 5: DOCUMENTATION & TEAM
# ============================================================
with tab_about:
    st.markdown("""
    <div class="hero-wrapper">
        <div class="hero-tag">🎓 Academic & Internship Project Profile</div>
        <div class="hero-title">About <span class="gradient-text">HomeWorth AI</span></div>
        <div class="hero-desc">
            Developed as part of the Artificial Intelligence & Machine Learning Summer Internship 2026 at IIHMF, Motilal Nehru National Institute of Technology (MNNIT) Prayagraj.
        </div>
    </div>
    """, unsafe_allow_html=True)

    dev_c1, dev_c2 = st.columns(2, gap="medium")

    with dev_c1:
        st.markdown("""
        <div class="glass-card">
            <h3>👨‍💻 Lead Developer</h3>
            <h2 style="color:#60a5fa; margin-bottom:4px;">Ujjaval Kumar Kesarwani</h2>
            <p style="color:#94a3b8;">B.Tech Computer Science & Engineering (AI & ML)<br>
            United College of Engineering & Research (UCER)</p>
            <hr style="border-color:rgba(255,255,255,0.08);">
            <p style="font-size:13.5px; color:#cbd5e1;"><b>Contributions:</b> ML Pipeline Design, Gradient Boosting Training, Streamlit Interactive Architecture, Frontend Design & Financial Algorithms.</p>
        </div>
        """, unsafe_allow_html=True)

    with dev_c2:
        st.markdown("""
        <div class="glass-card">
            <h3>👨‍💻 Co-Developer</h3>
            <h2 style="color:#a78bfa; margin-bottom:4px;">Shlok Tiwari</h2>
            <p style="color:#94a3b8;">B.Tech Computer Science & Engineering (AI & ML)<br>
            United College of Engineering & Research (UCER)</p>
            <hr style="border-color:rgba(255,255,255,0.08);">
            <p style="font-size:13.5px; color:#cbd5e1;"><b>Contributions:</b> Exploratory Data Analysis (EDA), Data Preprocessing & Missing Value Imputation, Model Evaluation & Presentation Reporting.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <div class="card-title">🏫 Host Institution & Organization</div>
        <p style="color:#f1f5f9; font-size:16px; font-weight:600;">
            IIHMF — Motilal Nehru National Institute of Technology (MNNIT), Prayagraj
        </p>
        <p style="color:#94a3b8; font-size:14px;">
            Artificial Intelligence & Machine Learning Summer Internship 2026. Project evaluated on real-world Indian real estate datasets comprising 34 attributes across 10 major metropolitan centers.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# Universal App Footer
# ============================================================
st.markdown("""
<div class="app-footer">
    🏡 <b>HomeWorth AI — Production Edition 2.0</b><br>
    Built with Python • Streamlit • Scikit-Learn • Plotly • Pandas • Gradient Boosting<br>
    Developed by <b>Ujjaval Kumar Kesarwani</b> & <b>Shlok Tiwari</b> • IIHMF, MNNIT Prayagraj
</div>
""", unsafe_allow_html=True)