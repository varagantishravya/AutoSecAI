@echo off
echo ============================================
echo   AutoSecAI — Starting Backend Server
echo ============================================
echo.

cd /d "%~dp0..\backend"

if exist "..\.venv\Scripts\activate.bat" (
    call ..\.venv\Scripts\activate.bat
    echo Virtual environment activated.
) else (
    echo WARNING: .venv not found in the root directory. Run setup.bat first.
    echo Attempting to run without venv...
)

echo Starting uvicorn on http://127.0.0.1:8000 ...
echo.
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

pause
