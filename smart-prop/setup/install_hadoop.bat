@echo off
setlocal

REM === CONFIG ===
set HADOOP_VERSION=3.3.1
set HADOOP_URL=https://github.com/kontext-tech/winutils/releases/download/v%HADOOP_VERSION%/hadoop-%HADOOP_VERSION%.zip
set HADOOP_ZIP=%TEMP%\hadoop-%HADOOP_VERSION%.zip
set HADOOP_DIR=C:\hadoop

echo [1/5] Downloading Hadoop %HADOOP_VERSION% for Windows...
curl -L -o "%HADOOP_ZIP%" "%HADOOP_URL%"
if not exist "%HADOOP_ZIP%" (
    echo ❌ Failed to download Hadoop ZIP. Aborting.
    echo 🔗 Check manually: %HADOOP_URL%
    pause
    exit /b 1
)

echo [2/5] Creating directory %HADOOP_DIR%...
mkdir "%HADOOP_DIR%" 2>nul

echo [3/5] Extracting ZIP to %HADOOP_DIR%...
powershell -Command "Expand-Archive -Path '%HADOOP_ZIP%' -DestinationPath '%HADOOP_DIR%' -Force"

REM === Ajusta estrutura para evitar pasta aninhada ===
if exist "%HADOOP_DIR%\hadoop-%HADOOP_VERSION%" (
    move "%HADOOP_DIR%\hadoop-%HADOOP_VERSION%\*" "%HADOOP_DIR%\" >nul
    rmdir /s /q "%HADOOP_DIR%\hadoop-%HADOOP_VERSION%"
)

echo [4/5] Setting environment variables...
setx HADOOP_HOME "%HADOOP_DIR%" /M
REM Adiciona ao PATH apenas se ainda não estiver presente
echo %PATH% | find /I "%HADOOP_DIR%\bin" >nul || setx PATH "%PATH%;%HADOOP_DIR%\bin" /M

echo [5/5] Setup completed successfully. ✔
echo 🔁 Please close and reopen o terminal ou VS Code para aplicar as mudanças.
pause
exit /b 0