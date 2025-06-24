@echo off
setlocal

set "TARGET_DIR=C:\headsystem"
set "GIT_REPO=git@github.com:vinicius-dossantos/head-system.git"

REM Check if the folder already exists
if exist "%TARGET_DIR%" (
    echo The folder "%TARGET_DIR%" already exists.
) else (
    echo Creating the folder "%TARGET_DIR%"...
    mkdir "%TARGET_DIR%"
)

REM Navigate to the folder
cd /d "%TARGET_DIR%"

REM Clone the repository (only if not already cloned)
if exist "%TARGET_DIR%\head-system" (
    echo The repository has already been cloned.
) else (
    echo Cloning the repository %GIT_REPO% ...
    git clone %GIT_REPO%
)

echo.
echo Operation completed.
timeout /t 5 >nul
exit