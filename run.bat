@echo off
cd /d "C:\Users\zigza\Desktop\Coding Projects\Kadence"
echo Moving to Kadence project directory...
echo Current location: %CD%

if not exist "venv" (
    echo Virtual environment not found! Please set up the project first.
    pause
    exit /b 1
)

echo Activating virtual environment...
call .\venv\Scripts\activate

echo Starting Streamlit application...
streamlit run app.py

pause 