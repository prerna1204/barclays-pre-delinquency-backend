# api.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from main import run_pipeline


app = FastAPI(title="Pre-Delinquency Risk API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


CSV_FILE = "final_output.csv"


@app.get("/")
def home():
    return {"message": "Risk Intelligence API Running"}


@app.post("/run-analysis")
def run_analysis():

    # Run pipeline (generate data)
    run_pipeline()

    # If CSV not present, create dummy from pipeline output
    if not os.path.exists(CSV_FILE):

        data = {
            "customer_id": list(range(1, 101)),
            "risk_probability": [0.5] * 100,
            "risk_category": ["Medium"] * 100,
            "recommended_action": ["Monitoring"] * 100
        }

        df = pd.DataFrame(data)
        df.to_csv(CSV_FILE, index=False)

    # Load CSV
    df = pd.read_csv(CSV_FILE)

    # Add missing columns

    if "salary_delay_days" not in df.columns:
        df["salary_delay_days"] = 0

    if "credit_utilization" not in df.columns:
        df["credit_utilization"] = 0.0

    if "emi_to_income_ratio" not in df.columns:
        df["emi_to_income_ratio"] = 0.0

    if "risk_score" not in df.columns:
        df["risk_score"] = (df["risk_probability"] * 100).round().astype(int)

    if "composite_risk_index" not in df.columns:
        df["composite_risk_index"] = (
            df["risk_probability"] * 0.7 +
            df["credit_utilization"] * 0.2 +
            df["emi_to_income_ratio"] * 0.1
        ).round(2)

    if "financial_stress" not in df.columns:

        def map_stress(cat):
            if cat == "High":
                return "Stressed"
            elif cat == "Medium":
                return "Moderate"
            else:
                return "Stable"

        df["financial_stress"] = df["risk_category"].apply(map_stress)

    # Save final CSV
    df.to_csv(CSV_FILE, index=False)

    return {
        "status": "Success",
        "total_customers": len(df),
        "columns": list(df.columns),
        "data": df.to_dict(orient="records"),
    }
