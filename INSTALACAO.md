# 🚨 GUIA DE INSTALAÇÃO E SOLUÇÃO DE PROBLEMAS

## ⚠️ PROBLEMA IDENTIFICADO
O Python não parece estar instalado ou configurado corretamente no sistema.

## 🔧 SOLUÇÕES PASSO A PASSO

### 1. INSTALAR PYTHON
1. Acesse: https://www.python.org/downloads/
2. Baixe Python 3.7 ou superior
3. **IMPORTANTE**: Marque "Add Python to PATH" durante a instalação
4. Reinicie o computador após a instalação

### 2. VERIFICAR INSTALAÇÃO
Abra o PowerShell/CMD e execute:
```bash
python --version
```
Deve retornar algo como: `Python 3.11.x`

Se não funcionar, tente:
```bash
py --version
```

### 3. INSTALAR DEPENDÊNCIAS

#### Opção A - Automática:
Execute o arquivo: `setup.bat`

#### Opção B - Manual:
```bash
python -m pip install --upgrade pip
python -m pip install requests beautifulsoup4 pandas lxml selenium webdriver-manager sqlalchemy python-dotenv matplotlib seaborn plotly
```

#### Opção C - Uma por vez:
```bash
python -m pip install requests
python -m pip install beautifulsoup4
python -m pip install pandas
python -m pip install lxml
python -m pip install selenium
python -m pip install webdriver-manager
python -m pip install sqlalchemy
python -m pip install python-dotenv
python -m pip install matplotlib
python -m pip install seaborn
python -m pip install plotly
```

### 4. EXECUTAR O SISTEMA

#### Opção A - Usar arquivo batch:
Execute: `executar.bat`

#### Opção B - Comando manual:
```bash
cd "c:\Users\Vinicius Radiadores\Documents\teste"
python main.py
```

## 🐛 PROBLEMAS COMUNS

### Python não encontrado
**Sintoma**: `'python' is not recognized as an internal or external command`

**Solução**:
1. Reinstalar Python marcando "Add to PATH"
2. Ou usar `py` ao invés de `python`
3. Ou adicionar manualmente ao PATH do Windows

### Erro de módulo não encontrado
**Sintoma**: `ModuleNotFoundError: No module named 'requests'`

**Solução**:
```bash
python -m pip install [nome-do-modulo]
```

### Problemas com pip
**Sintoma**: `'pip' is not recognized`

**Solução**:
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### Firewall/Antivírus bloqueando
**Sintoma**: Erro de conexão durante download

**Solução**:
1. Temporariamente desabilitar antivírus
2. Adicionar exceção para Python/pip
3. Usar conexão diferente

## 🔍 VERIFICAÇÃO DO SISTEMA

Execute este comando para verificar tudo:
```bash
python verificar_sistema.py
```

## 📂 ESTRUTURA DE ARQUIVOS ESPERADA

```
teste/
├── main.py                    # ← Sistema principal
├── sistema_automotivo.py      # ← Core do sistema
├── relatorios.py             # ← Relatórios
├── importador.py             # ← Import/export
├── verificar_sistema.py      # ← Verificador
├── setup.bat                 # ← Instalador Windows
├── executar.bat              # ← Executor Windows  
├── requirements.txt          # ← Dependências
├── README.md                 # ← Documentação
└── INSTALACAO.md            # ← Este arquivo
```

## 🚀 EXECUÇÃO RÁPIDA (SE PYTHON ESTIVER OK)

```bash
# Navegar para o diretório
cd "c:\Users\Vinicius Radiadores\Documents\teste"

# Instalar dependências
python -m pip install -r requirements.txt

# Executar sistema
python main.py
```

## 🆘 AINDA COM PROBLEMAS?

1. **Verificar versão do Windows**: O sistema funciona em Windows 10/11
2. **Usar PowerShell como Administrador**: Pode resolver problemas de permissão
3. **Verificar espaço em disco**: Pelo menos 500MB livres
4. **Conexão com internet**: Necessária para download de dependências
5. **Antivírus**: Pode estar bloqueando a instalação

## 📞 COMANDOS DE DIAGNÓSTICO

Execute estes comandos para diagnosticar problemas:

```bash
# Verificar Python
python --version
py --version

# Verificar pip
python -m pip --version
py -m pip --version

# Listar pacotes instalados
python -m pip list
py -m pip list

# Testar conexão
python -c "import requests; print('OK')"

# Verificar PATH
echo $env:PATH
```

## ✅ CHECKLIST DE VERIFICAÇÃO

- [ ] Python 3.7+ instalado
- [ ] Python adicionado ao PATH
- [ ] pip funcionando
- [ ] Conexão com internet ativa
- [ ] Antivírus não bloqueando
- [ ] Espaço em disco suficiente
- [ ] Todos os arquivos .py presentes
- [ ] Dependências instaladas

## 🎯 EXECUÇÃO DE TESTE SIMPLES

Teste básico para verificar se está tudo funcionando:

```bash
python -c "print('Python OK'); import sqlite3; print('SQLite OK'); import requests; print('Requests OK')"
```

Se este comando funcionar, o sistema base está OK!

---
**Desenvolvido para Windows com PowerShell**
**Se usar CMD, substitua os comandos accordingly**
