def format_price(price):
    """
    Format predicted price.
    """
    return f"₹ {price:,.2f} Lakhs"


def property_score(user_input):
    """
    Calculate an overall property score out of 100.
    """

    score = 50

    # Amenities
    score += user_input["Amenities_Score"] * 3

    # Safety
    if user_input["Crime_Rate_Index"] <= 30:
        score += 8

    # Air Quality
    if user_input["Air_Quality_Index"] <= 80:
        score += 6

    # Schools
    if user_input["Nearby_Schools_Count"] >= 4:
        score += 6

    # Hospitals
    if user_input["Nearby_Hospitals_Count"] >= 3:
        score += 5

    # Parking
    if user_input["Parking_Spaces"] >= 1:
        score += 4

    # Lift
    if user_input["Has_Lift"] == 1:
        score += 3

    # Security
    if user_input["Has_Security"] == 1:
        score += 4

    # Keep score between 0 and 100
    score = min(score, 100)

    return score


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