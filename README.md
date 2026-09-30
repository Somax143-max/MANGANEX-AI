# ⛏️ MANGANEX AI
### Smart India Hackathon 2026 | Problem Statement 26009
**Organization:** Ministry of Steel, Government of India  
**Theme:** Smart Automation | Software Edition  
**Title:** *Using AI/ML and Space Technology to Identify Manganese Reserves and Overcome Production Shortfalls*

---

## 🚀 Live Demo & Deployment Status

- **Web Application:** FastAPI + HTML5/Tailwind/Leaflet/Chart.js Dashboard
- **Production Port:** `7860` (or dynamic `$PORT`)
- **API Health Endpoint:** `/health` & `/api/health`
- **Deployment Guide:** Complete instructions for Vercel, Render, Railway, Hugging Face Spaces & Docker in [**`DEPLOYMENT.md`**](DEPLOYMENT.md)

---

## 📌 Problem Overview
India is among the world's leading producers of manganese ore, yet significant quantities of high-grade manganese ore are imported annually for specialized steelmaking and electric vehicle (EV) battery cathode chemistry (NMC). 

**MANGANEX AI** delivers an end-to-end space-to-decision bridge:
1. **Space & Earth Observation Integration:** Ingests European Space Agency (ESA) **Sentinel-2 MSI** multispectral bands (SWIR-1/SWIR-2 & NIR) and NASA/USGS **Landsat-8/9 Thermal LST** to detect surface gossan caps, hydrothermal clay alteration envelopes, and vegetation canopy stress.
2. **AI/ML Multi-Model Ensemble:** Dedicated Random Forest models for:
   - In-Situ Manganese Potential Estimation (tonnes)
   - Operational Extraction Shortfall Forecasting (tonnes)
   - Multi-Hazard Operational Risk Classification (Low / Medium / High)
3. **5-Module Executive GIS Dashboard:** Interactive 3D Leaflet & PyDeck geospatial mapping over 592 verified mining clusters across Madhya Pradesh, Maharashtra, Odisha, Karnataka, Andhra Pradesh, and Jharkhand.
4. **Explainable AI (XAI):** Transparent mathematical breakdown of composite prospectivity scores into exact feature contributions.

---

## 🚀 Key Modules
- **🏛️ Executive Command Center:** National supply metrics, state-wise potential vs. shortfall distribution, end-to-end pipeline flowchart, and top Tier-1 target zones.
- **🛰️ Space Tech & Prospectivity GIS Hub:** Interactive geospatial heatmap and candidate scatter points with filters for State, Min Prospectivity %, and Min Ore Grade (% Mn).
- **📈 Production Intelligence & Shortfall Analytics:** Historical baseline vs. AI forecasted output, equipment efficiency deficit tiering, and operational risk distribution.
- **🧪 AI Mineral Simulator & Scenario Lab:** Interactive sliders for Sentinel-2 SWIR band ratios, LST, Elevation, Geological Score, and Equipment Efficiency with instant live inference and XAI feature attribution.
- **🔍 Explainable AI & Space Architecture:** Mathematical formulations of satellite band ratios (B11/B12, B11/B8A), model cards with live validation metrics, and policy alignment.

---

## 🛠️ Tech Stack
- **Backend:** FastAPI, Uvicorn, Python 3.10+
- **Machine Learning:** Scikit-Learn (Random Forest Regressors & Classifiers), Joblib, NumPy, Pandas
- **Frontend / UI:** Modern HTML5, Tailwind CSS, Leaflet.js, Chart.js, Lucide Icons
- **Production & Containerization:** Docker, Docker Compose, Vercel, Render, Railway, Hugging Face Spaces

---

## 💻 Quickstart (Local Run)

```bash
# 1. Clone the repository
git clone https://github.com/Somax143-max/MANGANEX-AI.git
cd MANGANEX-AI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the Modern Web Dashboard (FastAPI + HTML5/Tailwind/Leaflet)
python server.py
# Open http://localhost:7860 in your browser!

# 4. Or run via Docker
docker compose up --build
```

---

## 🌐 1-Click Deployment

See [**`DEPLOYMENT.md`**](DEPLOYMENT.md) for complete guides:
- **Vercel:** Ready with `vercel.json` & `api/index.py`
- **Render:** 1-click deploy with `render.yaml` & `Procfile`
- **Railway:** Auto-configured with `railway.json`
- **Hugging Face Spaces:** Containerized with `Dockerfile` (Port 7860)
- **Docker / Cloud Run:** Multi-platform Linux container with built-in health check

---

## 📊 Presentation & Submission Documents
- Official 6-Slide SIH Presentation: `MANGANEX_AI_SIH2026_Final_Submission.pptx`
- Submission Text Guide: `SIH2026_MANGANEX_AI_Presentation_Guide.md`

---

### 🏛️ Ministry of Steel, Government of India • SIH 2026
