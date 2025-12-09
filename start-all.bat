@echo off
echo Starting Price Tracker Application...
echo.
echo This will start both backend and frontend servers.
echo.

start "Price Tracker Backend" cmd /k call start-backend.bat
timeout /t 5 /nobreak >nul
start "Price Tracker Frontend" cmd /k call start-frontend.bat

echo.
echo Both servers are starting...
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:3000
echo.
echo Press any key to exit this window (servers will continue running)
pause >nul


