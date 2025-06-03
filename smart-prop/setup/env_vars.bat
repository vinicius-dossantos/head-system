@echo off
echo Setting environment variables...

REM Define variáveis de ambiente permanentemente (requer permissões de administrador)
setx key 1747419014493122621 /M
setx user renan@mesasmartprop.com.br /M
setx password Mic@123456 /M
setx env prd /M
setx clientName smartprop /M
setx git_usrname "Vinicius Henrique dos Santos" /M
setx git_email "vinicius-dossantos@outlook.com" /M
setx git_key "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINcLhugNqm7wk7ultdzvDPhpbH/C8LQAvbBnVHkLprhm" /M


echo Variables created successfully.
timeout /t 2 >nul
exit