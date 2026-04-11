---
title: Жизненный цикл Maven — фазы
tags: [maven, build, java, lifecycle]
parent: [[00 Индекс всех тем]]
next: [[Dependency management]]
---
# 📦 Жизненный цикл Maven
## 🧠 Ментальная модель
**Конвейер сборки** — каждая фаза включает предыдущие.

compile → test → package → install → deploy  
↓ ↓ ↓ ↓ ↓  
сборка тесты упаковка в локаль на сервер

text

## 📋 Основные фазы
| Фаза | Что делает | Результат |
|------|-----------|-----------|
| `compile` | Компиляция `.java` → `.class` | `target/classes/` |
| `test` | Запуск unit-тестов | `target/surefire-reports/` |
| `package` | Упаковка в JAR/WAR | `target/app.jar` |
| `install` | В локальный репозиторий | `~/.m2/repository/` |
| `deploy` | На удалённый сервер | Nexus / Artifactory |
## ⚡ Важно
```bash
mvn package   # запустит compile → test → package
mvn install   # запустит всё + install
```
## 🔗 Связано

- [[Dependency management]]
    
- [[Профили Maven]]