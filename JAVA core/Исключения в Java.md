---
tags: [java, exceptions, core]
sources: [CORE 1 Вопросы технических собеседований.pdf]
---

# Исключения в Java

## 1. Проблема — зачем это существует?

В C и ранних языках ошибки сигнализировались через возвращаемые коды: `int result = readFile(); if (result == -1) { ... }`. Это засоряло бизнес-логику проверками, коды легко игнорировались, а источник ошибки терялся. Java решает это механизмом исключений: ошибка **выбрасывается** из места возникновения и **обязательно** обрабатывается где-то выше — иначе программа не скомпилируется (для checked) или упадёт с понятным стектрейсом.

## 2. Аналогия

Исключение — как сигнал тревоги в здании. Когда датчик срабатывает (место возникновения), он не сам тушит пожар — он **бросает сигнал** вверх по цепочке оповещения (call stack). Кто-то на нужном уровне должен **поймать** сигнал и среагировать. Если никто не поймал — здание эвакуируется полностью (JVM падает с ошибкой).

## 3. Как работает

### Иерархия Throwable:
```
Throwable
├── Error              (JVM-проблемы, не обрабатываем: OutOfMemoryError, StackOverflowError)
└── Exception
    ├── RuntimeException      (unchecked: NullPointerException, IllegalArgumentException)
    └── IOException, SQLException...  (checked: обязаны обработать)
```

### Checked vs Unchecked:
| | Checked | Unchecked |
|---|---|---|
| **Проверка** | Компилятором | Нет |
| **Обязанность** | `try-catch` или `throws` | По желанию |
| **Наследует** | `Exception` (не RuntimeException) | `RuntimeException` |
| **Примеры** | `IOException`, `SQLException` | `NPE`, `IllegalArgumentException` |
| **Смысл** | Предсказуемые внешние сбои | Баги в коде |

**Правило выбора:** checked — для восстановимых ситуаций, которые вне контроля (файл не найден, сеть упала). Unchecked — для ошибок программиста (null там где нельзя, неверный аргумент).

### Блок finally:
```java
try {
    // рискованный код
} catch (IOException e) {
    // обработка
} finally {
    // выполняется ВСЕГДА — даже если было return в try/catch
    connection.close();
}
```
**Исключения:** `finally` НЕ вызывается при `System.exit()` и при аварийном завершении JVM.

### try-with-resources (Java 7+):
```java
// До Java 7 — громоздко и небезопасно:
InputStream is = null;
try {
    is = new FileInputStream("file.txt");
    // работа
} finally {
    if (is != null) is.close(); // а если close() тоже бросит исключение?
}

// Java 7+: чисто и безопасно
try (InputStream is = new FileInputStream("file.txt");
     BufferedReader reader = new BufferedReader(new InputStreamReader(is))) {
    // работа
} // close() вызовется автоматически в обратном порядке объявления
```
**Требование:** ресурс должен реализовывать `AutoCloseable` (или `Closeable`).
**Подавление исключений:** если и в блоке `try`, и в `close()` брошено исключение — первичным считается из `try`, из `close()` добавляется как suppressed (`e.getSuppressed()`).

### Multi-catch (Java 7+):
```java
catch (IOException | SQLException e) {
    log.error("DB or IO error", e);
}
// e становится effectively final — нельзя переприсвоить
```

### Кастомный Exception:
```java
// Unchecked — для бизнес-ошибок (предпочтительно в Spring)
public class OrderNotFoundException extends RuntimeException {
    private final Long orderId;

    public OrderNotFoundException(Long orderId) {
        super("Order not found: " + orderId);
        this.orderId = orderId;
    }

    public Long getOrderId() { return orderId; }
}
```

## 4. Глубже — важные нюансы

**`return` в `finally` перекрывает `return` из `try`:**
```java
int test() {
    try { return 1; }
    finally { return 2; } // вернёт 2! return из try подавляется
}
```
Антипаттерн — никогда не пишем `return`/`throw` в `finally`.

**Checked exceptions в лямбдах не работают:**
```java
list.forEach(item -> {
    process(item); // если process() бросает IOException — не скомпилируется
});
// Решение: оборачивать в try-catch или использовать unchecked
```

## 5. Связи с другими концепциями

- [[Глобальная обработка исключений в Spring]] — `@ControllerAdvice` ловит unchecked на уровне контроллера
- [[Транзакции уровни изоляции]] — `@Transactional` откатывается по умолчанию только на `RuntimeException`

## 6. Ответ на собесе (2 минуты)

> "Исключения в Java делятся на две ветки: `Error` и `Exception`. `Error` — это JVM-проблемы вроде `OutOfMemoryError`, их не обрабатываем. `Exception` делится на checked и unchecked.
>
> **Checked** проверяются компилятором — ты обязан либо поймать, либо объявить в `throws`. Это предсказуемые внешние сбои: файл не найден, база недоступна. **Unchecked** (`RuntimeException`) — это ошибки в коде: `NullPointerException`, `IllegalArgumentException`. Их объявлять не обязательно.
>
> **В Spring я предпочитаю unchecked** для бизнес-исключений — они не загрязняют сигнатуры методов и хорошо работают с `@Transactional` (откат по умолчанию идёт на `RuntimeException`).
>
> **`try-with-resources`** — один из важнейших паттернов. До Java 7 закрытие ресурсов в `finally` было ненадёжным: если `close()` тоже бросает исключение — теряем оригинальное. `try-with-resources` решает это: ресурсы закрываются автоматически, а исключение из `close()` добавляется как suppressed.
>
> **`finally`** выполняется всегда, кроме `System.exit()`. Важный нюанс: `return` в `finally` перекроет `return` из `try` — это антипаттерн, так не делаем."

## Шпаргалка

| Концепция | Суть | Пример |
|-----------|------|--------|
| **Checked** | Компилятор обязывает обработать | `IOException`, `SQLException` |
| **Unchecked** | Ошибки программиста | `NullPointerException`, `IAE` |
| **Error** | JVM-проблемы, не обрабатываем | `OutOfMemoryError` |
| **finally** | Всегда, кроме `System.exit()` | Закрытие старых ресурсов |
| **try-with-resources** | AutoCloseable закрывается сам | `try (InputStream is = ...)` |
| **multi-catch** | Несколько типов в одном catch | `catch (A \| B e)` |
| **@Transactional rollback** | По умолчанию на RuntimeException | Проверяй при checked! |

**Связи:**
- [[Глобальная обработка исключений в Spring]]
- [[Транзакции уровни изоляции]]
