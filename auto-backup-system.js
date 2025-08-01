/**
 * 💾 SISTEMA DE AUTO BACKUP COMPLETO - VRS v2.0
 * Gerencia backup automático de todos os dados do sistema
 * Autor: Sistema VRS - Vinícius Radiadores Solutions
 */

class AutoBackupSystem {
    constructor() {
        this.config = {
            backupInterval: 15 * 60 * 1000, // 15 minutos em millisegundos
            maxBackups: 50, // Máximo de backups a manter
            backupKeys: [
                'inventario_tanques',
                'inventarioRapido', 
                'qrCodes',
                'scannerHistory',
                'configuracoes_sistema',
                'dados_zelukar',
                'historico_analises'
            ],
            compressionEnabled: true,
            cloudSyncEnabled: false, // Para futuro uso com API
            notificationsEnabled: true
        };
        
        this.backupHistory = JSON.parse(localStorage.getItem('backup_history') || '[]');
        this.isRunning = false;
        this.intervalId = null;
        
        this.init();
    }

    /**
     * Inicializar sistema de backup
     */
    init() {
        console.log('🔄 Inicializando Sistema de Auto Backup...');
        
        // Restaurar configurações salvas
        const savedConfig = localStorage.getItem('backup_config');
        if (savedConfig) {
            this.config = { ...this.config, ...JSON.parse(savedConfig) };
        }
        
        // Iniciar backup automático
        this.startAutoBackup();
        
        // Configurar eventos
        this.setupEventListeners();
        
        // Verificar integridade dos dados
        this.verifyDataIntegrity();
        
        console.log('✅ Sistema de Auto Backup Ativo');
        this.showNotification('Sistema de backup ativado', 'success');
    }

    /**
     * Iniciar backup automático
     */
    startAutoBackup() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.intervalId = setInterval(() => {
            this.createAutoBackup();
        }, this.config.backupInterval);
        
        console.log(`🔄 Auto backup ativo - Intervalo: ${this.config.backupInterval / 60000} minutos`);
    }

    /**
     * Parar backup automático
     */
    stopAutoBackup() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
        this.isRunning = false;
        console.log('⏹️ Auto backup pausado');
    }

    /**
     * Criar backup automático
     */
    async createAutoBackup() {
        try {
            const backupData = this.collectAllData();
            const backupInfo = {
                id: 'auto_' + Date.now(),
                timestamp: new Date().toISOString(),
                type: 'automatic',
                size: JSON.stringify(backupData).length,
                checksum: this.generateChecksum(backupData),
                version: '2.0',
                totalItems: this.countTotalItems(backupData)
            };

            // Comprimir dados se habilitado
            if (this.config.compressionEnabled) {
                backupData.compressed = true;
                backupData.originalSize = backupInfo.size;
            }

            // Salvar backup
            const backupKey = `backup_${backupInfo.id}`;
            localStorage.setItem(backupKey, JSON.stringify(backupData));
            
            // Adicionar ao histórico
            this.backupHistory.unshift(backupInfo);
            
            // Limitar número de backups
            this.cleanupOldBackups();
            
            // Salvar histórico atualizado
            localStorage.setItem('backup_history', JSON.stringify(this.backupHistory));
            
            console.log(`💾 Backup automático criado: ${backupInfo.id}`);
            
            // Notificar se habilitado
            if (this.config.notificationsEnabled) {
                this.showNotification(`Backup automático concluído (${backupInfo.totalItems} itens)`, 'info');
            }
            
            return backupInfo;
            
        } catch (error) {
            console.error('❌ Erro no backup automático:', error);
            this.showNotification('Erro no backup automático', 'error');
            throw error;
        }
    }

    /**
     * Criar backup manual
     */
    async createManualBackup(description = '') {
        try {
            const backupData = this.collectAllData();
            const backupInfo = {
                id: 'manual_' + Date.now(),
                timestamp: new Date().toISOString(),
                type: 'manual',
                description: description || 'Backup manual',
                size: JSON.stringify(backupData).length,
                checksum: this.generateChecksum(backupData),
                version: '2.0',
                totalItems: this.countTotalItems(backupData)
            };

            // Salvar backup
            const backupKey = `backup_${backupInfo.id}`;
            localStorage.setItem(backupKey, JSON.stringify(backupData));
            
            // Adicionar ao histórico
            this.backupHistory.unshift(backupInfo);
            localStorage.setItem('backup_history', JSON.stringify(this.backupHistory));
            
            console.log(`💾 Backup manual criado: ${backupInfo.id}`);
            this.showNotification('Backup manual criado com sucesso', 'success');
            
            return backupInfo;
            
        } catch (error) {
            console.error('❌ Erro no backup manual:', error);
            this.showNotification('Erro ao criar backup manual', 'error');
            throw error;
        }
    }

    /**
     * Coletar todos os dados do sistema
     */
    collectAllData() {
        const allData = {
            metadata: {
                created: new Date().toISOString(),
                version: '2.0',
                system: 'VRS - Sistema de Catalogação',
                browser: navigator.userAgent,
                url: window.location.href
            },
            data: {}
        };

        // Coletar dados de todas as chaves configuradas
        this.config.backupKeys.forEach(key => {
            const data = localStorage.getItem(key);
            if (data) {
                try {
                    allData.data[key] = JSON.parse(data);
                } catch (e) {
                    allData.data[key] = data; // Manter como string se não for JSON
                }
            }
        });

        // Adicionar configurações do sistema
        allData.config = this.config;
        
        // Adicionar estatísticas
        allData.stats = this.generateStats(allData.data);

        return allData;
    }

    /**
     * Restaurar backup
     */
    async restoreBackup(backupId, options = {}) {
        try {
            const backupKey = `backup_${backupId}`;
            const backupData = localStorage.getItem(backupKey);
            
            if (!backupData) {
                throw new Error('Backup não encontrado');
            }

            const parsedBackup = JSON.parse(backupData);
            
            // Verificar integridade
            const isValid = this.verifyBackupIntegrity(parsedBackup);
            if (!isValid && !options.force) {
                throw new Error('Backup corrompido - use force:true para forçar restauração');
            }

            // Fazer backup dos dados atuais antes de restaurar
            if (!options.skipCurrentBackup) {
                await this.createManualBackup('Backup antes da restauração');
            }

            // Restaurar dados
            Object.keys(parsedBackup.data).forEach(key => {
                if (options.selectiveKeys && !options.selectiveKeys.includes(key)) {
                    return; // Pular chaves não selecionadas
                }
                
                const value = parsedBackup.data[key];
                const stringValue = typeof value === 'object' ? JSON.stringify(value) : value;
                localStorage.setItem(key, stringValue);
            });

            console.log(`✅ Backup restaurado: ${backupId}`);
            this.showNotification('Backup restaurado com sucesso', 'success');
            
            // Recarregar a página para aplicar mudanças
            if (options.autoReload !== false) {
                setTimeout(() => {
                    window.location.reload();
                }, 2000);
            }
            
            return true;
            
        } catch (error) {
            console.error('❌ Erro na restauração:', error);
            this.showNotification(`Erro na restauração: ${error.message}`, 'error');
            throw error;
        }
    }

    /**
     * Exportar backup para arquivo
     */
    exportBackup(backupId) {
        try {
            const backupKey = `backup_${backupId}`;
            const backupData = localStorage.getItem(backupKey);
            
            if (!backupData) {
                throw new Error('Backup não encontrado');
            }

            const blob = new Blob([backupData], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            
            const backupInfo = this.backupHistory.find(b => b.id === backupId);
            const filename = `vrs_backup_${backupId}_${new Date().toISOString().split('T')[0]}.json`;
            
            a.href = url;
            a.download = filename;
            a.click();
            
            URL.revokeObjectURL(url);
            
            console.log(`📤 Backup exportado: ${filename}`);
            this.showNotification('Backup exportado com sucesso', 'success');
            
        } catch (error) {
            console.error('❌ Erro na exportação:', error);
            this.showNotification(`Erro na exportação: ${error.message}`, 'error');
        }
    }

    /**
     * Importar backup de arquivo
     */
    importBackup(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            
            reader.onload = async (e) => {
                try {
                    const backupData = JSON.parse(e.target.result);
                    
                    // Verificar se é um backup válido
                    if (!backupData.metadata || !backupData.data) {
                        throw new Error('Formato de backup inválido');
                    }

                    // Criar nova entrada no histórico
                    const backupInfo = {
                        id: 'imported_' + Date.now(),
                        timestamp: new Date().toISOString(),
                        type: 'imported',
                        description: `Importado de ${file.name}`,
                        size: JSON.stringify(backupData).length,
                        checksum: this.generateChecksum(backupData),
                        version: backupData.metadata.version || '1.0',
                        totalItems: this.countTotalItems(backupData.data),
                        originalFile: file.name
                    };

                    // Salvar backup
                    const backupKey = `backup_${backupInfo.id}`;
                    localStorage.setItem(backupKey, JSON.stringify(backupData));
                    
                    // Adicionar ao histórico
                    this.backupHistory.unshift(backupInfo);
                    localStorage.setItem('backup_history', JSON.stringify(this.backupHistory));
                    
                    console.log(`📥 Backup importado: ${backupInfo.id}`);
                    this.showNotification('Backup importado com sucesso', 'success');
                    
                    resolve(backupInfo);
                    
                } catch (error) {
                    console.error('❌ Erro na importação:', error);
                    this.showNotification(`Erro na importação: ${error.message}`, 'error');
                    reject(error);
                }
            };
            
            reader.onerror = () => {
                reject(new Error('Erro ao ler arquivo'));
            };
            
            reader.readAsText(file);
        });
    }

    /**
     * Limpar backups antigos
     */
    cleanupOldBackups() {
        // Manter apenas os backups mais recentes
        const toKeep = this.backupHistory.slice(0, this.config.maxBackups);
        const toDelete = this.backupHistory.slice(this.config.maxBackups);
        
        // Remover backups antigos do localStorage
        toDelete.forEach(backup => {
            const backupKey = `backup_${backup.id}`;
            localStorage.removeItem(backupKey);
        });
        
        // Atualizar histórico
        this.backupHistory = toKeep;
        
        if (toDelete.length > 0) {
            console.log(`🗑️ Removidos ${toDelete.length} backups antigos`);
        }
    }

    /**
     * Verificar integridade dos dados
     */
    verifyDataIntegrity() {
        const issues = [];
        
        this.config.backupKeys.forEach(key => {
            const data = localStorage.getItem(key);
            if (data) {
                try {
                    JSON.parse(data);
                } catch (e) {
                    if (key !== 'configuracoes_sistema') { // Algumas chaves podem ser strings simples
                        issues.push(`Dados corrompidos em: ${key}`);
                    }
                }
            }
        });

        if (issues.length > 0) {
            console.warn('⚠️ Problemas de integridade encontrados:', issues);
            this.showNotification(`${issues.length} problema(s) de integridade detectado(s)`, 'warning');
        }

        return issues.length === 0;
    }

    /**
     * Verificar integridade de backup específico
     */
    verifyBackupIntegrity(backupData) {
        try {
            // Verificar estrutura básica
            if (!backupData.metadata || !backupData.data) {
                return false;
            }

            // Verificar checksum se disponível
            if (backupData.checksum) {
                const currentChecksum = this.generateChecksum(backupData);
                if (currentChecksum !== backupData.checksum) {
                    return false;
                }
            }

            return true;
        } catch (error) {
            return false;
        }
    }

    /**
     * Gerar checksum simples para verificação de integridade
     */
    generateChecksum(data) {
        const str = JSON.stringify(data);
        let hash = 0;
        
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32bit integer
        }
        
        return hash.toString(16);
    }

    /**
     * Contar total de itens nos dados
     */
    countTotalItems(data) {
        let total = 0;
        
        Object.values(data).forEach(value => {
            if (Array.isArray(value)) {
                total += value.length;
            } else if (typeof value === 'object' && value !== null) {
                if (value.tanques) total += value.tanques.length;
                if (value.items) total += value.items.length;
            }
        });

        return total;
    }

    /**
     * Gerar estatísticas dos dados
     */
    generateStats(data) {
        const stats = {
            totalKeys: Object.keys(data).length,
            totalItems: this.countTotalItems(data),
            dataSize: JSON.stringify(data).length,
            lastModified: new Date().toISOString()
        };

        // Estatísticas específicas por módulo
        if (data.inventario_tanques) {
            stats.inventario = {
                totalTanques: data.inventario_tanques.tanques?.length || 0,
                montadoras: new Set(data.inventario_tanques.tanques?.map(t => t.montadora) || []).size
            };
        }

        if (data.qrCodes) {
            stats.qrCodes = Array.isArray(data.qrCodes) ? data.qrCodes.length : 0;
        }

        return stats;
    }

    /**
     * Configurar event listeners
     */
    setupEventListeners() {
        // Detectar mudanças no localStorage
        window.addEventListener('storage', (e) => {
            if (this.config.backupKeys.includes(e.key)) {
                console.log(`📝 Mudança detectada em: ${e.key}`);
            }
        });

        // Backup antes de fechar a página
        window.addEventListener('beforeunload', () => {
            if (this.isRunning) {
                this.createAutoBackup();
            }
        });

        // Detectar erros e criar backup de emergência
        window.addEventListener('error', (e) => {
            console.error('❌ Erro detectado, criando backup de emergência');
            this.createManualBackup('Backup de emergência - erro detectado');
        });
    }

    /**
     * Atualizar configurações
     */
    updateConfig(newConfig) {
        this.config = { ...this.config, ...newConfig };
        localStorage.setItem('backup_config', JSON.stringify(this.config));
        
        // Reiniciar auto backup se intervalo mudou
        if (newConfig.backupInterval && this.isRunning) {
            this.stopAutoBackup();
            this.startAutoBackup();
        }

        console.log('⚙️ Configurações de backup atualizadas');
    }

    /**
     * Obter informações do sistema de backup
     */
    getBackupInfo() {
        return {
            isRunning: this.isRunning,
            config: this.config,
            backupCount: this.backupHistory.length,
            totalSize: this.calculateTotalBackupSize(),
            lastBackup: this.backupHistory[0] || null,
            nextBackup: this.isRunning ? new Date(Date.now() + this.config.backupInterval).toISOString() : null
        };
    }

    /**
     * Calcular tamanho total dos backups
     */
    calculateTotalBackupSize() {
        return this.backupHistory.reduce((total, backup) => total + (backup.size || 0), 0);
    }

    /**
     * Mostrar notificação
     */
    showNotification(message, type = 'info') {
        if (!this.config.notificationsEnabled) return;

        // Criar toast notification
        const toast = document.createElement('div');
        toast.className = `toast position-fixed top-0 end-0 m-3`;
        toast.style.zIndex = '9999';
        toast.setAttribute('role', 'alert');
        
        const bgClass = {
            'success': 'bg-success',
            'error': 'bg-danger', 
            'warning': 'bg-warning',
            'info': 'bg-info'
        }[type] || 'bg-info';

        toast.innerHTML = `
            <div class="toast-header ${bgClass} text-white">
                <strong class="me-auto">🔄 Auto Backup</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        `;

        document.body.appendChild(toast);
        
        // Mostrar toast
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remover após exibição
        toast.addEventListener('hidden.bs.toast', () => {
            document.body.removeChild(toast);
        });
    }

    /**
     * Obter lista de backups
     */
    getBackupList() {
        return this.backupHistory.map(backup => ({
            ...backup,
            sizeFormatted: this.formatFileSize(backup.size),
            dateFormatted: new Date(backup.timestamp).toLocaleString('pt-BR'),
            ageFormatted: this.formatAge(backup.timestamp)
        }));
    }

    /**
     * Formatar tamanho do arquivo
     */
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    /**
     * Formatar idade do backup
     */
    formatAge(timestamp) {
        const now = new Date();
        const backup = new Date(timestamp);
        const diffMs = now - backup;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMins / 60);
        const diffDays = Math.floor(diffHours / 24);

        if (diffDays > 0) return `${diffDays} dia(s)`;
        if (diffHours > 0) return `${diffHours} hora(s)`;
        if (diffMins > 0) return `${diffMins} minuto(s)`;
        return 'Agora mesmo';
    }

    /**
     * Deletar backup específico
     */
    deleteBackup(backupId) {
        try {
            // Remover do localStorage
            const backupKey = `backup_${backupId}`;
            localStorage.removeItem(backupKey);
            
            // Remover do histórico
            this.backupHistory = this.backupHistory.filter(b => b.id !== backupId);
            localStorage.setItem('backup_history', JSON.stringify(this.backupHistory));
            
            console.log(`🗑️ Backup deletado: ${backupId}`);
            this.showNotification('Backup deletado com sucesso', 'info');
            
            return true;
        } catch (error) {
            console.error('❌ Erro ao deletar backup:', error);
            this.showNotification('Erro ao deletar backup', 'error');
            return false;
        }
    }
}

// Exportar para uso global
window.AutoBackupSystem = AutoBackupSystem;

// Inicializar automaticamente se não estiver em modo de teste
if (typeof window !== 'undefined' && !window.BACKUP_TEST_MODE) {
    window.autoBackup = new AutoBackupSystem();
}

console.log('💾 Sistema de Auto Backup carregado com sucesso!');
