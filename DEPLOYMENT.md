# Deployment Guide: The Decision Completeness Engine (DCE)

This guide provides step-by-step instructions to deploy the Decision Completeness Engine to the web.

---

## ⚡ 1. Instant Public Access (Live Now)

A live public tunnel has been launched for you:
- **Public Website URL:** [https://static-outstanding-palm-clarke.trycloudflare.com](https://static-outstanding-palm-clarke.trycloudflare.com)
- **Local Access:** [http://localhost:5000](http://localhost:5000)

To re-launch this public URL at any time from your machine:
```bash
python serve_public.py
```

---

## 🌐 2. Deploy to Free Cloud Providers

### Option A: Render.com (Recommended Free Tier)
1. Push this project folder to your GitHub or GitLab repository.
2. Sign up / Log in to [Render.com](https://render.com).
3. Click **New +** > **Web Service** > Connect your repository.
4. Render will automatically detect [`render.yaml`](file:///c:/Users/HP/Downloads/The%20Decision%20Completeness%20Engine/render.yaml):
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
5. Click **Create Web Service**. Your app will be live on `https://your-app-name.onrender.com`.

---

### Option B: Vercel (Serverless)
1. Install Vercel CLI or link GitHub to [Vercel](https://vercel.com).
2. The repository includes [`vercel.json`](file:///c:/Users/HP/Downloads/The%20Decision%20Completeness%20Engine/vercel.json) and [`api/index.py`](file:///c:/Users/HP/Downloads/The%20Decision%20Completeness%20Engine/api/index.py).
3. In terminal, run:
```bash
npx vercel
```
4. Follow the prompts. Vercel will deploy it to `https://your-project.vercel.app`.

---

### Option C: Railway.app
1. Push to GitHub.
2. Go to [Railway.app](https://railway.app), click **New Project** > **Deploy from GitHub repo**.
3. Railway will automatically detect [`railway.json`](file:///c:/Users/HP/Downloads/The%20Decision%20Completeness%20Engine/railway.json) and deploy your app.
4. Click **Settings** > **Generate Domain** to get a public `https://...up.railway.app` URL.

---

### Option D: Docker Container (Any Cloud / AWS / GCP / Azure)
Build and run the production container locally or on any cloud VPS:
```bash
# Build Docker image
docker build -t decision-completeness-engine .

# Run container on port 5000
docker run -d -p 5000:5000 --name dce decision-completeness-engine
```
Access at `http://localhost:5000`.

---

## 🔒 3. Production Environment Variables (Optional)

You can optionally configure external LLM API keys:
- `PORT`: (Default: `5000`)
- `GROQ_API_KEY`: For ultra-fast Groq LLM inference
- `OPENAI_API_KEY`: For OpenAI GPT models
- `GEMINI_API_KEY`: For Google Gemini models
*(Note: If no API key is provided, the built-in intelligent engine runs out of the box with zero external dependencies).*
