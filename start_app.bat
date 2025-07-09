@echo off
echo ========================================
echo    Failure Analysis Flask App
echo ========================================
echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting Flask application...
echo The web application will be available at: http://localhost:8080
echo Press Ctrl+C to stop the server
echo.
python app.py
pause 