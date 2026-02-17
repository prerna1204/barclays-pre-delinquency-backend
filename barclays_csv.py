# barclays_csv.py

import pandas as pd


def generate_decisions():

    df = pd.read_csv("customer_data.csv")

    def assign_risk(prob):
        if prob >= 0.7:
            return "High"
        elif prob >= 0.4:
            return "Medium"
        else:
            return "Low"

    def assign_action(risk):
        if risk == "High":
            return "Immediate Relationship Manager Outreach"
        elif risk == "Medium":
            return "Financial Advisory Consultation"
        else:
            return "Continuous Monitoring"

    df["risk_category"] = df["risk_probability"].apply(assign_risk)
    df["recommended_action"] = df["risk_category"].apply(assign_action)

    final_df = df[
        [
            "customer_id",
            "risk_probability",
            "risk_category",
            "recommended_action",
        ]
    ]

    final_df.to_csv("final_output.csv", index=False)

    print("final_output.csv generated")
