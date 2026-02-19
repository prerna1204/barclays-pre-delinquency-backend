import pandas as pd


def get_risk_category(score):
    if score >= 80:
        return "High"
    elif score >= 50:
        return "Medium"
    else:
        return "Low"


def recommend(row):
    if row["risk_category"] == "High":
        return "Immediate Relationship Manager Outreach"
    elif row["risk_category"] == "Medium":
        return "Targeted Financial Counseling"
    else:
        return "Continuous Monitoring"


def generate_decisions():

    print("Generating decisions...")

    # Load ML output file
    df = pd.read_csv("customer_data.csv")

    print("Columns before processing:", df.columns.tolist())

    # -----------------------------
    # Create risk_score if missing
    # -----------------------------
    if "risk_score" not in df.columns:

        if "risk_probability" in df.columns:
            df["risk_score"] = (df["risk_probability"] * 100).round().astype(int)
            print("risk_score created from risk_probability")

        else:
            # Fallback safety
            df["risk_score"] = 50
            print("Default risk_score assigned")

    # -----------------------------
    # Create risk_category
    # -----------------------------
    df["risk_category"] = df["risk_score"].apply(get_risk_category)

    # -----------------------------
    # Create recommended_action
    # -----------------------------
    df["recommended_action"] = df.apply(recommend, axis=1)

    # -----------------------------
    # Add missing optional columns safely
    # -----------------------------
    optional_cols = [
        "salary_delay_days",
        "credit_utilization",
        "emi_to_income_ratio",
        "financial_stress",
        "composite_risk_index"
    ]

    for col in optional_cols:
        if col not in df.columns:
            df[col] = 0
            print(f"{col} added as default")

    # -----------------------------
    # Final columns order
    # -----------------------------
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

    # Save output
    final_df.to_csv("final_output.csv", index=False)

    print("final_output.csv generated successfully")
