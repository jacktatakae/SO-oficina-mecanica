@echo off
title VRS - Deploy Manual GitHub Pages
cls

echo.
echo =========================================
echo   🚀 VRS - HOSPEDAGEM ONLINE MANUAL
echo =========================================
echo.
echo Como o Git nao esta instalado, vamos usar
echo o metodo manual mais simples!
echo.

:MENU
echo ESCOLHA O METODO DE HOSPEDAGEM:
echo.
echo [1] GitHub Pages - Drag & Drop (FACIL)
echo [2] Netlify - Arrastar pasta (MAIS FACIL)
echo [3] Servidor local temporario
echo [4] Instrucoes detalhadas
echo [0] Sair
echo.
set /p opcao="Digite o numero da opcao: "

if "%opcao%"=="1" goto GITHUB_MANUAL
if "%opcao%"=="2" goto NETLIFY
if "%opcao%"=="3" goto LOCAL_SERVER
if "%opcao%"=="4" goto INSTRUCTIONS
if "%opcao%"=="0" goto EXIT
goto MENU

:GITHUB_MANUAL
echo.
echo ========================================
echo   📁 GITHUB PAGES - UPLOAD MANUAL
echo ========================================
echo.
echo PASSO A PASSO COMPLETO:
echo.
echo 1. 🌐 CRIAR CONTA/LOGIN:
echo    - Acesse: https://github.com
echo    - Faca login ou criar conta gratuita
echo.
echo 2. ➕ CRIAR REPOSITORIO:
echo    - Clique no botao verde "New"
echo    - Nome do repositorio: vrs-inventario
echo    - Marque "Public"
echo    - NAO marque "Initialize with README"
echo    - Clique "Create repository"
echo.
echo 3. 📤 UPLOAD DOS ARQUIVOS:
echo    - Na pagina do repositorio vazio
echo    - Clique em "uploading an existing file"
echo    - Arraste TODA a pasta VRS
echo    - Ou selecione todos os arquivos
echo    - Commit message: "Deploy VRS Sistema"
echo    - Clique "Commit changes"
echo.
echo 4. ⚙️ ATIVAR GITHUB PAGES:
echo    - Va em "Settings" (no repositorio)
echo    - Role ate secao "Pages"
echo    - Em "Source": Deploy from a branch
echo    - Branch: main
echo    - Folder: / (root)
echo    - Clique "Save"
echo.
echo 5. ✅ RESULTADO:
echo    - Aguarde 5-10 minutos
echo    - URL sera: https://seuusuario.github.io/vrs-inventario
echo    - Acesse pelo celular e instale como PWA
echo.
echo 🔗 ABRIR GITHUB AGORA?
set /p github="Pressione ENTER para abrir GitHub: "
start https://github.com
echo.
echo ✅ GitHub aberto! Siga os passos acima.
echo.
pause
goto MENU

:NETLIFY
echo.
echo ========================================
echo   🚀 NETLIFY - DRAG & DROP
echo ========================================
echo.
echo METODO MAIS SIMPLES DE TODOS:
echo.
echo 1. 🌐 ACESSE NETLIFY:
echo    - Site: https://netlify.com
echo    - Nao precisa criar conta inicialmente
echo.
echo 2. 📁 PREPARE A PASTA:
echo    - Selecione TODOS os arquivos VRS
echo    - Ou comprima em um arquivo ZIP
echo.
echo 3. ⬆️ ARRASTAR E SOLTAR:
echo    - Na pagina principal do Netlify
echo    - Procure area "Drag and drop your site output folder here"
echo    - Arraste a pasta VRS ou ZIP
echo    - Upload automatico!
echo.
echo 4. ✅ PRONTO!:
echo    - Netlify gera URL automaticamente
echo    - Exemplo: https://random-name-123.netlify.app
echo    - Pode personalizar nome depois
echo.
echo 5. 📱 NO CELULAR:
echo    - Acesse a URL gerada
echo    - Instale como PWA
echo    - Nunca mais erro de arquivo!
echo.
echo 🔗 ABRIR NETLIFY AGORA?
set /p netlify="Pressione ENTER para abrir Netlify: "
start https://netlify.com
echo.
echo ✅ Netlify aberto! Arraste a pasta VRS.
echo.
pause
goto MENU

:LOCAL_SERVER
echo.
echo ========================================
echo   🖥️ SERVIDOR LOCAL TEMPORARIO
echo ========================================
echo.
echo Para usar AGORA sem hospedagem online:
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nao encontrado.
    echo.
    echo INSTALAR PYTHON:
    echo 1. Acesse: https://python.org/downloads
    echo 2. Baixe Python 3.x
    echo 3. Marque "Add to PATH" na instalacao
    echo 4. Execute este script novamente
    echo.
    set /p python="Pressione ENTER para abrir site do Python: "
    start https://python.org/downloads
    pause
    goto MENU
)

echo ✅ Python encontrado! Iniciando servidor...
echo.
echo 🌐 SEU VRS ESTARA DISPONIVEL EM:
echo.

REM Descobrir IP
echo 📍 ENDERECOS DISPONIVEIS:
ipconfig | findstr /i "IPv4"

echo.
echo 💡 COMO USAR:
echo 1. Anote um dos IPs acima (ex: 192.168.1.105)
echo 2. No celular, acesse: http://IP:8080
echo 3. Exemplo: http://192.168.1.105:8080
echo 4. Instale como PWA se quiser
echo.
echo ⚠️ IMPORTANTE:
echo - Celular deve estar na MESMA rede WiFi
echo - Deixe esta janela aberta
echo - Para parar: Ctrl+C
echo.
echo 🚀 INICIANDO SERVIDOR...
echo.

python -m http.server 8080

pause
goto MENU

:INSTRUCTIONS
echo.
echo ========================================
echo   📖 INSTRUCOES DETALHADAS
echo ========================================
echo.
echo QUAL METODO ESCOLHER?
echo.
echo 🥇 NETLIFY ^(MAIS FACIL^):
echo    ✅ Sem cadastro inicial
echo    ✅ Arrastar e soltar
echo    ✅ URL instantanea
echo    ✅ Sem configuracao
echo.
echo 🥈 GITHUB PAGES ^(MAIS PROFISSIONAL^):
echo    ✅ Gratuito para sempre
echo    ✅ URL personalizada
echo    ✅ Controle de versao
echo    ✅ Facil atualizacao
echo.
echo 🥉 SERVIDOR LOCAL ^(TEMPORARIO^):
echo    ✅ Funciona imediatamente
echo    ✅ Nao precisa upload
echo    ❌ So funciona com PC ligado
echo    ❌ Mesma rede WiFi apenas
echo.
echo 💡 RECOMENDACAO:
echo    1. Use Netlify para testar rapidamente
echo    2. Migre para GitHub Pages depois
echo    3. Servidor local so para emergencia
echo.
echo 🎯 OBJETIVO FINAL:
echo    - VRS funcionando online
echo    - Acesso de qualquer dispositivo
echo    - Instalacao PWA no celular
echo    - Sem erro ERR_FILE_NOT_FOUND
echo.
pause
goto MENU

:EXIT
echo.
echo ========================================
echo   ✅ HOSPEDAGEM CONFIGURADA
echo ========================================
echo.
echo PROXIMOS PASSOS:
echo.
echo 📱 NO CELULAR:
echo    1. Acesse a URL da hospedagem
echo    2. Menu → "Instalar app"
echo    3. Use como app nativo
echo.
echo 🔄 PARA ATUALIZAR:
echo    - Netlify: Arrastar pasta atualizada
echo    - GitHub: Upload novos arquivos
echo    - Local: Reiniciar servidor
echo.
echo 🎉 PROBLEMA RESOLVIDO!
echo    Nunca mais erro ERR_FILE_NOT_FOUND
echo.
pause
exit

echo ❌ Opcao invalida! Tente novamente.
pause
goto MENU
