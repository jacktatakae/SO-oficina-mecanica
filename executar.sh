#!/bin/bash
# -*- coding: utf-8 -*-

echo ""
echo "========================================"
echo "  🚗 SISTEMA DE PEÇAS AUTOMOTIVAS 🔧"
echo "========================================"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para verificar se um comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar se Python está disponível
echo "🔍 Verificando Python..."

if command_exists python3; then
    PYTHON_CMD="python3"
    echo -e "${GREEN}✅ Python3 encontrado!${NC}"
    $PYTHON_CMD --version
elif command_exists python; then
    PYTHON_CMD="python"
    echo -e "${GREEN}✅ Python encontrado!${NC}"
    $PYTHON_CMD --version
else
    echo -e "${RED}❌ ERRO: Python não encontrado!${NC}"
    echo ""
    echo "Para instalar Python no Arch Linux:"
    echo "sudo pacman -S python python-pip"
    echo ""
    echo "Ou se usar yay/paru:"
    echo "yay -S python python-pip"
    echo ""
    read -p "Pressione Enter para continuar..."
    exit 1
fi

echo ""
echo "🚀 Iniciando o sistema..."
echo ""

# Executar o sistema
$PYTHON_CMD main.py

# Verificar se houve erro
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ Erro ao executar o sistema!${NC}"
    echo ""
    echo -e "${YELLOW}Possíveis soluções:${NC}"
    echo "1. Execute ./setup.sh primeiro para instalar dependências"
    echo "2. Verifique se todas as bibliotecas estão instaladas:"
    echo "   pip install -r requirements.txt"
    echo "3. Consulte o README.md para mais informações"
    echo ""
fi

read -p "Pressione Enter para continuar..."
