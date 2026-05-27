"""
TruthLens AI — Forensic Reasoning Route
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../ai-engine"))

from fastapi import APIRouter, HTTPException
from models.schemas import ForensicReasoningRequest
from reasoning_engine.master_reasoner import generate_forensic_report

router = APIRouter()


@router.post("/synthesize")
async def synthesize_forensic_report(request: ForensicReasoningRequest):
    """
    Master forensic synthesis:
    Combines text, image, and video analysis results
    into a unified forensic verdict with evidence chain.
    """
    try:
        report = await generate_forensic_report(
            text_result=request.text_result,
            image_result=request.image_result,
            video_result=request.video_result,
            original_claim=request.original_claim,
        )
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forensic reasoning failed: {str(e)}")
