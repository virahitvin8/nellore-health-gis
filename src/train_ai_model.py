"""
AI/Machine Learning Pipeline for Health GIS: Nellore City & Kovur Mandal
Trains Random Forest Classifier to predict Zoonotic & Geo-Risk Categories.
Outputs Evaluation Metrics, Confusion Matrix, and Feature Importances.
"""

import json
import pickle
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")

def train_risk_prediction_model():
    geojson_path = os.path.join(DATA_DIR, "risk_analysis", "market_geo_risk_classified.geojson")
    with open(geojson_path) as f:
        data = json.load(f)

    records = [f["properties"] for f in data["features"]]
    df = pd.DataFrame(records)

    # Feature Engineering
    # Encode binary & categorical variables
    df["slaughter_flag"] = (df["slaughter_on_site"] == "Yes").astype(int)
    df["refrig_flag"] = (df["refrigeration_available"] == "Yes").astype(int)

    waste_map = {
        "Direct Open Drain Discharge": 3,
        "Open Dumping on Ground": 2,
        "Municipal Waste Bin": 1,
        "Closed Bin Collection": 0
    }
    df["waste_severity_score"] = df["waste_disposal_method"].map(waste_map).fillna(1)

    cat_map = {
        "Mixed Live Meat & Fish": 3,
        "Poultry (Broiler/Country Chicken)": 2,
        "Mutton / Sheep / Goat": 1,
        "Fish & Seafood": 0
    }
    df["category_code"] = df["category"].map(cat_map).fillna(0)

    feature_cols = [
        "distance_to_drain_m",
        "distance_to_waterbody_m",
        "distance_to_hospital_m",
        "daily_animals_handled",
        "market_crowd_index",
        "slaughter_flag",
        "refrig_flag",
        "waste_severity_score",
        "category_code"
    ]

    X = df[feature_cols]
    y = df["risk_level"]

    # Stratified Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    # Train Random Forest Classifier
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        min_samples_split=3,
        random_state=42
    )
    rf.fit(X_train, y_train)

    # Predictions & Evaluation
    y_pred = rf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    cv_scores = cross_val_score(rf, X, y, cv=5)
    report = classification_report(y_test, y_pred, output_dict=True)
    labels = sorted(list(y.unique()))
    cm = confusion_matrix(y_test, y_pred, labels=labels).tolist()

    # Feature Importances
    importances = rf.feature_importances_
    feat_imp = sorted(
        [{"feature": col, "importance": round(float(imp), 4)} for col, imp in zip(feature_cols, importances)],
        key=lambda x: x["importance"],
        reverse=True
    )

    print(f"Random Forest Training Successful!")
    print(f"Test Accuracy: {acc * 100:.2f}%")
    print(f"5-Fold Cross Validation Mean: {cv_scores.mean() * 100:.2f}%")
    print("\nTop Predictive Risk Factors:")
    for item in feat_imp:
        print(f" - {item['feature']}: {item['importance'] * 100:.2f}%")

    # Save Model Artifacts
    with open(os.path.join(MODEL_DIR, "risk_predictor_random_forest.pkl"), "wb") as f:
        pickle.dump(rf, f)

    metrics_output = {
        "model_type": "Random Forest Classifier (100 Estimators)",
        "test_accuracy": round(float(acc), 4),
        "cross_val_mean_accuracy": round(float(cv_scores.mean()), 4),
        "confusion_matrix": {
            "labels": labels,
            "matrix": cm
        },
        "classification_report": report,
        "feature_importances": feat_imp
    }

    with open(os.path.join(MODEL_DIR, "model_evaluation_metrics.json"), "w") as f:
        json.dump(metrics_output, f, indent=2)

    with open(os.path.join(MODEL_DIR, "feature_importance.json"), "w") as f:
        json.dump(feat_imp, f, indent=2)

    # Apply AI Predictions to full dataset
    all_preds = rf.predict(X)
    all_probs = rf.predict_proba(X)
    class_order = list(rf.classes_)

    for idx, feat in enumerate(data["features"]):
        pred_label = all_preds[idx]
        conf = float(np.max(all_probs[idx]))
        feat["properties"]["ai_predicted_risk"] = pred_label
        feat["properties"]["ai_prediction_confidence"] = round(conf * 100, 1)
        feat["properties"]["ai_concurrence"] = "True" if pred_label == feat["properties"]["risk_level"] else "False"

    # Save updated GeoJSON
    with open(geojson_path, "w") as f:
        json.dump(data, f, indent=2)

    print("Updated GeoJSON with AI Model Predictions & Confidence Scores!")

if __name__ == "__main__":
    train_risk_prediction_model()
