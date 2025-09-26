@echo off
echo ===================================================
echo       SIH CROP YIELD PREDICTION SYSTEM
echo ===================================================
echo.

echo Starting complete application stack...
echo.

echo [1/2] Starting Backend Server...
start \"SIH Backend\" cmd /k \"cd /d c:\\Users\\Sahana Madival\\OneDrive\\Desktop\\SIH\\backend && pip install -r requirements.txt > nul 2>&1 && uvicorn app.main:app --host localhost --port 8000 --reload\"

echo Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

echo [2/2] Starting Frontend Server...
start \"SIH Frontend\" cmd /k \"cd /d c:\\Users\\Sahana Madival\\OneDrive\\Desktop\\SIH\\frontend && npm install > nul 2>&1 && npm run dev\"

echo.
echo ✅ Application is starting up!
echo.
echo 🔗 Backend API: http://localhost:8000
echo 🌐 Frontend App: http://localhost:5173
echo 📖 API Docs: http://localhost:8000/docs
echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.
echo.
pause