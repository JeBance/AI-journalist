# AI-journalist Library

**Централизованная библиотека для взаимодействия с Telegram и Telegra.ph**

Все функции протестированы, используют правильное форматирование и исключают ошибки AI-агента при повторном запуске.

---

## 📦 Установка

Библиотека находится в `/root/git/AI-journalist/lib/`

**Добавьте путь в начало ваших скриптов:**

```python
import sys
sys.path.insert(0, '/root/git/AI-journalist/lib')

from ai_journalist import TelegramClient, TelegraphClient, format_post
```

Или используйте абсолютный импорт:

```python
from ai_journalist.telegram_client import TelegramClient
from ai_journalist.telegraph_client import TelegraphClient
from ai_journalist.formatting import escape_markdown_v2
```

---

## 🚀 Быстрый старт

### Пример 1: Отправка сообщения в Telegram

```python
from ai_journalist import TelegramClient, format_post

# Инициализация
tg = TelegramClient()

# Вариант A: Готовый пост с форматированием
post = format_post(
    title="Node.js security релиз",
    content="Исправлены 9 уязвимостей в Node.js",
    hashtags=["nodejs", "security", "javascript"],
    emoji="🔒"
)

# Отправка (auto_escape=True по умолчанию)
result = tg.send_message(post)

if result["success"]:
    print(f"✅ Опубликовано! Message ID: {result['message_id']}")
else:
    print(f"❌ Ошибка: {result['error']}")
```

### Пример 2: Публикация статьи на Telegra.ph

```python
from ai_journalist import TelegraphClient

tph = TelegraphClient()

article_content = """
## Введение

Текст введения с **жирным** и _курсивом_.

## Основная часть

· Пункт 1
· Пункт 2
· Пункт 3

[Ссылка](https://example.com)
"""

result = tph.create_page(
    title="Моя статья",
    content=article_content
)

if result["success"]:
    print(f"📰 URL: {result['url']}")
else:
    print(f"❌ Ошибка: {result['error']}")
```

### Пример 3: Публикация с анонсом в Telegram

```python
from ai_journalist import TelegraphClient, TelegramClient

tph = TelegraphClient()
tg = TelegramClient()

# Публикуем статью
article = tph.create_page(
    title="PHP 8.4: полное руководство",
    content="Содержимое статьи..."
)

# Создаём анонс
announcement = tph.create_announcement_post(
    article_url=article["url"],
    title="PHP 8.4: полное руководство",
    description="Разбираем новые фичи"
)

# Публикуем анонс (уже экранирован)
result = tg.send_message(announcement, auto_escape=False)
```

---

## 📚 API Документация

### TelegramClient

#### Инициализация

```python
tg = TelegramClient(config_path="/root/git/AI-journalist-bot/config.json")
```

#### send_message()

Отправить сообщение в Telegram канал.

```python
result = tg.send_message(
    text="Текст сообщения",
    parse_mode="MarkdownV2",  # или "HTML", None
    auto_escape=True,         # Автоматически экранировать
    disable_notification=False
)
```

**Возвращает:**
```python
{
    "success": True,
    "message_id": 123,
    "chat_id": "-100XXXXXXXXXX",
    "url": "https://t.me/channel/123"
}
```

#### send_message_with_image()

Отправить сообщение с изображением.

```python
result = tg.send_message_with_image(
    text="Подпись к фото",
    image_path="/path/to/image.jpg"
)
```

#### edit_message()

Редактировать сообщение.

```python
result = tg.edit_message(
    message_id=123,
    text="Новый текст"
)
```

#### delete_message()

Удалить сообщение.

```python
result = tg.delete_message(message_id=123)
```

#### get_bot_info()

Получить информацию о боте.

```python
info = tg.get_bot_info()
# {"success": True, "username": "bot_name", ...}
```

#### test_connection()

Проверить соединение.

```python
if tg.test_connection():
    print("✅ Бот работает")
```

#### send_to_user()

Отправить сообщение пользователю в ЛС.

```python
result = tg.send_to_user(
    user_id=5610580916,
    text="Личное сообщение"
)
```

#### send_draft_for_approval()

Отправить черновик на утверждение.

```python
result = tg.send_draft_for_approval(
    user_id=5610580916,
    text="Текст черновика",
    category="news"
)
```

---

### TelegraphClient

#### Инициализация

```python
tph = TelegraphClient(config_path="/root/git/AI-journalist-bot/telegraph_config.json")
```

#### create_page()

Создать статью на Telegra.ph.

```python
result = tph.create_page(
    title="Заголовок статьи",
    content="Текст в Markdown",
    author_name="AI Journalist",
    author_url="https://t.me/JeBanceOnline"
)
```

**Возвращает:**
```python
{
    "success": True,
    "url": "https://telegra.ph/Title-03-26",
    "path": "Title-03-26",
    "views": 0
}
```

#### edit_page()

Редактировать статью.

```python
result = tph.edit_page(
    path="Title-03-26",
    title="Новый заголовок",
    content="Новое содержимое"
)
```

#### get_page()

Получить информацию о странице.

```python
page = tph.get_page(path="Title-03-26", return_content=True)
```

#### get_account_info()

Получить информацию об аккаунте.

```python
info = tph.get_account_info()
# {"page_count": 42, "short_name": "AI Journalist", ...}
```

#### publish_with_announcement()

Опубликовать статью и анонс в Telegram.

```python
result = tph.publish_with_announcement(
    title="Статья",
    content="Содержимое",
    description="Краткое описание",
    telegram_publish=True,
    emoji="📖"
)
```

---

### Форматирование

#### escape_markdown_v2()

Экранировать специальные символы.

```python
from ai_journalist import escape_markdown_v2

text = "PHP 8.4 > 8.3 #тег"
escaped = escape_markdown_v2(text)
# "PHP 8\\.4 \\> 8\\.3 \\#тег"
```

#### format_post()

Сформировать пост для Telegram.

```python
from ai_journalist import format_post

post = format_post(
    title="Node.js security релиз",
    content="Исправлены 9 уязвимостей",
    hashtags=["nodejs", "security"],
    emoji="🔒",
    sources=["Node.js Blog", "GitHub"]
)
```

#### format_news_post()

Сформировать пост с новостью по шаблону.

```python
from ai_journalist import format_news_post

post = format_news_post(
    headline="Node.js выпустил security патчи",
    summary="Исправлены критические уязвимости",
    details=[
        "CVE-2026-21637 (High) — DoS",
        "CVE-2026-21710 (High) — DoS"
    ],
    category="javascript",
    sources=["Node.js Blog"]
)
```

#### format_tutorial_post()

Сформировать пост-туториал.

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

#### format_telegraph_article()

Сформировать статью для Telegra.ph.

```python
from ai_journalist import format_telegraph_article

article = format_telegraph_article(
    title="PHP 8.4: полное руководство",
    introduction="Обзор новых фич",
    sections=[
        {"heading": "Property Hooks", "content": "Описание...", "type": "text"},
        {"heading": "Пример кода", "content": "code here", "type": "code"}
    ],
    conclusion="Выводы",
    sources=["PHP.net"]
)
```

---

## 📁 Структура библиотеки

```
/root/git/AI-journalist/lib/
├── __init__.py              # Главный модуль (импорт)
├── telegram_client.py       # Telegram Bot API
├── telegraph_client.py      # Telegra.ph API
├── formatting.py            # Утилиты форматирования
└── README.md                # Эта документация
```

---

## 🔧 Конфигурация

### Telegram Bot

Файл: `/root/git/AI-journalist-bot/config.json`

```json
{
  "token": "ВАШ_ТОКЕН_БОТА",
  "channel_id": "-100XXXXXXXXXX"
}
```

### Telegra.ph

Файл: `/root/git/AI-journalist-bot/telegraph_config.json`

```json
{
  "short_name": "AI Journalist",
  "author_name": "AI Journalist",
  "author_url": "https://t.me/JeBanceOnline",
  "access_token": "d3b5... (получить через get_telegraph_token.py)"
}
```

---

## ⚠️ Важные правила

### 1. Всегда используйте auto_escape=True

```python
# ✅ Правильно:
tg.send_message("Текст с #хэштегами и 8.4 версиями")

# ❌ Неправильно (придётся экранировать вручную):
tg.send_message(escaped_text, auto_escape=False)
```

### 2. Проверяйте результат публикации

```python
result = tg.send_message("Текст")

if result["success"]:
    print(f"Message ID: {result['message_id']}")
else:
    print(f"Ошибка: {result['error']}")
```

### 3. Записывайте в историю

```python
# После успешной публикации:
# 1. Обновите 06_history/01_published_posts.md
# 2. Обновите 06_history/02_topics_covered.md
```

---

## 📊 Поддерживаемые символы Markdown

### Telegram MarkdownV2

| Элемент | Синтаксис | После экранирования |
|---------|-----------|---------------------|
| Жирный | `*текст*` | `\*текст\*` |
| Курсив | `_текст_` | `\_текст\_` |
| Код | `` `текст` `` | `` \`текст\` `` |
| Ссылка | `[текст](url)` | `\[текст\](url)` |
| Хэштег | `#тег` | `\#тег` |

### Telegra.ph Markdown

| Элемент | Синтаксис |
|---------|-----------|
| Заголовки | `#`, `##`, `###` |
| Жирный | `**текст**` |
| Курсив | `_текст_` |
| Код | ```` ```код``` ```` |
| Списки | `· `, `- ` |
| Ссылки | `[текст](url)` |

---

## 🐛 Решение проблем

### Ошибка: "Bad Request: can't parse entities"

**Причина:** Неправильное экранирование MarkdownV2

**Решение:**
```python
# Используйте auto_escape=True:
tg.send_message(text, auto_escape=True)
```

### Ошибка: "No access token"

**Причина:** Не получен токен Telegra.ph

**Решение:**
```bash
python3 get_telegraph_token.py
```

### Ошибка: "Chat not found"

**Причина:** Бот не в администраторах канала

**Решение:**
1. Добавьте бота в администраторы канала
2. Проверьте chat_id в config.json

---

## 📞 Контакты

**Канал:** @JeBanceOnline
**Бот:** @JeBanceOnlineBot
**Владелец:** @JeBance (ID: 5610580916)

---

**Версия:** 1.0.0
**Дата:** 2026-03-26
