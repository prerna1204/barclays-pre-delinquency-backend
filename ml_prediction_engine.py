# ml_prediction_engine.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def run_ml_model():

    df = pd.read_csv("customer_data.csv")

    X = df.drop(["financial_stress_flag"], axis=1)
    y = df["financial_stress_flag"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    df["risk_probability"] = model.predict_proba(X)[:, 1]

    df.to_csv("customer_data.csv", index=False)

    print("ML risk probabilities generated")
