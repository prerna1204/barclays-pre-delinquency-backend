# api.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from main import run_pipeline
import os

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

    # Run Pipeline
    run_pipeline()

    # Check CSV Exists
    if not os.path.exists("final_output.csv"):
        return {
            "status": "Error",
            "message": "final_output.csv not found. Pipeline failed."
        }

    # Read CSV
    df = pd.read_csv("final_output.csv")

    return {
        "status": "Success",
        "columns": list(df.columns),
        "total_customers": len(df),
        "data": df.to_dict(orient="records"),
    }
