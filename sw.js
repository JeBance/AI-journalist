/* ============================================
   AI Journalist -- Service Worker
   Lazy cache: articles.json fetched on-demand,
   not pre-cached (too large for mobile).
   ============================================ */

var CACHE_NAME = 'ai-journalist-v2';
var ASSETS_TO_CACHE = [
    '/',
    '/index.html',
    '/styles.css',
    '/app.js',
    '/manifest.json'
    // articles.json NOT pre-cached -- loaded on demand
];

// Install -- cache core assets only
self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                console.log('Caching core assets');
                return cache.addAll(ASSETS_TO_CACHE);
            })
            .catch(function(err) { console.log('Some assets not cached:', err); })
    );
    self.skipWaiting();
});

// Activate -- remove old caches
self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames
                    .filter(function(name) { return name !== CACHE_NAME; })
                    .map(function(name) { return caches.delete(name); })
            );
        })
    );
    self.clients.claim();
});

// Fetch -- network-first for articles.json, cache-first for rest
self.addEventListener('fetch', function(event) {
    if (event.request.url.endsWith('/articles.json')) {
        // Network-first for articles.json
        event.respondWith(
            fetch(event.request)
                .then(function(response) {
                    if (response.ok) {
                        var clone = response.clone();
                        caches.open(CACHE_NAME).then(function(cache) {
                            cache.put(event.request, clone);
                        });
                    }
                    return response;
                })
                .catch(function() { return caches.match(event.request); })
        );
        return;
    }

    // Cache-first for everything else
    event.respondWith(
        caches.match(event.request)
            .then(function(cached) {
                if (cached) return cached;

                return fetch(event.request).then(function(response) {
                    if (response.ok && event.request.url.indexOf(self.location.origin) === 0) {
                        var clone = response.clone();
                        caches.open(CACHE_NAME).then(function(cache) {
                            cache.put(event.request, clone);
                        });
                    }
                    return response;
                });
            })
    );
});
