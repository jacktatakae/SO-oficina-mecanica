# 🚗 Sistema de Peças Automotivas - Versão Arch Linux

## 📋 Pré-requisitos

### Sistema Operacional
- Arch Linux (ou derivados como Manjaro, EndeavourOS)
- Acesso a terminal com privilégios sudo

### Dependências do Sistema
```bash
# Atualizar sistema
sudo pacman -Syu

# Instalar Python e ferramentas básicas
sudo pacman -S python python-pip git

# Dependências opcionais para melhor performance
sudo pacman -S python-lxml python-requests python-beautifulsoup4
```

## 🚀 Instalação Rápida

### 1. Clonar/Baixar o Sistema
```bash
# Se usando git
git clone <repository-url>
cd sistema-automotivas

# Ou extrair arquivo ZIP
unzip sistema-automotivas.zip
cd sistema-automotivas
```

### 2. Executar Setup Automático
```bash
# Dar permissão de execução
chmod +x setup.sh
chmod +x executar.sh

# Executar instalação
./setup.sh
```

### 3. Executar Sistema
```bash
./executar.sh
```

## 🔧 Instalação Manual

### 1. Verificar Python
```bash
python3 --version
# ou
python --version
```

### 2. Instalar Dependências
```bash
# Via pip
pip install -r requirements.txt

# Ou individualmente
pip install requests beautifulsoup4 pandas matplotlib seaborn plotly lxml
```

### 3. Dependências do Sistema (se necessário)
```bash
# Para web scraping avançado
sudo pacman -S chromium chromedriver

# Para processamento XML
sudo pacman -S libxml2 libxslt

# Para visualizações
sudo pacman -S python-matplotlib python-seaborn
```

## 🖥️ Uso do Sistema

### Executar Sistema Principal
```bash
python3 main.py
# ou
python main.py
```

### Funcionalidades Disponíveis
1. **🔍 Buscar Peças** - Busca específica por modelo de carro
2. **📊 Relatórios** - Gerar relatórios de compatibilidade
3. **➕ Adicionar Peças** - Expandir banco de dados
4. **🔧 Configurações** - Personalizar sistema

## 📁 Estrutura do Projeto

```
sistema-automotivas/
├── main.py                    # Interface principal
├── sistema_automotivo.py      # Lógica do sistema
├── relatorios.py             # Geração de relatórios
├── importador.py             # Import de dados externos
├── automotivas.db            # Banco de dados SQLite
├── requirements.txt          # Dependências Python
├── executar.sh              # Script de execução Linux
├── setup.sh                 # Script de instalação Linux
├── GUIA_ADICIONAR_MODELOS.py # Guia para adicionar modelos
└── exemplo_adicionar_mobi.py # Exemplo prático
```

## 🎯 Recursos Específicos

### Base de Dados Técnica
- **32+ Radiadores** com especificações completas
- **8 Modelos de Carros** com dados reais
- **Códigos Originais** (Valeo, Behr, Denso, etc.)
- **Dimensões Precisas** e materiais

### Busca Inteligente
- Reconhecimento automático de modelos
- Filtros por fabricante, ano, motor
- Compatibilidade específica por veículo

### Relatórios Detalhados
- Exportação em Excel/PDF
- Gráficos de compatibilidade
- Análises de estoque

## 🐛 Solução de Problemas

### Erro: "Python não encontrado"
```bash
# Instalar Python
sudo pacman -S python python-pip

# Verificar instalação
which python3
```

### Erro: "Módulo não encontrado"
```bash
# Reinstalar dependências
pip install --upgrade -r requirements.txt

# Verificar instalação
python3 -c "import requests; print('OK')"
```

### Erro: "Permissão negada"
```bash
# Dar permissões aos scripts
chmod +x *.sh

# Executar com permissões adequadas
./executar.sh
```

### Problemas de Encoding
```bash
# Verificar locale
locale

# Configurar UTF-8 se necessário
export LANG=pt_BR.UTF-8
export LC_ALL=pt_BR.UTF-8
```

## 📞 Suporte

### Logs do Sistema
- Logs são salvos em: `~/.local/share/sistema-automotivas/logs/`
- Arquivo principal: `sistema.log`

### Informações de Debug
```bash
# Executar com debug
python3 main.py --debug

# Verificar versões
python3 --version
pip list | grep -E "(requests|beautifulsoup4|pandas)"
```

### Comandos Úteis
```bash
# Limpar cache Python
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# Verificar dependências
pip check

# Atualizar dependências
pip install --upgrade -r requirements.txt
```

## 🔄 Atualizações

### Atualizar Sistema
```bash
# Via git (se aplicável)
git pull origin main

# Reinstalar dependências
pip install --upgrade -r requirements.txt

# Verificar compatibilidade
python3 verificar_sistema.py
```

## 📈 Performance

### Otimizações para Arch Linux
- Use `python-lxml` do repositório oficial para melhor performance
- Configure cache local para web scraping
- Use SSD para banco de dados SQLite

### Configurações Recomendadas
```bash
# Instalar versões otimizadas
sudo pacman -S python-requests python-beautifulsoup4 python-pandas

# Para desenvolvimento
sudo pacman -S python-pytest python-black python-flake8
```
