# TruthLens AI — Architecture

## System Flow

```
User Input (Text/Image/Video)
          │
          ▼
    FastAPI Backend
    (api/routes/)
          │
          ├── /api/analyze/text  → ai-engine/text_forensics/analyzer.py
          ├── /api/analyze/image → ai-engine/image_forensics/analyzer.py
          ├── /api/analyze/video → ai-engine/video_forensics/analyzer.py
          └── /api/reasoning/synthesize → ai-engine/reasoning_engine/master_reasoner.py
                                              │
                                              ▼
                                     Ollama (gemma3:4b — local, free)
                                              │
                                              ▼
                                    Forensic Report + Verdict
```

## Text Pipeline

```
Raw Text
  → Clean + Tokenize
  → RoBERTa fake news classifier
  → AI text detector (ChatGPT-detector-roberta)
  → Propaganda pattern matcher (regex + heuristics)
  → Claim extractor (sentence heuristics)
  → Claude API: forensic reasoning + verdict
  → Return: credibility_score, verdict, claims, patterns
```

## Image Pipeline

```
Uploaded Image
  → PIL metadata extraction (EXIF, timestamps, software)
  → ELA (Error Level Analysis) — JPEG recompression diff
  → OpenCV face detection + landmark analysis
  → Blur + texture uniformity checks
  → imagehash perceptual hash
  → Claude API: forensic verdict
  → Return: ela_score, metadata_issues, face_issues, verdict
```

## Video Pipeline

```
Uploaded Video
  → cv2.VideoCapture frame extraction (sampled)
  → Blink pattern analysis (eye cascade per frame)
  → Face size + sharpness consistency
  → Frame-level noise variance (GAN artifact indicator)
  → Claude API: forensic verdict
  → Return: deepfake_risk, blink_anomaly, frame_artifacts, verdict
```

## Reasoning Engine

```
{text_result, image_result, video_result}
  → Build evidence chain (structured items per modality)
  → Find cross-modal contradictions
  → Weighted credibility score
  → Claude API: master synthesis prompt
  → Return: final_verdict, narrative, key_findings, recommendations
```

## Key Design Decisions

1. **Lazy model loading** — HuggingFace models load on first use to keep startup fast
2. **Mock fallback** — if models fail to load, deterministic mock responses are used
3. **Claude for reasoning** — NLP/CV models provide signals; Claude synthesizes the verdict
4. **Async throughout** — all AI calls are async to support concurrent requests
5. **Modular routes** — each modality is independently callable
