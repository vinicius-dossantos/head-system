@echo off
echo Setting environment variables...

REM === Variáveis específicas da aplicação ===
setx key 1747419014493122621 /M
setx user renan@mesasmartprop.com.br /M
setx password Mic@123456 /M
setx accountId 1358568 /M
setx brokerId 513 /M

REM === Securely set system-wide environment variables ===
setx key 1747419014493122621 /M
setx user renan@mesasmartprop.com.br /M
setx password Mic@123456 /M
setx env prd /M
setx clientName smartprop /M
setx git_usrname "Vinicius Henrique dos Santos" /M
setx git_email "vinicius-dossantos@outlook.com" /M
setx git_key "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINcLhugNqm7wk7ultdzvDPhpbH/C8LQAvbBnVHkLprhm" /M
setx JAVA_HOME "C:\Program Files\Eclipse Adoptium\jdk-17" /M
setx HADOOP_HOME "C:\hadoop" /M

REM === Safely add Java and Hadoop to PATH via registry ===
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH /t REG_EXPAND_SZ /d "%PATH%;C:\Program Files\Eclipse Adoptium\jdk-17\bin;C:\hadoop\bin" /f

echo ✅ Environment variables set successfully.
timeout /t 2 >nul
exit