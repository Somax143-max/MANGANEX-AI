import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "synthetic"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "manganex_dataset.csv"

# Real Indian Manganese Belts & Representative Mining Hubs
MINING_HUBS = [
    # Madhya Pradesh (Balaghat - Chhindwara Belt) - India's richest Mn belt
    {"state": "Madhya Pradesh", "district": "Balaghat", "belt": "Sausar Group (Balaghat Belt)", "base_lat": 21.81, "base_lon": 80.18, "formation": "Gondite / Sausar Metasediments", "base_grade": 44.5, "base_pot": 420000},
    {"state": "Madhya Pradesh", "district": "Balaghat (Bharveli)", "belt": "Bharveli Deep Underground", "base_lat": 21.87, "base_lon": 80.23, "formation": "Manganese Ore Bedding (MOIL Core)", "base_grade": 46.0, "base_pot": 510000},
    {"state": "Madhya Pradesh", "district": "Chhindwara", "belt": "Chhindwara-Gowari Wadhona", "base_lat": 21.65, "base_lon": 78.85, "formation": "Sausar Supergroup Calc-silicate", "base_grade": 38.0, "base_pot": 290000},
    
    # Maharashtra (Nagpur - Bhandara Belt)
    {"state": "Maharashtra", "district": "Nagpur (Mansar)", "belt": "Mansar-Kandri Belt", "base_lat": 21.40, "base_lon": 79.28, "formation": "Mansar Schist / Gondite", "base_grade": 41.5, "base_pot": 380000},
    {"state": "Maharashtra", "district": "Nagpur (Gumgaon)", "belt": "Gumgaon-Ramdongri", "base_lat": 21.42, "base_lon": 79.03, "formation": "Gondite Quartzite Series", "base_grade": 40.0, "base_pot": 340000},
    {"state": "Maharashtra", "district": "Bhandara (Dongri Buzurg)", "belt": "Dongri Buzurg-Chikla", "base_lat": 21.55, "base_lon": 79.72, "formation": "Pyrolusite / Cryptomelane Horizon", "base_grade": 45.0, "base_pot": 460000},

    # Odisha (Sundargarh - Keonjhar - Bonai Belt)
    {"state": "Odisha", "district": "Keonjhar (Joda)", "belt": "Joda-Barbil Iron-Manganese Belt", "base_lat": 22.01, "base_lon": 85.42, "formation": "Iron Ore Supergroup / Shale-BIF", "base_grade": 39.5, "base_pot": 450000},
    {"state": "Odisha", "district": "Sundargarh (Koira)", "belt": "Bonai-Koira Valley", "base_lat": 21.90, "base_lon": 85.25, "formation": "Banded Iron Formation & Wad", "base_grade": 36.0, "base_pot": 370000},
    {"state": "Odisha", "district": "Rayagada (Nishikhal)", "belt": "Eastern Ghats Mobile Belt", "base_lat": 19.22, "base_lon": 83.25, "formation": "Khondalite & Calc-granulite", "base_grade": 37.5, "base_pot": 310000},
    {"state": "Odisha", "district": "Koraput (Podakana)", "belt": "Koraput Manganese Horizon", "base_lat": 18.81, "base_lon": 82.71, "formation": "Khondalite Supergroup", "base_grade": 34.0, "base_pot": 260000},

    # Karnataka (Sandur - Bellary - Shimoga Belt)
    {"state": "Karnataka", "district": "Bellary (Sandur)", "belt": "Sandur Schist Belt", "base_lat": 15.09, "base_lon": 76.55, "formation": "Dharwar Supergroup / Deogiri Bed", "base_grade": 38.5, "base_pot": 390000},
    {"state": "Karnataka", "district": "Shimoga (Kumsi)", "belt": "Shimoga Schist Basin", "base_lat": 14.05, "base_lon": 75.40, "formation": "Chitradurga Group Phyllite", "base_grade": 32.0, "base_pot": 220000},
    {"state": "Karnataka", "district": "Uttara Kannada", "belt": "North Kanara Low-grade Belt", "base_lat": 15.15, "base_lon": 74.62, "formation": "Lateritic Manganese Cap", "base_grade": 30.5, "base_pot": 190000},

    # Andhra Pradesh (Vizianagaram - Srikakulam Belt)
    {"state": "Andhra Pradesh", "district": "Vizianagaram (Garbham)", "belt": "Garbham-Chipurupalle Belt", "base_lat": 18.35, "base_lon": 83.52, "formation": "Kodurite Series (Apatite-Mn)", "base_grade": 35.0, "base_pot": 270000},
    {"state": "Andhra Pradesh", "district": "Srikakulam", "belt": "Srikakulam Manganese Complex", "base_lat": 18.29, "base_lon": 83.89, "formation": "Kodurite / Khondalite Contact", "base_grade": 33.5, "base_pot": 240000},

    # Jharkhand (West Singhbhum - Chaibasa Belt)
    {"state": "Jharkhand", "district": "West Singhbhum (Chaibasa)", "belt": "Singhbhum Craton Belt", "base_lat": 22.55, "base_lon": 85.80, "formation": "Kolhan Group Conglomerate / Shale", "base_grade": 36.5, "base_pot": 280000},
]

def generate_dataset(n_samples=600, random_seed=42):
    np.random.seed(random_seed)
    records = []
    
    samples_per_hub = n_samples // len(MINING_HUBS)
    
    for hub in MINING_HUBS:
        for i in range(samples_per_hub):
            # Coordinates with natural spatial scatter (+/- 0.15 deg ~ 15-20 km cluster spread)
            lat_jitter = np.random.normal(0, 0.08)
            lon_jitter = np.random.normal(0, 0.08)
            lat = round(hub["base_lat"] + lat_jitter, 5)
            lon = round(hub["base_lon"] + lon_jitter, 5)
            
            # Geological Score (0 to 1) based on formation richness + local fault/lithology variance
            geo_noise = np.random.beta(5, 2) * 0.4 + np.random.uniform(0.3, 0.6)
            geological_score = float(np.clip(geo_noise, 0.15, 0.98))
            
            # Space & Earth Observation (Sentinel-2 & Landsat features)
            sentinel2_ferrous_index = round(float(np.clip(0.9 + 0.8 * geological_score + np.random.normal(0, 0.12), 0.5, 2.2)), 3)
            sentinel2_clay_index = round(float(np.clip(0.8 + 0.7 * geological_score + np.random.normal(0, 0.10), 0.4, 2.0)), 3)
            
            # NDVI (0.10 to 0.75) - lower where mineralized outcrop is high
            ndvi = round(float(np.clip(0.65 - 0.35 * geological_score + np.random.normal(0, 0.08), 0.10, 0.85)), 3)
            
            # Soil moisture (0.10 to 0.50)
            soil_moisture = round(float(np.clip(0.20 + 0.20 * np.random.beta(2, 2), 0.10, 0.55)), 3)
            
            # Land Surface Temperature (LST in °C from Landsat Thermal)
            land_surface_temperature = round(float(np.clip(28.0 + 8.0 * (1 - ndvi) + np.random.normal(0, 2.0), 22.0, 44.0)), 2)
            
            # Elevation (SRTM DEM in meters)
            elevation_m = round(float(np.clip(250 + 400 * np.random.beta(2, 3) + np.random.normal(0, 30), 120, 920)), 1)
            
            # Rainfall (mm)
            rainfall_mm = round(float(np.clip(900 + 700 * np.random.beta(3, 3) + np.random.normal(0, 80), 550, 1850)), 1)
            
            # Ore Grade (% Mn)
            ore_grade_percent = round(float(np.clip(hub["base_grade"] * (0.85 + 0.25 * geological_score) + np.random.normal(0, 1.8), 24.0, 49.5)), 2)
            
            # Operational Signals
            equipment_efficiency = round(float(np.clip(0.55 + 0.38 * np.random.beta(3, 2), 0.45, 0.98)), 3)
            historical_production_tonnes = round(float(np.random.uniform(8000, 48000)), 0)
            
            # Prospectivity Score (Transparent Composite of Space Tech + Geological Evidence)
            prospectivity_raw = (
                0.35 * geological_score
                + 0.25 * (sentinel2_ferrous_index / 2.0)
                + 0.15 * (sentinel2_clay_index / 1.8)
                + 0.15 * (1.0 - ndvi)
                + 0.10 * (land_surface_temperature / 42.0)
            )
            prospectivity_score = round(float(np.clip(prospectivity_raw, 0.05, 0.98)), 4)
            
            # Model-estimated Manganese Potential (tonnes)
            potential_tonnes = round(float(
                hub["base_pot"] * (0.4 + 0.9 * prospectivity_score + 0.2 * (ore_grade_percent / 40.0))
                + np.random.normal(0, 15000)
            ), 0)
            potential_tonnes = max(45000, potential_tonnes)
            
            # Production Prediction and Shortfall
            efficiency_factor = equipment_efficiency ** 1.15
            rainfall_penalty = max(0, (rainfall_mm - 1400) / 2500)
            pred_prod = historical_production_tonnes * (0.70 + 0.40 * efficiency_factor - rainfall_penalty) + np.random.normal(0, 1200)
            predicted_production_tonnes = round(float(max(3000, pred_prod)), 0)
            
            # Shortfall calculation
            shortfall_tonnes = round(float(max(0, historical_production_tonnes - predicted_production_tonnes)), 0)
            production_gap_pct = round(float(shortfall_tonnes / max(1, historical_production_tonnes) * 100), 2)
            
            # Confidence Score (%) based on signal alignment
            confidence_score = round(float(np.clip(72.0 + 24.0 * geological_score - 10.0 * abs(ndvi - 0.35) + np.random.normal(0, 3.0), 60.0, 98.5)), 1)
            
            # Risk Level Classification
            if production_gap_pct > 26.0 or equipment_efficiency < 0.62 or rainfall_mm > 1550:
                risk_level = "High"
            elif production_gap_pct > 12.0 or equipment_efficiency < 0.74:
                risk_level = "Medium"
            else:
                risk_level = "Low"
                
            records.append({
                "zone_id": f"MN-IND-{len(records)+1:04d}",
                "state": hub["state"],
                "district": hub["district"],
                "mining_belt": hub["belt"],
                "formation": hub["formation"],
                "latitude": lat,
                "longitude": lon,
                "elevation_m": elevation_m,
                "rainfall_mm": rainfall_mm,
                "soil_moisture": soil_moisture,
                "ndvi": ndvi,
                "sentinel2_ferrous_index": sentinel2_ferrous_index,
                "sentinel2_clay_index": sentinel2_clay_index,
                "land_surface_temperature": land_surface_temperature,
                "geological_score": round(geological_score, 3),
                "ore_grade_percent": ore_grade_percent,
                "historical_production_tonnes": historical_production_tonnes,
                "predicted_production_tonnes": predicted_production_tonnes,
                "production_shortfall_tonnes": shortfall_tonnes,
                "production_gap_percent": production_gap_pct,
                "predicted_manganese_reserve_tonnes": potential_tonnes,
                "prospectivity_score": prospectivity_score,
                "confidence_score": confidence_score,
                "equipment_efficiency": equipment_efficiency,
                "risk_level": risk_level,
            })
            
    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Generated {len(df)} records saved to {OUTPUT_FILE}")
    return df

if __name__ == "__main__":
    generate_dataset()
