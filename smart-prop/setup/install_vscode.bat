@echo off
cd /d "%~dp0"  :: Muda para o diretório onde o .bat está localizado

echo Downloading the Visual Studio Code installer...
powershell -Command "Invoke-WebRequest -Uri 'https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user' -OutFile 'vscode-installer.exe'"

echo Installing VS Code in silent mode...
vscode-installer.exe /VERYSILENT /NORESTART

echo Cleaning up the installer...
del vscode-installer.exe

echo Installation completed. VS Code is ready to use.
timeout /t 5
exit