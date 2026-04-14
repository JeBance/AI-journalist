#!/usr/bin/env python3
"""
AI-journalist -- articles.json generator

Parses markdown files from 06_history/ and creates a unified articles.json
for the ai.jebance.ru website.

Extracts full article content from <!-- CONTENT_START --> blocks.

Usage:
    python3 generate_json.py
"""

import re
import json
from pathlib import Path

HISTORY_DIR = Path(__file__).parent / "06_history"
OUTPUT_FILE = Path(__file__).parent / "articles.json"

# Emoji map for all categories
EMOJI_MAP = {
    # AI / ML
    "ai": "\U0001f916",
    "ai_tools": "\U0001f916",
    "ai_generated": "\U0001f916",
    "ai_models": "\U0001f916",
    "llm": "\U0001f916",
    "openai": "\U0001f916",
    "anthropic": "\U0001f916",
    "mistral": "\U0001f32b\ufe0f",
    "huggingface": "\U0001f917",
    "ollama": "\U0001f999",
    "cohere": "\U0001f399\ufe0f",

    # Languages
    "javascript": "\U0001f7e8",
    "typescript": "\U0001f535",
    "python": "\U0001f40d",
    "rust": "\U0001f980",
    "golang": "\U0001f535",
    "php": "\U0001f418",
    "java": "\u2615",
    "kotlin": "\U0001f7e0",
    "ruby": "\U0001f48e",
    "swift": "\U0001f54a\ufe0f",
    "zig": "\U0001f4a5",

    # Web / Frontend
    "react": "\u269b\ufe0f",
    "vuejs": "\U0001f7a9",
    "svelte": "\U0001f525",
    "nextjs": "\u25b2",
    "nuxt": "\U0001f7a9",
    "astro": "\u2728",
    "vite": "\u26a1",
    "css": "\U0001f3a8",
    "html": "\U0001f4c4",
    "solidjs": "\U0001f9ca",
    "flutter": "\U0001f98b",
    "webassembly": "\U0001f4e6",

    # Backend / Tools
    "nodejs": "\U0001f7e9",
    "NodeJS": "\U0001f7e9",
    "bun": "\U0001f35e",
    "deno": "\U0001f995",
    "npm": "\U0001f4e6",
    "pnpm": "\U0001f4e6",
    "laravel": "\U0001f53a",
    "symfony": "\U0001f3b5",
    "prisma": "\U0001f52e",
    "supabase": "\U0001f7e2",

    # Databases
    "databases": "\U0001f5c4\ufe0f",
    "postgresql": "\U0001f418",
    "sqlite": "\U0001f4d1",
    "redis": "\U0001f534",
    "valkey": "\U0001f511",
    "elasticsearch": "\U0001f50d",
    "meilisearch": "\U0001f50d",
    "grafana": "\U0001f4ca",

    # DevOps / Infra
    "devops": "\U0001f433",
    "docker": "\U0001f433",
    "kubernetes": "\u2388\ufe0f",
    "nginx": "\U0001f6e1\ufe0f",
    "terraform": "\U0001f3d7\ufe0f",
    "github": "\U0001f431",
    "gitlab": "\U0001f98a",
    "git": "\U0001f4c9",
    "vscode": "\U0001f4bb",
    "visualstudio": "\U0001f4bb",
    "jetbrains": "\U0001f4a1",
    "intellij": "\U0001f4a1",
    "intellijidea": "\U0001f4a1",
    "aws": "\u2601\ufe0f",
    "cloudflare": "\u2601\ufe0f",
    "ubuntu": "\U0001f7e7",
    "fedora": "\U0001f535",
    "linux": "\U0001f427",

    # Security / Privacy
    "security": "\U0001f512",
    "privacy": "\U0001f576\ufe0f",
    "vpn_security": "\U0001f512",

    # Platforms / Companies
    "google": "\U0001f50d",
    "microsoft": "\U0001f5d3\ufe0f",
    "apple": "\U0001f34e",
    "android": "\U0001f916",
    "samsung": "\U0001f4f1",
    "nvidia": "\U0001f7e9",
    "amd": "\U0001f534",
    "intel": "\U0001f535",
    "telegram": "\u2708\ufe0f",
    "discord": "\U0001f3ae",
    "bluesky": "\U0001f535",
    "figma": "\U0001f3a8",
    "ethereum": "\U0001f4b0",
    "godot": "\U0001f47e",

    # Other
    "hardware": "\U0001f4bb",
    "tutorial": "\U0001f4da",
    "news": "\U0001f4f0",
    "web": "\U0001f310",
    "mobile": "\U0001f4f1",
    "opensource": "\U0001f4e6",
    "developer_tools": "\U0001f6e0\ufe0f",
    "patterns": "\U0001f4d0",
    "chrome": "\U0001f310",
    "firefox": "\U0001f98a",
    "ffmpeg": "\U0001f3ac",
    "ocr": "\U0001f4dd",
    "arm": "\U0001f527",
    "dotnet": "\U0001f535",
    "opentelemetry": "\U0001f4a1",
    "phpmyadmin": "\U0001f418",
    "test": "\U0001f9ea",

    "default": "\U0001f4d6",
}


def parse_monthly_file(filepath: Path) -> list:
    """Parse one monthly file and return a list of articles."""
    articles = []

    with open(filepath, "r", encoding="utf-8") as f:
        file_content = f.read()

    # Pattern: ### [YYYY-MM-DD] Title\n\n(body)...---
    pattern = r"### \[(\d{4}-\d{2}-\d{2})\] (.+?)\n\n(.*?)(?=---\n\n### \[|---\n\n$|---$)"
    matches = re.findall(pattern, file_content, re.DOTALL)

    for date_str, title, body in matches:
        article = {
            "id": 0,
            "date": date_str,
            "title": title.strip(),
            "category": "",
            "tags": [],
            "description": "",
            "content": "",
            "telegraph_url": "",
            "telegram_id": 0,
            "status": "",
            "sources": [],
            "emoji": "\U0001f4d6",
        }

        # Category
        cat_match = re.search(r"\*\*Category:\*\* (.+)", body)
        if not cat_match:
            cat_match = re.search(r"\*\*\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f:\*\* (.+)", body)
        if cat_match:
            article["category"] = cat_match.group(1).strip()

        # Tags
        tags_match = re.search(r"\*\*Key topics:\*\* (.+)", body)
        if not tags_match:
            tags_match = re.search(r"\*\*\u041a\u043b\u044e\u0447\u0435\u0432\u044b\u0435 \u0442\u0435\u043c\u044b:\*\* (.+)", body)
        if tags_match:
            article["tags"] = [t.strip() for t in tags_match.group(1).split(",") if t.strip()]

        # Sources
        sources = re.findall(r"  - (.+?)(?:\n|$)", body)
        article["sources"] = [s.strip() for s in sources if s.strip()]

        # Telegra.ph URL
        tele_match = re.search(r"\*\*Telegra\.ph URL:\*\* (.+)", body)
        if tele_match:
            article["telegraph_url"] = tele_match.group(1).strip()

        # Telegram ID
        tg_match = re.search(r"\*\*Telegram ID:\*\* (\d+)", body)
        if tg_match:
            article["telegram_id"] = int(tg_match.group(1))

        # Status
        status_match = re.search(r"\*\*Status:\*\* (.+)", body)
        if not status_match:
            status_match = re.search(r"\*\*\u0421\u0442\u0430\u0442\u0443\u0441:\*\* (.+)", body)
        if status_match:
            article["status"] = status_match.group(1).strip()

        # Full article content from <!-- CONTENT_START --> block
        content_match = re.search(r"<!-- CONTENT_START -->(.*?)<!-- CONTENT_END -->", body, re.DOTALL)
        if content_match:
            article["content"] = content_match.group(1).strip()

        # Description
        article["description"] = _generate_description(article)

        # Emoji
        article["emoji"] = EMOJI_MAP.get(article["category"], EMOJI_MAP.get("default"))

        articles.append(article)

    return articles


def _generate_description(article: dict) -> str:
    """Generate a brief description from article data."""
    tags = article["tags"][:5]
    category = article["category"]
    if tags:
        return f"{category}: {', '.join(tags)}"
    return category


def main():
    """Main function."""
    print("=" * 60)
    print("AI-journalist: Generating articles.json")
    print("=" * 60)

    all_articles = []

    pattern = re.compile(r"published_posts_(\d{4}-\d{2})\.md")
    if not HISTORY_DIR.exists():
        print(f"Directory not found: {HISTORY_DIR}")
        return

    for filepath in sorted(HISTORY_DIR.iterdir()):
        if pattern.match(filepath.name):
            articles = parse_monthly_file(filepath)
            all_articles.extend(articles)
            print(f"  Parsed {filepath.name}: {len(articles)} articles")

    # Sort by date (newest first)
    all_articles.sort(key=lambda a: a["date"], reverse=True)

    # Assign IDs
    for i, article in enumerate(all_articles, 1):
        article["id"] = i

    # Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, indent=2, ensure_ascii=False)

    file_size = OUTPUT_FILE.stat().st_size
    articles_with_content = len([a for a in all_articles if a.get("content")])
    print(f"\nDone! articles.json created")
    print(f"  Total: {len(all_articles)} articles")
    print(f"  With content: {articles_with_content}")
    print(f"  Size: {file_size / 1024:.1f} KB")
    print("=" * 60)


if __name__ == "__main__":
    main()
