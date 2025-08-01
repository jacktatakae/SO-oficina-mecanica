@echo off
title VRS - Deploy GitHub Pages

echo 🚀 VRS - Deploy Automatico GitHub Pages
echo =======================================

REM Verificar se git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git nao encontrado. Instale git primeiro:
    echo    https://git-scm.com/downloads
    pause
    exit /b 1
)

REM Verificar se está em um repositório git
if not exist ".git" (
    echo 📁 Inicializando repositorio Git...
    git init
    
    echo 📝 Configurando Git ^(se necessario^)...
    set /p username=Digite seu nome de usuario GitHub: 
    set /p email=Digite seu email GitHub: 
    
    git config user.name "%username%"
    git config user.email "%email%"
    
    echo 🔗 Conecte este repositorio ao GitHub:
    echo    1. Va para https://github.com/new
    echo    2. Crie um repositorio publico chamado 'vrs-sistema'
    echo    3. NAO inicialize com README
    echo    4. Copie a URL do repositorio
    echo.
    set /p repo_url=Cole a URL do repositorio: 
    
    git remote add origin "%repo_url%"
)

REM Adicionar todos os arquivos
echo 📦 Adicionando arquivos ao Git...
git add .

REM Commit
echo 💾 Fazendo commit...
for /f "tokens=1-3 delims=/- " %%a in ('date /t') do set mydate=%%c-%%b-%%a
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set mytime=%%a:%%b
git commit -m "Deploy VRS Sistema - %mydate% %mytime%"

REM Push para GitHub
echo ⬆️ Enviando para GitHub...
git push -u origin main 2>nul || git push -u origin master

echo.
echo ✅ Deploy concluido!
echo.
echo 🌐 Proximos passos:
echo    1. Va para seu repositorio no GitHub
echo    2. Clique em 'Settings'
echo    3. Role ate 'Pages'
echo    4. Em 'Source', selecione 'Deploy from a branch'
echo    5. Escolha 'main' ^(ou 'master'^) e '/ ^(root^)'
echo    6. Clique 'Save'
echo.
echo ⏱️ Aguarde 5-10 minutos e seu VRS estara online!
echo 📱 Depois e so instalar como PWA no celular!
echo.
pause
