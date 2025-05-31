@echo off
echo ==========================================
echo    Bangalore Job Search Tool
echo ==========================================
echo.
echo Starting job search for Frontend/React/Full-stack positions...
echo Location: Bangalore
echo Experience: 2-5 years
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again.
    pause
    exit /b 1
)

echo Python detected. Running job search...
echo.

REM Run the Python job search script
python job_search.py

echo.
echo ==========================================
echo Job search completed!
echo Check the generated CSV file for results.
echo ==========================================
echo.
pause
