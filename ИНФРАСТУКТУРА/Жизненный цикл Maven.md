---
tags: [maven, build, java, lifecycle]
sources: [Вопросы технических собеседований (1).pdf]
---

# Жизненный цикл Maven

## 1. Проблема — зачем это существует?

Сборка Java-проекта — это не одно действие, а цепочка: скомпилировать → прогнать тесты → упаковать в JAR → загрузить в репозиторий. Без Maven это делается вручную или кастомными скриптами, у каждого разработчика по-своему. Maven стандартизирует этот процесс через декларативный жизненный цикл: пишешь `mvn install` — и Maven сам знает в каком порядке всё делать.

## 2. Аналогия

Maven — конвейер на заводе. Каждая станция (фаза) выполняет свою работу и передаёт результат следующей. Нельзя упаковать готовый продукт, не собрав детали. Нельзя отгрузить на склад, не упаковав. Запустив последнюю станцию, весь конвейер запускается автоматически с начала.

## 3. Основные фазы жизненного цикла

Maven имеет три встроенных жизненных цикла: `default`, `clean`, `site`. Главный — `default`.

### Default lifecycle (основной):

| Фаза | Что делает | Результат |
|------|-----------|-----------|
| `validate` | Проверяет корректность pom.xml | — |
| `compile` | Компилирует `.java` → `.class` | `target/classes/` |
| `test-compile` | Компилирует тесты | `target/test-classes/` |
| `test` | Запускает unit-тесты (Surefire) | `target/surefire-reports/` |
| `package` | Упаковывает в JAR/WAR | `target/app-1.0.jar` |
| `verify` | Проверяет интеграционные тесты | — |
| `install` | Копирует в локальный репозиторий | `~/.m2/repository/` |
| `deploy` | Загружает на удалённый сервер | Nexus / Artifactory |

**Ключевое правило:** каждая фаза включает все предыдущие:
```bash
mvn package   # запускает: validate → compile → test → package
mvn install   # запускает: ... → package → install
mvn deploy    # запускает: ... → install → deploy
```

### Другие циклы:
```bash
mvn clean     # удаляет папку target/
mvn clean install   # очистить и пересобрать с нуля
```

## 4. Зависимости и Dependency Management

### Транзитивные зависимости:
Если A зависит от B, а B зависит от C — Maven автоматически подтягивает C. Это транзитивная зависимость.

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <version>3.2.0</version>
    <!-- тянет: spring-web, spring-mvc, jackson, tomcat, ... -->
</dependency>
```

### Конфликт версий — правило ближайшего:
Если A нужен C:1.0, а B нужен C:2.0, Maven возьмёт ту версию, путь до которой короче в дереве зависимостей.

```bash
mvn dependency:tree   # посмотреть дерево зависимостей
```

### dependencyManagement — централизованное управление версиями:
```xml
<dependencyManagement>
    <dependencies>
        <!-- Задаём версию одним местом -->
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
            <version>2.16.0</version>
        </dependency>
    </dependencies>
</dependencyManagement>

<!-- В дочерних модулях версию указывать не нужно -->
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
</dependency>
```

### Scope зависимостей:
| Scope | Compile | Test | Runtime | Попадает в JAR |
|-------|---------|------|---------|---------------|
| `compile` (default) | ✅ | ✅ | ✅ | ✅ |
| `test` | ❌ | ✅ | ❌ | ❌ |
| `provided` | ✅ | ✅ | ❌ | ❌ (есть в контейнере) |
| `runtime` | ❌ | ✅ | ✅ | ✅ |

```xml
<dependency>
    <groupId>junit</groupId>
    <artifactId>junit</artifactId>
    <scope>test</scope>   <!-- только в тестах -->
</dependency>

<dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>javax.servlet-api</artifactId>
    <scope>provided</scope>   <!-- Tomcat сам предоставит -->
</dependency>
```

## 5. Профили Maven

Профиль — набор настроек, активируемый в зависимости от окружения.

```xml
<profiles>
    <profile>
        <id>dev</id>
        <activation>
            <activeByDefault>true</activeByDefault>
        </activation>
        <properties>
            <db.url>jdbc:h2:mem:testdb</db.url>
        </properties>
    </profile>

    <profile>
        <id>prod</id>
        <properties>
            <db.url>jdbc:postgresql://prod-server/mydb</db.url>
        </properties>
    </profile>
</profiles>
```

```bash
mvn package -P prod     # активировать профиль prod
mvn package -P dev,qa   # несколько профилей
```

Профили позволяют использовать одну кодовую базу с разными конфигурациями для dev/staging/prod.

## 6. Связи с другими концепциями

- [[Spring Boot]] — `spring-boot-starter-*` — это Maven-зависимости, управляемые через BOM
- [[Dockerfile и слои образа]] — `mvn package` создаёт JAR, который кладётся в Docker-образ
- [[Git merge vs rebase]] — CI/CD пайплайн запускает `mvn verify` при merge

## 7. Ответ на собесе (2 минуты)

> "Maven управляет сборкой через жизненный цикл с фазами. Основные: `compile` → `test` → `package` → `install` → `deploy`. Каждая фаза включает предыдущие — `mvn install` запустит всё включая тесты.
>
> **Dependency Management:** Maven автоматически тянет транзитивные зависимости. При конфликте версий берёт ближайшую в дереве. `dependencyManagement` позволяет централизованно управлять версиями в многомодульном проекте.
>
> **Scope:** `compile` — везде, `test` — только в тестах, `provided` — есть в окружении (Tomcat, JEE контейнер).
>
> **Профили:** `mvn package -P prod` активирует нужный набор настроек — разные datasource, логирование, конфигурации для разных окружений."

## Шпаргалка

| Концепция | Суть | Команда |
|-----------|------|---------|
| **compile** | Java → .class | `mvn compile` |
| **test** | Unit-тесты | `mvn test` |
| **package** | JAR/WAR | `mvn package` |
| **install** | В ~/.m2 | `mvn install` |
| **deploy** | На Nexus | `mvn deploy` |
| **clean** | Удалить target/ | `mvn clean` |
| **scope test** | Только в тестах | JUnit, Mockito |
| **scope provided** | Есть в контейнере | Servlet API |
| **dependencyManagement** | Централизованные версии | В родительском POM |
| **Профиль** | Конфиг для окружения | `-P prod` |

**Связи:**
- [[Spring Boot]]
- [[Dockerfile и слои образа]]
