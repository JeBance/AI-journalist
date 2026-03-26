# Инструкция по использованию библиотеки AI-journalist

## 📋 Назначение

Эта инструкция описывает порядок действий AI-агента при публикации новостей и статей.

**Важно:** Используй библиотеку `ai_journalist` для всех публикаций. Это исключает ошибки форматирования.

---

## 🔧 Настройка окружения

### Шаг 1: Добавь путь к библиотеке

```python
import sys
sys.path.insert(0, '/root/git/AI-journalist/lib')

from ai_journalist import TelegramClient, TelegraphClient, format_post, format_news_post
```

### Шаг 2: Проверь конфигурацию

```python
from ai_journalist import TelegramClient

tg = TelegramClient()
if tg.test_connection():
    print("✅ Бот готов к работе")
```

---

## 📝 Публикация новости (одиночный пост)

### Алгоритм действий

1. **Исследуй источники** (см. `02_research_protocol.md`)
2. **Выбери тему** (проверь уникальность в `06_history/`)
3. **Напиши пост** используя `format_news_post()`
4. **Опубликуй** через `tg.send_message()`
5. **Запиши в историю**

### Пример кода

```python
import sys
sys.path.insert(0, '/root/git/AI-journalist/lib')

from ai_journalist import TelegramClient, format_news_post

# Инициализация
tg = TelegramClient()

# Форматирование поста
post = format_news_post(
    headline="Node.js выпустил security патчи",
    summary="24 марта 2026 Node.js выпустил экстренные обновления для всех активных версий",
    details=[
        "CVE-2026-21637 (High) — DoS через TLS SNI",
        "CVE-2026-21710 (High) — DoS через __proto__",
        "CVE-2026-21717 (Medium) — HashDoS в V8",
        "Версии: v20.20.2, v22.22.2, v24.14.1, v25.8.2"
    ],
    category="javascript",
    sources=["Node.js Security Announcement", "GitHub Release Notes"]
)

# Публикация (auto_escape=True по умолчанию!)
result = tg.send_message(post)

if result["success"]:
    print(f"✅ Опубликовано! Message ID: {result['message_id']}")
    
    # Запись в историю (обнови файлы вручную или через скрипт)
else:
    print(f"❌ Ошибка: {result['error']}")
```

---

## 📖 Публикация статьи на Telegra.ph

### Алгоритм действий

1. **Исследуй тему глубоко** (см. `02_topic_research.md`)
2. **Напиши статью** (1000+ слов)
3. **Опубликуй** на Telegra.ph через `tph.create_page()`
4. **Создай анонс** через `tph.create_announcement_post()`
5. **Опубликуй анонс** в Telegram
6. **Запиши в историю**

### Пример кода

```python
import sys
sys.path.insert(0, '/root/git/AI-journalist/lib')

from ai_journalist import TelegraphClient, TelegramClient

# Инициализация
tph = TelegraphClient()
tg = TelegramClient()

# Статья в Markdown
article_content = """
## Введение

Текст введения с **жирным** и _курсивом_.

## Основная часть

· Пункт 1
· Пункт 2

[Ссылка](https://example.com)
"""

# Публикация статьи
result = tph.create_page(
    title="PHP 8.4: полное руководство",
    content=article_content
)

if result["success"]:
    article_url = result["url"]
    print(f"📰 Статья: {article_url}")
    
    # Создание анонса
    announcement = tph.create_announcement_post(
        article_url=article_url,
        title="PHP 8.4: полное руководство",
        description="Разбираем новые фичи"
    )
    
    # Публикация анонса (уже экранирован!)
    tg_result = tg.send_message(announcement, auto_escape=False)
    
    if tg_result["success"]:
        print(f"✅ Анонс опубликован! Message ID: {tg_result['message_id']}")
else:
    print(f"❌ Ошибка: {result['error']}")
```

---

## 🔄 Публикация с черновиком (на утверждение)

### Алгоритм действий

1. **Напиши пост**
2. **Отправь черновик** пользователю в ЛС
3. **Получи подтверждение** (вручную или через кнопки)
4. **Опубликуй** после подтверждения

### Пример кода

```python
import sys
sys.path.insert(0, '/root/git/AI-journalist/lib')

from ai_journalist import TelegramClient, format_post

tg = TelegramClient()

# Форматирование поста
post = format_post(
    title="Node.js security релиз",
    content="Исправлены 9 уязвимостей",
    hashtags=["nodejs", "security"],
    emoji="🔒"
)

# Отправка черновика
USER_ID = 5610580916  # @JeBance
result = tg.send_to_user(
    user_id=USER_ID,
    text=f"📝 ЧЕРНОВИК НА УТВЕРЖДЕНИЕ\n\n{post}\n\nОпубликовать?"
)

# После подтверждения (вручную):
# tg.send_message(post)
```

---

## 📊 Форматирование постов

### format_post() — базовый пост

```python
from ai_journalist import format_post

post = format_post(
    title="Заголовок",
    content="Текст новости",
    hashtags=["тег1", "тег2"],
    emoji="🔥",
    sources=["Источник 1", "Источник 2"]
)
```

### format_news_post() — новость

```python
from ai_journalist import format_news_post

post = format_news_post(
    headline="Заголовок новости",
    summary="Краткое описание (1-2 предложения)",
    details=[
        "Деталь 1",
        "Деталь 2",
        "Деталь 3"
    ],
    category="javascript",  # javascript, php, css, vpn_security, и т.д.
    sources=["Источник 1"]
)
```

### format_tutorial_post() — туториал

```python
from ai_journalist import format_tutorial_post

post = format_tutorial_post(
    title="Настройка VLESS за 10 минут",
    introduction="Пошаговая инструкция",
    steps=[
        {"title": "Шаг 1", "content": "Установите Xray-core"},
        {"title": "Шаг 2", "content": "Настройте конфиг"}
    ],
    conclusion="Готово!",
    tags=["vpn", "tutorial"]
)
```

---

## ⚠️ Критические правила

### 1. Всегда используй библиотеку

```python
# ✅ Правильно:
import sys
sys.path.insert(0, '/root/git/AI-journalist/lib')
from ai_journalist import TelegramClient, format_post

# ❌ Неправильно:
# import subprocess
# subprocess.run(["python3", "publisher.py", text])
```

### 2. Всегда проверяй результат

```python
result = tg.send_message(post)

if result["success"]:
    message_id = result["message_id"]
    # Запиши в историю
else:
    print(f"❌ Ошибка: {result['error']}")
    # Запиши ошибку в 01_error_log.md
```

### 3. Всегда записывай в историю

После публикации обнови:
- `06_history/01_published_posts.md`
- `06_history/02_topics_covered.md`

### 4. Не экранируй вручную

```python
# ✅ Правильно (библиотека экранирует автоматически):
post = format_post(title="PHP 8.4", ...)
tg.send_message(post)

# ❌ Неправильно (двойное экранирование):
text = escape_markdown_v2("PHP 8.4")
post = format_post(title=text, ...)  # Будет экранировано ещё раз!
```

---

## 🐛 Решение проблем

### Ошибка: "Bad Request: can't parse entities"

**Причина:** Двойное экранирование или неправильный Markdown

**Решение:**
```python
# Используй auto_escape=True (по умолчанию):
result = tg.send_message(text, auto_escape=True)

# Или не экранируй вручную:
post = format_post(...)  # Уже экранировано
result = tg.send_message(post)
```

### Ошибка: "No access token"

**Причина:** Не получен токен Telegra.ph

**Решение:**
```bash
python3 /root/git/AI-journalist-bot/get_telegraph_token.py
```

### Ошибка: "Chat not found"

**Причина:** Бот не в администраторах канала

**Решение:**
1. Добавь бота в администраторы канала
2. Проверь chat_id в `/root/git/AI-journalist-bot/config.json`

---

## 📞 Контакты

**Канал:** @JeBanceOnline
**Бот:** @JeBanceOnlineBot
**Владелец:** @JeBance (ID: 5610580916)

---

**Версия:** 1.0.0
**Дата:** 2026-03-26
