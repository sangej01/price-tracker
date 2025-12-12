@echo off
echo Starting Price Tracker Frontend...
setlocal

REM Always resolve paths relative to this script (works when double-clicked)
cd /d "%~dp0\..\frontend" || (
    echo [ERROR] Could not cd into frontend folder from: %~dp0
    pause
    exit /b 1
)

echo Checking for node_modules...
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
)

echo Starting development server...
REM Bind to all interfaces so it's reachable over LAN/Tailscale
npm run dev -- --host 0.0.0.0


