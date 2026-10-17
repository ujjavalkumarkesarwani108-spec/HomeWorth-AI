import os
import pandas as pd
import numpy as np

CURRENT_DIR = os.path.dirname(__file__)
DATASET_PATH = os.path.join(CURRENT_DIR, "..", "Dataset", "House_Price_Prediction_Dataset.xlsx")

# Cached DataFrame
_cached_df = None


def format_price(price: float) -> str:
    """
    Format predicted price safely into standard Indian real estate notations (Lakhs & Crores).
    Handles None gracefully to prevent crashes.
    """
    if price is None:
        return "₹ 0.00 Lakhs"
    
    try:
        price_float = float(price)
    except (ValueError, TypeError):
        return "₹ 0.00 Lakhs"
        
    if price_float >= 100.0:
        cr_val = price_float / 100.0
        return f"₹ {cr_val:,.2f} Cr ({price_float:,.2f} L)"
    else:
        return f"₹ {price_float:,.2f} Lakhs"


def property_score(user_input: dict) -> int:
    """
    Calculate an overall realistic property score out of 100.
    """
    sub_scores = get_property_subscores(user_input)
    return sub_scores["total"]


def get_property_subscores(user_input: dict) -> dict:
    """
    Calculate detailed component subscores across four key real-estate pillars:
    1. Location & Connectivity (25 pts)
    2. Physical Specs & Construction (25 pts)
    3. Amenities & Lifestyle (25 pts)
    4. Safety & Environment (25 pts)
    """
    # Pillar 1: Location & Transit (Max 25)
    dist = user_input.get("Distance_to_City_Center_km", 6.0)
    transit = user_input.get("Public_Transport_Access", "Medium")
    schools = user_input.get("Nearby_Schools_Count", 3)
    hospitals = user_input.get("Nearby_Hospitals_Count", 2)
    
    p1 = 0
    # Distance
    if dist <= 4:
        p1 += 9
    elif dist <= 8:
        p1 += 7
    elif dist <= 14:
        p1 += 5
    else:
        p1 += 3
        
    # Transit
    if transit == "High":
        p1 += 6
    elif transit == "Medium":
        p1 += 4
    else:
        p1 += 2
        
    # Social infra
    p1 += min(schools, 5) * 1.0  # max 5
    p1 += min(hospitals, 5) * 1.0  # max 5
    p1 = min(round(p1), 25)

    # Pillar 2: Specs & Construction (Max 25)
    area = user_input.get("Area_sqft", 1200)
    age = user_input.get("Age_of_Property_Years", 5)
    parking = user_input.get("Parking_Spaces", 1)
    furnishing = user_input.get("Furnishing_Status", "Semi-Furnished")
    facing = user_input.get("Facing", "East")
    
    p2 = 0
    # Area
    if area >= 2400:
        p2 += 8
    elif area >= 1600:
        p2 += 7
    elif area >= 1000:
        p2 += 5
    else:
        p2 += 3
        
    # Age
    if age <= 3:
        p2 += 7
    elif age <= 8:
        p2 += 5
    elif age <= 15:
        p2 += 3
    else:
        p2 += 1
        
    # Parking
    if parking >= 2:
        p2 += 4
    elif parking == 1:
        p2 += 3
    else:
        p2 += 1
        
    # Furnishing
    if furnishing == "Fully-Furnished":
        p2 += 3
    elif furnishing == "Semi-Furnished":
        p2 += 2
    else:
        p2 += 1
        
    # Facing
    if facing in ["East", "North-East"]:
        p2 += 3
    elif facing == "North":
        p2 += 2
    else:
        p2 += 1
    p2 = min(round(p2), 25)

    # Pillar 3: Amenities (Max 25)
    amenity_score_raw = user_input.get("Amenities_Score", 7)
    bonus = 0
    bonus += user_input.get("Has_Lift", 0) * 2
    bonus += user_input.get("Has_Security", 0) * 3
    bonus += user_input.get("Has_Gym", 0) * 2
    bonus += user_input.get("Has_Swimming_Pool", 0) * 2
    bonus += user_input.get("Has_Power_Backup", 0) * 2
    bonus += user_input.get("Has_Garden", 0) * 1
    bonus += user_input.get("Has_Clubhouse", 0) * 1
    
    p3 = min(round((amenity_score_raw * 1.5) + (bonus * 0.9)), 25)

    # Pillar 4: Safety & Air Quality (Max 25)
    crime = user_input.get("Crime_Rate_Index", 25)
    aqi = user_input.get("Air_Quality_Index", 60)
    
    p4 = 0
    # Crime (13 pts)
    if crime <= 20:
        p4 += 13
    elif crime <= 35:
        p4 += 10
    elif crime <= 50:
        p4 += 7
    elif crime <= 65:
        p4 += 4
    else:
        p4 += 2
        
    # AQI (12 pts)
    if aqi <= 45:
        p4 += 12
    elif aqi <= 75:
        p4 += 9
    elif aqi <= 110:
        p4 += 6
    elif aqi <= 160:
        p4 += 4
    else:
        p4 += 2
    p4 = min(round(p4), 25)

    total = min(p1 + p2 + p3 + p4, 100)
    return {
        "location": p1,
        "specs": p2,
        "amenities": p3,
        "environment": p4,
        "total": total
    }


def investment_rating(score: int) -> str:
    """
    Return investment rating grade.
    """
    if score >= 88:
        return "🟢 Grade AAA (Prime Outperform)"
    elif score >= 75:
        return "🟢 Grade AA (High Conviction Buy)"
    elif score >= 62:
        return "🟡 Grade A (Stable Quality)"
    elif score >= 50:
        return "🟠 Grade B (Moderate Risk)"
    else:
        return "🔴 Grade C (Speculative / Due Diligence)"


def market_category(price: float) -> str:
    """
    Categorize house based on predicted price.
    """
    if price is None:
        return "💙 Standard"
    if price < 50:
        return "💚 Affordable / Budget"
    elif price < 100:
        return "💙 Mid-Segment Premium"
    elif price < 200:
        return "💜 Luxury Residence"
    else:
        return "👑 Ultra-Luxury Estate"


def confidence_score(score: int) -> int:
    """
    Estimate model prediction confidence based on inputs & property score.
    """
    if score >= 88:
        return 96
    elif score >= 75:
        return 93
    elif score >= 62:
        return 89
    elif score >= 50:
        return 85
    else:
        return 80


def calculate_emi(
    principal_lakhs: float,
    down_payment_pct: float = 20.0,
    tenure_years: int = 20,
    annual_interest_rate: float = 8.5
) -> dict:
    """
    Calculate real-world Indian Home Loan EMI and financial breakdown.
    """
    if principal_lakhs is None or principal_lakhs <= 0:
        return {
            "down_payment_lakhs": 0.0,
            "loan_amount_lakhs": 0.0,
            "monthly_emi": 0.0,
            "total_interest_lakhs": 0.0,
            "total_payable_lakhs": 0.0
        }
        
    down_payment = (principal_lakhs * down_payment_pct) / 100.0
    loan_amount = principal_lakhs - down_payment
    
    # Principal in INR
    P = loan_amount * 100000.0
    monthly_r = (annual_interest_rate / 12.0) / 100.0
    num_months = tenure_years * 12
    
    if monthly_r > 0 and num_months > 0:
        # Standard EMI Formula: [P * r * (1+r)^n] / [(1+r)^n - 1]
        emi = (P * monthly_r * ((1 + monthly_r) ** num_months)) / (((1 + monthly_r) ** num_months) - 1)
        total_payment = emi * num_months
        total_interest = total_payment - P
    else:
        emi = P / num_months if num_months > 0 else 0.0
        total_interest = 0.0
        total_payment = P

    return {
        "down_payment_lakhs": round(down_payment, 2),
        "loan_amount_lakhs": round(loan_amount, 2),
        "monthly_emi": round(emi, 0),
        "total_interest_lakhs": round(total_interest / 100000.0, 2),
        "total_payable_lakhs": round((down_payment * 100000.0 + total_payment) / 100000.0, 2)
    }


def load_market_dataset():
    """
    Load and cache the project dataset for real-time analytics.
    """
    global _cached_df
    if _cached_df is not None:
        return _cached_df
        
    if os.path.exists(DATASET_PATH):
        try:
            _cached_df = pd.read_excel(DATASET_PATH)
            # Add derived metric: Price per sqft
            if "Price_per_sqft" not in _cached_df.columns:
                _cached_df["Price_per_sqft"] = (
                    (_cached_df["Price_Lakhs"] * 100000.0) / _cached_df["Area_sqft"]
                ).round(0)
            return _cached_df
        except Exception:
            pass
            
    # Synthetic fallback if excel read fails
    return pd.DataFrame()


def generate_property_report_text(user_input: dict, predicted_price: float, score: int, rating: str, emi_info: dict) -> str:
    """
    Generate downloadable comprehensive valuation summary.
    """
    lower, upper = round(predicted_price * 0.92, 2), round(predicted_price * 1.08, 2)
    area = user_input.get("Area_sqft", 1000)
    price_per_sqft = round((predicted_price * 100000) / area, 0) if area > 0 else 0
    
    lines = [
        "============================================================",
        "             HOMEWORTH AI - PROPERTY VALUATION REPORT",
        "     Generated by AI & Machine Learning Summer Project 2026",
        "============================================================",
        "",
        "1. VALUATION OVERVIEW",
        f"   - Estimated Market Value : {format_price(predicted_price)}",
        f"   - High-Confidence Range : ₹ {lower:,.2f} Lakhs - ₹ {upper:,.2f} Lakhs",
        f"   - Estimated Rate / sqft : ₹ {price_per_sqft:,.0f} / sq.ft.",
        f"   - Property Score        : {score}/100",
        f"   - Investment Rating     : {rating}",
        f"   - Market Segment        : {market_category(predicted_price)}",
        "",
        "2. PROPERTY SPECIFICATIONS",
        f"   - Location              : {user_input.get('City')}, {user_input.get('Locality')} ({user_input.get('Locality_Type')})",
        f"   - Property Type         : {user_input.get('Property_Type')}",
        f"   - Layout & Area         : {user_input.get('Bedrooms')} BHK | {area} sq.ft.",
        f"   - Bathrooms / Balconies : {user_input.get('Bathrooms')} Baths | {user_input.get('Balconies')} Balcony",
        f"   - Floor Details         : Floor {user_input.get('Floor_No')} of {user_input.get('Total_Floors')}",
        f"   - Facing & Age          : {user_input.get('Facing')} Facing | {user_input.get('Age_of_Property_Years')} Yrs Old",
        f"   - Parking & Furnishing  : {user_input.get('Parking_Spaces')} Spaces | {user_input.get('Furnishing_Status')}",
        "",
        "3. NEIGHBORHOOD & INFRASTRUCTURE",
        f"   - Distance to Center    : {user_input.get('Distance_to_City_Center_km')} km",
        f"   - Transit & Amenities   : {user_input.get('Public_Transport_Access')} Transit | Score {user_input.get('Amenities_Score')}/10",
        f"   - Crime Rate Index      : {user_input.get('Crime_Rate_Index')}/100",
        f"   - Air Quality Index     : {user_input.get('Air_Quality_Index')} AQI",
        "",
        "4. ESTIMATED FINANCING (20 Yrs @ 8.5%)",
        f"   - Down Payment (20%)    : ₹ {emi_info.get('down_payment_lakhs')} Lakhs",
        f"   - Loan Amount (80%)     : ₹ {emi_info.get('loan_amount_lakhs')} Lakhs",
        f"   - Estimated Monthly EMI : ₹ {emi_info.get('monthly_emi'):,.0f} / month",
        "",
        "============================================================",
        "Project Developers: Ujjaval Kumar Kesarwani & Shlok Tiwari",
        "MNNIT Prayagraj - IIHMF AIML Summer Internship 2026",
        "============================================================"
    ]
    return "\n".join(lines)