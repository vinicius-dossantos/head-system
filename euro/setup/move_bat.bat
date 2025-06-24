@echo off
echo Copying .bat files from shared folder to Documents...

xcopy "\\tsclient\smart-prop\setup\*.bat" "C:\Users\Administrator\Documents\setup" /Y /I

echo Done.
timeout /t 3
exit