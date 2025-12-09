@echo off
echo Starting Price Tracker Frontend...
cd frontend

echo Checking for node_modules...
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
)

echo Starting development server...
npm run dev


