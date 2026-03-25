# Интеграция с Telegra.ph

## 📋 Назначение

Публикация длинных статей на платформе **Telegra.ph** с последующим анонсом в Telegram канале.

---

## 🚀 Быстрая настройка

### Шаг 1: Проверка конфигурации

```bash
cd /root/git/AI-journalist-bot
cat telegraph_config.json
```

**Содержимое:**
```json
{
  "short_name": "AI Journalist",
  "author_name": "AI Journalist",
  "author_url": "https://t.me/JeBanceOnline"
}
```

### Шаг 2: Тестовая публикация

```bash
python3 telegraph_publisher.py \
  "Тестовая статья" \
  "Это тестовая публикация на Telegra.ph"
```

---

## 📖 Использование

### Вариант 1: Из командной строки

```bash
python3 telegraph_publisher.py \
  "Заголовок статьи" \
  "Содержание статьи (Markdown)" \
  "Автор"
```

### Вариант 2: Через Python

```python
from telegraph_publisher import publish_article, create_announcement_post

# Публикация статьи
result = publish_article(
    title="PHP 8.4: полное руководство",
    content="Содержание статьи...",
    author="AI Journalist"
)

if result["success"]:
    article_url = result["url"]
    
    # Создание анонса
    announcement = create_announcement_post(
        article_url=article_url,
        title="PHP 8.4: полное руководство",
        description="Разбираем новые фичи PHP 8.4"
    )
    
    # Публикация анонса в Telegram
    from publisher import publish
    publish(announcement)
```

### Вариант 3: С автоматическим анонсом

```python
from telegraph_publisher import publish_with_announcement

result = publish_with_announcement(
    title="PHP 8.4: полное руководство",
    content="...",
    description="Краткое описание для анонса",
    telegram_publish=True  # Опубликовать анонс в Telegram
)
```

---

## 🤖 Использование с AI-агентом

### Команда для AI

```
Изучи папку AI-journalist.

Выполни глубокое исследование по теме "PHP 8.4: полное руководство".

Используй сценарий "topic_research" из workflows.

Напиши подробную статью (1000+ слов) и опубликуй на Telegra.ph:
python3 /root/git/AI-journalist-bot/telegraph_publisher.py

Затем опубликуй анонс в Telegram:
python3 /root/git/AI-journalist-bot/publisher.py "текст анонса"

Запиши результат в историю.
```

### Рабочий процесс AI

1. **Исследование** (5-10 минут)
   - Проверка источников
   - Сбор информации

2. **Написание** (5-10 минут)
   - Структура статьи
   - Примеры кода
   - Источники

3. **Публикация на Telegra.ph** (1 минута)
   ```bash
   python3 telegraph_publisher.py "Заголовок" "Содержание"
   ```

4. **Создание анонса** (1 минута)
   ```
   📖 Новая статья на Telegra.ph
   
   *{Заголовок}*
   
   {Краткое описание}
   
   [Читать полностью →]({URL})
   
   \#статья \#telegraph
   ```

5. **Публикация анонса** (1 минута)
   ```bash
   python3 publisher.py "текст анонса"
   ```

6. **Запись в историю** (1 минута)
   - `06_history/01_published_posts.md`
   - Добавление URL статьи

---

## 📊 Форматирование

### Поддерживаемый Markdown

| Элемент | Telegra.ph | Telegram |
|---------|------------|----------|
| Заголовки | `#`, `##`, `###` | `*жирный*` |
| Жирный | `**текст**` | `*текст*` |
| Курсив | `_текст_` | `_текст_` |
| Код | ```` ```код``` ```` | ```` ```код``` ```` |
| Ссылки | `[текст](url)` | `[текст](url)` |
| Списки | `· `, `- ` | `· ` |

### Конвертация

Скрипт автоматически конвертирует Markdown в формат Telegra.ph (JSON).

**Пример:**

Input (Markdown):
```markdown
# Заголовок

Текст с **жирным** и _курсивом_.

· Пункт 1
· Пункт 2

[Ссылка](https://example.com)
```

Output (Telegra.ph JSON):
```json
[
  {"tag": "h3", "children": ["Заголовок"]},
  {"tag": "p", "children": ["Текст с <b>жирным</b> и <i>курсивом</i>."]},
  {"tag": "li", "children": ["Пункт 1"]},
  {"tag": "li", "children": ["Пункт 2"]},
  {"tag": "p", "children": ["<a href=\"https://example.com\">Ссылка</a>"]}
]
```

---

## 📁 Структура файлов

```
AI-journalist-bot/
├── telegraph_publisher.py    # Публикация на Telegra.ph
├── telegraph_config.json     # Конфигурация
└── publisher.py              # Публикация в Telegram
```

---

## 🎯 Примеры использования

### Пример 1: Туториал

**Команда AI:**
```
Напиши туториал "Настройка VLESS с Reality за 10 минут"
Опубликуй на Telegra.ph с анонсом
```

**Результат:**
- Статья: `https://telegra.ph/Nastrojka-VLESS-s-Reality-za-10-minut-03-25`
- Анонс в канале

---

### Пример 2: Сравнение технологий

**Команда AI:**
```
Сравни Prisma и Doctrine ORM
Опубликуй сравнение на Telegra.ph
```

**Результат:**
- Статья с таблицами и примерами
- Анонс с краткими выводами

---

### Пример 3: Еженедельный дайджест

**Команда AI:**
```
Собери дайджест за неделю
Опубликуй на Telegra.ph (полная версия)
и в Telegram (краткая версия)
```

**Результат:**
- Полная версия на Telegra.ph (5-7 новостей с деталями)
- Краткая версия в Telegram (только заголовки)

---

## ⚠️ Ограничения Telegra.ph

| Параметр | Значение |
|----------|----------|
| Макс. длина статьи | ~64KB |
| Поддержка изображений | ✅ Да |
| Поддержка видео | ❌ Нет |
| Редактирование | ✅ В течение 24 часов |
| Удаление | ❌ Нет |
| Аналитика | ❌ Нет |

---

## 🔧 Решение проблем

### Ошибка: "Invalid JSON"

**Причина:** Неправильный формат контента

**Решение:**
```python
# Убедись, что контент валидный Markdown
content = """
# Заголовок

Текст статьи.
"""
```

### Ошибка: "Title is required"

**Причина:** Пустой заголовок

**Решение:**
```python
publish_article(title="Заголовок", content="...")
```

### Статья не редактируется

**Причина:** Прошло более 24 часов

**Решение:**
- Telegra.ph позволяет редактировать только в течение 24 часов
- Для обновления создай новую статью

---

## 📊 Статистика публикаций

Веди учёт в `06_history/01_published_posts.md`:

```markdown
### [2026-03-25] PHP 8.4: полное руководство
- **Категория:** php
- **Шаблон:** tutorial
- **Telegra.ph URL:** https://telegra.ph/...
- **Telegram ID:** 12345
- **Статус:** опубликовано
```

---

## 💡 Советы

### Для AI-агента

1. **Пиши подробно** — Telegra.ph позволяет длинные тексты
2. **Добавляй структуру** — заголовки, списки, код
3. **Указывай источники** — ссылки в конце статьи
4. **Создавай краткий анонс** — 2-3 предложения для Telegram

### Для читателя

1. **Анонс в Telegram** — краткое содержание
2. **Ссылка на Telegra.ph** — полная версия
3. **Теги** — для поиска статей

---

## 🔗 Полезные ссылки

- **Telegra.ph:** https://telegra.ph
- **API документация:** https://core.telegram.org/telegraph
- **Примеры статей:** https://telegra.ph/trending

---

**Версия:** 1.0  
**Дата:** 2026-03-25
