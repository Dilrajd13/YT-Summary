@echo off
rem Double-click this file to start YT-Summary in your browser.
rem The first run sets everything up (a few minutes); after that it starts in seconds.
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo First run: setting up YT-Summary. This downloads a few hundred MB and can take a few minutes...
    py -3 -m venv .venv 2>nul || python -m venv .venv
    if not exist ".venv\Scripts\python.exe" (
        echo Could not find Python. Install it from https://www.python.org/downloads/ and run this again.
        pause
        exit /b 1
    )
    .venv\Scripts\python.exe -m pip install --upgrade pip
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Installing packages failed. Scroll up to see the error.
        pause
        exit /b 1
    )
)

if not exist ".env" copy ".env.example" ".env" >nul

rem YouTube changes often, so keep the downloader current
echo Checking for downloader updates...
.venv\Scripts\python.exe -m pip install --upgrade --quiet "yt-dlp[default]"

.venv\Scripts\python.exe src\app.py
pause
