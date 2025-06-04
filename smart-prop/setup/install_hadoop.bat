@echo off
setlocal

set HADOOP_VERSION=3.3.1
set HADOOP_URL=https://github.com/kontext-tech/winutils/releases/download/v%HADOOP_VERSION%/hadoop-%HADOOP_VERSION%.zip
set HADOOP_ZIP=%TEMP%\hadoop-%HADOOP_VERSION%.zip
set HADOOP_DIR=C:\hadoop

echo [1/5] Baixando Hadoop %HADOOP_VERSION%...
certutil -urlcache -split -f "%HADOOP_URL%" "%HADOOP_ZIP%" >nul
if not exist "%HADOOP_ZIP%" (
    echo ❌ Falha ao baixar Hadoop ZIP. Abortando.
    pause
    exit /b 1
)

echo [2/5] Criando diretório: %HADOOP_DIR%
mkdir "%HADOOP_DIR%" 2>nul

echo [3/5] Extraindo para: %HADOOP_DIR%
tar -xf "%HADOOP_ZIP%" -C "%HADOOP_DIR%"
if exist "%HADOOP_DIR%\hadoop-%HADOOP_VERSION%" (
    move "%HADOOP_DIR%\hadoop-%HADOOP_VERSION%\*" "%HADOOP_DIR%\" >nul
    rmdir /s /q "%HADOOP_DIR%\hadoop-%HADOOP_VERSION%"
)

echo [4/5] Configurando variáveis de ambiente...
setx HADOOP_HOME "%HADOOP_DIR%" /M
echo %PATH% | find /I "%HADOOP_DIR%\bin" >nul || setx PATH "%PATH%;%HADOOP_DIR%\bin" /M

echo [5/5] Finalizado com sucesso. ✔
echo 🔁 Feche e reabra o terminal para aplicar as variáveis.
pause
exit /b 0