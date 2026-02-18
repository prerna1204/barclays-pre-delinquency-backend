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

    # Read final CSV
    df = pd.read_csv("final_output.csv")

    # Rename CSV columns to match frontend
    df = df.rename(columns={
        "customer_id": "id",
        "salary_delay_days": "salaryDelayDays",
        "credit_utilization": "creditUtilization",
        "emi_to_income_ratio": "emiToIncomeRatio",
        "risk_score": "riskScore",
        "composite_risk_index": "compositeRiskIndex",
        "risk_category": "riskCategory",
        "recommended_action": "recommendedAction",
        "financial_stress_status": "financialStressStatus"
    })

    # Convert to JSON
    data = df.to_dict(orient="records")

    return {
        "status": "Success",
        "total_customers": len(df),
        "data": data
    }
