---
tags: [java, exceptions, core]
---
# Исключения в Java
## 1. Иерархия Throwable

Throwable  
├── Error (необрабатываемые, OutOfMemoryError)  
└── Exception  
├── RuntimeException (unchecked)  
└── (другие) (checked)

text

## 2. Checked vs Unchecked
| Checked                                   | Unchecked                    |
| ----------------------------------------- | ---------------------------- |
| Проверяются компилятором                  | Не проверяются               |
| Обязаны обработать (try-catch/throws)     | Могут не обрабатывать        |
| Наследуют Exception (не RuntimeException) | Наследуют RuntimeException   |
| Пример: IOException, SQLException         | Пример: NullPointerException |
## 3. Блок finally
Выполняется всегда, кроме System.exit() или JVM crash.
## 4. try-with-resources
```java
try (FileInputStream fis = new FileInputStream("file.txt")) {
    // читаем
}
// ресурсы закрываются автоматически (AutoCloseable)
```
## 5. Multi-catch

```java

catch (IOException | SQLException e) { }
```
## 6. Создать кастомный Exception

```java

public class BusinessException extends RuntimeException {
    public BusinessException(String message) {
        super(message);
    }
}
```
**Связи:**

- [[Глобальная обработка исключений в Spring]]
    
- [[Транзакции уровни изоляции]]