from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

from main import run_pipeline

app = FastAPI(title="Pre-Delinquency Risk API")

# Allow frontend access
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

    try:
        # Step 1: Run pipeline (creates CSV)
        run_pipeline()

        file_path = "final_output.csv"

        # Step 2: Check if file exists
        if not os.path.exists(file_path):
            return {
                "status": "Error",
                "message": "final_output.csv not found after pipeline run"
            }

        # Step 3: Read CSV
        df = pd.read_csv(file_path)

        # Step 4: Handle empty file
        if df.empty:
            return {
                "status": "Error",
                "message": "final_output.csv is empty"
            }

        # Step 5: Return safe response
        return {
            "status": "Success",
            "columns": list(df.columns),
            "total_customers": len(df),
            "data": df.to_dict(orient="records"),
        }

    except Exception as e:
        # Never crash → always return error message
        return {
            "status": "Error",
            "message": str(e)
        }
