@echo off
setlocal

set "SCRIPTS_DIR=C:\scripts"

echo Running scripts from %SCRIPTS_DIR% in sequence...
echo.

REM Step 1: env_vars.bat
echo [1/4] Running env_vars.bat...
call "%SCRIPTS_DIR%\env_vars.bat"

REM Step 2: install_git_repo.bat
echo [2/4] Running install_git_repo.bat...
call "%SCRIPTS_DIR%\install_git_repo.bat"

REM Step 3: install_python.bat
echo [3/4] Running install_python.bat...
call "%SCRIPTS_DIR%\install_python.bat"

REM Step 4: install_vscode.bat
echo [4/4] Running install_vscode.bat...
call "%SCRIPTS_DIR%\install_vscode.bat"

echo.
echo ✅ All scripts executed successfully.
pause
exit