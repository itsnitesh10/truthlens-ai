@echo off
echo ============================================
echo   TruthLens AI — Windows Setup Script
echo ============================================
echo.

:: Backend setup
echo [1/3] Setting up Python backend...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
echo   Backend ready.
echo.

:: Frontend setup
echo [2/3] Setting up Next.js frontend...
cd ..\frontend
call npm install
copy .env.example .env.local
echo   Frontend ready.
echo.

echo ============================================
echo   Setup Complete!
echo ============================================
echo.
echo   STEP 1 — Install Ollama (free, one-time):
echo     Download from: https://ollama.com/download
echo     Then run in a terminal:
echo     ollama pull gemma3:4b
echo.
echo   STEP 2 — Start Ollama (keep running):
echo     ollama serve
echo.
echo   STEP 3 — Open TWO more terminals:
echo.
echo   Terminal A (Backend):
echo     cd backend
echo     venv\Scripts\activate
echo     uvicorn main:app --reload --port 8000
echo.
echo   Terminal B (Frontend):
echo     cd frontend
echo     npm run dev
echo.
echo   Then open: http://localhost:3000
echo.
echo   NOTE: No API keys needed. Ollama runs 100%% locally for free.
echo   If Ollama is offline, the app still works with mock responses.
echo.
pause
