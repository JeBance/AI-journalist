# AI-journalist — Инструкция для Qwen Code

## 🚀 Что это?

**AI-journalist** — это файловая система знаний для превращения AI-агента (Qwen Code, Claude, ChatGPT) в технического журналиста Telegram-канала @JeBanceOnline.

---

## 📋 Быстрый старт для Qwen Code

### Шаг 1: Загрузка инфраструктуры

При запуске прочитай все файлы:

```bash
# Прочитай базовые промты
cat /root/git/AI-journalist/01_system_prompts/00_main_prompt.md
cat /root/git/AI-journalist/01_system_prompts/00_learned_prompts.md
cat /root/git/AI-journalist/01_system_prompts/01_error_log.md

# Изучи структуру
ls -la /root/git/AI-journalist/
```

### Шаг 2: Выбор сценария

**Сценарий 1: Ежедневная публикация (10-15 мин)**

```
Команда: Выполни daily_publication из 08_workflows/

AI делает:
1. Исследует источники (02_sources/)
2. Выбирает тему (проверяет 06_history/)
3. Пишет пост (03_templates/)
4. Публикует (publisher.py)
5. Записывает в историю
```

**Сценарий 2: Глубокое исследование с Telegra.ph (20-30 мин)**

```
Команда: Выполни topic_research + Telegra.ph

AI делает:
1. Исследует тему глубоко
2. Пишет статью (1000+ слов)
3. Публикует на Telegra.ph (telegraph_publisher.py)
4. Создаёт анонс
5. Публикует анонс в Telegram
6. Записывает в историю
```

---

## 🔧 Инструменты

### Публикация в Telegram

```bash
python3 /root/git/AI-journalist-bot/publisher.py "Текст поста"
```

**Важно:** Экранируй Markdown V2 символы:
```
_ * [ ] ( ) ~ ` > # + - = | { } . !
```

**Пример:**
```bash
python3 publisher.py "🔥 *PHP 8\.4\.0 released*

Вышел релиз PHP 8\.4\.

\#php \#javascript"
```

### Публикация на Telegra.ph

```bash
python3 /root/git/AI-journalist-bot/telegraph_publisher.py \
  "Заголовок статьи" \
  "Содержание (Markdown)"
```

### Публикация с анонсом (Python)

```python
from telegraph_publisher import publish_with_announcement

result = publish_with_announcement(
    title="PHP 8.4: полное руководство",
    content="...",
    description="Разбираем новые фичи",
    telegram_publish=True
)
```

### Обновление промтов

```bash
# Добавить правило
python3 update_prompts.py --rule "Экранировать # в тегах"

# Добавить ошибку
python3 update_prompts.py --error "Ошибка" --solution "Решение"

# Показать промты
python3 update_prompts.py --show
```

---

## 📁 Структура проекта

```
/root/git/AI-journalist/
├── README.md                    # Точка входа
├── 00_quick_start.md            # Быстрый старт
├── 01_system_prompts/           # ⭐ Читай при запуске!
│   ├── 00_main_prompt.md        # Базовый промпт
│   ├── 00_learned_prompts.md    # Накопленные знания
│   └── 01_error_log.md          # Журнал ошибок
├── 02_sources/                  # Источники (100+)
├── 03_templates/                # Шаблоны постов
├── 04_style/                    # Стиль канала
├── 05_categories/               # Категории
├── 06_history/                  # История (проверяй!)
├── 07_research_cache/           # Кэш
├── 08_workflows/                # Сценарии
├── 09_meta/                     # Мета
└── 10_integrations/             # Интеграции
    ├── 01_telegram_bot.md       # Telegram бот
    ├── 02_self_learning.md      # Самообучение
    └── 03_telegraph.md          # Telegra.ph

/root/git/AI-journalist-bot/
├── publisher.py                 # Публикация в Telegram
├── telegraph_publisher.py       # Публикация на Telegra.ph
├── update_prompts.py            # Обновление промтов
└── config.json                  # Конфигурация бота
```

---

## 🎯 Примеры команд

### Пример 1: Ежедневная публикация

```
Qwen, выступи как главный редактор IT-канала @JeBanceOnline.

1. Прочитай промты из 01_system_prompts/
2. Исследуй источники из 02_sources/
3. Выбери главную новость дня
4. Напиши пост по шаблону из 03_templates/01_single_post.md
5. Покажи черновик
6. После подтверждения опубликуй:
   python3 /root/git/AI-journalist-bot/publisher.py "текст"
7. Запиши в 06_history/01_published_posts.md
```

---

### Пример 2: Глубокое исследование с Telegra.ph

```
Qwen, выступи как технический журналист.

1. Прочитай промты из 01_system_prompts/
2. Выполни глубокое исследование по теме "PHP 8.4: полное руководство"
   - Проверь 02_sources/02_github_repos.md (php/php-src)
   - Проверь 02_sources/01_rss_feeds.md (PHP Weekly)
   - Проверь 02_sources/04_technical_blogs.md (PHP.net)
3. Напиши подробную статью (1000+ слов)
4. Опубликуй на Telegra.ph:
   python3 /root/git/AI-journalist-bot/telegraph_publisher.py "Заголовок" "Содержание"
5. Создай анонс и опубликуй в Telegram:
   python3 /root/git/AI-journalist-bot/publisher.py "текст анонса"
6. Запиши результаты в историю
```

---

### Пример 3: Еженедельный дайджест

```
Qwen, подготовь еженедельный дайджест.

1. Прочитай 08_workflows/03_weekly_summary.md
2. Собери новости за период (укажи даты)
3. Выбери 5-7 главных новостей
4. Напиши дайджест по шаблону 03_templates/02_daily_digest.md
5. Опубликуй в Telegram
6. Запиши в историю
```

---

## ⚠️ Критические правила

### 1. Всегда читай при запуске

- `00_main_prompt.md` — базовые инструкции
- `00_learned_prompts.md` — накопленные знания
- `01_error_log.md` — известные ошибки

### 2. Всегда экранируй Markdown V2

```
_ * [ ] ( ) ~ ` > # + - = | { } . !
```

**Примеры:**
- ❌ `PHP 8.4 > PHP 8.3 #тег`
- ✅ `PHP 8\.4 \> PHP 8\.3 \#тег`

### 3. Всегда проверяй историю

Перед публикацией проверь `06_history/02_topics_covered.md` — не дублируется ли тема.

### 4. Всегда показывай черновик

Перед публикацией покажи пост пользователю и получи подтверждение.

### 5. Всегда записывай результат

После публикации обнови:
- `06_history/01_published_posts.md`
- `06_history/02_topics_covered.md`
- `07_research_cache/01_last_session.md`

---

## 🧠 Самообучение

### После каждой сессии

Если обнаружил новое:

1. **Новое правило** → добавь в `00_learned_prompts.md`:
   ```bash
   python3 update_prompts.py --rule "Описание правила"
   ```

2. **Новая ошибка** → добавь в `01_error_log.md`:
   ```bash
   python3 update_prompts.py --error "Ошибка" --solution "Решение"
   ```

### При следующем запуске

Прочитай обновлённые файлы и примени новые правила.

---

## 📊 Статистика проекта

| Метрика | Значение |
|---------|----------|
| **Markdown файлов** | 63 |
| **Python скриптов** | 3 |
| **Источников** | 100+ |
| **Шаблонов** | 6 |
| **Категорий** | 9 |
| **Сценариев** | 4 |

---

## 📞 Контакты

**Канал:** @JeBanceOnline  
**Бот:** @JeBanceOnlineBot  
**Владелец:** @JeBance (ID: 5610580916)

---

## 🔗 Документация

- **Полная документация:** `README_FULL.md`
- **Telegra.ph интеграция:** `10_integrations/03_telegraph.md`
- **Самообучение:** `10_integrations/02_self_learning.md`
- **Telegram бот:** `../AI-journalist-bot/README.md`

---

**Версия:** 1.1  
**Дата:** 2026-03-25  
**Для:** Qwen Code
