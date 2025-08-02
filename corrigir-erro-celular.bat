@echo off
echo.
echo ========================================
echo   🚨 CORREÇÃO ERR_FILE_NOT_FOUND
echo ========================================
echo.
echo Este script resolve o erro de navegação
echo entre páginas no celular.
echo.
echo PROBLEMA: "Não foi possível acessar arquivo"
echo CAUSA: Protocolo file:// bloqueado no mobile
echo SOLUÇÃO: Servidor web local
echo.
echo ========================================
echo.

:MENU
echo ESCOLHA UMA OPÇÃO:
echo.
echo [1] Iniciar servidor Python (Recomendado)
echo [2] Iniciar servidor Node.js
echo [3] Abrir página de correção
echo [4] Descobrir IP do computador
echo [5] Instruções para celular
echo [6] Deploy online (GitHub Pages)
echo [0] Sair
echo.
set /p opcao="Digite o número da opção: "

if "%opcao%"=="1" goto PYTHON_SERVER
if "%opcao%"=="2" goto NODE_SERVER
if "%opcao%"=="3" goto OPEN_CORRECTION
if "%opcao%"=="4" goto SHOW_IP
if "%opcao%"=="5" goto MOBILE_INSTRUCTIONS
if "%opcao%"=="6" goto GITHUB_DEPLOY
if "%opcao%"=="0" goto EXIT
goto MENU

:PYTHON_SERVER
echo.
echo ========================================
echo   🐍 INICIANDO SERVIDOR PYTHON
echo ========================================
echo.
echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo.
    echo INSTALE PYTHON:
    echo 1. Acesse: https://python.org/downloads
    echo 2. Baixe Python 3.x
    echo 3. Marque "Add to PATH" na instalação
    echo 4. Execute este script novamente
    echo.
    pause
    goto MENU
)

echo ✅ Python encontrado!
echo.
echo 🌐 Iniciando servidor na porta 8080...
echo.
echo ⚠️  IMPORTANTE:
echo 1. Deixe esta janela ABERTA
echo 2. No celular, use: http://SEU-IP:8080
echo 3. Para descobrir seu IP, abra outra janela e execute opção 4
echo.
echo 🛑 Para parar: Pressione Ctrl+C
echo.
python -m http.server 8080
pause
goto MENU

:NODE_SERVER
echo.
echo ========================================
echo   📦 INICIANDO SERVIDOR NODE.JS
echo ========================================
echo.
echo Verificando Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js não encontrado!
    echo.
    echo INSTALE NODE.JS:
    echo 1. Acesse: https://nodejs.org
    echo 2. Baixe versão LTS
    echo 3. Execute este script novamente
    echo.
    pause
    goto MENU
)

echo ✅ Node.js encontrado!
echo.
echo 📦 Instalando http-server...
npm install -g http-server
echo.
echo 🌐 Iniciando servidor na porta 8080...
echo.
echo ⚠️  IMPORTANTE:
echo 1. Deixe esta janela ABERTA
echo 2. No celular, use: http://SEU-IP:8080
echo 3. Para descobrir seu IP, execute opção 4
echo.
http-server -p 8080
pause
goto MENU

:OPEN_CORRECTION
echo.
echo ========================================
echo   🔧 ABRINDO PÁGINA DE CORREÇÃO
echo ========================================
echo.
start correcao-err-file-not-found.html
echo ✅ Página de correção aberta no navegador
echo.
pause
goto MENU

:SHOW_IP
echo.
echo ========================================
echo   🌐 DESCOBRINDO IP DO COMPUTADOR
echo ========================================
echo.
echo Seu(s) endereço(s) IP:
echo.
ipconfig | findstr /i "IPv4"
echo.
echo 📱 USE NO CELULAR:
echo.
echo Se aparecer algo como "192.168.1.105", use:
echo http://192.168.1.105:8080
echo.
echo ⚠️  IMPORTANTE:
echo - Celular deve estar na MESMA rede WiFi
echo - Substitua o IP pelo mostrado acima
echo - Servidor deve estar rodando (opção 1 ou 2)
echo.
pause
goto MENU

:MOBILE_INSTRUCTIONS
echo.
echo ========================================
echo   📱 INSTRUÇÕES PARA CELULAR
echo ========================================
echo.
echo PASSO A PASSO:
echo.
echo 1. 🖥️  NO COMPUTADOR:
echo    - Execute opção 1 ou 2 (servidor)
echo    - Anote o IP (opção 4)
echo    - Deixe servidor rodando
echo.
echo 2. 📱 NO CELULAR:
echo    - Conecte na MESMA rede WiFi
echo    - Abra navegador (Chrome/Safari)
echo    - Digite: http://IP-DO-PC:8080
echo    - Exemplo: http://192.168.1.105:8080
echo.
echo 3. ✅ RESULTADO:
echo    - VRS abrirá normalmente
echo    - Navegação funcionará perfeitamente
echo    - Sem erro ERR_FILE_NOT_FOUND
echo.
echo 4. 📲 OPCIONAL - INSTALAR PWA:
echo    - No navegador: Menu → "Instalar app"
echo    - Ícone aparecerá na tela inicial
echo    - Use como app nativo
echo.
pause
goto MENU

:GITHUB_DEPLOY
echo.
echo ========================================
echo   🚀 DEPLOY NO GITHUB PAGES
echo ========================================
echo.
echo Para usar VRS online sem servidor local:
echo.
echo 1. 📂 PREPARAR ARQUIVOS:
echo    - Todos os arquivos VRS em uma pasta
echo    - Verificar se não há dependências locais
echo.
echo 2. 🌐 GITHUB:
echo    - Criar conta: https://github.com
echo    - Criar repositório público
echo    - Nome sugerido: vrs-inventario
echo.
echo 3. 📤 UPLOAD:
echo    - Arrastar arquivos para repositório
echo    - Ou usar GitHub Desktop
echo    - Commit: "Deploy VRS System"
echo.
echo 4. ⚙️  ATIVAR PAGES:
echo    - Settings → Pages
echo    - Source: Deploy from branch
echo    - Branch: main / root
echo    - Salvar
echo.
echo 5. 🎉 RESULTADO:
echo    - URL: https://seuusuario.github.io/vrs-inventario
echo    - Acesse de qualquer dispositivo
echo    - Instale como PWA no celular
echo.
echo 🔗 ABRIR GITHUB?
set /p github="Pressione ENTER para abrir GitHub ou qualquer tecla para voltar: "
if "%github%"=="" start https://github.com
echo.
pause
goto MENU

:EXIT
echo.
echo ========================================
echo   👋 CORREÇÃO FINALIZADA
echo ========================================
echo.
echo RESUMO DAS SOLUÇÕES:
echo.
echo ✅ Servidor local: Para uso doméstico
echo ✅ GitHub Pages: Para acesso universal
echo ✅ PWA: Para experiência de app nativo
echo.
echo 💡 DICA: Após corrigir, teste a navegação
echo entre páginas no celular para confirmar
echo que o erro ERR_FILE_NOT_FOUND foi resolvido.
echo.
echo Obrigado por usar o VRS! 🚀
echo.
pause
exit

:ERROR
echo.
echo ❌ Opção inválida! Tente novamente.
echo.
pause
goto MENU
