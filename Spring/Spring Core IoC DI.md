---
tags: [spring, ioc, di, core]
sources: [Spring Вопросы технических собеседований.pdf]
---

# Spring Core IoC DI

## 1. Проблема — зачем это существует?

Без IoC класс сам создаёт свои зависимости: `new OrderRepository()` внутри `OrderService`. Это жёсткая связь: нельзя подменить реализацию, нельзя изолировать в тесте без реальной БД. IoC переворачивает управление: не класс ищет зависимости — Spring Container их предоставляет.

## 2. Аналогия

IoC — как кадровое агентство. Обычно новый сотрудник (класс) сам ищет всё нужное для работы (зависимости). С IoC: компания (Spring Container) предоставляет сотруднику всё заранее — компьютер, доступы, коллег. Сотрудник только объявляет что нужно — через конструктор. Подмена коллеги (реализации) — без изменений у сотрудника.

## 3. IoC и DI

**IoC (Inversion of Control):** контейнер управляет жизненным циклом объектов и их связями. Класс не вызывает `new` для зависимостей.

**DI (Dependency Injection):** конкретный паттерн реализации IoC. Зависимости «вливаются» снаружи через конструктор, сеттер или поле.

```java
// Без DI — жёсткая связь:
class OrderService {
    private OrderRepository repo = new JpaOrderRepository(); // нельзя подменить
}

// С DI — loose coupling:
class OrderService {
    private final OrderRepository repo; // интерфейс

    public OrderService(OrderRepository repo) { // Spring инжектирует
        this.repo = repo;
    }
}
```

## 4. Bean Scopes

| Scope | Экземпляров | Когда создаётся | Применение |
|-------|-------------|----------------|------------|
| **singleton** (default) | 1 на контейнер | При старте | Stateless сервисы, репозитории |
| **prototype** | Новый при каждом `getBean()` | По запросу | Stateful объекты |
| **request** | 1 на HTTP-запрос | Каждый запрос | Request-специфичный стейт |
| **session** | 1 на HTTP-сессию | Каждая сессия | Данные пользователя |

### Ловушка: prototype в singleton:
```java
@Component // singleton
class OrderService {
    @Autowired
    PrototypeBean bean; // инжектируется ОДИН РАЗ при создании OrderService
                       // bean всегда один и тот же, несмотря на prototype scope!
}
// Решение: ApplicationContext.getBean() или @Lookup-метод
@Lookup
protected PrototypeBean getPrototypeBean() { return null; } // Spring переопределяет
```

## 5. @Component, @Service, @Repository, @Controller

Все четыре — стереотипы (`@Component` под капотом). Разница в **семантике** и **доп. поведении**:

| Аннотация | Слой | Дополнительное поведение |
|-----------|------|--------------------------|
| `@Component` | Любой | Только регистрация в контейнере |
| `@Service` | Бизнес-логика | Нет (только семантика) |
| `@Repository` | Доступ к данным | Перехват JPA/JDBC исключений → `DataAccessException` |
| `@Controller` | Веб-слой | Обрабатывается `DispatcherServlet` |

`@Repository` важен: если Hibernate бросит `PersistenceException`, Spring оборачивает её в иерархию `DataAccessException` — это позволяет менять ORM без изменения кода выше.

## 6. @Autowired: куда ставить

### Инъекция в поле (field injection) — не рекомендуется:
```java
@Autowired
private OrderRepository repo; // плохо
```
- Зависимости скрыты — нельзя создать объект без Spring
- Нельзя сделать `final`
- Трудно тестировать: нужен Spring Context или рефлексия

### Инъекция через сеттер (setter injection):
```java
@Autowired
public void setRepo(OrderRepository repo) { this.repo = repo; }
```
- Для **опциональных** зависимостей (`@Autowired(required = false)`)
- Позволяет менять зависимость после создания

### Инъекция через конструктор (constructor injection) — рекомендуется:
```java
private final OrderRepository repo;
private final PaymentService paymentService;

// @Autowired не нужен если один конструктор (Spring Boot 2+)
public OrderService(OrderRepository repo, PaymentService paymentService) {
    this.repo = repo;
    this.paymentService = paymentService;
}
```
- Зависимости **явные** и **обязательные**
- Поля `final` — immutable после создания
- Тест без Spring: `new OrderService(mockRepo, mockPayment)`

## 7. Жизненный цикл бина

```
1. BeanDefinition loaded     ← component scan / @Configuration
2. BeanFactory создаёт       ← вызов конструктора
3. Inject зависимостей       ← @Autowired поля/сеттеры
4. BeanPostProcessor.before  ← AOP-прокси создаётся здесь
5. @PostConstruct            ← инициализация (открыть соединение, загрузить кэш)
6. Bean готов к использованию
   ...
7. @PreDestroy               ← при завершении контекста (закрыть ресурсы)
8. destroy()
```

```java
@Component
class CacheService {
    private Map<String, String> cache;

    @PostConstruct
    void init() { cache = loadFromDB(); } // вызывается после DI

    @PreDestroy
    void cleanup() { cache.clear(); } // при shutdown
}
```

## 8. Циклические зависимости

```
A depends on B, B depends on A → Spring не может создать ни один
```

С **constructor injection** — ошибка при старте (`BeanCurrentlyInCreationException`). Это правильно — сигнал о проблеме дизайна.

С **setter/field injection** — Spring решает через early reference: создаёт неполный A, кладёт в кэш, создаёт B с этим незавершённым A, завершает A.

**Решения:**
```java
// 1. @Lazy — отложенная инициализация
@Autowired @Lazy
private ServiceB serviceB;

// 2. Рефакторинг — вынести общую логику в третий сервис (лучшее решение)
// A → C, B → C (нет цикла)
```

## 9. Связи с другими концепциями

- [[Интерфейс vs абстрактный класс]] — DI работает через интерфейсы (DIP из SOLID)
- [[Принципы SOLID]] — IoC/DI — прямая реализация принципа DIP
- [[Spring AOP]] — AOP-прокси создаётся как BeanPostProcessor в жизненном цикле
- [[Транзакции уровни изоляции]] — @Transactional работает через Spring DI + AOP

## 10. Ответ на собесе (2 минуты)

> "IoC — это принцип: не класс управляет своими зависимостями, а контейнер (Spring ApplicationContext). DI — конкретная реализация: зависимости передаются снаружи через конструктор, сеттер или поле.
>
> **Зачем:** loose coupling. `OrderService` зависит от интерфейса `OrderRepository`, а не от `JpaOrderRepository`. Spring инжектирует нужную реализацию. В тесте — подменяем на mock без изменений.
>
> **Scopes:** singleton — один на контейнер, по умолчанию, для stateless сервисов. Prototype — новый при каждом запросе, для stateful. Ловушка: prototype в singleton инжектируется один раз — нужен @Lookup.
>
> **@Autowired:** конструктор — рекомендуется. Зависимости явные, final, тест без Spring. Поле — антипаттерн: скрытые зависимости, нельзя final.
>
> **Циклические зависимости:** с constructor injection — ошибка при старте (правильно, это дизайн-проблема). Решаю рефакторингом или @Lazy. С field/setter injection Spring решает через early reference, но лучше не допускать."

## Шпаргалка

| Концепция | Суть | Деталь |
|-----------|------|--------|
| **IoC** | Контейнер управляет объектами | ApplicationContext |
| **DI** | Зависимости снаружи | constructor / setter / field |
| **singleton** | 1 экземпляр | Default scope, stateless |
| **prototype** | Новый при каждом запросе | Stateful, @Lookup в singleton |
| **@Repository** | DAO + exception translation | JPA исключения → DataAccessException |
| **Constructor DI** | Рекомендуется | final, testable, explicit |
| **Circular dep** | @Lazy или рефакторинг | С конструктором — сразу ошибка |
| **@PostConstruct** | После DI | Инициализация |
| **@PreDestroy** | При shutdown | Освобождение ресурсов |

**Связи:**
- [[Интерфейс vs абстрактный класс]]
- [[Принципы SOLID]]
- [[Spring AOP]]
- [[Транзакции уровни изоляции]]
