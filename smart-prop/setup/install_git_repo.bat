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

REM Inject known private key
echo Writing SSH private key...
(
echo -----BEGIN OPENSSH PRIVATE KEY-----
echo ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINcLhugNqm7wk7ultdzvDPhpbH/C8LQAvbBnVHkLprhm
echo -----END OPENSSH PRIVATE KEY-----
) > "%SSH_DIR%\id_ed25519"

REM Inject public key
echo Writing SSH public key...
echo ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINcLhugNqm7wk7ultdzvDPhpbH/C8LQAvbBnVHkLprhm >> "%SSH_DIR%\id_ed25519.pub"

REM Set correct permissions
echo Fixing SSH permissions...
icacls "%SSH_DIR%\id_ed25519" /inheritance:r /grant:r "%USERNAME%:R"
icacls "%SSH_DIR%\id_ed25519.pub" /inheritance:r /grant:r "%USERNAME%:R"

REM Test connection
echo Testing SSH connection with GitHub...
ssh -T git@github.com

echo.
echo Git and SSH setup completed.
pause
exit