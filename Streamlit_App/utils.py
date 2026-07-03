def format_price(price):
    """
    Format predicted price.
    """
    return f"₹ {price:,.2f} Lakhs"


def property_score(user_input):
    """
    Calculate a realistic property score out of 100.
    """

    score = 0

    # ======================================================
    # Area (15 Marks)
    # ======================================================
    area = user_input["Area_sqft"]

    if area >= 2500:
        score += 15
    elif area >= 1800:
        score += 12
    elif area >= 1200:
        score += 10
    elif area >= 800:
        score += 7
    else:
        score += 4

    # ======================================================
    # Amenities (20 Marks)
    # ======================================================
    score += user_input["Amenities_Score"] * 2

    # ======================================================
    # Crime (10 Marks)
    # ======================================================
    crime = user_input["Crime_Rate_Index"]

    if crime <= 20:
        score += 10
    elif crime <= 40:
        score += 8
    elif crime <= 60:
        score += 5
    else:
        score += 2

    # ======================================================
    # Air Quality (10 Marks)
    # ======================================================
    air = user_input["Air_Quality_Index"]

    if air <= 50:
        score += 10
    elif air <= 80:
        score += 8
    elif air <= 120:
        score += 5
    else:
        score += 2

    # ======================================================
    # Schools (8 Marks)
    # ======================================================
    schools = user_input["Nearby_Schools_Count"]

    if schools >= 5:
        score += 8
    elif schools >= 3:
        score += 6
    else:
        score += 3

    # ======================================================
    # Hospitals (8 Marks)
    # ======================================================
    hospitals = user_input["Nearby_Hospitals_Count"]

    if hospitals >= 4:
        score += 8
    elif hospitals >= 2:
        score += 6
    else:
        score += 3

    # ======================================================
    # Parking (5 Marks)
    # ======================================================
    parking = user_input["Parking_Spaces"]

    if parking >= 2:
        score += 5
    elif parking == 1:
        score += 3

    # ======================================================
    # Floor Preference (5 Marks)
    # ======================================================
    floor = user_input["Floor_No"]

    if 2 <= floor <= 8:
        score += 5
    elif floor <= 15:
        score += 3
    else:
        score += 2

    # ======================================================
    # Property Age (7 Marks)
    # ======================================================
    age = user_input["Age_of_Property_Years"]

    if age <= 5:
        score += 7
    elif age <= 10:
        score += 5
    elif age <= 20:
        score += 3
    else:
        score += 1

    # ======================================================
    # Bonus Features (12 Marks)
    # ======================================================
    bonus = 0

    bonus += user_input["Has_Lift"] * 2
    bonus += user_input["Has_Security"] * 3
    bonus += user_input["Has_Gym"] * 2
    bonus += user_input["Has_Swimming_Pool"] * 2
    bonus += user_input["Has_Garden"] * 1
    bonus += user_input["Has_Power_Backup"] * 1
    bonus += user_input["Has_Clubhouse"] * 1

    score += bonus

    return min(round(score), 100)


def investment_rating(score):
    """
    Return investment quality.
    """

    if score >= 90:
        return "🟢 Excellent"

    elif score >= 75:
        return "🟡 Good"

    elif score >= 60:
        return "🟠 Average"

    else:
        return "🔴 Needs Attention"


def market_category(price):
    """
    Categorize house based on predicted price.
    """

    if price < 50:
        return "💚 Budget"

    elif price < 100:
        return "💙 Premium"

    else:
        return "💜 Luxury"

def confidence_score(score):
    """
    Estimate prediction confidence based on property score.
    """

    if score >= 90:
        return 96

    elif score >= 80:
        return 93

    elif score >= 70:
        return 89

    elif score >= 60:
        return 84

    else:
        return 78    