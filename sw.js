/* ============================================
   AI Journalist — Service Worker
   Кэширует всё для оффлайн работы
   ============================================ */

const CACHE_NAME = 'ai-journalist-v1';
const ASSETS_TO_CACHE = [
    '/',
    '/index.html',
    '/styles.css',
    '/app.js',
    '/manifest.json',
    '/articles.json'
];

// Установка — кэшируем основные файлы
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('✅ Кэширование основных файлов');
                return cache.addAll(ASSETS_TO_CACHE);
            })
            .catch((err) => console.log('⚠️ Не все файлы кэшированы:', err))
    );
    self.skipWaiting();
});

// Активация — удаляем старые кэши
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames
                    .filter((name) => name !== CACHE_NAME)
                    .map((name) => caches.delete(name))
            );
        })
    );
    self.clients.claim();
});

// Fetch — стратегия: сеть с fallback на кэш
self.addEventListener('fetch', (event) => {
    // articles.json — всегда пробуем сеть, но fallback на кэш
    if (event.request.url.endsWith('/articles.json')) {
        event.respondWith(
            fetch(event.request)
                .then((response) => {
                    // Обновляем кэш
                    const clonedResponse = response.clone();
                    caches.open(CACHE_NAME)
                        .then((cache) => cache.put(event.request, clonedResponse));
                    return response;
                })
                .catch(() => caches.match(event.request))
        );
        return;
    }
    
    // Остальные ресурсы — cache first
    event.respondWith(
        caches.match(event.request)
            .then((cached) => {
                if (cached) return cached;
                
                return fetch(event.request).then((response) => {
                    // Кэшируем только свои ресурсы
                    if (response.ok && event.request.url.startsWith(self.location.origin)) {
                        const clonedResponse = response.clone();
                        caches.open(CACHE_NAME)
                            .then((cache) => cache.put(event.request, clonedResponse));
                    }
                    return response;
                });
            })
    );
});
