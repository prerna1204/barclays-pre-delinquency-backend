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

    # Load base customer data
    base_df = pd.read_csv("customer_data.csv")

    # Load ML output
    ml_df = pd.read_csv("final_output.csv")

    # Merge on id
    df = pd.merge(
        base_df,
        ml_df,
        on="id",
        how="left"
    )

    # Standardize column names for frontend
    df = df.rename(columns={

        # Base CSV
        "id": "customerId",
        "salary_delay": "salaryDelayDays",
        "credit_util": "creditUtilization",
        "emi_ratio": "emiToIncomeRatio",
        "risk_score": "riskScore",
        "composite_index": "compositeRiskIndex",
        "financial_stress": "financialStress",

        # ML output
        "risk_probability": "riskProbability",
        "risk_category": "riskCategory",
        "recommended_action": "recommendedAction"

    })

    # Optional: Fill missing values
    df = df.fillna(0)

    return {
        "status": "Success",
        "total_customers": len(df),
        "columns": list(df.columns),
        "data": df.to_dict(orient="records")
    }
