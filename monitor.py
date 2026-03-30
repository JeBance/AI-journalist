#!/usr/bin/env python3
"""
AI-journalist Monitor

Отправляет алерты в Telegram при ошибках публикации.
Проверяет логи systemd за последние 24 часа.

Использование:
    python3 /root/git/AI-journalist/monitor.py
"""

import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

TELEGRAM_REPORT_SCRIPT = Path("/root/git/AI-journalist/send_report.py")
LOG_THRESHOLD = 24  # часов


def get_journalctl_logs(hours: int = 24) -> str:
    """Получить логи systemd за последние N часов."""
    try:
        result = subprocess.run(
            ["journalctl", "-u", "ai-journalist-5min.service", "--since", f"{hours} hours ago", "--no-pager"],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout
    except Exception as e:
        return f"Ошибка получения логов: {e}"


def analyze_logs(logs: str) -> dict:
    """Анализировать логи и найти ошибки."""
    lines = logs.split('\n')
    
    stats = {
        "total_runs": 0,
        "successful": 0,
        "failed": 0,
        "duplicate_blocked": 0,
        "last_success": None,
        "last_failure": None,
        "errors": []
    }
    
    for line in lines:
        if "ПУБЛИКАЦИЯ ЗАВЕРШЕНА" in line or "published" in line.lower():
            stats["successful"] += 1
            stats["last_success"] = line.split()[0] + " " + line.split()[1]
        
        if "Failed with result" in line or "FAILURE" in line:
            stats["failed"] += 1
            stats["last_failure"] = line.split()[0] + " " + line.split()[1]
        
        if "ДУБЛИКАТ" in line or "дубликат" in line.lower():
            stats["duplicate_blocked"] += 1
        
        if "error" in line.lower() or "❌" in line:
            stats["errors"].append(line.strip())
    
    # Подсчёт запусков
    stats["total_runs"] = stats["successful"] + stats["failed"]
    
    return stats


def format_alert(stats: dict) -> str:
    """Сформатировать сообщение для Telegram."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    message = f"🔍 AI-JOURNALIST МОНИТОРИНГ\n"
    message += f"📅 {now}\n\n"
    
    message += f"📊 СТАТИСТИКА ЗА {LOG_THRESHOLD} Ч:\n"
    message += f"• Всего запусков: {stats['total_runs']}\n"
    message += f"• Успешно: {stats['successful']}\n"
    message += f"• Ошибки: {stats['failed']}\n"
    message += f"• Заблокировано (дубликаты): {stats['duplicate_blocked']}\n\n"
    
    if stats['last_success']:
        message += f"✅ Последняя успешная: {stats['last_success']}\n"
    
    if stats['last_failure']:
        message += f"❌ Последняя ошибка: {stats['last_failure']}\n"
    
    if stats['failed'] > 0:
        message += f"\n⚠️ ТРЕБУЕТСЯ ВНИМАНИЕ!\n"
        message += f"Проверьте логи: journalctl -u ai-journalist-5min.service\n"
    
    if stats['duplicate_blocked'] > 3:
        message += f"\n🚫 МНОГО ДУБЛИКАТОВ ({stats['duplicate_blocked']})!\n"
        message += f"Рекомендуется расширить пул источников.\n"
    
    return message


def send_alert(message: str):
    """Отправить алерт в Telegram."""
    if not TELEGRAM_REPORT_SCRIPT.exists():
        print(f"❌ Скрипт не найден: {TELEGRAM_REPORT_SCRIPT}")
        return False
    
    try:
        result = subprocess.run(
            ["python3", str(TELEGRAM_REPORT_SCRIPT), message],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Алерт отправлен")
            return True
        else:
            print(f"❌ Ошибка отправки: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


def main():
    """Главная функция."""
    print("=" * 60)
    print("🔍 AI-JOURNALIST МОНИТОРИНГ")
    print("=" * 60)
    
    # Получение логов
    print(f"\n📄 Загрузка логов за {LOG_THRESHOLD} ч...")
    logs = get_journalctl_logs(LOG_THRESHOLD)
    
    if not logs:
        print("❌ Логи не найдены")
        return False
    
    print(f"✅ Загружено {len(logs.split(chr(10)))} строк логов")
    
    # Анализ
    print("\n📊 Анализ логов...")
    stats = analyze_logs(logs)
    
    # Форматирование алерта
    alert = format_alert(stats)
    
    print("\n" + "=" * 60)
    print(alert)
    print("=" * 60)
    
    # Отправка
    print("\n📢 Отправка алерта...")
    success = send_alert(alert)
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
