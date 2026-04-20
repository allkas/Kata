---
tags: [java, java8, java11, features]
sources: [Прочие_Реже встречающиеся вопросы технических собеседований.pdf]
---

# Отличия Java 8 и Java 11

## 1. Проблема — зачем это существует?

Java 8 (2014) — самая долгоживущая LTS-версия, многие проекты всё ещё на ней. Java 11 (2018) — следующая LTS, с которой большинство мигрировало. На собесе этот вопрос проверяет: знаешь ли ты ключевые нововведения и не застрял ли в 2014 году. Понимание ключевых отличий важно при работе на Java 11+ проектах.

## 2. Аналогия

Java 8 → Java 11 как Android 8 → Android 11: не революция, а накопление улучшений: быстрее, удобнее, убраны legacy API, новый HTTP клиент вместо устаревшего.

## 3. Как работает

### Java 9–11: ключевые добавления

**Java 9 — Modules (Project Jigsaw)**
```java
// module-info.java — описание модуля
module com.example.myapp {
    requires java.net.http;           // зависимость от другого модуля
    requires spring.context;
    exports com.example.myapp.api;    // что открываем наружу
}
```
Разбивает монолитный JDK на модули. На практике для большинства приложений `--add-opens` нужны при миграции.

---

**Java 10 — Local-Variable Type Inference (`var`)**
```java
// Java 8 — явный тип
List<Map<String, Integer>> list = new ArrayList<>();
Map<String, Integer> map = new HashMap<>();

// Java 10+ — var
var list = new ArrayList<Map<String, Integer>>();
var map = new HashMap<String, Integer>();
var users = userRepository.findAll();   // List<User>

// var только для локальных переменных (не поля, не параметры)
// тип выводится компилятором, не runtime
```

---

**Java 11 — HTTP Client (стандартный)**
```java
// Java 8 — HttpURLConnection (громоздкий)
HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
// ... боль

// Java 11 — новый HTTP Client
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .connectTimeout(Duration.ofSeconds(10))
    .build();

// Синхронный запрос
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/users"))
    .header("Authorization", "Bearer " + token)
    .GET()
    .build();

HttpResponse<String> response = client.send(request, 
    HttpResponse.BodyHandlers.ofString());
System.out.println(response.statusCode());   // 200
System.out.println(response.body());

// Асинхронный запрос
client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
    .thenApply(HttpResponse::body)
    .thenAccept(System.out::println);
```

---

**Java 11 — String API новые методы**
```java
// isBlank() — проверяет пустоту с учётом whitespace
"  ".isBlank();    // true (в Java 8 нет — нужен Apache Commons)
"".isBlank();      // true

// strip() — trim() с поддержкой Unicode whitespace
"  hello  ".strip();         // "hello"
"  hello  ".stripLeading();  // "hello  "
"  hello  ".stripTrailing(); // "  hello"

// lines() — поток строк из многострочного текста
"line1\nline2\nline3".lines()
    .forEach(System.out::println);

// repeat() — повторение строки
"ab".repeat(3);  // "ababab"
```

---

**Java 11 — удалены устаревшие модули**
- Удалены: `java.xml.ws` (JAX-WS), `java.xml.bind` (JAXB), `java.corba` — нужно добавлять как зависимости
- `javax.*` → частично переехало в `jakarta.*` (в рамках Jakarta EE)

---

### Сводная таблица

| Версия | Ключевое | Важность |
|--------|----------|---------|
| Java 8 | Lambda, Stream API, Optional, java.time | Фундаментальные изменения |
| Java 9 | Modules, JShell, Collection factory methods | Архитектурное изменение JDK |
| Java 10 | `var` | Удобство |
| Java 11 | HTTP Client, String methods, удалены JAXB/JAX-WS | Практические улучшения |

---

### Collection Factory Methods (Java 9)
```java
// Java 8 — verbose
List<String> list = new ArrayList<>(Arrays.asList("a", "b", "c"));
Map<String, Integer> map = new HashMap<>();
map.put("a", 1); map.put("b", 2);

// Java 9+ — краткий синтаксис (immutable!)
List<String> list = List.of("a", "b", "c");
Set<String> set = Set.of("x", "y", "z");
Map<String, Integer> map = Map.of("a", 1, "b", 2);
// ⚠️ List.of() — immutable, UnsupportedOperationException при add()
```

## 4. Java 8 — Date/Time API (java.time)

До Java 8 — `java.util.Date` и `Calendar`: изменяемые (mutable), не thread-safe, неудобный API.

### Основные классы java.time:
```java
// LocalDate — только дата (без времени и зон)
LocalDate today = LocalDate.now();
LocalDate birthday = LocalDate.of(1990, Month.MARCH, 15);
LocalDate nextWeek = today.plusWeeks(1);
boolean isBefore = birthday.isBefore(today); // true

// LocalTime — только время
LocalTime now = LocalTime.now();
LocalTime noon = LocalTime.of(12, 0, 0);

// LocalDateTime — дата + время (без зоны)
LocalDateTime dt = LocalDateTime.now();
LocalDateTime event = LocalDateTime.of(2025, 6, 1, 14, 30);
String formatted = event.format(DateTimeFormatter.ofPattern("dd.MM.yyyy HH:mm"));

// ZonedDateTime — дата + время + зона
ZonedDateTime moscow = ZonedDateTime.now(ZoneId.of("Europe/Moscow"));
ZonedDateTime utc = moscow.withZoneSameInstant(ZoneId.of("UTC"));

// Period — разница в датах (годы, месяцы, дни)
Period age = Period.between(birthday, today);
System.out.println(age.getYears()); // возраст в годах

// Duration — разница во времени (часы, минуты, секунды)
Duration d = Duration.between(LocalTime.of(9, 0), LocalTime.of(17, 30));
System.out.println(d.toHours()); // 8
```

**Ключевые свойства java.time:**
- **Immutable** — все классы неизменяемы, thread-safe
- `plus/minus` возвращают новый объект
- Интегрируется с Hibernate, Spring через `@CreationTimestamp`, конвертеры

**Глубже — что важно знать

**Java 8 vs 11 — лицензия Oracle JDK:** с Java 11 Oracle JDK требует коммерческой лицензии для production. В production используют OpenJDK (Temurin/Eclipse Adoptium, Amazon Corretto, Azul Zulu) — бесплатные дистрибутивы.

**LTS-версии:** Java 8, 11, 17, 21 — long-term support. Большинство enterprise-проектов переходят с 8 → 11 → 17. Java 21 (2023) — актуальная LTS.

**Java 17 добавляет важное (хотя вопрос про 8 vs 11):**
- Sealed classes
- Records
- Pattern matching `instanceof`
- Text blocks (preview в Java 13, stable в 15)

## 5. Связи с другими концепциями

- [[Stream API]] — Stream API появился в Java 8, в Java 9 добавлены `takeWhile()`, `dropWhile()`, `ofNullable()`
- [[CompletableFuture и пулы потоков]] — HTTP Client Java 11 использует CompletableFuture для async
- [[Иммутабельность String]] — `strip()` vs `trim()` связано с Unicode

## 6. Ответ на собесе (2 минуты)

Ключевые изменения между Java 8 и Java 11 — три блока.

**Java 9: `var`** для вывода типа локальных переменных — меньше повторений, компилятор выводит тип. И **Collection.of()** — краткое создание immutable коллекций.

**Java 9: Модули** — разбивка JDK на модули (Project Jigsaw). Для большинства приложений практически незаметно, но при миграции могут потребоваться `--add-opens` флаги.

**Java 11: HTTP Client** — встроенный, поддерживает HTTP/2, sync и async API через CompletableFuture. Заменяет громоздкий `HttpURLConnection`.

**Java 11: String API** — `isBlank()`, `strip()`, `lines()`, `repeat()`. И **удалены** JAXB, JAX-WS из JDK — нужно добавлять как Maven-зависимости.

Практически важно: с Java 11 Oracle JDK платный для production, нужен OpenJDK-дистрибутив (Temurin).

## Шпаргалка

| Фича | Версия | Пример |
|------|--------|--------|
| `var` | Java 10 | `var list = new ArrayList<>()` |
| HTTP Client | Java 11 | `HttpClient.newBuilder().build()` |
| `isBlank()` | Java 11 | `"  ".isBlank() == true` |
| `strip()` | Java 11 | Unicode-aware trim |
| `lines()` | Java 11 | `"a\nb".lines()` → Stream |
| `repeat()` | Java 11 | `"ab".repeat(3)` → "ababab" |
| `List.of()` | Java 9 | Immutable factory method |
| Modules | Java 9 | `module-info.java` |
| `LocalDate/LocalDateTime` | Java 8 | `LocalDate.now()`, immutable |
| `ZonedDateTime` | Java 8 | Дата+время+зона |
| `DateTimeFormatter` | Java 8 | `ofPattern("dd.MM.yyyy")` |

**Связи:**
- [[Stream API]]
- [[CompletableFuture и пулы потоков]]
