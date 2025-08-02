#!/bin/bash

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

clear
echo
echo "========================================"
echo "  🚨 CORREÇÃO ERR_FILE_NOT_FOUND"
echo "========================================"
echo
echo "Este script resolve o erro de navegação"
echo "entre páginas no celular."
echo
echo -e "${RED}PROBLEMA:${NC} 'Não foi possível acessar arquivo'"
echo -e "${YELLOW}CAUSA:${NC} Protocolo file:// bloqueado no mobile"
echo -e "${GREEN}SOLUÇÃO:${NC} Servidor web local"
echo

show_menu() {
    echo
    echo "ESCOLHA UMA OPÇÃO:"
    echo
    echo "[1] Iniciar servidor Python (Recomendado)"
    echo "[2] Iniciar servidor Node.js"
    echo "[3] Iniciar servidor PHP"
    echo "[4] Abrir página de correção"
    echo "[5] Descobrir IP do computador"
    echo "[6] Instruções para celular"
    echo "[7] Deploy online (GitHub Pages)"
    echo "[0] Sair"
    echo
    read -p "Digite o número da opção: " opcao
}

python_server() {
    echo
    echo "========================================"
    echo "  🐍 INICIANDO SERVIDOR PYTHON"
    echo "========================================"
    echo

    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}❌ Python não encontrado!${NC}"
        echo
        echo "INSTALE PYTHON:"
        echo "Ubuntu/Debian: sudo apt install python3"
        echo "macOS: brew install python3"
        echo "CentOS/RHEL: sudo yum install python3"
        echo
        read -p "Pressione ENTER para voltar..."
        return
    fi

    echo -e "${GREEN}✅ Python encontrado!${NC}"
    echo
    echo -e "${BLUE}🌐 Iniciando servidor na porta 8080...${NC}"
    echo
    echo -e "${YELLOW}⚠️  IMPORTANTE:${NC}"
    echo "1. Deixe este terminal ABERTO"
    echo "2. No celular, use: http://SEU-IP:8080"
    echo "3. Para descobrir seu IP, abra outro terminal e execute opção 5"
    echo
    echo -e "${RED}🛑 Para parar: Pressione Ctrl+C${NC}"
    echo

    $PYTHON_CMD -m http.server 8080
}

node_server() {
    echo
    echo "========================================"
    echo "  📦 INICIANDO SERVIDOR NODE.JS"
    echo "========================================"
    echo

    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js não encontrado!${NC}"
        echo
        echo "INSTALE NODE.JS:"
        echo "Ubuntu/Debian: curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt-get install -y nodejs"
        echo "macOS: brew install node"
        echo "CentOS/RHEL: sudo yum install nodejs npm"
        echo
        read -p "Pressione ENTER para voltar..."
        return
    fi

    echo -e "${GREEN}✅ Node.js encontrado!${NC}"
    echo

    if ! command -v http-server &> /dev/null; then
        echo "📦 Instalando http-server..."
        npm install -g http-server
    fi

    echo
    echo -e "${BLUE}🌐 Iniciando servidor na porta 8080...${NC}"
    echo
    echo -e "${YELLOW}⚠️  IMPORTANTE:${NC}"
    echo "1. Deixe este terminal ABERTO"
    echo "2. No celular, use: http://SEU-IP:8080"
    echo "3. Para descobrir seu IP, execute opção 5"
    echo

    http-server -p 8080
}

php_server() {
    echo
    echo "========================================"
    echo "  🐘 INICIANDO SERVIDOR PHP"
    echo "========================================"
    echo

    if ! command -v php &> /dev/null; then
        echo -e "${RED}❌ PHP não encontrado!${NC}"
        echo
        echo "INSTALE PHP:"
        echo "Ubuntu/Debian: sudo apt install php"
        echo "macOS: brew install php"
        echo "CentOS/RHEL: sudo yum install php"
        echo
        read -p "Pressione ENTER para voltar..."
        return
    fi

    echo -e "${GREEN}✅ PHP encontrado!${NC}"
    echo
    echo -e "${BLUE}🌐 Iniciando servidor na porta 8080...${NC}"
    echo
    echo -e "${YELLOW}⚠️  IMPORTANTE:${NC}"
    echo "1. Deixe este terminal ABERTO"
    echo "2. No celular, use: http://SEU-IP:8080"
    echo "3. Para descobrir seu IP, execute opção 5"
    echo

    php -S 0.0.0.0:8080
}

open_correction() {
    echo
    echo "========================================"
    echo "  🔧 ABRINDO PÁGINA DE CORREÇÃO"
    echo "========================================"
    echo

    if command -v xdg-open &> /dev/null; then
        xdg-open correcao-err-file-not-found.html
    elif command -v open &> /dev/null; then
        open correcao-err-file-not-found.html
    else
        echo "Abra manualmente: correcao-err-file-not-found.html"
    fi

    echo -e "${GREEN}✅ Página de correção aberta no navegador${NC}"
    echo
    read -p "Pressione ENTER para voltar..."
}

show_ip() {
    echo
    echo "========================================"
    echo "  🌐 DESCOBRINDO IP DO COMPUTADOR"
    echo "========================================"
    echo

    echo "Seu(s) endereço(s) IP:"
    echo

    if command -v ip &> /dev/null; then
        ip addr show | grep "inet " | grep -v "127.0.0.1" | awk '{print $2}' | cut -d/ -f1
    elif command -v ifconfig &> /dev/null; then
        ifconfig | grep "inet " | grep -v "127.0.0.1" | awk '{print $2}'
    else
        echo "Use: hostname -I"
        hostname -I
    fi

    echo
    echo -e "${BLUE}📱 USE NO CELULAR:${NC}"
    echo
    echo "Se aparecer algo como '192.168.1.105', use:"
    echo -e "${GREEN}http://192.168.1.105:8080${NC}"
    echo
    echo -e "${YELLOW}⚠️  IMPORTANTE:${NC}"
    echo "- Celular deve estar na MESMA rede WiFi"
    echo "- Substitua o IP pelo mostrado acima"
    echo "- Servidor deve estar rodando (opção 1, 2 ou 3)"
    echo
    read -p "Pressione ENTER para voltar..."
}

mobile_instructions() {
    echo
    echo "========================================"
    echo "  📱 INSTRUÇÕES PARA CELULAR"
    echo "========================================"
    echo
    echo "PASSO A PASSO:"
    echo
    echo -e "${BLUE}1. 🖥️  NO COMPUTADOR:${NC}"
    echo "   - Execute opção 1, 2 ou 3 (servidor)"
    echo "   - Anote o IP (opção 5)"
    echo "   - Deixe servidor rodando"
    echo
    echo -e "${BLUE}2. 📱 NO CELULAR:${NC}"
    echo "   - Conecte na MESMA rede WiFi"
    echo "   - Abra navegador (Chrome/Safari)"
    echo "   - Digite: http://IP-DO-PC:8080"
    echo "   - Exemplo: http://192.168.1.105:8080"
    echo
    echo -e "${GREEN}3. ✅ RESULTADO:${NC}"
    echo "   - VRS abrirá normalmente"
    echo "   - Navegação funcionará perfeitamente"
    echo "   - Sem erro ERR_FILE_NOT_FOUND"
    echo
    echo -e "${YELLOW}4. 📲 OPCIONAL - INSTALAR PWA:${NC}"
    echo "   - No navegador: Menu → 'Instalar app'"
    echo "   - Ícone aparecerá na tela inicial"
    echo "   - Use como app nativo"
    echo
    read -p "Pressione ENTER para voltar..."
}

github_deploy() {
    echo
    echo "========================================"
    echo "  🚀 DEPLOY NO GITHUB PAGES"
    echo "========================================"
    echo
    echo "Para usar VRS online sem servidor local:"
    echo
    echo -e "${BLUE}1. 📂 PREPARAR ARQUIVOS:${NC}"
    echo "   - Todos os arquivos VRS em uma pasta"
    echo "   - Verificar se não há dependências locais"
    echo
    echo -e "${BLUE}2. 🌐 GITHUB:${NC}"
    echo "   - Criar conta: https://github.com"
    echo "   - Criar repositório público"
    echo "   - Nome sugerido: vrs-inventario"
    echo
    echo -e "${BLUE}3. 📤 UPLOAD:${NC}"
    echo "   - Arrastar arquivos para repositório"
    echo "   - Ou usar git:"
    echo "     git init"
    echo "     git add ."
    echo "     git commit -m 'Deploy VRS System'"
    echo "     git push origin main"
    echo
    echo -e "${BLUE}4. ⚙️  ATIVAR PAGES:${NC}"
    echo "   - Settings → Pages"
    echo "   - Source: Deploy from branch"
    echo "   - Branch: main / root"
    echo "   - Salvar"
    echo
    echo -e "${GREEN}5. 🎉 RESULTADO:${NC}"
    echo "   - URL: https://seuusuario.github.io/vrs-inventario"
    echo "   - Acesse de qualquer dispositivo"
    echo "   - Instale como PWA no celular"
    echo
    read -p "Pressione ENTER para abrir GitHub ou qualquer tecla para voltar: " github
    if [ -z "$github" ]; then
        if command -v xdg-open &> /dev/null; then
            xdg-open https://github.com
        elif command -v open &> /dev/null; then
            open https://github.com
        fi
    fi
    echo
}

# Loop principal
while true; do
    show_menu
    case $opcao in
        1)
            python_server
            ;;
        2)
            node_server
            ;;
        3)
            php_server
            ;;
        4)
            open_correction
            ;;
        5)
            show_ip
            ;;
        6)
            mobile_instructions
            ;;
        7)
            github_deploy
            ;;
        0)
            echo
            echo "========================================"
            echo "  👋 CORREÇÃO FINALIZADA"
            echo "========================================"
            echo
            echo "RESUMO DAS SOLUÇÕES:"
            echo
            echo -e "${GREEN}✅ Servidor local: Para uso doméstico${NC}"
            echo -e "${GREEN}✅ GitHub Pages: Para acesso universal${NC}"
            echo -e "${GREEN}✅ PWA: Para experiência de app nativo${NC}"
            echo
            echo -e "${YELLOW}💡 DICA: Após corrigir, teste a navegação${NC}"
            echo "entre páginas no celular para confirmar"
            echo "que o erro ERR_FILE_NOT_FOUND foi resolvido."
            echo
            echo -e "${BLUE}Obrigado por usar o VRS! 🚀${NC}"
            echo
            exit 0
            ;;
        *)
            echo
            echo -e "${RED}❌ Opção inválida! Tente novamente.${NC}"
            echo
            read -p "Pressione ENTER para continuar..."
            ;;
    esac
done
