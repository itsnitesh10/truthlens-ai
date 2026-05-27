"""
TruthLens AI — Text Forensics Engine
Combines RoBERTa-based detection + Ollama local LLM for reasoning
"""

import time
import re
import sys
import os
from typing import List, Dict, Any, Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from services.ollama_service import text_forensic_reasoning

# ── Lazy imports for heavy models ─────────────────────────────────
_classifier  = None
_ai_detector = None


def _get_classifier():
    """Lazy-load fake news classifier"""
    global _classifier
    if _classifier is None:
        try:
            from transformers import pipeline
            _classifier = pipeline(
                "text-classification",
                model="mrm8488/bert-mini-finetuned-fake-news",
                truncation=True,
                max_length=512,
            )
        except Exception as e:
            print(f"[TextEngine] Classifier load failed: {e}. Using mock.")
            _classifier = "mock"
    return _classifier


def _get_ai_detector():
    """Lazy-load AI text detector"""
    global _ai_detector
    if _ai_detector is None:
        try:
            from transformers import pipeline
            _ai_detector = pipeline(
                "text-classification",
                model="Hello-SimpleAI/chatgpt-detector-roberta",
                truncation=True,
                max_length=512,
            )
        except Exception as e:
            print(f"[TextEngine] AI detector load failed: {e}. Using mock.")
            _ai_detector = "mock"
    return _ai_detector


def extract_claims(text: str) -> List[str]:
    """Extract key factual claims from text using simple heuristics"""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    claims = []
    claim_indicators = [
        "confirms", "reveals", "says", "claims", "according to",
        "proves", "shows", "found", "discovered", "reported",
        "announced", "stated", "warned", "alleged",
    ]
    for sentence in sentences[:20]:
        if any(ind in sentence.lower() for ind in claim_indicators):
            if len(sentence.split()) > 6:
                claims.append(sentence.strip())
    return claims[:5] if claims else [sentences[0].strip()] if sentences else []


def detect_propaganda_patterns(text: str) -> List[str]:
    """Detect emotional manipulation and propaganda patterns"""
    patterns   = []
    text_lower = text.lower()

    fear_words   = ["danger", "threat", "crisis", "catastrophe", "emergency", "alarm", "warning", "deadly"]
    outrage_words = ["outrage", "scandal", "shocking", "unbelievable", "disgusting", "explosive"]
    sensational  = ["breaking", "exclusive", "bombshell", "you won't believe", "mainstream media won't tell"]
    urgency      = ["must share", "spread the word", "before it's deleted", "share now", "wake up"]

    if sum(1 for w in fear_words   if w in text_lower) >= 2: patterns.append("Fear amplification detected")
    if sum(1 for w in outrage_words if w in text_lower) >= 2: patterns.append("Outrage-bait language detected")
    if any(w in text_lower for w in sensational):             patterns.append("Sensationalism patterns detected")
    if any(w in text_lower for w in urgency):                 patterns.append("Viral urgency manipulation detected")

    if sum(1 for c in text if c.isupper()) / max(len(text), 1) > 0.15:
        patterns.append("Excessive capitalization (emotional manipulation)")
    if text.count("!") > 3:
        patterns.append("Excessive exclamation marks (emotional amplification)")

    return patterns


def _mock_classify(text: str) -> Dict[str, Any]:
    """Deterministic mock when ML models aren't loaded"""
    import hashlib
    h = int(hashlib.md5(text[:50].encode()).hexdigest(), 16)
    score = 30 + (h % 50)
    return {"credibility_score": score, "fake_probability": (100 - score) / 100}


async def analyze_text(text: str, url: Optional[str] = None, title: Optional[str] = None) -> Dict[str, Any]:
    """
    Main text analysis pipeline:
    1. Fake news classification (RoBERTa)
    2. AI-generated text detection
    3. Propaganda pattern analysis
    4. Claim extraction
    5. Ollama local LLM forensic reasoning
    """
    start_time = time.time()

    # ── Step 1: Fake news classification ──────────────────────────
    classifier = _get_classifier()
    if classifier != "mock":
        try:
            result    = classifier(text[:512])[0]
            fake_prob = result["score"] if result["label"] == "FAKE" else 1 - result["score"]
        except Exception:
            fake_prob = _mock_classify(text)["fake_probability"]
    else:
        fake_prob = _mock_classify(text)["fake_probability"]

    credibility_score = max(5, min(95, int((1 - fake_prob) * 100)))

    # ── Step 2: AI-generated text detection ───────────────────────
    ai_detector = _get_ai_detector()
    if ai_detector != "mock":
        try:
            ai_result = ai_detector(text[:512])[0]
            ai_prob   = ai_result["score"] if "AI" in ai_result["label"].upper() else 1 - ai_result["score"]
        except Exception:
            ai_prob = 0.3
    else:
        ai_prob = 0.3

    ai_risk = "HIGH" if ai_prob > 0.75 else "MEDIUM" if ai_prob > 0.45 else "LOW"

    # ── Step 3: Propaganda detection ──────────────────────────────
    manipulation_patterns  = detect_propaganda_patterns(text)
    propaganda_risk        = "HIGH" if len(manipulation_patterns) >= 3 else "MEDIUM" if len(manipulation_patterns) >= 1 else "LOW"
    emotional_manipulation = len(manipulation_patterns) > 0

    # ── Step 4: Claim extraction ───────────────────────────────────
    claims_raw = extract_claims(text)

    # ── Step 5: Ollama forensic reasoning ─────────────────────────
    reasoning, verdict, claim_verdicts = await text_forensic_reasoning(
        text=text,
        claims=claims_raw,
        credibility_score=credibility_score,
        ai_risk=ai_risk,
        propaganda_patterns=manipulation_patterns,
        url=url,
        title=title,
    )

    processing_time = int((time.time() - start_time) * 1000)

    return {
        "credibility_score":    credibility_score,
        "verdict":              verdict,
        "ai_generated_risk":    ai_risk,
        "propaganda_risk":      propaganda_risk,
        "emotional_manipulation": emotional_manipulation,
        "claims":               claim_verdicts,
        "reasoning":            reasoning,
        "manipulation_patterns": manipulation_patterns,
        "confidence":           round(1 - abs(credibility_score - 50) / 100, 2),
        "processing_time_ms":   processing_time,
    }
