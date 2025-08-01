// 🔄 SERVICE WORKER VRS - Funcionamento Offline
// Versão 2.1 - Compatibilidade Total entre Plataformas

const CACHE_NAME = 'vrs-catalogo-v2.2';
const CACHE_VERSION = '2025.08.01.1';

// Arquivos essenciais para cache
const CORE_FILES = [
  './',
  './index.html',
  './inventario-rapido.html',
  './scanner-visual.html',
  './gerenciador-backup.html',
  './qr-catalogacao.html',
  './inventario-mobile.html',
  './teste-completo.html',
  './github-sync-mobile.html',
  './teste-github-sync.html',
  './instalar-app.html',
  './teste-pwa.html',
  './cadastro-cliente.html',
  './central-sistemas.html',
  './gerenciador-clientes.html',
  './qr-teste.html',
  './vrs-universal.html',
  './offline.html',
  './auto-backup-system.js',
  './ia-visual-radiadores.js',
  './github-sync.js',
  './python-bridge.js',
  './catalogo-manager.js',
  './config-contatos.js',
  './navigation-fixer.js',
  './manifest.json',
  './styles.css',
  './mobile-responsive.css'
];

// Recursos externos (CDN) para cache
const EXTERNAL_RESOURCES = [
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
  'https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css',
  'https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.css',
  'https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.js',
  'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js'
];

// URLs que devem sempre ser buscadas da rede
const NETWORK_FIRST = [
  '/api/',
  '.json',
  'github.com',
  'api.github.com'
];

// Instalar Service Worker
self.addEventListener('install', (event) => {
  console.log('🔧 Instalando Service Worker VRS v' + CACHE_VERSION);
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('📦 Criando cache inicial...');
        
        // Cache dos arquivos principais
        const cachePromises = [
          cache.addAll(CORE_FILES.map(url => new Request(url, { 
            mode: 'cors',
            credentials: 'omit' 
          }))).catch(err => {
            console.warn('⚠️ Erro ao cachear arquivos core:', err);
            // Tentar cachear individualmente
            return Promise.allSettled(
              CORE_FILES.map(url => 
                cache.add(new Request(url, { mode: 'cors', credentials: 'omit' }))
                  .catch(e => console.warn('❌ Falha ao cachear:', url, e))
              )
            );
          }),
          
          // Cache dos recursos externos
          Promise.allSettled(
            EXTERNAL_RESOURCES.map(url =>
              cache.add(new Request(url, { mode: 'cors', credentials: 'omit' }))
                .catch(e => console.warn('❌ Falha ao cachear recurso externo:', url, e))
            )
          )
        ];
        
        return Promise.all(cachePromises);
      })
      .then(() => {
        console.log('✅ Service Worker instalado com sucesso');
        return self.skipWaiting(); // Ativar imediatamente
      })
      .catch((error) => {
        console.error('❌ Erro na instalação do Service Worker:', error);
      })
  );
});

// Ativar Service Worker
self.addEventListener('activate', (event) => {
  console.log('🚀 Ativando Service Worker VRS');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        // Limpar caches antigos
        const deletePromises = cacheNames
          .filter(cacheName => cacheName !== CACHE_NAME)
          .map(cacheName => {
            console.log('🗑️ Removendo cache antigo:', cacheName);
            return caches.delete(cacheName);
          });
        
        return Promise.all(deletePromises);
      })
      .then(() => {
        console.log('✅ Service Worker ativado');
        return self.clients.claim(); // Controlar todas as abas
      })
      .catch((error) => {
        console.error('❌ Erro na ativação:', error);
      })
  );
});

// Interceptar requisições
self.addEventListener('fetch', (event) => {
  const request = event.request;
  const url = new URL(request.url);
  
  // Ignorar requisições não-HTTP
  if (!request.url.startsWith('http')) {
    return;
  }
  
  // Ignorar requisições de extensões do navegador
  if (url.protocol === 'chrome-extension:' || url.protocol === 'moz-extension:') {
    return;
  }
  
  // Estratégia: Cache First para recursos estáticos
  if (isStaticResource(request)) {
    event.respondWith(cacheFirst(request));
    return;
  }
  
  // Estratégia: Network First para dados dinâmicos
  if (isNetworkFirst(request)) {
    event.respondWith(networkFirst(request));
    return;
  }
  
  // Estratégia padrão: Cache First com fallback
  event.respondWith(cacheFirstWithFallback(request));
});

// Verificar se é recurso estático
function isStaticResource(request) {
  const url = request.url;
  return url.includes('.css') || 
         url.includes('.js') || 
         url.includes('.html') ||
         url.includes('.svg') ||
         url.includes('.png') ||
         url.includes('.jpg') ||
         url.includes('.woff') ||
         url.includes('bootstrap') ||
         url.includes('font-awesome');
}

// Verificar se deve priorizar rede
function isNetworkFirst(request) {
  const url = request.url;
  return NETWORK_FIRST.some(pattern => url.includes(pattern)) ||
         request.method !== 'GET';
}

// Estratégia: Cache First
async function cacheFirst(request) {
  try {
    const cache = await caches.open(CACHE_NAME);
    const cached = await cache.match(request);
    
    if (cached) {
      console.log('📱 Servindo do cache:', request.url);
      return cached;
    }
    
    console.log('🌐 Buscando na rede:', request.url);
    const response = await fetch(request);
    
    if (response.ok) {
      // Clonar resposta para cache
      const responseClone = response.clone();
      cache.put(request, responseClone);
    }
    
    return response;
  } catch (error) {
    console.error('❌ Erro em cacheFirst:', error);
    return new Response('Recurso não disponível offline', { 
      status: 503,
      statusText: 'Service Unavailable'
    });
  }
}

// Estratégia: Network First
async function networkFirst(request) {
  try {
    console.log('🌐 Network first para:', request.url);
    const response = await fetch(request);
    
    if (response.ok && request.method === 'GET') {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    
    return response;
  } catch (error) {
    console.log('📱 Fallback para cache:', request.url);
    const cache = await caches.open(CACHE_NAME);
    const cached = await cache.match(request);
    
    if (cached) {
      return cached;
    }
    
    return new Response('Dados não disponíveis offline', { 
      status: 503,
      statusText: 'Service Unavailable'
    });
  }
}

// Estratégia: Cache First com Fallback
async function cacheFirstWithFallback(request) {
  try {
    const cache = await caches.open(CACHE_NAME);
    const cached = await cache.match(request);
    
    if (cached) {
      return cached;
    }
    
    const response = await fetch(request);
    
    if (response.ok) {
      cache.put(request, response.clone());
    }
    
    return response;
  } catch (error) {
    console.error('❌ Erro total na requisição:', error);
    
    // Melhor tratamento de fallback
    return await handleAdvancedFallback(request, cache);
  }
}

// Tratamento avançado de fallback
async function handleAdvancedFallback(request, cache) {
  const url = new URL(request.url);
  const pathname = url.pathname;
  
  // Para páginas HTML
  if (request.destination === 'document' || request.headers.get('accept')?.includes('text/html')) {
    console.log('🔄 Fallback para página HTML:', pathname);
    
    // Lista de fallbacks em ordem de prioridade
    const fallbacks = [
      './inventario-rapido.html',
      './index.html',
      './offline.html'
    ];
    
    for (const fallback of fallbacks) {
      try {
        const fallbackResponse = await cache.match(fallback);
        if (fallbackResponse) {
          console.log('✅ Usando fallback:', fallback);
          return fallbackResponse;
        }
      } catch (e) {
        console.log('⚠️ Fallback falhou:', fallback);
      }
    }
    
    // Criar página de erro customizada
    return createErrorPage(pathname);
  }
  
  // Para arquivos JavaScript
  if (pathname.includes('.js')) {
    return new Response(`
      console.warn('📄 Arquivo JS não encontrado (offline):', '${pathname}');
      // Funções básicas para evitar erros
      window.offlineMode = true;
    `, {
      headers: { 'Content-Type': 'application/javascript' }
    });
  }
  
  // Para arquivos CSS
  if (pathname.includes('.css')) {
    return new Response(`
      /* 📄 Arquivo CSS não encontrado (offline): ${pathname} */
      .offline-warning {
        background: #ffeb3b !important;
        color: #333 !important;
        padding: 10px !important;
        text-align: center !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 9999 !important;
      }
    `, {
      headers: { 'Content-Type': 'text/css' }
    });
  }
  
  // Resposta padrão
  return new Response('Recurso não encontrado offline: ' + pathname, { 
    status: 404,
    statusText: 'Not Found',
    headers: { 'Content-Type': 'text/plain; charset=utf-8' }
  });
}

// Criar página de erro amigável
function createErrorPage(requestedPath) {
  const html = `
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Página não encontrada - VRS</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            text-align: center; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: rgba(255,255,255,0.1);
            padding: 2rem;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            max-width: 500px;
            width: 90%;
        }
        h1 { color: #ffeb3b; margin-bottom: 1rem; font-size: 2rem; }
        .btn {
            background: #2196F3;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            text-decoration: none;
            margin: 5px;
            display: inline-block;
            font-weight: bold;
            cursor: pointer;
        }
        .btn:hover { background: #1976D2; }
        .error-info {
            background: rgba(255,255,255,0.1);
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            font-family: monospace;
            font-size: 0.9rem;
            word-break: break-all;
        }
        @media (max-width: 480px) {
            .container { padding: 1rem; }
            h1 { font-size: 1.5rem; }
            .btn { padding: 10px 20px; font-size: 0.9rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Página Não Encontrada</h1>
        <p>A página solicitada não está disponível offline.</p>
        
        <div class="error-info">
            <strong>Solicitado:</strong><br>
            ${requestedPath}
        </div>
        
        <p>Navegue para uma das páginas disponíveis:</p>
        
        <div style="margin: 20px 0;">
            <a href="./inventario-rapido.html" class="btn">📦 Inventário</a>
            <a href="./index.html" class="btn">🏠 Início</a>
            <br>
            <a href="./scanner-visual.html" class="btn">📷 Scanner</a>
            <a href="./instalar-app.html" class="btn">📱 Instalar App</a>
        </div>
        
        <div style="margin: 20px 0;">
            <button onclick="history.back()" class="btn">⬅️ Voltar</button>
            <button onclick="location.reload()" class="btn">🔄 Recarregar</button>
        </div>
        
        <p><small>💡 <strong>Dica:</strong> Instale o VRS como app para melhor experiência offline!</small></p>
        
        <div id="autoRedirect" style="margin-top: 20px; font-size: 0.8rem;"></div>
    </div>
    
    <script>
        // Auto-redirect após alguns segundos
        let countdown = 5;
        const redirectDiv = document.getElementById('autoRedirect');
        
        function updateCountdown() {
            redirectDiv.innerHTML = 'Redirecionando para página principal em ' + countdown + 's...';
            countdown--;
            
            if (countdown < 0) {
                window.location.href = './inventario-rapido.html';
            } else {
                setTimeout(updateCountdown, 1000);
            }
        }
        
        // Iniciar countdown após 2 segundos
        setTimeout(updateCountdown, 2000);
        
        // Cancelar countdown se usuário interagir
        document.addEventListener('click', () => {
            redirectDiv.innerHTML = 'Redirecionamento cancelado.';
            countdown = -1;
        });
    </script>
</body>
</html>`;

  return new Response(html, {
    headers: { 'Content-Type': 'text/html; charset=utf-8' }
  });
}

// Gerenciar mensagens do cliente
self.addEventListener('message', (event) => {
  console.log('📨 Mensagem recebida:', event.data);
  
  if (event.data && event.data.type) {
    switch (event.data.type) {
      case 'SKIP_WAITING':
        self.skipWaiting();
        break;
        
      case 'CACHE_STATUS':
        caches.open(CACHE_NAME).then(cache => {
          cache.keys().then(keys => {
            event.ports[0].postMessage({
              type: 'CACHE_STATUS_RESPONSE',
              cached: keys.length,
              version: CACHE_VERSION
            });
          });
        });
        break;
        
      case 'CLEAR_CACHE':
        caches.delete(CACHE_NAME).then(() => {
          event.ports[0].postMessage({
            type: 'CACHE_CLEARED'
          });
        });
        break;
        
      case 'UPDATE_CACHE':
        updateCache().then(() => {
          event.ports[0].postMessage({
            type: 'CACHE_UPDATED'
          });
        });
        break;
    }
  }
});

// Atualizar cache manualmente
async function updateCache() {
  try {
    console.log('🔄 Atualizando cache...');
    const cache = await caches.open(CACHE_NAME);
    
    const updatePromises = CORE_FILES.map(async (url) => {
      try {
        const response = await fetch(url, { cache: 'no-cache' });
        if (response.ok) {
          await cache.put(url, response);
          console.log('✅ Atualizado:', url);
        }
      } catch (error) {
        console.warn('⚠️ Erro ao atualizar:', url, error);
      }
    });
    
    await Promise.allSettled(updatePromises);
    console.log('✅ Cache atualizado');
  } catch (error) {
    console.error('❌ Erro ao atualizar cache:', error);
  }
}

// Limpeza periódica de cache
self.addEventListener('periodicsync', (event) => {
  if (event.tag === 'cache-cleanup') {
    event.waitUntil(cleanupCache());
  }
});

async function cleanupCache() {
  try {
    const cache = await caches.open(CACHE_NAME);
    const keys = await cache.keys();
    
    // Remover itens antigos (mais de 7 dias)
    const oneWeekAgo = Date.now() - (7 * 24 * 60 * 60 * 1000);
    
    const cleanupPromises = keys.map(async (request) => {
      const response = await cache.match(request);
      if (response) {
        const dateHeader = response.headers.get('date');
        if (dateHeader) {
          const responseDate = new Date(dateHeader).getTime();
          if (responseDate < oneWeekAgo) {
            await cache.delete(request);
            console.log('🗑️ Removido cache antigo:', request.url);
          }
        }
      }
    });
    
    await Promise.allSettled(cleanupPromises);
    console.log('✅ Limpeza de cache concluída');
  } catch (error) {
    console.error('❌ Erro na limpeza de cache:', error);
  }
}

// Notificações push (para futuro uso)
self.addEventListener('push', (event) => {
  console.log('📬 Notificação push recebida');
  
  const options = {
    body: 'Seus dados foram atualizados',
    icon: './manifest.json',
    badge: './manifest.json',
    tag: 'vrs-update',
    renotify: true,
    actions: [
      {
        action: 'open',
        title: 'Abrir Sistema'
      },
      {
        action: 'dismiss',
        title: 'Dispensar'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('Sistema VRS', options)
  );
});

// Clique em notificação
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  if (event.action === 'open') {
    event.waitUntil(
      clients.openWindow('./')
    );
  }
});

console.log('🚀 Service Worker VRS carregado - Versão', CACHE_VERSION);
