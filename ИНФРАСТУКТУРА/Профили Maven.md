---
tags: [maven, profiles, configuration, infrastructure]
sources: [DevOps И ИНФРАСТУКТУРА Вопросы технических собеседований.pdf]
---

# Профили Maven

## 1. Проблема — зачем это существует?

Сборка для dev-окружения отличается от production: другой URL базы данных, другой уровень логирования, другие ключи. Хранить все конфигурации в одном `pom.xml` и переключать вручную — ошибкоёмко. Maven profiles — это именованные наборы настроек, которые включаются по команде или автоматически по условию.

## 2. Аналогия

Электрический щиток с несколькими переключателями: `dev`, `test`, `prod`. Включаешь один — активируются соответствующие настройки: нужные плагины, переменные, ресурсы. Остальные выключены. Не нужно лезть в каждый провод вручную.

## 3. Как работает

### Объявление профилей в pom.xml

```xml
<profiles>
    <!-- DEV профиль -->
    <profile>
        <id>dev</id>
        <activation>
            <activeByDefault>true</activeByDefault>   <!-- активен по умолчанию -->
        </activation>
        <properties>
            <db.url>jdbc:postgresql://localhost:5432/mydb</db.url>
            <log.level>DEBUG</log.level>
        </properties>
    </profile>

    <!-- PROD профиль -->
    <profile>
        <id>prod</id>
        <properties>
            <db.url>jdbc:postgresql://prod.example.com:5432/mydb</db.url>
            <log.level>WARN</log.level>
        </properties>
        <build>
            <plugins>
                <!-- Минификация только для prod -->
                <plugin>
                    <groupId>com.github.eirslett</groupId>
                    <artifactId>frontend-maven-plugin</artifactId>
                </plugin>
            </plugins>
        </build>
    </profile>

    <!-- TEST профиль — зависимости только для тестирования -->
    <profile>
        <id>integration-test</id>
        <dependencies>
            <dependency>
                <groupId>org.testcontainers</groupId>
                <artifactId>postgresql</artifactId>
                <scope>test</scope>
            </dependency>
        </dependencies>
    </profile>
</profiles>
```

---

### Активация профиля

```bash
# Явная активация через CLI
mvn package -Pprod
mvn test -Pintegration-test
mvn package -Pprod,security-scan   # несколько профилей

# Проверить какие профили активны
mvn help:active-profiles

# Деактивировать профиль по умолчанию
mvn package -P!dev
```

---

### Автоматическая активация по условиям

```xml
<profile>
    <id>windows</id>
    <activation>
        <os>
            <family>Windows</family>   <!-- по ОС -->
        </os>
    </activation>
</profile>

<profile>
    <id>java-11</id>
    <activation>
        <jdk>[11,17)</jdk>   <!-- по версии JDK -->
    </activation>
</profile>

<profile>
    <id>ci</id>
    <activation>
        <property>
            <name>env.CI</name>   <!-- по переменной окружения -->
            <value>true</value>
        </property>
    </activation>
</profile>
```

---

### Профили для разных ресурсов (application.properties)

```xml
<build>
    <resources>
        <resource>
            <directory>src/main/resources</directory>
            <filtering>true</filtering>   <!-- подставляет ${db.url} из профиля -->
        </resource>
    </resources>
</build>
```

```properties
# application.properties — переменные подставятся из активного профиля
spring.datasource.url=${db.url}
logging.level.root=${log.level}
```

## 4. Глубже — что важно знать

**Профили и Spring profiles — разные вещи:**
- Maven profiles — на уровне сборки (что включить в артефакт, какие плагины запустить)
- Spring profiles (`@Profile`, `application-dev.properties`) — на уровне запуска (какие бины создать, какой конфиг загрузить)

В современных Spring Boot проектах конфигурация окружений обычно через `application-{profile}.properties` + переменные окружения, а Maven profiles — для управления сборкой (ресурсы, плагины, зависимости).

**Наследование профилей:** дочерние pom.xml наследуют профили родителя. Профили из parent активируются, если их conditions выполнены или явно указаны.

**settings.xml** (`~/.m2/settings.xml`): глобальные профили Maven, не хранятся в репозитории — для учётных данных (репозитории, credentials). Приоритет ниже чем pom.xml.

```xml
<!-- ~/.m2/settings.xml -->
<profiles>
    <profile>
        <id>nexus</id>
        <repositories>
            <repository>
                <id>nexus</id>
                <url>https://nexus.company.com/repository/maven-public/</url>
            </repository>
        </repositories>
    </profile>
</profiles>
```

## 5. Связи с другими концепциями

- [[Жизненный цикл Maven]] — профили влияют на фазы lifecycle: добавляют плагины, изменяют ресурсы
- [[Dependency management]] — профили могут добавлять зависимости для конкретного окружения
- [[Service Discovery Config Server]] — Spring Config Server — альтернативный подход к управлению конфигурацией окружений на уровне runtime

## 6. Ответ на собесе (2 минуты)

Maven profiles — это именованные наборы настроек сборки, активируемые по команде или автоматически. Основные use cases: разные database URL для dev/prod, включение/выключение плагинов, разные ресурсы для разных окружений.

Активация: `mvn package -Pprod`. Можно активировать несколько: `mvn package -Pprod,security`. Автоматически — по ОС, версии JDK, переменной окружения. `activeByDefault` — активен без явного указания.

Важно понимать разницу с Spring profiles: Maven profiles — на уровне сборки (что положить в артефакт), Spring profiles — на уровне runtime (какие бины создать). В современных Spring Boot проектах конфиг окружений чаще делают через `application-{env}.properties` + переменные окружения, а Maven profiles — для управления плагинами и ресурсами сборки.

## Шпаргалка

| Способ активации | Синтаксис |
|-----------------|-----------|
| CLI | `mvn package -Pprod` |
| По умолчанию | `<activeByDefault>true</activeByDefault>` |
| По переменной | `<activation><property><name>CI</name></property></activation>` |
| По ОС | `<activation><os><family>Windows</family></os></activation>` |
| По JDK | `<activation><jdk>[11,17)</jdk></activation>` |

| Maven профили | Spring профили |
|--------------|----------------|
| Уровень сборки | Уровень runtime |
| `mvn -Pprod` | `--spring.profiles.active=prod` |
| Какие файлы включить в jar | Какие бины создать |
| Плагины, зависимости | `@Profile`, `application-prod.properties` |

**Связи:**
- [[Жизненный цикл Maven]]
- [[Dependency management]]
- [[Service Discovery Config Server]]
