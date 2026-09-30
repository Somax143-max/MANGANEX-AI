# 🚀 MANGANEX AI — Production Deployment Guide
## 🌐 Architecture: FastAPI Backend on Render + Modern Frontend on Vercel

This repository is configured for decoupled, scalable cloud deployment:
- **Backend API & ML Models:** Hosted on **[Render](https://render.com)** (Free Python Web Service)
- **Interactive UI Dashboard:** Hosted on **[Vercel](https://vercel.com)** (High-Speed Global Edge CDN)

---

## 🏗️ Step 1: Deploy Backend to Render

### 1-Click Render Blueprint Setup:
1. Push your repository to GitHub: `git push origin main`
2. Open **[dashboard.render.com/blueprints](https://dashboard.render.com/blueprints)** (or click **New +** → **Web Service**).
3. Connect your repository (`MANGANEX-AI`).
4. Render will automatically read [`render.yaml`](file:///d:/2nd%20move%20from%20os/d/MANGANEX_AI_SIHPOLISH/render.yaml):
   - **Name:** `manganex-ai-backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn server:app --host 0.0.0.0 --port $PORT --workers 2`
   - **Health Check Path:** `/health`
5. Click **Apply / Create Web Service**.
6. Once deployed (approx 2 minutes), copy your Render backend URL:
   > 📌 *Example:* `https://manganex-ai-backend.onrender.com`

---

## ⚡ Step 2: Deploy Frontend to Vercel

### 1-Click Vercel Setup:
1. Open **[vercel.com/new](https://vercel.com/new)**.
2. Select and import your GitHub repository (`MANGANEX-AI`).
3. Under **Build and Output Settings**:
   - **Framework Preset:** `Other`
   - **Root Directory:** `./` (or `frontend`)
4. Click **Deploy**.
5. Your frontend is instantly live with free SSL!
   > 📌 *Example:* `https://manganex-ai.vercel.app`

---

## 🔗 Step 3: Connect Frontend (Vercel) to Backend (Render)

You have **two easy ways** to connect them:

### Option A: Using the Live UI Settings (Instant, Zero Re-deploy)
1. Open your live Vercel URL in your browser.
2. In the top navbar, click the **`⚙️ Backend: Connect`** button.
3. Paste your Render backend URL (e.g. `https://manganex-ai-backend.onrender.com`) and click **Test & Connect**.
4. The status turns **`🟢 Render Backend: Connected`** and data loads immediately. Your choice is saved in browser storage.

### Option B: Automatic Proxy via `vercel.json` (Zero CORS)
Add your Render URL directly into [`vercel.json`](file:///d:/2nd%20move%20from%20os/d/MANGANEX_AI_SIHPOLISH/vercel.json) rewrites:
```json
{
  "rewrites": [
    { "source": "/", "destination": "/frontend/index.html" },
    { "source": "/app.js", "destination": "/frontend/app.js" },
    { "source": "/static/:path*", "destination": "/frontend/:path*" },
    { "source": "/api/:path*", "destination": "https://YOUR-RENDER-BACKEND.onrender.com/api/:path*" },
    { "source": "/health", "destination": "https://YOUR-RENDER-BACKEND.onrender.com/health" }
  ]
}
```

---

## 🧪 Local Testing Before Deploy

```bash
# Terminal 1: Run Backend (Port 7860)
python server.py

# Terminal 2: Test Health Check & API
curl http://localhost:7860/health
curl http://localhost:7860/api/summary
```
Open `http://localhost:7860` in your browser.

---

### 🏛️ Ministry of Steel, Government of India • Smart India Hackathon 2026
