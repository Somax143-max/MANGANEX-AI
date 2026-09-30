import json
import os
import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from prediction_engine import get_model_metadata, predict_location

app = FastAPI(
    title="MANGANEX AI Platform",
    description="Space Technology & AI Decision-Support Platform for Ministry of Steel (SIH 2026)",
    version="3.0.0",
)

# Configurable CORS
cors_origins_raw = os.getenv("CORS_ORIGINS", "*")
cors_origins = [origin.strip() for origin in cors_origins_raw.split(",") if origin.strip()] or ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = ROOT / "data" / "synthetic" / "manganex_dataset.csv"
FRONTEND_DIR = ROOT / "frontend"
FRONTEND_DIR.mkdir(exist_ok=True)

df_cache = None


def get_df():
    global df_cache
    if df_cache is None:
        if not DATA_FILE.exists():
            from generate_dataset import generate_dataset
            df_cache = generate_dataset()
        else:
            df_cache = pd.read_csv(DATA_FILE)
    return df_cache


class SimulationRequest(BaseModel):
    sentinel2_ferrous_index: float = 1.45
    sentinel2_clay_index: float = 1.30
    ndvi: float = 0.28
    land_surface_temperature: float = 34.5
    elevation_m: float = 480.0
    geological_score: float = 0.85
    ore_grade_percent: float = 42.5
    historical_production_tonnes: float = 32000.0
    equipment_efficiency: float = 0.72
    rainfall_mm: float = 1150.0


@app.get("/health")
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "MANGANEX-AI",
        "version": "3.0.0",
        "environment": os.getenv("ENVIRONMENT", "production"),
    }


@app.get("/api/summary")
def get_summary():
    df = get_df()
    total_potential = float(df["predicted_manganese_reserve_tonnes"].sum())
    total_historical = float(df["historical_production_tonnes"].sum())
    total_predicted = float(df["predicted_production_tonnes"].sum())
    total_shortfall = float(max(0, total_historical - total_predicted))
    national_gap_pct = float(round((total_shortfall / total_historical) * 100, 2)) if total_historical else 0.0
    tier1_zones = int((df["prospectivity_score"] >= 0.75).sum())
    high_risk_zones = int((df["risk_level"] == "High").sum())

    state_pot = df.groupby("state")["predicted_manganese_reserve_tonnes"].sum().to_dict()
    state_pot_mt = {k: round(v / 1e6, 2) for k, v in state_pot.items()}

    state_short = df.groupby("state")["production_shortfall_tonnes"].sum().to_dict()
    state_short_kt = {k: round(v / 1e3, 1) for k, v in state_short.items()}

    risk_counts = df["risk_level"].value_counts().to_dict()

    df_copy = df.copy()
    df_copy["efficiency_tier"] = pd.cut(
        df_copy["equipment_efficiency"],
        bins=[0, 0.60, 0.75, 0.90, 1.0],
        labels=["< 60% (Suboptimal)", "60-75% (Moderate)", "75-90% (Good)", "> 90% (High Efficiency)"]
    )
    tier_shortfall = df_copy.groupby("efficiency_tier", observed=False)["production_shortfall_tonnes"].sum().to_dict()

    top_targets = (
        df.sort_values(["prospectivity_score", "ore_grade_percent"], ascending=False)
        .head(10)
        .to_dict(orient="records")
    )

    return {
        "kpis": {
            "total_potential_tonnes": total_potential,
            "total_potential_mt": round(total_potential / 1e6, 2),
            "total_historical_tonnes": total_historical,
            "total_historical_mt": round(total_historical / 1e6, 2),
            "total_predicted_tonnes": total_predicted,
            "total_predicted_mt": round(total_predicted / 1e6, 2),
            "total_shortfall_tonnes": total_shortfall,
            "total_shortfall_mt": round(total_shortfall / 1e6, 2),
            "national_gap_pct": national_gap_pct,
            "tier1_zones_count": tier1_zones,
            "high_risk_zones_count": high_risk_zones,
            "total_zones": len(df),
            "states_count": df["state"].nunique(),
            "mining_belts_count": df["mining_belt"].nunique(),
        },
        "state_potential_mt": state_pot_mt,
        "state_shortfall_kt": state_short_kt,
        "risk_distribution": risk_counts,
        "tier_shortfall": tier_shortfall,
        "top_targets": top_targets,
    }


@app.get("/api/zones")
def get_zones(
    state: Optional[str] = None,
    min_prospectivity: float = Query(0.0, ge=0.0, le=100.0),
    min_grade: float = Query(0.0, ge=0.0, le=100.0),
    limit: int = Query(600, ge=1, le=1000),
):
    df = get_df()
    filtered = df[
        (df["prospectivity_score"] * 100 >= min_prospectivity) &
        (df["ore_grade_percent"] >= min_grade)
    ].copy()

    if state and state != "All States":
        filtered = filtered[filtered["state"] == state]

    records = filtered.head(limit).to_dict(orient="records")
    return {
        "total_matching": len(filtered),
        "zones": records,
        "available_states": ["All States"] + sorted(df["state"].unique().tolist()),
    }


@app.post("/api/predict")
def run_prediction(req: SimulationRequest):
    result = predict_location(
        sentinel2_ferrous_index=req.sentinel2_ferrous_index,
        sentinel2_clay_index=req.sentinel2_clay_index,
        ndvi=req.ndvi,
        land_surface_temperature=req.land_surface_temperature,
        elevation_m=req.elevation_m,
        geological_score=req.geological_score,
        ore_grade_percent=req.ore_grade_percent,
        historical_production_tonnes=req.historical_production_tonnes,
        equipment_efficiency=req.equipment_efficiency,
        rainfall_mm=req.rainfall_mm,
    )
    return result


@app.get("/api/metrics")
def get_metrics():
    return get_model_metadata()


# Mount static assets
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
def serve_index():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file, media_type="text/html")
    return HTMLResponse("<h1>MANGANEX AI Server Running</h1>")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    is_dev = os.environ.get("ENVIRONMENT", "development").lower() == "development"
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=is_dev)
