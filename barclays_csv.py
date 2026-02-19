# barclays_csv.py

import pandas as pd


def generate_decisions():

    # Read previous stage data
    try:
        df = pd.read_csv("customer_data.csv")
    except:
        raise Exception("customer_data.csv not found. Pipeline failed.")

    # Generate Risk Category
    def get_risk_category(score):
        if score >= 75:
            return "High"
        elif score >= 40:
            return "Medium"
        else:
            return "Low"

    # Generate Recommended Action
    def recommend(row):
        if row["risk_category"] == "High":
            return "Immediate Relationship Manager Outreach"
        elif row["risk_category"] == "Medium":
            return "Targeted Financial Counseling"
        else:
            return "Continuous Monitoring"

    # Risk Category
    df["risk_category"] = df["risk_score"].apply(get_risk_category)

    # Risk Probability (simple normalized version)
    df["risk_probability"] = df["risk_score"] / 100

    # Composite Risk Index
    df["composite_risk_index"] = (
        0.3 * df["credit_utilization"] +
        0.3 * df["emi_to_income_ratio"] +
        0.4 * df["risk_probability"]
    )

    # Financial Stress
    def stress_status(row):
        if row["risk_score"] >= 75:
            return "Stressed"
        elif row["risk_score"] >= 40:
            return "Moderate"
        else:
            return "Stable"

    df["financial_stress"] = df.apply(stress_status, axis=1)

    # Recommended Action
    df["recommended_action"] = df.apply(recommend, axis=1)

    # Final Columns
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

    # Save Final Output
    final_df.to_csv("final_output.csv", index=False)

    print("final_output.csv generated successfully with full columns")
