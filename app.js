/* ============================================
   AI Journalist -- Application Logic
   Shows full article content from JSON
   Fixed infinite scroll
   ============================================ */

var ARTICLES_URL = '/articles.json';
var BATCH_SIZE = 30;

var allArticles = [];
var filteredArticles = [];
var displayedCount = 0;
var currentFilter = 'all';
var searchQuery = '';
var isLoading = false;

// ====== INITIALIZATION ======

async function init() {
    try {
        var response = await fetch(ARTICLES_URL);
        if (!response.ok) throw new Error('Failed to load articles');

        allArticles = await response.json();
        filteredArticles = allArticles.slice();

        updateArticleCount();
        renderFilters();
        renderBatch();
        setupInfiniteScroll();
        setupSearch();
        updateLastUpdated();
        registerServiceWorker();

    } catch (error) {
        document.getElementById('articles-grid').innerHTML =
            '<div class="no-results"><p>Error loading articles. Please refresh.</p></div>';
    }
}

// ====== RENDERING ======

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

    if (displayedCount === 0) {
        grid.innerHTML = '';
    }

    var end = Math.min(displayedCount + BATCH_SIZE, filteredArticles.length);

    for (var i = displayedCount; i < end; i++) {
        grid.appendChild(renderArticleCard(filteredArticles[i]));
    }

    displayedCount = end;
    isLoading = false;

    // Update footer message
    var footer = document.getElementById('end-message');
    if (displayedCount >= filteredArticles.length) {
        footer.style.display = 'block';
    } else {
        footer.style.display = 'none';
    }
}

// ====== FILTERS ======

function renderFilters() {
    var categories = {};

    allArticles.forEach(function(article) {
        var cat = article.category;
        categories[cat] = (categories[cat] || 0) + 1;
    });

    var sorted = Object.entries(categories).sort(function(a, b) { return b[1] - a[1]; });

    var container = document.getElementById('filters');
    container.innerHTML = '<button class="filter-btn active" data-category="all">All (' + allArticles.length + ')</button>';

    sorted.forEach(function(entry) {
        var cat = entry[0];
        var count = entry[1];
        var btn = document.createElement('button');
        btn.className = 'filter-btn';
        btn.dataset.category = cat;
        btn.textContent = cat + ' (' + count + ')';
        btn.addEventListener('click', function() { setFilter(cat); });
        container.appendChild(btn);
    });
}

function setFilter(category) {
    currentFilter = category;
    applyFilters();

    document.querySelectorAll('.filter-btn').forEach(function(btn) {
        btn.classList.toggle('active', btn.dataset.category === category);
    });
}

function applyFilters() {
    filteredArticles = allArticles.slice();

    if (currentFilter !== 'all') {
        filteredArticles = filteredArticles.filter(function(a) { return a.category === currentFilter; });
    }

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
        document.getElementById('articles-grid').innerHTML =
            '<div class="no-results"><p>No results found</p><p>Try changing filters</p></div>';
        document.getElementById('end-message').style.display = 'none';
    } else {
        renderBatch();
    }

    updateArticleCount();
}

// ====== SEARCH ======

function setupSearch() {
    var input = document.getElementById('search');
    var debounceTimer;

    input.addEventListener('input', function(e) {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(function() {
            searchQuery = e.target.value.trim();
            applyFilters();
        }, 250);
    });
}

// ====== INFINITE SCROLL (fixed) ======

function setupInfiniteScroll() {
    // Observe the grid itself -- load more when bottom enters viewport
    var sentinel = document.createElement('div');
    sentinel.id = 'scroll-sentinel';
    sentinel.style.height = '1px';
    document.getElementById('articles-grid').after(sentinel);

    var observer = new IntersectionObserver(function(entries) {
        if (entries[0].isIntersecting && displayedCount < filteredArticles.length) {
            renderBatch();
        }
    }, { rootMargin: '400px' });

    observer.observe(sentinel);
}

// ====== ARTICLE MODAL ======

function openArticle(id) {
    var article = allArticles.find(function(a) { return a.id === id; });
    if (!article) return;

    var modal = document.getElementById('article-modal');
    var body = document.getElementById('modal-body');

    if (article.content) {
        renderArticleFromContent(article);
    } else if (article.telegraph_url) {
        body.innerHTML = '<div class="loading"><div class="spinner"></div><p>Loading from Telegra.ph...</p></div>';
        modal.showModal();
        loadFromTelegraph(article);
    } else {
        renderArticleFallback(article);
    }

    if (!document.getElementById('article-modal').open) {
        modal.showModal();
    }
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
    } catch (e) {
        renderArticleFallback(article);
    }
}

function renderArticleFromContent(article) {
    var modal = document.getElementById('article-modal');
    var body = document.getElementById('modal-body');

    var html = markdownToHtml(article.content);
    var sourcesHtml = buildSourcesHtml(article);

    body.innerHTML =
        '<div class="modal-header">' +
            '<h1 class="modal-title">' + article.emoji + ' ' + escapeHtml(article.title) + '</h1>' +
            '<div class="modal-meta">' +
                '<span>' + formatDate(article.date) + '</span>' +
                '<span>' + escapeHtml(article.category) + '</span>' +
            '</div>' +
        '</div>' +
        '<div class="modal-body">' + html + '</div>' +
        sourcesHtml +
        '<div class="modal-actions">' +
            (article.telegraph_url ? '<a href="' + escapeHtml(article.telegraph_url) + '" target="_blank" rel="noopener">Read on Telegra.ph</a>' : '') +
            '<a href="https://t.me/JeBanceOnline" target="_blank" rel="noopener" class="secondary">Telegram channel</a>' +
        '</div>';

    modal.showModal();
}

function renderArticleContent(article, content) {
    var body = document.getElementById('modal-body');
    var htmlContent = '';

    if (Array.isArray(content)) {
        content.forEach(function(node) {
            htmlContent += telegraphNodeToHtml(node);
        });
    }

    body.innerHTML =
        '<div class="modal-header">' +
            '<h1 class="modal-title">' + article.emoji + ' ' + escapeHtml(article.title) + '</h1>' +
            '<div class="modal-meta">' +
                '<span>' + formatDate(article.date) + '</span>' +
                '<span>' + escapeHtml(article.category) + '</span>' +
            '</div>' +
        '</div>' +
        '<div class="modal-body">' + htmlContent + '</div>' +
        buildSourcesHtml(article) +
        '<div class="modal-actions">' +
            (article.telegraph_url ? '<a href="' + escapeHtml(article.telegraph_url) + '" target="_blank" rel="noopener">Read on Telegra.ph</a>' : '') +
            '<a href="https://t.me/JeBanceOnline" target="_blank" rel="noopener" class="secondary">Telegram channel</a>' +
        '</div>';
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
            '<div class="modal-meta">' +
                '<span>' + formatDate(article.date) + '</span>' +
                '<span>' + escapeHtml(article.category) + '</span>' +
            '</div>' +
            '<div class="card-tags" style="margin-top:0.75rem;">' + tagsHtml + '</div>' +
        '</div>' +
        '<div class="modal-body">' +
            '<p>' + escapeHtml(article.description) + '</p>' +
            '<p>Full article available via link below.</p>' +
        '</div>' +
        buildSourcesHtml(article) +
        '<div class="modal-actions">' +
            (article.telegraph_url ? '<a href="' + escapeHtml(article.telegraph_url) + '" target="_blank" rel="noopener">Read on Telegra.ph</a>' : '') +
            '<a href="https://t.me/JeBanceOnline" target="_blank" rel="noopener" class="secondary">Telegram channel</a>' +
        '</div>';

    modal.showModal();
}

function buildSourcesHtml(article) {
    if (!article.sources || article.sources.length === 0) return '';
    return '<div class="modal-sources"><h3>Sources</h3><ul>' +
        article.sources.map(function(s) {
            var urlMatch = s.match(/\((https?:\/\/[^)]+)\)/);
            if (urlMatch) {
                var name = s.replace(/\s*\(.*\)/, '');
                return '<li><a href="' + escapeHtml(urlMatch[1]) + '" target="_blank" rel="noopener">' + escapeHtml(name || s) + '</a></li>';
            }
            return '<li>' + escapeHtml(s) + '</li>';
        }).join('') + '</ul></div>';
}

// ====== MARKDOWN TO HTML ======

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

// ====== TELEGRAPH NODE TO HTML ======

function telegraphNodeToHtml(node) {
    if (!node || !node.tag) return '';
    switch (node.tag) {
        case 'p': return '<p>' + processNodeContent(node.children || node) + '</p>';
        case 'h3': case 'h4': return '<h2>' + processNodeContent(node.children || node) + '</h2>';
        case 'ul':
            if (Array.isArray(node.children)) {
                return '<ul>' + node.children.map(function(c) {
                    return c.tag === 'li' ? '<li>' + processNodeContent(c.children || c) + '</li>' : '';
                }).join('') + '</ul>';
            }
            return '<ul>' + processNodeContent(node) + '</ul>';
        case 'ol':
            if (Array.isArray(node.children)) {
                return '<ol>' + node.children.map(function(c) {
                    return c.tag === 'li' ? '<li>' + processNodeContent(c.children || c) + '</li>' : '';
                }).join('') + '</ol>';
            }
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
    if (typeof node === 'object' && node !== null) {
        return Object.values(node).filter(function(v) { return typeof v === 'string'; }).join(' ');
    }
    return String(node || '');
}

// ====== CLOSE MODAL ======

document.getElementById('close-modal').addEventListener('click', function() {
    document.getElementById('article-modal').close();
});

document.getElementById('article-modal').addEventListener('click', function(e) {
    if (e.target === document.getElementById('article-modal')) {
        document.getElementById('article-modal').close();
    }
});

// ====== HELPERS ======

function escapeHtml(text) {
    var div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateStr) {
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var date = new Date(dateStr);
    return date.getDate() + ' ' + months[date.getMonth()] + ' ' + date.getFullYear();
}

function updateArticleCount() {
    document.getElementById('article-count').textContent = filteredArticles.length;
}

function updateLastUpdated() {
    if (allArticles.length > 0) {
        document.getElementById('last-updated').textContent = formatDate(allArticles[0].date);
    }
}

function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js')
            .then(function() { console.log('SW registered'); })
            .catch(function(err) { console.log('SW registration failed:', err); });
    }
}

document.addEventListener('DOMContentLoaded', init);
