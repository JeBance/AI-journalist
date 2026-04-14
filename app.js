/* ============================================
   AI Journalist — Application Logic
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
        if (!response.ok) throw new Error('Не удалось загрузить статьи');
        
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
        document.getElementById('articles-grid').innerHTML = `
            <div class="no-results">
                <p>❌ Ошибка загрузки: ${error.message}</p>
                <p>Попробуйте обновить страницу</p>
            </div>
        `;
    }
}

// ====== RENDERING ======

function renderArticleCard(article) {
    const tagsHtml = article.tags.slice(0, 3).map(tag => 
        `<span class="card-tag">${escapeHtml(tag)}</span>`
    ).join('');
    
    return `
        <article class="article-card" data-id="${article.id}" onclick="openArticle(${article.id})">
            <div class="card-header">
                <span class="card-emoji">${article.emoji}</span>
                <h3 class="card-title">${escapeHtml(article.title)}</h3>
            </div>
            <div class="card-meta">
                <span class="card-date">📅 ${formatDate(article.date)}</span>
                <span class="card-category">${escapeHtml(article.category)}</span>
            </div>
            <p class="card-description">${escapeHtml(article.description)}</p>
            <div class="card-tags">${tagsHtml}</div>
        </article>
    `;
}

function renderBatch() {
    const grid = document.getElementById('articles-grid');
    
    if (displayedCount === 0) {
        grid.innerHTML = '';
    }
    
    const end = Math.min(displayedCount + BATCH_SIZE, filteredArticles.length);
    const fragment = document.createDocumentFragment();
    const tempDiv = document.createElement('div');
    
    for (let i = displayedCount; i < end; i++) {
        tempDiv.innerHTML = renderArticleCard(filteredArticles[i]);
        fragment.appendChild(tempDiv.firstElementChild);
    }
    
    grid.appendChild(fragment);
    displayedCount = end;
    
    // Показываем "все загружены" если конец
    const endMessage = document.getElementById('end-message');
    if (displayedCount >= filteredArticles.length) {
        endMessage.style.display = 'block';
    } else {
        endMessage.style.display = 'none';
    }
}

// ====== FILTERS ======

function renderFilters() {
    const categories = {};
    
    allArticles.forEach(article => {
        const cat = article.category;
        categories[cat] = (categories[cat] || 0) + 1;
    });
    
    const sorted = Object.entries(categories).sort((a, b) => b[1] - a[1]);
    
    const container = document.getElementById('filters');
    // Сохранем "Все" кнопку
    container.innerHTML = `<button class="filter-btn active" data-category="all">Все (${allArticles.length})</button>`;
    
    sorted.forEach(([cat, count]) => {
        const btn = document.createElement('button');
        btn.className = 'filter-btn';
        btn.dataset.category = cat;
        btn.textContent = `${cat} (${count})`;
        btn.addEventListener('click', () => setFilter(cat));
        container.appendChild(btn);
    });
}

function setFilter(category) {
    currentFilter = category;
    applyFilters();
    
    // Обновляем активную кнопку
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.category === category);
    });
}

function applyFilters() {
    filteredArticles = allArticles;
    
    // Фильтр по категории
    if (currentFilter !== 'all') {
        filteredArticles = filteredArticles.filter(a => a.category === currentFilter);
    }
    
    // Поиск
    if (searchQuery) {
        const q = searchQuery.toLowerCase();
        filteredArticles = filteredArticles.filter(a => 
            a.title.toLowerCase().includes(q) ||
            a.tags.some(t => t.toLowerCase().includes(q)) ||
            a.category.toLowerCase().includes(q) ||
            a.description.toLowerCase().includes(q)
        );
    }
    
    // Сброс и ререндер
    displayedCount = 0;
    document.getElementById('articles-grid').innerHTML = '';
    
    if (filteredArticles.length === 0) {
        document.getElementById('articles-grid').innerHTML = `
            <div class="no-results">
                <p>🔍 Ничего не найдено</p>
                <p>Попробуйте изменить фильтр или поисковый запрос</p>
            </div>
        `;
        document.getElementById('end-message').style.display = 'none';
    } else {
        renderBatch();
    }
    
    updateArticleCount();
}

// ====== SEARCH ======

function setupSearch() {
    const input = document.getElementById('search');
    let debounceTimer;
    
    input.addEventListener('input', (e) => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            searchQuery = e.target.value.trim();
            applyFilters();
        }, 250);
    });
}

// ====== INFINITE SCROLL ======

function setupInfiniteScroll() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && displayedCount < filteredArticles.length) {
                renderBatch();
            }
        });
    }, { rootMargin: '200px' });
    
    observer.observe(document.getElementById('end-message'));
}

// ====== ARTICLE MODAL ======

async function openArticle(id) {
    const article = allArticles.find(a => a.id === id);
    if (!article) return;
    
    const modal = document.getElementById('article-modal');
    const body = document.getElementById('modal-body');
    
    // Показываем загрузку
    body.innerHTML = '<div class="loading"><div class="spinner"></div><p>Загрузка статьи...</p></div>';
    modal.showModal();
    
    // Если есть Telegra.ph URL — пробуем загрузить контент
    if (article.telegraph_url) {
        try {
            const path = article.telegraph_url.replace('https://telegra.ph/', '');
            const apiUrl = `https://telegra.ph/api/getPage/${path}?return_content=true`;
            
            const response = await fetch(apiUrl);
            const data = await response.json();
            
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
    const body = document.getElementById('modal-body');
    
    // Конвертируем Telegraph nodes в HTML
    let htmlContent = '';
    
    if (Array.isArray(content)) {
        content.forEach(node => {
            htmlContent += telegraphNodeToHtml(node);
        });
    }
    
    const sourcesHtml = article.sources.length > 0 ? `
        <div class="modal-sources">
            <h3>📚 Источники</h3>
            <ul>
                ${article.sources.map(s => {
                    // Извлекаем URL если есть
                    const urlMatch = s.match(/\((https?:\/\/[^)]+)\)/);
                    if (urlMatch) {
                        const name = s.replace(/\s*\(.*\)/, '');
                        return `<li><a href="${escapeHtml(urlMatch[1])}" target="_blank" rel="noopener">${escapeHtml(name || s)}</a></li>`;
                    }
                    return `<li>${escapeHtml(s)}</li>`;
                }).join('')}
            </ul>
        </div>
    ` : '';
    
    body.innerHTML = `
        <div class="modal-header">
            <h1 class="modal-title">${article.emoji} ${escapeHtml(article.title)}</h1>
            <div class="modal-meta">
                <span>📅 ${formatDate(article.date)}</span>
                <span>📂 ${escapeHtml(article.category)}</span>
            </div>
        </div>
        <div class="modal-body">
            ${htmlContent}
        </div>
        ${sourcesHtml}
        <div class="modal-actions">
            ${article.telegraph_url ? `<a href="${escapeHtml(article.telegraph_url)}" target="_blank" rel="noopener">📰 Telegra.ph</a>` : ''}
            <a href="https://t.me/JeBanceOnline" target="_blank" rel="noopener" class="secondary">💬 Telegram</a>
        </div>
    `;
}

function renderArticleFallback(article) {
    const body = document.getElementById('modal-body');
    
    const tagsHtml = article.tags.map(tag => 
        `<span class="card-tag" style="display:inline-block;margin:0.25rem;">${escapeHtml(tag)}</span>`
    ).join('');
    
    const sourcesHtml = article.sources.length > 0 ? `
        <div class="modal-sources">
            <h3>📚 Источники</h3>
            <ul>
                ${article.sources.map(s => {
                    const urlMatch = s.match(/\((https?:\/\/[^)]+)\)/);
                    if (urlMatch) {
                        const name = s.replace(/\s*\(.*\)/, '');
                        return `<li><a href="${escapeHtml(urlMatch[1])}" target="_blank" rel="noopener">${escapeHtml(name || s)}</a></li>`;
                    }
                    return `<li>${escapeHtml(s)}</li>`;
                }).join('')}
            </ul>
        </div>
    ` : '';
    
    body.innerHTML = `
        <div class="modal-header">
            <h1 class="modal-title">${article.emoji} ${escapeHtml(article.title)}</h1>
            <div class="modal-meta">
                <span>📅 ${formatDate(article.date)}</span>
                <span>📂 ${escapeHtml(article.category)}</span>
            </div>
            <div class="card-tags" style="margin-top:0.75rem;">${tagsHtml}</div>
        </div>
        <div class="modal-body">
            <p>${escapeHtml(article.description)}</p>
            <p>Полная статья доступна по ссылке ниже.</p>
        </div>
        ${sourcesHtml}
        <div class="modal-actions">
            ${article.telegraph_url ? `<a href="${escapeHtml(article.telegraph_url)}" target="_blank" rel="noopener">📰 Читать на Telegra.ph</a>` : ''}
            <a href="https://t.me/JeBanceOnline" target="_blank" rel="noopener" class="secondary">💬 Telegram канал</a>
        </div>
    `;
}

function telegraphNodeToHtml(node) {
    if (!node || !node.tag) return '';
    
    switch (node.tag) {
        case 'p':
            return `<p>${processNodeContent(node.children || node)}</p>`;
        case 'h3':
        case 'h4':
            return `<h2>${processNodeContent(node.children || node)}</h2>`;
        case 'ul':
            if (Array.isArray(node.children)) {
                const items = node.children.map(child => {
                    if (child.tag === 'li') {
                        return `<li>${processNodeContent(child.children || child)}</li>`;
                    }
                    return '';
                }).join('');
                return `<ul>${items}</ul>`;
            }
            return `<ul>${processNodeContent(node)}</ul>`;
        case 'ol':
            if (Array.isArray(node.children)) {
                const items = node.children.map(child => {
                    if (child.tag === 'li') {
                        return `<li>${processNodeContent(child.children || child)}</li>`;
                    }
                    return '';
                }).join('');
                return `<ol>${items}</ol>`;
            }
            return `<ol>${processNodeContent(node)}</ol>`;
        case 'a':
            return `<a href="${escapeHtml(node.attrs?.href || '#')}" target="_blank" rel="noopener">${processNodeContent(node.children || node)}</a>`;
        case 'strong':
        case 'b':
            return `<strong>${processNodeContent(node.children || node)}</strong>`;
        case 'em':
        case 'i':
            return `<em>${processNodeContent(node.children || node)}</em>`;
        case 'code':
            return `<code>${escapeHtml(processNodeContent(node.children || node))}</code>`;
        case 'pre':
            return `<pre><code>${escapeHtml(processNodeContent(node.children || node))}</code></pre>`;
        case 'br':
            return '<br>';
        case 'blockquote':
            return `<blockquote>${processNodeContent(node.children || node)}</blockquote>`;
        case 'figure':
            if (node.attrs?.src) {
                const caption = node.children ? processNodeContent(node.children) : '';
                return `<figure><img src="${escapeHtml(node.attrs.src)}" alt="${escapeHtml(caption)}" loading="lazy">${caption ? `<figcaption>${caption}</figcaption>` : ''}</figure>`;
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
    if (typeof node === 'object') {
        // Для простых узлов
        const text = Object.values(node)
            .filter(v => typeof v === 'string')
            .join(' ');
        return text || '';
    }
    return String(node || '');
}

// ====== CLOSE MODAL ======

document.getElementById('close-modal').addEventListener('click', () => {
    document.getElementById('article-modal').close();
});

document.getElementById('article-modal').addEventListener('click', (e) => {
    if (e.target === document.getElementById('article-modal')) {
        document.getElementById('article-modal').close();
    }
});

// ====== HELPERS ======

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    const months = ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек'];
    return `${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear()}`;
}

function updateArticleCount() {
    document.getElementById('article-count').textContent = filteredArticles.length;
}

function updateLastUpdated() {
    if (allArticles.length > 0) {
        const latest = allArticles[0].date;
        document.getElementById('last-updated').textContent = formatDate(latest);
    }
}

// ====== SERVICE WORKER ======

function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js')
            .then(reg => console.log('✅ Service Worker registered'))
            .catch(err => console.log('⚠️ SW registration failed:', err));
    }
}

// ====== START ======

document.addEventListener('DOMContentLoaded', init);
