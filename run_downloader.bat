@echo off
REM Twitter Profile Image Downloader - One Click Setup and Run
REM This script will install Python (if needed), required packages, and run the downloader.

REM 1. Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python not found. Downloading and installing Python 3.10...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe -OutFile python-installer.exe"
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    del python-installer.exe
    REM Refresh environment variables
    setx PATH "%PATH%;C:\\Program Files\\Python310;C:\\Program Files\\Python310\\Scripts"
    echo Python installed.
) else (
    echo Python found.
)

REM 2. Install required Python packages
python -m pip install --upgrade pip
python -m pip install playwright pillow requests

REM 3. Install Playwright browsers
python -m playwright install

REM 4. Run the main script
python download_twitter_profile_images.py

pause
