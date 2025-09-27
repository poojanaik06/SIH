@echo off
echo Testing crop viability validation through API...
echo.

echo === TEST 1: Antarctica + Wheat (Should FAIL) ===
curl -X POST "http://127.0.0.1:8000/predict/farmer-friendly" -H "Content-Type: application/json" -d "{\"location\": \"Antarctica\", \"crop_name\": \"Wheat\"}"
echo.
echo.

echo === TEST 2: India + Wheat (Should SUCCEED) ===
curl -X POST "http://127.0.0.1:8000/predict/farmer-friendly" -H "Content-Type: application/json" -d "{\"location\": \"India\", \"crop_name\": \"Wheat\"}"
echo.
echo.

echo === TEST 3: Sahara Desert + Rice (Should FAIL) ===
curl -X POST "http://127.0.0.1:8000/predict/farmer-friendly" -H "Content-Type: application/json" -d "{\"location\": \"Sahara Desert\", \"crop_name\": \"Rice\"}"
echo.
echo.

echo Validation tests complete!