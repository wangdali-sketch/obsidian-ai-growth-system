@echo off
setlocal enabledelayedexpansion

chcp 65001 >nul

set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

set "PYTHONDONTWRITEBYTECODE=1"
set "PYTHONUTF8=1"

if not exist "logs" (
    mkdir "logs"
)

for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set "TODAY=%%I"
set "LOG_FILE=%PROJECT_DIR%logs\%TODAY%.log"

(
    for /f "tokens=*" %%T in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-ddTHH:mm:ss"') do set "START_TIME=%%T"
    echo ========================================
    echo Start time: !START_TIME!
    echo Project directory: %PROJECT_DIR%
    echo Log file: %LOG_FILE%
    echo Security note: this script does not print .env content.

    if exist ".venv\Scripts\activate.bat" (
        echo Virtual environment found: .venv
        call ".venv\Scripts\activate.bat"
    ) else if exist "venv\Scripts\activate.bat" (
        echo Virtual environment found: venv
        call "venv\Scripts\activate.bat"
    ) else (
        echo No virtual environment found. Using system Python.
    )

    echo Running: python main.py
    python main.py
    set "EXIT_CODE=!ERRORLEVEL!"

    for /f "tokens=*" %%T in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-ddTHH:mm:ss"') do set "END_TIME=%%T"
    echo End time: !END_TIME!
    echo Exit code: !EXIT_CODE!
    echo.
) >> "%LOG_FILE%" 2>&1

exit /b %EXIT_CODE%
