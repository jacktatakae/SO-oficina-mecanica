# 🌐 Interface Web - Sistema de Peças Automotivas

Uma interface web moderna e interativa para o Sistema de Gestão de Peças Automotivas, criada para facilitar o uso de todas as funcionalidades do sistema Python de forma visual e intuitiva.

## 🚀 Como Usar

### Opção 1: Launcher (Recomendado)
```bash
# Abra o arquivo launcher.html no seu navegador
start launcher.html  # Windows
open launcher.html   # macOS
xdg-open launcher.html  # Linux
```

### Opção 2: Interface Web Direta
```bash
# Abra o arquivo index.html no seu navegador
start index.html  # Windows
```

## 📋 Funcionalidades da Interface Web

### 🌐 **Extração de Dados**
- **Atualização Completa**: Extrai peças de todas as categorias
- **Busca Específica**: Busca por termo específico (ex: "vela ignição")
- **Visualização em Tempo Real**: Acompanhe o progresso da extração
- **Integração com Python**: Executa os scripts reais de extração

### 👤 **Gestão de Clientes**
- **Cadastro Visual**: Formulário intuitivo para novos clientes
- **Busca Avançada**: Por nome, telefone ou marca do carro
- **Listagem Dinâmica**: Visualização em tabela responsiva
- **Validação em Tempo Real**: Campos obrigatórios e formatação

### 🔍 **Consulta de Peças**
- **Busca por Categoria**: Navegação por categorias organizadas
- **Busca por Fabricante**: Filtragem por marca específica
- **Busca por Nome**: Pesquisa textual avançada
- **Ranking de Preços**: Visualização das peças mais caras/baratas

### 📊 **Relatórios Visuais**
- **Dashboard Interativo**: Gráficos em tempo real
- **Estatísticas Gerais**: Métricas principais do sistema
- **Análise de Preços**: Gráficos por categoria
- **Relatório de Estoque**: Controle visual do inventário

### 📥 **Import/Export Visual**
- **Upload de Arquivos**: Interface drag-and-drop
- **Templates Automáticos**: Geração de modelos CSV
- **Preview de Dados**: Visualização antes da importação
- **Download Direto**: Exportação com um clique

### ⚙️ **Configurações**
- **Verificação de Sistema**: Status das dependências
- **Backup Visual**: Interface para backup/restore
- **Limpeza de Cache**: Manutenção do sistema
- **Integração Python**: Execução dos scripts originais

## 🎨 Design e UX

### **Características Visuais**
- ✨ **Design Moderno**: Interface clean e profissional
- 📱 **Responsivo**: Adaptável a desktop, tablet e mobile
- 🎯 **Intuitivo**: Navegação simples e clara
- 🚀 **Animações**: Transições suaves e feedback visual
- 🎨 **Cores Organizadas**: Esquema de cores consistente

### **Componentes Interativos**
- 🔄 **Loading States**: Indicadores de progresso
- 📝 **Formulários Inteligentes**: Validação e sugestões
- 📊 **Gráficos Dinâmicos**: Chart.js integrado
- 🔍 **Busca em Tempo Real**: Resultados instantâneos
- 📋 **Tabelas Responsivas**: Ordenação e filtros

## 🔗 Integração com Python

### **Execução Real dos Scripts**
A interface web pode executar os scripts Python reais através do arquivo `python-bridge.js`:

```javascript
// Exemplo de execução real
await pythonBridge.executeFullExtraction();
await pythonBridge.registerClient(clientData);
await pythonBridge.generateDashboard();
```

### **Scripts Suportados**
- ✅ `main.py` - Sistema principal
- ✅ `sistema_automotivo.py` - Core do sistema
- ✅ `relatorios.py` - Relatórios avançados
- ✅ `importador.py` - Import/export de dados
- ✅ `demo_simples.py` - Versão simplificada
- ✅ `verificar_sistema.py` - Verificação de sistema

## 📱 Modo Responsivo

### **Desktop (1200px+)**
- Layout de 3-4 colunas
- Gráficos em tela cheia
- Sidebar expansível
- Múltiplos modais simultâneos

### **Tablet (768px - 1199px)**
- Layout de 2 colunas
- Navegação por abas
- Gráficos adaptáveis
- Formulários otimizados

### **Mobile (até 767px)**
- Layout de 1 coluna
- Menu hambúrguer
- Cards empilhados
- Touch-friendly

## 🛠️ Tecnologias Utilizadas

### **Frontend**
- **HTML5**: Estrutura semântica
- **CSS3**: Estilos modernos com gradientes e animações
- **JavaScript ES6+**: Funcionalidades interativas
- **Bootstrap 5**: Framework CSS responsivo
- **Font Awesome**: Ícones vetoriais
- **AOS**: Animações on scroll

### **Gráficos e Visualização**
- **Chart.js**: Gráficos interativos
- **Plotly.js**: Visualizações avançadas (via Python)
- **CSS Grid/Flexbox**: Layouts flexíveis

### **Integração Backend**
- **Python Bridge**: Conexão com scripts Python
- **File API**: Upload de arquivos
- **Local Storage**: Persistência de configurações

## 📂 Estrutura dos Arquivos

```
front engine/
├── launcher.html          # Página inicial de seleção
├── index.html            # Interface principal web
├── python-bridge.js      # Ponte para scripts Python
├── README_WEB.md         # Este arquivo
│
├── main.py              # Sistema principal Python
├── sistema_automotivo.py # Core do sistema
├── relatorios.py         # Relatórios avançados
├── importador.py         # Import/export
├── demo_simples.py       # Demo simplificado
└── automotivas.db        # Banco de dados SQLite
```

## 🎯 Casos de Uso

### **Para Usuários Iniciantes**
1. Abra `launcher.html`
2. Clique em "Interface Web Interativa"
3. Use a interface visual para todas as operações
4. Visualize resultados em tempo real

### **Para Usuários Avançados**
1. Use a interface web para operações rápidas
2. Execute scripts Python diretamente quando necessário
3. Combine ambas as abordagens conforme a necessidade

### **Para Desenvolvimento**
1. Modifique `python-bridge.js` para novas integrações
2. Adicione novos modais em `index.html`
3. Estenda funcionalidades mantendo compatibilidade

## 🔧 Configuração Avançada

### **Personalizar Conexão Python**
```javascript
// Em python-bridge.js
const pythonBridge = new PythonBridge();
pythonBridge.pythonPath = 'python3'; // Para Linux/macOS
pythonBridge.basePath = './scripts/'; // Caminho personalizado
```

### **Adicionar Novas Funcionalidades**
```javascript
// Exemplo de nova funcionalidade
async function customFunction() {
    const result = await pythonBridge.executePython('custom_script.py', ['--param']);
    return result;
}
```

## 🚨 Solução de Problemas

### **Interface não carrega**
- Verifique se todos os arquivos estão na mesma pasta
- Use um servidor local se necessário: `python -m http.server 8000`

### **Scripts Python não executam**
- Verifique se o Python está instalado e no PATH
- Confirme que todas as dependências estão instaladas
- Use `python verificar_sistema.py` para diagnóstico

### **Dados não aparecem**
- Execute primeiro uma extração de dados
- Verifique se o banco de dados `automotivas.db` existe
- Use o modo "Demo Simples" para teste

## 🎉 Vantagens da Interface Web

### **Facilidade de Uso**
- ✅ Não requer conhecimento de linha de comando
- ✅ Interface visual e intuitiva
- ✅ Feedback imediato das operações
- ✅ Prevenção de erros com validação

### **Produtividade**
- ⚡ Acesso rápido a todas as funcionalidades
- 📊 Visualização imediata de dados
- 🔄 Operações em paralelo
- 💾 Persistência de configurações

### **Acessibilidade**
- 🌐 Funciona em qualquer navegador moderno
- 📱 Responsivo para dispositivos móveis
- 🎨 Design acessível e contrastado
- ⌨️ Suporte a navegação por teclado

---

**💡 Dica**: Para a melhor experiência, mantenha tanto a interface web quanto os scripts Python funcionando. A interface oferece praticidade visual, enquanto o Python garante todas as funcionalidades avançadas!
