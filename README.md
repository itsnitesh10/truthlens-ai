# TruthLens AI 
### Multi-Modal Misinformation Forensics Platform
**100% Free — Powered by Ollama + gemma3:4b (runs locally on CPU)**

---

## Quick Start (Windows + VS Code)

### Prerequisites
- Python 3.10+
- Node.js 18+
- [Ollama](https://ollama.com/download) (free, local AI)

---

## Setup

### 1. Install Ollama + pull the model (one-time)
```bash
# Download Ollama from https://ollama.com/download
# Then in a terminal:
ollama pull gemma3:4b
```

### 2. Run setup script (auto-installs everything)
```
Double-click setup.bat
```

Or manually:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env

cd ..\frontend
npm install
copy .env.example .env.local
```

---

##  Running the App

### Terminal 1 — Ollama (keep running)
```bash
ollama serve
```

### Terminal 2 — Backend
```bash
cd backend
venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

### Terminal 3 — Frontend
```bash
cd frontend
npm run dev
```

Visit: **http://localhost:3000**  
API Docs: **http://localhost:8000/docs**  
Health Check: **http://localhost:8000/api/health**

---

## AI Architecture

| Component | Technology | Cost |
|-----------|-----------|------|
| Fake news detection | RoBERTa (HuggingFace) | Free |
| AI text detection | ChatGPT-detector-roberta | Free |
| Image forensics | OpenCV + PIL + ELA | Free |
| Video analysis | DeepFace + MediaPipe | Free |
| **Forensic reasoning** | **Ollama gemma3:4b (local)** | **Free** |

### Ollama Config (backend/.env)
```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma3:4b
OLLAMA_TIMEOUT_SECONDS=120
```

> **Offline fallback:** If Ollama is not running, all endpoints still return
> deterministic mock responses — the app never crashes.

---

## Project Structure

```
truthlens-ai/
├── frontend/          # Next.js 14 + Tailwind + Framer Motion
├── backend/           # FastAPI — routes, schemas, main
├── ai-engine/
│   ├── services/
│   │   └── ollama_service.py   ← All Ollama calls live here
│   ├── text_forensics/
│   ├── image_forensics/
│   ├── video_forensics/
│   └── reasoning_engine/
├── datasets/
├── docker/
└── docs/
```

---

## Switching Models

To use a different Ollama model, edit `backend/.env`:
```
OLLAMA_MODEL=llama3.2:3b      # lighter, faster
OLLAMA_MODEL=mistral:7b       # more capable
OLLAMA_MODEL=gemma3:4b        # default (recommended)
```
Then restart the backend.

---

## Phases
- **Phase 1** — Text Forensics + Dashboard 
- **Phase 2** — Image Manipulation Detection 
- **Phase 3** — Video Deepfake Detection 
- **Phase 4** — Forensic Reasoning Engine (Ollama) 
- **Phase 5** — Social Tracking + Browser Extension 
