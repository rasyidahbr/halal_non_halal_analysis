@echo off
echo Starting Halal Ingredient Analysis Application...
echo.
echo Checking Python environment...
python --version

echo.
echo Installing requirements...
pip install -r requirements.txt

echo.
echo Running application...
echo.
streamlit run app_improved.py

echo.
echo If the application didn't start automatically, please open your browser and go to:
echo http://localhost:8501
echo.