# main.py

from data_generator import generate_data
from ml_prediction_engine import run_ml_model
from barclays_csv import generate_decisions


def run_pipeline():

    print("BARCLAYS RISK PIPELINE STARTED")

    generate_data()
    run_ml_model()
    generate_decisions()

    print("PIPELINE COMPLETED")


if __name__ == "__main__":
    run_pipeline()
