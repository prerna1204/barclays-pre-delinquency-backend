# api.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from main import run_pipeline


app = FastAPI(title="Pre-Delinquency Risk API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Risk Intelligence API Running"}


@app.post("/run-analysis")
def run_analysis():

    # Run pipeline
    run_pipeline()

    # Load CSV
    df = pd.read_csv("final_output.csv")

    # Add missing columns safely (if not present)

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

        def stress_mapper(row):
            if row["risk_category"] == "High":
                return "Stressed"
            elif row["risk_category"] == "Medium":
                return "Moderate"
            else:
                return "Stable"

        df["financial_stress"] = df.apply(stress_mapper, axis=1)

    # Save updated CSV
    df.to_csv("final_output.csv", index=False)

    return {
        "status": "Success",
        "total_customers": len(df),
        "columns": list(df.columns),
        "data": df.to_dict(orient="records"),
    }
