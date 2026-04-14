/* ============================================
   AI Journalist — IndexedDB cache
   Кэширует articles.json для мгновенной загрузки
   ============================================ */

var DB_NAME = 'ai-journalist-db';
var DB_VERSION = 1;
var STORE_NAME = 'articles';
var CACHE_KEY = 'articles-data';
var META_KEY = 'articles-meta';

function openDB() {
    return new Promise(function(resolve, reject) {
        var request = indexedDB.open(DB_NAME, DB_VERSION);
        request.onupgradeneeded = function(e) {
            var db = e.target.result;
            if (!db.objectStoreNames.contains(STORE_NAME)) {
                db.createObjectStore(STORE_NAME);
            }
        };
        request.onsuccess = function(e) { resolve(e.target.result); };
        request.onerror = function(e) { reject(e.target.error); };
    });
}

function getFromCache() {
    return openDB().then(function(db) {
        return new Promise(function(resolve, reject) {
            var tx = db.transaction(STORE_NAME, 'readonly');
            var store = tx.objectStore(STORE_NAME);
            var dataReq = store.get(CACHE_KEY);
            var metaReq = store.get(META_KEY);
            var data = null;
            var meta = null;
            dataReq.onsuccess = function() { data = dataReq.result; };
            metaReq.onsuccess = function() { meta = metaReq.result; };
            tx.oncomplete = function() { resolve({ data: data, meta: meta }); };
            tx.onerror = function() { reject(tx.error); };
        });
    }).catch(function() { return { data: null, meta: null }; });
}

function saveToCache(articles) {
    return openDB().then(function(db) {
        return new Promise(function(resolve, reject) {
            var tx = db.transaction(STORE_NAME, 'readwrite');
            var store = tx.objectStore(STORE_NAME);
            var meta = {
                savedAt: Date.now(),
                count: articles.length,
                lastDate: articles.length > 0 ? articles[0].date : null,
                version: 1
            };
            store.put(articles, CACHE_KEY);
            store.put(meta, META_KEY);
            tx.oncomplete = function() { resolve(meta); };
            tx.onerror = function() { reject(tx.error); };
        });
    }).catch(function() { return null; });
}

function fetchArticles() {
    return fetch(ARTICLES_URL).then(function(response) {
        if (!response.ok) throw new Error('Network error');
        return response.json();
    });
}

async function loadArticles() {
    // 1. Попробуем из кэша
    var cached = await getFromCache();

    if (cached.data && cached.data.length > 0) {
        // Есть кэш — показываем сразу
        var isStale = !cached.meta || (Date.now() - cached.meta.savedAt) > 30 * 60 * 1000; // 30 мин

        if (!isStale) {
            // Кэш свежий — используем его
            return { articles: cached.data, source: 'cache', fresh: true };
        }

        // Кэш старый — показываем его пока грузим с сервера
        var cachedArticles = cached.data;

        // Загружаем с сервера в фоне
        try {
            var fresh = await fetchArticles();
            await saveToCache(fresh);
            return { articles: fresh, source: 'network', fresh: true, cachedArticles: cachedArticles };
        } catch (e) {
            // Сервер недоступен — используем кэш
            return { articles: cachedArticles, source: 'cache', fresh: false };
        }
    }

    // Кэша нет — грузим с сервера
    try {
        var articles = await fetchArticles();
        await saveToCache(articles);
        return { articles: articles, source: 'network', fresh: true };
    } catch (e) {
        return { articles: [], source: 'error' };
    }
}
