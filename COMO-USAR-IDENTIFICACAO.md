# 🔧 Sistema de Identificação de Peças por Código

## Como Usar

O sistema identifica automaticamente o fabricante e busca informações da peça apenas digitando o código do fabricante.

### Exemplos de Códigos Suportados

#### Zelukar (Radiadores)
- **FI-001** → Caixa de Radiador Doblô Superior
- **VW-001** → Radiador Gol G5/G6 Completo
- **GM-123** → Peças GM (formato reconhecido)

#### Cofap (Filtros)
- **CF-1234** → Filtro de Óleo Motor
- **CF-5678** → Filtro de Ar Motor
- **C12345** → Filtros diversos

#### Bosch (Sistema Elétrico)
- **B456** → Vela de Ignição Iridium
- **F123456** → Peças diversas
- **0123456789** → Código de 10 dígitos

#### Delphi (Combustível e Ignição)
- **D789** → Bomba de Combustível
- **DG123456** → Peças diversas
- **AF1234** → Filtros de ar

#### Mahle (Componentes do Motor)
- **M321** → Pistão com Anéis
- **ML1234** → Metal Leve
- **KC123** → Componentes KC

## Funcionalidades

### 🔍 Busca Inteligente
- Digite apenas o código da peça
- Sistema identifica automaticamente o fabricante
- Mostra informações completas: preço, estoque, aplicações

### 📥 Importação Automática
- Se a peça não estiver na base local
- Sistema oferece importação do catálogo online
- Adiciona automaticamente à sua base de dados

### ➕ Cadastro Manual
- Para peças não encontradas
- Formulário inteligente com dados do catálogo
- Salva na base para próximas consultas

### 📋 Catálogos Integrados
- 5 fabricantes principais configurados
- Formatos de código pré-definidos
- Links diretos para catálogos online

## Como Testar

1. **Abra o arquivo:** `identificacao-pecas.html`
2. **Digite um código:** Ex: `FI-001`
3. **Pressione Enter** ou clique em "Buscar Peça"
4. **Veja o resultado** com todas as informações

### Códigos de Teste Disponíveis
```
FI-001  → Caixa Radiador Doblô (Zelukar)
CF-1234 → Filtro Óleo (Cofap)
B456    → Vela Ignição (Bosch)
D789    → Bomba Combustível (Delphi)
M321    → Pistão (Mahle)
```

## Integração com Sistema Principal

Para integrar com seu sistema atual:

1. **Inclua os arquivos:**
   ```html
   <script src="catalogo-manager.js"></script>
   ```

2. **Inicialize o sistema:**
   ```javascript
   const catalogoManager = new CatalogoManager();
   ```

3. **Use a função de busca:**
   ```javascript
   const resultado = catalogoManager.buscarPeca('FI-001');
   ```

## Adicionando Novos Fabricantes

No arquivo `catalogo-manager.js`, adicione:

```javascript
this.addCatalogo('NOVO_FABRICANTE', {
    nome: 'Nome do Fabricante',
    prefixos: ['NF-', 'N'],
    categoria: 'Categoria das Peças',
    formato: {
        codigo: /^NF-\d{3,4}$/i,
        descricao: 'NF- seguido de 3-4 dígitos'
    },
    url: 'https://site-do-fabricante.com',
    contato: '(11) 1234-5678'
});
```

## Próximos Passos

- **Conectar com API real** dos fabricantes
- **Sincronização automática** de preços e estoque
- **Histórico de consultas** para análise
- **Alertas de novas peças** disponíveis
- **Integração com WhatsApp** para notificações

---

**Desenvolvido para Oficina VRS** 🔧
*Sistema inteligente de identificação de peças automotivas*
