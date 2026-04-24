---
tags: [testing, mockito, java]
sources: [Тестирование Вопросы технических собеседований.pdf]
---

# Как проверить, что метод вызывался (verify)

## 1. Проблема — зачем это существует?

Некоторые методы ничего не возвращают (void) или их результат — это побочный эффект: запись в БД, отправка письма, публикация события в Kafka. Классический `assertEquals()` здесь не поможет — нечего сравнивать. `verify()` — инструмент **поведенческого тестирования**: проверяет, что метод был вызван, с какими аргументами и сколько раз.

## 2. Аналогия

Ты тестируешь секретаря: дал задание «отправь письмо клиенту». Как проверить, что он это сделал, не дожидаясь ответа клиента?

**Проверка состояния** — проверить, что письмо пришло. Но это медленно и не всегда возможно (асинхронность).

**Проверка вызова (verify)** — поставить камеру над секретарём. Смотришь запись: взял телефон, набрал номер, произнёс «Здравствуйте». Ты не проверяешь, что клиент услышал — проверяешь, что секретарь сделал свою работу.

## 3. Как работает

### Базовый синтаксис

```java
// Проверить, что метод был вызван ровно 1 раз (дефолт)
verify(emailService).send("user@example.com");

// Проверить с конкретными аргументами
verify(emailService).send("user@example.com", "Welcome!");
```

---

### Счётчики вызовов

```java
verify(service, times(1)).save(user);      // ровно 1 раз (дефолт)
verify(service, times(3)).notify();        // ровно 3 раза
verify(service, never()).delete(any());    // ни разу
verify(service, atLeast(1)).process();     // хотя бы 1 раз
verify(service, atMost(2)).log();          // не более 2 раз
verify(service, atLeastOnce()).check();    // эквивалент atLeast(1)
```

---

### Матчеры аргументов

```java
// any() — любой аргумент
verify(logger).log(anyString());
verify(repo).save(any(User.class));

// eq() — точное совпадение (нужен когда смешиваются any и конкретные значения)
verify(service).process(eq("admin"), anyInt());

// ArgumentCaptor — захват аргумента для детальной проверки
ArgumentCaptor<Email> captor = ArgumentCaptor.forClass(Email.class);
verify(emailService).send(captor.capture());
Email sent = captor.getValue();
assertEquals("alice@mail.com", sent.getRecipient());
assertEquals("Welcome!", sent.getSubject());
```

---

### Проверка порядка вызовов (InOrder)

```java
// Гарантирует, что payment был до inventory
InOrder inOrder = inOrder(paymentService, inventoryService);
inOrder.verify(paymentService).charge(any());
inOrder.verify(inventoryService).reserve(any());

// Практическое применение — тест саги
InOrder sagaOrder = inOrder(orderService, paymentService, notificationService);
sagaOrder.verify(orderService).create(any());
sagaOrder.verify(paymentService).charge(any());
sagaOrder.verify(notificationService).sendConfirmation(anyString());
```

---

### Типичные сценарии

```java
// 1. Метод void — единственный способ проверить вызов
orderService.createOrder(order);
verify(notificationService).sendOrderConfirmation(order.getId());

// 2. Метод НЕ должен вызваться при невалидных данных
assertThrows(ValidationException.class, () -> service.register(invalidUser));
verify(emailService, never()).send(any());

// 3.批-операция — проверить количество вызовов
service.processAll(users);   // users.size() == 10
verify(repo, times(10)).save(any(User.class));

// 4. Kafka — проверить, что событие опубликовано
orderService.placeOrder(order);
verify(kafkaTemplate).send(eq("orders"), any(OrderEvent.class));
```

## 4. Глубже — что важно знать

**State verification vs Behavior verification:**

| Тип | Что проверяет | Инструмент | Когда |
|-----|---------------|-----------|-------|
| State verification | Состояние объекта после вызова | `assertEquals`, `assertThat` | Метод возвращает значение или меняет поле |
| Behavior verification | Взаимодействие с зависимостями | `verify()` | void-метод, внешние вызовы, async |

В unit-тестах чаще behavior (verify) — проверяем изолированный класс и его взаимодействие с замоканными зависимостями. В интеграционных тестах чаще state — данные реально попали в БД.

**Не злоупотреблять verify:**
- Проверять только то, что критично для логики теста
- Не писать `verify` на каждый вызов — тест станет хрупким и сломается при любом рефакторинге
- Если можно проверить состояние — предпочесть state verification

**verifyNoInteractions и verifyNoMoreInteractions:**
```java
// После всех verify — убедиться, что больше ничего не вызывалось
verifyNoInteractions(emailService);         // ни одного вызова
verifyNoMoreInteractions(userRepository);   // всё уже проверено через verify
```

## 5. Связи с другими концепциями

- [[Чем Mock отличается от Spy (Mockito)]] — verify работает с обоими; Spy осторожно — реальные методы
- [[@Mock, @InjectMocks, @Spy — разница]] — шаблон теста с verify внутри
- [[Как тестировать void методы в Mockito]] — verify — основной инструмент для void
- [[Распределённые транзакции саги]] — InOrder идеален для проверки последовательности шагов саги

## 6. Ответ на собесе (2 минуты)

`verify()` — это инструмент поведенческого тестирования в Mockito. Когда метод ничего не возвращает или его результат — это побочный эффект (отправка письма, запись в БД, событие в Kafka), `assertEquals()` не поможет. `verify()` проверяет, что конкретный метод был вызван с нужными аргументами.

Базовый синтаксис: `verify(mock).method(args)` — по умолчанию проверяет ровно один вызов. Дополнительные модификаторы: `times(N)`, `never()`, `atLeast(N)`, `atMost(N)`.

Для захвата сложных аргументов — `ArgumentCaptor`: перехватываю переданный объект и проверяю его поля. Для проверки порядка — `InOrder`: создаю `inOrder(a, b)` и верифицирую в нужном порядке. Это особенно полезно при тестировании саг — проверяю, что шаги выполняются в правильной последовательности.

Важный принцип: не злоупотреблять. Если можно проверить состояние — проверяй состояние. `verify` — для взаимодействий, которые нельзя иначе проверить.

## Шпаргалка

| Сценарий | Синтаксис |
|----------|-----------|
| Вызван 1 раз | `verify(mock).method()` |
| Вызван N раз | `verify(mock, times(N)).method()` |
| Не вызван | `verify(mock, never()).method()` |
| Хотя бы 1 раз | `verify(mock, atLeastOnce()).method()` |
| Проверить аргумент | `ArgumentCaptor` → `captor.getValue()` |
| Проверить порядок | `InOrder` → `inOrder.verify(a).m1(); inOrder.verify(b).m2()` |
| Ничего не вызвано | `verifyNoInteractions(mock)` |

**Связи:**
- [[Чем Mock отличается от Spy (Mockito)]]
- [[@Mock, @InjectMocks, @Spy — разница]]
- [[Как тестировать void методы в Mockito]]
