# Contributing to TruthLens AI

## Setup for Development

1. **Clone the repo**
   ```bash
   git clone https://github.com/YOUR_USERNAME/truthlens-ai.git
   cd truthlens-ai
   ```

2. **Install Ollama** (free, local AI)
   - Download: https://ollama.com/download
   - Pull model: `ollama pull gemma3:4b`

3. **Backend setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   ```

4. **Frontend setup**
   ```bash
   cd frontend
   npm install
   cp .env.example .env.local
   ```

## Running Locally

```bash
# Terminal 1: Ollama (must be running)
ollama serve

# Terminal 2: Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000

# Terminal 3: Frontend
cd frontend
npm run dev
```

Visit: http://localhost:3000

## Code Style

- **Python**: 120 char line length max, PEP8
- **TypeScript**: Prettier formatting (run `npm run format`)
- No Anthropic/paid API dependencies

## Adding Features

1. **New detection module**: Add to `ai-engine/[module_name]/analyzer.py`
2. **New route**: Add to `backend/api/routes/[feature].py`
3. **New UI component**: Add to `frontend/src/components/`

All reasoning should go through `ollama_service.py` — never add direct API calls elsewhere.

## Before Pushing

```bash
# Lint Python
flake8 ai-engine backend

# Type-check TypeScript
cd frontend && npm run type-check

# Test syntax
python -m py_compile ai-engine/**/*.py backend/**/*.py
```

## Issues & PRs

- **Bug reports**: Include `backend/api/health` output
- **Features**: Propose in Issues first
- **PRs**: Link to relevant issue, test locally with Ollama running
