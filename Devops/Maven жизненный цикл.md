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
## 6. Ответ на собесе (2 минуты)

> "Maven — это система сборки с фиксированным жизненным циклом. Когда запускаем `mvn package`, Maven последовательно выполняет фазы: `validate → compile → test → package`. Каждая следующая фаза включает предыдущие — нельзя запустить `package`, минуя `test`.
>
> Три основных цикла: default (сборка), clean (очистка), site (документация). В default цикле ключевые фазы: compile → test → package → install (в локальный repo) → deploy (на удалённый).
>
> Dependency management — это механизм централизованного управления версиями зависимостей в parent POM через `<dependencyManagement>`. Дочерние модули наследуют версии и не указывают их явно. Это предотвращает 'dependency hell' в многомодульных проектах."

**Связи:**

- [[Жизненный цикл Maven]]
- [[Dependency management]]
- [[Профили Maven]]
- [[Spring Boot]]

> ⚠️ Устаревший файл. Актуальные страницы находятся в `ИНФРАСТУКТУРА/`.