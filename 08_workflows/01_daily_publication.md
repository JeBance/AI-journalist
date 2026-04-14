# Workflow: Daily Publication

## Goal

Publish one quality post (or digest) to the Telegram channel based on fresh news from the last 24-48 hours.

**Execution time:** 10-15 minutes
**Frequency:** Daily

---

## Steps

### Step 1: Init (1 min)

1. Read `01_system_prompts/01_role_and_mission.md`
2. Open `06_history/01_published_posts.md` -- check recent publications
3. Open `06_history/02_topics_covered.md` -- check recently covered topics

### Step 2: Research (5-7 min)

Follow the protocol from `01_system_prompts/02_research_protocol.md`

### Step 3: Selection (2 min)

1. Collect findings in `07_research_cache/03_temp_notes.md`
2. Prioritize: critical > important > optional
3. Check uniqueness in `06_history/02_topics_covered.md`

### Step 4: Writing (3-5 min)

1. Use templates from `03_templates/`
2. Follow rules from `04_style/`
3. Add source links and tags from `05_categories/`

### Step 5: Publish (1 min)

Run `publisher_final.py` with the article data. It will:
- Publish to Telegra.ph
- Publish announcement to Telegram
- Record history with full content
- Generate articles.json
- Git push to GitHub

### Step 6: History (automatic)

`publisher_final.py` handles this automatically:

1. Adds entry to monthly file `06_history/published_posts_YYYY-MM.md`
2. Entry format:

```markdown
### [YYYY-MM-DD] {Title}

- **Category:** {category}
- **Template:** {template}
- **Key topics:** {tags}
- **Sources:**
  - {name} ({URL})
- **Telegra.ph URL:** {url}
- **Telegram ID:** {id}
- **Status:** published

<!-- CONTENT_START -->
{full article content in markdown}
<!-- CONTENT_END -->

---
```

3. Updates `02_topics_covered.md` with the topic and next repeat date.

---

## Checklist

- [ ] Read role instructions
- [ ] Check publication history
- [ ] Research GitHub, RSS, Telegram, blogs
- [ ] Select unique topic
- [ ] Write post by template
- [ ] Auto-publish via `publisher_final.py`
- [ ] History recorded automatically
- [ ] User notified: "Post published. ID: {id}"
