def generate_structured_advice(user_input: dict, predicted_price: float) -> dict:
    """
    Generate an intelligent multi-dimensional buying & investment advisory report.
    Returns: dict with categories:
        - strengths: list of strong asset points
        - opportunities: list of potential appreciation and lifestyle upsides
        - cautions: list of risk factors and due diligence requirements
        - negotiation: actionable negotiation tactics for buyers
        - target_profile: recommended buyer/investor persona
    """
    strengths = []
    opportunities = []
    cautions = []
    negotiation = []
    
    # 1. Price & Valuation Dynamics
    if predicted_price < 50:
        strengths.append({
            "icon": "💰",
            "title": "High Affordability",
            "desc": f"At an estimated ₹ {predicted_price:,.2f} Lakhs, this home sits in the high-demand entry-level budget bracket, minimizing borrowing risk."
        })
        opportunities.append({
            "icon": "📈",
            "title": "Fast Rental Liquidity",
            "desc": "Entry-level residential units consistently experience minimal vacancy periods and rapid tenant absorption."
        })
    elif predicted_price <= 120:
        strengths.append({
            "icon": "💎",
            "title": "Prime Mid-Segment Asset",
            "desc": f"Valued at ₹ {predicted_price:,.2f} Lakhs, this home matches the preferred urban demographic segment with balanced capital appreciation."
        })
        opportunities.append({
            "icon": "🚀",
            "title": "Strong Resale Velocity",
            "desc": "Properties in this segment exhibit the healthiest volume of secondary market transactions across major metro zones."
        })
    else:
        strengths.append({
            "icon": "👑",
            "title": "Prestige Luxury Living",
            "desc": f"Premium asset valued at ₹ {predicted_price:,.2f} Lakhs offering expansive living spaces and exclusivity."
        })
        cautions.append({
            "icon": "⏳",
            "title": "Longer Resale Horizon",
            "desc": "High-ticket luxury inventory traditionally requires a longer transaction timeline to liquidate at market rate."
        })

    # 2. Safety & Crime Index
    crime = user_input.get("Crime_Rate_Index", 30)
    if crime <= 25:
        strengths.append({
            "icon": "🛡️",
            "title": "Exceptional Safety Profile",
            "desc": f"Crime rate index of {crime}/100 places this locality in the top safety quartile, ideal for family security."
        })
    elif crime <= 50:
        strengths.append({
            "icon": "✅",
            "title": "Moderate Neighborhood Security",
            "desc": f"Crime index of {crime}/100 is within average municipal benchmarks; gated security adds sufficient protection."
        })
    else:
        cautions.append({
            "icon": "⚠️",
            "title": "Elevated Crime Index",
            "desc": f"Crime index of {crime}/100 warrants thorough local verification of street lighting, night patrolling, and CCTV perimeter."
        })
        negotiation.append({
            "icon": "🔍",
            "title": "Safety Discount Negotiation",
            "desc": "Leverage higher local crime stats to request a 3-5% pricing concession or complimentary security upgrades from the seller."
        })

    # 3. Environment & Air Quality (AQI)
    aqi = user_input.get("Air_Quality_Index", 60)
    if aqi <= 50:
        strengths.append({
            "icon": "🌿",
            "title": "Pristine Air Quality",
            "desc": f"AQI of {aqi} is pristine, significantly enhancing daily wellness, child health, and long-term livability."
        })
    elif aqi <= 100:
        strengths.append({
            "icon": "🌤️",
            "title": "Acceptable Air Standards",
            "desc": f"AQI of {aqi} represents standard healthy urban living conditions."
        })
    else:
        cautions.append({
            "icon": "🏭",
            "title": "Compromised Air Quality",
            "desc": f"AQI of {aqi} indicates noticeable particulate pollution. Consider indoor air filtration and double-glazed windows."
        })

    # 4. Connectivity & Distance to Center
    distance = user_input.get("Distance_to_City_Center_km", 6.0)
    transit = user_input.get("Public_Transport_Access", "Medium")
    if distance <= 5:
        opportunities.append({
            "icon": "📍",
            "title": "Strategic City-Core Proximity",
            "desc": f"Only {distance} km from the city center, saving hundreds of commuting hours yearly and commanding a premium rental yield."
        })
    elif distance >= 15:
        cautions.append({
            "icon": "🚗",
            "title": "Commuting Overhead",
            "desc": f"Being {distance} km out means higher travel overhead; verify upcoming metro expansion or arterial expressways."
        })
        negotiation.append({
            "icon": "🛣️",
            "title": "Distance Arbitrage",
            "desc": "Highlight peripheral location and transit delays to push for lower per-sqft pricing."
        })
        
    if transit == "High":
        strengths.append({
            "icon": "🚇",
            "title": "Rapid Transit Hub",
            "desc": "High public transport access significantly boosts tenant attraction and eliminates reliance on private vehicles."
        })

    # 5. Social Infrastructure (Schools & Hospitals)
    schools = user_input.get("Nearby_Schools_Count", 3)
    hospitals = user_input.get("Nearby_Hospitals_Count", 2)
    if schools >= 4 and hospitals >= 3:
        opportunities.append({
            "icon": "🏫",
            "title": "Complete Social Infrastructure",
            "desc": f"Surrounded by {schools} schools and {hospitals} hospitals, guaranteeing enduring family tenancy and steady property valuation."
        })
    elif schools <= 1 or hospitals <= 1:
        cautions.append({
            "icon": "🏥",
            "title": "Limited Healthcare/School Density",
            "desc": "Basic social amenities are sparse; ensure emergency medical services are within acceptable driving distance."
        })

    # 6. Age of Property & Maintenance
    age = user_input.get("Age_of_Property_Years", 5)
    if age <= 3:
        strengths.append({
            "icon": "✨",
            "title": "Brand-New / Modern Construction",
            "desc": f"At {age} year(s) old, the building incorporates contemporary building codes with near-zero initial maintenance overhead."
        })
    elif age >= 18:
        cautions.append({
            "icon": "🔧",
            "title": "Aging Structural Infrastructure",
            "desc": f"Property is {age} years old. Budget for potential plumbing, electrical rewiring, and waterproofing repairs."
        })
        negotiation.append({
            "icon": "🔨",
            "title": "Renovation Cost Buffer",
            "desc": "Request a 5-8% reduction to account for impending modernizations and society repair funds."
        })

    # 7. Floor & Orientation
    floor = user_input.get("Floor_No", 3)
    total_floors = user_input.get("Total_Floors", 10)
    facing = user_input.get("Facing", "East")
    
    if facing in ["East", "North-East"]:
        strengths.append({
            "icon": "🌅",
            "title": f"Optimal {facing} Orientation",
            "desc": "Morning sunlight exposure and favorable Vaastu alignment provide high daylight efficiency and superior resale liquidity."
        })
        
    if floor == 0:
        cautions.append({
            "icon": "🚪",
            "title": "Ground Floor Privacy & Security",
            "desc": "Ground floors offer zero lift dependency but require enhanced window grilles and insect mesh."
        })
    elif floor == total_floors and total_floors > 3:
        opportunities.append({
            "icon": "🌆",
            "title": "Top-Floor Panoramic Views",
            "desc": "Top-level location guarantees panoramic horizon views, enhanced natural breeze, and zero overhead footstep noise."
        })

    # 8. Months on Market & Negotiation Power
    months = user_input.get("Months_on_Market", 2)
    if months >= 6:
        negotiation.append({
            "icon": "⌛",
            "title": f"Motivated Seller Advantage ({months} Mos Active)",
            "desc": f"The listing has been active for {months} months. Make an initial offer 8-12% below asking price to test seller urgency."
        })
    else:
        negotiation.append({
            "icon": "⚡",
            "title": "Competitive Fresh Listing",
            "desc": f"Listed for just {months} month(s). Benchmark closely against recent society comps before submitting a firm bid."
        })

    # 9. Amenities Score
    amenities = user_input.get("Amenities_Score", 7)
    if amenities >= 8:
        strengths.append({
            "icon": "🏊",
            "title": "Full-Spectrum Lifestyle Amenities",
            "desc": f"Clubhouse amenities rated {amenities}/10 directly support premium rental rates and elevated standard of living."
        })

    # Target Buyer Profile
    if predicted_price < 60 and user_input.get("Bedrooms", 2) <= 2:
        target_profile = {
            "title": "First-Time Homebuyer & Young Professionals",
            "rationale": "High cost-efficiency, manageable EMIs, and rapid capital recovery make this an ideal starter residence."
        }
    elif predicted_price > 130 or user_input.get("Property_Type") == "Villa":
        target_profile = {
            "title": "High-Net-Worth Individuals & Luxury Seekers",
            "rationale": "Prioritizes luxury square footage, privacy, expansive parking, and exclusive community amenities."
        }
    elif user_input.get("Nearby_Schools_Count", 0) >= 3 and user_input.get("Bedrooms", 2) >= 3:
        target_profile = {
            "title": "Long-Term End-User Families",
            "rationale": "Spacious multi-bedroom layout backed by nearby educational, healthcare, and leisure amenities."
        }
    else:
        target_profile = {
            "title": "Balanced Rental Yield & Wealth Preservation Investor",
            "rationale": "Consistent urban tenant demand with resilient per-square-foot valuation stability."
        }

    return {
        "strengths": strengths[:4],
        "opportunities": opportunities[:3],
        "cautions": cautions[:3],
        "negotiation": negotiation[:3],
        "target_profile": target_profile
    }


def generate_advice(user_input, predicted_price):
    """
    Backwards-compatible wrapper returning list of top textual insights.
    """
    structured = generate_structured_advice(user_input, predicted_price)
    flat_list = []
    for item in structured["strengths"]:
        flat_list.append(f"{item['icon']} **{item['title']}**: {item['desc']}")
    for item in structured["opportunities"]:
        flat_list.append(f"{item['icon']} **{item['title']}**: {item['desc']}")
    for item in structured["cautions"]:
        flat_list.append(f"{item['icon']} **{item['title']}**: {item['desc']}")
    return flat_list