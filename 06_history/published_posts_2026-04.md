# Архив публикаций: Апрель 2026

Автоматически сгенерированный файл с публикациями за 2026-04.

---

### [2026-04-13] Google выпустила Gemma 4: открытая модель уровня Gemini 3.1 Pro

- **Категория:** google
- **Шаблон:** telegra.ph article
- **Ключевые темы:** google, ai, gemini, opensource, llm
- **Источники:**
  - RenovateQR — AI Models in April 2026 (https://renovateqr.com/blog/ai-models-april-2026)
  - Google AI Blog (https://ai.google/blog/)
- **Telegra.ph URL:** https://telegra.ph/Google-vypustila-Gemma-4-otkrytaya-model-urovnya-Gemini-31-Pro-04-13
- **Telegram ID:** 459
- **Статус:** опубликован

<!-- CONTENT_START -->
Google выпустила **Gemma 4** — новое поколение открытых языковых моделей, способных конкурировать с закрытыми проприетарными системами. Релиз состоялся 2 апреля 2026 года и标志着 значительный скачок в эффективности open-source ИИ.

## Ключевые особенности

Gemma 4 построен на той же исследовательской базе и методах обучения, что и **Gemini 3.1 Pro** от Google DeepMind. Модель оптимизирована для локального запуска, что исключает передачу данных внешним API и снижает требования к оборудованию.

## Что нового

- **Лицензия Apache 2.0** — полностью открытая модель с разрешением на коммерческое использование

- **Мультимодальность** — поддержка текстовых и изображений на входе

- **Контекстное окно до 256 000 токенов** — работа с длинными документами и кодовыми базами

- **Масштабируемость** — от компактных версий для смартфонов до крупных для корпоративной инфраструктуры

## Производительность

Крупнейшие варианты Gemma 4 приближаются к производительности **Gemini 3.1 Pro** в тестах на логическое мышление. Это впервые среди открытых моделей от Google напрямую конкурирует с закрытыми системами уровня frontier.

## Специализация

Модель оптимизирована для:

- Сложных логических рассуждений

- Агентных рабочих процессов (agentic workflows)

- Локального развёртывания на потребительских устройствах

## Почему это важно

Предыдущие версии Gemma имели ограничения на использование и заметно уступали закрытым аналогам. Gemma 4 меняет правила игры: модель предоставляет **frontier-level intelligence per parameter** при полной открытости кода и весов.

Разработчики теперь могут запускать передовые ИИ-модели на мобильных и потребительских устройствах без потери качества и без зависимости от облачных API.

## Где попробовать

Модель доступна для скачивания с официальной страницы проекта. Документация и примеры использования опубликованы в репозитории Google.

---

Источники:

- [RenovateQR — AI Models in April 2026](https://renovateqr.com/blog/ai-models-april-2026)

- [Google AI Blog](https://ai.google/blog/)
<!-- CONTENT_END -->
---

### [2026-04-13] Claude Code захватил 4% коммитов на GitHub и получил 6 новых функций

- **Категория:** anthropic
- **Шаблон:** telegra.ph article
- **Ключевые темы:** anthropic, ai, github, developer_tools, automation
- **Источники:**
  - MindStudio — Claude Code Q1 2026 Update Roundup (https://www.mindstudio.ai/blog/claude-code-q1-2026-update-roundup-2/)
  - Claude Code Docs — What's New Week 14 (https://code.claude.com/docs/en/whats-new/2026-w14)
  - SemiAnalysis — Claude Code is the Inflection Point (https://newsletter.semianalysis.com/p/claude-code-is-the-inflection-point)
  - Reddit r/accelerate — GitHub commit statistics (https://www.reddit.com/r/accelerate/comments/1rgktvu/4_of_github_public_commits_are_being_authored_by/)
- **Telegra.ph URL:** https://telegra.ph/Claude-Code-zahvatil-4-kommitov-na-GitHub-i-poluchil-6-novyh-funkcij-04-13
- **Telegram ID:** 460
- **Статус:** опубликован

<!-- CONTENT_START -->
AI-агент для разработки **Claude Code** от Anthropic стал одним из главных трендов первого квартала 2026 года. Инструмент, запущенный в феврале 2025 года, сейчас генерирует **4% всех публичных коммитов** на GitHub, а аналитики прогнозируют рост до **20%+ ежедневных коммитов** к концу 2026 года.

## Шесть ключевых обновлений Q1 2026

В первом квартале Anthropic выпустила шесть значимых функций для Claude Code:

- **Remote Control** — режим headless-агента: Claude Code работает на сервере или в CI/CD-пайплайне без привязки к локальному терминалу. Управление через REST API и WebSocket с аутентификацией по API-ключам и гибкой системой разрешений.

- **Dispatch** — система планирования задач: встроенная очередь заданий для масштабирования работы агентов. Поддерживает маршрутизацию по профилям разрешений, цепочки зависимостей и автоматические повторы при сбоях.

- **Channels** — координация мультиагентных систем: pub/sub-слой с тремя типами каналов — `Command` (назначение задач), `Status` (прогресс) и `Artifact` (передача кода). Все сообщения типизированы и изолированы в рамках проекта.

- **Computer Use** — масштабное обновление работы с GUI: задержка взаимодействия сократилась вдвое благодаря скользящему окну визуального контекста. Добавлена поддержка drag-and-drop, нескольких мониторов и буфера обмена.

- **Auto Mode** — автономный режим принятия решений: настраиваемые профили риска (`Conservative`, `Balanced`, `Aggressive`) позволяют агенту самостоятельно выполнять низкоуровневые действия. Все решения логируются в аудиторский отчёт.

- **AutoDream** — генератор архитектурных планов: превращает текстовое описание задачи в разбивку задач, архитектурные схемы, карты зависимостей и реестр рисков. Не пишет код — создаёт структуру проекта.

## Возможности терминала: неделя 14

В последней неделе марта — начале апреля Claude Code получил **компьютерное зрение прямо в CLI**. Теперь агент может:

- Открывать нативные приложения (macOS, iOS, GUI-программы) и кликать по интерфейсу

- Самостоятельно тестировать UI-изменения и исправлять ошибки в графических приложениях

- Проводить сквозные проверки сценариев: «Открой симулятор, пройди онбординг, сделай скриншоты»

- Использовать плагины как обычные консольные команды без указания абсолютных путей

Дополнительно добавлены: рендеринг без мерцания (`CLAUDE_CODE_NO_FLICKER=1`), индивидуальные лимиты размера ответов MCP (до 500 000 символов) и хуки `PermissionDenied` для режима Auto.

## Интеграция с GitHub

Claude Code полностью автоматизирует Git-воркфлоу: создаёт ветки, формирует коммиты, открывает pull-запросы, проводит code review и закрывает issues через нативную интеграцию с GitHub API. Именно поэтому доля AI-коммитов растёт экспоненциально.

## Доступность

Claude Code включён в подписку **Claude Pro ($20/мес)** и доступен через API по тарифам Claude 3.5/3.7 Sonnet (~$3 за 1 млн входных и ~$15 за 1 млн выходных токенов). Поддерживает Python, JavaScript/TypeScript, Rust, Go и другие языки.

---

Источники:

- [MindStudio — Claude Code Q1 2026 Update Roundup](https://www.mindstudio.ai/blog/claude-code-q1-2026-update-roundup-2/)

- [Claude Code Docs — Week 14 Updates](https://code.claude.com/docs/en/whats-new/2026-w14)

- [SemiAnalysis — Claude Code is the Inflection Point](https://newsletter.semianalysis.com/p/claude-code-is-the-inflection-point)

- [Reddit — 4% of GitHub commits by Claude Code](https://www.reddit.com/r/accelerate/comments/1rgktvu/4_of_github_public_commits_are_being_authored_by/)
<!-- CONTENT_END -->
---

### [2026-04-13] Servo появился на crates.io: браузерный движок на Rust получил LTS-релиз

- **Категория:** rust
- **Шаблон:** telegra.ph article
- **Ключевые темы:** rust, browser_engine, servo, embedded, opensource
- **Источники:**
  - Phoronix — Servo Making It Easier For Embedded Use (https://www.phoronix.com/news/Servo-Embed-Crates-LTS)
  - Servo.org — Official Blog (https://servo.org/blog/)
- **Telegra.ph URL:** https://telegra.ph/Servo-poyavilsya-na-cratesio-brauzernyj-dvizhok-na-Rust-poluchil-LTS-reliz-04-13
- **Telegram ID:** 461
- **Статус:** опубликован

<!-- CONTENT_START -->
Сервисный браузерный движок **Servo**, разработанный на языке Rust, стал доступен на **crates.io** — официальном репозитории пакетов для Rust-разработчиков. Релиз сопровождается выпуском первой **LTS-версии (0.1 LTS)** с долгосрочной поддержкой.

## Почему это важно

До сегодняшнего дня интеграция Servo требовала ручной сборки из исходного кода. Теперь подключить движок можно **одной строкой в Cargo.toml**, что значительно упрощает CI/CD-процессы и снижает порог входа для разработчиков.

Команда Servo подчёркивает, что одна из самых перспективных областей применения — **встраиваемое использование** как альтернатива Chromium Embedded Framework (CEF). Это открывает возможности для:

- **IoT-устройств** — легковесный рендеринг веб-контента на ограниченных ресурсах

- **Кастомных оболочек** — собственные браузеры на базе Servoshell

- **Десктопных приложений** — WebView API для встраивания в любые проекты

- **Мобильных платформ** — поддержка Android и OpenHarmony

## Модель LTS: стабильность для продакшена

Servo внедрил предсказуемый цикл поддержки:

- **LTS-релизы** — каждые 6 месяцев, поддержка 9 месяцев

- **Feature-релизы** — ежемесячно, возможны breaking changes

- **LTS-обновления** — только исправления безопасности

Такой подход снижает риски для долгосрочных коммерческих проектов: разработчики могут锁定иться на LTS-ветке и получать только критические патчи, не опасаясь изменений API.

## Технические особенности

Движок построен на **модульной архитектуре** с использованием популярных Rust-крейтов, что позволяет заменять отдельные компоненты. Благодаря гарантиям безопасности памяти Rust, Servo минимизирует уязвимости, связанные с указателями и гонками данных. **Конкурентные вычисления** обеспечивают ускоренный и энергоэффективный рендеринг на многоядерных процессорах.

Проект работает под управлением **открытого управления (open governance)** под эгидой Linux Foundation Europe.

## Где следить

- Официальный блог: [Servo.org](https://servo.org/blog/)

- Статья на Phoronix: [Servo Making It Easier For Embedded Use](https://www.phoronix.com/news/Servo-Embed-Crates-LTS)

---

Источники:

- [Phoronix — Servo Making It Easier For Embedded Use](https://www.phoronix.com/news/Servo-Embed-Crates-LTS)

- [Servo.org — Official Blog](https://servo.org/blog/)
<!-- CONTENT_END -->
---

### [2026-04-13] Google выпустила LiteRT-LM: движок ИИ-инференса для мобильных устройств

- **Категория:** google
- **Шаблон:** telegra.ph article
- **Ключевые темы:** google, ai, mobile, opensource, edge_computing
- **Источники:**
  - Google AI Edge (https://ai.google.dev/edge/litert)
  - Google Developers Blog (https://developers.googleblog.com/litert-the-universal-framework-for-on-device-ai/)
  - GitHub Repository (https://github.com/google-ai-edge/LiteRT-LM)
- **Telegra.ph URL:** https://telegra.ph/Google-vypustila-LiteRT-LM-dvizhok-II-inferensa-dlya-mobilnyh-ustrojstv-04-13
- **Telegram ID:** 462
- **Статус:** опубликован

<!-- CONTENT_START -->
Google [AI Edge](https://ai.google.dev/edge/litert) выпустила **LiteRT-LM** — open-source фреймворк для локального инференса больших языковых моделей на периферийных устройствах. Проект набрал более **3,6 тысяч звёзд** на GitHub за первую неделю после релиза.

## Что такое LiteRT-LM

LiteRT-LM — это кроссплатформенный движок на **C++**, который позволяет запускать LLM напрямую на устройстве без обращения к облаку. Фреймворк уже используется в продуктах Google: **Chrome**, **Chromebook Plus** и **Pixel Watch**.

## Ключевые возможности

- **Кроссплатформенность** — Android, iOS, Web, Desktop и IoT (включая Raspberry Pi)

- **Аппаратное ускорение** — использование GPU и NPU для максимальной производительности

- **Мультимодальность** — поддержка обработки визуальных и аудиоданных

- **Tool Use** — встроенная поддержка вызова инструментов для агентных сценариев

- **Широкая совместимость** — модели Gemma, Llama, Phi-4, Qwen и другие

## Почему это важно

В 2026 году тренд на **локальный инференс** набирает обороты. Apple развивает mlx-vlm, Qualcomm — AI Engine Direct, и теперь Google закрывает критический пробел в экосистеме **Android** с помощью LiteRT-LM.

**Преимущества для разработчиков:**

- **Нулевая задержка** — ответы модели без сетевых запросов

- **Конфиденциальность** — данные не покидают устройство

- **Автономность** — работа без подключения к интернету

- **Единый стек** — конвертация, оптимизация (квантование) и деплой через инструменты Google AI Edge

## Ограничения

Фактическая производительность зависит от **аппаратных ресурсов** конкретного устройства. На бюджетных смартфонах запуск крупных моделей может быть ограничен объёмом памяти.

---

Источники:

- [Google AI Edge — LiteRT](https://ai.google.dev/edge/litert)

- [Google Developers Blog — LiteRT: The Universal Framework](https://developers.googleblog.com/litert-the-universal-framework-for-on-device-ai/)

- [GitHub — google-ai-edge/LiteRT-LM](https://github.com/google-ai-edge/LiteRT-LM)
<!-- CONTENT_END -->
---

### [2026-04-13] ФБР извлекло удалённые сообщения Signal через уведомления iPhone

- **Категория:** security
- **Шаблон:** telegra.ph article
- **Ключевые темы:** security, privacy, signal, iphone, ios
- **Источники:**
  - 404 Media — Original Report (https://www.404media.co)
  - 9to5Mac — FBI Used iPhone Notification Data (https://9to5mac.com/2026/04/09/fbi-used-iphone-notification-data-to-retrieve-deleted-signal-messages/)
  - TechRadar — iPhone Privacy Warning (https://www.techradar.com/phones/iphone-owners-urged-to-change-this-key-privacy-setting-after-fbi-recovers-suspects-deleted-signal-messages)
  - WIRED — Push Notifications Security (https://www.wired.com/story/security-news-this-week-your-push-notifications-arent-safe-from-the-fbi/)
- **Telegra.ph URL:** https://telegra.ph/FBR-izvleklo-udalyonnye-soobshcheniya-Signal-cherez-uvedomleniya-iPhone-04-13
- **Telegram ID:** 463
- **Статус:** опубликован

<!-- CONTENT_START -->
ФБР обнаружило способ извлекать содержимое удалённых сообщений Signal через системную базу данных push-уведомлений iOS. Об этом стало известно из показаний специального агента ФБР Кларка Витхорна в суде по делу в Алварадо (Техас).

## Как это работает

Signal использует сквозное шифрование, которое защищает содержимое сообщений внутри приложения. Однако **входящие уведомления** попадают в системный кэш iOS до того, как пользователь откроет мессенджер.

- Приложение Signal было удалено с устройства подозреваемого

- iOS продолжала хранить кэшированные push-уведомления в памяти

- ФБР извлекло входящие сообщения через forensic-анализ базы данных уведомлений

- Исходящие сообщения через этот метод **не доступны**

Ключевой факт: у подозреваемого была включена функция предпросмотра содержимого уведомлений в Signal. Именно поэтому полный текст сообщений попадал в системный кэш iOS.

## Техническая сторона

Токены push-уведомлений **не инвалидируются мгновенно** при удалении приложения. Сервер Apple продолжает отправлять уведомления, а iOS кэширует их локально. Доступ правоохранителей, вероятно, получен через резервную копию устройства с использованием коммерческих forensic-инструментов.

Уязвимость носит **системный характер** — она затрагивает все приложения на iOS, использующие стандартные push-уведомления, а не только Signal.

## Что делать пользователям

Для защиты своих данных выполните следующие шаги:

- Откройте **Signal** → **Настройки** → **Уведомления**

- Выберите параметр **Без имени и содержания** для максимальной приватности

- Проверьте аналогичные настройки в других мессенджерах (WhatsApp, Telegram)

- Учитывайте, что отключение предпросмотра снизит удобство, но повысит безопасность

Отдельно стоит отметить, что в **iOS 26.4** Apple изменила механизм валидации токенов push-уведомлений. Прямая связь с этим делом не подтверждена, но совпадение по времени показательно.

## Контекст

Это не первый случай, когда правоохранительные органы обходят шифрование через системные уязвимости. Signal давно рекомендует отключать предпросмотр уведомлений, но большинство пользователей игнорируют эту настройку.

---

Источники:

- [404 Media — Original Report](https://www.404media.co/)

- [9to5Mac — FBI Used iPhone Notification Data](https://9to5mac.com/2026/04/09/fbi-used-iphone-notification-data-to-retrieve-deleted-signal-messages/)

- [TechRadar — iPhone Privacy Warning](https://www.techradar.com/phones/iphone-owners-urged-to-change-this-key-privacy-setting-after-fbi-recovers-suspects-deleted-signal-messages)

- [WIRED — Push Notifications Security](https://www.wired.com/story/security-news-this-week-your-push-notifications-arent-safe-from-the-fbi/)

- [heise — iOS Signal Data Extraction](https://www.heise.de/en/news/iOS-Deleted-Signal-data-extracted-by-FBI-via-notification-database-11252199.html)
<!-- CONTENT_END -->
---

### [2026-04-13] Anthropic запустила Project Glasswing: Claude Mythos для киберзащиты

- **Категория:** security
- **Шаблон:** telegra.ph article
- **Ключевые темы:** security, anthropic, ai, cybersecurity, opensource
- **Источники:**
  - Fortune (https://fortune.com/2026/04/07/anthropic-claude-mythos-model-project-glasswing-cybersecurity/)
  - Security Brief (https://securitybrief.com.au/story/anthropic-launches-project-glasswing-for-cyber-defence)
  - Till Freitag Analysis (https://till-freitag.com/en/blog/anthropic-mythos-glasswing-analysis)
- **Telegra.ph URL:** https://telegra.ph/Anthropic-zapustila-Project-Glasswing-Claude-Mythos-dlya-kiberzashchity-04-13
- **Telegram ID:** 464
- **Статус:** опубликован

<!-- CONTENT_START -->
Anthropic объявила о запуске **Project Glasswing** — масштабной инициативы по киберобороне, которая предоставляет отобранным организациям доступ к превью-версии самой продвинутой модели компании **Claude Mythos**. Цель проекта — опережающее обнаружение и устранение уязвимостей до того, как ими воспользуются злоумышленники.

## Участники проекта

К инициативе присоединились крупнейшие технологические компании:

- **Amazon Web Services** — облачная инфраструктура

- **Apple** — защита экосистемы устройств

- **Broadcom** — полупроводниковые решения

- **Cisco** — сетевая безопасность

- **CrowdStrike** — endpoint-защита

- **Google** — облачные и потребительские сервисы

- **Microsoft** — корпоративная безопасность

- **Nvidia** — GPU-инфраструктура

- **JPMorganChase** — финансовый сектор

Всего в проекте участвуют около **40 организаций**, отвечающих за разработку и поддержку критической программной инфраструктуры.

## Что умеет Claude Mythos

Claude Mythos Preview — универсальная модель, чья эффективность в задачах безопасности обусловлена продвинутыми навыками программирования и логического вывода. В ходе тестирования модель продемонстрировала впечатляющие результаты:

- Обнаружены **тысячи zero-day уязвимостей**, включая 27-летний баг в OpenBSD и 16-летнюю уязвимость в распространённом видеоПО

- Модель нашла скрытые ошибки в коде, который автоматизированные инструменты тестирования прогоняли до **5 млн раз** без результата

- Выявлены уязвимости во всех основных операционных системах и веб-браузерах

## Финансовая поддержка

Anthropic выделяет значительные ресурсы на развитие проекта:

- До **$100 млн** в кредитах на использование модели партнёрами

- **$4 млн** прямых донатов open-source организациям по безопасности

## Почему это важно

С приходом ИИ окно между обнаружением уязвимости и её эксплуатацией сократилось с месяцев до минут. Project Glasswing ставит целью демократизацию экспертизы в области безопасности — предоставление мощных ИИ-инструментов мейнтейнерам open-source проектов, у которых нет ресурсов на крупные команды SOC.

Модель имеет **двойное назначение**: те же возможности, что помогают защитникам, могут быть использованы злоумышленниками для автоматизации сложных кибератак. Именно поэтому массового релиза Claude Mythos не планируется — доступ строго ограничен проверенными партнёрами.

## Что дальше

Anthropic проводит консультации с правительством США относительно оборонительных и атакующих характеристик модели в контексте регулирования передового ИИ. Безопасный запуск модели на масштабе запланирован только после внедрения новых защитных механизмов.

---

Источники:

- [Fortune — Anthropic Claude Mythos Project Glasswing](https://fortune.com/2026/04/07/anthropic-claude-mythos-model-project-glasswing-cybersecurity/)

- [Security Brief — Anthropic Project Glasswing](https://securitybrief.com.au/story/anthropic-launches-project-glasswing-for-cyber-defence)

- [Till Freitag — Claude Mythos & Project Glasswing Analysis](https://till-freitag.com/en/blog/anthropic-mythos-glasswing-analysis)
<!-- CONTENT_END -->
---

### [2026-04-13] Telegram выпустил апрельское обновление: ИИ-редактор текста и живые фото

- **Категория:** telegram
- **Шаблон:** telegra.ph article
- **Ключевые темы:** telegram, messaging, ai_editor, mobile, privacy
- **Источники:**
  - TechishKenya (https://www.facebook.com/techishkenya/posts/telegrams-april-2026-update-adds-an-ai-text-editor-improved-polls-live-and-motio/1726225735024591/)
  - FoneArena (https://www.facebook.com/fonearena/posts/telegram-update-brings-ai-text-editor-advanced-poll-features-and-live-photos-sup/1528548528859376/)
  - Threads @mattnavarra (https://www.threads.com/@mattnavarra/post/DWl4IIpiooD/telegram-unleashes-new-ai-editor-smarter-polls-and-bot-building-bots-telegram)
- **Telegra.ph URL:** https://telegra.ph/Telegram-vypustil-aprelskoe-obnovlenie-II-redaktor-teksta-i-zhivye-foto-04-13
- **Telegram ID:** 465
- **Статус:** опубликован

<!-- CONTENT_START -->
Мессенджер Telegram выпустил крупное обновление для платформ Android и iOS, добавив ряд долгожданных функций, включая встроенный ИИ-редактор текста, поддержку живых фотографий и расширенные возможности для опросов.

## ИИ-редактор текста

Ключевая новинка — встроенный редактор текста на базе искусственного интеллекта. Он умеет:

- **Исправлять грамматику** — автоматическая проверка орфографии и пунктуальности прямо в поле ввода

- **Переписывать сообщения** — изменение тона и стиля текста одним нажатием

- **Переводить текст** — мгновенный перевод сообщений на другие языки

Разработчики подчёркивают конфиденциальность функции: обработка запросов происходит с акцентом на локальную и защищённую обработку. Бесплатно доступно **200 запросов в час**.

## Улучшенные опросы

Функция опросов получила значительное расширение возможностей:

- **Медиафайлы в опросах** — теперь можно добавлять изображения и видео к вопросам и вариантам ответов

- **Геолокации** — возможность привязывать варианты ответов к местоположению

- **Временные ограничения** — установка таймера для автоматического завершения голосования

- **Перемешивание вариантов** — случайный порядок ответов для объективности результатов

## Live Photos и Motion Photos

Telegram добавил полную поддержку живых и анимированных фотографий. Пользователи могут отправлять Live Photos (iOS) и Motion Photos (Android) без потери анимации — фото отображаются в движении прямо в чате.

## Дополнительные нововведения

Помимо основных функций, обновление включает:

- **Сканирование документов на iOS** — встроенный инструмент для сканирования и отправки документов прямо из приложения

- **Плейлисты профиля** — пользователи могут организовывать публикации в профиле в виде тематических плейлистов

- **Chat Saving** — возможность сохранять и управлять предыдущими разговорами

- **Системные сообщения** — новые информационные уведомления внутри чатов

- **Защита от неофициальных клиентов** — предупреждения при использовании сторонних приложений Telegram

## Значение обновления

Апрельское обновление Telegram демонстрирует тренд на интеграцию ИИ-функций непосредственно в мессенджеры. Встроенный редактор текста конкурирует с аналогичными решениями от конкурентов, при этом Telegram делает акцент на приватности и бесплатном базовом доступе.

---

Источники:

- [TechishKenya](https://www.facebook.com/techishkenya/posts/telegrams-april-2026-update-adds-an-ai-text-editor-improved-polls-live-and-motio/1726225735024591/)

- [FoneArena](https://www.facebook.com/fonearena/posts/telegram-update-brings-ai-text-editor-advanced-poll-features-and-live-photos-sup/1528548528859376/)

- [Threads @mattnavarra](https://www.threads.com/@mattnavarra/post/DWl4IIpiooD/telegram-unleashes-new-ai-editor-smarter-polls-and-bot-building-bots-telegram)

- [LinkedIn](https://www.linkedin.com/posts/dicksonotieno_telegrams-april-2026-update-adds-ai-text-activity-7445055761891647490-1Ji6)
<!-- CONTENT_END -->
---

### [2026-04-13] MemPalace: AI-память с архитектурой дворца памяти улучшила поиск на 34%

- **Категория:** ai_tools
- **Шаблон:** telegra.ph article
- **Ключевые темы:** ai_tools, memory, opensource, mcp, llm
- **Источники:**
  - MemPalace GitHub (https://github.com/milla-jovovich/mempalace)
  - GitHub Trending Weekly 2026-04-08 (https://www.shareuhack.com/en/posts/github-trending-weekly-2026-04-08)
- **Telegra.ph URL:** https://telegra.ph/MemPalace-AI-pamyat-s-arhitekturoj-dvorca-pamyati-uluchshila-poisk-na-34-04-13
- **Telegram ID:** 466
- **Статус:** опубликован

<!-- CONTENT_START -->
Каждый разговор с ИИ заканчивается одинаково — контекст исчезает. Часы отладки, архитектурные дискуссии, принятые решения — всё теряется при завершении сессии. Новый open-source проект **MemPalace** решает эту проблему, применяя классический мнемонический метод — **дворец памяти**.

## Что такое MemPalace

MemPalace — это локальная система управления памятью для ИИ-агентов с открытым исходным кодом (лицензия MIT). Вместо плоского векторного поиска она организует данные в структурированную архитектуру:

- **Крылья (Wings)** — отдельные проекты или пользователи

- **Комнаты (Rooms)** — конкретные темы внутри крыла, например `auth-migration` или `billing`

- **Коридоры и туннели** — связи между комнатами внутри крыла и между крыльями

- **Шкафы и ящики** — указатели ведут к исходным файлам, хранящимся без изменений

## Ключевое отличие: хранение без суммаризации

Главная философия проекта — **ИИ не решает, что важно запомнить**. MemPalace сохраняет исходный текст диалогов в ChromaDB в неизменном виде. Это контрастирует с подходом большинства систем, где LLM суммаризует контекст, неизбежно теряя детали.

Структурная организация данных даёт прирост **+34% к точности поиска (R@10)** без единого вызова API — исключительно за счёт фильтрации по крыльям и комнатам.

## Бенчмарки

- **LongMemEval R@5** (raw-режим, ChromaDB) — **96,6%** без вызовов API

- **LongMemEval R@5** (гибридный режим с reranking) — **100%**, ~500 вызовов API

- **LoCoMo R@10** (session level) — 60,3%

- **Стоимость хранения за год** — ~$10 против ~$507 у систем с LLM-суммаризацией

Результат 96,6% — наивысший опубликованный показатель для бесплатной локальной системы управления памятью.

## Интеграция с ИИ-агентами

MemPalace подключается к ИИ-агентам тремя способами:

- **MCP-сервер** — 19 инструментов для чтения, записи, навигации и работы с графом знаний

- **Плагины Claude Code** — нативная интеграция с Claude Code Skills

- **CLI-команды** — `wake-up` и `search` для локальных моделей

Каждый агент получает собственное «крыло» и дневник, сохраняющий экспертизу между сессиями. Контекст автоматически сохраняется каждые 15 сообщений или перед сжатием окна контекста.

## Граф знаний с временными метками

Помимо векторного поиска, MemPalace строит **временной граф отношений** (субъект-предикат-объект) на SQLite. Каждая связь валидна в определённом диапазоне дат, что позволяет отслеживать эволюцию решений и фактов.

## Честность перед сообществом

Авторы проекта — Милла Йовович и Бен Сигман — опубликовали открытое признание неточностей в первоначальном описании:

- Заявленное «30-кратное сжатие без потерь» для диалекта AAAK оказалось преувеличением — диалект является **lossy** и эффективен только при больших объёмах повторяющихся данных

- «Обнаружение противоречий» существует как отдельный скрипт, но пока не интегрировано в граф знаний

- Рекордные 96,6% достигнуты в raw-режиме, а не в AAAK

Проект активно развивается: фиксируются и исправляются баги, включая уязвимость shell injection в хуках и segfault на macOS ARM64.

## Технические детали

- **Стек:** Python 3.9+, ChromaDB, SQLite, PyYAML

- **Архитектура:** CLI + MCP Server + Semantic Searcher + Temporal Knowledge Graph

- **Лицензия:** MIT

- **Репозиторий:** [GitHub](https://github.com/milla-jovovich/mempalace)

---

Источники:

- [MemPalace GitHub Repository](https://github.com/milla-jovovich/mempalace)

- [GitHub Trending Weekly 2026-04-08](https://www.shareuhack.com/en/posts/github-trending-weekly-2026-04-08)
<!-- CONTENT_END -->
---

### [2026-04-13] Adobe экстренно устранила zero-day уязвимость в Acrobat Reader

- **Категория:** security
- **Шаблон:** telegra.ph article
- **Ключевые темы:** security, adobe, zero_day, pdf, cybersecurity
- **Источники:**
  - Security Affairs (https://securityaffairs.com/190697/security/adobe-fixes-actively-exploited-acrobat-reader-flaw-cve-2026-34621.html)
  - PurpleOps (https://purple-ops.io/blog/adobe-acrobat-cve-2026-34621-patch)
  - Cybersecurity Help (https://www.cybersecurity-help.cz/vdb/vulns/125813/)
  - Mondoo Vulnerability Intelligence (https://mondoo.com/vulnerability-intelligence/vulnerability/CVE-2026-34621)
- **Telegra.ph URL:** https://telegra.ph/Adobe-ehkstrenno-ustranila-zero-day-uyazvimost-v-Acrobat-Reader-04-13
- **Telegram ID:** 467
- **Статус:** опубликован

<!-- CONTENT_START -->
Adobe выпустила экстренное обновление безопасности для Acrobat и Acrobat Reader, устраняющее критическую уязвимость **CVE-2026-34621** с оценкой **CVSS 8.6**. Уязвимость активно эксплуатируется в дикой природе как минимум с **декабря 2025 года**.

## Детали уязвимости

Баг представляет собой **prototype pollution** в JavaScript-движке Adobe Acrobat. При открытии специально созданного PDF-файла злоумышленник может манипулировать свойствами объектов, обходить встроенные средства защиты и выполнять произвольный код с правами текущего пользователя.

Атакующие используют многоэтапную схему:

- Эксплойт обходит защитные механизмы и запускает привилегированные API

- Через `util.readFileIntoStream()` считываются локальные файлы жертвы

- Данные передаются на удалённый сервер через `RSS.addFeed()`

- Загружается дополнительный вредоносный JavaScript для кражи учётных данных

- В отдельных случаях возможна полная компрометация системы (RCE)

## Затронутые версии

- **Acrobat DC / Reader DC** — `26.001.21367` и более ранние (Windows, macOS)

- **Acrobat 2024** — `24.001.30356` и более ранние (Windows, macOS)

## Версии с исправлением

Adobe рекомендует обновиться до следующих версий:

- **Acrobat DC / Reader DC** — `26.001.21411`

- **Acrobat 2024 (Windows)** — `24.001.30362`

- **Acrobat 2024 (macOS)** — `24.001.30360`

## Что делать

- **Пользователям:** откройте `Справка → Проверить обновления` или скачайте последнюю версию с сайта Adobe

- **Администраторам:** разверните патч через системы управления (Intune, SCCM) в экстренном порядке

- **Временная мера:** отключите JavaScript (`Настройки → JavaScript`) и включите защищённый режим

- **Корпоративным средам:** блокируйте PDF-вложения на почтовом шлюзе до полной установки патчей

Уязвимость была обнаружена **Хаофэй Ли (Haifei Li)**, основателем EXPMON. Adobe настоятельно рекомендует установить обновления в течение **72 часов**.

---

Источники:

- [Security Affairs](https://securityaffairs.com/190697/security/adobe-fixes-actively-exploited-acrobat-reader-flaw-cve-2026-34621.html)

- [PurpleOps](https://purple-ops.io/blog/adobe-acrobat-cve-2026-34621-patch)

- [Cybersecurity Help](https://www.cybersecurity-help.cz/vdb/vulns/125813/)

- [Mondoo Vulnerability Intelligence](https://mondoo.com/vulnerability-intelligence/vulnerability/CVE-2026-34621)
<!-- CONTENT_END -->
---

### [2026-04-13] Rockstar Games подтвердила утечку данных через взлом стороннего сервиса

- **Категория:** security
- **Шаблон:** telegra.ph article
- **Ключевые темы:** security, кибербезопасность, утечка_данных, supply_chain, snowflake
- **Источники:**
  - Times of India (https://timesofindia.indiatimes.com/technology/tech-news/rockstar-games-confirms-data-breach-read-hackers-open-threat-message-to-gta-maker/articleshow/130225704.cms)
  - TechStartups (https://techstartups.com/2026/04/13/top-tech-news-today-april-13-2026/)
  - The Sunday Guardian via Daily Hunt (https://m.dailyhunt.in/news/india/english/the+sunday+guardian-epaper-sndygrde/gta+6+rockstar+data+breach+rockstar+games+confirms+limited+data+exposure+shinyhunters+allegedly+exploit+demand+ransom+with+april+14+deadline-newsid-n708174667)
- **Telegra.ph URL:** https://telegra.ph/Rockstar-Games-podtverdila-utechku-dannyh-cherez-vzlom-storonnego-servisa-04-13
- **Telegram ID:** 468
- **Статус:** опубликован

<!-- CONTENT_START -->
13 апреля 2026 года стало известно о крупной утечке данных в Rockstar Games — студии, стоящей за серией Grand Theft Auto. Хакерская группировка **ShinyHunters** опубликовала ультиматум с требованием связаться для переговоров до **14 апреля**, угрожая в противном случае опубликовать похищенную информацию.

## Вектор атаки

Инцидент произошёл не через прямую атаку на инфраструктуру Rockstar, а через **сторонний аналитический сервис Anodot**, интегрированный с облачными базами данных **Snowflake** компании. Злоумышленники использовали компрометацию цепочки поставок — метод, при котором доступ к целевой организации получается через уязвимости в подключённых сервисах.

## Тактика ShinyHunters

Группировка ShinyHunters известна своими масштабными кампаниями по компрометации SaaS-платформ. Их стандартная методология включает:

- **Целевые фишинговые атаки** (vishing) на сотрудников компаний

- **Кража API-ключей и токенов** интеграций

- **Создание поддельных доменов**, имитирующих легитимные сервисы

- **Использование легитимных учётных данных** для маскировки под обычный доступ

За последний год группировка заявила об атаках на **более чем 100 организаций**, включая такие компании, как Atlassian, Canva, HubSpot, ZoomInfo и WeWork. Ранее через аналогичные схемы были скомпрометированы системы **Google, Microsoft, Cisco и Европейской комиссии**.

## Ответ Rockstar

Представитель Rockstar Games подтвердил инцидент изданию *Kotaku*:

> «Мы можем подтвердить, что был получен доступ к ограниченному объему нематериальной корпоративной информации в связи с утечкой данных у третьей стороны. Этот инцидент не оказывает влияния на нашу организацию или наших игроков».

Компания подчёркивает, что **данные учётных записей игроков не были затронуты**, а сам инцидент носит корпоративный, а не потребительский характер.

## Уроки для индустрии

Этот инцидент наглядно демонстрирует критическую проблему современной кибербезопасности:

- **Зависимость от сторонних сервисов** создаёт дополнительные векторы атак

- **Snowflake-утечки** стали массовым трендом 2025–2026 годов

- **Аналитические интеграции** часто имеют избыточные привилегии доступа

- **Мониторинг цепочки поставок** остаётся слабы местом в большинстве организаций

## Что делать разработчикам и компаниям

- **Проведите аудит всех интеграций** со сторонними сервисами и API

- **Ограничьте привилегии** для подключённых аналитических систем

- **Внедрите мониторинг аномальной активности** в Snowflake и других облачных БД

- **Используйте ротацию API-ключей** и многофакторную аутентификацию для всех интеграций

- **Обновите incident response планы** с учётом supply chain атак

---

Источники:

- [Times of India](https://timesofindia.indiatimes.com/technology/tech-news/rockstar-games-confirms-data-breach-read-hackers-open-threat-message-to-gta-maker/articleshow/130225704.cms)

- [TechStartups](https://techstartups.com/2026/04/13/top-tech-news-today-april-13-2026/)

- [Daily Hunt — The Sunday Guardian](https://m.dailyhunt.in/news/india/english/the+sunday+guardian-epaper-sndygrde/gta+6+rockstar+data+breach+rockstar+games+confirms+limited+data+exposure+shinyhunters+allegedly+exploit+demand+ransom+with+april+14+deadline-newsid-n708174667)
<!-- CONTENT_END -->
---

### [2026-04-13] Kubernetes v1.36: удаление уязвимых компонентов и новая работа с GPU

- **Категория:** kubernetes
- **Шаблон:** telegra.ph article
- **Ключевые темы:** kubernetes, devops, containers, security, cloud
- **Источники:**
  - Kubernetes Blog (https://kubernetes.io/blog/2026/03/30/kubernetes-v1-36-sneak-peek/)
  - Kubernetes Dev Group (https://groups.google.com/a/kubernetes.io/g/dev/c/22f8Kdc_VfA)
- **Telegra.ph URL:** https://telegra.ph/Kubernetes-v136-udalenie-uyazvimyh-komponentov-i-novaya-rabota-s-GPU-04-13
- **Telegram ID:** 469
- **Статус:** опубликован

<!-- CONTENT_START -->
Kubernetes v1.36 готовится к релизу 22 апреля 2026 года и приносит значительные изменения в области безопасности и управления ресурсами кластера.

## Удаление уязвимых компонентов

Релиз v1.36 станет переломным для безопасности Kubernetes:

- **externalIPs объявлен устаревшим** — поле `service.spec.externalIPs` депрекейтед из-за риска MITM-атак (CVE-2020-8554). Предупреждения появятся уже в v1.36, полное удаление — в v1.43. Рекомендуемые замены: `LoadBalancer`, `NodePort` или `Gateway API`

- **gitRepo Volume отключён** — драйвер, устаревший с v1.11, полностью отключён. Он позволял запускать код от имени `root` на узле. Мигрируйте на `init`-контейнеры или утилиты типа `git-sync`

- **Ingress NGINX выведен из поддержки** — с 24 марта 2026 сообщество больше не выпускает релизы и security-патчи. Существующие деплои работают, но рекомендуется переход на альтернативные контроллеры

## Новые возможности

**Ускоренная маркировка SELinux (GA)**

Рекурсивное переназначение меток заменено на опцию монтирования `mount -o context=XYZ`. Это сокращает время запуска подов в средах с SELinux. Функция включена по умолчанию, но требует корректной настройки `spec.SELinuxMount` для смешанных привилегированных и непривилегированных подов.

**Внешняя подпись токенов ServiceAccount**

`kube-apiserver` теперь может делегировать подпись токенов внешним KMS или аппаратным модулям безопасности (HSM). Это повышает безопасность кластера и упрощает централизованное управление ключами.

## Улучшения Dynamic Resource Allocation

**Taints и Tolerations для устройств (Beta)**

Драйверы DRA получили возможность помечать устройства как недоступные для планировщика. Администраторы создают правила `DeviceTaintRule` для массовой маркировки оборудования, что обеспечивает строгий контроль специализированных ресурсов.

**Разделяемые GPU (Partitionable Devices)**

Одно физическое устройство (например, GPU) теперь можно разделить на несколько логических изолированных частей для одновременного использования разными ворклоадами. Это значительно повышает эффективность дорогостоящей инфраструктуры.

## Что делать

- Проверьте, используете ли вы `externalIPs` — начинайте миграцию на `LoadBalancer` или `Gateway API`

- Если работаете с `gitRepo` volumes — переходите на `init`-контейнеры

- Для Ingress NGINX — оцените альтернативные контроллеры (Gateway API, Traefik, HAProxy)

- Протестируйте SELinux Mount acceleration в staging-окружении

---

Источники:

- [Kubernetes Blog — v1.36 Sneak Peek](https://kubernetes.io/blog/2026/03/30/kubernetes-v1-36-sneak-peek/)

- [Kubernetes Dev Group — State of the Release](https://groups.google.com/a/kubernetes.io/g/dev/c/22f8Kdc_VfA)
<!-- CONTENT_END -->
---

### [2026-04-13] OpenAI отозвала сертификаты macOS после атаки на цепочку поставок

- **Категория:** security
- **Шаблон:** telegra.ph article
- **Ключевые темы:** security, openai, npm, supply_chain, cybersecurity
- **Источники:**
  - DevOps.com — North Korean Hackers Suspected in Supply Chain Attack on Axios (https://devops.com/north-korean-hackers-suspected-in-supply-chain-attack-on-popular-axios-project/)
  - Google Threat Intelligence Group — Axios NPM Package Compromised (https://www.linkedin.com/posts/mandiant_google-threat-intelligence-group-is-tracking-activity-7445107711836352512-L-mZ)
  - CYBER Magazine — How Did North Korean Hackers Compromise Axios (https://cybermagazine.com/news/gtig-how-did-north-korean-hackers-compromise-axios)
  - TechStartups — Top Tech News April 13, 2026 (https://techstartups.com/2026/04/13/top-tech-news-today-april-13-2026/)
- **Telegra.ph URL:** https://telegra.ph/OpenAI-otozvala-sertifikaty-macOS-posle-ataki-na-cepochku-postavok-04-13
- **Telegram ID:** 470
- **Статус:** опубликован

<!-- CONTENT_START -->
OpenAI **отозвала сертификаты macOS** для своих приложений после обнаружения компрометации рабочего процесса GitHub Actions. Атака приписывается северокорейской хакерской группировке **UNC1069**, которая использовала схему внедрения вредоносного кода в цепочку поставок программного обеспечения.

## Как произошла атака

Злоумышленники скомпрометировали npm-аккаунт основного сопровождающего популярной HTTP-библиотеки **Axios** (более 100 миллионов загрузок в неделю) и заменили email на адрес ProtonMail. Через модифицированную версию пакета вредоносный код попал в автоматизированный конвейер сборки OpenAI.

- **Цель:** внедрение бэкдора в продукты через компрометацию открытых зависимостей

- **Метод:** подмена npm-пакета Axios в CI/CD-процессе

- **Исполнитель:** группировка UNC1069, связанная с КНДР

## Ответ OpenAI

Компания оперативно отреагировала на инцидент:

- **Сертификаты macOS** отозваны в качестве превентивной меры

- **Данные пользователей** не пострадали

- **Внутренние системы** не были скомпрометированы

Отзыв сертификатов временно затрагивает распространение и проверку подписи приложений OpenAI для macOS, однако компания prioritizes безопасность над удобством.

## Контекст угроы

Группировка UNC1069 известна изощрёнными методами социальной инженерии. По данным Google Threat Intelligence Group, хакеры создали **поддельную компанию** с фальшивыми профилями сотрудников, брендированным Slack-каналом и профессиональной онлайн-инфраструктурой, чтобы завоевать доверие сопровождающего открытого проекта.

Это не изолированный инцидент — подобная тактика указывает на растущую тенденцию **supply chain атак** на открытые экосистемы, где злоумышленники атакуют не конечные продукты, а их зависимости.

## Рекомендации разработчикам

- **Закрепляйте версии зависимостей** через lock-файлы (package-lock.json, yarn.lock)

- **Мониторьте обновления** критических пакетов через инструменты аудита

- **Используйте подписи пакетов** и верификацию контрольных сумм

- **Внедрите политики безопасности** для CI/CD-конвейеров (OIDC, attestation)

- **Рассмотрите прокси-репозитории** с дополнительной проверкой перед публикацией

---

Источники:

- [DevOps.com — North Korean Hackers Suspected in Supply Chain Attack on Axios](https://devops.com/north-korean-hackers-suspected-in-supply-chain-attack-on-popular-axios-project/)

- [Google Threat Intelligence Group — Axios NPM Package Compromised](https://www.linkedin.com/posts/mandiant_google-threat-intelligence-group-is-tracking-activity-7445107711836352512-L-mZ)

- [CYBER Magazine — How Did North Korean Hackers Compromise Axios](https://cybermagazine.com/news/gtig-how-did-north-korean-hackers-compromise-axios)

- [TechStartups — Top Tech News April 13, 2026](https://techstartups.com/2026/04/13/top-tech-news-today-april-13-2026/)
<!-- CONTENT_END -->
---

### [2026-04-13] Apple тестирует несколько дизайнов ИИ-очков для конкуренции с Meta Ray-Ban

- **Категория:** apple
- **Шаблон:** telegra.ph article
- **Ключевые темы:** apple, ai_glasses, wearables, meta, технологии
- **Источники:**
  - Bloomberg (https://www.bloomberg.com)
  - TechStartups (https://techstartups.com/2026/04/13/top-tech-news-today-april-13-2026/)
- **Telegra.ph URL:** https://telegra.ph/Apple-testiruet-neskolko-dizajnov-II-ochkov-dlya-konkurencii-s-Meta-Ray-Ban-04-13
- **Telegram ID:** 471
- **Статус:** опубликован

<!-- CONTENT_START -->
Apple активно работает над своими первыми умными очками с искусственным интеллектом, готовясь к выходу на рынок, который сейчас агрессивно захватывает Meta с линейкой Ray-Ban Meta.

## Что известно

По данным Bloomberg, Apple тестирует **несколько вариантов дизайна** своих будущих ИИ-очков. Инженеры компании проверяют как минимум **четыре различные конфигурации** с разными типами оправ и расположением компонентов.

Ключевые особенности разрабатываемого устройства:

- **Вертикальная камера** — нестандартное расположение для лучшего качества фото и видео

- **ИИ-функции** — интеграция с Apple Intelligence для голосового управления и контекстных подсказок

- **Разные оправы** — возможность выбора стиля под разные предпочтения пользователей

- **Лёгкий форм-фактор** — Apple делает ставку на комфорт при длительном ношении

## Почему это важно

Рынок умных очков переживает **бум в 2026 году**. Meta Ray-Ban стали хитом продаж, объединив стильный дизайн с ИИ-ассистентом. Apple не может позволить себе отстать в этой категории — носимые устройства с ИИ считаются одним из главных технологических трендов года.

- Meta уже продала **миллионы единиц** Ray-Ban Meta

- Рынок умных очков вырастет до **$14 млрд к 2028 году**

- ИИ-очки становятся **альтернативой смартфона** для быстрых задач

## Конкуренция с Meta

Стратегия Apple отличается от подхода Meta. Если Meta делает ставку на **социальные функции** и интеграцию с Instagram и Facebook, то Apple фокусируется на **глубокой интеграции с экосистемой** iPhone, iPad и Mac.

Ожидается, что ИИ-очки Apple получат:

- Интеграцию с **Siri и Apple Intelligence**

- Доступ к **контактам, картам и уведомлениям**

- Поддержку **Continuity** для бесшовной работы с другими устройствами Apple

## Когда ждать релиз

Точная дата выхода пока не объявлена. Однако активное тестирование нескольких дизайнов говорит о том, что Apple **серьёзно продвинулась** в разработке. Аналитики предполагают анонс не ранее **2027 года**.

---

Источники:

- [Bloomberg — Apple Testing Multiple AI Glasses Designs](https://www.bloomberg.com/)

- [TechStartups — Top Tech News April 13, 2026](https://techstartups.com/2026/04/13/top-tech-news-today-april-13-2026/)
<!-- CONTENT_END -->
---

### [2026-04-13] Cursor 3: редактор кода стал консолью управления ИИ-агентами

- **Категория:** developer_tools
- **Шаблон:** telegra.ph article
- **Ключевые темы:** developer_tools, ai, cursor, coding, ide
- **Источники:**
  - Cursor Blog — Meet the new Cursor (https://cursor.com/blog/cursor-3)
  - The New Stack — Cursor 3 Demotes IDE (https://thenewstack.io/cursor-3-demotes-ide/)
  - Medium — Cursor 3 Is Not an IDE Update (https://medium.com/@han.heloir/cursor-3-is-not-an-ide-update-its-a-bet-that-you-ll-manage-agents-not-write-code-0d2bc51f0dcb)
- **Telegra.ph URL:** https://telegra.ph/Cursor-3-redaktor-koda-stal-konsolyu-upravleniya-II-agentami-04-13
- **Telegram ID:** 472
- **Статус:** опубликован

<!-- CONTENT_START -->
Компания Cursor представила **Cursor 3** — полностью переработанную среду для разработки программного обеспечения, где ИИ-агенты вышли на первый план, а классический редактор кода отошёл на второй план.

Релиз состоялся **2 апреля 2026 года** и знаменует собой фундаментальный сдвиг в подходе к созданию программного обеспечения. Интерфейс под кодовым названием **Glass** создан с нуля: вместо дерева файлов основное место заняло поле ввода промпта, а сам IDE превратился в консоль управления ИИ-агентами.

## Ключевые возможности

- **Консоль управления агентами** — единая боковая панель агрегирует все локальные и облачные агенты, включая сессии из мобильного приложения, Slack, GitHub и Linear

- **Параллельный запуск агентов** — поддержка одновременной работы множества ИИ-агентов над разными задачами

- **Мультирепозиторная архитектура** — встроенная работа с несколькими репозиториями одновременно

- **Cloud Handoff** — мгновенный перенос активной сессии между локальной машиной и облаком без прерывания задачи

- **Автоматическая верификация** — облачные агенты сами генерируют демо и скриншоты выполненных задач

## Встроенная модель Composer 2

Cursor 3 использует специализированную модель **Composer 2**, созданную для агентной разработки. Модель оптимизирована для долгосрочного планирования и выполнения сложных многофайловых задач. Она демонстрирует сильные результаты в автономном написании, проверке и комите кода.

## Маркетплейс плагинов

Пользователи получили возможность расширять возможности агентов через **маркетплейс плагинов** — установка MCP-серверов, навыков и субагентов в один клик. Поддерживаются приватные командные магазины для корпоративных клиентов.

## Как изменился рабочий процесс

Роль разработчика трансформируется: вместо написания кода основное время тратится на **ревью сгенерированных диффов**, проверку скриншотов от облачных агентов, распределение задач и управление PR-воркфлоу. Разработчик превращается в **инженера-менеджера** или оператора платформы.

Архитектурная аналогия проста: традиционный IDE стал аналогом SSH (для редких ручных правок), а новая консоль выступает в роли **Control Plane** — центра принятия решений и мониторинга.

## Конкурентный контекст

Запуск Cursor 3 ускорен под давлением конкурентов: **Claude Code** от Anthropic достиг $2,5 млрд годовой выручки, что вынудило Cursor выпустить Automations, Composer 2 и Cursor 3 за один месяц. На рынке формируется архитектурный раскол: Anthropic и OpenAI делают ставку на CLI-интерфейсы, тогда как Cursor интегрирует консоль управления непосредственно в IDE.

---

Источники:

- [Cursor Blog — Meet the new Cursor](https://cursor.com/blog/cursor-3)

- [The New Stack — Cursor 3 Demotes IDE](https://thenewstack.io/cursor-3-demotes-ide/)

- [Medium — Cursor 3 Is Not an IDE Update](https://medium.com/@han.heloir/cursor-3-is-not-an-ide-update-its-a-bet-that-you-ll-manage-agents-not-write-code-0d2bc51f0dcb)
<!-- CONTENT_END -->
---

### [2026-04-14] Python 3.14.4 и 3.13.13: критические security-патчи и исправления

- **Категория:** python
- **Шаблон:** telegra.ph article
- **Ключевые темы:** python, security, release, opensource, cve
- **Источники:**
  - Python.org Changelog (https://docs.python.org/3/whatsnew/changelog.html)
  - Python Downloads (https://www.python.org/downloads/source/)
  - Microsoft Oryx Issue #2869 (https://github.com/microsoft/Oryx/issues/2869)
- **Telegra.ph URL:** https://telegra.ph/Python-3144-i-31313-kriticheskie-security-patchi-i-ispravleniya-04-14
- **Telegram ID:** 473
- **Статус:** опубликован

<!-- CONTENT_START -->
Python-команда выпустила обновления **3.14.4** и **3.13.13** с пакетом security-исправлений и важных баг-фиксов. Релиз затрагивает обе активные ветки и рекомендует всем разработчикам обновиться.

## Security-исправления

Обновление закрывает несколько уязвимостей:

- **CVE-2026-4224** — сбой в xml.parsers.expat из-за неограниченной C-рекурсии при обработке глубоко вложенных XML через ElementDeclHandler()

- **CVE-2026-3644** — передача управляющих символов в http.cookies.Morsel.update() и js_output()

- **CVE-2026-2297** — небезопасное открытие .pyc файлов через SourcelessFileLoader

- **Инъекция HTTP-заголовков** — запрещены управляющие символы в статусе wsgiref.handlers

- **URL-уязвимость** — отклонены URL с ведущими дефисами в webbrowser.open()

## Ключевые исправления

Ряд важных баг-фиксов в ядре и стандартной библиотеке:

- Устранены **утечки памяти** в SyntaxError, socket, atexit.register() и ssl.SSLContext

- **base64** декодер теперь соответствует RFC 4648

- Исправлена бесконечная рекурсия в collections.defaultdict.__repr__()

- Устранено зависание annotationlib.get_annotations() при циклических цепочках __wrapped__

- struct.pack('f', float) корректно вызывает OverflowError

- ensurepip больше не ищет pip-*.whl в текущей директории

## Free-threading и производительность

Значительные улучшения для сборки без GIL:

- Устранены **гонки данных** в PyDict_Watch/Unwatch, importlib и list.__sizeof__()

- Улучшена масштабируемость sys.intern() и PyObject_SetAttr()

- bytearray.resize() стало **потокобезопасным**

- Исправлены взаимоблокировки при stop-the-world паузах

## Другие улучшения

- \N{name} поддерживает регистронезависимый поиск идеографов CJK и слогов хангыль

- В unicodedata добавлена поддержка **тангутских идеографов**

- Все опции -X теперь передаются дочерним процессам multiprocessing

- Обновлена зависимость **libexpat** до версии 2.7.5

## Рекомендация

Разработчикам рекомендуется обновиться до **3.14.4** или **3.13.13** как можно скорее, особенно если ваше приложение работает с XML-данными или cookie.

---

Источники:

- [Python Changelog 3.14.4](https://docs.python.org/3/whatsnew/changelog.html)

- [Python Downloads](https://www.python.org/downloads/source/)

- [Microsoft Oryx Issue #2869](https://github.com/microsoft/Oryx/issues/2869)
<!-- CONTENT_END -->
---

### [2026-04-14] SiFive привлекла $400 млн на развитие RISC-V процессоров для ИИ-дата-центров

- **Категория:** hardware
- **Шаблон:** telegra.ph article
- **Ключевые темы:** hardware, riscv, ai_chips, datacenter, nvidia
- **Источники:**
  - TechCrunch (https://techcrunch.com/2026/04/11/nvidia-backed-sifive-hits-3-65-billion-valuation-for-open-ai-chips/)
  - HPCWire (https://www.hpcwire.com/aiwire/2026/04/09/sifive-raises-400m-series-g-to-advance-risc-v-architecture-for-ai-infrastructure/)
  - SemiWiki (https://semiwiki.com/ip/sifive/365958-sifive-to-power-next-gen-risc-v-ai-data-centers-with-nvidia-nvlink-fusion/)
- **Telegra.ph URL:** https://telegra.ph/SiFive-privlekla-400-mln-na-razvitie-RISC-V-processorov-dlya-II-data-centrov-04-14
- **Telegram ID:** 474
- **Статус:** опубликован

<!-- CONTENT_START -->
Разработчик открытых процессорных архитектур SiFive привлёк **$400 млн** в рамках переподписанного раунда Series G. Компанию оценили в **$3,65 млрд** — это крупнейшая инвестиция в отрасль RISC-V на сегодняшний день.

## Ключевые детали раунда

- **Лидер инвестирования:** Atreides Management (основатель — экс-инвестор Fidelity Гэвин Бейкер)

- **Стратегические инвесторы:** NVIDIA, Apollo Global Management, D1 Capital Partners, Point72 Turion, T. Rowe Price, Sutter Hill Ventures

- **Предыдущий раунд (2022):** $175 млн при оценке $2,33 млрд

- **Статус раунда:** oversubscribed — заявок было больше, чем мест

## Почему RISC-V для ИИ-дата-центров?

SiFive основана инженерами из UC Berkeley в 2015 году и изначально разрабатывала процессоры на базе открытой архитектуры **RISC-V** — альтернативы проприетарным x86 (Intel, AMD) и ARM. До сих пор фокус был на встраиваемых системах, но новый раунд направлен на проектирование CPU для **ИИ-дата-центров**.

Главное преимущество — открытость и нейтральность. SiFive не производит чипы самостоятельно и не привязана к конкретным заказчикам. Клиенты лицензируют дизайны и модифицируют архитектуру под свои задачи, аналогично бизнес-модели Arm, но без конфликта интересов.

## Интеграция с NVIDIA NVLink Fusion

SiFive объявила о поддержке технологии **NVLink Fusion** от NVIDIA — межсоединения серверного уровня для когерентной связи между CPU, GPU и ускорителями.

- NVLink Fusion устраняет узкие места традиционной шины **PCIe**

- Процессоры SiFive смогут напрямую подключаться к GPU NVIDIA

- Поддержка программного стека **CUDA** и экосистемы «AI factory»

- RISC-V CPU станут «полноправными компонентами» в ИИ-инфраструктуре

Как отмечает TechCrunch, пока Intel и AMD конкурируют с GPU NVIDIA, сама NVIDIA инвестирует в открытую и нейтральную альтернативу — SiFive на базе RISC-V.

## Конкуренция с ARM и x86

Рынок процессоров для дата-центров исторически разделён между **x86** (Intel, AMD) и **ARM** (Ampere, AWS Graviton, Apple). RISC-V предлагает третий путь:

- **Открытая спецификация** — любой может использовать и модифицировать

- **Энергоэффективность** — оптимизация под конкретные workload'ы

- **Отсутствие vendor lock-in** — нет зависимости от одного вендора

При этом ARM в марте 2026 года начала выпускать собственные ИИ-чипы совместно с Meta, что создаёт конфликт интересов для лицензиатов. SiFive сохраняет нейтральную позицию.

## Что дальше

CEO SiFive Патрик Литтл заявил, что Series G станет **последним раундом финансирования** перед выходом на публичный рынок. Компания планирует ускорить разработку высокопроизводительных платформ для ИИ-инференса и обучения больших языковых моделей.

---

Источники:

- [TechCrunch — Nvidia-backed SiFive hits $3.65B valuation](https://techcrunch.com/2026/04/11/nvidia-backed-sifive-hits-3-65-billion-valuation-for-open-ai-chips/)

- [HPCWire — SiFive Raises $400M Series G](https://www.hpcwire.com/aiwire/2026/04/09/sifive-raises-400m-series-g-to-advance-risc-v-architecture-for-ai-infrastructure/)

- [SemiWiki — SiFive to Power Next-Gen RISC-V AI Data Centers](https://semiwiki.com/ip/sifive/365958-sifive-to-power-next-gen-risc-v-ai-data-centers-with-nvidia-nvlink-fusion/)
<!-- CONTENT_END -->
---

### [2026-04-14] Linux 7.0: квантовая защита, самовосстановление XFS и PCIe 6.0

- **Категория:** linux
- **Шаблон:** telegra.ph article
- **Ключевые темы:** linux, kernel, quantum_security, xfs, opensource
- **Источники:**
  - Linux Kernel 7.0 Release (https://medium.com/@ajaymaurya73130/linux-kernel-7-0-release-bug-fixes-stability-improvements-hardware-enhancements-explained-438dc28682d2)
  - Linux Journal (https://www.linuxjournal.com/content/linux-70-coming-what-expect-next-major-kernel-release)
  - Phoronix (https://www.phoronix.com/)
  - Kernel Newbies (https://kernelnewbies.org/LinuxChanges)
- **Telegra.ph URL:** https://telegra.ph/Linux-70-kvantovaya-zashchita-samovosstanovlenie-XFS-i-PCIe-60-04-14
- **Telegram ID:** 475
- **Статус:** опубликован

<!-- CONTENT_START -->
Проект Linux официально выпустил ядро **7.0** — первый мажорный релиз с версии 6.0, вышедшей более пяти лет назад. Обновление приносит значительные изменения в области безопасности, файловой системы и поддержки оборудования.

## Квантовая криптография

В ядро встроена поддержка постквантового алгоритма **ML-DSA** (Module-Lattice-based Digital Signature Algorithm). Новый алгоритм используется для верификации подписей модулей ядра, интегрирован в подсистему keyrings и стеки TLS/IPsec. Это закладывает фундамент для миграции на квантово-устойчивую криптографию.

## Самовосстановление XFS

Файловая система **XFS** получила фоновую автоматическую диагностику и восстановление повреждённых метаданных. Механизм online-repair снижает зависимость от утилиты xfs_repair и повышает устойчивость к внезапным отключениям питания. Администраторам больше не нужно вручную запускать проверку после аварийного завершения.

## Планировщик и производительность

Планировщик **EEVDF** оптимизирован для снижения латентности и повышения пропускной способности. Улучшенный балансировщик нагрузки эффективнее распределяет задачи на гетерогенных процессорах (big.LITTLE). Новые политики NUMA-aware размещения потоков и расширенное управление энергопотреблением через cgroups v2.

## Поддержка оборудования

Ядро получило нативную поддержку:

- **PCIe 6.0** — удвоенная пропускная способность шины

- **CXL 3.0** — гибкое управление памятью в дата-центрах

- **Intel Nova Lake** и **AMD Zen 6** — новейшие семейства процессоров

- **RISC-V** — расширенные векторные расширения

- **ARMv9.2** — актуальная серверная архитектура

- **Wi-Fi 7** (802.11be) — драйверы нового поколения

## Файловые системы и сеть

Стабилизирована **bcachefs**, улучшения в ext4/btrfs включают прозрачное блочное сжатие и оптимизированный io_uring доступ. Подсистема XDP/AF_XDP обрабатывает пакеты с нулевым копированием, TCP BBRv3 интегрирован в ядро, а netfilter ускорен через eBPF-хуки.

## Что значит для разработчиков

- Квантовая безопасность — ML-DSA доступен из коробки, без внешних модулей

- Онлайн-ремонт XFS снижает время простоя серверов

- PCIe 6.0 и CXL 3.0 открывают возможности для новых конфигураций GPU-кластеров

- Улучшенный EEVDF-планировщик уменьшает задержки для latency-sensitive приложений

## Как обновиться

Стабильная версия уже доступна на kernel.org. Дистрибутивы (Ubuntu 26.04 LTS, Fedora 44) интегрируют ядро 7.0 в ближайшие недели. Перед обновлением на серверах рекомендуется протестировать критичные модули в staging-окружении.

---

Источники:

- [Linux Kernel 7.0 Release](https://medium.com/@ajaymaurya73130/linux-kernel-7-0-release-bug-fixes-stability-improvements-hardware-enhancements-explained-438dc28682d2)

- [Linux Journal: Linux 7.0 Preview](https://www.linuxjournal.com/content/linux-70-coming-what-expect-next-major-kernel-release)

- [Phoronix: Linux 7.0 Coverage](https://www.phoronix.com/)

- [Kernel Newbies](https://kernelnewbies.org/LinuxChanges)
<!-- CONTENT_END -->
---

### [2026-04-14] Vercel готовится к IPO: ИИ-агенты обеспечили рост выручки в 3 раза

- **Category:** vercel
- **Template:** telegra.ph article
- **Key topics:** vercel, ipo, ai_agents, разработка, облачные_технологии
- **Sources:**
  - TechCrunch (https://techcrunch.com/2026/04/13/vercel-ceo-guillermo-rauch-signals-ipo-readiness-as-ai-agents-fuel-revenue-surge/)
  - CryptoRank (https://cryptorank.io/news/feed/655db-vercel-ipo-ai-agents-revenue)
  - Yahoo Finance (https://finance.yahoo.com/markets/stocks/articles/vercel-ceo-guillermo-rauch-signals-152229505.html)
- **Telegra.ph URL:** https://telegra.ph/Vercel-gotovitsya-k-IPO-II-agenty-obespechili-rost-vyruchki-v-3-raza-04-14
- **Telegram ID:** 476
- **Status:** published

<!-- CONTENT_START -->
Платформа Vercel, созданная для развёртывания веб-приложений, приблизилась к выходу на фондовый рынок. Генеральный директор **Гильермо Раух** в интервью TechCrunch заявил, что компания «полностью готова» к IPO, хотя конкретных сроков не назвал.

## Финансовые показатели

Выручка Vercel по модели **ARR** (годовой регулярный доход) выросла более чем в **3 раза** за последние два года:

· Начало 2024 — $100 млн ARR
· Февраль 2026 — $340 млн ARR
· Сентябрь 2025 — оценка $9,3 млрд после раунда Series F ($300 млн от Accel)

## Влияние ИИ-агентов

Ключевой драйвер роста — распространение **ИИ-агентов** для генерации кода. По данным компании:

· **30%** приложений на Vercel уже развёрнуты ИИ-агентами
· Агенты ускоряют создание кастомных приложений, делая разработку проще, чем покупку готового ПО
· Раух: «Агенты чрезвычайно продуктивны в развёртывании. Всё это ПО должно где-то работать — мы считаем, что это будет Vercel»

## Рынок без потолка

Раух подчеркнул, что **адресуемый рынок инфраструктуры** больше не имеет ограничений:

> «Когда я начинал эту компанию, развёртывание было доступно лишь десяткам миллионов людей. Теперь каждый в мире может создать приложение»

Несмотря на текущее охлаждение рынка IPO в секторе ПО, вызванное опасениями по поводу ИИ-дисрапции, Vercel чувствует себя уверенно. Компания позиционирует себя как основную платформу хостинга для приложений, генерируемых ИИ-агентами.

## Что дальше

Точная дата IPO не раскрыта. Раух отметил: «Нет идеального таймлайна или квартала. Компания готова и становится ещё готовее с каждым днём». Выход на биржу ожидается в ближайшем будущем.

---

Источники:
· [TechCrunch — Vercel CEO Signals IPO Readiness](https://techcrunch.com/2026/04/13/vercel-ceo-guillermo-rauch-signals-ipo-readiness-as-ai-agents-fuel-revenue-surge/)
· [CryptoRank — Vercel IPO: 240% Revenue Growth](https://cryptorank.io/news/feed/655db-vercel-ipo-ai-agents-revenue)
· [Yahoo Finance — Vercel CEO Guillermo Rauch](https://finance.yahoo.com/markets/stocks/articles/vercel-ceo-guillermo-rauch-signals-152229505.html)
<!-- CONTENT_END -->

---

### [2026-04-14] Cloudflare запустил Agent Cloud: платформа для ИИ-агентов с интеграцией OpenAI

- **Category:** cloudflare
- **Template:** telegra.ph article
- **Key topics:** cloudflare, ai_agents, openai, developer_tools, cloud
- **Sources:**
  - Cloudflare Press Release (https://www.cloudflare.com/press/press-releases/2026/cloudflare-expands-its-agent-cloud-to-power-the-next-generation-of-agents/)
  - SiliconANGLE (https://siliconangle.com/2026/04/13/cloudflare-expands-agent-cloud-new-tools-build-scale-ai-agents/)
  - OpenAI Blog (https://openai.com/index/cloudflare-openai-agent-cloud/)
- **Telegra.ph URL:** https://telegra.ph/Cloudflare-zapustil-Agent-Cloud-platforma-dlya-II-agentov-s-integraciej-OpenAI-04-14
- **Telegram ID:** 477
- **Status:** published

<!-- CONTENT_START -->
Компания Cloudflare объявила о масштабном расширении платформы **Agent Cloud**, предназначенной для разработки production-готовых ИИ-агентов. Обновление включает несколько ключевых компонентов, которые позволяют разработчикам создавать автономных агентов, способных работать в глобальной сети Cloudflare с безопасностью по умолчанию.

## Dynamic Workers

Новая среда выполнения на основе изолятов обеспечивает запуск кода, сгенерированного ИИ, за миллисекунды без периода «прогрева». Dynamic Workers обеспечивают уровень изоляции, сопоставимый с контейнерами, но работают в **100 раз быстрее** и стоят лишь долю их цены.

## Sandboxes стали общедоступными

Изолированные Linux-окружения вышли в статус **General Availability**. Каждая песочница предоставляет:

· Полноценную оболочку и файловую систему
· Поддержку фоновых процессов
· Возможность клонирования репозиториев и установки пакетов
· Запуск сборок и итеративную отладку

## Artifacts и Think

Новый примитив хранилища **Artifacts** полностью совместим с Git и позволяет создавать миллионы репозиториев для агентов. Фреймворк **Think** в составе Agents SDK обеспечивает персистентность — сохранение состояния между шагами многошаговых задач.

## Интеграция с OpenAI

Платформа получила официальную поддержку моделей **GPT-5.4** и **Codex** от OpenAI. После приобретения Replicate Cloudflare создала единый каталог ИИ-моделей, позволяющий переключаться между вендорами изменением одной строки кода.

## Масштабирование

Платформа поддерживает до **миллионов одновременных выполнений**. Агенты способны выполнять API-вызовы, преобразование данных и цепочки вызовов инструментов в масштабах enterprise.

## Позиция рынка

Мэтью Принс, сооснователь и CEO Cloudflare:

> «Способ создания ПО фундаментально меняется. Мы вступаем в мир, где код пишут и выполняют сами агенты. Сегодня мы делаем Cloudflare определяющей платформой для агентного веба».

Рохан Варма из OpenAI отметил, что облачные агенты становятся фундаментальным элементом организации работы.

---

Источники:
· [Cloudflare Press Release — Agent Cloud Expansion](https://www.cloudflare.com/press/press-releases/2026/cloudflare-expands-its-agent-cloud-to-power-the-next-generation-of-agents/)
· [SiliconANGLE — Cloudflare Expands Agent Cloud](https://siliconangle.com/2026/04/13/cloudflare-expands-agent-cloud-new-tools-build-scale-ai-agents/)
· [OpenAI — Cloudflare OpenAI Agent Cloud](https://openai.com/index/cloudflare-openai-agent-cloud/)
<!-- CONTENT_END -->

---

### [2026-04-14] Индия лидирует в Азии по внедрению агентного ИИ

- **Category:** ai
- **Template:** telegra.ph article
- **Key topics:** ai, india, agentic_ai, технологии, бизнес
- **Sources:**
  - TechWire Asia (https://techwireasia.com/)
  - OutSystems State of AI Development 2026 (https://www.outsystems.com/)
  - PYMNTS (https://www.pymnts.com/)
- **Telegra.ph URL:** https://telegra.ph/Indiya-lidiruet-v-Azii-po-vnedreniyu-agentnogo-II-04-14
- **Telegram ID:** 478
- **Status:** published

<!-- CONTENT_START -->
Индия стала безоговорочным лидером Азиатско-Тихокеанского региона по внедрению **агентного ИИ** — автономных ИИ-систем, способных самостоятельно выполнять задачи. Об этом свидетельствуют данные отчёта **OutSystems State of AI Development 2026**, основанного на опросе 1 879 ИТ-руководителей по всему миру.

## Ключевые показатели

Индийский рынок демонстрирует впечатляющие результаты:

· **Уровень экспертизы** — самая высокая концентрация пользователей со статусом «эксперт» по агентному ИИ среди всех опрошенных стран
· **ROI 50%** — лидирующие позиции в АТР по возврату инвестиций в ИИ-разработку и производительность
· **Переход в продакшн** — вместе с Бразилией Индия показывает самые высокие темпы перевода ИИ-проектов из пилотной стадии в промышленное использование
· **Доверие к автономным агентам** — индийские компании чаще других готовы доверять агентам критически важные бизнес-процессы

## Региональное сравнение

Другие страны АТР заметно отстают:

· **Япония** — лидер по ROI операционной эффективности (37%), но 44% компаний указывают на нехватку внутренних навыков как главный барьер
· **Австралия** — находится на промежуточном этапе перевода пилотов в продакшн
· **Умеренное доверие** — доминирующий ответ в большинстве стран АТР, тогда как в Индии преобладает «высокий уровень доверия»

## Глобальный контекст

Агентный ИИ переходит из стадии экспериментов в практическую реализацию:

· **49%** — глобальный медианный показатель перехода ИИ-проектов в продакшн
· **36%** компаний имеют централизованную стратегию управления агентным ИИ
· **40%+** ИТ-лидеров называют фрагментацию legacy-систем и сложности интеграции главными препятствиями

## Главный вызов

Несмотря на лидерство во внедрении, Индии необходимо ускорить развитие систем **управления и регулирования** (governance), чтобы они соответствовали высоким темпам развёртывания технологий. Быстрое внедрение рассматривается как рациональная реакция на специфику индийского корпоративного рынка.

---

Источники:
· [TechWire Asia — India Leading Asia's Agentic AI Adoption](https://techwireasia.com/india-leading-asia-agentic-ai-adoption/)
· [OutSystems — State of AI Development 2026](https://www.outsystems.com/)
· [PYMNTS — India and the Gulf Race Ahead on Agentic AI](https://www.pymnts.com/artificial-intelligence-2/2026/india-and-the-gulf-race-ahead-on-agentic-ai-deployment/)
<!-- CONTENT_END -->

---

### [2026-04-14] Axios взломан: supply chain атака через npm доставила RAT на все платформы

- **Category:** npm
- **Template:** telegra.ph article
- **Key topics:** npm, security, axios, javascript, supply_chain
- **Sources:**
  - GitHub — axios post-mortem (https://github.com/axios/axios/issues/10636)
  - Cisco Talos Blog (https://blog.talosintelligence.com/axois-npm-supply-chain-incident/)
  - Elastic Security Labs (https://www.elastic.co/security-labs/axios-one-rat-to-rule-them-all)
  - Malwarebytes (https://www.malwarebytes.com/blog/news/2026/03/axios-supply-chain-attack-chops-away-at-npm-trust)
  - The Hacker News (https://thehackernews.com/2026/03/axios-supply-chain-attack-pushes-cross.html)
- **Telegra.ph URL:** https://telegra.ph/Axios-vzloman-supply-chain-ataka-cherez-npm-dostavila-RAT-na-vse-platformy-04-14
- **Telegram ID:** 479
- **Status:** published

<!-- CONTENT_START -->
Один из самых популярных HTTP-клиентов для JavaScript — **Axios** (более 60 млн еженедельных загрузок на npm) — стал жертвой серьёзной атаки на цепочку поставок. 31 марта 2026 года ведущий мейнтейнер Джейсон Сааман подтвердил компрометацию своей учётной записи и публикацию двух вредоносных версий пакета.

## Что произошло

Злоумышленники провели целевую атаку через социальную инженерию, установив RAT-малварь на компьютер мейнтейнера. Получив доступ к учётным данным npm-аккаунта, атакующие опубликовали версии **axios@1.14.1** и **axios@0.30.4** с внедрённой зависимостью `plain-crypto-js@4.2.1`.

## Механизм атаки

Вредоносная зависимость работала как загрузчик (dropper):

· При установке пакета на систему загружался и исполнялся **троян удалённого доступа (RAT)**
· Поддержка **трёх платформ**: macOS, Windows и Linux
· Атакующие установили серверы командного управления на домене `sfrclak[.]com` и IP `142.11.206.73:8000`

## Как проверить свой проект

Выполните поиск в файлах блокировки зависимостей:

```
grep -E "axios@(1\.14\.1|0\.30\.4)|plain-crypto-js" package-lock.json yarn.lock
```

Если найдены совпадения — **считайте систему скомпрометированной** и выполните действия по восстановлению.

## Шаги по устранению

· **Откатитесь** до безопасных версий: `axios@1.14.0` или `axios@0.30.3` для ветки 0.x
· **Удалите** `node_modules/plain-crypto-js/`
· **Ротируйте все секреты** — API-ключи, токены, учётные данные на затронутой машине
· **Проверьте сетевые логи** на подключения к домену `sfrclak[.]com`
· Если атака затронула **CI-раннер** — смените все секреты, доступные в момент сборки

## Рекомендации по превенции

Атака на Axios — напоминание о хрупкости экосистемы npm. Ведущий мейнтейнер призвал сообщество:

· Перейти на публикацию пакетов через **OIDC-поток** (OpenID Connect)
· Настроить **immutable-релизы** — запрет на перезапись опубликованных версий
· Обновить **GitHub Actions** в соответствии с лучшими практиками безопасности
· Внедрить мониторинг целостности пакетов в CI/CD-пайплайны

## Контекст

Это не первый случай компрометации npm-пакетов в 2026 году. Ранее группировка TeamPCP атаковала Trivy, Checkmarx KICS и более 66 npm-пакетов, украв сотни гигабайт данных. Инцидент с Axios подчёркивает необходимость многоуровневой защиты open-source экосистемы.

---

Источники:
· [GitHub — axios post-mortem #10636](https://github.com/axios/axios/issues/10636)
· [Cisco Talos — Axios NPM supply chain incident](https://blog.talosintelligence.com/axois-npm-supply-chain-incident/)
· [Elastic Security Labs — One RAT to rule them all](https://www.elastic.co/security-labs/axios-one-rat-to-rule-them-all)
· [Malwarebytes — Axios supply chain attack](https://www.malwarebytes.com/blog/news/2026/03/axios-supply-chain-attack-chops-away-at-npm-trust)
· [The Hacker News — Axios supply chain attack](https://thehackernews.com/2026/03/axios-supply-chain-attack-pushes-cross.html)
<!-- CONTENT_END -->

---

### [2026-04-14] Аренда GPU NVIDIA Blackwell выросла на 48% на фоне острейшего дефицита за 5 лет

- **Category:** nvidia
- **Template:** telegra.ph article
- **Key topics:** nvidia, gpu, ai_infrastructure, cloud_computing, hardware
- **Sources:**
  - Kucoin News (https://www.kucoin.com/news/flash/nvidia-gpu-rental-prices-surge-48-in-two-months-amid-ai-industry-s-worst-compute-shortage-in-five-years)
  - SemiAnalysis — The Great GPU Shortage (https://www.instagram.com/p/DWndYGpkjeF/)
  - Seeking Alpha (https://seekingalpha.com/news/4572260-nvidias-h100-gpu-rental-prices-surge-nearly-40-in-6-months-semianalysis)
  - TechStartups (https://techstartups.com/2026/04/13/top-tech-news-today-april-13-2026/)
- **Telegra.ph URL:** https://telegra.ph/Arenda-GPU-NVIDIA-Blackwell-vyrosla-na-48-na-fone-ostrejshego-deficita-za-5-let-04-14
- **Telegram ID:** 480
- **Status:** published

<!-- CONTENT_START -->
Облачные провайдеры зафиксировали рекордный рост цен на аренду GPU нового поколения **NVIDIA Blackwell**. Спотовая стоимость увеличилась на **48%** — с $2,75 до **$4,08 в час** — за последние два месяца. По данным индекса Ornn's Compute Price Index (интегрирован в Bloomberg Terminal), это самый серьёзный дефицит вычислительных ресурсов в ИИ-индустрии за пять лет.

## Причины кризиса

CEO Vultr Дж. Дж. Кардвелл подтвердил: все доступные электрические мощности для дата-центров на 2026 год уже полностью зарезервированы. Циклы строительства новых центров обработки данных слишком длительны и не успевают за взрывным ростом спроса на обучение и инференс ИИ-моделей.

Аналитики **Bank of America** прогнозируют сохранение дисбаланса спроса и предложения минимум до **2029 года**.

## Кто пострадал

Крупнейшие ИИ-компании уже ощутили последствия дефицита:

· **Anthropic** ограничила потребление токенов в будние часы (5:00–11:00 PT). Аптайм Claude API упал до **98,95%** при отраслевом стандарте 99,99%. Клиенты уходят к конкурентам из-за частых простоев

· **OpenAI** обрабатывает **15 млрд токенов в минуту** (рост с 6 млрд в октябре). Компания приостановила работу видеогенератора Sora, чтобы перераспределить чипы на программирование и корпоративные продукты. Финансовый директор Сара Фрайер подтвердила закрытие некоторых проектов из-за нехватки ресурсов

· **CoreWeave** повысил цены более чем на **20%** и изменил условия контрактов для малого и среднего бизнеса — срок аренды увеличен с 1 года до **3 лет**

## Экономический контекст

Выручка Anthropic выросла экспоненциально: $9 млрд (конец 2025) → $14 млрд (февраль 2026) → **$30 млрд (апрель 2026)**. Однако инфраструктура не успевает за коммерческим ростом.

Параллельно аренда GPU предыдущего поколения **H100** также подорожала почти на **40%** за шесть месяцев — до $2,35 в час по годовому контракту. Это указывает на системный характер проблемы: дефицит затрагивает весь спектр ускорителей.

## Что значит для отрасли

Рост стоимости вычислений создаёт серьёзные барьеры для стартапов и исследователей. Крупные игроки с собственными дата-центрами получают стратегическое преимущество, тогда как малые команды вынуждены оптимизировать модели или искать альтернативы.

Эксперты отмечают, что кризис ускорит переход к **энергоэффективным архитектурам** ИИ и стимулирует инвестиции в инфраструктуру возобновляемой энергетики для дата-центров.

---

Источники:
· [Kucoin News — NVIDIA GPU rental prices surge 48%](https://www.kucoin.com/news/flash/nvidia-gpu-rental-prices-surge-48-in-two-months-amid-ai-industry-s-worst-compute-shortage-in-five-years)
· [SemiAnalysis — The Great GPU Shortage](https://www.instagram.com/p/DWndYGpkjeF/)
· [Seeking Alpha — Nvidia H100 GPU rental prices surge](https://seekingalpha.com/news/4572260-nvidias-h100-gpu-rental-prices-surge-nearly-40-in-6-months-semianalysis)
· [TechStartups — AI compute rationing](https://techstartups.com/2026/04/13/top-tech-news-today-april-13-2026/)
<!-- CONTENT_END -->

---

