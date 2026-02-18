# barclays_csv.py

import pandas as pd


def generate_decisions():

    # Load previous outputs
    base_data = pd.read_csv("customer_data.csv")
    predictions = pd.read_csv("ml_predictions.csv")

    final_rows = []

    for i in range(len(base_data)):

        row_base = base_data.iloc[i]
        row_pred = predictions.iloc[i]

        risk_prob = row_pred["risk_probability"]

        # Risk Category
        if risk_prob >= 0.7:
            risk_category = "High"
            action = "Immediate Relationship Manager Outreach"
            stress = "Stressed"

        elif risk_prob >= 0.4:
            risk_category = "Medium"
            action = "Financial Counseling"
            stress = "Moderate"

        else:
            risk_category = "Low"
            action = "Continuous Monitoring"
            stress = "Stable"

        final_row = {
            "customer_id": int(row_base["customer_id"]),

            "salary_delay_days": int(row_base["salary_delay_days"]),

            "credit_utilization": float(row_base["credit_utilization"]),

            "emi_to_income_ratio": float(row_base["emi_to_income_ratio"]),

            "risk_score": int(row_base["risk_score"]),

            "composite_risk_index": round(float(row_base["composite_risk_index"]), 2),

            "risk_probability": round(float(risk_prob), 2),

            "risk_category": risk_category,

            "financial_stress": stress,

            "recommended_action": action,
        }

        final_rows.append(final_row)

    final_df = pd.DataFrame(final_rows)

    final_df.to_csv("final_output.csv", index=False)

    print("final_output.csv generated successfully")
