#!/bin/bash

# 🚀 Script para Deploy Automático do VRS no GitHub Pages
# Execute este script para hospedar seu VRS online automaticamente

echo "🚀 VRS - Deploy Automático GitHub Pages"
echo "======================================="

# Verificar se git está instalado
if ! command -v git &> /dev/null; then
    echo "❌ Git não encontrado. Instale git primeiro:"
    echo "   https://git-scm.com/downloads"
    exit 1
fi

# Verificar se está em um repositório git
if [ ! -d ".git" ]; then
    echo "📁 Inicializando repositório Git..."
    git init
    
    echo "📝 Configurando Git (se necessário)..."
    read -p "Digite seu nome de usuário GitHub: " username
    read -p "Digite seu email GitHub: " email
    
    git config user.name "$username"
    git config user.email "$email"
    
    echo "🔗 Conecte este repositório ao GitHub:"
    echo "   1. Vá para https://github.com/new"
    echo "   2. Crie um repositório público chamado 'vrs-sistema'"
    echo "   3. NÃO inicialize com README"
    echo "   4. Copie a URL do repositório"
    echo ""
    read -p "Cole a URL do repositório (ex: https://github.com/usuario/vrs-sistema.git): " repo_url
    
    git remote add origin "$repo_url"
fi

# Adicionar todos os arquivos
echo "📦 Adicionando arquivos ao Git..."
git add .

# Commit
echo "💾 Fazendo commit..."
git commit -m "Deploy VRS Sistema - $(date +'%Y-%m-%d %H:%M')"

# Push para GitHub
echo "⬆️ Enviando para GitHub..."
git push -u origin main 2>/dev/null || git push -u origin master

echo ""
echo "✅ Deploy concluído!"
echo ""
echo "🌐 Próximos passos:"
echo "   1. Vá para seu repositório no GitHub"
echo "   2. Clique em 'Settings'"
echo "   3. Role até 'Pages'"
echo "   4. Em 'Source', selecione 'Deploy from a branch'"
echo "   5. Escolha 'main' (ou 'master') e '/ (root)'"
echo "   6. Clique 'Save'"
echo ""
echo "⏱️ Aguarde 5-10 minutos e seu VRS estará online em:"
echo "   https://$(git config remote.origin.url | sed 's/.*github.com[:/]\([^/]*\)\/\([^.]*\).*/\1.github.io\/\2/')/"
echo ""
echo "📱 Depois é só instalar como PWA no celular!"
