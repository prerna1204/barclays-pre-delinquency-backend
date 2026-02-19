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

    # Load ML output
    df = pd.read_csv("customer_data.csv")

    print("Initial columns:", df.columns.tolist())

    # -------------------------
    # Create risk_score safely
    # -------------------------
    if "risk_score" not in df.columns:

        if "risk_probability" in df.columns:
            df["risk_score"] = (df["risk_probability"] * 100).round().astype(int)
            print("risk_score generated from risk_probability")

        else:
            df["risk_score"] = 50
            print("Default risk_score assigned")

    # -------------------------
    # Create risk_category
    # -------------------------
    df["risk_category"] = df["risk_score"].apply(get_risk_category)

    # -------------------------
    # Recommended action
    # -------------------------
    df["recommended_action"] = df.apply(recommend, axis=1)

    # -------------------------
    # Add missing columns
    # -------------------------
    default_columns = {
        "salary_delay_days": 0,
        "credit_utilization": 0,
        "emi_to_income_ratio": 0,
        "financial_stress": 0,
        "composite_risk_index": 0,
    }

    for col, default in default_columns.items():
        if col not in df.columns:
            df[col] = default
            print(f"{col} added with default value")

    # -------------------------
    # Final Output
    # -------------------------
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

    final_df.to_csv("final_output.csv", index=False)

    print("final_output.csv generated successfully")
