---
tags: [spring, beans, lifecycle]
sources: [Kata Spring Framework & HTTP.pdf]
---

# Жизненный цикл Spring бина

## 1. Проблема — зачем это существует?

Бину нужно выполнить инициализацию после того, как контейнер внедрил зависимости (открыть коннект к БД, прочитать конфиг, прогреть кэш). И нужно корректно освободить ресурсы при остановке приложения (закрыть коннекты, сбросить буферы). Lifecycle hooks дают контролируемые точки входа для этой логики без ручного управления порядком создания.

## 2. Аналогия

Жизненный цикл бина — как жизнь сотрудника в компании: нанят → прошёл онбординг (инициализация) → работает (используется) → уволен с передачей дел (destroy). HR (Spring) управляет каждой стадией. Сотрудник может выполнить особые действия в ключевые моменты (подписать договор, сдать ноутбук), не беспокоясь об остальных деталях.

## 3. Как работает

### 6 шагов жизненного цикла (по Борисову)

```
1. INSTANTIATION    — создание объекта (вызов конструктора)
        ↓
2. PROPERTY INJECTION — внедрение зависимостей (@Autowired, @Value, XML-свойства)
        ↓
3. AWARE INTERFACES — установка контекстных ссылок
        ↓
4. BeanPostProcessor.postProcessBeforeInitialization()
        ↓
5. INITIALIZATION   — инициализационные методы
        ↓
6. BeanPostProcessor.postProcessAfterInitialization()
        ↓
   [БИН ГОТОВ К ИСПОЛЬЗОВАНИЮ]
        ↓
   [ОСТАНОВКА ПРИЛОЖЕНИЯ]
        ↓
7. DESTRUCTION      — методы уничтожения
```

### Шаг 3 — Aware-интерфейсы

Spring вызывает Aware-методы для предоставления бину ссылок на инфраструктуру:

```java
@Component
public class MyBean implements BeanNameAware, ApplicationContextAware {

    @Override
    public void setBeanName(String name) {
        // имя бина в контейнере ("myBean")
    }

    @Override
    public void setApplicationContext(ApplicationContext ctx) {
        // ссылка на ApplicationContext
    }
}
```

| Интерфейс | Что устанавливает |
|-----------|-----------------|
| `BeanNameAware` | имя бина |
| `BeanFactoryAware` | ссылка на BeanFactory |
| `ApplicationContextAware` | ссылка на ApplicationContext |
| `EnvironmentAware` | ссылка на Environment |

### Шаг 5 — Инициализация (3 способа, порядок важен!)

```java
@Component
public class DatabaseConnectionPool
        implements InitializingBean {

    @PostConstruct              // 1. Вызывается ПЕРВЫМ
    public void init() {
        System.out.println("@PostConstruct");
    }

    @Override
    public void afterPropertiesSet() {  // 2. Вызывается ВТОРЫМ
        System.out.println("InitializingBean.afterPropertiesSet");
    }

    // 3. Вызывается ТРЕТЬИМ (задан через @Bean(initMethod="customInit"))
    public void customInit() {
        System.out.println("initMethod");
    }
}
```

**Порядок инициализации:**
1. `@PostConstruct` — JSR-250, рекомендуется
2. `InitializingBean.afterPropertiesSet()` — Spring-специфичный интерфейс
3. `initMethod` из `@Bean(initMethod="...")` или XML `init-method`

### Шаг 7 — Уничтожение (3 способа, зеркальный порядок)

```java
@Component
public class DatabaseConnectionPool
        implements DisposableBean {

    @PreDestroy                 // 1. Вызывается ПЕРВЫМ
    public void preDestroy() {
        System.out.println("@PreDestroy");
    }

    @Override
    public void destroy() {    // 2. Вызывается ВТОРЫМ
        System.out.println("DisposableBean.destroy");
    }

    // 3. Вызывается ТРЕТЬИМ (задан через @Bean(destroyMethod="cleanup"))
    public void cleanup() {
        System.out.println("destroyMethod");
    }
}
```

> **Важно:** методы уничтожения вызываются **только для singleton-бинов**. Для prototype Spring не отслеживает бины после выдачи — cleanup нужно делать вручную.

### Полная схема с кодом

```java
@Component
public class FullLifecycleBean
        implements BeanNameAware, InitializingBean, DisposableBean {

    private String beanName;

    // Шаг 1: конструктор
    public FullLifecycleBean() {
        System.out.println("1. Constructor");
    }

    // Шаг 2: внедрение зависимостей
    @Autowired
    private SomeService service; // Spring внедрит после конструктора

    // Шаг 3: Aware
    @Override
    public void setBeanName(String name) {
        this.beanName = name;
        System.out.println("3. BeanNameAware: " + name);
    }

    // Шаг 4: BeanPostProcessor.postProcessBefore (вызывается Spring автоматически)

    // Шаг 5: @PostConstruct → afterPropertiesSet → initMethod
    @PostConstruct
    public void postConstruct() {
        System.out.println("5a. @PostConstruct — зависимости уже внедрены!");
    }

    @Override
    public void afterPropertiesSet() {
        System.out.println("5b. afterPropertiesSet");
    }

    // Шаг 6: BeanPostProcessor.postProcessAfter (вызывается Spring автоматически)

    // Шаг 7: @PreDestroy → destroy → destroyMethod
    @PreDestroy
    public void preDestroy() {
        System.out.println("7a. @PreDestroy");
    }

    @Override
    public void destroy() {
        System.out.println("7b. DisposableBean.destroy");
    }
}
```

---

## 4. Глубже — Scope бинов

### Scopes

| Scope | Жизненный цикл | Применение |
|-------|---------------|------------|
| **singleton** (default) | Один экземпляр на контейнер, живёт до закрытия | Сервисы, репозитории |
| **prototype** | Новый экземпляр при каждом запросе | Stateful-объекты |
| **request** | Один экземпляр на HTTP-запрос | Web-слой (userId, корзина) |
| **session** | Один экземпляр на HTTP-сессию | Пользовательская сессия |
| **websocket** | Один экземпляр на WebSocket-сессию | WebSocket-обработчики |

```java
@Bean
@Scope("prototype")
public ReportBuilder reportBuilder() {
    return new ReportBuilder();
}

// Или:
@Component
@Scope(value = WebApplicationContext.SCOPE_REQUEST, proxyMode = ScopedProxyMode.TARGET_CLASS)
public class RequestContext { ... }
```

### Singleton vs Prototype — проблема

```java
// ПРОБЛЕМА: singleton зависит от prototype
@Component  // singleton
public class UserService {
    @Autowired
    private UserSession session; // prototype — но Spring внедрит ОДИН РАЗ

    // session будет одна и та же для всех запросов!
}

// РЕШЕНИЕ 1: @Lookup
@Component
public abstract class UserService {
    @Lookup
    public abstract UserSession getSession(); // Spring переопределит метод
}

// РЕШЕНИЕ 2: proxyMode
@Component
@Scope(value = "request", proxyMode = ScopedProxyMode.TARGET_CLASS)
public class UserSession { ... }
```

### Lazy initialization

```java
@Component
@Lazy  // создать только при первом обращении, не при старте
public class HeavyService { ... }

// Для всего приложения (Spring Boot):
// spring.main.lazy-initialization=true
```

---

## 5. Связи с другими концепциями

- [[Spring Core IoC DI]] — IoC-контейнер управляет lifecycle; BeanPostProcessor — ключевой участник
- [[Spring AOP]] — AOP-прокси создаётся в postProcessAfterInitialization (шаг 6)
- [[Транзакции уровни изоляции]] — @Transactional применяется через AOP на шаге 6

## 6. Ответ на собесе (2 минуты)

> "Жизненный цикл Spring-бина — 6 шагов (по Борисову):
>
> 1. **Instantiation** — вызов конструктора.
> 2. **Property injection** — Spring внедряет `@Autowired`-зависимости, `@Value`.
> 3. **Aware-интерфейсы** — бин получает ссылки на контекст: `setBeanName`, `setApplicationContext`.
> 4. **BeanPostProcessor.postProcessBeforeInitialization** — например, обработка `@PostConstruct`.
> 5. **Initialization** — в порядке: `@PostConstruct` → `afterPropertiesSet` → `initMethod`.
> 6. **BeanPostProcessor.postProcessAfterInitialization** — здесь AOP-прокси (@Transactional, @Cacheable).
>
> Затем бин готов к использованию.
>
> При остановке: `@PreDestroy` → `DisposableBean.destroy()` → `destroyMethod`. Только для singleton — prototype Spring не уничтожает.
>
> **Scope:** singleton (по умолчанию) — один экземпляр на контейнер. prototype — новый при каждом `getBean`. request/session — web-scoped, живут в рамках HTTP-запроса/сессии."

## Шпаргалка

| Шаг | Что происходит | Хуки |
|-----|---------------|------|
| 1. Instantiation | Вызов конструктора | — |
| 2. Property injection | @Autowired, @Value | — |
| 3. Aware | Контекстные ссылки | BeanNameAware, ApplicationContextAware |
| 4. BPP Before | Пред-обработка | BeanPostProcessor.postProcessBefore |
| 5. Init | Инициализация | @PostConstruct → afterPropertiesSet → initMethod |
| 6. BPP After | Пост-обработка, **AOP-прокси** | BeanPostProcessor.postProcessAfter |
| 7. Destroy | Уничтожение (singleton) | @PreDestroy → destroy → destroyMethod |

| Scope | Когда создаётся | Когда уничтожается |
|-------|----------------|-------------------|
| singleton | При старте контейнера | При закрытии контейнера |
| prototype | При каждом getBean() | **Не уничтожается Spring** |
| request | При каждом HTTP-запросе | По окончании запроса |
| session | При создании HTTP-сессии | По окончании сессии |

**Связи:**
- [[Spring Core IoC DI]]
- [[Spring AOP]]
- [[Транзакции уровни изоляции]]
