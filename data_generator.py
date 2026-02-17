# data_generator.py

import pandas as pd
import numpy as np


def generate_data():

    np.random.seed(42)

    n = 500

    data = {
        "customer_id": range(1, n + 1),
        "salary_delay_days": np.random.randint(0, 10, n),
        "savings_drop_percent": np.random.randint(0, 40, n),
        "credit_utilization_ratio": np.random.uniform(0.1, 0.95, n),
        "EMI_to_income_ratio": np.random.uniform(0.1, 0.7, n),
        "number_of_late_payments_last_6m": np.random.randint(0, 6, n),
        "atm_withdrawal_increase": np.random.randint(0, 50, n),
        "debt_to_income_ratio": np.random.uniform(0.1, 0.9, n),
    }

    df = pd.DataFrame(data)

    # Simple stress logic for target
    df["financial_stress_flag"] = (
        (df["credit_utilization_ratio"] > 0.7)
        | (df["EMI_to_income_ratio"] > 0.5)
        | (df["salary_delay_days"] > 5)
    ).astype(int)

    df.to_csv("customer_data.csv", index=False)

    print("customer_data.csv generated")
