import os
import joblib
import pandas as pd


CURRENT_DIR = os.path.dirname(__file__)

MODEL_PATH = os.path.join(
    CURRENT_DIR,
    "..",
    "Model",
    "house_price_pipeline.pkl"
)


pipeline = joblib.load(MODEL_PATH)


def predict_price(user_input):

    input_df = pd.DataFrame([user_input])

    prediction = pipeline.predict(input_df)[0]

    return round(float(prediction), 2)