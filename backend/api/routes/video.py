"""
TruthLens AI — Video Analysis Route
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../ai-engine"))

from fastapi import APIRouter, HTTPException, UploadFile, File
import aiofiles
import uuid
from video_forensics.analyzer import analyze_video

router = APIRouter()

ALLOWED_VIDEO_TYPES = {"video/mp4", "video/webm", "video/avi", "video/mov", "video/quicktime"}
MAX_SIZE = 100 * 1024 * 1024  # 100MB


@router.post("/video")
async def analyze_video_endpoint(file: UploadFile = File(...)):
    """
    Analyze video for:
    - Deepfake face detection
    - Blink pattern anomalies
    - Frame-level GAN artifacts
    - Face consistency across frames
    """
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

    upload_dir = os.getenv("UPLOAD_DIR", "./uploads")
    os.makedirs(upload_dir, exist_ok=True)

    ext = file.filename.rsplit(".", 1)[-1] if "." in file.filename else "mp4"
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(upload_dir, filename)

    try:
        async with aiofiles.open(filepath, "wb") as f:
            content = await file.read()
            if len(content) > MAX_SIZE:
                raise HTTPException(status_code=413, detail="File too large (max 100MB)")
            await f.write(content)

        result = await analyze_video(filepath)
        result["filename"] = filename
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video analysis failed: {str(e)}")
