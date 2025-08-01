// 🔧 CORRETOR AUTOMÁTICO DE NAVEGAÇÃO - VRS Mobile
// Resolve problemas de arquivos ausentes e navegação entre páginas

(function() {
    'use strict';
    
    console.log('🔧 Inicializando corretor de navegação VRS...');
    
    // Configurações
    const config = {
        debug: true,
        autoFix: true,
        fallbackPage: './inventario-rapido.html',
        retryAttempts: 3,
        retryDelay: 1000
    };
    
    // Lista de páginas conhecidas do VRS
    const knownPages = [
        'index.html',
        'inventario-rapido.html',
        'scanner-visual.html',
        'github-sync-mobile.html',
        'instalar-app.html',
        'teste-pwa.html',
        'diagnostico-arquivos.html',
        'gerenciador-backup.html',
        'cadastro-cliente.html',
        'central-sistemas.html'
    ];
    
    // Recursos críticos
    const criticalResources = [
        'auto-backup-system.js',
        'github-sync.js',
        'manifest.json',
        'sw.js'
    ];
    
    // Inicializar quando DOM estiver pronto
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initNavigationFixer);
    } else {
        initNavigationFixer();
    }
    
    function initNavigationFixer() {
        log('🚀 Corretor de navegação iniciado');
        
        // Verificar se estamos offline
        checkOnlineStatus();
        
        // Interceptar cliques em links
        interceptLinkClicks();
        
        // Verificar recursos críticos
        checkCriticalResources();
        
        // Configurar tratamento de erros
        setupErrorHandling();
        
        // Monitorar mudanças de conectividade
        window.addEventListener('online', handleOnline);
        window.addEventListener('offline', handleOffline);
        
        // Detectar problemas de navegação
        detectNavigationIssues();
    }
    
    function checkOnlineStatus() {
        const isOnline = navigator.onLine;
        log(`🌐 Status da conexão: ${isOnline ? 'Online' : 'Offline'}`);
        
        if (!isOnline) {
            showOfflineWarning();
        }
    }
    
    function interceptLinkClicks() {
        document.addEventListener('click', function(event) {
            const target = event.target.closest('a, button[onclick]');
            if (!target) return;
            
            let url = null;
            
            // Extrair URL do link ou onclick
            if (target.tagName === 'A') {
                url = target.href;
            } else if (target.onclick) {
                const onclickStr = target.onclick.toString();
                const match = onclickStr.match(/window\.location\.href\s*=\s*['"]([^'"]+)['"]/);
                if (match) {
                    url = match[1];
                }
            }
            
            if (url && isVRSPage(url)) {
                log(`🔗 Interceptando navegação para: ${url}`);
                
                // Prevenir navegação padrão
                event.preventDefault();
                
                // Navegar com tratamento de erro
                safeNavigate(url);
            }
        });
    }
    
    function isVRSPage(url) {
        const filename = url.split('/').pop().split('?')[0];
        return knownPages.includes(filename) || url.includes('./');
    }
    
    async function safeNavigate(url, attempt = 1) {
        try {
            log(`🚀 Tentativa ${attempt} de navegação para: ${url}`);
            
            // Verificar se página existe
            const exists = await checkPageExists(url);
            
            if (exists) {
                log(`✅ Página encontrada, navegando...`);
                window.location.href = url;
            } else {
                log(`❌ Página não encontrada: ${url}`);
                handleNavigationFailure(url, attempt);
            }
            
        } catch (error) {
            log(`❌ Erro na navegação: ${error.message}`);
            handleNavigationFailure(url, attempt);
        }
    }
    
    async function checkPageExists(url) {
        try {
            const response = await fetch(url, { 
                method: 'HEAD',
                cache: 'no-cache',
                signal: AbortSignal.timeout(5000)
            });
            return response.ok;
        } catch (error) {
            log(`⚠️ Erro ao verificar página: ${error.message}`);
            return false;
        }
    }
    
    function handleNavigationFailure(originalUrl, attempt) {
        if (attempt < config.retryAttempts) {
            log(`🔄 Tentando novamente em ${config.retryDelay}ms...`);
            setTimeout(() => safeNavigate(originalUrl, attempt + 1), config.retryDelay);
            return;
        }
        
        log(`🚨 Falha definitiva na navegação para: ${originalUrl}`);
        
        // Tentar alternativas
        const alternatives = findAlternatives(originalUrl);
        
        if (alternatives.length > 0) {
            showNavigationOptions(originalUrl, alternatives);
        } else {
            navigateToFallback();
        }
    }
    
    function findAlternatives(failedUrl) {
        const alternatives = [];
        const filename = failedUrl.split('/').pop().split('?')[0];
        
        // Sugerir páginas similares
        if (filename.includes('github') || filename.includes('sync')) {
            alternatives.push('./github-sync-mobile.html');
        }
        
        if (filename.includes('install') || filename.includes('app')) {
            alternatives.push('./instalar-app.html');
        }
        
        if (filename.includes('test') || filename.includes('diagnostic')) {
            alternatives.push('./teste-pwa.html', './diagnostico-arquivos.html');
        }
        
        // Adicionar páginas principais
        alternatives.push('./inventario-rapido.html', './index.html');
        
        // Remover duplicatas e página que falhou
        return [...new Set(alternatives)].filter(alt => !alt.includes(filename));
    }
    
    function showNavigationOptions(failedUrl, alternatives) {
        const modal = createNavigationModal(failedUrl, alternatives);
        document.body.appendChild(modal);
        
        // Auto-remover modal após 10 segundos
        setTimeout(() => {
            if (modal.parentNode) {
                modal.remove();
                navigateToFallback();
            }
        }, 10000);
    }
    
    function createNavigationModal(failedUrl, alternatives) {
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.8);
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: Arial, sans-serif;
        `;
        
        const content = document.createElement('div');
        content.style.cssText = `
            background: white;
            padding: 2rem;
            border-radius: 15px;
            max-width: 500px;
            width: 90%;
            text-align: center;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        `;
        
        content.innerHTML = `
            <h3 style="color: #dc3545; margin-bottom: 1rem;">
                🚨 Página Não Encontrada
            </h3>
            <p style="margin-bottom: 1.5rem; color: #666;">
                A página <strong>${failedUrl}</strong> não está disponível.
                <br>Escolha uma alternativa:
            </p>
            <div style="margin: 1rem 0;">
                ${alternatives.map(alt => `
                    <button onclick="window.location.href='${alt}'; this.closest('[style*=\"position: fixed\"]').remove();"
                            style="display: block; width: 100%; margin: 0.5rem 0; padding: 0.75rem; 
                                   background: #007bff; color: white; border: none; border-radius: 8px; 
                                   cursor: pointer; font-size: 1rem;">
                        📄 ${alt.replace('./', '').replace('.html', '')}
                    </button>
                `).join('')}
            </div>
            <button onclick="this.closest('[style*=\"position: fixed\"]').remove();"
                    style="margin-top: 1rem; padding: 0.5rem 1rem; background: #6c757d; 
                           color: white; border: none; border-radius: 5px; cursor: pointer;">
                ✖️ Fechar
            </button>
            <p style="font-size: 0.8rem; color: #999; margin-top: 1rem;">
                Auto-redirecionamento em 10 segundos...
            </p>
        `;
        
        modal.appendChild(content);
        return modal;
    }
    
    function navigateToFallback() {
        log(`🏠 Navegando para página de fallback: ${config.fallbackPage}`);
        window.location.href = config.fallbackPage;
    }
    
    async function checkCriticalResources() {
        log('🔍 Verificando recursos críticos...');
        
        const missing = [];
        
        for (const resource of criticalResources) {
            try {
                const response = await fetch(resource, { method: 'HEAD' });
                if (!response.ok) {
                    missing.push(resource);
                }
            } catch (error) {
                missing.push(resource);
            }
        }
        
        if (missing.length > 0) {
            log(`⚠️ Recursos ausentes: ${missing.join(', ')}`);
            showResourceWarning(missing);
        } else {
            log('✅ Todos os recursos críticos encontrados');
        }
    }
    
    function showResourceWarning(missingResources) {
        const warning = document.createElement('div');
        warning.style.cssText = `
            position: fixed;
            top: 10px;
            left: 10px;
            right: 10px;
            background: #fff3cd;
            color: #856404;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #ffeaa7;
            z-index: 9999;
            font-size: 0.9rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        `;
        
        warning.innerHTML = `
            <strong>⚠️ Alguns arquivos não foram encontrados:</strong><br>
            ${missingResources.join(', ')}<br>
            <small>Algumas funcionalidades podem não funcionar corretamente.</small>
            <button onclick="this.parentNode.remove()" 
                    style="float: right; background: none; border: none; font-size: 1.2rem; cursor: pointer;">
                ✖️
            </button>
        `;
        
        document.body.appendChild(warning);
        
        // Auto-remover após 15 segundos
        setTimeout(() => {
            if (warning.parentNode) {
                warning.remove();
            }
        }, 15000);
    }
    
    function setupErrorHandling() {
        // Interceptar erros de carregamento
        window.addEventListener('error', function(event) {
            if (event.target !== window) {
                const element = event.target;
                const src = element.src || element.href;
                
                if (src) {
                    log(`❌ Erro ao carregar recurso: ${src}`);
                    handleResourceError(element, src);
                }
            }
        });
        
        // Interceptar erros não tratados
        window.addEventListener('unhandledrejection', function(event) {
            log(`❌ Erro não tratado: ${event.reason}`);
        });
    }
    
    function handleResourceError(element, src) {
        const filename = src.split('/').pop();
        
        // Tentar caminhos alternativos
        const alternatives = [
            `./${filename}`,
            `../${filename}`,
            `./js/${filename}`,
            `./css/${filename}`
        ];
        
        tryAlternativePaths(element, alternatives, 0);
    }
    
    async function tryAlternativePaths(element, paths, index) {
        if (index >= paths.length) {
            log(`❌ Nenhuma alternativa encontrada para: ${element.src || element.href}`);
            return;
        }
        
        const path = paths[index];
        
        try {
            const response = await fetch(path, { method: 'HEAD' });
            if (response.ok) {
                log(`✅ Alternativa encontrada: ${path}`);
                if (element.src) {
                    element.src = path;
                } else if (element.href) {
                    element.href = path;
                }
                return;
            }
        } catch (error) {
            // Continuar para próxima alternativa
        }
        
        // Tentar próxima alternativa
        tryAlternativePaths(element, paths, index + 1);
    }
    
    function detectNavigationIssues() {
        // Verificar se estamos em uma página de erro
        if (document.title.includes('404') || document.body.textContent.includes('não encontrado')) {
            log('🚨 Página de erro detectada');
            showNavigationHelp();
        }
        
        // Verificar console para erros de rede
        const originalError = console.error;
        console.error = function(...args) {
            const message = args.join(' ');
            if (message.includes('Failed to fetch') || message.includes('net::ERR')) {
                log('🚨 Erro de rede detectado no console');
                handleNetworkError();
            }
            originalError.apply(console, args);
        };
    }
    
    function showNavigationHelp() {
        const help = document.createElement('div');
        help.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #007bff;
            color: white;
            padding: 1rem;
            border-radius: 10px;
            max-width: 300px;
            z-index: 9998;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        `;
        
        help.innerHTML = `
            <strong>🆘 Problemas de Navegação?</strong><br>
            <small>
            • Use os botões do VRS ao invés de links diretos<br>
            • Instale como PWA para melhor experiência<br>
            • Execute o diagnóstico se problemas persistirem
            </small>
            <br>
            <button onclick="window.location.href='./inventario-rapido.html'" 
                    style="margin-top: 0.5rem; padding: 0.25rem 0.5rem; background: white; 
                           color: #007bff; border: none; border-radius: 4px; cursor: pointer;">
                🏠 Ir para Início
            </button>
            <button onclick="this.parentNode.remove()" 
                    style="float: right; background: none; border: none; color: white; 
                           cursor: pointer; font-size: 1.2rem;">
                ✖️
            </button>
        `;
        
        document.body.appendChild(help);
    }
    
    function handleOnline() {
        log('🌐 Conectado à internet');
        hideOfflineWarning();
    }
    
    function handleOffline() {
        log('📱 Modo offline detectado');
        showOfflineWarning();
    }
    
    function showOfflineWarning() {
        if (document.getElementById('vrs-offline-warning')) return;
        
        const warning = document.createElement('div');
        warning.id = 'vrs-offline-warning';
        warning.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: #ffc107;
            color: #212529;
            padding: 0.5rem;
            text-align: center;
            z-index: 10001;
            font-weight: bold;
        `;
        
        warning.innerHTML = `
            📱 Modo Offline - Algumas funcionalidades podem estar limitadas
            <button onclick="this.parentNode.remove()" 
                    style="float: right; background: none; border: none; font-size: 1.2rem; cursor: pointer;">
                ✖️
            </button>
        `;
        
        document.body.appendChild(warning);
    }
    
    function hideOfflineWarning() {
        const warning = document.getElementById('vrs-offline-warning');
        if (warning) {
            warning.remove();
        }
    }
    
    function handleNetworkError() {
        log('🚨 Erro de rede detectado');
        
        if (!navigator.onLine) {
            showOfflineWarning();
        }
    }
    
    function log(message) {
        if (config.debug) {
            console.log(`[VRS Navigation Fixer] ${message}`);
        }
    }
    
    // Expor funcões globais para debugging
    window.vrsNavigationFixer = {
        safeNavigate,
        checkPageExists,
        checkCriticalResources,
        config
    };
    
    log('✅ Corretor de navegação VRS carregado com sucesso');
    
})();
