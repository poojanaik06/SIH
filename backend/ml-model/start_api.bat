@echo off
echo 🌾===============================================🌾
echo    FAST CROP YIELD PREDICTION API LAUNCHER
echo 🌾===============================================🌾
echo.

echo 🔍 Checking Python environment...
python --version
if %ERRORLEVEL% neq 0 (
    echo ❌ Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

echo.
echo 📦 Installing/updating dependencies...
pip install -r deployment\requirements.txt
if %ERRORLEVEL% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo 🚀 Starting Fast Prediction API...
echo 📖 Interactive docs will be available at: http://localhost:8000/docs
echo 🌐 API endpoint: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

cd deployment
python fast_prediction_api.py

pause