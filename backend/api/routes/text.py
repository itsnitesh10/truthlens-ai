"""
TruthLens AI — Text Analysis Route
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../ai-engine"))

from fastapi import APIRouter, HTTPException
from models.schemas import TextAnalysisRequest, TextAnalysisResponse
from text_forensics.analyzer import analyze_text

router = APIRouter()


@router.post("/text", response_model=None)
async def analyze_text_endpoint(request: TextAnalysisRequest):
    """
    Analyze text for:
    - Fake news / credibility
    - AI-generated content
    - Propaganda patterns
    - Claim verification
    """
    try:
        result = await analyze_text(
            text=request.text,
            url=request.url,
            title=request.title,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text analysis failed: {str(e)}")
