@echo off
setlocal

REM === CONFIG ===
set HADOOP_VERSION=3.3.1
set WINUTILS_URL=https://github.com/cdarlint/winutils/raw/master/hadoop-%HADOOP_VERSION%/bin/winutils.exe
set HADOOP_DIR=C:\hadoop
set BIN_DIR=%HADOOP_DIR%\bin

echo [1/4] Creating directory: %BIN_DIR%
mkdir "%BIN_DIR%" 2>nul

echo [2/4] Downloading winutils.exe for Hadoop %HADOOP_VERSION%...
powershell -Command "try { Invoke-WebRequest -Uri '%WINUTILS_URL%' -OutFile '%BIN_DIR%\winutils.exe' -ErrorAction Stop } catch { Write-Host '❌ Download failed:' $_.Exception.Message }"

if not exist "%BIN_DIR%\winutils.exe" (
    echo ❌ Failed to download winutils.exe. Aborting setup.
    echo 💡 Tip: Check your internet connection or try opening the link directly:
    echo %WINUTILS_URL%
    pause
    exit /b 1
)

echo [3/4] Setting environment variables...
setx HADOOP_HOME "%HADOOP_DIR%" /M
setx PATH "%PATH%;%BIN_DIR%" /M

echo [4/4] Setup completed successfully. ✔
echo 🔁 Please close and reopen your terminal for changes to take effect.
pause