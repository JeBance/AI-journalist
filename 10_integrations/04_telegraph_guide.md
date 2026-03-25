# Telegra.ph — Полное руководство

## 📚 Официальная документация

**API:** https://api.telegra.ph  
**Методы:** GET/POST  
**Формат:** JSON

---

## 🔑 Основные методы

### createPage

Создание новой статьи.

**Endpoint:**
```
POST https://api.telegra.ph/createPage
```

**Параметры:**

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `access_token` | String | ✅ Да | Токен доступа аккаунта |
| `title` | String | ✅ Да | Заголовок (1-256 символов) |
| `content` | Array | ✅ Да | Контент страницы (до 64 KB) |
| `author_name` | String | ❌ Нет | Имя автора (0-128 символов) |
| `author_url` | String | ❌ Нет | Ссылка на профиль (0-512 символов) |
| `return_content` | Boolean | ❌ Нет | Вернуть контент в ответе |

**Пример запроса:**
```python
import requests
import json

url = "https://api.telegra.ph/createPage"
data = {
    "access_token": "YOUR_TOKEN",
    "title": "Заголовок статьи",
    "content": json.dumps([
        {"tag": "p", "children": ["Текст параграфа"]},
        {"tag": "h3", "children": ["Заголовок раздела"]},
        {"tag": "ul", "children": [
            {"tag": "li", "children": ["Пункт 1"]},
            {"tag": "li", "children": ["Пункт 2"]}
        ]}
    ]),
    "author_name": "Автор",
    "author_url": "https://example.com"
}

response = requests.post(url, json=data)
result = response.json()

if result["ok"]:
    print(result["result"]["url"])
```

---

## 📄 Формат контента (Node Array)

Контент — это **массив узлов (Array of Node)**.

### Типы узлов

**1. Text Node (строка):**
```json
"Просто текст"
```

**2. Element Node (объект):**
```json
{
  "tag": "p",
  "attrs": {},
  "children": [...]
}
```

### Поддерживаемые теги

| Тег | Описание | children |
|-----|----------|----------|
| `p` | Параграф | Текст + inline теги |
| `h3` | Заголовок уровня 3 | Текст |
| `h4` | Заголовок уровня 4 | Текст |
| `ul` | Маркированный список | `li` |
| `ol` | Нумерованный список | `li` |
| `li` | Элемент списка | Текст + inline теги |
| `b`, `strong` | Жирный | Текст |
| `i`, `em` | Курсив | Текст |
| `u` | Подчёркнутый | Текст |
| `s` | Зачёркнутый | Текст |
| `code` | Код | Текст |
| `a` | Ссылка | Текст |
| `blockquote` | Цитата | Текст + inline теги |
| `br` | Перенос строки | — |
| `hr` | Горизонтальная линия | — |
| `img` | Изображение | — |
| `iframe` | Встраиваемый контент | — |
| `figure`, `figcaption` | Фигура с подписью | — |
| `aside` | Боковая заметка | Текст |
| `pre` | Предформатированный текст | Текст |
| `video` | Видео | — |

---

## ✅ Правильные примеры

### Параграф с форматированием

```json
{
  "tag": "p",
  "children": [
    "Текст с ",
    {"tag": "b", "children": ["жирным"]},
    " и ",
    {"tag": "i", "children": ["курсивом"]}
  ]
}
```

### Заголовок

```json
{
  "tag": "h3",
  "children": ["Заголовок раздела"]
}
```

### Список (правильно!)

```json
{
  "tag": "ul",
  "children": [
    {"tag": "li", "children": ["Пункт 1"]},
    {"tag": "li", "children": ["Пункт 2"]},
    {"tag": "li", "children": ["Пункт 3"]}
  ]
}
```

### Ссылка

```json
{
  "tag": "p",
  "children": [
    "Читать на ",
    {
      "tag": "a",
      "attrs": {"href": "https://example.com"},
      "children": ["сайте"]
    }
  ]
}
```

### Цитата

```json
{
  "tag": "blockquote",
  "children": ["Текст цитаты"]
}
```

### Код

```json
{
  "tag": "p",
  "children": [
    "Используй ",
    {"tag": "code", "children": ["print()"]},
    " для вывода"
  ]
}
```

---

## ❌ Неправильные примеры

### Список без ul/ol

```json
// ❌ НЕПРАВИЛЬНО:
[
  {"tag": "li", "children": ["Пункт 1"]},
  {"tag": "li", "children": ["Пункт 2"]}
]

// ✅ ПРАВИЛЬНО:
[
  {
    "tag": "ul",
    "children": [
      {"tag": "li", "children": ["Пункт 1"]},
      {"tag": "li", "children": ["Пункт 2"]}
    ]
  }
]
```

### Пустой параграф

```json
// ❌ НЕПРАВИЛЬНО:
{"tag": "p", "children": []}

// ✅ ПРАВИЛЬНО:
// Просто не добавляй пустой параграф
```

---

## 🔄 Полный пример статьи

```json
[
  {"tag": "h3", "children": ["Введение"]},
  {"tag": "p", "children": ["Текст введения"]},
  
  {"tag": "h3", "children": ["Основная часть"]},
  {"tag": "p", "children": ["Текст с ", {"tag": "b", "children": ["жирным"]}]},
  
  {"tag": "ul", "children": [
    {"tag": "li", "children": ["Пункт 1"]},
    {"tag": "li", "children": ["Пункт 2"]}
  ]},
  
  {"tag": "blockquote", "children": ["Цитата"]},
  
  {"tag": "hr"},
  
  {"tag": "p", "children": [
    "Источники: ",
    {"tag": "a", "attrs": {"href": "https://example.com"}, "children": ["ссылка"]}
  ]}
]
```

---

## 🛠️ Python конвертер Markdown → Telegra.ph

### Правила конвертации

1. **Пустая строка** → закрывает параграф и список
2. **`# `, `## `, `### `** → `h3`
3. **`- `, `· `** → добавляет `li` в текущий `ul`
4. **`> `** → `blockquote`
5. **Обычный текст** → накапливается в параграф
6. **`**текст**`** → `<b>текст</b>`
7. **`_текст_`** → `<i>текст</i>`
8. **`` `текст` ``** → `<code>текст</code>`
9. **`[текст](url)`** → `<a href="url">текст</a>`

### Алгоритм

```python
def create_telegraph_content(markdown_text):
    content = []
    lines = markdown_text.split('\n')
    
    current_paragraph = []
    current_list = []
    in_list = False
    
    for line in lines:
        line = line.strip()
        
        if not line:
            # Закрываем параграф и список
            if current_paragraph:
                content.append({"tag": "p", "children": [" ".join(current_paragraph)]})
                current_paragraph = []
            
            if in_list and current_list:
                content.append({"tag": "ul", "children": current_list})
                current_list = []
                in_list = False
            continue
        
        # Обработка заголовков, списков, цитат, текста...
    
    # Добавляем остаток
    if current_paragraph:
        content.append({"tag": "p", "children": [" ".join(current_paragraph)]})
    
    if in_list and current_list:
        content.append({"tag": "ul", "children": current_list})
    
    return content
```

---

## 📊 Ответ API

### Успешный ответ

```json
{
  "ok": true,
  "result": {
    "path": "Article-Title-03-25",
    "url": "https://telegra.ph/Article-Title-03-25",
    "title": "Article Title",
    "description": "Краткое описание",
    "author_name": "Author Name",
    "views": 0,
    "can_edit": true
  }
}
```

### Ошибки

```json
{
  "ok": false,
  "error": "ACCESS_TOKEN_INVALID"
}
```

```json
{
  "ok": false,
  "error": "TITLE_TOO_LONG"
}
```

---

## 💡 Лучшие практики

### 1. Структура статьи

- Заголовок `h3` в начале
- Короткие параграфы (2-4 предложения)
- Списки для перечислений
- Пустые строки между секциями

### 2. Форматирование

- Жирный для акцентов
- Курсив для терминов
- Код для технических терминов
- Ссылки для источников

### 3. Списки

- Всегда оборачивай в `ul` или `ol`
- Каждый `li` с новой строки
- Пустая строка перед списком

### 4. Изображения

Telegra.ph поддерживает `img`:

```json
{
  "tag": "img",
  "attrs": {
    "src": "https://example.com/image.jpg"
  }
}
```

### 5. Редактирование

- Статьи можно редактировать 24 часа
- Используйте `editPage` метод
- Нужен тот же `access_token`

---

## 🔗 Полезные ссылки

- **Официальная документация:** https://core.telegram.org/telegraph
- **API референс:** https://telegra.ph/api
- **Создать аккаунт:** https://api.telegra.ph/createAccount

---

**Версия:** 1.0  
**Дата:** 2026-03-25  
**Статус:** Актуально
