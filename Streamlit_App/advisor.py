def generate_advice(user_input, predicted_price):
    """
    Generate AI-like buying tips based on property details.
    """

    advice = []

    # Property Price
    if predicted_price < 50:
        advice.append("💰 This property appears to be budget-friendly.")
    elif predicted_price < 100:
        advice.append("💰 This property falls in the mid-range price segment.")
    else:
        advice.append("💎 This is a premium property with high market value.")

    # Crime Rate
    if user_input["Crime_Rate_Index"] <= 30:
        advice.append("🛡️ Located in a relatively safe neighbourhood.")
    else:
        advice.append("⚠️ Consider reviewing the area's safety before purchasing.")

    # Air Quality
    if user_input["Air_Quality_Index"] <= 50:
        advice.append("🌿 Excellent air quality for healthy living.")
    elif user_input["Air_Quality_Index"] <= 100:
        advice.append("🌤️ Air quality is acceptable for daily life.")
    else:
        advice.append("🏭 Air quality is relatively poor.")

    # Schools
    if user_input["Nearby_Schools_Count"] >= 4:
        advice.append("🏫 Good educational facilities are available nearby.")

    # Hospitals
    if user_input["Nearby_Hospitals_Count"] >= 3:
        advice.append("🏥 Healthcare facilities are easily accessible.")

    # Facing
    if user_input["Facing"] == "East":
        advice.append("🌅 East-facing homes are popular for natural morning sunlight.")
    elif user_input["Facing"] == "North-East":
        advice.append("✨ North-East facing properties are often considered highly desirable.")

    # Property Age
    if user_input["Age_of_Property_Years"] <= 5:
        advice.append("🏡 Relatively new property requiring minimal maintenance.")
    elif user_input["Age_of_Property_Years"] >= 20:
        advice.append("🔧 Older property—consider renovation costs.")

    # Amenities
    if user_input["Amenities_Score"] >= 8:
        advice.append("⭐ Excellent amenities increase lifestyle and resale value.")
    elif user_input["Amenities_Score"] >= 5:
        advice.append("👍 Decent amenities suitable for comfortable living.")

    return advice