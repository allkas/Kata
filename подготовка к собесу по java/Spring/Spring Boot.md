---
tags: [spring, boot, auto-configuration]
sources: [Spring Вопросы технических собеседований.pdf]
---

# Spring Boot

## 1. Проблема — зачем это существует?

Чистый Spring Framework мощный, но многословный. Для простого REST API нужно вручную настроить: `DispatcherServlet`, `DataSource`, `EntityManagerFactory`, `TransactionManager`, `ObjectMapper`, развернуть WAR в Tomcat. Сотни строк XML или Java-конфига. Spring Boot устраняет это через авто-конфигурацию: определяет зависимости на classpath и настраивает всё сам.

## 2. Аналогия

**Чистый Spring** — пустая квартира. Есть всё необходимое на рынке, но ты сам покупаешь мебель, подключаешь интернет, настраиваешь всё под себя.

**Spring Boot** — furnished apartment с умным управляющим. Управляющий видит что ты разработчик (spring-web на classpath) и заранее ставит компьютер, настраивает интернет, устанавливает Tomcat. Что-то не устраивает — просто заменяешь один предмет мебели (свой `@Bean`).

## 3. Spring Boot vs Spring Framework

| | Spring Framework | Spring Boot |
|---|---|---|
| **Конфигурация** | Вручную (XML / Java) | Авто-конфигурация |
| **Сервер** | Внешний Tomcat/WildFly | Встроенный (Tomcat/Jetty/Undertow) |
| **Запуск** | Деплой WAR | `java -jar app.jar` |
| **Стартеры** | Нет, зависимости вручную | `spring-boot-starter-*` |
| **Версии зависимостей** | Вручную | BOM (Bill of Materials) |

## 4. Как работает авто-конфигурация

```
1. @SpringBootApplication → @EnableAutoConfiguration
2. Spring загружает список авто-конфигураций из:
   META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
3. Каждая авто-конфигурация имеет условия:
   @ConditionalOnClass     — если класс есть на classpath
   @ConditionalOnMissingBean — если бин ещё не определён
   @ConditionalOnProperty  — если свойство задано
4. Если условие выполнено → авто-конфигурация создаёт бины
```

**Пример того, что Spring Boot делает за тебя:**
```java
// DataSourceAutoConfiguration (упрощённо):
@Configuration
@ConditionalOnClass(DataSource.class)           // есть JDBC драйвер?
@ConditionalOnMissingBean(DataSource.class)     // нет своего DataSource?
class DataSourceAutoConfiguration {
    @Bean
    DataSource dataSource(DataSourceProperties props) {
        return DataSourceBuilder.create()
            .url(props.getUrl())
            .username(props.getUsername())
            .password(props.getPassword())
            .build();
    }
}
```
Ты только пишешь в `application.properties`:
```properties
spring.datasource.url=jdbc:postgresql://localhost/mydb
spring.datasource.username=user
spring.datasource.password=pass
```

## 5. Стартеры (spring-boot-starter-*)

Стартер — это POM-агрегатор: набор **проверенных совместимых зависимостей** для конкретной функциональности. Не нужно думать о версиях и совместимости.

| Стартер | Что включает |
|---------|-------------|
| `spring-boot-starter-web` | Spring MVC + Jackson + Embedded Tomcat + Validation |
| `spring-boot-starter-data-jpa` | Hibernate + Spring Data JPA + Transaction Management |
| `spring-boot-starter-security` | Spring Security |
| `spring-boot-starter-test` | JUnit 5 + Mockito + AssertJ + Spring Test |
| `spring-boot-starter-actuator` | Health checks, metrics, info endpoints |

## 6. @SpringBootApplication

```java
@SpringBootApplication
// = @Configuration + @EnableAutoConfiguration + @ComponentScan
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

| Включённая аннотация | Что делает |
|----------------------|------------|
| `@Configuration` | Класс — источник определений бинов (`@Bean` методы) |
| `@EnableAutoConfiguration` | Запускает механизм авто-конфигурации |
| `@ComponentScan` | Сканирует текущий пакет и подпакеты на `@Component` |

## 7. Как отключить / переопределить авто-конфигурацию

### Отключить конкретную:
```java
@SpringBootApplication(exclude = {
    DataSourceAutoConfiguration.class,
    SecurityAutoConfiguration.class
})
```

### Переопределить (самый частый случай):
```java
// Spring видит твой @Bean → пропускает авто-конфигурацию (@ConditionalOnMissingBean)
@Configuration
class AppConfig {
    @Bean
    DataSource dataSource() {
        return new HikariDataSource(customConfig()); // своя настройка
    }
}
```

### Через properties:
```properties
# Отключить через свойство
spring.autoconfigure.exclude=org.springframework.boot.autoconfigure.security.SecurityAutoConfiguration
```

## 8. Связи с другими концепциями

- [[Spring Core IoC DI]] — Spring Boot надстраивается над IoC-контейнером
- [[Spring MVC REST (Controller vs RestController)]] — `spring-boot-starter-web` даёт Spring MVC
- [[Транзакции уровни изоляции]] — `spring-boot-starter-data-jpa` настраивает транзакции автоматически

## 9. Ответ на собесе (2 минуты)

> "Spring Boot — это надстройка над Spring Framework, которая устраняет boilerplate-конфигурацию через три механизма.
>
> **Авто-конфигурация:** Spring Boot смотрит на classpath — есть `spring-webmvc`? Настрою `DispatcherServlet`. Есть JDBC-драйвер? Настрою `DataSource`. Каждая авто-конфигурация обёрнута в `@ConditionalOnClass` и `@ConditionalOnMissingBean` — если ты определил свой бин, авто-конфигурация отступает.
>
> **Стартеры:** вместо ручного подбора совместимых версий — один `spring-boot-starter-web` тянет Spring MVC, Jackson, Tomcat в проверенных версиях.
>
> **Embedded server:** приложение запускается как `java -jar`, без деплоя в Tomcat.
>
> **@SpringBootApplication** = три аннотации: `@Configuration` (это источник бинов), `@EnableAutoConfiguration` (запуск авто-конфигурации), `@ComponentScan` (сканировать текущий пакет).
>
> Чтобы отключить нежелательную авто-конфигурацию — `exclude` в аннотации или просто определить свой `@Bean`."

## Шпаргалка

| Концепция | Суть | Как использовать |
|-----------|------|-----------------|
| **Авто-конфигурация** | Бины по условиям classpath | `@ConditionalOnClass/MissingBean` |
| **@SpringBootApplication** | Configuration + AutoConfig + ComponentScan | Точка входа |
| **Стартер** | Набор совместимых зависимостей | `spring-boot-starter-web` |
| **Embedded Tomcat** | Запуск через `java -jar` | Не нужен внешний сервер |
| **Переопределить** | Свой `@Bean` → авто-конфиг отступает | `@ConditionalOnMissingBean` |
| **Отключить** | `exclude` в аннотации | Или через `spring.autoconfigure.exclude` |

**Связи:**
- [[Spring Core IoC DI]]
- [[Spring MVC REST (Controller vs RestController)]]
- [[Транзакции уровни изоляции]]

**Hexlet:**
- [[Java Корпоративные приложения на Spring Boot]]
