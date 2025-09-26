@echo off
echo Starting SIH Crop Yield Prediction Backend...
echo.

cd /d \"c:\\Users\\Sahana Madival\\OneDrive\\Desktop\\SIH\\backend\"

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Starting FastAPI server...
uvicorn app.main:app --host localhost --port 8000 --reload

pause