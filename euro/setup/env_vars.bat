@echo off
echo Setting environment variables...

REM === Variáveis específicas da aplicação ===
setx key 14718386451779203944 /M
setx user 18638492000100 /M
setx password EuroDLL@2025 /M
setx accountId 102383173 /M
setx brokerId 513 /M

REM === Securely set system-wide environment variables ===
setx key 1747419014493122621 /M
setx user 18638492000100 /M
setx password EuroDLL@2025 /M
setx env prd /M
setx clientName euro /M
setx git_usrname "Vinicius Henrique dos Santos" /M
setx git_email "vinicius-dossantos@outlook.com" /M
setx git_key "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINcLhugNqm7wk7ultdzvDPhpbH/C8LQAvbBnVHkLprhm" /M
setx JAVA_HOME "C:\Program Files\Eclipse Adoptium\jdk-17" /M

echo ✅ Environment variables set successfully.
timeout /t 2 >nul
exit