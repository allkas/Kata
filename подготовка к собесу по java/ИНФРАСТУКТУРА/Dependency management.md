---
tags: [maven, dependencies, java, infrastructure]
sources: [DevOps И ИНФРАСТУКТУРА Вопросы технических собеседований.pdf]
---

# Dependency management в Maven

## 1. Проблема — зачем это существует?

Java-проект зависит от десятков библиотек, которые сами зависят от других — транзитивные зависимости. Без управления версиями возникает «dependency hell»: разные части проекта тянут разные версии одной библиотеки, итог — `ClassNotFoundException` или тихая несовместимость. Maven автоматически разрешает транзитивные зависимости и определяет, какая версия победит при конфликте.

## 2. Аналогия

Ты организуешь вечеринку и просишь друзей принести закуски. Один друг приносит колу (v1) и чипсы, другой приносит колу (v2) и соус. Два ящика колы — конфликт. Maven — как хозяйка, которая заранее решила: «будет кола только одна, та, что ближе к дому» (nearest wins).

## 3. Как работает

### Объявление зависимостей

```xml
<dependencies>
    <!-- Компилируемая зависимость (scope: compile — default) -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
        <version>3.2.0</version>
    </dependency>

    <!-- Только для тестов, не попадает в production -->
    <dependency>
        <groupId>org.mockito</groupId>
        <artifactId>mockito-core</artifactId>
        <version>5.0.0</version>
        <scope>test</scope>
    </dependency>

    <!-- Предоставляется контейнером (Tomcat встроен в jar) -->
    <dependency>
        <groupId>javax.servlet</groupId>
        <artifactId>javax.servlet-api</artifactId>
        <version>4.0.1</version>
        <scope>provided</scope>
    </dependency>
</dependencies>
```

---

### Транзитивные зависимости

```
Мой проект
└── spring-boot-starter-web
    └── spring-webmvc
        └── spring-context
            └── spring-core (v6.1.0)
└── some-library
    └── spring-core (v5.3.0)   ← конфликт!
```

Maven автоматически тянет всё дерево. Конфликт версий разрешается по правилам.

---

### Правила разрешения конфликтов версий

| Правило | Описание | Пример |
|---------|----------|--------|
| **Nearest wins** | Побеждает версия, ближайшая к корню дерева | Прямая зависимость побеждает транзитивную |
| **First declared wins** | При одинаковой глубине побеждает первая объявленная | Порядок `<dependency>` в pom.xml важен |

```xml
<!-- Принудительно зафиксировать версию (override) -->
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-core</artifactId>
    <version>6.1.0</version>   <!-- эта версия победит, т.к. прямая зависимость -->
</dependency>
```

---

### dependencyManagement — централизованное управление версиями

```xml
<!-- В parent pom.xml: объявляем версии, но не тянем сами зависимости -->
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>3.2.0</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<!-- В child pom.xml: объявляем зависимость БЕЗ версии -->
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
        <!-- версия берётся из dependencyManagement родителя -->
    </dependency>
</dependencies>
```

---

### Exclusion — исключение нежелательной транзитивной зависимости

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <exclusions>
        <exclusion>
            <!-- Исключаем Tomcat, будем использовать Jetty -->
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-tomcat</artifactId>
        </exclusion>
    </exclusions>
</dependency>

<!-- Добавляем Jetty вместо Tomcat -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jetty</artifactId>
</dependency>
```

---

### Scope — область видимости зависимости

| Scope | Compile | Test | Runtime | Упаковка |
|-------|:-------:|:----:|:-------:|:--------:|
| `compile` (default) | ✅ | ✅ | ✅ | ✅ |
| `test` | ❌ | ✅ | ❌ | ❌ |
| `provided` | ✅ | ✅ | ❌ | ❌ |
| `runtime` | ❌ | ✅ | ✅ | ✅ |
| `system` | ✅ | ✅ | ❌ | ❌ |

## 4. Глубже — что важно знать

**Посмотреть дерево зависимостей:**
```bash
mvn dependency:tree                          # всё дерево
mvn dependency:tree -Dincludes=spring-core   # только конкретная библиотека
mvn dependency:resolve                       # загрузить без сборки
```

**`mvn dependency:tree` — лучший способ** диагностировать конфликты версий. Показывает, какая версия победила и почему (`omitted for conflict`, `omitted for duplicate`).

**BOM (Bill of Materials)** — специальный `pom` с только `dependencyManagement`, без кода. Spring Boot использует `spring-boot-dependencies` как BOM — он фиксирует совместимые версии сотен библиотек. Подключаешь один BOM — и все версии согласованы.

**Локальный репозиторий** (`~/.m2/repository`): Maven кэширует все скачанные артефакты локально. Первый раз тянет из Maven Central, потом из кэша.

## 5. Связи с другими концепциями

- [[Жизненный цикл Maven]] — фазы `compile`, `test`, `package` используют зависимости с нужными scope
- [[Профили Maven]] — профили могут добавлять зависимости только для конкретного окружения

## 6. Ответ на собесе (2 минуты)

Maven управляет зависимостями через `pom.xml`. Объявляю зависимости в `<dependencies>`, Maven автоматически скачивает их и все их транзитивные зависимости.

При конфликте версий срабатывает правило **nearest wins**: побеждает версия, объявленная ближе к корню дерева. Прямая зависимость всегда побеждает транзитивную. Посмотреть что победило — `mvn dependency:tree`.

`scope` контролирует когда зависимость доступна: `compile` — везде (дефолт), `test` — только в тестах, `provided` — компилируется, но не упаковывается (предоставляет контейнер). Исключить ненужную транзитивную зависимость — `<exclusions>`.

Для enterprise-проектов используют `<dependencyManagement>` в parent pom или BOM: централизованно объявляют версии, child-модули подключают зависимости без явного указания версии. Spring Boot делает именно так — `spring-boot-dependencies` BOM содержит все совместимые версии.

## Шпаргалка

| Scope | Когда нужен |
|-------|-------------|
| `compile` | Везде (default) — библиотеки в коде |
| `test` | Только тесты — JUnit, Mockito |
| `provided` | Компиляция, но не в jar — servlet-api |
| `runtime` | Только runtime — JDBC драйвер |

| Проблема | Решение |
|----------|---------|
| Конфликт версий | `mvn dependency:tree` + прямая зависимость |
| Ненужная транзитивная | `<exclusions>` |
| Разные версии в модулях | `<dependencyManagement>` в parent |
| Согласованные версии | BOM (`spring-boot-dependencies`) |

**Связи:**
- [[Жизненный цикл Maven]]
- [[Профили Maven]]
