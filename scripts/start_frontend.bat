@echo off
echo ============================================
echo   AutoSecAI — Starting Frontend Dev Server
echo ============================================
echo.

cd /d "%~dp0..\frontend"

if not exist "node_modules" (
    echo node_modules not found. Running npm install...
    npm install
    echo.
)

echo Starting Vite dev server...
echo.
npm run dev

pause
