@echo off
REM Windows Startup Script for Employee Performance Evaluation System

echo ========================================
echo Starting Health Check...
echo ========================================
python health_check.py

if %errorlevel% neq 0 (
    echo.
    echo Health check failed. Fix issues and try again.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Launching Streamlit Application...
echo ========================================
streamlit run main.py

pause
