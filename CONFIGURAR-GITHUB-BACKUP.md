# 🔄 GUIA: Configurar Backup no GitHub

## 📋 **SITUAÇÃO ATUAL:**

### ❌ **Sem GitHub (Padrão):**
- ✅ Dados salvos no **navegador local**
- ❌ **NÃO sincroniza** entre computador e celular
- ❌ **Perde dados** se limpar o navegador
- ❌ **Sem backup** na nuvem

### ✅ **Com GitHub (Recomendado):**
- ✅ Dados salvos no **navegador + GitHub**
- ✅ **Sincroniza** entre todos os dispositivos
- ✅ **Backup automático** na nuvem
- ✅ **Histórico de versões**
- ✅ **Acesso de qualquer lugar**

---

## 🚀 **COMO CONFIGURAR GITHUB (5 MINUTOS):**

### **1️⃣ Criar Repositório no GitHub**

1. Acesse: https://github.com
2. Clique em **"New repository"**
3. Nome: `vrs-inventario-backup`
4. Deixe **Public** ou **Private** (sua escolha)
5. Marque **"Add a README file"**
6. Clique **"Create repository"**

### **2️⃣ Criar Token de Acesso**

1. Acesse: https://github.com/settings/tokens
2. Clique **"Generate new token (classic)"**
3. Nome: `VRS Inventário Backup`
4. Selecione a permissão: **`repo`** (marque toda a seção)
5. Clique **"Generate token"**
6. **COPIE O TOKEN** (ghp_xxxxxxxxxxxx) - só aparece uma vez!

### **3️⃣ Configurar no Sistema VRS**

1. No **Inventário Rápido**, clique **"Config GitHub"**
2. Cole o **Token** copiado
3. **Usuário GitHub**: seu nome de usuário
4. **Repositório**: `vrs-inventario-backup`
5. Clique **"Testar Conexão"**
6. Se OK, clique **"Salvar e Ativar"**

---

## 🎯 **RESULTADO:**

### **✅ Backup Automático:**
- **A cada mudança** no inventário → Auto backup no GitHub
- **Máximo 1 backup por minuto** (evita spam)
- **Arquivo JSON** com todos os dados

### **📱 Sincronização:**
- **Computador**: Adiciona tanque → Salva no GitHub
- **Celular**: Abre inventário → Baixa do GitHub
- **Sempre sincronizado** entre dispositivos

### **📂 Localização dos Backups:**
```
https://github.com/SEU-USUARIO/vrs-inventario-backup/tree/main/backups
```

### **📄 Formato dos Arquivos:**
```
backup_inventario_2025-08-01.json
backup_inventario_2025-08-02.json
...
```

---

## 🔧 **FUNÇÕES DISPONÍVEIS:**

| **Função** | **Descrição** |
|------------|---------------|
| **Auto Backup** | Salva automaticamente a cada mudança |
| **Backup Manual** | Força backup imediato |
| **Baixar Backup** | Restaura dados de backup específico |
| **Listar Backups** | Mostra todos os backups disponíveis |
| **Testar Conexão** | Verifica se configuração está OK |

---

## ⚠️ **IMPORTANTE:**

### **🔐 Segurança do Token:**
- **NÃO compartilhe** o token com ninguém
- **Use repositório privado** para dados sensíveis
- **Token expira** - renove quando necessário

### **📊 Limitações GitHub:**
- **1000 requests/hora** por token
- **100MB por arquivo** (mais que suficiente)
- **1GB total** por repositório gratuito

### **🔄 Sincronização:**
- **Auto sync**: 1 por minuto máximo
- **Manual sync**: Quantas vezes quiser
- **Conexão obrigatória** para sync

---

## 🎉 **CONFIGURAÇÃO FEITA!**

Agora seus dados estarão **100% seguros** e **sincronizados**!

### **Para testar:**
1. **Computador**: Adicione um tanque
2. **Celular**: Abra o inventário
3. **Clique**: "Config GitHub" → "Baixar Backup"
4. **Resultado**: Dados sincronizados! ✅

---

## 🆘 **SOLUÇÃO DE PROBLEMAS:**

### **❌ "Erro 401":**
- Token inválido ou expirado
- Gere novo token

### **❌ "Erro 404":**
- Repositório não existe
- Verifique nome do usuário/repositório

### **❌ "Erro de permissão":**
- Token sem permissão `repo`
- Recrie token com permissão correta

### **❌ "Timeout":**
- Conexão lenta
- Tente novamente

---

**✅ Com GitHub configurado, seus dados estão 100% seguros! 🛡️**
