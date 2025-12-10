@echo off
echo =============================================
echo  Price Tracker - Data Cleanup Utility
echo =============================================
echo.

cd ..
cd backend

echo Activating virtual environment...
call venv\Scripts\activate

echo.
python clean_price_data.py

echo.
pause

