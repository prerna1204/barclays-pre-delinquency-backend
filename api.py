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

    # 🔹 DEBUG: show real column names
    print("CSV COLUMNS:", list(df.columns))

    return {
        "status": "Success",
        "columns": list(df.columns),   # <-- send columns to frontend
        "total_customers": len(df),
        "data": df.to_dict(orient="records"),
    }
