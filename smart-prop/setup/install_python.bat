@echo off
echo Downloading Python 3.10.11...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe' -OutFile $env:TEMP\python-installer.exe"

echo Installing Python 3.10.11 silently...
powershell -Command "Start-Process -FilePath $env:TEMP\python-installer.exe -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1 Include_pip=1' -Wait"

echo Verifying Python installation...
python --version

echo Verifying pip installation...
pip --version
if errorlevel 1 (
    echo Pip not found. Installing pip manually...
    python -m ensurepip --upgrade
    python -m pip install --upgrade pip
)

echo Installation completed.
timeout /t 15 >nul
exit