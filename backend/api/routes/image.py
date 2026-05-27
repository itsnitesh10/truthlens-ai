"""
TruthLens AI — Image Analysis Route
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../ai-engine"))

from fastapi import APIRouter, HTTPException, UploadFile, File
import aiofiles
import uuid
from image_forensics.analyzer import analyze_image

router = APIRouter()

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_SIZE = 20 * 1024 * 1024  # 20MB


@router.post("/image")
async def analyze_image_endpoint(file: UploadFile = File(...)):
    """
    Analyze image for:
    - Metadata anomalies
    - ELA (Error Level Analysis)
    - Face inconsistencies / deepfake indicators
    - GAN artifact detection
    """
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

    # Save uploaded file
    upload_dir = os.getenv("UPLOAD_DIR", "./uploads")
    os.makedirs(upload_dir, exist_ok=True)

    ext = file.filename.rsplit(".", 1)[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(upload_dir, filename)

    try:
        async with aiofiles.open(filepath, "wb") as f:
            content = await file.read()
            if len(content) > MAX_SIZE:
                raise HTTPException(status_code=413, detail="File too large (max 20MB)")
            await f.write(content)

        result = await analyze_image(filepath)
        result["filename"] = filename
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image analysis failed: {str(e)}")
