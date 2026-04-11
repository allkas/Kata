---
tags: [spring, boot, auto-configuration]
---
# Spring Boot
## 1. Чем Spring Boot отличается от Spring
- **Spring** — фреймворк, требует много конфигурации.
- **Spring Boot** — надстройка с авто-конфигурацией, встроенным сервером, стартерами.
## 2. Стартеры
`spring-boot-starter-*` — набор зависимостей для конкретной функциональности (web, data-jpa, test).
## 3. Как отключить авто-конфигурацию
```java
@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})
```
## 4. @SpringBootApplication

Включает:

- `@Configuration`
    
- `@EnableAutoConfiguration`
    
- `@ComponentScan`
    

**Связи:**

- [[Spring Core IoC DI]]
    
- [[Spring MVC REST (Controller vs RestController)]]