import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
N = 2000
rng = np.random.default_rng(SEED)

# Synthetic spatial clusters chosen only to make the prototype visually
# representative of a mineral-prospectivity workflow. They are NOT claims
# about actual reserves or actual mineralization.
centers = np.array([
    [21.8, 85.1],  # Odisha / Jharkhand belt-like synthetic cluster
    [22.4, 83.0],  # Central-east synthetic cluster
    [20.3, 82.8],  # Odisha/Chhattisgarh synthetic cluster
    [23.1, 84.8],  # Jharkhand synthetic cluster
    [19.3, 84.4],  # South Odisha synthetic cluster
])
cluster_scales = np.array([
    [0.75, 0.85],
    [0.65, 0.75],
    [0.70, 0.80],
    [0.55, 0.65],
    [0.55, 0.70],
])
cluster_id = rng.choice(len(centers), size=N, p=[0.28, 0.20, 0.22, 0.15, 0.15])

lat = centers[cluster_id, 0] + rng.normal(0, cluster_scales[cluster_id, 0])
lon = centers[cluster_id, 1] + rng.normal(0, cluster_scales[cluster_id, 1])
lat = np.clip(lat, 18.0, 24.0)
lon = np.clip(lon, 80.0, 87.0)

# Spatially coherent geological signal with noise.
geo_signal = np.zeros(N)
for i, (c_lat, c_lon) in enumerate(centers):
    d = ((lat - c_lat) / 1.15) ** 2 + ((lon - c_lon) / 1.25) ** 2
    geo_signal = np.maximum(geo_signal, np.exp(-0.5 * d) * (0.72 + 0.08 * i / len(centers)))

df = pd.DataFrame({
    "latitude": lat,
    "longitude": lon,
    "rainfall_mm": rng.uniform(500, 1800, N),
    "soil_moisture": rng.uniform(0.10, 0.55, N),
    "ndvi": rng.uniform(0.10, 0.85, N),
    "land_surface_temperature": rng.uniform(20, 42, N),
    "elevation_m": rng.uniform(100, 900, N),
    "geological_score": np.clip(0.12 + 0.82 * geo_signal + rng.normal(0, 0.08, N), 0, 1),
    "historical_production_tonnes": rng.uniform(1000, 50000, N),
    "equipment_efficiency": rng.uniform(0.50, 0.98, N),
})

df["prospectivity_score"] = (
    0.45 * df["geological_score"]
    + 0.20 * (1 - df["ndvi"])
    + 0.15 * df["soil_moisture"]
    + 0.10 * (df["land_surface_temperature"] / 42)
    + 0.10 * df["equipment_efficiency"]
).clip(0, 1)

base_potential = (
    50000
    + 350000 * df["prospectivity_score"]
    + 25000 * df["geological_score"]
    + 10000 * df["soil_moisture"]
)
df["predicted_manganese_reserve_tonnes"] = (
    base_potential + rng.normal(0, 5000, N)
).clip(lower=10000)

df["predicted_production_tonnes"] = (
    df["historical_production_tonnes"]
    * df["equipment_efficiency"]
    * (0.7 + 0.5 * df["prospectivity_score"])
)
df["production_shortfall_tonnes"] = (
    df["historical_production_tonnes"] - df["predicted_production_tonnes"]
).clip(lower=0)

df["risk_score"] = (
    0.35 * (1 - df["equipment_efficiency"])
    + 0.25 * (1 - df["geological_score"])
    + 0.20 * (df["production_shortfall_tonnes"] / df["historical_production_tonnes"].replace(0, 1))
    + 0.20 * (df["rainfall_mm"] / 1800)
).clip(0, 1)

df["risk_level"] = pd.cut(
    df["risk_score"],
    bins=[-np.inf, 0.30, 0.60, np.inf],
    labels=["Low", "Medium", "High"],
)

output = Path(__file__).resolve().parents[2] / "data" / "synthetic" / "manganex_dataset.csv"
output.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output, index=False)
print(f"Dataset regenerated: {output}")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
