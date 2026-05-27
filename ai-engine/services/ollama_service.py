"""
TruthLens AI — Ollama Local LLM Service
Replaces Anthropic Claude API with free local Ollama (gemma3:4b)
Endpoint: http://localhost:11434/api/generate
"""

import os
import json
import re
import asyncio
import httpx
from typing import Optional, Any

# ── Config (from .env) ────────────────────────────────────────────
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL    = os.getenv("OLLAMA_MODEL", "gemma3:4b")
OLLAMA_TIMEOUT  = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "120"))


async def _call_ollama(prompt: str, expect_json: bool = True) -> Optional[str]:
    """
    Core async Ollama API call.
    Returns raw response text, or None if Ollama is unavailable.
    """
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,       # Low temp = consistent, deterministic forensic output
            "num_predict": 1024,
            "top_p": 0.9,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=OLLAMA_TIMEOUT) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()

    except httpx.ConnectError:
        print(f"[Ollama] Connection refused — is Ollama running on {OLLAMA_BASE_URL}?")
        return None
    except httpx.TimeoutException:
        print(f"[Ollama] Request timed out after {OLLAMA_TIMEOUT}s")
        return None
    except httpx.HTTPStatusError as e:
        print(f"[Ollama] HTTP error: {e.response.status_code} — {e.response.text[:200]}")
        return None
    except Exception as e:
        print(f"[Ollama] Unexpected error: {e}")
        return None


def _parse_json_response(raw: Optional[str], fallback: dict) -> dict:
    """
    Safely parse JSON from Ollama response.
    Strips markdown fences, extracts first JSON block found.
    Returns fallback dict if parsing fails.
    """
    if not raw:
        return fallback

    # Strip markdown code fences
    cleaned = re.sub(r"```json|```", "", raw).strip()

    # Try direct parse
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Try to extract first {...} block
    match = re.search(r"\{[\s\S]*\}", cleaned)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    print(f"[Ollama] Could not parse JSON from response: {cleaned[:200]}")
    return fallback


async def check_ollama_health() -> dict:
    """Health check — returns model availability status"""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            response.raise_for_status()
            models = response.json().get("models", [])
            model_names = [m.get("name", "") for m in models]
            model_available = any(OLLAMA_MODEL in name for name in model_names)
            return {
                "ollama_running": True,
                "model": OLLAMA_MODEL,
                "model_available": model_available,
                "available_models": model_names,
            }
    except Exception as e:
        return {
            "ollama_running": False,
            "model": OLLAMA_MODEL,
            "model_available": False,
            "error": str(e),
        }


# ═══════════════════════════════════════════════════════════════════
# TEXT FORENSICS REASONING
# ═══════════════════════════════════════════════════════════════════

async def text_forensic_reasoning(
    text: str,
    claims: list,
    credibility_score: int,
    ai_risk: str,
    propaganda_patterns: list,
    url: Optional[str] = None,
    title: Optional[str] = None,
) -> tuple:
    """
    Ollama-powered text forensic reasoning.
    Returns: (reasoning: str, verdict: str, claim_verdicts: list)
    """
    claims_str   = "\n".join(f"- {c}" for c in claims)          if claims               else "- None extracted"
    patterns_str = "\n".join(f"- {p}" for p in propaganda_patterns) if propaganda_patterns else "- None detected"

    prompt = f"""You are TruthLens AI, a misinformation forensics expert. Analyze this content and respond with ONLY a JSON object.

ARTICLE DATA:
Title: {title or 'Not provided'}
URL: {url or 'Not provided'}
Credibility Score (pre-analysis): {credibility_score}/100
AI-Generated Risk: {ai_risk}
Propaganda Patterns:
{patterns_str}
Extracted Claims:
{claims_str}
Article Text (first 600 chars):
{text[:600]}

Respond with this exact JSON (no other text, no markdown):
{{
  "verdict": "MISLEADING",
  "reasoning": "2-3 sentence forensic explanation",
  "claim_verdicts": [
    {{"claim": "claim text", "verdict": "SUPPORTED", "confidence": 0.7, "evidence": ["brief note"]}}
  ],
  "key_red_flags": ["flag1", "flag2"],
  "confidence": 0.75
}}

verdict must be one of: VERIFIED, LIKELY_TRUE, UNCERTAIN, MISLEADING, HIGHLY_MISLEADING, FABRICATED"""

    raw = await _call_ollama(prompt)

    fallback = {
        "verdict": _score_to_verdict(credibility_score),
        "reasoning": "Automated analysis completed. Local AI model unavailable for deep reasoning.",
        "claim_verdicts": [
            {"claim": c, "verdict": "UNVERIFIABLE", "confidence": 0.5, "evidence": ["Manual review needed"]}
            for c in claims
        ],
        "key_red_flags": propaganda_patterns[:3],
        "confidence": 0.5,
    }

    data = _parse_json_response(raw, fallback)

    verdict       = _validate_verdict(data.get("verdict", "UNCERTAIN"))
    reasoning     = data.get("reasoning", fallback["reasoning"])
    claim_verdicts = data.get("claim_verdicts", fallback["claim_verdicts"])

    return reasoning, verdict, claim_verdicts


# ═══════════════════════════════════════════════════════════════════
# IMAGE FORENSICS REASONING
# ═══════════════════════════════════════════════════════════════════

async def image_forensic_reasoning(
    metadata_issues: list,
    ela_score: float,
    face_issues: list,
    credibility_score: int,
) -> tuple:
    """
    Ollama-powered image forensic reasoning.
    Returns: (reasoning: str, verdict: str)
    """
    meta_str = "\n".join(f"- {i}" for i in metadata_issues) if metadata_issues else "- None"
    face_str = "\n".join(f"- {i}" for i in face_issues)     if face_issues      else "- None"

    prompt = f"""You are TruthLens AI, an image forensics expert. Respond with ONLY a JSON object.

IMAGE FORENSIC SIGNALS:
ELA Anomaly Score: {ela_score} (0.0=clean, 1.0=heavily manipulated)
Credibility Score: {credibility_score}/100
Metadata Issues:
{meta_str}
Facial Inconsistencies:
{face_str}

Respond with this exact JSON (no other text):
{{
  "verdict": "UNCERTAIN",
  "reasoning": "2-3 sentence forensic explanation of image authenticity",
  "confidence": 0.7
}}

verdict must be one of: VERIFIED, LIKELY_TRUE, UNCERTAIN, MISLEADING, HIGHLY_MISLEADING, FABRICATED"""

    raw = await _call_ollama(prompt)

    fallback = {
        "verdict": _score_to_verdict(credibility_score),
        "reasoning": "Image forensic signals analyzed. Local AI model unavailable for deep reasoning.",
        "confidence": 0.5,
    }

    data    = _parse_json_response(raw, fallback)
    verdict  = _validate_verdict(data.get("verdict", "UNCERTAIN"))
    reasoning = data.get("reasoning", fallback["reasoning"])

    return reasoning, verdict


# ═══════════════════════════════════════════════════════════════════
# VIDEO FORENSICS REASONING
# ═══════════════════════════════════════════════════════════════════

async def video_forensic_reasoning(
    blink_result: dict,
    face_result: dict,
    frame_artifacts: list,
    credibility_score: int,
    frames_analyzed: int,
) -> tuple:
    """
    Ollama-powered video deepfake reasoning.
    Returns: (reasoning: str, verdict: str)
    """
    artifacts_str = "\n".join(f"- {a}" for a in frame_artifacts)         if frame_artifacts              else "- None"
    blink_str     = "\n".join(f"- {n}" for n in blink_result.get("notes", [])) if blink_result.get("notes") else "- Normal pattern"

    prompt = f"""You are TruthLens AI, a deepfake forensics expert. Respond with ONLY a JSON object.

VIDEO FORENSIC SIGNALS:
Frames Analyzed: {frames_analyzed}
Credibility Score: {credibility_score}/100
Blink Analysis: {blink_str}
Face Consistency Issues: {face_result.get('artifact_count', 0)} found
Frame Artifacts:
{artifacts_str}

Respond with this exact JSON (no other text):
{{
  "verdict": "UNCERTAIN",
  "reasoning": "2-3 sentence forensic explanation of video authenticity",
  "confidence": 0.65
}}

verdict must be one of: VERIFIED, LIKELY_TRUE, UNCERTAIN, MISLEADING, HIGHLY_MISLEADING, FABRICATED"""

    raw = await _call_ollama(prompt)

    fallback = {
        "verdict": _score_to_verdict(credibility_score),
        "reasoning": "Video frame analysis completed. Local AI model unavailable for deep reasoning.",
        "confidence": 0.5,
    }

    data     = _parse_json_response(raw, fallback)
    verdict   = _validate_verdict(data.get("verdict", "UNCERTAIN"))
    reasoning = data.get("reasoning", fallback["reasoning"])

    return reasoning, verdict


# ═══════════════════════════════════════════════════════════════════
# MASTER FORENSIC SYNTHESIS
# ═══════════════════════════════════════════════════════════════════

async def master_forensic_synthesis(
    text_result:    Optional[dict],
    image_result:   Optional[dict],
    video_result:   Optional[dict],
    evidence_chain: list,
    contradictions: list,
    combined_score: int,
    original_claim: Optional[str],
) -> tuple:
    """
    Ollama master synthesis — combines all modality results.
    Returns: (final_verdict, narrative, key_findings, recommendations)
    """
    summaries = []
    if text_result:
        summaries.append(f"TEXT: verdict={text_result.get('verdict')}, score={text_result.get('credibility_score')}/100, ai_risk={text_result.get('ai_generated_risk')}")
    if image_result:
        summaries.append(f"IMAGE: verdict={image_result.get('verdict')}, score={image_result.get('credibility_score')}/100, ela={image_result.get('ela_anomaly_score')}, manipulated={image_result.get('manipulation_detected')}")
    if video_result:
        summaries.append(f"VIDEO: verdict={video_result.get('verdict')}, score={video_result.get('credibility_score')}/100, deepfake_risk={video_result.get('deepfake_risk')}")

    modality_str      = "\n".join(f"- {s}" for s in summaries)
    contradictions_str = "\n".join(f"- {c}" for c in contradictions) if contradictions else "- None"

    prompt = f"""You are TruthLens AI master forensic analyst. Synthesize all signals into a final verdict. Respond with ONLY a JSON object.

INVESTIGATION SUMMARY:
Original Claim: {original_claim or 'Not specified'}
Combined Credibility Score: {combined_score}/100
Modality Results:
{modality_str}
Contradictions:
{contradictions_str}

Respond with this exact JSON (no other text):
{{
  "final_verdict": "MISLEADING",
  "narrative": "3-4 sentence forensic investigator summary of the complete multi-modal analysis",
  "key_findings": [
    "Specific finding 1",
    "Specific finding 2",
    "Specific finding 3"
  ],
  "recommendations": [
    "What the user should do next",
    "How to verify this content",
    "Safety advice if sharing"
  ],
  "confidence": 0.78
}}

final_verdict must be one of: VERIFIED, LIKELY_TRUE, UNCERTAIN, MISLEADING, HIGHLY_MISLEADING, FABRICATED"""

    raw = await _call_ollama(prompt)

    fallback_verdict = _score_to_verdict(combined_score)
    fallback = {
        "final_verdict":  fallback_verdict,
        "narrative":      f"Multi-modal forensic analysis completed with combined credibility score of {combined_score}/100. Local AI model was unavailable for deep synthesis.",
        "key_findings":   [f"Combined credibility score: {combined_score}/100", f"Overall verdict: {fallback_verdict}", f"Modalities analyzed: {len(summaries)}"],
        "recommendations": ["Verify with trusted news sources before sharing", "Cross-reference with official fact-checking sites", "Do not share until independently verified"],
        "confidence":     0.5,
    }

    data = _parse_json_response(raw, fallback)

    return (
        _validate_verdict(data.get("final_verdict", fallback_verdict)),
        data.get("narrative",         fallback["narrative"]),
        data.get("key_findings",      fallback["key_findings"]),
        data.get("recommendations",   fallback["recommendations"]),
    )


# ═══════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════

VALID_VERDICTS = {"VERIFIED", "LIKELY_TRUE", "UNCERTAIN", "MISLEADING", "HIGHLY_MISLEADING", "FABRICATED"}

def _validate_verdict(verdict: str) -> str:
    """Ensure verdict is always one of the valid enum values"""
    v = str(verdict).strip().upper()
    return v if v in VALID_VERDICTS else "UNCERTAIN"

def _score_to_verdict(score: int) -> str:
    """Fallback: derive verdict from numeric credibility score"""
    if score >= 75: return "LIKELY_TRUE"
    if score >= 50: return "UNCERTAIN"
    if score >= 30: return "MISLEADING"
    return "HIGHLY_MISLEADING"
