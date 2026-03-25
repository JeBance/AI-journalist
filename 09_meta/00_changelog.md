# Changelog инфраструктуры

## 📋 Назначение

История изменений файловой инфраструктуры AI-journalist.

---

## [1.1.0] — 2026-03-25

### Добавлено

**Telegra.ph интеграция:**
- `telegraph_publisher.py` — публикация статей на Telegra.ph
- `telegraph_config.json` — конфигурация
- `10_integrations/03_telegraph.md` — инструкция по интеграции

**Самообучение AI:**
- `00_main_prompt.md` — базовый промпт с конфигурацией
- `00_learned_prompts.md` — накопленные знания
- `01_error_log.md` — журнал ошибок
- `update_prompts.py` — скрипт обновления промтов
- `10_integrations/02_self_learning.md` — инструкция по самообучению

**Документация:**
- `README_FULL.md` — полная документация проекта
- Обновлённый `README.md` с новыми возможностями

### Изменения

- Обновлён основной промпт с информацией о канале @JeBanceOnline
- Добавлено экранирование Markdown V2 в примеры
- Интеграция с ботом @JeBanceOnlineBot

---

## [1.0.0] — 2026-03-25

### Добавлено

**Структура проекта:**
- ✅ 9 основных папок
- ✅ 53 файла с документацией

**01_system_prompts/:**
- `01_role_and_mission.md` — роль AI-агента
- `02_research_protocol.md` — протокол исследования
- `03_writing_guidelines.md` — правила написания постов
- `04_quality_checklist.md` — чек-лист качества

**02_sources/:**
- `00_index.md` — оглавление источников
- `01_rss_feeds.md` — 19 RSS-лент
- `02_github_repos.md` — 27 репозиториев
- `03_telegram_channels.md` — 14 Telegram-каналов
- `04_technical_blogs.md` — 22 технических блога
- `05_newsletters.md` — 8 email-рассылок
- `06_podcasts_and_videos.md` — 10 подкастов/видео
- `07_forums_and_communities.md` — 10 форумов
- `08_keywords.md` — ключевые слова по 9 категориям

**03_templates/:**
- `00_index.md` — оглавление шаблонов
- `01_single_post.md` — одиночная новость
- `02_daily_digest.md` — ежедневный дайджест
- `03_breaking_news.md` — срочная новость
- `04_tutorial.md` — туториал
- `05_code_review.md` — разбор кода
- `06_comparison.md` — сравнение технологий

**04_style/:**
- `00_index.md` — оглавление стиля
- `01_tone_and_voice.md` — тон и голос канала
- `02_emoji_guide.md` — правила использования эмодзи
- `03_formatting_rules.md` — Telegram Markdown V2
- `04_terminology.md` — техническая терминология
- `05_examples.md` — примеры идеальных постов

**05_categories/:**
- `00_index.md` — оглавление категорий
- `01_javascript.md` — JavaScript/TypeScript/Node.js
- `02_php.md` — PHP и фреймворки
- `03_css.md` — CSS/Tailwind/дизайн
- `04_vpn_security.md` — VPN, vless, безопасность
- `05_hardware.md` — гаджеты, железо, ноутбуки
- `06_devops.md` — Docker, CI/CD, облака
- `07_patterns.md` — паттерны, архитектура, SOLID
- `08_databases.md` — SQL, NoSQL, ORM
- `09_ai_tools.md` — AI для разработчиков

**06_history/:**
- `00_index.md` — оглавление истории
- `01_published_posts.md` — архив публикаций
- `02_topics_covered.md` — уникальные темы
- `03_sources_used.md` — статистика источников
- `04_templates_used.md` — статистика шаблонов

**07_research_cache/:**
- `00_index.md` — оглавление кэша
- `01_last_session.md` — результаты последней сессии
- `02_processed_urls.md` — обработанные URL
- `03_temp_notes.md` — временные заметки

**08_workflows/:**
- `00_index.md` — оглавление сценариев
- `01_daily_publication.md` — ежедневная публикация
- `02_topic_research.md` — исследование по запросу
- `03_weekly_summary.md` — еженедельный дайджест
- `04_emergency_news.md` — срочная новость

**09_meta/:**
- `00_changelog.md` — этот файл
- `01_roadmap.md` — план развития
- `02_contributing.md` — как дополнять систему
- `03_license.md` — лицензия (MIT)

**Корневые файлы:**
- `README.md` — точка входа
- `00_quick_start.md` — быстрый старт

### Особенности версии 1.0.0

- **Zero-Infrastructure Approach** — не требует кода, сервера, БД
- **AI-agnostic** — работает с Claude, ChatGPT, DeepSeek, Gemini
- **Текстовая архитектура** — вся логика в Markdown-файлах
- **Масштабируемость** — копирование папки для новых каналов
- **Предотвращение повторов** — система истории публикаций

---

## 📊 Статистика релиза

| Метрика | Значение |
|---------|----------|
| Папок | 9 |
| Файлов | 53 |
| Строк кода | ~0 (только Markdown) |
| Источников | 100+ |
| Шаблонов | 6 |
| Категорий | 9 |
| Сценариев | 4 |

---

## 🔮 Планы на будущее

См. `01_roadmap.md` для деталей.

---

## 📝 Лицензия

MIT — используйте, модифицируйте, улучшайте!
