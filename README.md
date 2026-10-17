# 🏡 HomeWorth AI — Production Real Estate Intelligence Platform

### Next-Gen AI Residential Property Valuation & Market Intelligence Platform
Developed during the **AIML Summer Internship 2026** at **IIHMF, Motilal Nehru National Institute of Technology (MNNIT), Prayagraj**.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-0.9392%20R2-orange?logo=scikitlearn)
![Streamlit](https://img.shields.io/badge/Streamlit-Production%20UI-red?logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

---

## 📌 Project Overview

**HomeWorth AI** is an enterprise-grade AI-powered residential property valuation and investment intelligence platform. Built on empirical real-estate transaction benchmarks across 10 major Indian metropolitan areas (Mumbai, Delhi, Bengaluru, Chennai, Hyderabad, Pune, Kolkata, Ahmedabad, Jaipur, Lucknow), the platform predicts fair market prices with **93.92% accuracy** using a trained **Gradient Boosting Regressor** pipeline.

Beyond standard price calculators, HomeWorth AI provides end-to-end investment decision support:

- 🏠 **Estimated Market Value & Confidence Ranges** (Lower & Upper Bounds based on MAE)
- 📐 **Price per Square Foot** with real-time locality comp benchmarks
- 🏆 **Composite Property Score (0–100)** across 4 core pillars:
  - Location & Connectivity (25 pts)
  - Physical Specs & Architecture (25 pts)
  - Society Amenities & Lifestyle (25 pts)
  - Safety & Environmental Air Quality (25 pts)
- 📈 **Investment Rating Grade** (Grade AAA to Grade C)
- 🏷 **Market Segment Classification** (Budget, Mid-Segment Premium, Luxury, Ultra-Luxury)
- 🤖 **AI House Buying Advisor** (Categorized into Strengths, Value Drivers, Due Diligence Cautions, and Buyer Negotiation Playbook)
- 🏦 **Integrated Mortgage & Home Loan EMI Planner** (Down payment, loan tenure, interest rate, monthly EMI breakdown)
- 📊 **Real-time Market Intelligence & EDA Studio** (City price hierarchies, Area vs Price regression, Amenities premium analysis, filterable benchmark dataset explorer)
- ⚖️ **Property Comparison Studio** (Side-by-side evaluation of two properties)
- 🧠 **Explainable AI (XAI)** (Empirical model leaderboard & feature importance rankings)
- 📄 **Exportable Valuation Reports** (One-click text summary export for clients/banks)

---

## ✨ System Architecture & Modules

```
┌────────────────────────────────────────────────────────────────────────┐
│                        HomeWorth AI Architecture                       │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  [ Web Frontend: Streamlit + Modern Dark Glassmorphic Theme ]         │
│                                │                                       │
│    ┌───────────────┬───────────┴───────────┬───────────────┐           │
│    ▼               ▼                       ▼               ▼           │
│ 1. Valuation    2. Market Intelligence  3. Property     4. Model XAI   │
│    Studio       & Exploratory Data      Comparison      & Leaderboard  │
│                 Analysis (Plotly)       Studio                         │
│    │                                                       │           │
│    └───────────────────────┬───────────────────────────────┘           │
│                            ▼                                           │
│  [ Analytics Engine: predictor.py, advisor.py, utils.py ]              │
│                            │                                           │
│    ┌───────────────────────┴───────────────────────┐                   │
│    ▼                                               ▼                   │
│  [ Trained ML Pipeline ]               [ Benchmark Dataset ]           │
│  house_price_pipeline.pkl              House_Price_Prediction_         │
│  (One-Hot Encoder +                    Dataset.xlsx                    │
│   ColumnTransformer +                  (506 Properties, 34 Attributes) │
│   Gradient Boosting Regressor)                                         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🧠 Machine Learning Performance

Three candidate algorithms were trained and evaluated on an 80/20 train-test split using standard regression metrics:

| Model | MAE (₹ Lakhs) | RMSE (₹ Lakhs) | R² Score | Performance Verdict |
|---|:---:|:---:|:---:|:---:|
| **Gradient Boosting Regressor** | **10.01** | **13.85** | **0.9392** | 🏆 **Best Model (Deployed)** |
| **Linear Regression** | 13.79 | 18.42 | 0.8925 | Baseline Model |
| **Random Forest Regressor** | 15.86 | 22.00 | 0.8467 | Moderate Ensemble |

### Top Predictive Feature Drivers:
1. **Carpet Area (`Area_sqft`)**: **63.56%** contribution
2. **City Tier (Delhi, Lucknow, Bengaluru, Mumbai, Ahmedabad)**: ~**23%** combined
3. **Property Type (Villa premium)**: **2.37%**
4. **Distance to City Center**: **1.99%**
5. **Property Age & Construction**: **1.50%**

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Machine Learning:** Scikit-Learn (Pipelines, ColumnTransformer, OneHotEncoder, GradientBoostingRegressor)
- **Web App & Dashboard:** Streamlit
- **Visualization:** Plotly Express & Plotly Graph Objects
- **Data Manipulation:** Pandas, NumPy, OpenPyXL
- **Model Serialization:** Joblib
- **Styling:** Custom CSS3 (Glassmorphism, Dark Mode, Responsive Cards, Grid Layouts)

---

## 📂 Project Directory Structure

```
HousePricePrediction/
├── Dataset/
│   └── House_Price_Prediction_Dataset.xlsx    # 506 Benchmark Homes (34 features)
├── Model/
│   └── house_price_pipeline.pkl               # Serialized trained scikit-learn pipeline
├── Notebook/
│   └── EDA.ipynb                              # Research, preprocessing, EDA & training
├── Streamlit_App/
│   ├── app.py                                 # Multi-tab enterprise Streamlit application
│   ├── predictor.py                           # Model inference, range estimation & XAI
│   ├── advisor.py                             # Multi-pillar real estate advisory engine
│   ├── utils.py                               # Scoring, currency formatting, EMI planner
│   ├── style.css                              # Glassmorphic responsive dark theme
│   └── assets/
│       └── hero_banner.png                    # Brand banner asset
├── HomeWorth_AI_Project Report By Ujjaval Kumar Kesarwani & Shlok Tiwari.pdf
├── HomeWorth_AI_Presentation By Ujjaval Kumar Kesarwani & Shlok Tiwari.pdf
├── README.md                                  # Complete documentation
└── requirements.txt                           # Verified Python dependencies
```

---

## 🚀 Quickstart Installation & Execution

### 1. Clone the repository
```bash
git clone https://github.com/your-username/HomeWorth-AI.git
cd HomeWorth-AI/HousePricePrediction
```

### 2. Create and activate a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Web Application
```bash
cd Streamlit_App
streamlit run app.py
```
The application will launch automatically in your browser at `http://localhost:8501`.

---

## 👨‍💻 Project Team

- **Ujjaval Kumar Kesarwani**  
  *B.Tech Computer Science & Engineering (AI & ML)*  
  *United College of Engineering & Research (UCER)*

- **Shlok Tiwari**  
  *B.Tech Computer Science & Engineering (AI & ML)*  
  *United College of Engineering & Research (UCER)*

---

## 🎓 Academic Host & Internship

**Artificial Intelligence & Machine Learning Summer Internship 2026**  
**IIHMF** — **Motilal Nehru National Institute of Technology (MNNIT), Prayagraj**

---

## 📜 License

This project is licensed under the MIT License — open for academic, educational, and research use.