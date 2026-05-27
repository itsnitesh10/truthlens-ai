# TruthLens AI — Deployment Guide

## Local Development
See README.md for Windows/Mac setup.

## Docker Deployment

```bash
docker-compose up -d
```

This starts:
- FastAPI backend (port 8000)
- Next.js frontend (port 3000)
- PostgreSQL database
- Ollama service must run separately

## Cloud Deployment

### Option 1: Render (free tier)

1. **Backend**
   - Push repo to GitHub
   - Create new Web Service on Render
   - Build: `pip install -r backend/requirements.txt`
   - Start: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Set env vars: `OLLAMA_BASE_URL`, `OLLAMA_MODEL`, etc.
   - **Important**: Render's free tier runs on shared CPU, so Ollama will be slow

2. **Frontend**
   - Create new Static Site on Render
   - Build command: `cd frontend && npm run build`
   - Publish directory: `frontend/.next`
   - Set `NEXT_PUBLIC_API_URL=https://your-backend.onrender.com`

### Option 2: Vercel (frontend) + Railway (backend)

**Frontend** (Vercel)
- Connect GitHub repo
- Framework: Next.js 14
- Vercel auto-deploys on push

**Backend** (Railway.app)
- Create PostgreSQL plugin
- Deploy with Railway CLI or GitHub integration
- Set all required env vars

### Note on Ollama in Cloud

Ollama runs locally on CPU. For cloud deployment:
1. **Option A**: Run self-hosted Ollama server separately, point `OLLAMA_BASE_URL` to it
2. **Option B**: Use a lighter model like `mistral:3b` for cloud CPU limits
3. **Option C**: Fallback to mock responses if Ollama unavailable (built-in)

## Environment Variables (Production)

```
OLLAMA_BASE_URL=http://your-ollama-server:11434
OLLAMA_MODEL=gemma3:4b
OLLAMA_TIMEOUT_SECONDS=120
APP_ENV=production
ALLOWED_ORIGINS=https://yourdomain.com
DATABASE_URL=postgresql://...
```

## Database Migrations

TruthLens uses async SQLAlchemy. To reset:

```bash
# In backend/
python -c "from models.database import Base, engine; Base.metadata.drop_all(engine); Base.metadata.create_all(engine)"
```

## Monitoring

Health endpoint:
```bash
curl http://localhost:8000/api/health
```

Returns Ollama status, model availability, all module readiness.

## Performance Tuning

- **Ollama context size**: Tune `num_predict` in `ollama_service.py`
- **Model size**: Smaller models = faster responses
  - `phi:2.7b` (fastest, on CPU)
  - `gemma3:4b` (default, balanced)
  - `mistral:7b` (most capable, slower)
- **Frontend**: Next.js `npm run build` for production
