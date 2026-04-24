---
tags: [testing, mockito, junit, unit-tests]
sources: [Вопросы технических собеседований (1).pdf]
---

# Unit-тесты Mockito

## 1. Проблема — зачем это существует?

`OrderService` зависит от `UserRepository`, `PaymentService`, `EmailService`. Чтобы протестировать его логику, нужно поднять базу, платёжный шлюз, почтовый сервер. Это медленно, нестабильно, невоспроизводимо. Mockito создаёт заменители (test doubles) для зависимостей — изолирует тестируемый код от инфраструктуры.

## 2. Аналогия

Unit-тест — испытание пилота на авиасимуляторе. Симулятор (Mockito) полностью имитирует поведение самолёта (зависимостей). Пилот (тестируемый код) тренируется в изолированных условиях. Не нужно реальный самолёт и аэродром — нужно только проверить реакцию пилота на ситуации.

## 3. Анатомия теста с Mockito

```java
@ExtendWith(MockitoExtension.class)    // инициализирует @Mock, @Spy, @InjectMocks
class OrderServiceTest {

    @Mock
    private UserRepository userRepository;   // полностью поддельный

    @Mock
    private EmailService emailService;       // полностью поддельный

    @InjectMocks
    private OrderService orderService;       // реальный, зависимости внедрены

    @Test
    void createOrder_whenUserExists_shouldSaveAndNotify() {
        // Arrange (Given) — настройка моков
        User user = new User(1L, "Alice");
        when(userRepository.findById(1L)).thenReturn(Optional.of(user));

        OrderRequest request = new OrderRequest(1L, List.of("item1"));

        // Act (When) — вызов тестируемого метода
        orderService.createOrder(request);

        // Assert (Then) — проверки
        verify(userRepository).save(any(Order.class));       // был вызван save?
        verify(emailService).sendConfirmation(eq("Alice")); // был вызван sendConfirmation?
    }
}
```

## 4. @Mock vs @Spy vs @InjectMocks

| Аннотация | Что создаёт | Реальное поведение | Когда использовать |
|-----------|------------|-------------------|-------------------|
| `@Mock` | Полностью поддельный объект | Нет (всё заглушки) | Изоляция зависимостей |
| `@Spy` | Обёртка над реальным объектом | Да (по умолчанию) | Частичный контроль |
| `@InjectMocks` | Реальный тестируемый объект | Да (его код) | Тестируемый класс |

**Mock — дублёр актёра:**
```java
@Mock
private UserRepository userRepository;
// Все методы — заглушки: null, 0, false по умолчанию
when(userRepository.findById(1L)).thenReturn(Optional.of(user));
```

**Spy — актёр с правкой сценария:**
```java
@Spy
private UserService userService = new UserService();
// Реальные методы работают, отдельные можно переопределить:
doReturn(cachedUser).when(userService).findById(1L);
// Важно: doReturn().when() — не when().thenReturn(), иначе реальный метод вызовется
```

Подробнее: [[Чем Mock отличается от Spy (Mockito)]]

## 5. Настройка поведения моков

```java
// when().thenReturn() — вернуть значение
when(userRepository.findById(1L)).thenReturn(Optional.of(user));

// when().thenThrow() — выбросить исключение
when(userRepository.findById(99L)).thenThrow(new UserNotFoundException(99L));

// when().thenAnswer() — динамическое поведение
when(userRepository.save(any())).thenAnswer(inv -> inv.getArgument(0));

// doNothing() — для void-методов (или Spy)
doNothing().when(emailService).sendConfirmation(any());

// doThrow() — для void-методов
doThrow(new RuntimeException("Mail failed")).when(emailService).send(any());
```

## 6. Проверка вызовов — verify()

```java
// Был ли вызван метод?
verify(userRepository).save(any(Order.class));

// Ровно N раз:
verify(emailService, times(2)).send(any());

// Ни разу:
verify(emailService, never()).sendError(any());

// Захват аргумента для проверки:
ArgumentCaptor<Order> captor = ArgumentCaptor.forClass(Order.class);
verify(userRepository).save(captor.capture());
assertEquals("Alice", captor.getValue().getOwnerName());

// Порядок вызовов (InOrder):
InOrder inOrder = inOrder(paymentService, emailService);
inOrder.verify(paymentService).charge(any());
inOrder.verify(emailService).sendReceipt(any());
```

Подробнее: [[Как проверить, что метод вызывался (verify)]]

## 7. Тестирование void-методов

Void-методы не возвращают результат — проверяем поведение через `verify()` или ловим исключения:

```java
// Проверить что void-метод был вызван:
orderService.cancelOrder(orderId);
verify(notificationService).sendCancellation(orderId);

// Настроить void-метод на исключение:
doThrow(new RuntimeException("SMS failed")).when(smsService).send(any());
assertThrows(RuntimeException.class, () -> orderService.notifyUser(user));

// Проверить через ArgumentCaptor:
ArgumentCaptor<String> msgCaptor = ArgumentCaptor.forClass(String.class);
verify(smsService).send(msgCaptor.capture());
assertTrue(msgCaptor.getValue().contains("cancelled"));
```

## 8. Связи с другими концепциями

- [[Чем Mock отличается от Spy (Mockito)]] — детальное сравнение с кодом и антипаттернами
- [[@Mock, @InjectMocks, @Spy — разница]] — как работает внедрение зависимостей в тестах
- [[Как проверить, что метод вызывался (verify)]] — verify, times, InOrder, ArgumentCaptor
- [[Spring Core IoC DI]] — `@InjectMocks` имитирует DI-контейнер в тестах

## 9. Ответ на собесе (2 минуты)

> "Mockito создаёт test doubles — заменители зависимостей — для изоляции тестируемого класса.
>
> **@Mock** — полностью поддельный объект, все методы — заглушки. **@Spy** — обёртка над реальным объектом, реальные методы работают, часть можно переопределить. **@InjectMocks** — создаёт реальный тестируемый объект и автоматически внедряет все @Mock и @Spy.
>
> **verify()** — проверяет поведение: был ли вызван метод, сколько раз, с какими аргументами. Особенно важен для void-методов, где нет возврата для assertа.
>
> **ArgumentCaptor** — захватывает аргументы, переданные в мок, для их проверки.
>
> Мой подход: `@Mock` для всех зависимостей, `@InjectMocks` для тестируемого класса. `@Spy` — только когда реально нужно реальное поведение части объекта."

## Шпаргалка

| Концепция | Суть | Пример |
|-----------|------|--------|
| **@Mock** | Полный заменитель | `when().thenReturn()` |
| **@Spy** | Реальный + контроль части | `doReturn().when()` |
| **@InjectMocks** | Автовнедрение моков | Тестируемый класс |
| **when().thenReturn()** | Настройка возврата | `when(repo.find(1L)).thenReturn(user)` |
| **doThrow().when()** | Настройка исключения void | `doThrow(ex).when(service).send()` |
| **verify()** | Был ли вызван метод | `verify(mock, times(1)).method()` |
| **verify(never())** | Не был вызван | При ошибке email не отправляется |
| **ArgumentCaptor** | Захват аргумента | `captor.getValue()` |
| **InOrder** | Порядок вызовов | Сначала оплата, потом уведомление |

**Связи:**
- [[Чем Mock отличается от Spy (Mockito)]]
- [[@Mock, @InjectMocks, @Spy — разница]]
- [[Как проверить, что метод вызывался (verify)]]
- [[Spring Core IoC DI]]
