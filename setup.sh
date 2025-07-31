#!/bin/bash
# -*- coding: utf-8 -*-

echo ""
echo "========================================"
echo "  🚗 SETUP - SISTEMA AUTOMOTIVAS 🔧"
echo "========================================"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para verificar se um comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo -e "${BLUE}📦 Configurando ambiente Python para Arch Linux...${NC}"
echo ""

# Verificar se Python está instalado
if ! command_exists python3 && ! command_exists python; then
    echo -e "${RED}❌ Python não encontrado!${NC}"
    echo ""
    echo -e "${YELLOW}Instalando Python no Arch Linux...${NC}"
    
    if command_exists pacman; then
        sudo pacman -S --needed python python-pip python-setuptools
    elif command_exists yay; then
        yay -S --needed python python-pip python-setuptools
    elif command_exists paru; then
        paru -S --needed python python-pip python-setuptools
    else
        echo -e "${RED}❌ Gerenciador de pacotes não encontrado!${NC}"
        echo "Instale manualmente: sudo pacman -S python python-pip"
        exit 1
    fi
fi

# Determinar comando Python
if command_exists python3; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command_exists python; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
fi

echo -e "${GREEN}✅ Python encontrado:${NC}"
$PYTHON_CMD --version
echo ""

# Verificar se pip está instalado
if ! command_exists $PIP_CMD; then
    echo -e "${YELLOW}📦 Instalando pip...${NC}"
    sudo pacman -S --needed python-pip
fi

echo -e "${GREEN}✅ Pip encontrado:${NC}"
$PIP_CMD --version
echo ""

# Atualizar pip
echo -e "${BLUE}🔄 Atualizando pip...${NC}"
$PIP_CMD install --upgrade pip

echo ""
echo -e "${BLUE}📚 Instalando dependências do requirements.txt...${NC}"
echo ""

# Instalar dependências
if [ -f "requirements.txt" ]; then
    $PIP_CMD install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ Todas as dependências foram instaladas com sucesso!${NC}"
        
        # Instalar dependências específicas do Arch se necessário
        echo ""
        echo -e "${BLUE}🔧 Verificando dependências específicas do Arch...${NC}"
        
        # SQLite (geralmente já incluído)
        if ! $PYTHON_CMD -c "import sqlite3" 2>/dev/null; then
            echo -e "${YELLOW}📦 Instalando SQLite...${NC}"
            sudo pacman -S --needed sqlite
        fi
        
        # Bibliotecas de desenvolvimento se necessário
        if ! $PYTHON_CMD -c "import lxml" 2>/dev/null; then
            echo -e "${YELLOW}📦 Instalando dependências XML...${NC}"
            sudo pacman -S --needed libxml2 libxslt
        fi
        
        echo ""
        echo -e "${GREEN}🎉 Setup concluído com sucesso!${NC}"
        echo ""
        echo -e "${BLUE}Para executar o sistema:${NC}"
        echo "./executar.sh"
        echo ""
        echo -e "${BLUE}Ou diretamente:${NC}"
        echo "$PYTHON_CMD main.py"
        
    else
        echo ""
        echo -e "${RED}❌ Erro ao instalar dependências!${NC}"
        echo ""
        echo -e "${YELLOW}Tente instalar manualmente:${NC}"
        echo "$PIP_CMD install requests beautifulsoup4 pandas matplotlib seaborn plotly"
        exit 1
    fi
else
    echo -e "${RED}❌ Arquivo requirements.txt não encontrado!${NC}"
    echo ""
    echo -e "${YELLOW}Instalando dependências básicas...${NC}"
    $PIP_CMD install requests beautifulsoup4 pandas matplotlib seaborn plotly
fi

echo ""
read -p "Pressione Enter para continuar..."
