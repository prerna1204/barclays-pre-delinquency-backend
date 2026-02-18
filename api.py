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

    # Load final CSV
    df = pd.read_csv("final_output.csv")

    # Rename CSV columns for frontend
    df = df.rename(columns={
        "customer_id": "id",
        "salary_delay": "salaryDelayDays",
        "credit_utilization": "creditUtilization",
        "emi_to_income": "emiToIncomeRatio",
        "risk_score": "riskScore",
        "composite_index": "compositeRiskIndex",
        "risk_category": "riskCategory"
    })

    return {
        "status": "Success",
        "total_customers": len(df),
        "data": df.to_dict(orient="records"),
    }
