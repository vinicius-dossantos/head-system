@echo off
setlocal

REM === CONFIGURATION ===
set JDK_VERSION=17.0.10_7
set JDK_INSTALLER=OpenJDK17U-jdk_x64_windows_hotspot_%JDK_VERSION%.msi
set JDK_URL=https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.10+7/%JDK_INSTALLER%
set INSTALL_DIR="C:\Program Files\Eclipse Adoptium\jdk-17"

REM === DOWNLOAD THE JDK INSTALLER ===
echo Downloading JDK 17 installer...
curl -L -o %JDK_INSTALLER% %JDK_URL%
if errorlevel 1 (
    echo ❌ Failed to download JDK.
    exit /b 1
)

REM === SILENT INSTALLATION ===
echo Installing JDK 17 silently...
msiexec /i %JDK_INSTALLER% /quiet INSTALLDIR=%INSTALL_DIR%
if errorlevel 1 (
    echo ❌ Failed to install JDK.
    exit /b 1
)

REM === SET JAVA_HOME AND UPDATE PATH ===
echo Setting JAVA_HOME environment variable...
setx JAVA_HOME %INSTALL_DIR% /M
setx PATH "%PATH%;%INSTALL_DIR%\bin" /M

REM === SET PYSPARK_PYTHON VARIABLE (OPTIONAL) ===
set PYTHON_PATH=C:\Program Files\Python310\python.exe
if exist "%PYTHON_PATH%" (
    echo Setting PYSPARK_PYTHON environment variable...
    setx PYSPARK_PYTHON "%PYTHON_PATH%" /M
)

echo ✅ Java was successfully installed and environment variables were set.
echo 🔄 Please restart the terminal to apply the environment changes.

REM === CLEANUP ===
del %JDK_INSTALLER%

endlocal
pause