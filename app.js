/* ============================================
   AI Journalist -- Application Logic
   ============================================ */

const ARTICLES_URL = '/articles.json';
const BATCH_SIZE = 20;

let allArticles = [];
let filteredArticles = [];
let displayedCount = 0;
let currentFilter = 'all';
let searchQuery = '';

// ====== INITIALIZATION ======

async function init() {
    try {
        const response = await fetch(ARTICLES_URL);
        if (!response.ok) throw new Error('Failed to load articles');

        allArticles = await response.json();
        filteredArticles = [...allArticles];

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
    const tagsHtml = article.tags.slice(0, 3).map(tag =>
        '<span class="card-tag">' + escapeHtml(tag) + '</span>'
    ).join('');

    const card = document.createElement('article');
    card.className = 'article-card';
    card.dataset.id = article.id;
    card.innerHTML =
        '<div class="card-header">' +
            '<span class="card-emoji">' + article.emoji + '</span>' +
            '<h3 class="card-title">' + escapeHtml(article.title) + '</h3>' +
        '</div>' +
        '<div class="card-meta">' +
            '<span class="card-date">' + formatDate(article.date) + '</span>' +
            '<span class="card-category">' + escapeHtml(article.category) + '</span>' +
        '</div>' +
        '<p class="card-description">' + escapeHtml(article.description) + '</p>' +
        '<div class="card-tags">' + tagsHtml + '</div>';

    card.addEventListener('click', function() { openArticle(article.id); });

    return card;
}

function renderBatch() {
    const grid = document.getElementById('articles-grid');

    if (displayedCount === 0) {
        grid.innerHTML = '';
    }

    const end = Math.min(displayedCount + BATCH_SIZE, filteredArticles.length);

    for (let i = displayedCount; i < end; i++) {
        grid.appendChild(renderArticleCard(filteredArticles[i]));
    }

    displayedCount = end;

    var endMessage = document.getElementById('end-message');
    if (displayedCount >= filteredArticles.length) {
        endMessage.style.display = 'block';
    } else {
        endMessage.style.display = 'none';
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
                a.description.toLowerCase().indexOf(q) !== -1;
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

// ====== INFINITE SCROLL ======

function setupInfiniteScroll() {
    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting && displayedCount < filteredArticles.length) {
                renderBatch();
            }
        });
    }, { rootMargin: '200px' });

    observer.observe(document.getElementById('end-message'));
}

// ====== ARTICLE MODAL ======

async function openArticle(id) {
    var article = allArticles.find(function(a) { return a.id === id; });
    if (!article) return;

    var modal = document.getElementById('article-modal');
    var body = document.getElementById('modal-body');

    body.innerHTML = '<div class="loading"><div class="spinner"></div><p>Loading article...</p></div>';
    modal.showModal();

    if (article.telegraph_url) {
        try {
            var path = article.telegraph_url.replace('https://telegra.ph/', '');
            var apiUrl = 'https://telegra.ph/api/getPage/' + path + '?return_content=true';

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
    } else {
        renderArticleFallback(article);
    }
}

function renderArticleContent(article, content) {
    var body = document.getElementById('modal-body');
    var htmlContent = '';

    if (Array.isArray(content)) {
        content.forEach(function(node) {
            htmlContent += telegraphNodeToHtml(node);
        });
    }

    var sourcesHtml = '';
    if (article.sources.length > 0) {
        sourcesHtml = '<div class="modal-sources"><h3>Sources</h3><ul>' +
            article.sources.map(function(s) {
                var urlMatch = s.match(/\((https?:\/\/[^)]+)\)/);
                if (urlMatch) {
                    var name = s.replace(/\s*\(.*\)/, '');
                    return '<li><a href="' + escapeHtml(urlMatch[1]) + '" target="_blank" rel="noopener">' + escapeHtml(name || s) + '</a></li>';
                }
                return '<li>' + escapeHtml(s) + '</li>';
            }).join('') + '</ul></div>';
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
        sourcesHtml +
        '<div class="modal-actions">' +
            (article.telegraph_url ? '<a href="' + escapeHtml(article.telegraph_url) + '" target="_blank" rel="noopener">Read on Telegra.ph</a>' : '') +
            '<a href="https://t.me/JeBanceOnline" target="_blank" rel="noopener" class="secondary">Telegram channel</a>' +
        '</div>';
}

function renderArticleFallback(article) {
    var body = document.getElementById('modal-body');

    var tagsHtml = article.tags.map(function(tag) {
        return '<span class="card-tag" style="display:inline-block;margin:0.25rem;">' + escapeHtml(tag) + '</span>';
    }).join('');

    var sourcesHtml = '';
    if (article.sources.length > 0) {
        sourcesHtml = '<div class="modal-sources"><h3>Sources</h3><ul>' +
            article.sources.map(function(s) {
                var urlMatch = s.match(/\((https?:\/\/[^)]+)\)/);
                if (urlMatch) {
                    var name = s.replace(/\s*\(.*\)/, '');
                    return '<li><a href="' + escapeHtml(urlMatch[1]) + '" target="_blank" rel="noopener">' + escapeHtml(name || s) + '</a></li>';
                }
                return '<li>' + escapeHtml(s) + '</li>';
            }).join('') + '</ul></div>';
    }

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
        sourcesHtml +
        '<div class="modal-actions">' +
            (article.telegraph_url ? '<a href="' + escapeHtml(article.telegraph_url) + '" target="_blank" rel="noopener">Read on Telegra.ph</a>' : '') +
            '<a href="https://t.me/JeBanceOnline" target="_blank" rel="noopener" class="secondary">Telegram channel</a>' +
        '</div>';
}

function telegraphNodeToHtml(node) {
    if (!node || !node.tag) return '';

    switch (node.tag) {
        case 'p':
            return '<p>' + processNodeContent(node.children || node) + '</p>';
        case 'h3':
        case 'h4':
            return '<h2>' + processNodeContent(node.children || node) + '</h2>';
        case 'ul':
            if (Array.isArray(node.children)) {
                var items = node.children.map(function(child) {
                    if (child.tag === 'li') return '<li>' + processNodeContent(child.children || child) + '</li>';
                    return '';
                }).join('');
                return '<ul>' + items + '</ul>';
            }
            return '<ul>' + processNodeContent(node) + '</ul>';
        case 'ol':
            if (Array.isArray(node.children)) {
                var items2 = node.children.map(function(child) {
                    if (child.tag === 'li') return '<li>' + processNodeContent(child.children || child) + '</li>';
                    return '';
                }).join('');
                return '<ol>' + items2 + '</ol>';
            }
            return '<ol>' + processNodeContent(node) + '</ol>';
        case 'a':
            return '<a href="' + escapeHtml((node.attrs && node.attrs.href) || '#') + '" target="_blank" rel="noopener">' + processNodeContent(node.children || node) + '</a>';
        case 'strong':
        case 'b':
            return '<strong>' + processNodeContent(node.children || node) + '</strong>';
        case 'em':
        case 'i':
            return '<em>' + processNodeContent(node.children || node) + '</em>';
        case 'code':
            return '<code>' + escapeHtml(processNodeContent(node.children || node)) + '</code>';
        case 'pre':
            return '<pre><code>' + escapeHtml(processNodeContent(node.children || node)) + '</code></pre>';
        case 'br':
            return '<br>';
        case 'blockquote':
            return '<blockquote>' + processNodeContent(node.children || node) + '</blockquote>';
        case 'figure':
            if (node.attrs && node.attrs.src) {
                var caption = node.children ? processNodeContent(node.children) : '';
                return '<figure><img src="' + escapeHtml(node.attrs.src) + '" alt="' + escapeHtml(caption) + '" loading="lazy">' + (caption ? '<figcaption>' + caption + '</figcaption>' : '') + '</figure>';
            }
            return processNodeContent(node.children || node);
        default:
            return processNodeContent(node.children || node);
    }
}

function processNodeContent(node) {
    if (typeof node === 'string') return node;
    if (Array.isArray(node)) return node.map(processNodeContent).join('');
    if (node.children) return node.children.map(processNodeContent).join('');
    if (typeof node === 'object' && node !== null) {
        var text = Object.values(node).filter(function(v) { return typeof v === 'string'; }).join(' ');
        return text || '';
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
        var latest = allArticles[0].date;
        document.getElementById('last-updated').textContent = formatDate(latest);
    }
}

// ====== SERVICE WORKER ======

function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js')
            .then(function(reg) { console.log('SW registered'); })
            .catch(function(err) { console.log('SW registration failed:', err); });
    }
}

// ====== START ======

document.addEventListener('DOMContentLoaded', init);
