---
title: Dependency management в Maven
tags: [maven, dependencies, java]
parent: [[00 Индекс всех тем]]
prev: [[Жизненный цикл Maven]]
next: [[Профили Maven]]
---
# 📚 Dependency management
## 🧠 Ментальная модель
**Dependency** = библиотека, которую тянет Maven.
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <version>3.0.0</version>
</dependency>

## 🔄 Транзитивные зависимости
```
```text

Spring Boot Starter Web
    └── Spring MVC
        └── Spring Core
            └── ... (тянет всё за собой)
```
## 🧩 Разрешение конфликтов

|Правило|Что значит|
|---|---|
|**Nearest wins**|Ближайший к корню wins|
|**First wins**|При равной глубине — первый объявленный|

## 🛠️ Exclusion (исключение)

```xml

<dependency>
    <groupId>log4j</groupId>
    <artifactId>log4j</artifactId>
    <exclusions>
        <exclusion>
            <groupId>javax.mail</groupId>
            <artifactId>mail</artifactId>
        </exclusion>
    </exclusions>
</dependency>
```
## 🔗 Связано

- [[Жизненный цикл Maven]]
    
- [[Профили Maven]]