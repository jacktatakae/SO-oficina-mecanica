# 📞 Atualização de Contatos - Oficina VRS

## ✅ Contatos da Oficina VRS Atualizados

**WhatsApp:** (11) 97196-0699  
**Email:** samusan18@gmail.com

⚠️ **IMPORTANTE:** Apenas os contatos da **Oficina VRS** foram alterados.  
Os contatos dos **fornecedores** (Zelukar, Cofap, etc.) permanecem os originais.

## 📁 Arquivos Atualizados

### ✅ Contatos da Oficina VRS:
1. **`cadastro-cliente.html`** - Email da oficina
2. **`qr-permanente.html`** - Contatos para suporte
3. **`config-contatos.js`** - Configuração da oficina

### 🔄 Contatos dos Fornecedores (Mantidos Originais):
1. **`catalogo-manager.js`** - Zelukar: (11) 2359-6457 / contato@zelukar.com.br
2. **`INTEGRACAO-ZELUKAR.md`** - Documentação com contatos originais

### 🔧 Arquivos Centrais de Configuração

#### **`config-contatos.js`** - Configuração Master
```javascript
// Use este arquivo para futuras atualizações
CONFIG_CONTATOS.contatos.whatsapp.numero = '5511971960699';
CONFIG_CONTATOS.contatos.email.principal = 'samusan18@gmail.com';
```

## 📋 Como Usar a Nova Configuração

### 1. **Incluir nos HTMLs:**
```html
<script src="config-contatos.js"></script>
```

### 2. **Usar nos Scripts:**
```javascript
// WhatsApp automático
const link = ContatosHelper.gerarLinkWhatsApp('cadastro', {url: 'https://...'});

// Email automático  
const email = ContatosHelper.gerarLinkEmail('Assunto', 'Mensagem');

// Contatos formatados
const contatos = ContatosHelper.obterContatos();
```

### 3. **HTML Automático:**
```html
<!-- Será atualizado automaticamente -->
<span data-whatsapp></span>
<span data-email></span>
<span data-telefone></span>

<script>
    ContatosHelper.atualizarElementosHTML();
</script>
```

## 🎯 Próximas Atualizações

### Para atualizar todos os contatos:

1. **Edite apenas:** `config-contatos.js`
2. **Execute:** `ContatosHelper.atualizarElementosHTML()`
3. **Pronto!** ✅

### Arquivos que ainda podem precisar de atualização manual:

- **`login.html`** - Verificar mensagens WhatsApp
- **`index.html`** - Verificar se há contatos hardcoded
- **`guia-uso.html`** - Documentação de contato

## 🔍 Como Verificar Contatos

### Buscar contatos antigos:
```bash
# No VS Code, usar busca global (Ctrl+Shift+F)
contato@zelukar
98115
2359
oficinaVRS
```

### Substituir por:
```
samusan18@gmail.com
971960699
971960699
samusan18@gmail.com
```

## 🚀 Vantagens do Sistema Centralizado

1. **✅ Uma única fonte:** Todos os contatos em um arquivo
2. **✅ Atualização automática:** Scripts se atualizam sozinhos
3. **✅ Consistência:** Mesmo formato em todo sistema
4. **✅ Fácil manutenção:** Mudança em um lugar = mudança em tudo

## 📱 Funcionalidades Automáticas

### **WhatsApp Inteligente:**
- Mensagens pré-formatadas
- Links automáticos
- Códigos de peças inclusos

### **Email Automático:**
- Assuntos preenchidos
- Corpo da mensagem formatado
- Links diretos

### **Telefone Formatado:**
- Formato brasileiro: (11) 97196-0699
- Formato internacional: +55 11 971960699
- Links tel: automáticos

---

**✅ Sistema atualizado e centralizado!**  
*Agora todas as atualizações de contato ficaram muito mais fáceis.*
