@echo off
echo ============================================
echo   AutoSecAI — Full Project Setup
echo ============================================
echo.

REM ── Backend setup ──────────────────────────────────────────────

echo [1/4] Setting up Python virtual environment...
cd /d "%~dp0..\backend"

if not exist ".venv" (
    python -m venv .venv
    echo       Created .venv
) else (
    echo       .venv already exists — skipping
)

call .venv\Scripts\activate.bat

echo [2/4] Installing Python dependencies...
pip install -r requirements.txt --quiet
echo       Done.
echo.

REM ── Frontend setup ─────────────────────────────────────────────

echo [3/4] Installing Node.js dependencies...
cd /d "%~dp0..\frontend"
npm install
echo       Done.
echo.

REM ── Environment check ─────────────────────────────────────────

echo [4/4] Checking .env configuration...
cd /d "%~dp0..\backend"

if not exist ".env" (
    echo       WARNING: backend/.env file not found!
    echo       Create it with your GITHUB_TOKEN and GROQ_API_KEY.
) else (
    echo       .env file found.
)

echo.
echo ============================================
echo   Setup Complete!
echo.
echo   To start the app:
echo     scripts\start_backend.bat
echo     scripts\start_frontend.bat
echo ============================================

pause
