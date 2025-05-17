@echo off
echo Twitter Profile Image Downloader
echo ===============================
echo.

rem Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

rem Check for required packages and install if missing
echo Checking required packages...
python -m pip install --upgrade pip
python -c "import pkg_resources; pkg_resources.require(['requests', 'Pillow'])" >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Installing required packages...
    python -m pip install requests Pillow
)

:menu
cls
echo Twitter Profile Image Downloader
echo ===============================
echo.
echo 1. Run with default settings
echo 2. Specify input file
echo 3. Exit
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    if not exist usernames.txt (
        echo Creating example usernames.txt file...
        echo @twitter > usernames.txt
        echo https://twitter.com/x >> usernames.txt
        echo elonmusk >> usernames.txt
    )
    echo.
    echo Using usernames.txt as input file and 'output' as output folder.
    python twitter_profile_downloader.py usernames.txt
    echo.
    echo Images saved to the 'output' folder.
    pause
    goto menu
)

if "%choice%"=="2" (
    echo.
    set /p input_file="Enter the path to your usernames file: "
    set /p output_folder="Enter the output folder name (or press Enter for default): "
    
    if "%output_folder%"=="" set output_folder=output
    
    echo.
    echo Processing images...
    python twitter_profile_downloader.py "%input_file%" --output "%output_folder%"
    echo.
    echo Images saved to the '%output_folder%' folder.
    pause
    goto menu
)

if "%choice%"=="3" (
    exit /b 0
)

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto menu
