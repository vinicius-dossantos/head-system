@echo off
echo Installing Git for Windows...

REM Download Git installer
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.49.0.windows.1/Git-2.49.0-64-bit.exe' -OutFile $env:TEMP\git-installer.exe"

REM Silent install
echo Running installer...
%TEMP%\git-installer.exe /VERYSILENT /NORESTART

REM Set Git global configs using environment variables
echo Configuring Git with environment variables...
git config --global user.name "%git_usrname%"
git config --global user.email "%git_email%"

REM Generate SSH key (optional)
echo Generating SSH key (if not exists)...
IF NOT EXIST "%USERPROFILE%\.ssh\id_ed25519" (
    ssh-keygen -t ed25519 -C "%git_email%" -f %USERPROFILE%\.ssh\id_ed25519 -N ""
)

REM Display public key to add on GitHub
echo Public key generated:
type %USERPROFILE%\.ssh\id_ed25519.pub

echo.
echo === NEXT STEP ===
echo 1. Copy the public key above.
echo 2. Go to https://github.com/settings/ssh/new and add the key.
echo 3. Then run the command below to test:
echo     ssh -T git@github.com
echo.
pause
exit