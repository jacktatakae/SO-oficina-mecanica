// 🔄 SERVICE WORKER VRS - Funcionamento Offline
// Versão 2.0 - Compatibilidade Total entre Plataformas

const CACHE_NAME = 'vrs-catalogo-v2.0';
const CACHE_VERSION = '2025.08.01';

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
  './auto-backup-system.js',
  './ia-visual-radiadores.js',
  './manifest.json'
];

// Recursos externos (CDN) para cache
const EXTERNAL_RESOURCES = [
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
  'https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css',
  'https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js'
];

// URLs que devem sempre ser buscadas da rede
const NETWORK_FIRST = [
  '/api/',
  '.json'
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
    
    // Fallback para página offline
    if (request.destination === 'document') {
      const cache = await caches.open(CACHE_NAME);
      const fallback = await cache.match('./index.html');
      
      if (fallback) {
        return fallback;
      }
    }
    
    return new Response('Sistema offline - Recarregue quando conectado', { 
      status: 503,
      statusText: 'Service Unavailable',
      headers: { 'Content-Type': 'text/plain; charset=utf-8' }
    });
  }
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
