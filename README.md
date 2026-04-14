# AI Journalist — IT-новости

Автоматический AI-журналист: публикация IT-новостей в Telegram-канал с архивом на сайте.

## 🌐 Ссылки

| Ресурс | URL |
|--------|-----|
| 📰 Сайт | https://ai.jebance.ru |
| 💬 Telegram канал | https://t.me/JeBanceOnline |
| 📦 Репозиторий | https://github.com/JeBance/AI-journalist |
| 📝 Telegra.ph | Статьи публикуются автоматически |

## 🚀 Что это?

AI-журналист работает на сервере и каждые 30 минут:
1. Исследует свежие IT-новости (GitHub, RSS, блоги)
2. Пишет статью на основе найденных материалов
3. Публикует на **Telegra.ph** (полная статья)
4. Отправляет анонс в **Telegram канал**
5. Сохраняет в историю с полным контентом
6. Пушит обновления на **GitHub Pages** → сайт обновляется автоматически

### 📊 Статистика

| Показатель | Значение |
|-----------|----------|
| Всего статей | 234 |
| С полным контентом | 218 (93%) |
| Публикаций в день | ~6-8 |
| Активных категорий | 73+ |

## 🏗️ Архитектура

```
┌─────────────────────────────────────┐
│  Латвийский сервер (89.40.204.239) │
│                                     │
│  AI-journalist (каждые 30 мин):    │
│  1. Ищет новости                   │
│  2. Публикует в Telegram           │
│  3. Публикует на Telegra.ph        │
│  4. Пишет в 06_history/*.md        │
│  5. Генерирует articles.json       │
│  6. git add + commit + push        │
└──────────────┬──────────────────────┘
               │ git push
               ▼
┌─────────────────────────────────────┐
│  GitHub Pages (бесплатно)           │
│  JeBance/AI-journalist @ gh-pages  │
│                                     │
│  ├── index.html      (UI)          │
│  ├── app.js          (логика)      │
│  ├── styles.css      (стили)       │
│  ├── idb-cache.js    (кэш)         │
│  ├── articles.json   (данные)      │
│  └── sw.js           (PWA)         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  ai.jebance.ru → GitHub Pages       │
│                                     │
│  • Фильтрация по категориям         │
│  • Поиск по заголовкам и тегам      │
│  • Чтение в модальных окнах         │
│  • IndexedDB кэш (мгновенная        │
│    загрузка при повторном визите)   │
│  • PWA (работает оффлайн)           │
│  • Адаптивный дизайн                │
│    — Desktop: sidebar + grid        │
│    — Mobile: drawer + 1 column      │
│  • Тёмная/светлая тема              │
│    (с сохранением в localStorage)   │
└─────────────────────────────────────┘
```

## 📁 Структура проекта

```
AI-journalist/
├── 01_system_prompts/     # Промты для AI-агента
│   ├── 00_main_prompt.md
│   ├── 01_role_and_mission.md
│   ├── 02_research_protocol.md
│   ├── 03_writing_guidelines.md
│   └── 04_quality_checklist.md
├── 02_sources/            # Источники новостей
│   ├── 01_rss_feeds.md
│   ├── 02_github_repos.md
│   ├── 03_telegram_channels.md
│   └── 04_technical_blogs.md
├── 03_templates/          # Шаблоны постов
├── 04_style/              # Правила стиля
├── 05_categories/         # Категории и теги
├── 06_history/            # История публикаций
│   ├── published_posts_2026-03.md
│   ├── published_posts_2026-04.md
│   └── 02_topics_covered.md
├── 07_research_cache/     # Кэш исследований
├── 08_workflows/          # Сценарии работы
│   ├── 01_daily_publication.md
│   └── 02_topic_research.md
├── 09_meta/               # Метаданные проекта
├── ai_journalist/         # Python модуль
│   ├── history_manager.py
│   ├── telegram_client.py
│   └── telegraph_client.py
├── publisher_final.py     # Основной скрипт публикации
├── generate_json.py       # Генератор articles.json
├── check_duplicates.py    # Проверка дубликатов
├── monitor.py             # Мониторинг ошибок
├── index.html             # Сайт (GitHub Pages)
├── app.js                 # Логика сайта
├── styles.css             # Стили сайта
├── idb-cache.js           # IndexedDB кэш
├── sw.js                  # Service Worker (PWA)
└── manifest.json          # PWA манифест
```

## 🔧 Технологии

| Компонент | Технология |
|-----------|-----------|
| Backend | Python 3.12 |
| Frontend | Vanilla JS + CSS (no frameworks) |
| Хостинг | GitHub Pages (бесплатно) |
| БД | IndexedDB (браузер) |
| PWA | Service Worker + manifest |
| Публикации | Telegra.ph + Telegram Bot API |
| Автоматизация | systemd timer (каждые 30 мин) |

## 📈 Потребление ресурсов

| Ресурс | Потребление |
|--------|-------------|
| RAM | 0 MB на сервере (всё на GitHub) |
| CPU | ~2-5% при git push (раз в 30 мин) |
| Диск | articles.json ~1 MB (растёт с каждой статьёй) |
| Трафик | GitHub Pages CDN (бесплатно) |

##  Особенности сайта

### Адаптивный дизайн
- **Desktop (>768px):** sidebar с фильтрами + сетка карточек
- **Tablet (≤1024px):** узкий sidebar + адаптивная сетка
- **Mobile (≤768px):** drawer с фильтрами, одна колонка

### Кэширование
- **IndexedDB:** articles.json кэшируется в браузере
- **Первый визит:** ~2-3 сек загрузка (925 KB)
- **Повторный визит:** ~50ms из IndexedDB
- **Оффлайн:** полная работоспособность

### Темы
- 🌙 Тёмная (по умолчанию)
- ☀️ Светлая (через переключатель)
- Сохранение в `localStorage`

### Поиск и фильтры
- Поиск по заголовкам, тегам, категориям, описаниям
- Фильтрация по категориям с счётчиками
- Синхронизация поиска между desktop/mobile/drawer

## 📝 Формат истории

Каждая статья в `06_history/` содержит:

```markdown
### [2026-04-14] Заголовок статьи

- **Категория:** python
- **Шаблон:** telegra.ph article
- **Ключевые темы:** python, security, release
- **Источники:**
  - Python.org Changelog (https://...)
  - Python Downloads (https://...)
- **Telegra.ph URL:** https://telegra.ph/...
- **Telegram ID:** 473
- **Статус:** опубликован

<!-- CONTENT_START -->
Полный текст статьи в Markdown...
<!-- CONTENT_END -->

---
```

## 🤖 Автоматическая публикация

`publisher_final.py` делает:
1. Проверка на дубликаты (тема + заголовок)
2. Публикация на Telegra.ph
3. Публикация анонса в Telegram
4. Запись в историю с полным контентом
5. Генерация `articles.json`
6. `git add + commit + push` в GitHub

## 📊 Статистика публикаций

| Месяц | Постов |
|-------|--------|
| Март 2026 | 210 |
| Апрель 2026 | 24+ |

## 🛠️ Разработка

### Локальный запуск

```bash
cd /root/git/AI-journalist
source venv/bin/activate
python3 publisher_final.py --input article_data.json
```

### Генерация данных для сайта

```bash
python3 generate_json.py
# Создаёт articles.json из 06_history/*.md
```

### Backfill контента (с латвийского сервера)

```bash
python3 backfill_content.py
# Загружает полный текст статей из Telegra.ph API
```

## 📄 Лицензия

Проект разработан для автоматизации IT-журналистики.

##  Благодарности

- **Telegra.ph** — платформа для публикаций
- **Telegram Bot API** — доставка контента
- **GitHub Pages** — бесплатный хостинг сайта
- **AI-агенты** — Claude, ChatGPT, DeepSeek, Qwen
