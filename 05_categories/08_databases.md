# Категория: Databases

## 📋 Описание

Базы данных, SQL, NoSQL, ORM и всё о работе с данными.

## 🏷️ Теги

**Основной:** `#databases`

**Дополнительные:**
```
#postgresql #mysql #mariadb #mongodb #redis #sqlite #clickhouse
#prisma #doctrine #eloquent #typeorm #drizzle #mikroorm
#sql #nosql #orm #migrations #indexing #queryoptimization
```

## 📰 Темы для публикаций

### Реляционные БД

- PostgreSQL (новые версии, фичи)
- MySQL, MariaDB
- SQLite (embedded use cases)
- ClickHouse (аналитика)

### NoSQL БД

- MongoDB (документные)
- Redis (key-value, cache)
- Cassandra, ScyllaDB (column-family)
- Neo4j (графовые)

### ORM и работа с данными

- Prisma (TypeScript-first)
- Doctrine (PHP)
- Eloquent (Laravel)
- TypeORM, MikroORM, Drizzle

### Миграции и seeders

- Версионирование схемы
- Инструменты миграций
- Rollback стратегии
- Seeders для тестов

### Оптимизация

- Индексы (B-tree, hash, GIN, GiST)
- Query optimization
- Execution plan, EXPLAIN ANALYZE
- Connection pooling

### Репликация и кластеризация

- Master-slave репликация
- Master-master
- Sharding, partitioning
- High availability

### NewSQL и специализированные БД

- TimescaleDB (time series)
- InfluxDB (metrics)
- Elasticsearch (search)
- Vector databases (Pinecone, Qdrant, Milvus)

## 🔗 Источники

### GitHub
- https://github.com/postgres/postgres
- https://github.com/mysql/mysql-server
- https://github.com/redis/redis
- https://github.com/prisma/prisma

### RSS
- https://www.postgresql.org/feed/
- https://www.mongodb.com/blog/rss

### Блоги
- https://www.postgresql.org/about/news/
- https://www.mongodb.com/blog/
- https://redis.com/blog/
- https://www.prisma.io/blog

## 📝 Примеры заголовков

- «PostgreSQL 17: новые возможности и оптимизации»
- «Prisma 6.0: улучшенная типизация и миграции»
- «Redis 8.0: новые структуры данных»
- «Vector databases для AI: сравнение решений»
- «Query optimization: от медленного запроса к быстрому»

## 🎯 Аудитория

- Backend-разработчики
- Fullstack-разработчики
- Data engineers
- DBA (database administrators)

## 📚 Связанные категории

- `#php` — ORM в PHP
- `#javascript` — ORM в Node.js
- `#devops` — managed databases, деплой
- `#ai_tools` — vector databases для AI
- `#patterns` — паттерны работы с данными

## 💡 Советы по контенту

### Для сравнений БД

- Показывай **бенчмарки**
- Сравнивай **use cases**
- Указывай **ограничения**

### Для ORM

- Показывай **код на обоих сторонах** (ORM и raw SQL)
- Объясняй **trade-offs** (удобство vs производительность)
- Давай **best practices** (N+1 проблема, eager loading)

### Для оптимизации

- Показывай **EXPLAIN ANALYZE** вывод
- Объясняй **почему индекс помогает**
- Давай **конкретные примеры** до и после
