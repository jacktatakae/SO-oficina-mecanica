// Service Worker Universal para VRS
const CACHE_NAME = 'vrs-universal-v1.0.0';
const STATIC_CACHE = 'vrs-static-v1.0.0';
const DYNAMIC_CACHE = 'vrs-dynamic-v1.0.0';

// Recursos críticos que devem ser cacheados imediatamente
const CRITICAL_RESOURCES = [
    './vrs-universal.html',
    './manifest-universal.json',
    './scanner-visual.html',
    './inventario-rapido.html',
    './central-sistemas.html',
    './gerenciador-clientes.html',
    './identificacao-pecas.html',
    './qr-permanente.html'
];

// CDNs que devem ser cacheadas
const CDN_RESOURCES = [
    'https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.0/jquery.min.js'
];

// Instalação do Service Worker
self.addEventListener('install', event => {
    console.log('[SW] Instalando Service Worker Universal...');
    
    event.waitUntil(
        Promise.all([
            // Cache estático
            caches.open(STATIC_CACHE).then(cache => {
                console.log('[SW] Cacheando recursos críticos...');
                return cache.addAll(CRITICAL_RESOURCES.concat(CDN_RESOURCES))
                    .catch(error => {
                        console.warn('[SW] Alguns recursos falharam ao cachear:', error);
                        // Tentar cachear individualmente
                        return Promise.allSettled(
                            CRITICAL_RESOURCES.concat(CDN_RESOURCES).map(url => 
                                fetch(url)
                                    .then(response => {
                                        if (response.ok) {
                                            return cache.put(url, response);
                                        }
                                    })
                                    .catch(() => console.warn(`[SW] Falha ao cachear: ${url}`))
                            )
                        );
                    });
            }),
            
            // Forçar ativação imediata
            self.skipWaiting()
        ])
    );
});

// Ativação do Service Worker
self.addEventListener('activate', event => {
    console.log('[SW] Ativando Service Worker Universal...');
    
    event.waitUntil(
        Promise.all([
            // Limpar caches antigos
            caches.keys().then(cacheNames => {
                return Promise.all(
                    cacheNames.map(cacheName => {
                        if (cacheName !== STATIC_CACHE && 
                            cacheName !== DYNAMIC_CACHE && 
                            cacheName !== CACHE_NAME) {
                            console.log(`[SW] Removendo cache antigo: ${cacheName}`);
                            return caches.delete(cacheName);
                        }
                    })
                );
            }),
            
            // Tomar controle de todas as abas
            self.clients.claim()
        ])
    );
});

// Interceptação de requisições
self.addEventListener('fetch', event => {
    const request = event.request;
    const url = new URL(request.url);
    
    // Ignorar requisições não-HTTP
    if (!request.url.startsWith('http')) {
        return;
    }
    
    // Estratégia: Cache First para recursos estáticos
    if (isStaticResource(request)) {
        event.respondWith(cacheFirst(request));
        return;
    }
    
    // Estratégia: Network First para APIs e dados dinâmicos
    if (isDynamicResource(request)) {
        event.respondWith(networkFirst(request));
        return;
    }
    
    // Estratégia: Stale While Revalidate para recursos de CDN
    if (isCDNResource(request)) {
        event.respondWith(staleWhileRevalidate(request));
        return;
    }
    
    // Padrão: Network First
    event.respondWith(networkFirst(request));
});

// Verificar se é recurso estático
function isStaticResource(request) {
    const url = request.url;
    return url.includes('.html') || 
           url.includes('.css') || 
           url.includes('.js') || 
           url.includes('.json') ||
           url.includes('/assets/');
}

// Verificar se é recurso dinâmico
function isDynamicResource(request) {
    const url = request.url;
    return url.includes('/api/') || 
           url.includes('github.com/api/') ||
           request.method !== 'GET';
}

// Verificar se é recurso de CDN
function isCDNResource(request) {
    const url = request.url;
    return url.includes('cdnjs.cloudflare.com') ||
           url.includes('fonts.googleapis.com') ||
           url.includes('unpkg.com');
}

// Estratégia Cache First
async function cacheFirst(request) {
    try {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        const networkResponse = await fetch(request);
        
        if (networkResponse.ok) {
            const cache = await caches.open(STATIC_CACHE);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.error('[SW] Cache First falhou:', error);
        
        // Fallback para página offline se disponível
        if (request.destination === 'document') {
            const offlinePage = await caches.match('./offline.html');
            return offlinePage || new Response('Offline - VRS Universal', {
                status: 503,
                headers: { 'Content-Type': 'text/plain' }
            });
        }
        
        return new Response('Recurso indisponível offline', {
            status: 503,
            headers: { 'Content-Type': 'text/plain' }
        });
    }
}

// Estratégia Network First
async function networkFirst(request) {
    try {
        const networkResponse = await fetch(request);
        
        if (networkResponse.ok && request.method === 'GET') {
            const cache = await caches.open(DYNAMIC_CACHE);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.warn('[SW] Network falhou, tentando cache:', error);
        
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        throw error;
    }
}

// Estratégia Stale While Revalidate
async function staleWhileRevalidate(request) {
    const cache = await caches.open(STATIC_CACHE);
    const cachedResponse = await cache.match(request);
    
    const fetchPromise = fetch(request).then(networkResponse => {
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    }).catch(error => {
        console.warn('[SW] Revalidation falhou:', error);
        return cachedResponse;
    });
    
    return cachedResponse || fetchPromise;
}

// Mensagens do cliente
self.addEventListener('message', event => {
    const { type, data } = event.data;
    
    switch (type) {
        case 'SKIP_WAITING':
            self.skipWaiting();
            break;
            
        case 'GET_CACHE_STATUS':
            getCacheStatus().then(status => {
                event.ports[0].postMessage({ type: 'CACHE_STATUS', data: status });
            });
            break;
            
        case 'CLEAR_CACHE':
            clearAllCaches().then(() => {
                event.ports[0].postMessage({ type: 'CACHE_CLEARED' });
            });
            break;
            
        case 'FORCE_UPDATE':
            forceUpdate().then(() => {
                event.ports[0].postMessage({ type: 'UPDATE_COMPLETE' });
            });
            break;
    }
});

// Obter status do cache
async function getCacheStatus() {
    const cacheNames = await caches.keys();
    const status = {
        cacheNames,
        totalCaches: cacheNames.length,
        cacheSize: 0
    };
    
    for (const cacheName of cacheNames) {
        const cache = await caches.open(cacheName);
        const keys = await cache.keys();
        status.cacheSize += keys.length;
    }
    
    return status;
}

// Limpar todos os caches
async function clearAllCaches() {
    const cacheNames = await caches.keys();
    await Promise.all(cacheNames.map(name => caches.delete(name)));
    console.log('[SW] Todos os caches foram limpos');
}

// Forçar atualização
async function forceUpdate() {
    await clearAllCaches();
    
    // Recarregar recursos críticos
    const cache = await caches.open(STATIC_CACHE);
    await cache.addAll(CRITICAL_RESOURCES);
    
    console.log('[SW] Atualização forçada concluída');
}

// Sincronização em background
self.addEventListener('sync', event => {
    console.log('[SW] Background Sync:', event.tag);
    
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

async function doBackgroundSync() {
    console.log('[SW] Executando sincronização em background...');
    
    try {
        // Verificar se há dados pendentes para sincronizar
        const pendingData = await self.registration.sync.getTags();
        
        for (const tag of pendingData) {
            if (tag.startsWith('sync-')) {
                // Processar sincronização específica
                console.log(`[SW] Sincronizando: ${tag}`);
            }
        }
    } catch (error) {
        console.error('[SW] Erro na sincronização:', error);
    }
}

// Push notifications
self.addEventListener('push', event => {
    console.log('[SW] Push recebido:', event);
    
    const options = {
        body: event.data ? event.data.text() : 'Atualização do VRS Universal',
        icon: './assets/icon-192.png',
        badge: './assets/badge-72.png',
        vibrate: [100, 50, 100],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        }
    };
    
    event.waitUntil(
        self.registration.showNotification('VRS Universal', options)
    );
});

// Click em notificação
self.addEventListener('notificationclick', event => {
    console.log('[SW] Notificação clicada:', event);
    
    event.notification.close();
    
    event.waitUntil(
        self.clients.openWindow('./vrs-universal.html')
    );
});

console.log('[SW] Service Worker Universal carregado');
