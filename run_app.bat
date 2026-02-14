@echo off
echo Activating virtual environment...
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo Virtual environment not found in .venv. Using system Python...
)

echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Setting PYTHONPATH...
set PYTHONPATH=%CD%\src;%PYTHONPATH%
echo Starting CodeAlign...
:: Use python from venv directly or active environment
python -m streamlit run src/codealign/ui_app.py --browser.gatherUsageStats=false
pause
