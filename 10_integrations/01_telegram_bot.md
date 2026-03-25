# Интеграция с Telegram ботом

## 📋 Назначение

Эта инструкция описывает, как настроить автоматическую публикацию постов из AI-journalist инфраструктуры в Telegram.

---

## 🚀 Быстрая настройка

### Шаг 1: Настроить бота

1. Перейдите в `/root/git/AI-journalist-bot/`
2. Следуйте инструкции из `README.md`
3. Создайте `config.json` с токеном и Chat ID

### Шаг 2: Проверить работу

```bash
cd /root/git/AI-journalist-bot
python3 publisher.py test
```

### Шаг 3: Использовать с AI-агентом

При загрузке инфраструктуры в AI-агента, добавьте инструкцию:

```
Для публикации используй бота из папки AI-journalist-bot.

Пример:
```python
import sys
sys.path.insert(0, '/root/git/AI-journalist-bot')
from publisher import publish

result = publish(текст_поста)
if result["success"]:
    print(f"✅ Опубликовано! Message ID: {result['message_id']}")
```
```

---

## 📝 Обновление workflow

### Изменить `08_workflows/01_daily_publication.md`

В шаге 6 (Публикация) использовать:

**Вариант B: Через бота**

```python
import sys
sys.path.insert(0, '/root/git/AI-journalist-bot')
from publisher import publish

# Публикация поста
result = publish(текст_поста)

if result["success"]:
    telegram_id = result["message_id"]
    print(f"✅ Пост опубликован. ID: {telegram_id}")
else:
    print(f"❌ Ошибка: {result['error']}")
```

---

## 🔄 Полный цикл публикации

### 1. AI исследует источники

```
AI-агент:
1. Читает 01_system_prompts/
2. Исследует 02_sources/
3. Выбирает тему
4. Пишет пост по шаблону из 03_templates/
```

### 2. AI показывает черновик

```
Готовый пост:

{текст поста}

---

Опубликовать этот пост в Telegram?
```

### 3. Пользователь подтверждает

```
Да, публикуй
```

### 4. AI публикует через бота

```python
import sys
sys.path.insert(0, '/root/git/AI-journalist-bot')
from publisher import publish

result = publish(текст_поста)
telegram_id = result["message_id"]
```

### 5. AI записывает в историю

```markdown
### [2026-03-25] Заголовок поста
- **Категория:** php
- **Шаблон:** single_post
- **Telegram ID:** {telegram_id}
- **Статус:** опубликован
```

---

## 📊 Архитектура

```
┌─────────────────┐
│   AI-агент      │
│  (Claude/ChatGPT)│
└────────┬────────┘
         │
         │ Пишет пост
         ↓
┌─────────────────┐
│  publisher.py   │
│  (бот-посредник)│
└────────┬────────┘
         │
         │ Telegram API
         ↓
┌─────────────────┐
│  Telegram       │
│  канал          │
└─────────────────┘
```

---

## ⚙️ Конфигурация

### config.json

```json
{
  "token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
  "channel_id": "-1001234567890"
}
```

**Где взять:**
- `token` — у @BotFather после создания бота
- `channel_id` — через @GetMyIDBot или API

---

## 🐛 Решение проблем

### Бот не публикует

1. Проверьте, что бот в администраторах канала
2. Проверьте права бота (публикация сообщений)
3. Запустите `python3 publisher.py test`

### Ошибка Markdown

1. Проверьте экранирование символов: `_ * [ ] ( ) ~ ` > # + - = | { } . !`
2. Убедитесь, что все теги закрыты

### Ошибка токена

1. Проверьте токен в `config.json`
2. При необходимости получите новый у @BotFather

---

## 📁 Пути

| Компонент | Путь |
|-----------|------|
| AI-journalist инфраструктура | `/root/git/AI-journalist/` |
| Telegram бот | `/root/git/AI-journalist-bot/` |
| Конфигурация бота | `/root/git/AI-journalist-bot/config.json` |

---

## ✅ Чек-лист настройки

- [ ] Бот создан через @BotFather
- [ ] Токен сохранён
- [ ] Бот добавлен в администраторы канала
- [ ] Chat ID получен
- [ ] `config.json` создан и заполнен
- [ ] `python3 publisher.py test` работает
- [ ] AI-агент знает о боте

---

## 🎯 Следующие шаги

1. **Настройте бота** по этой инструкции
2. **Протестируйте** публикацию:
   ```bash
   python3 publisher.py "🔥 *Тестовый пост*
   
   Проверка работы бота\.
   
   #test"
   ```
3. **Используйте с AI-агентом** для регулярных публикаций

---

**Версия:** 1.0  
**Дата:** 2026-03-25
