@echo off
echo Downloading Python 3.10.11
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe' -OutFile $env:TEMP\python-installer.exe"

echo Installing Python 3.10.11
powershell -Command "Start-Process -FilePath $env:TEMP\python-installer.exe -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait"

echo Python has been installed successfully.
python --version

echo It is done
timeout /t 15 >nul
exit
