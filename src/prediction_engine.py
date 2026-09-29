import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = ROOT / "models"

reserve_model = joblib.load(MODEL_DIR / "reserve_model.joblib")
production_model = joblib.load(MODEL_DIR / "production_shortfall_model.joblib")
risk_model = joblib.load(MODEL_DIR / "risk_model.joblib")

METRICS_FILE = MODEL_DIR / "model_metrics.json"


def get_model_metadata():
    if METRICS_FILE.exists():
        with open(METRICS_FILE, "r") as f:
            return json.load(f)
    return {
        "reserve_model": {"algorithm": "Random Forest Regressor"},
        "shortfall_model": {"algorithm": "Random Forest Regressor"},
        "risk_model": {"algorithm": "Random Forest Classifier"},
    }


def predict_location(
    sentinel2_ferrous_index: float,
    sentinel2_clay_index: float,
    ndvi: float,
    land_surface_temperature: float,
    elevation_m: float,
    geological_score: float,
    ore_grade_percent: float,
    historical_production_tonnes: float,
    equipment_efficiency: float,
    rainfall_mm: float = 1100.0,
    soil_moisture: float = 0.28,
):
    """
    End-to-end MANGANEX AI Inference Pipeline:
    1. Transparent Space Tech + Geological Prospectivity Scoring
    2. Random Forest Potential (tonnes) Regressor
    3. Random Forest Shortfall (tonnes) Regressor
    4. Random Forest Operational Risk Classifier
    5. Explainable AI Driver Decomposition & Strategic Recommendations
    """
    # 1. Prospectivity Scoring
    prospectivity_raw = (
        0.35 * geological_score
        + 0.25 * (sentinel2_ferrous_index / 2.0)
        + 0.15 * (sentinel2_clay_index / 1.8)
        + 0.15 * (1.0 - ndvi)
        + 0.10 * (land_surface_temperature / 42.0)
    )
    prospectivity = float(np.clip(prospectivity_raw, 0.05, 0.99))
    prospectivity_pct = round(prospectivity * 100, 2)

    # 2. Reserve / Potential Model Input
    res_input = pd.DataFrame([{
        "sentinel2_ferrous_index": sentinel2_ferrous_index,
        "sentinel2_clay_index": sentinel2_clay_index,
        "ndvi": ndvi,
        "land_surface_temperature": land_surface_temperature,
        "elevation_m": elevation_m,
        "geological_score": geological_score,
        "ore_grade_percent": ore_grade_percent,
    }])
    estimated_potential = float(reserve_model.predict(res_input)[0])
    estimated_potential = max(40000.0, estimated_potential)

    # 3. Production Shortfall Model Input
    short_input = pd.DataFrame([{
        "historical_production_tonnes": historical_production_tonnes,
        "equipment_efficiency": equipment_efficiency,
        "rainfall_mm": rainfall_mm,
        "soil_moisture": soil_moisture,
        "geological_score": geological_score,
        "elevation_m": elevation_m,
    }])
    predicted_shortfall = float(production_model.predict(short_input)[0])
    predicted_shortfall = max(0.0, min(predicted_shortfall, historical_production_tonnes * 0.75))
    predicted_production = max(0.0, historical_production_tonnes - predicted_shortfall)
    production_gap_pct = (
        round((predicted_shortfall / historical_production_tonnes) * 100, 2)
        if historical_production_tonnes > 0 else 0.0
    )

    # 4. Operational Risk Classifier
    risk_input = pd.DataFrame([{
        "production_shortfall_tonnes": predicted_shortfall,
        "equipment_efficiency": equipment_efficiency,
        "rainfall_mm": rainfall_mm,
        "soil_moisture": soil_moisture,
        "geological_score": geological_score,
    }])
    risk_level = str(risk_model.predict(risk_input)[0])

    # Confidence Score (%)
    confidence = float(np.clip(
        72.0 + 22.0 * geological_score - 10.0 * abs(ndvi - 0.35) + 6.0 * (sentinel2_ferrous_index / 2.0),
        62.0, 98.8
    ))

    # 5. Transparent Explainable AI (XAI) Signal Contributions
    prospectivity_signals = [
        {
            "Signal": "Geological Formation Score",
            "Contribution": round(0.35 * geological_score, 3),
            "Category": "Geological",
            "Description": "Host rock & fault contact mineralization probability",
        },
        {
            "Signal": "Sentinel-2 Ferrous Oxide (SWIR/NIR)",
            "Contribution": round(0.25 * (sentinel2_ferrous_index / 2.0), 3),
            "Category": "Space Tech",
            "Description": "Band 11/8A ratio detecting iron-manganese gossan caps",
        },
        {
            "Signal": "Sentinel-2 Clay Minerals (SWIR)",
            "Contribution": round(0.15 * (sentinel2_clay_index / 1.8), 3),
            "Category": "Space Tech",
            "Description": "Band 11/12 ratio indicating hydrothermal alteration",
        },
        {
            "Signal": "Vegetation Stress (1 - NDVI)",
            "Contribution": round(0.15 * (1.0 - ndvi), 3),
            "Category": "Space Tech",
            "Description": "Suppressed canopy reflectance over metal-rich outcrop",
        },
        {
            "Signal": "Landsat Thermal LST Factor",
            "Contribution": round(0.10 * (land_surface_temperature / 42.0), 3),
            "Category": "Space Tech",
            "Description": "Thermal inertia signature of exposed lithology",
        },
    ]

    # Strategic Actionable Recommendations (Ministry of Steel / Mine Operator)
    recommendations = []
    if prospectivity_pct >= 75.0:
        recommendations.append(
            "Priority Tier-1 Exploration Target: Strong multispectral ferrous/clay anomalies combined with favorable lithology. Recommend core drilling and geophysical IP surveys."
        )
    elif prospectivity_pct >= 50.0:
        recommendations.append(
            "Tier-2 Exploration Prospect: Moderate satellite alteration signals. Recommend high-resolution UAV multispectral mapping and soil geochemistry sampling."
        )
    else:
        recommendations.append(
            "Low Prospectivity Indicator: Background spectral signature. Baseline monitoring recommended before allocating exploratory drilling capital."
        )

    if predicted_shortfall > 6000:
        recommendations.append(
            f"Severe Supply Deficit Warning: Predicted shortfall of {predicted_shortfall:,.0f} tonnes ({production_gap_pct}% gap). Urgent overhaul of fleet dispatch and crushing plant maintenance required."
        )
    elif predicted_shortfall > 1500:
        recommendations.append(
            f"Moderate Production Deficit: Predicted shortfall of {predicted_shortfall:,.0f} tonnes. Optimize bench face extraction sequencing to stabilize feed grade."
        )
    else:
        recommendations.append(
            "Production Output on Track: Projected delivery matches historical baselines with minimal operational slippage."
        )

    if risk_level == "High":
        recommendations.append(
            "High Operational Risk Zone: Inadequate equipment uptime or heavy weather vulnerability detected. Implement automated fleet monitoring and slope stability sensors."
        )
    elif risk_level == "Medium":
        recommendations.append(
            "Medium Operational Risk: Periodic maintenance scheduling and monsoon drainage auditing advised."
        )
    else:
        recommendations.append(
            "Low Operational Risk: Operational parameters within optimal safety and productivity thresholds."
        )

    return {
        "prospectivity_score": round(prospectivity, 4),
        "prospectivity_percent": prospectivity_pct,
        "confidence_score": round(confidence, 1),
        "estimated_reserve_tonnes": round(estimated_potential, 0),
        "predicted_production_tonnes": round(predicted_production, 0),
        "predicted_shortfall_tonnes": round(predicted_shortfall, 0),
        "production_gap_percent": production_gap_pct,
        "risk_level": risk_level,
        "recommendations": recommendations,
        "prospectivity_signals": prospectivity_signals,
    }


if __name__ == "__main__":
    res = predict_location(
        sentinel2_ferrous_index=1.45,
        sentinel2_clay_index=1.30,
        ndvi=0.28,
        land_surface_temperature=34.5,
        elevation_m=480.0,
        geological_score=0.88,
        ore_grade_percent=42.5,
        historical_production_tonnes=35000.0,
        equipment_efficiency=0.72,
    )
    print("Test inference successful:")
    print(json.dumps(res, indent=2))
