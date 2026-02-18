# barclays_csv.py

import pandas as pd


def generate_decisions():

    # Load raw customer data
    raw_df = pd.read_csv("customer_data.csv")

    # Load ML prediction output
    ml_df = pd.read_csv("ml_output.csv")

    # Merge both on customer_id
    df = pd.merge(raw_df, ml_df, on="customer_id", how="inner")

    # Calculate composite risk index (example formula)
    df["composite_risk_index"] = (
        (df["risk_probability"] * 0.4)
        + (df["credit_utilization"] * 0.3)
        + (df["emi_to_income_ratio"] * 0.3)
    ).round(2)

    # Financial stress classification
    def stress_label(row):
        if row["composite_risk_index"] >= 0.7:
            return "High"
        elif row["composite_risk_index"] >= 0.4:
            return "Moderate"
        else:
            return "Low"

    df["financial_stress"] = df.apply(stress_label, axis=1)

    # Recommended actions
    def recommend(row):
        if row["risk_category"] == "High":
            return "Immediate Relationship Manager Outreach"
        elif row["risk_category"] == "Medium":
            return "Targeted Financial Counseling"
        else:
            return "Continuous Monitoring"

    df["recommended_action"] = df.apply(recommend, axis=1)

    # Select final columns
    final_df = df[
        [
            "customer_id",
            "salary_delay_days",
            "credit_utilization",
            "emi_to_income_ratio",
            "risk_score",
            "risk_probability",
            "risk_category",
            "composite_risk_index",
            "financial_stress",
            "recommended_action",
        ]
    ]

    # Save final output
    final_df.to_csv("final_output.csv", index=False)

    print("final_output.csv generated successfully")
