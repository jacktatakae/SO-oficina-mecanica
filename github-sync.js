// github-sync.js - Sistema de sincronização com GitHub

class GitHubSync {
    constructor() {
        this.token = null; // Token do GitHub (será configurado pelo usuário)
        this.repo = null;  // Repositório (será configurado)
        this.owner = null; // Usuário do GitHub
        this.isEnabled = false;
        this.lastSync = null;
        
        this.loadConfig();
        console.log('🔄 Sistema GitHub Sync inicializado');
    }
    
    // Carregar configuração salva
    loadConfig() {
        const config = localStorage.getItem('github_sync_config');
        if (config) {
            const parsed = JSON.parse(config);
            this.token = parsed.token;
            this.repo = parsed.repo;
            this.owner = parsed.owner;
            this.isEnabled = parsed.isEnabled || false;
            this.lastSync = parsed.lastSync;
        }
    }
    
    // Salvar configuração
    saveConfig() {
        const config = {
            token: this.token,
            repo: this.repo,
            owner: this.owner,
            isEnabled: this.isEnabled,
            lastSync: this.lastSync
        };
        localStorage.setItem('github_sync_config', JSON.stringify(config));
    }
    
    // Configurar GitHub
    configure(token, owner, repo) {
        this.token = token;
        this.owner = owner;
        this.repo = repo;
        this.isEnabled = true;
        this.saveConfig();
        
        console.log(`✅ GitHub configurado: ${owner}/${repo}`);
        return this.testConnection();
    }
    
    // Testar conexão
    async testConnection() {
        try {
            const response = await fetch(`https://api.github.com/repos/${this.owner}/${this.repo}`, {
                headers: {
                    'Authorization': `token ${this.token}`,
                    'Accept': 'application/vnd.github.v3+json'
                }
            });
            
            if (response.ok) {
                console.log('✅ Conexão com GitHub OK');
                return { success: true, message: 'Conexão estabelecida com sucesso!' };
            } else {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
        } catch (error) {
            console.error('❌ Erro na conexão:', error);
            return { success: false, message: `Erro: ${error.message}` };
        }
    }
    
    // Sincronizar dados do inventário
    async syncInventory(inventoryData) {
        if (!this.isEnabled || !this.token) {
            return { success: false, message: 'GitHub Sync não configurado' };
        }
        
        try {
            const fileName = `backup_inventario_${new Date().toISOString().split('T')[0]}.json`;
            const content = JSON.stringify(inventoryData, null, 2);
            const encodedContent = btoa(unescape(encodeURIComponent(content)));
            
            // Verificar se arquivo já existe
            let sha = null;
            try {
                const existingResponse = await fetch(`https://api.github.com/repos/${this.owner}/${this.repo}/contents/backups/${fileName}`, {
                    headers: {
                        'Authorization': `token ${this.token}`,
                        'Accept': 'application/vnd.github.v3+json'
                    }
                });
                
                if (existingResponse.ok) {
                    const existingData = await existingResponse.json();
                    sha = existingData.sha;
                }
            } catch (e) {
                // Arquivo não existe, isso é OK
            }
            
            // Criar/atualizar arquivo
            const payload = {
                message: `🔄 Auto backup do inventário - ${new Date().toISOString()}`,
                content: encodedContent,
                branch: 'main'
            };
            
            if (sha) {
                payload.sha = sha; // Para atualizar arquivo existente
            }
            
            const response = await fetch(`https://api.github.com/repos/${this.owner}/${this.repo}/contents/backups/${fileName}`, {
                method: 'PUT',
                headers: {
                    'Authorization': `token ${this.token}`,
                    'Accept': 'application/vnd.github.v3+json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            
            if (response.ok) {
                this.lastSync = new Date().toISOString();
                this.saveConfig();
                
                const result = await response.json();
                console.log('✅ Backup enviado para GitHub:', result.content.html_url);
                
                return {
                    success: true,
                    message: 'Backup salvo no GitHub com sucesso!',
                    url: result.content.html_url
                };
            } else {
                const error = await response.json();
                throw new Error(error.message || 'Erro desconhecido');
            }
            
        } catch (error) {
            console.error('❌ Erro no sync:', error);
            return {
                success: false,
                message: `Erro no backup: ${error.message}`
            };
        }
    }
    
    // Auto sync (chamado a cada mudança)
    async autoSync(inventoryData) {
        if (!this.isEnabled) return;
        
        // Limitar auto sync para não spammar (máximo 1 por minuto)
        const lastSyncTime = this.lastSync ? new Date(this.lastSync).getTime() : 0;
        const now = Date.now();
        const oneMinute = 60 * 1000;
        
        if (now - lastSyncTime < oneMinute) {
            console.log('⏱️ Auto sync em cooldown');
            return;
        }
        
        console.log('🔄 Executando auto sync...');
        return this.syncInventory(inventoryData);
    }
    
    // Baixar backup do GitHub
    async downloadBackup(fileName) {
        if (!this.isEnabled || !this.token) {
            return { success: false, message: 'GitHub Sync não configurado' };
        }
        
        try {
            const response = await fetch(`https://api.github.com/repos/${this.owner}/${this.repo}/contents/backups/${fileName}`, {
                headers: {
                    'Authorization': `token ${this.token}`,
                    'Accept': 'application/vnd.github.v3+json'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                const content = atob(data.content);
                const inventoryData = JSON.parse(content);
                
                return {
                    success: true,
                    data: inventoryData,
                    message: 'Backup baixado do GitHub!'
                };
            } else {
                throw new Error(`Arquivo não encontrado: ${fileName}`);
            }
            
        } catch (error) {
            return {
                success: false,
                message: `Erro ao baixar: ${error.message}`
            };
        }
    }
    
    // Listar backups disponíveis
    async listBackups() {
        if (!this.isEnabled || !this.token) {
            return { success: false, message: 'GitHub Sync não configurado' };
        }
        
        try {
            const response = await fetch(`https://api.github.com/repos/${this.owner}/${this.repo}/contents/backups`, {
                headers: {
                    'Authorization': `token ${this.token}`,
                    'Accept': 'application/vnd.github.v3+json'
                }
            });
            
            if (response.ok) {
                const files = await response.json();
                const backups = files
                    .filter(file => file.name.startsWith('backup_inventario_') && file.name.endsWith('.json'))
                    .map(file => ({
                        name: file.name,
                        size: file.size,
                        url: file.html_url,
                        downloadUrl: file.download_url
                    }))
                    .sort((a, b) => b.name.localeCompare(a.name)); // Mais recente primeiro
                
                return {
                    success: true,
                    backups: backups,
                    message: `${backups.length} backups encontrados`
                };
            } else {
                throw new Error('Erro ao listar backups');
            }
            
        } catch (error) {
            return {
                success: false,
                message: `Erro: ${error.message}`
            };
        }
    }
    
    // Desabilitar sync
    disable() {
        this.isEnabled = false;
        this.saveConfig();
        console.log('❌ GitHub Sync desabilitado');
    }
    
    // Status do sync
    getStatus() {
        return {
            enabled: this.isEnabled,
            configured: !!(this.token && this.owner && this.repo),
            lastSync: this.lastSync,
            repo: this.isEnabled ? `${this.owner}/${this.repo}` : null
        };
    }
}

// Instância global
window.githubSync = new GitHubSync();

console.log('🔄 GitHub Sync carregado!');
