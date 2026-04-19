"""
Model training pipeline for Sales Lead Scorer.
"""

import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

def train(data_path: str, model_path: str = "model/lead_scorer.pkl"):
    df = pd.read_csv(data_path)
    X = df.drop(columns=["converted"])
    y = df["converted"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = GradientBoostingClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    print(classification_report(y_test, model.predict(X_test)))
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
