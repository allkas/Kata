---
tags: [spring, exceptions, error-handling, controlleradvice]
sources: [Spring Вопросы технических собеседований.pdf]
---

# Глобальная обработка исключений в Spring

## 1. Проблема — зачем это существует?

Без глобального обработчика: `try/catch` в каждом контроллере, дублирование кода, разные форматы ошибок. Клиент получает `500 Internal Server Error` вместо `404 Not Found` — или стектрейс в JSON. `@ControllerAdvice` выносит обработку ошибок в одно место для всего приложения.

## 2. Аналогия

`@ControllerAdvice` — как служба безопасности аэропорта. Каждый пассажир (запрос) проходит через свой гейт (контроллер). Если что-то пошло не так — служба безопасности (ControllerAdvice) перехватывает ситуацию по единому протоколу. Не каждый сотрудник гейта отдельно решает, что делать с нарушителем.

## 3. @ControllerAdvice и @ExceptionHandler

`@ControllerAdvice` — специальный `@Component`, видимый всем контроллерам. Методы с `@ExceptionHandler` внутри — обработчики конкретных типов исключений.

```java
@RestControllerAdvice  // = @ControllerAdvice + @ResponseBody
public class GlobalExceptionHandler {

    // 404 — ресурс не найден
    @ExceptionHandler(EntityNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handleNotFound(EntityNotFoundException ex) {
        return new ErrorResponse("NOT_FOUND", ex.getMessage());
    }

    // 400 — ошибка валидации Bean Validation (@Valid)
    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ErrorResponse handleValidation(MethodArgumentNotValidException ex) {
        String message = ex.getBindingResult().getFieldErrors().stream()
            .map(e -> e.getField() + ": " + e.getDefaultMessage())
            .collect(Collectors.joining(", "));
        return new ErrorResponse("VALIDATION_ERROR", message);
    }

    // 409 — бизнес-конфликт
    @ExceptionHandler(OrderAlreadyExistsException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    public ErrorResponse handleConflict(OrderAlreadyExistsException ex) {
        return new ErrorResponse("CONFLICT", ex.getMessage());
    }

    // 500 — всё остальное
    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public ErrorResponse handleUnexpected(Exception ex, HttpServletRequest request) {
        log.error("Unexpected error at {}: {}", request.getRequestURI(), ex.getMessage(), ex);
        return new ErrorResponse("INTERNAL_ERROR", "Unexpected error occurred");
    }
}

// DTO для ошибок (единый формат)
public record ErrorResponse(String code, String message) {}
```

## 4. Три способа вернуть HTTP-статус

### Способ 1: @ResponseStatus на методе обработчика
```java
@ExceptionHandler(NotFoundException.class)
@ResponseStatus(HttpStatus.NOT_FOUND)          // статус задаётся здесь
public ErrorResponse handle(NotFoundException ex) {
    return new ErrorResponse(ex.getMessage());
}
```

### Способ 2: @ResponseStatus на классе исключения
```java
@ResponseStatus(HttpStatus.NOT_FOUND)          // статус встроен в исключение
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(Long id) {
        super("User not found: " + id);
    }
}
```
Минус: смешивает бизнес-логику с HTTP — исключение знает о HTTP-статусе. Удобно для простых случаев.

### Способ 3: ResponseEntity (максимальный контроль)
```java
@ExceptionHandler(ConflictException.class)
public ResponseEntity<ErrorResponse> handleConflict(ConflictException ex) {
    ErrorResponse body = new ErrorResponse("CONFLICT", ex.getMessage());
    return ResponseEntity
        .status(HttpStatus.CONFLICT)
        .header("X-Error-Code", "CONFLICT")    // можно добавить заголовки
        .body(body);
}
```

## 5. @ControllerAdvice vs @RestControllerAdvice

```
@RestControllerAdvice = @ControllerAdvice + @ResponseBody
```

| | `@ControllerAdvice` | `@RestControllerAdvice` |
|--|--------------------|-----------------------|
| **@ResponseBody** | Нужен на каждом методе | Включён по умолчанию |
| **Применение** | Смешанные приложения (MVC + REST) | Только REST API |

## 6. Сужение области действия

По умолчанию `@ControllerAdvice` применяется ко всем контроллерам. Можно ограничить:

```java
// Только контроллеры конкретного пакета:
@ControllerAdvice("com.example.api")

// Только контроллеры определённого типа:
@ControllerAdvice(assignableTypes = {UserController.class, OrderController.class})

// Только контроллеры с определённой аннотацией:
@ControllerAdvice(annotations = RestController.class)
```

## 7. Связь с AOP

`@ControllerAdvice` — это AOP-механизм. Обработчики исключений — `@AfterThrowing` advice для всех методов всех контроллеров. Spring перехватывает исключения через `DispatcherServlet`, который делегирует `HandlerExceptionResolver`. `@ControllerAdvice` регистрируется как `ExceptionHandlerExceptionResolver`.

```
Controller → throws Exception
    ↓
DispatcherServlet
    ↓
ExceptionHandlerExceptionResolver
    ↓
@ControllerAdvice.@ExceptionHandler  ← перехват здесь
    ↓
ErrorResponse → JSON → HTTP Response
```

## 8. Связи с другими концепциями

- [[Spring AOP]] — `@ControllerAdvice` — AOP-механизм, перехват через DispatcherServlet
- [[Spring MVC REST (Controller vs RestController)]] — обрабатывает исключения из контроллеров
- [[Исключения в Java]] — иерархия исключений, checked vs unchecked
- [[Какой статус возвращать при валидации, бизнес конфликте]] — HTTP status codes 400/409/422/404

## 9. Ответ на собесе (2 минуты)

> "Без глобального обработчика — `try/catch` в каждом контроллере и разные форматы ошибок. `@ControllerAdvice` — это `@Component`, видимый всем контроллерам. Методы с `@ExceptionHandler` внутри перехватывают исключения конкретных типов.
>
> **Три способа вернуть статус:** `@ResponseStatus` на методе обработчика, `@ResponseStatus` на классе исключения, или `ResponseEntity` для полного контроля (статус + заголовки + тело).
>
> **Для REST API** использую `@RestControllerAdvice` = `@ControllerAdvice` + `@ResponseBody` — не нужно на каждом методе писать `@ResponseBody`.
>
> **Под капотом:** это AOP. DispatcherServlet ловит исключения и делегирует `ExceptionHandlerExceptionResolver`, который ищет подходящий `@ExceptionHandler` в `@ControllerAdvice`."

## Шпаргалка

| Концепция | Суть | Деталь |
|-----------|------|--------|
| **@ControllerAdvice** | Глобальный обработчик | Видим всем контроллерам |
| **@RestControllerAdvice** | @ControllerAdvice + @ResponseBody | Для REST API |
| **@ExceptionHandler** | Метод-обработчик | Указать тип исключения |
| **@ResponseStatus** | HTTP-статус | На методе или классе исключения |
| **ResponseEntity** | Полный контроль | Статус + заголовки + тело |
| **Порядок** | Более конкретный тип — первый | `EntityNotFoundException` > `Exception` |
| **Под капотом** | AOP через DispatcherServlet | ExceptionHandlerExceptionResolver |

**Связи:**
- [[Spring AOP]]
- [[Spring MVC REST (Controller vs RestController)]]
- [[Исключения в Java]]
- [[Какой статус возвращать при валидации, бизнес конфликте]]
