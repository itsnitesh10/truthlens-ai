"""
TruthLens AI — Image Forensics Engine
ELA + Metadata + GAN artifact detection + Ollama local LLM reasoning
"""

import time
import os
import io
import sys
from typing import Dict, Any, List, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from services.ollama_service import image_forensic_reasoning


def _ela_analysis(image_path: str, quality: int = 90) -> Tuple[float, str]:
    """
    Error Level Analysis (ELA)
    Detects image editing by comparing JPEG compression artifacts.
    Returns anomaly score (0-1) and ELA image path.
    """
    try:
        from PIL import Image, ImageChops, ImageEnhance
        import numpy as np

        original   = Image.open(image_path).convert("RGB")
        buffer     = io.BytesIO()
        original.save(buffer, format="JPEG", quality=quality)
        buffer.seek(0)
        compressed = Image.open(buffer).convert("RGB")

        diff          = ImageChops.difference(original, compressed)
        diff_enhanced = ImageEnhance.Brightness(diff).enhance(10)

        ela_path = image_path.rsplit(".", 1)[0] + "_ela.jpg"
        diff_enhanced.save(ela_path)

        import numpy as np
        diff_array    = np.array(diff)
        anomaly_score = min(1.0, (diff_array.mean() + diff_array.std()) / 255.0 * 3)
        return round(anomaly_score, 3), ela_path

    except Exception as e:
        print(f"[ELA] Error: {e}")
        return 0.3, ""


def _extract_metadata(image_path: str) -> Dict[str, Any]:
    """Extract and analyse image metadata for suspicious patterns"""
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS

        img      = Image.open(image_path)
        metadata = {"format": img.format, "mode": img.mode, "size": img.size, "issues": []}

        exif_data = {}
        if hasattr(img, "_getexif") and img._getexif():
            for tag_id, value in img._getexif().items():
                exif_data[TAGS.get(tag_id, tag_id)] = str(value)[:100]

        metadata["exif"] = exif_data

        if "Software" in exif_data:
            sw = exif_data["Software"].lower()
            if any(x in sw for x in ["photoshop", "gimp", "lightroom", "affinity", "stable diffusion"]):
                metadata["issues"].append(f"Editing software detected: {exif_data['Software']}")

        if not exif_data:
            metadata["issues"].append("No EXIF data — metadata may have been stripped")

        if "DateTime" in exif_data and "DateTimeOriginal" in exif_data:
            if exif_data["DateTime"] != exif_data["DateTimeOriginal"]:
                metadata["issues"].append("Timestamp mismatch — file may have been modified")

        return metadata

    except Exception as e:
        print(f"[Metadata] Error: {e}")
        return {"format": "unknown", "issues": ["Could not read metadata"]}


def _detect_face_inconsistencies(image_path: str) -> List[str]:
    """Detect facial inconsistencies typical of deepfakes/GAN images"""
    issues = []
    try:
        import cv2

        img = cv2.imread(image_path)
        if img is None:
            return ["Could not load image for face analysis"]

        gray          = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade  = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        eye_cascade   = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
        faces         = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_roi  = gray[y:y+h, x:x+w]
            lap_var   = cv2.Laplacian(face_roi, cv2.CV_64F).var()
            if lap_var < 50:
                issues.append("Unusual blur pattern in facial region")

            eyes = eye_cascade.detectMultiScale(face_roi)
            if len(eyes) == 0:
                issues.append("No eyes detected in face region — possible manipulation")
            elif len(eyes) > 3:
                issues.append("Abnormal eye detection count — possible GAN artifact")

            if img[y:y+h, x:x+w].std() < 15:
                issues.append("Unusually uniform skin texture — possible AI generation")

    except Exception as e:
        print(f"[FaceCheck] Error: {e}")
    return issues


def _calculate_image_hash(image_path: str) -> str:
    """Generate perceptual hash for reverse image matching"""
    try:
        import imagehash
        from PIL import Image
        return str(imagehash.phash(Image.open(image_path)))
    except Exception:
        return ""


async def analyze_image(image_path: str) -> Dict[str, Any]:
    """
    Main image analysis pipeline:
    1. Metadata extraction
    2. ELA analysis
    3. Face inconsistency detection
    4. Perceptual hash
    5. Ollama local LLM forensic reasoning
    """
    start_time = time.time()

    metadata       = _extract_metadata(image_path)
    metadata_issues = metadata.get("issues", [])
    ela_score, _   = _ela_analysis(image_path)
    face_issues    = _detect_face_inconsistencies(image_path)
    img_hash       = _calculate_image_hash(image_path)

    # Score
    manipulation_score  = 0
    if ela_score > 0.5:   manipulation_score += 40
    elif ela_score > 0.25: manipulation_score += 20
    manipulation_score += len(metadata_issues) * 15
    manipulation_score += len(face_issues)     * 20
    manipulation_score  = min(manipulation_score, 95)

    credibility_score    = max(5, 100 - manipulation_score)
    manipulation_detected = manipulation_score > 35
    ai_risk = "HIGH" if manipulation_score > 65 else "MEDIUM" if manipulation_score > 35 else "LOW"

    # Ollama reasoning
    reasoning, verdict = await image_forensic_reasoning(
        metadata_issues=metadata_issues,
        ela_score=ela_score,
        face_issues=face_issues,
        credibility_score=credibility_score,
    )

    return {
        "credibility_score":    credibility_score,
        "verdict":              verdict,
        "ai_generated_risk":    ai_risk,
        "manipulation_detected": manipulation_detected,
        "ela_anomaly_score":    ela_score,
        "metadata_issues":      metadata_issues,
        "face_inconsistencies": face_issues,
        "image_hash":           img_hash,
        "reasoning":            reasoning,
        "confidence":           round(0.5 + abs(credibility_score - 50) / 100, 2),
        "processing_time_ms":   int((time.time() - start_time) * 1000),
    }
