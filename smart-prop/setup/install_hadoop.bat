@echo off
SETLOCAL ENABLEEXTENSIONS

REM === Configuration ===
set "HADOOP_VERSION=3.3.1"
set "HADOOP_HOME=C:\hadoop"  REM Target install directory
set "HADOOP_TGZ_URL=https://archive.apache.org/dist/hadoop/common/hadoop-%HADOOP_VERSION%/hadoop-%HADOOP_VERSION%.tar.gz"
set "WINUTILS_REPO_URL=https://raw.githubusercontent.com/kontext-tech/winutils/master/hadoop-%HADOOP_VERSION%/bin"

REM === Download Hadoop tarball ===
echo Downloading Hadoop %HADOOP_VERSION% core package...
set "TMP_TGZ=%TEMP%\hadoop-%HADOOP_VERSION%.tar.gz"
powershell -Command "Invoke-WebRequest -Uri '%HADOOP_TGZ_URL%' -OutFile '%TMP_TGZ%'" 
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to download Hadoop %HADOOP_VERSION% tarball. >&2
    EXIT /B 1
)

REM === Extract Hadoop to C:\hadoop ===
echo Extracting Hadoop package to %HADOOP_HOME%...
mkdir "%HADOOP_HOME%" >NUL 2>&1
REM Use Windows tar to extract and strip the top-level folder:
tar -xzf "%TMP_TGZ%" -C "%HADOOP_HOME%" --strip-components=1 
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Extraction failed (archive may be corrupted or tar not available). >&2
    EXIT /B 1
)

REM === Download winutils.exe and Hadoop DLL ===
echo Downloading Windows native binaries (winutils.exe, hadoop.dll)...
powershell -Command "Invoke-WebRequest -Uri '%WINUTILS_REPO_URL%/winutils.exe' -OutFile '%HADOOP_HOME%\bin\winutils.exe'"
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to download winutils.exe. >&2
    EXIT /B 1
)
powershell -Command "Invoke-WebRequest -Uri '%WINUTILS_REPO_URL%/hadoop.dll' -OutFile '%HADOOP_HOME%\bin\hadoop.dll'"
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to download hadoop.dll. >&2
    EXIT /B 1
)

REM (Optionally, you could verify the files exist)
IF NOT EXIST "%HADOOP_HOME%\bin\winutils.exe" (
    echo ERROR: winutils.exe not found in %HADOOP_HOME%\bin. >&2
    EXIT /B 1
)
IF NOT EXIST "%HADOOP_HOME%\bin\hadoop.dll" (
    echo ERROR: hadoop.dll not found in %HADOOP_HOME%\bin. >&2
    EXIT /B 1
)

REM === Set environment variables (HADOOP_HOME and PATH) ===
echo Configuring HADOOP_HOME and PATH environment variables...
REM Set HADOOP_HOME system-wide
setx /M HADOOP_HOME "%HADOOP_HOME%" >NUL
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to set HADOOP_HOME environment variable (check permissions). >&2
    REM Not fatal? Choose to exit or not. We exit:
    EXIT /B 1
)
REM Append Hadoop \bin to system PATH
set "NewPath=%PATH%;%HADOOP_HOME%\bin"
setx /M PATH "%NewPath%" >NUL
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to update PATH (it may be too long or permission denied). >&2
    EXIT /B 1
)

echo.
echo Hadoop %HADOOP_VERSION% installed to %HADOOP_HOME%. Environment variables set.
echo Please restart your terminal or log off and on for changes to take effect.
ENDLOCAL