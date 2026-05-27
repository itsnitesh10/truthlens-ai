"""
TruthLens AI — Video Deepfake Detection Engine
Frame extraction + face analysis + Ollama local LLM reasoning
"""

import time
import os
import sys
import tempfile
from typing import Dict, Any, List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from services.ollama_service import video_forensic_reasoning


def _extract_frames(video_path: str, max_frames: int = 30) -> List[str]:
    """Extract evenly-sampled frames from video"""
    frames = []
    try:
        import cv2
        cap          = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames <= 0:
            return frames

        step      = max(1, total_frames // max_frames)
        frame_dir = tempfile.mkdtemp()
        count = saved = 0

        while cap.isOpened() and saved < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            if count % step == 0:
                path = os.path.join(frame_dir, f"frame_{saved:04d}.jpg")
                cv2.imwrite(path, frame)
                frames.append(path)
                saved += 1
            count += 1
        cap.release()
    except Exception as e:
        print(f"[VideoEngine] Frame extraction error: {e}")
    return frames


def _analyze_blink_patterns(frames: List[str]) -> Dict[str, Any]:
    """Analyse eye blink patterns — deepfakes often have abnormal blinking"""
    result = {"blink_anomaly": False, "blink_rate": None, "notes": []}
    try:
        import cv2
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        eye_cascade  = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
        eye_states   = []

        for fp in frames[:20]:
            img = cv2.imread(fp)
            if img is None:
                continue
            gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)
            if len(faces):
                x, y, w, h = faces[0]
                eyes = eye_cascade.detectMultiScale(gray[y:y+h, x:x+w])
                eye_states.append(len(eyes) >= 2)

        if len(eye_states) > 5:
            blinks = sum(1 for i in range(1, len(eye_states)) if eye_states[i] != eye_states[i-1])
            result["blink_rate"] = blinks
            if blinks == 0:
                result["blink_anomaly"] = True
                result["notes"].append("Zero blinks detected — abnormal for real video")
            elif blinks > 15:
                result["blink_anomaly"] = True
                result["notes"].append("Excessive blink rate detected — possible deepfake artifact")
    except Exception as e:
        print(f"[BlinkAnalysis] Error: {e}")
    return result


def _analyze_face_consistency(frames: List[str]) -> Dict[str, Any]:
    """Check facial landmark consistency across frames"""
    result = {"consistent": True, "issues": [], "artifact_count": 0}
    try:
        import cv2
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        face_sizes   = []
        blur_scores  = []

        for fp in frames[:15]:
            img = cv2.imread(fp)
            if img is None:
                continue
            gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)
            if len(faces):
                x, y, w, h = faces[0]
                face_sizes.append(w * h)
                blur_scores.append(cv2.Laplacian(gray[y:y+h, x:x+w], cv2.CV_64F).var())

        if face_sizes and max(face_sizes) / max(min(face_sizes), 1) > 3:
            result["issues"].append("Inconsistent face size across frames")
            result["artifact_count"] += 1

        if blur_scores:
            avg  = sum(blur_scores) / len(blur_scores)
            var  = sum((b - avg) ** 2 for b in blur_scores) / len(blur_scores)
            if var > 5000:
                result["issues"].append("Inconsistent sharpness in facial regions")
                result["artifact_count"] += 1
            if avg < 30:
                result["issues"].append("Unusually low sharpness — possible synthetic generation")
                result["artifact_count"] += 1

        result["consistent"] = result["artifact_count"] == 0
    except Exception as e:
        print(f"[FaceConsistency] Error: {e}")
    return result


def _analyze_frame_artifacts(frames: List[str]) -> List[str]:
    """Detect GAN-specific frame artifacts via noise analysis"""
    artifacts = []
    try:
        import cv2
        noise_levels = []
        for fp in frames[:10]:
            img = cv2.imread(fp)
            if img is None:
                continue
            noise_levels.append(abs(cv2.Laplacian(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.CV_64F)).mean())

        if noise_levels:
            avg = sum(noise_levels) / len(noise_levels)
            var = sum((n - avg) ** 2 for n in noise_levels) / len(noise_levels)
            if var > 200:
                artifacts.append("High frame-to-frame noise variance — possible GAN generation")
            if avg > 50 and var > 100:
                artifacts.append("Inconsistent texture patterns across frames")
    except Exception as e:
        print(f"[FrameArtifacts] Error: {e}")
    return artifacts


async def analyze_video(video_path: str) -> Dict[str, Any]:
    """
    Main video analysis pipeline:
    1. Frame extraction
    2. Blink pattern analysis
    3. Face consistency analysis
    4. Frame artifact detection
    5. Ollama local LLM reasoning
    """
    start_time = time.time()
    frames     = _extract_frames(video_path)

    if not frames:
        return {
            "credibility_score":  50,
            "verdict":            "UNCERTAIN",
            "deepfake_risk":      "MEDIUM",
            "lip_sync_mismatch":  False,
            "blink_anomaly":      False,
            "voice_synthetic":    False,
            "frame_artifacts":    ["Could not extract frames for analysis"],
            "reasoning":          "Video could not be processed. Check format compatibility.",
            "confidence":         0.3,
            "processing_time_ms": int((time.time() - start_time) * 1000),
        }

    blink_result   = _analyze_blink_patterns(frames)
    face_result    = _analyze_face_consistency(frames)
    frame_artifacts = _analyze_frame_artifacts(frames) + face_result["issues"]

    deepfake_score  = 0
    if blink_result["blink_anomaly"]:       deepfake_score += 35
    deepfake_score += face_result["artifact_count"] * 20
    deepfake_score += len(frame_artifacts)  * 15
    deepfake_score  = min(deepfake_score, 95)

    credibility_score = max(5, 100 - deepfake_score)
    deepfake_risk     = "HIGH" if deepfake_score > 60 else "MEDIUM" if deepfake_score > 30 else "LOW"

    reasoning, verdict = await video_forensic_reasoning(
        blink_result=blink_result,
        face_result=face_result,
        frame_artifacts=frame_artifacts,
        credibility_score=credibility_score,
        frames_analyzed=len(frames),
    )

    # Cleanup temp frames
    for fp in frames:
        try:
            os.remove(fp)
        except Exception:
            pass

    return {
        "credibility_score":  credibility_score,
        "verdict":            verdict,
        "deepfake_risk":      deepfake_risk,
        "lip_sync_mismatch":  False,
        "blink_anomaly":      blink_result["blink_anomaly"],
        "voice_synthetic":    False,
        "frame_artifacts":    frame_artifacts,
        "reasoning":          reasoning,
        "confidence":         round(0.4 + abs(credibility_score - 50) / 100, 2),
        "processing_time_ms": int((time.time() - start_time) * 1000),
        "frames_analyzed":    len(frames),
    }
