# 🚗 Sistema de Gestão de Peças Automotivas

Sistema completo desenvolvido em Python para gerenciar peças automotivas e clientes, com extração automática de dados da internet.

## 📋 Funcionalidades

### 🌐 Extração de Dados da Internet
- Busca automática de peças no MercadoLivre e OLX
- Categorização inteligente das peças encontradas
- Atualização periódica dos preços

### 👤 Gestão de Clientes
- Cadastro completo de clientes
- Informações do veículo (marca, modelo, ano)
- Busca por nome, telefone ou marca do carro

### 📦 Categorias de Peças
- **Motor**: Velas, pistões, válvulas, correias
- **Suspensão**: Amortecedores, molas, braços
- **Arrefecimento**: Radiadores, ventoinhas, termostatos
- **Ar Condicionado**: Compressores, condensadores
- **Injeção Eletrônica**: Bicos injetores, sensores, módulos
- **Freios**: Pastilhas, discos, tambores
- **Elétrica**: Baterias, alternadores, fusíveis
- **Transmissão**: Embreagens, câmbios, diferenciais

### 📊 Relatórios e Análises
- Estatísticas gerais do sistema
- Análise de preços por categoria
- Relatórios de estoque
- Dashboard HTML interativo
- Gráficos e visualizações

### 📥 Importação/Exportação
- Import/export de dados via CSV
- Templates pré-configurados
- Backup automático do banco de dados

## 🛠️ Instalação

### 1. Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Dependências Principais
```
requests==2.31.0
beautifulsoup4==4.12.2
pandas==2.0.3
matplotlib==3.7.1
seaborn==0.12.2
plotly==5.15.0
sqlalchemy==2.0.19
lxml==4.9.3
```

## 🚀 Como Usar

### Executar o Sistema Principal
```bash
python main.py
```

### Executar Módulos Individuais

#### Sistema Base
```bash
python sistema_automotivo.py
```

#### Relatórios Avançados
```bash
python relatorios.py
```

#### Importação de Dados
```bash
python importador.py
```

## 📁 Estrutura do Projeto

```
teste/
├── main.py                 # Interface principal do sistema
├── sistema_automotivo.py   # Core do sistema (DB + Web Scraping)
├── relatorios.py          # Relatórios e análises avançadas
├── importador.py          # Import/export de dados CSV
├── requirements.txt       # Dependências Python
├── README.md             # Este arquivo
├── automotivas.db        # Banco de dados SQLite (criado automaticamente)
└── templates/            # Templates CSV (criados automaticamente)
    ├── template_pecas.csv
    └── template_clientes.csv
```

## 💾 Banco de Dados

O sistema usa SQLite com as seguintes tabelas:

### Tabelas Principais
- **categorias**: Categorias de peças
- **pecas**: Informações das peças automotivas
- **clientes**: Dados dos clientes
- **vendas**: Registro de vendas (futuro)
- **itens_venda**: Itens das vendas (futuro)

### Esquema das Tabelas

#### Peças
```sql
CREATE TABLE pecas (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(200),
    categoria_id INTEGER,
    preco DECIMAL(10,2),
    fabricante VARCHAR(100),
    codigo_peca VARCHAR(50),
    aplicacao TEXT,
    descricao TEXT,
    url_fonte TEXT,
    data_atualizacao TIMESTAMP
);
```

#### Clientes
```sql
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(200),
    endereco TEXT,
    telefone VARCHAR(20),
    email VARCHAR(100),
    marca_carro VARCHAR(50),
    modelo_carro VARCHAR(100),
    ano_carro INTEGER,
    data_cadastro TIMESTAMP
);
```

## 🌐 Fontes de Dados

### Sites Suportados
1. **MercadoLivre Brasil**
   - Busca por categorias específicas
   - Extração de preços e descrições
   - URLs dos produtos

2. **OLX Brasil**
   - Seção de peças automotivas
   - Preços e descrições
   - Identificação de peças usadas

### Processo de Extração
1. Busca automática por termos específicos
2. Análise do HTML das páginas
3. Extração de dados estruturados
4. Categorização inteligente
5. Armazenamento no banco de dados

## 📊 Exemplos de Uso

### 1. Cadastrar um Cliente
```python
sistema = SistemaAutomotivo()
sistema.cadastrar_cliente(
    nome="João Silva",
    endereco="Rua das Flores, 123",
    telefone="11999999999",
    email="joao@email.com",
    marca_carro="Volkswagen",
    modelo_carro="Gol",
    ano_carro=2018
)
```

### 2. Buscar Peças por Categoria
```python
pecas_motor = sistema.buscar_pecas_por_categoria("Motor")
print(pecas_motor)
```

### 3. Gerar Relatório
```python
relatorios = RelatoriosAvancados()
stats = relatorios.estatisticas_gerais()
print(f"Total de peças: {stats['total_pecas']}")
```

## 📈 Relatórios Disponíveis

### 1. Estatísticas Gerais
- Total de peças e clientes
- Categorias ativas
- Preços médios
- Marca de carro mais comum

### 2. Análise de Preços
- Distribuição por categoria
- Gráficos box-plot
- Estatísticas descritivas

### 3. Dashboard HTML
- Gráficos interativos
- Visualizações com Plotly
- Exportação para HTML

### 4. Relatórios de Estoque
- Quantidade por categoria
- Faixas de preço
- Fabricantes mais comuns

## 🔧 Configurações Avançadas

### Personalizar Fontes de Dados
Edite o arquivo `sistema_automotivo.py` na classe `WebScraper` para adicionar novos sites:

```python
def extrair_pecas_novo_site(self, termo_busca):
    # Implementar extração de novo site
    pass
```

### Adicionar Novas Categorias
```python
# No DatabaseManager.init_database()
novas_categorias = [
    ('Pneus', 'Pneus e rodas'),
    ('Som', 'Sistema de som automotivo')
]
```

### Customizar Relatórios
Crie novos métodos na classe `RelatoriosAvancados`:

```python
def meu_relatorio_customizado(self):
    # Implementar relatório personalizado
    pass
```

## 🐛 Solução de Problemas

### Erro ao Instalar Dependências
```bash
# Atualizar pip
python -m pip install --upgrade pip

# Instalar uma por vez
pip install requests
pip install beautifulsoup4
pip install pandas
```

### Erro de Conexão com Sites
- Verificar conexão com internet
- Alguns sites podem bloquear requisições automatizadas
- Usar VPN se necessário

### Banco de Dados Corrompido
```bash
# Deletar e recriar
rm automotivas.db
python sistema_automotivo.py
```

## 🔒 Considerações de Segurança

### Web Scraping Ético
- Respeitar robots.txt dos sites
- Não fazer muitas requisições simultâneas
- Usar delays entre requisições
- Não sobrecarregar os servidores

### Dados Pessoais
- Criptografar dados sensíveis se necessário
- Fazer backups regulares
- Implementar controle de acesso

## 🚀 Futuras Melhorias

### Funcionalidades Planejadas
- [ ] Sistema de vendas completo
- [ ] Integração com APIs oficiais
- [ ] Notificações de preços
- [ ] App mobile
- [ ] Sistema de estoque avançado
- [ ] Integração com e-commerce

### Melhorias Técnicas
- [ ] Cache de requisições
- [ ] Processamento assíncrono
- [ ] API REST
- [ ] Testes automatizados
- [ ] Docker container

## 📞 Suporte

Para problemas ou sugestões:
1. Verificar este README
2. Consultar o código fonte
3. Criar issue no repositório

## 📄 Licença

Este projeto é de código aberto e pode ser usado para fins educacionais e comerciais.

---

**Desenvolvido com ❤️ para o mercado automotivo brasileiro**
