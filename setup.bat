@echo off
echo ========================================
echo  SISTEMA DE PECAS AUTOMOTIVAS - SETUP
echo ========================================

echo.
echo Verificando Python...
py --version 2>nul
if errorlevel 1 (
    python --version 2>nul
    if errorlevel 1 (
        echo ERRO: Python nao encontrado!
        echo Por favor, instale Python 3.7+ em: https://python.org
        pause
        exit /b 1
    )
    set PYTHON_CMD=python
) else (
    set PYTHON_CMD=py
)

echo.
echo Instalando dependencias...
%PYTHON_CMD% -m pip install --upgrade pip
%PYTHON_CMD% -m pip install requests beautifulsoup4 pandas lxml selenium webdriver-manager sqlalchemy python-dotenv matplotlib seaborn plotly

if errorlevel 1 (
    echo.
    echo ERRO na instalacao das dependencias!
    echo Tentando instalar uma por vez...
    
    %PYTHON_CMD% -m pip install requests
    %PYTHON_CMD% -m pip install beautifulsoup4
    %PYTHON_CMD% -m pip install pandas
    %PYTHON_CMD% -m pip install lxml
    %PYTHON_CMD% -m pip install selenium
    %PYTHON_CMD% -m pip install webdriver-manager
    %PYTHON_CMD% -m pip install sqlalchemy
    %PYTHON_CMD% -m pip install python-dotenv
    %PYTHON_CMD% -m pip install matplotlib
    %PYTHON_CMD% -m pip install seaborn
    %PYTHON_CMD% -m pip install plotly
)

echo.
echo ========================================
echo  INSTALACAO CONCLUIDA!
echo ========================================
echo.
echo Para executar o sistema, use:
echo   %PYTHON_CMD% main.py
echo.
echo Para criar templates CSV:
echo   %PYTHON_CMD% importador.py
echo.
echo Para gerar relatorios:
echo   %PYTHON_CMD% relatorios.py
echo.
pause
