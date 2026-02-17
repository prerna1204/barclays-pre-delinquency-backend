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

    run_pipeline()

    df = pd.read_csv("final_output.csv")

    return {
        "status": "Success",
        "total_customers": len(df),
        "data": df.to_dict(orient="records"),
    }
