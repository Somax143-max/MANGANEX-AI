import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "synthetic" / "manganex_dataset.csv"
MODEL_DIR = ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA)

# -------------------------------------------------------------
# 1. Manganese Potential / Reserve Model (Random Forest Regressor)
# Features: Space Tech (Ferrous, Clay, NDVI, LST, DEM) + Geological Score
# -------------------------------------------------------------
reserve_features = [
    "sentinel2_ferrous_index",
    "sentinel2_clay_index",
    "ndvi",
    "land_surface_temperature",
    "elevation_m",
    "geological_score",
    "ore_grade_percent",
]
X_res = df[reserve_features]
y_res = df["predicted_manganese_reserve_tonnes"]

X_train_res, X_test_res, y_train_res, y_test_res = train_test_split(
    X_res, y_res, test_size=0.2, random_state=42
)
reserve_model = RandomForestRegressor(n_estimators=300, max_depth=12, random_state=42, n_jobs=-1)
reserve_model.fit(X_train_res, y_train_res)
pred_res = reserve_model.predict(X_test_res)

res_mae = float(mean_absolute_error(y_test_res, pred_res))
res_r2 = float(r2_score(y_test_res, pred_res))
print(f"Manganese Potential Model | MAE: {res_mae:,.2f} t | R²: {res_r2:.4f}")
joblib.dump(reserve_model, MODEL_DIR / "reserve_model.joblib")

# Feature importances
res_importances = dict(zip(reserve_features, [round(float(v), 4) for v in reserve_model.feature_importances_]))

# -------------------------------------------------------------
# 2. Production Shortfall Model (Random Forest Regressor)
# Features: Historical Output + Equipment Efficiency + Rainfall + Space/Geo
# -------------------------------------------------------------
shortfall_features = [
    "historical_production_tonnes",
    "equipment_efficiency",
    "rainfall_mm",
    "soil_moisture",
    "geological_score",
    "elevation_m",
]
X_short = df[shortfall_features]
y_short = df["production_shortfall_tonnes"]

X_train_short, X_test_short, y_train_short, y_test_short = train_test_split(
    X_short, y_short, test_size=0.2, random_state=42
)
production_model = RandomForestRegressor(n_estimators=300, max_depth=12, random_state=42, n_jobs=-1)
production_model.fit(X_train_short, y_train_short)
pred_short = production_model.predict(X_test_short)

short_mae = float(mean_absolute_error(y_test_short, pred_short))
short_r2 = float(r2_score(y_test_short, pred_short))
print(f"Production Shortfall Model | MAE: {short_mae:,.2f} t | R²: {short_r2:.4f}")
joblib.dump(production_model, MODEL_DIR / "production_shortfall_model.joblib")

short_importances = dict(zip(shortfall_features, [round(float(v), 4) for v in production_model.feature_importances_]))

# -------------------------------------------------------------
# 3. Operational & Mine Risk Model (Random Forest Classifier)
# -------------------------------------------------------------
risk_features = [
    "production_shortfall_tonnes",
    "equipment_efficiency",
    "rainfall_mm",
    "soil_moisture",
    "geological_score",
]
X_risk = df[risk_features]
y_risk = df["risk_level"].astype(str)

X_train_risk, X_test_risk, y_train_risk, y_test_risk = train_test_split(
    X_risk, y_risk, test_size=0.2, random_state=42, stratify=y_risk
)
risk_model = RandomForestClassifier(n_estimators=300, max_depth=10, random_state=42, n_jobs=-1)
risk_model.fit(X_train_risk, y_train_risk)
pred_risk = risk_model.predict(X_test_risk)

risk_acc = float(accuracy_score(y_test_risk, pred_risk))
print(f"Operational Risk Model | Accuracy: {risk_acc*100:.2f}%")
joblib.dump(risk_model, MODEL_DIR / "risk_model.joblib")

risk_importances = dict(zip(risk_features, [round(float(v), 4) for v in risk_model.feature_importances_]))

# -------------------------------------------------------------
# Save Metrics & Metadata for Live XAI Display in Dashboard
# -------------------------------------------------------------
metrics_payload = {
    "reserve_model": {
        "algorithm": "Random Forest Regressor (300 Estimators)",
        "features": reserve_features,
        "mae": round(res_mae, 2),
        "r2_score": round(res_r2, 4),
        "feature_importances": res_importances,
    },
    "shortfall_model": {
        "algorithm": "Random Forest Regressor (300 Estimators)",
        "features": shortfall_features,
        "mae": round(short_mae, 2),
        "r2_score": round(short_r2, 4),
        "feature_importances": short_importances,
    },
    "risk_model": {
        "algorithm": "Random Forest Classifier (300 Estimators)",
        "features": risk_features,
        "accuracy": round(risk_acc, 4),
        "classes": list(risk_model.classes_),
        "feature_importances": risk_importances,
    },
    "total_training_samples": len(df),
    "geographical_belts": df["mining_belt"].nunique(),
    "states_covered": df["state"].nunique(),
}

with open(MODEL_DIR / "model_metrics.json", "w") as f:
    json.dump(metrics_payload, f, indent=2)

print("All MANGANEX AI models and metrics saved successfully.")
