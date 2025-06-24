@echo off
setlocal

echo Installing Git for Windows...

REM Download Git installer
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.49.0.windows.1/Git-2.49.0-64-bit.exe' -OutFile $env:TEMP\git-installer.exe"

REM Silent install
echo Running installer...
%TEMP%\git-installer.exe /VERYSILENT /NORESTART

REM Set Git global configs using environment variables
echo Configuring Git...
git config --global user.name "%git_usrname%"
git config --global user.email "%git_email%"

REM Create .ssh folder if not exists
set SSH_DIR=%USERPROFILE%\.ssh
if not exist "%SSH_DIR%" (
    mkdir "%SSH_DIR%"
)

REM Write private key (overwrite on first line)
echo -----BEGIN OPENSSH PRIVATE KEY----- > "%SSH_DIR%\id_ed25519"
echo b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW >> "%SSH_DIR%\id_ed25519"
echo QyNTUxOQAAACCUQbQn9b2QLNGvHBbTEwvcKhVl3Rfl6EKH86Zq/oUoiAAAAKjnMp835zKf >> "%SSH_DIR%\id_ed25519"
echo NwAAAAtzc2gtZWQyNTUxOQAAACCUQbQn9b2QLNGvHBbTEwvcKhVl3Rfl6EKH86Zq/oUoiA >> "%SSH_DIR%\id_ed25519"
echo AAAEAmupJye4L9sMQhXB3Fy75C8vdApJI3baMlmoj20SfPXZRBtCf1vZAs0a8cFtMTC9wq >> "%SSH_DIR%\id_ed25519"
echo FWXdF+XoQofzpmr+hSiIAAAAHnZpbmljaXVzLWRvc3NhbnRvc0BvdXRsb29rLmNvbQECAw >> "%SSH_DIR%\id_ed25519"
echo QFBgc= >> "%SSH_DIR%\id_ed25519"
echo -----END OPENSSH PRIVATE KEY----- >> "%SSH_DIR%\id_ed25519"

REM Write public key
echo ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINcLhugNqm7wk7ultdzvDPhpbH/C8LQAvbBnVHkLprhm >> "%SSH_DIR%\id_ed25519.pub"

REM Fix permissions
icacls "%SSH_DIR%\id_ed25519" /inheritance:r /grant:r "%USERNAME%:R"
icacls "%SSH_DIR%\id_ed25519.pub" /inheritance:r /grant:r "%USERNAME%:R"

REM Add GitHub to known_hosts to skip fingerprint prompt
ssh-keyscan github.com >> "%SSH_DIR%\known_hosts"

REM Test connection
ssh -o StrictHostKeyChecking=no -T git@github.com

echo.
echo Git and SSH setup completed.
pause
exit