---
tags:
  - docker
  - dockerfile
  - containers
  - infrastructure
sources:
  - Вопросы технических собеседований (1).pdf
  - Алгоритмы и паттерны Вопросы технических собеседований.pdf
---

# Dockerfile и слои образа

## 1. Проблема — зачем это существует?

Разные разработчики запускают приложение по-разному: разные версии JDK, разные ОС, разные системные библиотеки — «у меня работает» становится проблемой. Dockerfile решает это: он описывает окружение воспроизводимо, как рецепт. Образ — это упакованное приложение со всем, что нужно для запуска, без зависимости от хостовой ОС.

## 2. Аналогия

Dockerfile — это рецепт торта. Каждый шаг рецепта (`FROM`, `RUN`, `COPY`) — один слой теста. Готовый торт — образ. Контейнер — конкретный кусок торта, нарезанный из него.

Если хочешь изменить начинку (только одну строку Dockerfile) — пересобирается только этот слой, остальные берутся из кэша. Как переделать только крем, не выпекая заново коржи.

## 3. Как работает

### Инструкции Dockerfile

```dockerfile
# Базовый образ — отправная точка
FROM openjdk:17-jre-slim

# Метаданные (не создают слой)
LABEL maintainer="team@example.com"

# Команда при сборке — создаёт слой
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копирование файлов из хоста в образ
COPY target/app.jar app.jar

# Переменная окружения
ENV JAVA_OPTS="-Xmx512m"

# Открываемый порт (документация, не firewall)
EXPOSE 8080

# Команда запуска контейнера
CMD ["java", "-jar", "app.jar"]
```

---

### Слои образа и кэш

Каждая инструкция `RUN`, `COPY`, `ADD` создаёт новый read-only слой. Docker кэширует слои по хэшу содержимого — если файлы не изменились, слой берётся из кэша.

```
Слой 5 (RW)  ← контейнер (runtime, можно писать)
────────────────────────────────────────
Слой 4 (RO)  COPY app.jar
Слой 3 (RO)  COPY pom.xml + mvn install
Слой 2 (RO)  RUN apt-get install
Слой 1 (RO)  FROM openjdk:17
```

**Правило оптимизации кэша:** менее изменяемые инструкции — вверх, часто изменяемые — вниз. Копировать `pom.xml` и запускать `mvn dependency:resolve` отдельно от копирования исходников — тогда зависимости кэшируются.

```dockerfile
# Плохо: любое изменение кода инвалидирует кэш maven-зависимостей
COPY . .
RUN mvn package

# Хорошо: зависимости кэшируются, пересобирается только код
COPY pom.xml .
RUN mvn dependency:resolve
COPY src/ src/
RUN mvn package -DskipTests
```

---

### CMD vs ENTRYPOINT

| | CMD | ENTRYPOINT |
|--|-----|------------|
| Переопределяется при `docker run` | Да (`docker run img echo hello`) | Нет (только `--entrypoint`) |
| Назначение | Аргументы по умолчанию | Фиксированная команда |
| Типичное использование | Дефолтные параметры | Обязательный executable |

```dockerfile
# Только ENTRYPOINT — нельзя передать другую команду
ENTRYPOINT ["java", "-jar", "app.jar"]

# CMD как аргументы по умолчанию для ENTRYPOINT
ENTRYPOINT ["java"]
CMD ["-jar", "app.jar"]
# docker run img -jar other.jar — заменит CMD

# Shell form vs exec form
CMD java -jar app.jar           # shell form: запускается через /bin/sh -c, PID 1 = sh
CMD ["java", "-jar", "app.jar"] # exec form: java = PID 1, получает SIGTERM напрямую
```

---

### Multi-stage сборка

Финальный образ не должен содержать Maven, JDK, исходники — только JRE и jar. Multi-stage: несколько `FROM`, финальный образ копирует артефакт из промежуточного.

```dockerfile
# Stage 1 — сборка
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /build
COPY pom.xml .
RUN mvn dependency:resolve
COPY src/ src/
RUN mvn package -DskipTests

# Stage 2 — финальный образ (только JRE + jar)
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=builder /build/target/app.jar app.jar
EXPOSE 8080
CMD ["java", "-jar", "app.jar"]
```

**Результат:** образ Maven ~500MB → финальный образ ~150MB. Исходники и Maven не попадают в production-образ.

## 4. Глубже — что важно знать

**`.dockerignore`** — аналог `.gitignore` для сборки. Без него `COPY . .` тянет `target/`, `.git/`, `node_modules/` в контекст сборки и в образ:

```
.git
target/
*.md
*.log
```

**Почему `RUN` нужно объединять через `&&`:**
```dockerfile
# Плохо: три слоя, apt-кэш остаётся в промежуточных слоях
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*

# Хорошо: один слой, финальный размер меньше
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
```

**COPY vs ADD:**
- `COPY` — простое копирование файлов/директорий (предпочтительно)
- `ADD` — умеет распаковывать `.tar.gz` и копировать URL (не рекомендуется без нужды — неявное поведение)

**Non-root пользователь (security best practice):**
```dockerfile
RUN addgroup --system app && adduser --system --ingroup app app
USER app
```

## 5. Связи с другими концепциями

- [[Docker vs VM]] — Docker-образ vs VM-образ, namespace/cgroups, Union FS
- [[Kubernetes pod deployment service]] — образ — то, что деплоится в Pod
- [[Жизненный цикл Maven]] — `mvn package` внутри multi-stage сборки

## 6. Ответ на собесе (2 минуты)

Dockerfile — это рецепт для создания образа. Каждая инструкция `RUN`, `COPY`, `ADD` создаёт отдельный read-only слой. Docker кэширует слои — если содержимое не изменилось, пересборка не нужна. Из-за этого важен порядок: то, что меняется редко (зависимости), — вверх; то, что меняется часто (код) — вниз.

Ключевое отличие `CMD` vs `ENTRYPOINT`: `CMD` — дефолтная команда, переопределяется при запуске. `ENTRYPOINT` — фиксированный исполняемый файл. Лучшая практика — exec form `["java", "-jar", "app.jar"]`, чтобы процесс получал `SIGTERM` напрямую без промежуточного shell.

Multi-stage сборка решает проблему раздутого образа: первый stage с Maven собирает jar, второй stage с JRE только запускает его. Maven, JDK и исходники в production не попадают — образ уменьшается с ~500MB до ~150MB.

## Шпаргалка

| Инструкция | Что делает | Создаёт слой |
|------------|-----------|:---:|
| `FROM` | Базовый образ | Нет |
| `RUN` | Команда при сборке | Да |
| `COPY` | Копирование файлов | Да |
| `ADD` | COPY + tar-распаковка + URL | Да |
| `WORKDIR` | Рабочая директория | Да |
| `ENV` | Переменная окружения | Нет |
| `EXPOSE` | Декларация порта | Нет |
| `CMD` | Команда по умолчанию | Нет |
| `ENTRYPOINT` | Фиксированная команда | Нет |

| Приём | Зачем |
|-------|-------|
| Объединить `RUN` через `&&` | Меньше слоёв, меньше размер |
| `COPY pom.xml` до `COPY src/` | Кэш зависимостей не инвалидируется |
| Multi-stage сборка | Builder-образ не попадает в production |
| `.dockerignore` | Исключить ненужное из контекста |
| `CMD ["exec", "form"]` | PID 1 = приложение, получает SIGTERM |

**Связи:**
- [[Docker vs VM]]
- [[Kubernetes pod deployment service]]
- [[Жизненный цикл Maven]]

**Hexlet:**
- [[Docker — Основы]]
