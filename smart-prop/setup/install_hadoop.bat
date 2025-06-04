@echo off
setlocal

REM === CONFIG ===
set HADOOP_VERSION=3.3.1
set HADOOP_DIR=C:\hadoop
set BIN_DIR=%HADOOP_DIR%\bin
set WINUTILS_URL=https://github.com/kontext-tech/winutils/raw/master/hadoop-%HADOOP_VERSION%/bin/winutils.exe

echo [1/4] Creating folder: %BIN_DIR%
mkdir "%BIN_DIR%" 2>nul

echo [2/4] Downloading winutils.exe from Kontext GitHub repo...
powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; try { Invoke-WebRequest -Uri '%WINUTILS_URL%' -OutFile '%BIN_DIR%\winutils.exe' -ErrorAction Stop } catch { Write-Host '❌ Download failed:' $_.Exception.Message }"

if not exist "%BIN_DIR%\winutils.exe" (
    echo ❌ Failed to download winutils.exe. Aborting setup.
    echo 🔗 Check manually: %WINUTILS_URL%
    pause
    exit /b 1
)

echo [3/4] Setting environment variables...
setx HADOOP_HOME "%HADOOP_DIR%" /M
setx PATH "%PATH%;%BIN_DIR%" /M

echo [4/4] Setup completed successfully. ✔
echo 🔁 Please close and reopen your terminal for the new variables to take effect.
pause