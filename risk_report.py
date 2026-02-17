# risk_report.py

import pandas as pd


def show_top_10(risk_level="High"):

    df = pd.read_csv("final_output.csv")

    df_filtered = df[df["risk_category"] == risk_level]
    df_sorted = df_filtered.sort_values(
        by="risk_probability", ascending=False
    ).head(10)

    print(f"\nTOP 10 {risk_level.upper()} RISK CUSTOMERS\n")
    print(df_sorted)


if __name__ == "__main__":
    show_top_10("High")
