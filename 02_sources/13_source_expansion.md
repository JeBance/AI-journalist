# Расширение пула источников AI-journalist

## 📊 Текущее состояние

| Тип источников | Количество | Файл |
|----------------|------------|------|
| RSS-ленты | 15+ | `01_rss_feeds.md` |
| GitHub репозитории | 20+ | `02_github_repos.md` |
| Telegram-каналы | 10+ | `03_telegram_channels.md` |
| Технические блоги | 15+ | `04_technical_blogs.md` |
| Крипто RSS | 16+ | `09_crypto_rss_feeds.md` |
| Крипто GitHub | 23+ | `10_crypto_github_repos.md` |
| Крипто Telegram | 14+ | `11_crypto_telegram_channels.md` |
| Крипто блоги | 22+ | `12_crypto_blogs.md` |

**Итого:** 100+ источников

---

## 🔮 Рекомендуемые новые источники

### 1. AI и Machine Learning (ПРИОРИТЕТ)

#### RSS-ленты:
```markdown
### arXiv AI Papers
- **URL:** https://arxiv.org/list/cs.AI/recent
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** ai_tools
- **Описание:** Научные статьи по AI/ML

### Hugging Face Blog
- **URL:** https://huggingface.co/blog/feed.xml
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** ai_tools
- **Описание:** AI модели, датасеты, инструменты

### The Batch (DeepLearning.AI)
- **URL:** https://www.deeplearning.ai/the-batch/
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** ai_tools
- **Описание:** Еженедельная рассылка от Эндрю Ына

### Import AI
- **URL:** https://jack-clark.net/feed/
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** ai_tools
- **Описание:** Еженедельный дайджест AI-новостей

### OpenAI Blog
- **URL:** https://openai.com/blog/rss
- **Тип:** RSS
- **Приоритет:** Критический
- **Категория:** ai_tools
- **Описание:** Официальный блог OpenAI

### Anthropic Blog
- **URL:** https://www.anthropic.com/news/rss
- **Тип:** RSS
- **Приоритет:** Критический
- **Категория:** ai_tools
- **Описание:** Новости от создателей Claude

### Google AI Blog
- **URL:** https://ai.google/blog/rss
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** ai_tools
- **Описание:** Исследования Google AI

### Microsoft Research Blog
- **URL:** https://www.microsoft.com/en-us/research/feed/
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** ai_tools
- **Описание:** Исследования Microsoft AI
```

#### GitHub репозитории:
```markdown
### Hugging Face Transformers
- **URL:** https://github.com/huggingface/transformers
- **Приоритет:** Критический
- **Категория:** ai_tools
- **Описание:** Библиотека трансформеров
- **Что следить:** Releases, New models

### LangChain
- **URL:** https://github.com/langchain-ai/langchain
- **Приоритет:** Высокий
- **Категория:** ai_tools
- **Описание:** Фреймворк для LLM-приложений
- **Что следить:** Releases, Integrations

### LlamaIndex
- **URL:** https://github.com/run-llama/llama_index
- **Приоритет:** Высокий
- **Категория:** ai_tools
- **Описание:** Интеграция LLM с данными
- **Что следить:** Releases, New features

### Ollama
- **URL:** https://github.com/ollama/ollama
- **Приоритет:** Высокий
- **Категория:** ai_tools
- **Описание:** Локальный запуск LLM
- **Что следить:** Releases, New models

### vLLM
- **URL:** https://github.com/vllm-project/vllm
- **Приоритет:** Средний
- **Категория:** ai_tools
- **Описание:** Высокопроизводительный inference
- **Что следить:** Releases, Performance

### Replicate
- **URL:** https://github.com/replicate/replicate
- **Приоритет:** Средний
- **Категория:** ai_tools
- **Описание:** Запуск ML-моделей в облаке
- **Что следить:** Releases, New models
```

---

### 2. DevOps и Cloud

#### RSS-ленты:
```markdown
### Kubernetes Blog
- **URL:** https://kubernetes.io/feed.xml
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** devops
- **Описание:** Официальный блог Kubernetes

### Docker Blog
- **URL:** https://www.docker.com/blog/feed/
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** devops
- **Описание:** Новости Docker

### AWS News Blog
- **URL:** https://aws.amazon.com/blogs/aws/feed/
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** devops
- **Описание:** Новости AWS

### Google Cloud Blog
- **URL:** https://cloud.google.com/blog/products/feed
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** devops
- **Описание:** Новости Google Cloud

### Azure Blog
- **URL:** https://azure.microsoft.com/en-us/blog/feed/
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** devops
- **Описание:** Новости Microsoft Azure

### GitHub Actions Blog
- **URL:** https://github.blog/changelog/label:github-actions/
- **Тип:** RSS
- **Приоритет:** Средний
- **Категория:** devops
- **Описание:** Новости GitHub Actions
```

#### GitHub репозитории:
```markdown
### Kubernetes
- **URL:** https://github.com/kubernetes/kubernetes
- **Приоритет:** Критический
- **Категория:** devops
- **Описание:** Оркестрация контейнеров
- **Что следить:** Releases, Security patches

### Docker
- **URL:** https://github.com/docker/cli
- **Приоритет:** Высокий
- **Категория:** devops
- **Описание:** Docker CLI
- **Что следить:** Releases, New features

### Terraform
- **URL:** https://github.com/hashicorp/terraform
- **Приоритет:** Высокий
- **Категория:** devops
- **Описание:** Infrastructure as Code
- **Что следить:** Releases, Breaking changes

### Ansible
- **URL:** https://github.com/ansible/ansible
- **Приоритет:** Средний
- **Категория:** devops
- **Описание:** Automation tool
- **Что следить:** Releases, Modules

### Prometheus
- **URL:** https://github.com/prometheus/prometheus
- **Приоритет:** Средний
- **Категория:** devops
- **Описание:** Monitoring system
- **Что следить:** Releases, Integrations

### Grafana
- **URL:** https://github.com/grafana/grafana
- **Приоритет:** Средний
- **Категория:** devops
- **Описание:** Observability platform
- **Что следить:** Releases, New panels
```

---

### 3. Security

#### RSS-ленты:
```markdown
### CVE Details
- **URL:** https://www.cvedetails.com/rss_search.php
- **Тип:** RSS
- **Приоритет:** Критический
- **Категория:** security
- **Описание:** База данных уязвимостей

### Krebs on Security
- **URL:** https://krebsonsecurity.com/feed/
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** security
- **Описание:** Блог о кибербезопасности

### Schneier on Security
- **URL:** https://www.schneier.com/feed/atom/
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** security
- **Описание:** Блог Брюса Шнайера

### The Hacker News
- **URL:** https://feeds.feedburner.com/TheHackersNews
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** security
- **Описание:** Новости хакинга

### BleepingComputer
- **URL:** https://www.bleepingcomputer.com/feed/
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** security
- **Описание:** Новости безопасности
```

#### GitHub репозитории:
```markdown
### OWASP
- **URL:** https://github.com/OWASP/Top10
- **Приоритет:** Высокий
- **Категория:** security
- **Описание:** Топ-10 уязвимостей
- **Что следить:** Updates, New vulnerabilities

### Trivy
- **URL:** https://github.com/aquasecurity/trivy
- **Приоритет:** Высокий
- **Категория:** security
- **Описание:** Security scanner
- **Что следить:** Releases, New detectors

### Wazuh
- **URL:** https://github.com/wazuh/wazuh
- **Приоритет:** Средний
- **Категория:** security
- **Описание:** Security monitoring
- **Что следить:** Releases, Integrations
```

---

### 4. Базы данных

#### RSS-ленты:
```markdown
### PostgreSQL Blog
- **URL:** https://www.postgresql.org/about/news/
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** databases
- **Описание:** Новости PostgreSQL

### MongoDB Blog
- **URL:** https://www.mongodb.com/blog/rss
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** databases
- **Описание:** Новости MongoDB

### Redis Blog
- **URL:** https://redis.com/blog/feed/
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** databases
- **Описание:** Новости Redis

### ClickHouse Blog
- **URL:** https://clickhouse.com/blog/rss
- **Тип:** RSS
- **Приоритет:** Средний
- **Категория:** databases
- **Описание:** Новости ClickHouse
```

#### GitHub репозитории:
```markdown
### PostgreSQL
- **URL:** https://github.com/postgres/postgres
- **Приоритет:** Высокий
- **Категория:** databases
- **Описание:** PostgreSQL source
- **Что следить:** Releases, Major features

### MongoDB
- **URL:** https://github.com/mongodb/mongo
- **Приоритет:** Высокий
- **Категория:** databases
- **Описание:** MongoDB source
- **Что следить:** Releases, New features

### Redis
- **URL:** https://github.com/redis/redis
- **Приоритет:** Высокий
- **Категория:** databases
- **Описание:** Redis source
- **Что следить:** Releases, Modules

### DuckDB
- **URL:** https://github.com/duckdb/duckdb
- **Приоритет:** Высокий
- **Категория:** databases
- **Описание:** In-process SQL DB
- **Что следить:** Releases, Extensions

### Neon
- **URL:** https://github.com/neondatabase/neon
- **Приоритет:** Средний
- **Категория:** databases
- **Описание:** Serverless PostgreSQL
- **Что следить:** Releases, Features
```

---

### 5. Мобильная разработка

#### RSS-ленты:
```markdown
### Android Developers Blog
- **URL:** https://android-developers.googleblog.com/feeds/posts/default
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** mobile
- **Описание:** Новости Android разработки

### Apple Developer News
- **URL:** https://developer.apple.com/news/
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** mobile
- **Описание:** Новости iOS/macOS разработки

### Kotlin Blog
- **URL:** https://blog.jetbrains.com/kotlin/feed/
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** mobile
- **Описание:** Новости Kotlin

### Swift Blog
- **URL:** https://www.swift.org/blog/feed.xml
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** mobile
- **Описание:** Новости Swift
```

#### GitHub репозитории:
```markdown
### Kotlin
- **URL:** https://github.com/JetBrains/kotlin
- **Приоритет:** Высокий
- **Категория:** mobile
- **Описание:** Kotlin language
- **Что следить:** Releases, K2 compiler

### Compose Multiplatform
- **URL:** https://github.com/JetBrains/compose-multiplatform
- **Приоритет:** Высокий
- **Категория:** mobile
- **Описание:** UI фреймворк
- **Что следить:** Releases, Platforms

### SwiftUI
- **URL:** https://github.com/apple/swift-ui
- **Приоритет:** Высокий
- **Категория:** mobile
- **Описание:** SwiftUI samples
- **Что следить:** New APIs

### Flutter
- **URL:** https://github.com/flutter/flutter
- **Приоритет:** Высокий
- **Категория:** mobile
- **Описание:** UI toolkit от Google
- **Что следить:** Releases, New widgets

### React Native
- **URL:** https://github.com/facebook/react-native
- **Приоритет:** Высокий
- **Категория:** mobile
- **Описание:** Mobile от Meta
- **Что следить:** Releases, New architecture
```

---

### 6. Производительность и Инструменты

#### RSS-ленты:
```markdown
### Web.dev
- **URL:** https://web.dev/feed.xml
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** javascript
- **Описание:** Best practices от Google

### V8 Blog
- **URL:** https://v8.dev/blog.atom
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** javascript
- **Описание:** Новости V8 движка

### WebKit Blog
- **URL:** https://webkit.org/blog/feed/
- **Тип:** RSS
- **Приоритет:** Высокий
- **Категория:** javascript
- **Описание:** Новости WebKit
```

#### GitHub репозитории:
```markdown
### ESBuild
- **URL:** https://github.com/evanw/esbuild
- **Приоритет:** Высокий
- **Категория:** javascript
- **Описание:** Быстрый бандлер
- **Что следить:** Releases, Performance

### Vite
- **URL:** https://github.com/vitejs/vite
- **Приоритет:** Высокий
- **Категория:** javascript
- **Описание:** Dev server
- **Что следить:** Releases, Plugins

### Turbopack
- **URL:** https://github.com/vercel/turbo
- **Приоритет:** Высокий
- **Категория:** javascript
- **Описание:** Incremental bundler
- **Что следить:** Releases, Integrations

### Biome
- **URL:** https://github.com/biomejs/biome
- **Приоритет:** Высокий
- **Категория:** javascript
- **Описание:** Linter/formatter
- **Что следить:** Releases, Rules

### Ruff
- **URL:** https://github.com/astral-sh/ruff
- **Приоритет:** Высокий
- **Категория:** python
- **Описание:** Быстрый Python linter
- **Что следить:** Releases, Rules
```

---

## 📋 План внедрения

### Этап 1: AI Tools (Критический)
1. Добавить 8 RSS-лент AI/ML
2. Добавить 6 GitHub репозиториев AI
3. Обновить `08_keywords.md` для AI категории

### Этап 2: DevOps/Cloud (Высокий)
1. Добавить 6 RSS-лент Cloud
2. Добавить 6 GitHub репозиториев DevOps
3. Обновить приоритеты в `02_github_repos.md`

### Этап 3: Security (Высокий)
1. Добавить 5 RSS-лент Security
2. Добавить 3 GitHub репозитория Security
3. Интегрировать с CVE Details API

### Этап 4: Databases (Средний)
1. Добавить 4 RSS-лент Databases
2. Добавить 5 GitHub репозиториев Databases

### Этап 5: Mobile (Средний)
1. Добавить 4 RSS-лент Mobile
2. Добавить 5 GitHub репозиториев Mobile

---

## 🎯 Итоговые метрики

| После расширения | Количество | Изменение |
|------------------|------------|-----------|
| RSS-ленты | 40+ | +25 |
| GitHub репозитории | 40+ | +20 |
| Telegram-каналы | 15+ | +5 |
| Технические блоги | 20+ | +5 |
| **Итого** | **150+** | **+55** |

---

## 📝 Следующие шаги

1. Выбрать приоритетные категории для добавления
2. Создать PR с новыми источниками
3. Обновить системные промпты для учёта новых источников
4. Настроить мониторинг для новых RSS-лент
5. Протестировать генерацию новостей из новых источников
