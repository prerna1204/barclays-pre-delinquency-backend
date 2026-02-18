# api.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from main import run_pipeline


app = FastAPI(title="Pre-Delinquency Risk API")


# Enable CORS (for frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/")
def home():
    return {"message": "Risk Intelligence API Running"}


# Main API endpoint
@app.post("/run-analysis")
def run_analysis():

    # Run full backend pipeline
    run_pipeline()

    # Load final CSV
    df = pd.read_csv("final_output.csv")

    # Return complete structured data
    return {
        "status": "Success",
        "columns": list(df.columns),
        "total_customers": len(df),
        "data": df.to_dict(orient="records"),
    }
