# 🚀 MANGANEX AI — Production Deployment Guide
## 🌐 Architecture: FastAPI Backend on Render + Modern Frontend on Vercel

This repository is configured for decoupled, high-performance cloud deployment:
- **Backend API & ML Models:** Hosted on **[Render](https://render.com)**: `https://manganex-ai-4l0l.onrender.com`
- **Interactive UI Dashboard:** Hosted on **[Vercel](https://vercel.com)**: `https://manganex-ai.vercel.app`

---

## 🏗️ Live Cloud Architecture

| Component | Platform | Live URL / Endpoint |
|---|---|---|
| **FastAPI ML Backend** | Render | `https://manganex-ai-4l0l.onrender.com` |
| **API Health Status** | Render | `https://manganex-ai-4l0l.onrender.com/health` |
| **National Summary API** | Render | `https://manganex-ai-4l0l.onrender.com/api/summary` |
| **GIS Prospectivity Zones** | Render | `https://manganex-ai-4l0l.onrender.com/api/zones` |
| **AI Inference & Simulation** | Render | `https://manganex-ai-4l0l.onrender.com/api/predict` |
| **Dashboard UI** | Vercel / Edge CDN | Fast Global Edge Distribution |

---

## 🔄 Automatic Keep-Alive & High-Availability Engine

Render free-tier web services automatically spin down after 15 minutes of inactivity. To ensure 100% smooth evaluation and real-time responsiveness:
1. **Automated Heartbeat Pinger:** The frontend automatically pings `https://manganex-ai-4l0l.onrender.com/health` every 5 minutes while the page is open to keep the backend warm and active.
2. **Cold-Start Auto-Retry:** If a request is made while the container is spinning up, the frontend automatically displays a non-intrusive status notification and executes exponential backoff retries.
3. **Resilient Local Fallback Engine:** If offline or during temporary network interruptions, the frontend seamlessly executes local mathematical predictions mirroring the Random Forest regression and classification models, ensuring zero broken graphs or missing metrics.

---

## ⚡ 1-Click Vercel Deployment

1. Open **[vercel.com/new](https://vercel.com/new)**.
2. Import your GitHub repository (`MANGANEX-AI`).
3. Under **Build & Output Settings**:
   - Framework Preset: `Other`
   - Root Directory: `./` (or `frontend`)
4. Click **Deploy**.
5. The frontend is automatically wired to `https://manganex-ai-4l0l.onrender.com` via `vercel.json` rewrites and `app.js` default configurations.

---

## 🧪 Testing Backend Endpoints

```bash
# Health Check
curl -X GET https://manganex-ai-4l0l.onrender.com/health

# Executive Summary KPIs
curl -X GET https://manganex-ai-4l0l.onrender.com/api/summary

# AI Prediction Inference
curl -X POST https://manganex-ai-4l0l.onrender.com/api/predict \
     -H "Content-Type: application/json" \
     -d '{"sentinel2_ferrous_index": 1.45, "sentinel2_clay_index": 1.30, "ndvi": 0.28, "land_surface_temperature": 34.5, "elevation_m": 480.0, "geological_score": 0.85, "ore_grade_percent": 42.5, "historical_production_tonnes": 32000.0, "equipment_efficiency": 0.72, "rainfall_mm": 1150.0}'
```

---

### 🏛️ Ministry of Steel, Government of India • Smart India Hackathon 2026
