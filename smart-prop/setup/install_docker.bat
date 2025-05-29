@echo off
echo Downloading Docker Desktop installer...

powershell -Command "Invoke-WebRequest -Uri https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe -OutFile %TEMP%\DockerInstaller.exe"

echo Installing Docker Desktop silently...
%TEMP%\DockerInstaller.exe install --quiet

echo Installation started. Docker may request a restart.
timeout /t 10 >nul

echo Enabling WSL2 (required for Docker Desktop)...
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

echo Downloading WSL2 kernel update...
powershell -Command "Invoke-WebRequest -Uri https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi -OutFile %TEMP%\wsl_update_x64.msi"
msiexec /i %TEMP%\wsl_update_x64.msi /quiet

echo It is strongly recommended to manually restart the computer after installation.

timeout /t 15 >nul
exit