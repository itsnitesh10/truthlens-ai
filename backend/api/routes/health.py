"""
TruthLens AI — Health Check Route
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../ai-engine"))

from fastapi import APIRouter
from services.ollama_service import check_ollama_health, OLLAMA_MODEL, OLLAMA_BASE_URL

router = APIRouter()


@router.get("/health")
async def health_check():
    """System health check — includes Ollama availability"""
    ollama = await check_ollama_health()
    return {
        "status": "ok",
        "llm_backend": "ollama (local)",
        "ollama": ollama,
        "ollama_url": OLLAMA_BASE_URL,
        "model": OLLAMA_MODEL,
        "modules": {
            "text_forensics":  "ready",
            "image_forensics": "ready",
            "video_forensics": "ready",
            "reasoning_engine": "ready",
        },
    }
