#### 1. Открытие: "Проблема void-методов" (15 секунд)

> "Главная особенность void-методов в том, что они **ничего не возвращают**. Поэтому классическое тестирование через `assertEquals()` к ним неприменимо. Вместо этого мы проверяем **побочные эффекты** — что метод сделал: изменил состояние объекта, вызвал другие методы, выбросил исключение."

---

#### 2. Аналогия: "Повар без выдачи блюда" (30 секунд)

> "Я объясняю через аналогию с **поваром, который готовит блюдо, но не отдает его вам**:

Представьте, что вы тестируете повара. Он получает заказ, готовит, но вы не можете попробовать результат (метод void).

**Как проверить, что он сработал?**

> - **Проверить, что он взял нужные ингредиенты** → `verify(ingredients).take()`
>     
> - **Проверить, что он включил плиту** → `verify(stove).turnOn()`
>     
> - **Проверить, что он выбросил исключение, если ингредиентов нет** → `assertThrows()`
>     
> - **Проверить, что изменилось состояние кухни** → `assertEquals("готово", kitchen.getStatus())`
>     

Void-методы тестируются именно так — через **проверку взаимодействий и состояния**."

---

#### 3. Три основных подхода (1 минута)

**Подход 1: Проверка вызовов зависимостей (verify)**

> Это самый частый способ. Метод void должен вызвать другие методы — мы проверяем, что он это сделал.

```java

@Test
void shouldSendEmailWhenOrderCreated() {
    // given
    Order order = new Order("123");
    
    // when
    orderService.createOrder(order);  // void метод
    
    // then — проверяем, что вызван emailService
    verify(emailService).sendOrderConfirmation("123");
    verify(emailService, times(1)).send(any());
    verify(emailService, never()).sendError(any());
}
```
**Подход 2: Проверка состояния объекта**

> Если void-метод меняет состояние объекта, мы проверяем это состояние.

```java

@Test
void shouldUpdateOrderStatus() {
    // given
    Order order = new Order();
    order.setStatus(OrderStatus.NEW);
    
    // when
    orderService.processOrder(order);  // void метод
    
    // then — проверяем состояние
    assertEquals(OrderStatus.PROCESSED, order.getStatus());
    assertNotNull(order.getProcessedAt());
}
```
**Подход 3: Проверка исключений (assertThrows)**

> Если void-метод должен выбросить исключение при ошибке.

```java

@Test
void shouldThrowExceptionWhenUserNotFound() {
    // given
    when(userRepository.findById(1L)).thenReturn(Optional.empty());
    
    // when & then
    assertThrows(UserNotFoundException.class, () -> {
        userService.deleteUser(1L);  // void метод
    });
    
    // дополнительно проверяем, что ничего не удалилось
    verify(userRepository, never()).delete(any());
}
```
---

#### 4. Специальные возможности Mockito для void-методов (45 секунд)

> "Mockito предоставляет специальный синтаксис для настройки void-методов на моках и спаях."

**doNothing() — ничего не делать (дефолт для void)**

```java

// Явно указать, что void-метод ничего не делает
doNothing().when(emailService).send(anyString());
// Обычно не нужно, но полезно для читаемости или при использовании spy
```
**doThrow() — выбросить исключение при вызове**

```java

// Настроить мок на выброс исключения
doThrow(new RuntimeException("SMTP error"))
    .when(emailService)
    .send(anyString());
// Проверяем, что сервис обрабатывает ошибку
assertThrows(RuntimeException.class, () -> {
    orderService.notifyUser(order);
});
```
**doAnswer() — выполнить произвольное действие**

```java

// Выполнить кастомную логику при вызове void-метода
doAnswer(invocation -> {
    String email = invocation.getArgument(0);
    System.out.println("Sending to: " + email);
    // можно модифицировать аргументы, бросить исключение и т.д.
    return null;  // void методы возвращают null
}).when(emailService).send(anyString());
```
**doCallRealMethod() — вызвать реальный метод (для spy)**


```java

@Spy
private EmailService emailService;
// Для конкретного вызова использовать реальную реализацию
doCallRealMethod().when(emailService).send(anyString());
// Остальные вызовы остаются под контролем спая
```
---

#### 5. Важный нюанс: when() vs doX() для void-методов (30 секунд)

> "Для void-методов **нельзя** использовать стандартный `when().thenReturn()`, потому что void ничего не возвращает.

**Правильный синтаксис:**

|Что нужно|Неправильно|Правильно|
|---|---|---|
|Ничего не делать|`when(mock.method()).thenReturn(null)` ❌|`doNothing().when(mock).method()` ✅|
|Выбросить исключение|`when(mock.method()).thenThrow(...)` ❌|`doThrow(...).when(mock).method()` ✅|

**Почему?**

> - `when(mock.method())` пытается вызвать метод, чтобы получить возвращаемое значение.
>     
> - Для void это невозможно, поэтому Mockito падает с ошибкой.
>     
> - `doX().when(mock).method()` — это специальный синтаксис для void-методов."
>     

---

#### 6. Связь с прошлыми темами (30 секунд)

> "Теперь свяжу с более широким контекстом.

**Связь с Mock vs Spy:**

> - Для void-методов на моках используем `doNothing()` или `doThrow()`.
>     
> - Для спаев важно: `doCallRealMethod()` позволяет реально выполнить void-метод на спае.
>     

**Связь с сагами:**

> - В сагах много void-методов: `compensate()`, `rollback()`, `notify()`.
>     
> - При тестировании саги мы проверяем, что эти методы были вызваны в правильном порядке: `InOrder.verify(service).rollback()`
>     

**Связь с Circuit Breaker:**

> - Тестируем, что при открытом состоянии Circuit Breaker void-методы **не вызываются**: `verify(dependency, never()).call()`
>     

**Связь с Kafka:**

> - Void-методы, отправляющие сообщения в Kafka: проверяем, что `kafkaTemplate.send()` был вызван с правильными аргументами.
>     

**Связь с verify() из прошлого урока:**

> - `verify()` — основной инструмент для тестирования void-методов.
>     
> - `never()`, `times()`, `atLeast()`, `InOrder` — всё это работает с void."
>     

---

#### 7. Закрытие: "Коротко о главном" (15 секунд)

> "Резюмирую: void-методы тестируются через **проверку побочных эффектов**. Три основных подхода:
> 
> 1. **verify()** — проверяем, что вызваны нужные зависимости
>     
> 2. **assert состояния** — проверяем, что изменилось состояние объекта
>     
> 3. **assertThrows()** — проверяем, что метод выбросил исключение
>     
> 
> Для настройки void-методов на моках используем специальный синтаксис `doNothing()`, `doThrow()`, `doAnswer()`."

---

## Шпаргалка для запоминания (одна страница)

### Подходы к тестированию void-методов

|Подход|Инструмент|Когда использовать|Пример|
|---|---|---|---|
|**Проверка вызовов**|`verify()`|Метод должен вызвать другие методы|`verify(emailService).send(any())`|
|**Проверка состояния**|`assertEquals()`|Метод меняет состояние объекта|`assertEquals(Status.PROCESSED, order.getStatus())`|
|**Проверка исключений**|`assertThrows()`|Метод должен выбросить исключение|`assertThrows(Exception.class, () -> service.process())`|

### Специальный синтаксис Mockito для void

|Что нужно|Синтаксис|
|---|---|
|Ничего не делать|`doNothing().when(mock).voidMethod()`|
|Выбросить исключение|`doThrow(new RuntimeException()).when(mock).voidMethod()`|
|Выполнить кастомную логику|`doAnswer(invocation -> { ... }).when(mock).voidMethod()`|
|Вызвать реальный метод (spy)|`doCallRealMethod().when(spy).voidMethod()`|

### Связь с прошлыми темами

| Тема                | Связь                                                               |
| ------------------- | ------------------------------------------------------------------- |
| **Mock vs Spy**     | `doNothing()` для mock, `doCallRealMethod()` для spy                |
| **Сага**            | `InOrder.verify()` — проверка последовательности void-методов       |
| **Circuit Breaker** | `verify(dependency, never()).call()` — проверка, что вызовы не идут |
| **Kafka**           | `verify(kafkaTemplate).send()` — проверка отправки сообщений        |
| **verify()**        | Основной инструмент для void-методов                                |
