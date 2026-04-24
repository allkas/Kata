---
tags: [spring, transactions, transactional, propagation]
sources: [Kata Spring Framework & HTTP.pdf]
---

# @Transactional и уровни Propagation

## 1. Проблема — зачем это существует?

Бизнес-операция часто затрагивает несколько таблиц и должна быть атомарной: либо всё сохранилось, либо всё откатилось. Ручное управление `connection.commit()` / `connection.rollback()` в каждом методе — это дублирование и ошибки. `@Transactional` декларативно описывает транзакционное поведение, а Spring применяет его через AOP-прокси прозрачно для бизнес-кода.

## 2. Аналогия

Propagation — как политика командировочных расходов:
- **REQUIRED** — если поездка уже оплачивается командировкой — присоединись к ней. Нет командировки — создай новую.
- **REQUIRES_NEW** — всегда бери отдельный бюджет, независимо от чужой командировки.
- **MANDATORY** — работаешь только если уже есть активная командировка, иначе ошибка.
- **SUPPORTS** — если есть командировка — используй, нет — работай без неё.
- **NOT_SUPPORTED** — всегда работаю без командировки, даже если она есть рядом.
- **NEVER** — запрещено работать в командировке, иначе ошибка.
- **NESTED** — sub-командировка: откат sub не трогает родительскую.

## 3. Как работает

### @Transactional через AOP

```
Client → [TransactionProxy] → [UserService.save()]
               ↓
  @Before:  TransactionManager.begin()
            → реальный метод
  @AfterReturning: TransactionManager.commit()
  @AfterThrowing:  TransactionManager.rollback()
```

Spring оборачивает бин с `@Transactional` в прокси (CGLIB или JDK). При вызове метода прокси открывает транзакцию, вызывает оригинальный метод, затем commit или rollback.

### 7 уровней Propagation

| Propagation | Есть активная транзакция | Нет активной транзакции |
|-------------|--------------------------|------------------------|
| **REQUIRED** (default) | Присоединиться | Создать новую |
| **REQUIRES_NEW** | Приостановить старую, создать новую | Создать новую |
| **MANDATORY** | Присоединиться | **Exception** |
| **SUPPORTS** | Присоединиться | Без транзакции |
| **NOT_SUPPORTED** | Приостановить старую | Без транзакции |
| **NEVER** | **Exception** | Без транзакции |
| **NESTED** | Вложенная (savepoint) | Создать новую |

```java
@Service
public class OrderService {

    @Transactional  // REQUIRED по умолчанию
    public void createOrder(OrderDto dto) {
        orderRepository.save(dto.toOrder());
        notificationService.send(dto); // тоже в REQUIRED → та же транзакция
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void logAudit(String action) {
        // всегда своя транзакция — откат createOrder не откатит audit-лог
        auditRepository.save(new AuditLog(action));
    }
}
```

### Physical vs Logical транзакция

**Physical transaction** — реальная DB-транзакция (одно соединение с СУБД, один commit/rollback).

**Logical transaction** — уровень Spring: участок кода, обёрнутый в `@Transactional`. Несколько logical могут делить одну physical (REQUIRED).

```
Вызов A (REQUIRED) → открывает physical transaction
  Вызов B (REQUIRED) → присоединяется к той же physical
    Откат B → Spring помечает logical transaction как rollback-only
  Возврат в A → A пытается commit, но видит rollback-only → rollback
```

### Rollback: что откатывает, а что нет

```java
@Transactional  // по умолчанию откат только на RuntimeException и Error
public void createOrder() throws Exception { }

@Transactional(rollbackFor = Exception.class)  // откат на любое исключение
public void createOrder() throws IOException { }

@Transactional(noRollbackFor = BusinessException.class)  // не откатывать на это
public void createOrder() { }
```

**По умолчанию `@Transactional` НЕ откатывает на checked exceptions** — только на `RuntimeException` и `Error`.

### @Transactional атрибуты

```java
@Transactional(
    propagation   = Propagation.REQUIRED,        // стратегия при вызове
    isolation     = Isolation.READ_COMMITTED,    // уровень изоляции СУБД
    readOnly      = true,                        // оптимизация для SELECT
    timeout       = 30,                          // таймаут в секундах
    rollbackFor   = Exception.class              // откат на это исключение
)
```

---

## 4. Глубже — что важно знать

**Self-invocation:** вызов `@Transactional`-метода из **того же класса** через `this` обходит прокси — транзакция не открывается. Решение: вынести в отдельный бин или инжектировать себя через `@Lazy`.

```java
@Service
class OrderService {
    @Transactional
    public void createOrder(OrderDto dto) {
        // ПРОБЛЕМА: this.logAudit() — прокси обходится, @Transactional IGNORED
        this.logAudit("create");
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void logAudit(String action) { ... } // не сработает из createOrder!
}
```

**NESTED vs REQUIRES_NEW:** NESTED использует savepoint — откат вложенной транзакции возвращает к savepoint, родительская продолжается. REQUIRES_NEW создаёт полностью отдельную физическую транзакцию.

**`readOnly = true`:** Spring подсказывает ORM (Hibernate) что это read-операция → Hibernate не отслеживает dirty checking → экономит память. PostgreSQL может направить запрос на read-реплику.

**@Transactional на уровне класса:** применяется ко всем public-методам. Метод-уровневая аннотация переопределяет классовую.

```java
@Service
@Transactional(readOnly = true)  // всем методам — readOnly
public class UserService {

    @Transactional  // перекрывает — обычная транзакция для мутации
    public User createUser(UserDto dto) { ... }

    public User findById(Long id) { ... }  // inherits readOnly = true
}
```

---

## 5. Связи с другими концепциями

- [[Spring AOP]] — `@Transactional` реализован как AOP-аспект; self-invocation обходит прокси
- [[Транзакции уровни изоляции]] — `isolation` атрибут @Transactional задаёт уровень изоляции СУБД
- [[Spring Core IoC DI]] — транзакционные бины должны быть Spring-бинами (IoC управляет прокси)

## 6. Ответ на собесе (2 минуты)

> "@Transactional работает через AOP-прокси. Когда Spring видит аннотацию, создаёт прокси-обёртку: перед вызовом открывает транзакцию, после успешного завершения — commit, после RuntimeException — rollback.
>
> **Propagation** — стратегия при вызове из транзакционного контекста. REQUIRED (default) — присоединяется к существующей или создаёт. REQUIRES_NEW — всегда своя транзакция, приостанавливает родительскую. MANDATORY — обязательно должна быть активная, иначе exception. NESTED — вложенная через savepoint.
>
> **Физические vs логические транзакции:** несколько @Transactional(REQUIRED) делят одну физическую. Если любая logical помечена rollback-only — откатится вся физическая.
>
> **Ловушка:** по умолчанию rollback только на RuntimeException, не на checked. И self-invocation — вызов @Transactional-метода через this — прокси не участвует, транзакция не стартует.
>
> **readOnly = true** — оптимизация: Hibernate отключает dirty checking, СУБД может оптимизировать."

## Шпаргалка

| Propagation | Если есть транзакция | Если нет | Когда использовать |
|-------------|---------------------|----------|-------------------|
| REQUIRED | Присоединиться | Создать | По умолчанию |
| REQUIRES_NEW | Приостановить и создать свою | Создать | Аудит, независимые логи |
| MANDATORY | Присоединиться | Exception | Метод требует вызова внутри транзакции |
| SUPPORTS | Присоединиться | Без транзакции | Опциональная транзакционность |
| NOT_SUPPORTED | Приостановить | Без транзакции | Читать вне транзакции |
| NEVER | Exception | Без транзакции | Запрет транзакций |
| NESTED | Savepoint | Создать | Откат части без отката всего |

| Атрибут | Смысл | Дефолт |
|---------|-------|--------|
| `propagation` | Стратегия при вызове | REQUIRED |
| `isolation` | Уровень изоляции СУБД | DEFAULT |
| `rollbackFor` | На каких исключениях откатывать | RuntimeException, Error |
| `readOnly` | Оптимизация для SELECT | false |
| `timeout` | Таймаут в секундах | -1 (бесконечно) |

**Связи:**
- [[Spring AOP]]
- [[Транзакции уровни изоляции]]
- [[Spring Core IoC DI]]
