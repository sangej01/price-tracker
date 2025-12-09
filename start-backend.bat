@echo off
echo Starting Price Tracker Backend...
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
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


