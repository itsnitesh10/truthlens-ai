"""
TruthLens AI — Forensic Reasoning Engine
The HEART of the platform — multi-modal synthesis with Ollama local LLM
"""

import os
import sys
import time
from typing import Dict, Any, List, Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from services.ollama_service import master_forensic_synthesis

VERDICT_WEIGHTS = {
    "VERIFIED":          90,
    "LIKELY_TRUE":       72,
    "UNCERTAIN":         50,
    "MISLEADING":        30,
    "HIGHLY_MISLEADING": 15,
    "FABRICATED":        5,
}


def _weighted_score(results: List[Dict[str, Any]]) -> int:
    scores = [r.get("credibility_score", 50) for r in results if r]
    return int(sum(scores) / len(scores)) if scores else 50


async def generate_forensic_report(
    text_result:  Optional[Dict[str, Any]] = None,
    image_result: Optional[Dict[str, Any]] = None,
    video_result: Optional[Dict[str, Any]] = None,
    original_claim: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Master forensic synthesis:
    1. Collect all module outputs
    2. Find contradictions
    3. Build evidence chain
    4. Ollama LLM for final verdict + narrative
    """
    start_time     = time.time()
    active_results = [r for r in [text_result, image_result, video_result] if r]

    if not active_results:
        return {
            "final_verdict":           "UNCERTAIN",
            "overall_credibility_score": 50,
            "overall_risk":            "MEDIUM",
            "key_findings":            ["No analysis data provided"],
            "evidence_chain":          [],
            "contradictions":          [],
            "reasoning_narrative":     "No media was provided for analysis.",
            "confidence":              0.1,
            "recommendations":         ["Please upload media for analysis"],
        }

    evidence_chain  = _build_evidence_chain(text_result, image_result, video_result)
    contradictions  = _find_contradictions(text_result, image_result, video_result)
    combined_score  = _weighted_score(active_results)

    final_verdict, narrative, key_findings, recommendations = await master_forensic_synthesis(
        text_result=text_result,
        image_result=image_result,
        video_result=video_result,
        evidence_chain=evidence_chain,
        contradictions=contradictions,
        combined_score=combined_score,
        original_claim=original_claim,
    )

    if combined_score >= 70:   overall_risk = "LOW"
    elif combined_score >= 45: overall_risk = "MEDIUM"
    elif combined_score >= 25: overall_risk = "HIGH"
    else:                      overall_risk = "CRITICAL"

    return {
        "final_verdict":             final_verdict,
        "overall_credibility_score": combined_score,
        "overall_risk":              overall_risk,
        "key_findings":              key_findings,
        "evidence_chain":            evidence_chain,
        "contradictions":            contradictions,
        "reasoning_narrative":       narrative,
        "confidence":                round(0.5 + abs(combined_score - 50) / 100, 2),
        "recommendations":           recommendations,
        "modalities_analyzed":       [
            m for m, r in [("text", text_result), ("image", image_result), ("video", video_result)]
            if r is not None
        ],
        "processing_time_ms":        int((time.time() - start_time) * 1000),
    }


def _build_evidence_chain(
    text_result:  Optional[Dict],
    image_result: Optional[Dict],
    video_result: Optional[Dict],
) -> List[Dict[str, Any]]:
    chain = []

    if text_result:
        chain.append({
            "type": "text_analysis",
            "description": f"Text credibility: {text_result.get('credibility_score','?')}/100 — {text_result.get('verdict','UNCERTAIN')}",
            "confidence": text_result.get("confidence", 0.5),
            "source": "NLP + Ollama Forensics Engine",
        })
        for pattern in text_result.get("manipulation_patterns", [])[:3]:
            chain.append({"type": "text_manipulation", "description": pattern, "confidence": 0.75, "source": "Pattern Recognition Engine"})

    if image_result:
        chain.append({
            "type": "image_analysis",
            "description": f"Image credibility: {image_result.get('credibility_score','?')}/100 — ELA score: {image_result.get('ela_anomaly_score','?')}",
            "confidence": image_result.get("confidence", 0.5),
            "source": "Computer Vision Engine",
        })
        for issue in image_result.get("metadata_issues", [])[:2]:
            chain.append({"type": "image_metadata", "description": issue, "confidence": 0.8, "source": "Metadata Forensics"})

    if video_result:
        chain.append({
            "type": "video_analysis",
            "description": f"Video deepfake risk: {video_result.get('deepfake_risk','?')} — {video_result.get('frames_analyzed','?')} frames analyzed",
            "confidence": video_result.get("confidence", 0.5),
            "source": "Video Forensics Engine",
        })
        if video_result.get("blink_anomaly"):
            chain.append({"type": "deepfake_indicator", "description": "Abnormal blink pattern detected in video", "confidence": 0.8, "source": "Blink Pattern Analyzer"})

    return chain


def _find_contradictions(
    text_result:  Optional[Dict],
    image_result: Optional[Dict],
    video_result: Optional[Dict],
) -> List[str]:
    contradictions = []
    verdicts = {}
    if text_result:  verdicts["text"]  = VERDICT_WEIGHTS.get(text_result.get("verdict",  "UNCERTAIN"), 50)
    if image_result: verdicts["image"] = VERDICT_WEIGHTS.get(image_result.get("verdict", "UNCERTAIN"), 50)
    if video_result: verdicts["video"] = VERDICT_WEIGHTS.get(video_result.get("verdict", "UNCERTAIN"), 50)

    vals = list(verdicts.values())
    if len(vals) >= 2 and max(vals) - min(vals) > 40:
        contradictions.append(f"Conflicting signals: {' vs '.join(f'{k.upper()} ({v}/100)' for k, v in verdicts.items())}")

    if text_result and image_result:
        ts, is_ = text_result.get("credibility_score", 50), image_result.get("credibility_score", 50)
        if abs(ts - is_) > 40:
            contradictions.append(f"Text ({ts}/100) and image ({is_}/100) credibility scores diverge significantly")

    if image_result and image_result.get("manipulation_detected") and text_result:
        if text_result.get("credibility_score", 0) > 60:
            contradictions.append("Image manipulation detected despite credible article text — image may have been swapped")

    return contradictions
