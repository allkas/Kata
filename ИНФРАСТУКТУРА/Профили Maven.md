---
title: Профили Maven
tags: [maven, profiles, configuration]
parent: [[00 Индекс всех тем]]
prev: [[Dependency management]]
---
# 🎛️ Профили Maven
## 🧠 Ментальная модель
**Профиль** = набор настроек для разных окружений.

dev ──► БД localhost, debug=true  
test ──► БД test-server, debug=false  
prod ──► БД prod-server, debug=false

text

## 📋 Как задать профиль
```xml
<profiles>
    <profile>
        <id>dev</id>
        <properties>
            <db.url>localhost:5432</db.url>
            <debug>true</debug>
        </properties>
    </profile>
    <profile>
        <id>prod</id>
        <properties>
            <db.url>prod.example.com</db.url>
            <debug>false</debug>
        </properties>
    </profile>
</profiles>
```
## 🚀 Активация профиля

|Способ|Команда|
|---|---|
|CLI|`mvn package -Pdev`|
|По умолчанию|`<activation><activeByDefault>true</activeByDefault></activation>`|
|По свойству|`<activation><property><name>env</name><value>dev</value></property></activation>`|

## 🔗 Связано

- [[Жизненный цикл Maven]]
    
- [[Dependency management]]