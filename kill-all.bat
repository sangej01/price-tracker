@echo off
echo ============================================
echo  Stopping Price Tracker (All Processes)
echo ============================================
echo.

echo Killing Python processes...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM pythonw.exe 2>nul
if %errorlevel% equ 0 (
    echo   [OK] Python processes stopped
) else (
    echo   [INFO] No Python processes found
)

echo.
echo Killing Node.js processes...
taskkill /F /IM node.exe 2>nul
if %errorlevel% equ 0 (
    echo   [OK] Node.js processes stopped
) else (
    echo   [INFO] No Node.js processes found
)

echo.
echo ============================================
echo  All processes stopped!
echo ============================================
echo.
echo Ready to restart with: start-all.bat
pause

