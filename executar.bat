@echo off
echo.
echo ========================================
echo  🚗 SISTEMA DE PECAS AUTOMOTIVAS 🔧
echo ========================================
echo.

REM Verificar se Python esta disponivel
py --version >nul 2>&1
if errorlevel 1 (
    python --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ ERRO: Python nao encontrado!
        echo.
        echo Por favor, instale Python 3.7+ em: https://python.org
        echo Apos a instalacao, execute novamente este arquivo.
        echo.
        pause
        exit /b 1
    )
    set PYTHON_CMD=python
) else (
    set PYTHON_CMD=py
)

echo ✅ Python encontrado!
%PYTHON_CMD% --version

echo.
echo Iniciando o sistema...
echo.

%PYTHON_CMD% main.py

if errorlevel 1 (
    echo.
    echo ❌ Erro ao executar o sistema!
    echo.
    echo Possiveis solucoes:
    echo 1. Execute setup.bat primeiro para instalar dependencias
    echo 2. Verifique se todas as bibliotecas estao instaladas
    echo 3. Consulte o README.md para mais informacoes
    echo.
)

pause
