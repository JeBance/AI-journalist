#!/usr/bin/env python3
"""
Backfill content from Telegra.ph API.
Directly updates articles.json and markdown files.
Fuzzy title matching to handle emoji/title differences.
"""

import re
import json
import time
import subprocess
from pathlib import Path

HISTORY_DIR = Path("/root/git/AI-journalist/06_history")
ARTICLES_FILE = Path("/root/git/AI-journalist/articles.json")
DELAY = 1.0


def fetch_content(telegraph_url):
    try:
        path = telegraph_url.replace("https://telegra.ph/", "")
        url = f"https://api.telegra.ph/getPage/{path}?return_content=true"
        result = subprocess.run(
            ["curl", "-s", "--connect-timeout", "10", "--max-time", "15", url],
            capture_output=True, text=True, timeout=20
        )
        if not result.stdout.strip():
            return None
        data = json.loads(result.stdout)
        if data.get("ok") and data.get("result", {}).get("content"):
            return telegraph_nodes_to_markdown(data["result"]["content"])
    except Exception as e:
        print(f"    Error: {e}")
    return None


def telegraph_nodes_to_markdown(nodes):
    if not isinstance(nodes, list):
        return ""
    md = []
    for node in nodes:
        tag = node.get("tag", "")
        children = node.get("children", [])
        text = _nodes_to_text(children)
        if tag == "p":
            md.append(text)
        elif tag in ("h3", "h4"):
            md.append(f"## {text}")
        elif tag == "h1":
            md.append(f"# {text}")
        elif tag == "ul":
            for child in children:
                if child.get("tag") == "li":
                    md.append(f"- {_nodes_to_text(child.get('children', []))}")
        elif tag == "ol":
            for i, child in enumerate(children, 1):
                if child.get("tag") == "li":
                    md.append(f"{i}. {_nodes_to_text(child.get('children', []))}")
        elif tag == "blockquote":
            md.append(f"> {text}")
        elif tag == "pre":
            md.append(f"```\n{text}\n```")
        elif tag == "figure":
            src = node.get("attrs", {}).get("src", "")
            if src:
                caption = _nodes_to_text(children)
                md.append(f"![{caption}]({src})")
        elif tag == "hr":
            md.append("---")
    return "\n\n".join(md)


def _nodes_to_text(children):
    if not children:
        return ""
    if isinstance(children, str):
        return children
    parts = []
    for child in children:
        if isinstance(child, str):
            parts.append(child)
        elif isinstance(child, dict):
            sub = _nodes_to_text(child.get("children", []))
            tag = child.get("tag", "")
            if tag == "a":
                href = child.get("attrs", {}).get("href", "")
                parts.append(f"[{sub}]({href})" if sub else "")
            elif tag == "strong":
                parts.append(f"**{sub}**")
            elif tag == "em":
                parts.append(f"_{sub}_")
            elif tag == "code":
                parts.append(f"`{sub}`")
            else:
                parts.append(sub)
    return "".join(parts)


def load_monthly_files():
    """Load all monthly files into a dict: filepath -> content."""
    files = {}
    pattern = re.compile(r"published_posts_(\d{4}-\d{2})\.md")
    for f in HISTORY_DIR.iterdir():
        if pattern.match(f.name):
            with open(f, "r", encoding="utf-8") as fh:
                files[f] = fh.read()
    return files


def find_article_in_content(file_content, date_str, title):
    """Find article position in file content using fuzzy matching."""
    # Try exact date+title first
    patterns = [
        rf"### \[{re.escape(date_str)}\] {re.escape(title)}",
        # Try without leading emoji
        rf"### \[{re.escape(date_str)}\] .{{0,5}}{re.escape(title[15:])}",
        # Try matching just the last 40 chars of title
        rf"### \[{re.escape(date_str)}\] .*{re.escape(title[-40:])}" if len(title) > 40 else None,
    ]
    patterns = [p for p in patterns if p]

    for pattern in patterns:
        match = re.search(pattern, file_content)
        if match:
            return match
    return None


def inject_content(file_content, match_pos, title, content):
    """Inject content into file content at the position after title."""
    # Find the "---" after this article entry
    after_title = file_content[match_pos.end():]
    sep_match = re.search(r"\n---\n", after_title)

    if sep_match:
        insert_pos = match_pos.end() + sep_match.start()
        # Check if content block already exists
        existing = re.search(r"<!-- CONTENT_START -->.*?<!-- CONTENT_END -->",
                           file_content[match_pos.end():insert_pos], re.DOTALL)
        if existing:
            return file_content  # Already has content

        new_content = (file_content[:insert_pos] +
                       "\n<!-- CONTENT_START -->\n" + content + "\n<!-- CONTENT_END -->" +
                       file_content[insert_pos:])
    else:
        new_content = file_content + "\n<!-- CONTENT_START -->\n" + content + "\n<!-- CONTENT_END -->\n\n---\n"

    return new_content


def main():
    print("=" * 60)
    print("Backfilling content from Telegra.ph (v3 - fuzzy match)")
    print("=" * 60)

    with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
        articles = json.load(f)

    to_fetch = [a for a in articles if not a.get("content") and a.get("telegraph_url")]
    print(f"Articles to fetch: {len(to_fetch)}")
    print()

    # Load all monthly files
    monthly_files = load_monthly_files()
    print(f"Loaded {len(monthly_files)} monthly files")

    success = 0
    failed = 0

    for i, article in enumerate(to_fetch):
        title = article["title"]
        url = article["telegraph_url"]
        date = article["date"]

        print(f"[{i+1}/{len(to_fetch)}] {title[:55]}...", end=" ", flush=True)

        content = fetch_content(url)
        if content and len(content) > 20:
            # Update articles.json
            article["content"] = content

            # Find and update monthly file
            month = date[:7]
            target_file = None
            for fp in monthly_files:
                if month in fp.name:
                    target_file = fp
                    break

            if target_file and target_file in monthly_files:
                match = find_article_in_content(monthly_files[target_file], date, title)
                if match:
                    monthly_files[target_file] = inject_content(
                        monthly_files[target_file], match, title, content)
                    print(f"OK ({len(content)} chars)")
                    success += 1
                else:
                    print(f"NOT_FOUND_IN_FILE")
                    failed += 1
            else:
                print(f"NO_MONTHLY_FILE")
                failed += 1
        else:
            failed += 1
            print("FETCH_FAILED")

        if i < len(to_fetch) - 1:
            time.sleep(DELAY)

        # Save progress every 10
        if (i + 1) % 10 == 0:
            with open(ARTICLES_FILE, "w", encoding="utf-8") as f:
                json.dump(articles, f, indent=2, ensure_ascii=False)

    # Save articles.json
    with open(ARTICLES_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

    # Save updated monthly files
    for fp, content in monthly_files.items():
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"\n{'=' * 60}")
    print(f"Done! Success: {success}, Failed: {failed}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
