# 🚀 MANGANEX AI — Production Deployment Guide

This repository is fully configured and ready for **1-click / zero-config deployment** across all major cloud providers and container platforms.

---

## ⚡ Deployment Options Summary

| Platform | Deployment Type | Config File | Free Tier Available |
| :--- | :--- | :--- | :--- |
| **Vercel** | Serverless Python (FastAPI) | [`vercel.json`](file:///d:/2nd%20move%20from%20os/d/MANGANEX_AI_SIHPOLISH/vercel.json), [`api/index.py`](file:///d:/2nd%20move%20from%20os/d/MANGANEX_AI_SIHPOLISH/api/index.py) | ✅ Yes |
| **Render** | Docker / Native Web Service | [`render.yaml`](file:///d:/2nd%20move%20from%20os/d/MANGANEX_AI_SIHPOLISH/render.yaml), [`Procfile`](file:///d:/2nd%20move%20from%20os/d/MANGANEX_AI_SIHPOLISH/Procfile) | ✅ Yes |
| **Railway** | Nixpacks / Docker | [`railway.json`](file:///d:/2nd%20move%20from%20os/d/MANGANEX_AI_SIHPOLISH/railway.json), [`Dockerfile`](file:///d:/2nd%20move%20from%20os/d/MANGANEX_AI_SIHPOLISH/Dockerfile) | ✅ Yes |
| **Docker / Cloud Run / AWS / VPS** | Container (Linux Slim) | [`Dockerfile`](file:///d:/2nd%20move%20from%20os/d/MANGANEX_AI_SIHPOLISH/Dockerfile), [`docker-compose.yml`](file:///d:/2nd%20move%20from%20os/d/MANGANEX_AI_SIHPOLISH/docker-compose.yml) | ✅ Yes |
| **Hugging Face Spaces** | Docker Space | [`Dockerfile`](file:///d:/2nd%20move%20from%20os/d/MANGANEX_AI_SIHPOLISH/Dockerfile), [`README.md`](file:///d:/2nd%20move%20from%20os/d/MANGANEX_AI_SIHPOLISH/README.md) | ✅ Yes (2vCPU / 16GB) |
| **Streamlit Community Cloud** | Native Streamlit App | [`.streamlit/config.toml`](file:///d:/2nd%20move%20from%20os/d/MANGANEX_AI_SIHPOLISH/.streamlit/config.toml), [`dashboard/app.py`](file:///d:/2nd%20move%20from%20os/d/MANGANEX_AI_SIHPOLISH/dashboard/app.py) | ✅ Yes |

---

## 1. 🔺 Deploy to Vercel (Fastest Serverless Option)

### Option A: Using Vercel Web Dashboard (Recommended)
1. Push this repository to your GitHub account: `https://github.com/Somax143-max/MANGANEX-AI`
2. Go to **[vercel.com/new](https://vercel.com/new)** and import your repository.
3. Framework Preset: **Other** (Vercel automatically detects `vercel.json` and `api/index.py`).
4. Click **Deploy**. Your app will be live with full SSL and global CDN in ~60 seconds!

### Option B: Using Vercel CLI
```bash
# 1. Install Vercel CLI globally
npm i -g vercel

# 2. Login & deploy to production
vercel --prod
```

---

## 2. 🌊 Deploy to Render

### Option A: Render Blueprint (1-Click)
1. Go to **[dashboard.render.com/blueprints](https://dashboard.render.com/blueprints)**.
2. Connect your repo `MANGANEX-AI`.
3. Render will read [`render.yaml`](file:///d:/2nd%20move%20from%20os/d/MANGANEX_AI_SIHPOLISH/render.yaml) and automatically configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn server:app --host 0.0.0.0 --port $PORT`
   - Health Check: `/health`
4. Click **Apply**.

### Option B: Render Web Service Manual Setup
- **Environment:** Python
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn server:app --host 0.0.0.0 --port $PORT`
- **Health Check Path:** `/health`

---

## 3. 🚂 Deploy to Railway

1. Go to **[railway.app/new](https://railway.app/new)**.
2. Select **Deploy from GitHub repo** and select `MANGANEX-AI`.
3. Railway automatically recognizes [`railway.json`](file:///d:/2nd%20move%20from%20os/d/MANGANEX_AI_SIHPOLISH/railway.json) or [`Dockerfile`](file:///d:/2nd%20move%20from%20os/d/MANGANEX_AI_SIHPOLISH/Dockerfile).
4. Click **Deploy**. Generate a public domain under Settings → Networking.

---

## 4. 🐳 Deploy with Docker / Local / Cloud Run / AWS / VPS

### Run locally with Docker Compose:
```bash
# Build and run container
docker compose up --build

# Open in browser
# http://localhost:7860
```

### Build & Run Docker Image directly:
```bash
# Build Docker image
docker build -t manganex-ai .

# Run container
docker run -d -p 7860:7860 --name manganex-app manganex-ai

# Test health check
curl http://localhost:7860/health
```

### Deploy to Google Cloud Run:
```bash
gcloud run deploy manganex-ai \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 7860
```

---

## 5. 🤗 Deploy to Hugging Face Spaces

1. Create a new Space on [Hugging Face](https://huggingface.co/new-space).
2. Space SDK: **Docker** (Blank).
3. Push or sync this repository to the HF Space git remote:
```bash
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/manganex-ai
git push space main
```
4. HF Spaces will build the [`Dockerfile`](file:///d:/2nd%20move%20from%20os/d/MANGANEX_AI_SIHPOLISH/Dockerfile) on port `7860` and host it continuously.

---

## 6. 🎈 Deploy Streamlit Edition (Streamlit Community Cloud)

If you wish to host the optional Streamlit GIS edition alongside the FastAPI web app:
1. Go to **[share.streamlit.io](https://share.streamlit.io)**.
2. Select repository: `Somax143-max/MANGANEX-AI`.
3. Main file path: `dashboard/app.py`.
4. Python version: `3.11`.
5. Click **Deploy**.

---

## 🔍 Verification & Health Checks

Once deployed to any URL, verify all subsystems:
- **API Health:** `GET https://your-domain.com/health` (Returns `{"status": "healthy", ...}`)
- **Executive Summary:** `GET https://your-domain.com/api/summary`
- **GIS Zones Filter:** `GET https://your-domain.com/api/zones?state=Madhya%20Pradesh`
- **Sim Inference:** `POST https://your-domain.com/api/predict`
- **Interactive UI:** `GET https://your-domain.com/` (Full 5-module Leaflet + Chart.js Dashboard)
