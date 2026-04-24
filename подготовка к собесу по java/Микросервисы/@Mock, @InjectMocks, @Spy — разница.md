---
tags: [testing, mockito, java]
sources: [Тестирование Вопросы технических собеседований.pdf]
---

# @Mock, @InjectMocks, @Spy — разница

## 1. Проблема — зачем это существует?

Создавать моки программно (`Mockito.mock(...)`, `new OrderService(mockRepo, mockEmail)`) — verbose и ломается при добавлении новых зависимостей. Три аннотации автоматизируют рутину: `@Mock` создаёт поддельные зависимости, `@Spy` — реальные с возможностью подмены, `@InjectMocks` собирает тестируемый объект и автоматически внедряет все моки и спаи.

## 2. Аналогия

Сборка двигателя на тестовом стенде:

**@Mock** — создать **муляж детали**: вместо реального топливного насоса ставим симулятор. Он делает ровно то, что мы запрограммируем: «при запросе — вернуть давление 2 атм».

**@Spy** — взять **реальную деталь**, но с возможностью переопределить одно поведение: насос работает как обычно, но в этом тесте пусть «нештатно» не даёт давление.

**@InjectMocks** — **автосборщик**: ты создал муляжи и реальные детали, а он сам монтирует их в двигатель. Не нужно вручную писать `engine.setFuelPump(mockPump)`.

## 3. Как работает

### Стандартный паттерн теста

```java
@ExtendWith(MockitoExtension.class)   // активирует аннотации Mockito
class OrderServiceTest {

    @Mock
    private UserRepository userRepository;   // зависимость 1 — полный мок

    @Mock
    private EmailService emailService;       // зависимость 2 — полный мок

    @InjectMocks
    private OrderService orderService;       // тестируемый класс — получит оба мока

    @Test
    void createOrder_shouldSendEmail() {
        when(userRepository.findById(1L)).thenReturn(Optional.of(new User("Alice")));

        orderService.createOrder(new Order(1L));

        verify(emailService).sendConfirmation(anyString());
    }
}
```

---

### @Mock — поддельная зависимость

```java
@Mock
private UserRepository userRepository;
// эквивалентно: UserRepository userRepository = Mockito.mock(UserRepository.class);
```

- Все методы — заглушки (null / 0 / false / пустые коллекции по умолчанию)
- Настраивается через `when().thenReturn()`
- Используется для **зависимостей** тестируемого класса

---

### @Spy — частично реальный объект

```java
@Spy
private AuditLogger auditLogger = new AuditLogger();   // требует инициализации!
```

- Реальный объект — методы работают по-настоящему если не переопределены
- Настраивается через `doReturn().when()` (не `when().thenReturn()` — опасно!)
- Используется когда нужно реальное поведение с подменой части методов

---

### @InjectMocks — тестируемый класс

```java
@InjectMocks
private OrderService orderService;
// Mockito создаст: new OrderService(userRepository, emailService)
// автоматически найдёт подходящие @Mock и @Spy по типу и имени
```

**Порядок внедрения (приоритет):**
1. **Конструктор** — предпочтительный способ (если есть подходящий конструктор)
2. **Сеттеры** — если нет подходящего конструктора
3. **Поля** — field injection как запасной вариант

**Алгоритм поиска зависимостей:**
- По типу — если один мок нужного типа в тесте
- По имени — если несколько моков одного типа, Mockito ищет совпадение по имени поля

---

### Когда нужен @BeforeEach

```java
// Вариант без @ExtendWith — ручная инициализация
class OrderServiceTest {
    @Mock UserRepository userRepository;
    @InjectMocks OrderService orderService;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);   // инициализирует аннотации
    }
}

// Вариант с расширением (рекомендуется для JUnit 5)
@ExtendWith(MockitoExtension.class)
class OrderServiceTest { ... }

// Вариант для Spring (интеграционный тест)
@SpringBootTest
class OrderServiceTest { ... }
```

## 4. Глубже — что важно знать

**Сравнительная таблица:**

| Аннотация | Что создаёт | Реальное поведение | Внедряет | Когда |
|-----------|-------------|:---:|:---:|---|
| `@Mock` | Поддельный объект | Нет | Нет | Зависимости (репозитории, клиенты) |
| `@Spy` | Обёртка над реальным | Да | Нет | Частичный контроль |
| `@InjectMocks` | Реальный тестируемый объект | Да (его код) | Да (авто) | Тестируемый класс |

**Ловушки @InjectMocks:**

```java
// Не работает если зависимость создаётся внутри метода через new
public class OrderService {
    public void process() {
        EmailService email = new EmailService();   // ← @InjectMocks не достанет это
        email.send();
    }
}
// Решение: зависимости только через конструктор или поле

// Работает только с одним экземпляром класса — нельзя иметь два @InjectMocks
```

**`@Spy` без инициализации:**
```java
@Spy
private UserService userService;        // ❌ NullPointerException — нет реального объекта

@Spy
private UserService userService = new UserService();   // ✅
```

## 5. Связи с другими концепциями

- [[Чем Mock отличается от Spy (Mockito)]] — детали Mock vs Spy, критичный нюанс синтаксиса
- [[Как проверить, что метод вызывался (verify)]] — verify() проверяет взаимодействие после @InjectMocks
- [[Unit-тесты Mockito]] — общий обзор и пирамида тестирования
- [[Spring Core IoC DI]] — @InjectMocks имитирует IoC-контейнер Spring в тестах

## 6. Ответ на собесе (2 минуты)

Три аннотации — три роли в тесте.

`@Mock` создаёт поддельную зависимость: все методы — заглушки, поведение настраиваю через `when().thenReturn()`. Использую для всего, что тестируемый класс вызывает извне: репозиторий, email-сервис, HTTP-клиент.

`@Spy` создаёт обёртку над реальным объектом. Методы работают по-настоящему, если не переопределены. Синтаксис другой — `doReturn().when(spy).method()`. Если использовать `when(spy.method())` — реальный метод вызовется до перехвата. Применяю редко — обычно для легаси-кода или частичного контроля.

`@InjectMocks` создаёт реальный тестируемый класс и автоматически внедряет в него все `@Mock` и `@Spy`. Это замена ручному `new OrderService(mockRepo, mockEmail)`. Mockito ищет подходящие зависимости сначала через конструктор, потом сеттеры, потом поля.

Стандартный паттерн: `@Mock` на все зависимости, `@InjectMocks` на тестируемый класс, `@ExtendWith(MockitoExtension.class)` на тестовый класс.

## Шпаргалка

| Аннотация | Аналогия | Ключевой факт |
|-----------|----------|---------------|
| `@Mock` | Муляж детали | Заглушка; `when().thenReturn()` |
| `@Spy` | Реальная деталь с правкой | Требует `new`; `doReturn().when()` |
| `@InjectMocks` | Автосборщик | Создаёт тестируемый класс + внедряет все моки |

```java
// Шаблон теста
@ExtendWith(MockitoExtension.class)
class MyServiceTest {
    @Mock  DependencyA depA;         // зависимость 1
    @Mock  DependencyB depB;         // зависимость 2
    @InjectMocks MyService service;  // тестируемый класс
}
```

**Связи:**
- [[Чем Mock отличается от Spy (Mockito)]]
- [[Как проверить, что метод вызывался (verify)]]
- [[Unit-тесты Mockito]]
