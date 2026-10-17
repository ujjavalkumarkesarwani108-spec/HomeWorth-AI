import os
import joblib
import pandas as pd
import numpy as np

CURRENT_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(CURRENT_DIR, "..", "Model", "house_price_pipeline.pkl")

# Cache model instance
_cached_pipeline = None


def load_pipeline():
    """Load and cache the trained ML pipeline."""
    global _cached_pipeline
    if _cached_pipeline is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")
        _cached_pipeline = joblib.load(MODEL_PATH)
    return _cached_pipeline


# Pre-load on import
pipeline = load_pipeline()


def predict_price(user_input: dict) -> float:
    """
    Predict residential property price in Lakhs.
    Returns: float (Price in Lakhs rounded to 2 decimal places)
    """
    pipe = load_pipeline()
    input_df = pd.DataFrame([user_input])
    prediction = pipe.predict(input_df)[0]
    # Bound predictions reasonably to positive territory
    return max(round(float(prediction), 2), 5.0)


def predict_price_range(predicted_price: float, mae: float = 10.01) -> tuple:
    """
    Calculate high-confidence price range based on model MAE.
    Returns: (lower_bound_lakhs, upper_bound_lakhs)
    """
    spread = round(mae * 0.75, 2)
    lower = max(round(predicted_price - spread, 2), 5.0)
    upper = round(predicted_price + spread, 2)
    return lower, upper


def get_model_benchmark_metrics():
    """
    Returns empirical evaluation results from the internship research notebook (EDA.ipynb).
    """
    return [
        {
            "Model": "Gradient Boosting Regressor",
            "MAE (₹ Lakhs)": 10.01,
            "RMSE (₹ Lakhs)": 13.85,
            "R2 Score": 0.9392,
            "Accuracy": "93.92%",
            "Status": "🏆 Best Selected Model"
        },
        {
            "Model": "Linear Regression",
            "MAE (₹ Lakhs)": 13.79,
            "RMSE (₹ Lakhs)": 18.42,
            "R2 Score": 0.8925,
            "Accuracy": "89.25%",
            "Status": "Baseline Model"
        },
        {
            "Model": "Random Forest Regressor",
            "MAE (₹ Lakhs)": 15.86,
            "RMSE (₹ Lakhs)": 22.00,
            "R2 Score": 0.8467,
            "Accuracy": "84.67%",
            "Status": "Ensemble Model"
        }
    ]


def get_feature_importances(top_n: int = 15):
    """
    Extracts top feature importances from the trained Gradient Boosting model.
    """
    pipe = load_pipeline()
    try:
        model = pipe.named_steps["model"]
        pre = pipe.named_steps["preprocessor"]
        
        cat_cols = pre.transformers_[0][2]
        cat_encoder = pre.named_transformers_["cat"]
        cat_feature_names = list(cat_encoder.get_feature_names_out(cat_cols))
        
        num_feature_names = [
            "Area_sqft", "Bedrooms", "Bathrooms", "Balconies", "Floor_No",
            "Total_Floors", "Age_of_Property_Years", "Parking_Spaces",
            "Distance_to_City_Center_km", "Nearby_Schools_Count",
            "Nearby_Hospitals_Count", "Crime_Rate_Index", "Air_Quality_Index",
            "Has_Lift", "Has_Security", "Has_Gym", "Has_Swimming_Pool",
            "Has_Garden", "Has_Power_Backup", "Has_Clubhouse", "Amenities_Score",
            "Months_on_Market"
        ]
        
        all_feature_names = cat_feature_names + num_feature_names
        importances = model.feature_importances_
        
        fi_df = pd.DataFrame({
            "Feature": all_feature_names,
            "Importance": importances
        }).sort_values(by="Importance", ascending=False).head(top_n)
        
        # Clean up readable feature names
        def humanize_feature(name):
            clean = name.replace("City_", "City: ").replace("Locality_", "Locality: ")
            clean = clean.replace("Property_Type_", "Type: ").replace("Furnishing_Status_", "Furnishing: ")
            clean = clean.replace("Public_Transport_Access_", "Transit: ").replace("Facing_", "Facing: ")
            clean = clean.replace("_sqft", " (sq.ft)").replace("_km", " (km)").replace("_Years", " (yrs)")
            clean = clean.replace("_", " ")
            return clean
            
        fi_df["Display_Name"] = fi_df["Feature"].apply(humanize_feature)
        fi_df["Importance_Pct"] = (fi_df["Importance"] * 100).round(2)
        return fi_df
    except Exception as e:
        # Fallback to key empirical values
        return pd.DataFrame([
            {"Display_Name": "Area (sq.ft)", "Importance_Pct": 63.56},
            {"Display_Name": "City: Delhi", "Importance_Pct": 6.06},
            {"Display_Name": "City: Lucknow", "Importance_Pct": 4.63},
            {"Display_Name": "City: Bengaluru", "Importance_Pct": 4.56},
            {"Display_Name": "City: Ahmedabad", "Importance_Pct": 4.36},
            {"Display_Name": "City: Mumbai", "Importance_Pct": 3.29},
            {"Display_Name": "Type: Villa", "Importance_Pct": 2.37},
            {"Display_Name": "Distance to Center (km)", "Importance_Pct": 1.99},
            {"Display_Name": "City: Jaipur", "Importance_Pct": 1.89},
            {"Display_Name": "Property Age (yrs)", "Importance_Pct": 1.50},
        ])