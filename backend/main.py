"""
TruthLens AI — FastAPI Backend Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

load_dotenv()

from api.routes import text, image, video, reasoning, health

app = FastAPI(
    title="TruthLens AI API",
    description="Multi-Modal Misinformation Forensics Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ──────────────────────────────────────────────────────────
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static files for uploads ──────────────────────────────────────
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ── Routes ────────────────────────────────────────────────────────
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(text.router, prefix="/api/analyze", tags=["Text Forensics"])
app.include_router(image.router, prefix="/api/analyze", tags=["Image Forensics"])
app.include_router(video.router, prefix="/api/analyze", tags=["Video Forensics"])
app.include_router(reasoning.router, prefix="/api/reasoning", tags=["Forensic Reasoning"])


@app.get("/")
async def root():
    return {
        "name": "TruthLens AI",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
    }
