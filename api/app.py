"""FastAPI application setup"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from api.routes import chat_router, channels_router, webhooks_router

# Create FastAPI app
app = FastAPI(
    title="Retail AI Agent API",
    description="Multi-agent retail AI system with omnichannel support",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(channels_router, prefix="/api/channels", tags=["channels"])
app.include_router(webhooks_router, prefix="/api/webhooks", tags=["webhooks"])

# Determine base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
ASSETS_DIR = os.path.join(FRONTEND_DIR, "assets")

# Mount static files
# We mount it at /static for assets, but we also want to serve html files from root
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

@app.get("/")
async def root():
    """Serve landing page"""
    return FileResponse(os.path.join(FRONTEND_DIR, 'landing.html'))

@app.get("/index.html")
async def chat_page():
    """Serve chat page"""
    return FileResponse(os.path.join(FRONTEND_DIR, 'index.html'))

@app.get("/landing.html")
async def landing_page():
    """Serve landing page explicitly"""
    return FileResponse(os.path.join(FRONTEND_DIR, 'landing.html'))

# Mount the rest of the frontend files (css, js) at root
# This must be last to avoid overriding API routes
app.mount("/", StaticFiles(directory=FRONTEND_DIR), name="frontend")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "retail-ai-agent"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
