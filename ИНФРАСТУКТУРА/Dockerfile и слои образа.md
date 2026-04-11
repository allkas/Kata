---
title: Dockerfile — из чего состоит образ
tags: [docker, dockerfile, containers]
parent: [[00 Индекс всех тем]]
prev: [[Docker vs VM]]
next: [[Kubernetes pod deployment service]]
---

# 📝 Dockerfile и слои образа

## 🧠 Ментальная модель

**Dockerfile** = рецепт
**Образ** = слоёный пирог
**Каждая инструкция** = один слой

## 📋 Основные инструкции

| Инструкция | Что делает |
|------------|-----------|
| `FROM` | Базовый образ |
| `RUN` | Команда при сборке |
| `COPY` / `ADD` | Копирование файлов |
| `WORKDIR` | Рабочая директория |
| `ENV` | Переменные окружения |
| `EXPOSE` | Открываемый порт |
| `CMD` | Команда по умолчанию |
| `ENTRYPOINT` | Фиксированная команда |

## ⚡ CMD vs ENTRYPOINT

| | CMD | ENTRYPOINT |
|--|-----|------------|
| Переопределяется | ✅ | ❌ |
| Назначение | Дефолтные аргументы | Фиксированная команда |

## 🚀 Multi-stage сборка

```dockerfile
FROM maven:3.8 AS builder
RUN mvn package

FROM openjdk:17-jre-slim
COPY --from=builder /build/app.jar 
```

связи

- [[Docker vs VM]]
-  [[Kubernetes pod deployment service]]
-  [[Garbage Collector JVM]]