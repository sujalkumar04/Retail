# Deployment Guide

This project is configured for easy deployment on **Render** (recommended) and **Vercel**.

## Prerequisites

1.  **GitHub Account**: Ensure your code is pushed to a GitHub repository.
2.  **Groq API Key**: You will need your `GROQ_API_KEY` for the application to work.

---

## Option 1: Deploy to Render (Recommended)

Render is excellent for Python FastAPI applications.

1.  **Sign Up/Login**: Go to [render.com](https://render.com) and log in with GitHub.
2.  **New Web Service**: Click **New +** -> **Web Service**.
3.  **Connect Repo**: Select your `Retail` repository.
4.  **Configure**:
    *   **Name**: `retail-ai-agent` (or any name)
    *   **Region**: Choose one close to you (e.g., Singapore, Frankfurt).
    *   **Branch**: `main`
    *   **Root Directory**: Leave empty (default).
    *   **Runtime**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn api.app:app --host 0.0.0.0 --port $PORT`
5.  **Environment Variables**:
    *   Scroll down to "Environment Variables".
    *   Add Key: `GROQ_API_KEY`
    *   Add Value: `your_actual_api_key_here`
    *   (Optional) Add `LLM_PROVIDER` = `groq`
6.  **Deploy**: Click **Create Web Service**.

Render will build your app and deploy it. It usually takes 2-3 minutes.

---

## Option 2: Deploy to Vercel

Vercel is great for serverless deployments.

1.  **Sign Up/Login**: Go to [vercel.com](https://vercel.com) and log in with GitHub.
2.  **Add New Project**: Click **Add New...** -> **Project**.
3.  **Import Repo**: Find your `Retail` repo and click **Import**.
4.  **Configure Project**:
    *   **Framework Preset**: Select **Other**.
    *   **Root Directory**: `./` (default).
5.  **Environment Variables**:
    *   Expand the "Environment Variables" section.
    *   Add `GROQ_API_KEY` with your key value.
6.  **Deploy**: Click **Deploy**.

Vercel will use the `vercel.json` configuration file included in the project to set up the Python runtime.

---

## Troubleshooting

*   **Application Error**: Check the "Logs" tab in Render or Vercel.
*   **API Key Error**: Ensure `GROQ_API_KEY` is set correctly in the environment variables.
*   **Static Files Not Loading**: Ensure the `frontend` folder is present in your GitHub repository.
