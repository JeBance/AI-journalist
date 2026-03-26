#!/usr/bin/env python3
"""
Скрипт для отправки отчётов AI-journalist в Telegram боту @JeBanceOnlineBot
"""

import requests
import json
import sys
from pathlib import Path

# Конфигурация AI-journalist bot
CONFIG_FILE = Path("/root/git/AI-journalist-bot/config.json")

# Загрузка конфига
if CONFIG_FILE.exists():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)
    BOT_TOKEN = config.get("token")
else:
    print("❌ Ошибка: config.json не найден!")
    sys.exit(1)

# Ваш Telegram ID
OWNER_ID = 5610580916  # @JeBance


def send_report(text):
    """Отправить текстовый отчёт в Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': OWNER_ID,
        'text': text,
        'parse_mode': None  # Отправляем как простой текст
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("✅ Отчёт отправлен в @JeBanceOnlineBot!")
        return True
    else:
        print(f"❌ Ошибка отправки: {response.status_code}")
        print(f"Ответ: {response.text}")
        return False


if __name__ == '__main__':
    if '-f' in sys.argv and sys.argv.index('-f') + 1 < len(sys.argv):
        # Чтение из файла
        file_idx = sys.argv.index('-f') + 1
        with open(sys.argv[file_idx], 'r', encoding='utf-8') as f:
            send_report(f.read())
    elif len(sys.argv) > 1:
        # Собираем все аргументы в одно сообщение (поддержка пробелов)
        message = ' '.join(sys.argv[1:])
        send_report(message)
    else:
        print("Использование: python3 send_report.py \"Текст отчёта\"")
        print("Или: python3 send_report.py -f файл.txt")
        sys.exit(1)
