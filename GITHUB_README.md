# TruthLens AI  — Multi-Modal Misinformation Forensics Platform

[![Python Lint](https://github.com/YOUR_USERNAME/truthlens-ai/actions/workflows/python-lint.yml/badge.svg)](https://github.com/YOUR_USERNAME/truthlens-ai/actions)
[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Tech Stack](https://img.shields.io/badge/Stack-Next.js%20%7C%20FastAPI%20%7C%20Ollama-black)](README.md)

**100% Free. No Paid APIs. Runs Locally on CPU.**

Analyze text articles, images, and videos for misinformation, deepfakes, and manipulation using AI forensics powered by **Ollama** (local LLM).

![TruthLens Architecture](docs/architecture.png)

---

##  Features

### Text Forensics
- Fake news detection (RoBERTa)
- AI-generated text detection
- Propaganda pattern analysis
- Claim extraction & verification
- **0/100 credibility scoring**

### Image Forensics
- Error Level Analysis (ELA)
- Metadata inspection
- GAN artifact detection
- Face inconsistency detection
- Deepfake face analysis

### Video Analysis
- Per-frame deepfake detection
- Blink pattern anomaly detection
- Face consistency across frames
- GAN artifact detection
- Frame-level forensics

### Forensic Reasoning
- Multi-modal evidence synthesis
- Contradiction detection
- Evidence chain tracking
- Claude-like reasoning with **Ollama gemma3:4b** (free, local)
- Explainable verdicts with confidence scores

---

##  Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- [Ollama](https://ollama.com/download) (free, 5-minute install)

### Setup (3 steps)

```bash
# 1. Clone & install
git clone https://github.com/YOUR_USERNAME/truthlens-ai.git
cd truthlens-ai
./setup.bat  # Windows | bash setup.sh for Mac/Linux

# 2. Pull Ollama model (one-time, ~2.5GB)
ollama pull gemma3:4b

# 3. Run (3 terminals)
# Terminal A: Ollama
ollama serve

# Terminal B: Backend
cd backend && source venv/bin/activate && uvicorn main:app --reload

# Terminal C: Frontend
cd frontend && npm run dev
```

**Visit**: http://localhost:3000

---

##  Architecture

```
Frontend (Next.js 14 + Tailwind)
         ↓
FastAPI Backend (8 routes)
         ↓
    Multi-Modal Pipeline
    ├── Text Forensics (RoBERTa)
    ├── Image Forensics (OpenCV + ELA)
    ├── Video Analysis (DeepFace + MediaPipe)
    └── Ollama Reasoning Engine (local gemma3:4b)
```

**Key Innovation**: All reasoning happens locally via Ollama — zero paid API calls, zero privacy concerns.

---

##  AI Stack

| Component | Technology | Cost | Speed |
|---|---|---|---|
| Fake news | RoBERTa (HF) | Free | ~100ms |
| AI text | ChatGPT-detector-roberta | Free | ~100ms |
| Image forensics | OpenCV + PIL | Free | ~500ms |
| Video analysis | DeepFace + MediaPipe | Free | ~2s per video |
| **Reasoning** | **Ollama gemma3:4b** | **Free** | **~2-5s** |

---

##  Project Structure

```
truthlens-ai/
├── frontend/               # Next.js 14 + React + Tailwind
│   ├── src/app/           # Pages (/, /analyze, /about)
│   ├── src/components/    # Dashboard, upload, results UI
│   └── src/lib/api.ts     # API client
├── backend/               # FastAPI + Python
│   ├── main.py           # Entry point
│   ├── api/routes/       # 5 endpoints (text, image, video, reasoning, health)
│   ├── models/schemas.py # Pydantic schemas
│   └── requirements.txt   # Dependencies (no Anthropic!)
├── ai-engine/            # AI modules
│   ├── services/ollama_service.py  # ⭐ All Ollama logic here
│   ├── text_forensics/
│   ├── image_forensics/
│   ├── video_forensics/
│   └── reasoning_engine/
├── docs/                 # Architecture, API docs
├── docker/              # Docker & docker-compose
└── datasets/            # Dataset links & loaders
```

---

##  Configuration

### Local Ollama Settings (backend/.env)

```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma3:4b
OLLAMA_TIMEOUT_SECONDS=120
```

### Other Models (same format)

```
OLLAMA_MODEL=phi:2.7b        # Fastest (2.7B)
OLLAMA_MODEL=mistral:7b      # Most capable (7B)
OLLAMA_MODEL=llama3.2:3b     # Balanced (3B)
```

---

##  API Endpoints

### Health Check
```bash
GET /api/health
```
Returns Ollama status, model availability, all module readiness.

### Text Analysis
```bash
POST /api/analyze/text
{
  "text": "Article content...",
  "url": "https://...",
  "title": "Article title"
}
```

### Image Analysis
```bash
POST /api/analyze/image
# Multipart form: file (image)
```

### Video Analysis
```bash
POST /api/analyze/video
# Multipart form: file (video)
```

### Forensic Report
```bash
POST /api/reasoning/synthesize
{
  "text_result": {...},
  "image_result": {...},
  "video_result": {...},
  "original_claim": "..."
}
```

Full docs: http://localhost:8000/docs

---

##  Deployment

### Docker (Recommended)
```bash
docker-compose up -d
```

### Cloud (Render, Railway, Vercel)
See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step guides.

**Note**: Ollama runs locally on CPU. For cloud:
1. Self-host Ollama separately
2. Use lighter model (`phi:2.7b`)
3. Falls back to mock responses if offline

---

##  Testing

### Health Check
```bash
curl http://localhost:8000/api/health
```

### Sample Text Analysis
```bash
curl -X POST http://localhost:8000/api/analyze/text \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Breaking: Scientists discover new cure for cancer!",
    "title": "Cancer breakthrough"
  }'
```

---

##  Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, coding standards, and PR process.

**Quick contribute:**
1. Fork repo
2. Create feature branch: `git checkout -b feature/amazing-detection`
3. Commit: `git commit -m "Add X forensic detection"`
4. Push: `git push origin feature/amazing-detection`
5. PR against `main`

---

##   Roadmap

- [x] Phase 1: Text Forensics + Dashboard
- [x] Phase 2: Image Manipulation Detection
- [x] Phase 3: Video Deepfake Detection
- [x] Phase 4: Ollama Reasoning Engine
- [ ] Phase 5: Social media tracking + browser extension
- [ ] Audio deepfake detection
- [ ] Real-time misinformation trending
- [ ] Blockchain authenticity certificates

---

##  Disclaimer

TruthLens AI is a research & educational tool. It should not be used as sole arbiter of truth. Always cross-reference with authoritative sources and domain experts for critical decisions.

---

##  License

MIT — See [LICENSE](LICENSE)

---

##  Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/truthlens-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/truthlens-ai/discussions)
- **Docs**: [README.md](README.md) | [DEPLOYMENT.md](DEPLOYMENT.md) | [Architecture](docs/ARCHITECTURE.md)

---

##  Acknowledgments

- [Ollama](https://ollama.com) — Free local LLM
- [HuggingFace](https://huggingface.co) — Model hub
- [Next.js](https://nextjs.org) — Frontend framework
- [FastAPI](https://fastapi.tiangolo.com) — Backend framework

---

**Made with love for truth. Powered by Ollama. No paywalls.**
