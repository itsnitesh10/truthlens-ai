"""
TruthLens AI — Pydantic Models (Request + Response Schemas)
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class VerdictLevel(str, Enum):
    VERIFIED = "VERIFIED"
    LIKELY_TRUE = "LIKELY_TRUE"
    UNCERTAIN = "UNCERTAIN"
    MISLEADING = "MISLEADING"
    HIGHLY_MISLEADING = "HIGHLY_MISLEADING"
    FABRICATED = "FABRICATED"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# ── Text Analysis ─────────────────────────────────────────────────

class TextAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Article or claim text to analyze")
    url: Optional[str] = Field(None, description="Source URL if available")
    title: Optional[str] = Field(None, description="Article title")


class ClaimResult(BaseModel):
    claim: str
    verdict: str
    confidence: float
    evidence: List[str]


class TextAnalysisResponse(BaseModel):
    credibility_score: int = Field(..., ge=0, le=100)
    verdict: VerdictLevel
    ai_generated_risk: RiskLevel
    propaganda_risk: RiskLevel
    emotional_manipulation: bool
    claims: List[ClaimResult]
    reasoning: str
    manipulation_patterns: List[str]
    confidence: float
    processing_time_ms: int


# ── Image Analysis ────────────────────────────────────────────────

class ImageAnalysisResponse(BaseModel):
    credibility_score: int = Field(..., ge=0, le=100)
    verdict: VerdictLevel
    ai_generated_risk: RiskLevel
    manipulation_detected: bool
    ela_anomaly_score: float
    metadata_issues: List[str]
    face_inconsistencies: List[str]
    reasoning: str
    confidence: float
    processing_time_ms: int


# ── Video Analysis ────────────────────────────────────────────────

class VideoAnalysisResponse(BaseModel):
    credibility_score: int = Field(..., ge=0, le=100)
    verdict: VerdictLevel
    deepfake_risk: RiskLevel
    lip_sync_mismatch: bool
    blink_anomaly: bool
    voice_synthetic: bool
    frame_artifacts: List[str]
    reasoning: str
    confidence: float
    processing_time_ms: int


# ── Forensic Reasoning ────────────────────────────────────────────

class ForensicReasoningRequest(BaseModel):
    text_result: Optional[Dict[str, Any]] = None
    image_result: Optional[Dict[str, Any]] = None
    video_result: Optional[Dict[str, Any]] = None
    original_claim: Optional[str] = None


class EvidenceItem(BaseModel):
    type: str
    description: str
    confidence: float
    source: str


class ForensicReasoningResponse(BaseModel):
    final_verdict: VerdictLevel
    overall_credibility_score: int
    overall_risk: RiskLevel
    key_findings: List[str]
    evidence_chain: List[EvidenceItem]
    contradictions: List[str]
    reasoning_narrative: str
    confidence: float
    recommendations: List[str]
