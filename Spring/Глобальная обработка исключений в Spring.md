---
tags: [spring, exceptions, error-handling]
---
# Глобальная обработка исключений в Spring
## 1. @ControllerAdvice
Глобальный обработчик исключений для всех контроллеров.
```java
@ControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(EntityNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handleNotFound(EntityNotFoundException ex) {
        return new ErrorResponse(ex.getMessage());
    }
}
```
## 2. Как вернуть нужный HTTP-статус на исключение

- `@ResponseStatus` на классе исключения.
    
- `@ResponseStatus` в методе `@ExceptionHandler`.
    
- Возврат `ResponseEntity` с нужным статусом.
    

**Связи:**

- [[Исключения в Java]]
    
- [[Разница HTTP методов]]
    
- [[Spring MVC REST (Controller vs RestController)]]