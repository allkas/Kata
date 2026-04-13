---
tags: [spring, aop, proxy]
sources: [Spring Вопросы технических собеседований.pdf]
---

# Spring AOP

## 1. Проблема — зачем это существует?

Логирование, проверка безопасности, управление транзакциями, метрики — эти задачи повторяются в каждом методе каждого сервиса. Без AOP: копируй-вставляй в сотни методов. При изменении логики логирования — правь сотни мест. AOP (Aspect-Oriented Programming) выносит эти **сквозные задачи** в отдельные модули и применяет их декларативно.

## 2. Аналогия

AOP — как система видеонаблюдения в городе. Вместо того чтобы ставить камеру **внутрь** каждой машины (добавлять логирование в каждый метод), камеры (аспекты) размещаются на **перекрёстках** (join points). Камера автоматически снимает все машины, проходящие через заданный перекрёсток (pointcut), и выполняет нужное действие (advice).

## 3. Ключевые понятия

| Термин | Суть | Пример |
|--------|------|--------|
| **Aspect** | Модуль со сквозной логикой | `LoggingAspect`, `SecurityAspect` |
| **Join Point** | Точка выполнения программы | Вызов метода (в Spring — только это) |
| **Advice** | Что и когда делать | `@Before`, `@After`, `@Around` |
| **Pointcut** | Выражение выбора Join Points | `execution(* com.example.service.*.*(..))` |
| **Weaving** | Применение аспектов к объектам | Spring делает в runtime через прокси |

### Виды Advice:
```java
@Aspect @Component
public class LoggingAspect {

    @Before("execution(* com.example.service.*.*(..))")
    public void logBefore(JoinPoint jp) {
        log.info("→ {}", jp.getSignature()); // до метода
    }

    @AfterReturning(pointcut = "serviceLayer()", returning = "result")
    public void logAfter(Object result) {
        log.info("← result: {}", result); // после успешного возврата
    }

    @AfterThrowing(pointcut = "serviceLayer()", throwing = "ex")
    public void logError(Exception ex) {
        log.error("✗ exception: {}", ex.getMessage()); // после исключения
    }

    @Around("serviceLayer()")
    public Object timeIt(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.currentTimeMillis();
        try {
            return pjp.proceed(); // вызов оригинального метода
        } finally {
            log.info("{}ms — {}", System.currentTimeMillis() - start,
                     pjp.getSignature());
        }
    }

    @Pointcut("execution(* com.example.service.*.*(..))")
    public void serviceLayer() {} // переиспользуемый pointcut
}
```

## 4. Как Spring реализует AOP — прокси

Spring AOP — **runtime weaving** через прокси-объекты. При создании бина с аспектом Spring оборачивает его в прокси. Клиент получает прокси вместо реального объекта.

```
Client → [Proxy] → [Real Bean]
           ↑
      Выполняет Advice
```

### JDK Dynamic Proxy:
- Создаёт прокси, **реализующий те же интерфейсы**
- Требует наличия интерфейса у целевого класса
- Работает через `java.lang.reflect.Proxy`

### CGLIB Proxy:
- Создаёт **подкласс** целевого класса
- Работает без интерфейсов
- Не может проксировать `final` классы и `final` методы
- Default в Spring Boot 2.x+ (даже если интерфейс есть)

```java
// JDK proxy — только если интерфейс:
@Service
class OrderService implements IOrderService { ... }
// → прокси реализует IOrderService

// CGLIB — всегда в Spring Boot по умолчанию:
@Service
class OrderService { ... } // нет интерфейса — CGLIB
// → прокси является подклассом OrderService
```

## 5. Глубже — ловушка self-invocation

**Ключевая проблема AOP:** вызов метода **внутри того же класса** обходит прокси.

```java
@Service
class OrderService {

    @Transactional
    public void createOrder(OrderDto dto) {
        // ... создаём заказ
        notifyUser(dto); // вызов через this — ПРОКСИ ОБХОДИТСЯ
    }

    @Transactional(propagation = REQUIRES_NEW)
    public void notifyUser(OrderDto dto) {
        // @Transactional здесь ИГНОРИРУЕТСЯ — транзакция не открывается
    }
}
```

**Почему:** клиент вызывает `orderService.createOrder()` через прокси. Но внутри метода `this.notifyUser()` — прямой вызов, прокси не участвует.

**Решения:**
```java
// 1. Инжектировать сам себя (через ApplicationContext или @Lazy self-injection):
@Autowired @Lazy
private OrderService self;
self.notifyUser(dto); // через прокси

// 2. Вынести notifyUser в отдельный бин
// 3. Использовать ApplicationEventPublisher
```

## 6. @Transactional как AOP

`@Transactional` — встроенный аспект Spring:
```
Client → [TransactionProxy] → [OrderService]
                ↓
    @Before: TransactionManager.begin()
    → вызов метода
    @AfterReturning: TransactionManager.commit()
    @AfterThrowing: TransactionManager.rollback()
```

Именно поэтому self-invocation ломает `@Transactional` — нет прокси, нет транзакции.

## 7. Связи с другими концепциями

- [[Spring Core IoC DI]] — AOP-прокси создаётся BeanPostProcessor'ом в жизненном цикле бина
- [[Транзакции уровни изоляции]] — `@Transactional` реализован через AOP
- [[Глобальная обработка исключений в Spring]] — `@ControllerAdvice` — тоже AOP-механизм

## 8. Ответ на собесе (2 минуты)

> "AOP решает проблему сквозных задач — логирование, транзакции, безопасность. Вместо дублирования в каждом методе — отдельный Aspect с Pointcut (какие методы перехватывать) и Advice (что делать).
>
> **Spring AOP работает через прокси.** Когда бин помечен аннотацией (например, @Transactional), Spring при старте оборачивает его в прокси-объект. Клиент получает прокси, прокси выполняет advice и вызывает оригинальный метод.
>
> **JDK proxy vs CGLIB:** JDK создаёт прокси через интерфейс, CGLIB — через подкласс. Spring Boot 2.x+ использует CGLIB по умолчанию. CGLIB не может проксировать final классы и методы.
>
> **Главная ловушка:** self-invocation. Вызов `@Transactional`-метода из того же класса через `this` обходит прокси — транзакция не стартует. Решение: вынести в отдельный бин или инжектировать себя через @Lazy."

## Шпаргалка

| Концепция | Суть | Пример |
|-----------|------|--------|
| **Aspect** | Модуль сквозной логики | `LoggingAspect` |
| **Pointcut** | Какие методы перехватывать | `execution(* service.*.*(..))` |
| **@Before/@After** | До/после метода | Логирование |
| **@Around** | Обёртка с `proceed()` | Замер времени |
| **JDK Proxy** | Через интерфейс | Требует интерфейс |
| **CGLIB** | Через подкласс | Default в Spring Boot, нельзя `final` |
| **Self-invocation** | Обходит прокси | `this.method()` — нет AOP |
| **@Transactional** | AOP-аспект | Before=begin, AfterReturn=commit |

**Связи:**
- [[Spring Core IoC DI]]
- [[Транзакции уровни изоляции]]
- [[Глобальная обработка исключений в Spring]]
