---
tags: [testing, mockito, java]
sources: [Тестирование Вопросы технических собеседований.pdf]
---

# Как тестировать void методы в Mockito

## 1. Проблема — зачем это существует?

Классическое тестирование строится на сравнении возвращаемого значения: `assertEquals(expected, actual)`. Но void-методы ничего не возвращают. Тестировать их нужно через **побочные эффекты**: что изменилось в состоянии объекта, какие зависимости были вызваны, было ли брошено исключение.

## 2. Аналогия

Повар получил заказ, приготовил блюдо — но тебе его не отдал (void). Как проверить, что он сработал?
- Проверить, что взял нужные ингредиенты → `verify(ingredients).use()`
- Проверить, что включил плиту → `verify(stove).turnOn()`
- Проверить, что выбросил исключение при отсутствии продуктов → `assertThrows()`
- Проверить изменение состояния кухни → `assertEquals("готово", kitchen.getStatus())`

## 3. Как работает

### Три подхода к тестированию void-методов

**Подход 1: verify() — проверить вызовы зависимостей (самый частый)**

```java
@Test
void createOrder_shouldSendConfirmationEmail() {
    Order order = new Order("123");

    orderService.createOrder(order);   // void метод

    verify(emailService).sendOrderConfirmation("123");
    verify(emailService, never()).sendError(any());
}
```

**Подход 2: assertEquals() — проверить изменение состояния объекта**

```java
@Test
void processOrder_shouldUpdateStatus() {
    Order order = new Order();
    order.setStatus(OrderStatus.NEW);

    orderService.processOrder(order);   // void метод меняет статус

    assertEquals(OrderStatus.PROCESSED, order.getStatus());
    assertNotNull(order.getProcessedAt());
}
```

**Подход 3: assertThrows() — проверить исключение**

```java
@Test
void deleteUser_shouldThrowWhenNotFound() {
    when(userRepository.findById(1L)).thenReturn(Optional.empty());

    assertThrows(UserNotFoundException.class, () -> {
        userService.deleteUser(1L);   // void метод
    });

    verify(userRepository, never()).delete(any());   // убедиться, что не удалилось
}
```

---

### Специальный синтаксис Mockito для void-методов

Стандартный `when(mock.method()).thenReturn(value)` не работает для void — нечего возвращать. Используется специальный синтаксис `doX().when(mock).method()`:

```java
// doNothing — ничего не делать (дефолт для моков, явно для читаемости)
doNothing().when(emailService).send(anyString());

// doThrow — выбросить исключение
doThrow(new RuntimeException("SMTP error"))
    .when(emailService).send(anyString());

// Тест: сервис обрабатывает ошибку отправки
assertThrows(NotificationException.class, () -> orderService.notify(order));

// doAnswer — выполнить произвольную логику
doAnswer(invocation -> {
    String email = invocation.getArgument(0);
    log.info("Test: отправка на {}", email);
    return null;   // void методы возвращают null
}).when(emailService).send(anyString());

// doCallRealMethod — вызвать реальный метод на Spy
@Spy EmailService emailSpy = new EmailService();
doCallRealMethod().when(emailSpy).send(anyString());
```

**Таблица синтаксиса:**

| Нужно | Неправильно | Правильно |
|-------|-------------|-----------|
| Ничего не делать | `when(mock.voidM()).thenReturn(null)` ❌ | `doNothing().when(mock).voidM()` ✅ |
| Бросить исключение | `when(mock.voidM()).thenThrow(...)` ❌ | `doThrow(...).when(mock).voidM()` ✅ |
| Кастомная логика | — | `doAnswer(...).when(mock).voidM()` ✅ |

**Почему `when(mock.voidMethod())` не работает:** Mockito вызывает метод внутри `when()` чтобы перехватить вызов. Для void-метода на Spy это означает реальный вызов. `doX()` — специальная форма, которая настраивает мок без фактического вызова.

## 4. Глубже — что важно знать

**ArgumentCaptor для void-методов с объектами:**

```java
// void метод принимает сложный объект — хотим проверить его содержимое
orderService.createOrder(order);

ArgumentCaptor<EmailMessage> captor = ArgumentCaptor.forClass(EmailMessage.class);
verify(emailService).send(captor.capture());

EmailMessage sent = captor.getValue();
assertEquals("alice@mail.com", sent.getTo());
assertTrue(sent.getBody().contains("order-123"));
```

**Когда какой подход:**

| Сценарий | Подход |
|----------|--------|
| Void вызывает другие зависимости | `verify()` |
| Void изменяет поля объекта | `assertEquals()` на поля |
| Void должен бросать исключение | `assertThrows()` |
| Нужно проверить, ЧТО передано в зависимость | `ArgumentCaptor` + `verify` |
| Настроить void-мок на исключение | `doThrow().when()` |

## 5. Связи с другими концепциями

- [[Как проверить, что метод вызывался (verify)]] — verify() — основной инструмент для void
- [[Чем Mock отличается от Spy (Mockito)]] — doX()-синтаксис обязателен для void на Spy
- [[@Mock, @InjectMocks, @Spy — разница]] — настройка тестового контекста для void-тестов

## 6. Ответ на собесе (2 минуты)

Void-методы тестируются через побочные эффекты — три подхода. Первый и самый частый: `verify()` — проверяем, что нужные зависимости были вызваны с правильными аргументами. Второй: `assertEquals()` на состояние объекта — если void меняет поля. Третий: `assertThrows()` — если void должен бросить исключение при ошибке.

Для настройки поведения void-методов на моках нельзя использовать `when().thenReturn()` — void ничего не возвращает. Используется специальный синтаксис: `doNothing().when(mock).method()`, `doThrow().when(mock).method()`, `doAnswer().when(mock).method()`.

Если нужно проверить не факт вызова, а что именно передали в метод — `ArgumentCaptor`: перехватывает аргумент и позволяет проверить его поля через `captor.getValue()`.

## Шпаргалка

| Что проверяем | Инструмент | Пример |
|---------------|-----------|--------|
| Зависимость вызвана | `verify()` | `verify(email).send(any())` |
| Зависимость НЕ вызвана | `verify(mock, never())` | `verify(email, never()).send(any())` |
| Состояние изменилось | `assertEquals` | `assertEquals(DONE, order.getStatus())` |
| Бросит исключение | `assertThrows` | `assertThrows(Ex.class, () -> svc.do())` |
| Что передано в void | `ArgumentCaptor` | `captor.getValue().getField()` |
| Настроить void на исключение | `doThrow().when()` | `doThrow(ex).when(mock).m()` |

**Связи:**
- [[Как проверить, что метод вызывался (verify)]]
- [[Чем Mock отличается от Spy (Mockito)]]
- [[@Mock, @InjectMocks, @Spy — разница]]
