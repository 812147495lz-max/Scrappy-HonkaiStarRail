@echo off
setlocal

REM Set strict error handling
set "EXIT_ON_ERROR=0"

echo ==========================================
echo        [Scrappy-HSR] Auto Sync Script
echo ==========================================

REM --- Step 1: Save local changes ---
echo.
echo [1/3] Saving local changes...
git add .
set /p msg="Enter commit message (Press Enter for 'Update'): "
if "%msg%"=="" set msg="Update"
git commit -m "%msg%"

echo.
echo ------------------------------------------
echo [Info] Ready to PULL from remote.
echo If it crashes here, check git config.
pause
echo ------------------------------------------

REM --- Step 2: Pull from remote ---
echo.
echo [2/3] Pulling from GitHub...
git pull origin main

if %errorlevel% neq 0 (
    color 0c
    echo.
    echo ==========================================
    echo [ERROR] Pull failed! Conflict detected.
    echo Please fix conflicts manually in files.
    echo ==========================================
    pause
    goto :EOF
)

echo.
echo [Success] Pull completed.
echo ------------------------------------------

REM --- Step 3: Push to remote ---
echo.
echo [3/3] Pushing to GitHub...
git push origin main

if %errorlevel% neq 0 (
    color 0c
    echo.
    echo [ERROR] Push failed! Check network.
    pause
    goto :EOF
)

echo.
echo -------------------------------
echo [Scrappy-HSR] All Done! Success!
pause