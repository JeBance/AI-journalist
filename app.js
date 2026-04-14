/* ============================================
   AI Journalist — Логика приложения
   С IndexedDB кэшированием
   ============================================ */

var ARTICLES_URL = '/articles.json';
var BATCH_SIZE = 30;

var allArticles = [];
var filteredArticles = [];
var displayedCount = 0;
var currentFilter = 'all';
var searchQuery = '';
var isLoading = false;

// ====== ТЕМА ======

function initTheme() {
    var saved = localStorage.getItem('theme');
    if (saved) document.documentElement.setAttribute('data-theme', saved);
    updateThemeIcon();
}

function toggleTheme() {
    var current = document.documentElement.getAttribute('data-theme');
    var next = current === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    updateThemeIcon();
}

function updateThemeIcon() {
    var btn = document.getElementById('theme-toggle');
    if (!btn) return;
    var isLight = document.documentElement.getAttribute('data-theme') === 'light';
    btn.textContent = isLight ? '🌙' : '☀️';
    btn.title = isLight ? 'Включить тёмную тему' : 'Включить светлую тему';
}

// ====== МОБИЛЬНЫЙ DRAWER ======

function openFilterDrawer() {
    var overlay = document.getElementById('filter-overlay');
    if (overlay) overlay.classList.add('open');
}

function closeFilterDrawer() {
    var overlay = document.getElementById('filter-overlay');
    if (overlay) overlay.classList.remove('open');
}

function setupFilterDrawer() {
    var btn = document.getElementById('filter-toggle-btn');
    var closeBtn = document.getElementById('filter-close-btn');
    var overlay = document.getElementById('filter-overlay');
    if (btn) btn.addEventListener('click', openFilterDrawer);
    if (closeBtn) closeBtn.addEventListener('click', closeFilterDrawer);
    if (overlay) overlay.addEventListener('click', function(e) { if (e.target === overlay) closeFilterDrawer(); });
}

// ====== ИНИЦИАЛИЗАЦИЯ ======

async function init() {
    initTheme();
    setupFilterDrawer();

    // Показываем статус загрузки
    var grid = document.getElementById('articles-grid');
    grid.innerHTML = '<div class="loading"><div class="spinner"></div><p>Загрузка статей...</p></div>';

    // Загружаем статьи (IndexedDB → сеть)
    var result = await loadArticles();

    if (result.source === 'error') {
        grid.innerHTML = '<div class="no-results"><p>Ошибка загрузки. Обновите страницу.</p></div>';
        return;
    }

    allArticles = result.articles;
    filteredArticles = allArticles.slice();

    // Показываем откуда загрузили
    if (result.source === 'cache' && result.fresh) {
        console.log('📦 Загружено из кэша IndexedDB (' + allArticles.length + ' статей)');
    } else if (result.source === 'network') {
        console.log('🌐 Загружено с сервера (' + allArticles.length + ' статей)');
    }

    updateArticleCount();
    renderFilters();
    renderBatch();
    setupInfiniteScroll();
    setupSearch();
    updateLastUpdated();
    registerServiceWorker();
}

// ====== РЕНДЕР КАРТОЧЕК ======

function renderArticleCard(article) {
    var tagsHtml = article.tags.slice(0, 3).map(function(tag) {
        return '<span class="card-tag">' + escapeHtml(tag) + '</span>';
    }).join('');
    var card = document.createElement('article');
    card.className = 'article-card';
    card.dataset.id = article.id;
    var header = document.createElement('div');
    header.className = 'card-header';
    var emoji = document.createElement('span');
    emoji.className = 'card-emoji';
    emoji.textContent = article.emoji;
    var h3 = document.createElement('h3');
    h3.className = 'card-title';
    h3.textContent = article.title;
    header.appendChild(emoji);
    header.appendChild(h3);
    var meta = document.createElement('div');
    meta.className = 'card-meta';
    var dateSpan = document.createElement('span');
    dateSpan.textContent = formatDate(article.date);
    var catSpan = document.createElement('span');
    catSpan.className = 'card-category';
    catSpan.textContent = article.category;
    meta.appendChild(dateSpan);
    meta.appendChild(catSpan);
    var desc = document.createElement('p');
    desc.className = 'card-description';
    desc.textContent = article.description;
    var tagsDiv = document.createElement('div');
    tagsDiv.className = 'card-tags';
    tagsDiv.innerHTML = tagsHtml;
    card.appendChild(header);
    card.appendChild(meta);
    card.appendChild(desc);
    card.appendChild(tagsDiv);
    card.addEventListener('click', function() { openArticle(article.id); });
    return card;
}

function renderBatch() {
    if (isLoading) return;
    isLoading = true;
    var grid = document.getElementById('articles-grid');
    if (displayedCount === 0) grid.innerHTML = '';
    var end = Math.min(displayedCount + BATCH_SIZE, filteredArticles.length);
    for (var i = displayedCount; i < end; i++) {
        grid.appendChild(renderArticleCard(filteredArticles[i]));
    }
    displayedCount = end;
    isLoading = false;
}

// ====== ФИЛЬТРЫ ======

function buildFilterButtons() {
    var categories = {};
    allArticles.forEach(function(article) { categories[article.category] = (categories[article.category] || 0) + 1; });
    var sorted = Object.entries(categories).sort(function(a, b) { return b[1] - a[1]; });
    var html = '<button class="filter-btn active" data-category="all"><span>Все</span><span class="count">' + allArticles.length + '</span></button>';
    sorted.forEach(function(entry) {
        html += '<button class="filter-btn" data-category="' + escapeHtml(entry[0]) + '"><span>' + escapeHtml(entry[0]) + '</span><span class="count">' + entry[1] + '</span></button>';
    });
    return html;
}

function setupFilterEvents(container) {
    if (!container) return;
    container.querySelectorAll('.filter-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            currentFilter = btn.dataset.category;
            applyFilters();
            document.querySelectorAll('.filter-btn').forEach(function(b) {
                b.classList.toggle('active', b.dataset.category === currentFilter);
            });
            closeFilterDrawer();
        });
    });
}

function renderFilters() {
    var html = buildFilterButtons();
    var desktop = document.getElementById('filters-desktop');
    if (desktop) { desktop.innerHTML = html; setupFilterEvents(desktop); }
    var drawer = document.getElementById('filters-drawer');
    if (drawer) { drawer.innerHTML = html; setupFilterEvents(drawer); }
}

function applyFilters() {
    filteredArticles = allArticles.slice();
    if (currentFilter !== 'all') filteredArticles = filteredArticles.filter(function(a) { return a.category === currentFilter; });
    if (searchQuery) {
        var q = searchQuery.toLowerCase();
        filteredArticles = filteredArticles.filter(function(a) {
            return a.title.toLowerCase().indexOf(q) !== -1 ||
                a.tags.some(function(t) { return t.toLowerCase().indexOf(q) !== -1; }) ||
                a.category.toLowerCase().indexOf(q) !== -1 ||
                a.description.toLowerCase().indexOf(q) !== -1 ||
                (a.content && a.content.toLowerCase().indexOf(q) !== -1);
        });
    }
    displayedCount = 0;
    document.getElementById('articles-grid').innerHTML = '';
    if (filteredArticles.length === 0) {
        document.getElementById('articles-grid').innerHTML = '<div class="no-results"><p>Ничего не найдено</p><p>Попробуйте изменить фильтры или запрос</p></div>';
    } else {
        renderBatch();
    }
    updateArticleCount();
}

// ====== ПОИСК ======

function setupSearch() {
    var inputs = [document.getElementById('search-desktop'), document.getElementById('search-mobile'), document.getElementById('search-drawer')];
    inputs.forEach(function(input) {
        if (!input) return;
        var debounceTimer;
        input.addEventListener('input', function(e) {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(function() {
                searchQuery = e.target.value.trim();
                inputs.forEach(function(other) { if (other && other !== input) other.value = searchQuery; });
                applyFilters();
            }, 250);
        });
    });
}

// ====== БЕСКОНЕЧНЫЙ СКРОЛЛ ======

function setupInfiniteScroll() {
    var sentinel = document.createElement('div');
    sentinel.id = 'scroll-sentinel';
    sentinel.style.height = '1px';
    document.getElementById('articles-grid').after(sentinel);
    new IntersectionObserver(function(entries) {
        if (entries[0].isIntersecting && displayedCount < filteredArticles.length) renderBatch();
    }, { rootMargin: '400px' }).observe(sentinel);
}

// ====== МОДАЛЬНОЕ ОКНО ======

function openArticle(id) {
    var article = allArticles.find(function(a) { return a.id === id; });
    if (!article) return;
    var modal = document.getElementById('article-modal');
    var body = document.getElementById('modal-body');
    if (article.content) {
        renderArticleFromContent(article);
    } else if (article.telegraph_url) {
        body.innerHTML = '<div class="loading"><div class="spinner"></div><p>Загрузка с Telegra.ph...</p></div>';
        modal.showModal();
        loadFromTelegraph(article);
    } else {
        renderArticleFallback(article);
    }
    if (!document.getElementById('article-modal').open) modal.showModal();
}

async function loadFromTelegraph(article) {
    var body = document.getElementById('modal-body');
    try {
        var path = article.telegraph_url.replace('https://telegra.ph/', '');
        var apiUrl = 'https://api.telegra.ph/getPage/' + path + '?return_content=true';
        var response = await fetch(apiUrl);
        var data = await response.json();
        if (data.ok && data.result && data.result.content) {
            renderArticleContent(article, data.result.content);
        } else {
            renderArticleFallback(article);
        }
    } catch (e) { renderArticleFallback(article); }
}

function buildModalActions(article) {
    var actions = '<div class="modal-actions">';
    if (article.telegraph_url) actions += '<a href="' + escapeHtml(article.telegraph_url) + '" target="_blank" rel="noopener">📰 Telegra.ph</a>';
    actions += '<a href="https://t.me/JeBanceOnline" target="_blank" rel="noopener" class="secondary">💬 Telegram канал</a>';
    actions += '</div>';
    return actions;
}

function renderArticleFromContent(article) {
    var modal = document.getElementById('article-modal');
    var body = document.getElementById('modal-body');
    var html = markdownToHtml(article.content);
    body.innerHTML =
        '<div class="modal-header">' +
            '<h1 class="modal-title">' + article.emoji + ' ' + escapeHtml(article.title) + '</h1>' +
            '<div class="modal-meta"><span>📅 ' + formatDate(article.date) + '</span><span>📂 ' + escapeHtml(article.category) + '</span></div>' +
        '</div>' +
        '<div class="modal-body">' + html + '</div>' +
        buildModalActions(article);
    modal.showModal();
}

function renderArticleContent(article, content) {
    var body = document.getElementById('modal-body');
    var htmlContent = '';
    if (Array.isArray(content)) content.forEach(function(node) { htmlContent += telegraphNodeToHtml(node); });
    body.innerHTML =
        '<div class="modal-header">' +
            '<h1 class="modal-title">' + article.emoji + ' ' + escapeHtml(article.title) + '</h1>' +
            '<div class="modal-meta"><span>📅 ' + formatDate(article.date) + '</span><span>📂 ' + escapeHtml(article.category) + '</span></div>' +
        '</div>' +
        '<div class="modal-body">' + htmlContent + '</div>' +
        buildModalActions(article);
}

function renderArticleFallback(article) {
    var modal = document.getElementById('article-modal');
    var body = document.getElementById('modal-body');
    var tagsHtml = article.tags.map(function(tag) {
        return '<span class="card-tag" style="display:inline-block;margin:0.25rem;">' + escapeHtml(tag) + '</span>';
    }).join('');
    body.innerHTML =
        '<div class="modal-header">' +
            '<h1 class="modal-title">' + article.emoji + ' ' + escapeHtml(article.title) + '</h1>' +
            '<div class="modal-meta"><span>📅 ' + formatDate(article.date) + '</span><span>📂 ' + escapeHtml(article.category) + '</span></div>' +
            '<div class="card-tags" style="margin-top:0.75rem;">' + tagsHtml + '</div>' +
        '</div>' +
        '<div class="modal-body"><p>' + escapeHtml(article.description) + '</p><p>Полная статья доступна по ссылке ниже.</p></div>' +
        buildModalActions(article);
    modal.showModal();
}

// ====== MARKDOWN В HTML ======

function markdownToHtml(md) {
    if (!md) return '';
    var lines = md.split('\n');
    var html = '';
    var inList = false;
    var inOl = false;
    for (var i = 0; i < lines.length; i++) {
        var line = lines[i];
        if (line.match(/^#{1,3}\s+/)) {
            if (inList) { html += '</ul>'; inList = false; }
            if (inOl) { html += '</ol>'; inOl = false; }
            var level = line.match(/^(#{1,3})/)[1].length;
            html += '<h' + (level + 1) + '>' + inlineFormat(line.replace(/^#{1,3}\s+/, '')) + '</h' + (level + 1) + '>';
        } else if (line.match(/^[-*]\s+/)) {
            if (inOl) { html += '</ol>'; inOl = false; }
            if (!inList) { html += '<ul>'; inList = true; }
            html += '<li>' + inlineFormat(line.replace(/^[-*]\s+/, '')) + '</li>';
        } else if (line.match(/^\d+\.\s+/)) {
            if (inList) { html += '</ul>'; inList = false; }
            if (!inOl) { html += '<ol>'; inOl = true; }
            html += '<li>' + inlineFormat(line.replace(/^\d+\.\s+/, '')) + '</li>';
        } else if (line.match(/^---+$/)) {
            if (inList) { html += '</ul>'; inList = false; }
            if (inOl) { html += '</ol>'; inOl = false; }
            html += '<hr>';
        } else if (line.trim() === '') {
            if (inList) { html += '</ul>'; inList = false; }
            if (inOl) { html += '</ol>'; inOl = false; }
        } else {
            if (inList) { html += '</ul>'; inList = false; }
            if (inOl) { html += '</ol>'; inOl = false; }
            html += '<p>' + inlineFormat(line) + '</p>';
        }
    }
    if (inList) html += '</ul>';
    if (inOl) html += '</ol>';
    return html;
}

function inlineFormat(text) {
    text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/_(.+?)_/g, '<em>$1</em>');
    text = text.replace(/`(.+?)`/g, '<code>$1</code>');
    text = text.replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
    return text;
}

// ====== TELEGRAPH NODE В HTML ======

function telegraphNodeToHtml(node) {
    if (!node || !node.tag) return '';
    switch (node.tag) {
        case 'p': return '<p>' + processNodeContent(node.children || node) + '</p>';
        case 'h3': case 'h4': return '<h2>' + processNodeContent(node.children || node) + '</h2>';
        case 'ul':
            if (Array.isArray(node.children)) return '<ul>' + node.children.map(function(c) { return c.tag === 'li' ? '<li>' + processNodeContent(c.children || c) + '</li>' : ''; }).join('') + '</ul>';
            return '<ul>' + processNodeContent(node) + '</ul>';
        case 'ol':
            if (Array.isArray(node.children)) return '<ol>' + node.children.map(function(c) { return c.tag === 'li' ? '<li>' + processNodeContent(c.children || c) + '</li>' : ''; }).join('') + '</ol>';
            return '<ol>' + processNodeContent(node) + '</ol>';
        case 'a': return '<a href="' + escapeHtml((node.attrs && node.attrs.href) || '#') + '" target="_blank" rel="noopener">' + processNodeContent(node.children || node) + '</a>';
        case 'strong': case 'b': return '<strong>' + processNodeContent(node.children || node) + '</strong>';
        case 'em': case 'i': return '<em>' + processNodeContent(node.children || node) + '</em>';
        case 'code': return '<code>' + escapeHtml(processNodeContent(node.children || node)) + '</code>';
        case 'pre': return '<pre><code>' + escapeHtml(processNodeContent(node.children || node)) + '</code></pre>';
        case 'br': return '<br>';
        case 'blockquote': return '<blockquote>' + processNodeContent(node.children || node) + '</blockquote>';
        case 'figure':
            if (node.attrs && node.attrs.src) {
                var caption = node.children ? processNodeContent(node.children) : '';
                return '<figure><img src="' + escapeHtml(node.attrs.src) + '" alt="' + escapeHtml(caption) + '" loading="lazy">' + (caption ? '<figcaption>' + caption + '</figcaption>' : '') + '</figure>';
            }
            return processNodeContent(node.children || node);
        default: return processNodeContent(node.children || node);
    }
}

function processNodeContent(node) {
    if (typeof node === 'string') return node;
    if (Array.isArray(node)) return node.map(processNodeContent).join('');
    if (node && node.children) return node.children.map(processNodeContent).join('');
    if (typeof node === 'object' && node !== null) return Object.values(node).filter(function(v) { return typeof v === 'string'; }).join(' ');
    return String(node || '');
}

// ====== ЗАКРЫТЬ МОДАЛКУ ======

document.getElementById('close-modal').addEventListener('click', function() { document.getElementById('article-modal').close(); });
document.getElementById('article-modal').addEventListener('click', function(e) { if (e.target === document.getElementById('article-modal')) document.getElementById('article-modal').close(); });
document.getElementById('theme-toggle').addEventListener('click', toggleTheme);

// ====== ВСПОМОГАТЕЛЬНЫЕ ======

function escapeHtml(text) { var div = document.createElement('div'); div.textContent = text; return div.innerHTML; }

function formatDate(dateStr) {
    var months = ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек'];
    var date = new Date(dateStr);
    return date.getDate() + ' ' + months[date.getMonth()] + ' ' + date.getFullYear();
}

function updateArticleCount() { document.getElementById('article-count').textContent = filteredArticles.length; }

function updateLastUpdated() {
    if (allArticles.length > 0) document.getElementById('last-updated').textContent = formatDate(allArticles[0].date);
}

function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js')
            .then(function() { console.log('SW зарегистрирован'); })
            .catch(function(err) { console.log('SW ошибка:', err); });
    }
}

document.addEventListener('DOMContentLoaded', init);
