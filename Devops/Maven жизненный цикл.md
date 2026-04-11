---
tags: [maven, build, tools]
---
# Maven жизненный цикл
## 1. Фазы
- **compile** — компиляция
- **test** — тесты
- **package** — JAR/WAR
- **install** — в локальный репозиторий
- **deploy** — на удалённый
## 2. Dependency management
Управление версиями в parent POM для многомодульных проектов.
## 3. Профили Maven
Для разных окружений (dev/prod).
```xml
<profiles>
    <profile>
        <id>dev</id>
        <properties>
            <db.url>jdbc:h2:mem:dev</db.url>
        </properties>
    </profile>
</profiles>
```
**Связи:**

- [[Docker Kubernetes]]
    
- [[Spring Boot]]