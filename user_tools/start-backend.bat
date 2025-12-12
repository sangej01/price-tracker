@echo off
echo Starting Price Tracker Backend...
setlocal EnableExtensions EnableDelayedExpansion

REM If launched by double-click, pause when the server stops so errors are visible.
REM start-all.bat passes --no-pause to avoid extra prompts.
set "NO_PAUSE=0"
if /i "%~1"=="--no-pause" set "NO_PAUSE=1"

REM Always resolve paths relative to this script (works when double-clicked)
REM We run from the PROJECT ROOT and use the single root Pipfile/Pipfile.lock.
cd /d "%~dp0\.." || (
    echo [ERROR] Could not cd into project root from: %~dp0
    pause
    exit /b 1
)

REM Prefer pipenv if available (user preference)
where pipenv >nul 2>&1
if errorlevel 1 (
    echo [INFO] pipenv not found on PATH. Falling back to venv+pip...
    goto :venv_fallback
)

if not exist "Pipfile" (
    echo [WARN] pipenv is installed but root Pipfile is missing. Falling back to venv+pip...
    goto :venv_fallback
)

echo Using pipenv (root Pipfile found)...

REM Force pipenv to use Python 3.11 (avoids slow builds / Rust toolchain issues on 3.13)
set "PY311_EXE="
for /f "usebackq delims=" %%P in (`py -3.11 -c "import sys; print(sys.executable)" 2^>nul`) do set "PY311_EXE=%%P"
if not defined PY311_EXE (
    echo [ERROR] Python 3.11 not found. Install Python 3.11+ or ensure the Windows 'py' launcher can run: py -3.11
    set "EXITCODE=1"
    goto :maybe_pause_and_exit
)
set "PIPENV_PYTHON=%PY311_EXE%"

echo Installing/updating dependencies with pipenv...
pipenv sync
if errorlevel 1 (
    echo pipenv sync failed - trying pipenv install...
    pipenv install
    if errorlevel 1 (
        echo [ERROR] pipenv install failed.
        set "EXITCODE=1"
        goto :maybe_pause_and_exit
    )
)

echo Starting FastAPI server (pipenv)...
pushd backend
pipenv run python run.py
set "EXITCODE=!errorlevel!"
popd
goto :maybe_pause_and_exit

:venv_fallback
cd backend

echo Checking for virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing/updating dependencies...
pip install -r requirements.txt

echo Starting FastAPI server...
python run.py

:maybe_pause_and_exit
if not defined EXITCODE set "EXITCODE=!errorlevel!"
if "%NO_PAUSE%"=="0" (
    echo.
    echo Backend process exited with code !EXITCODE!.
    pause
)
exit /b !EXITCODE!


