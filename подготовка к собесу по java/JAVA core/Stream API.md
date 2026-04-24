---
tags: [java, streams, functional]
sources: [CORE 2 Вопросы технических собеседований.pdf]
---

# Stream API

## 1. Проблема — зачем это существует?

Обработка коллекций через `for`-циклы многословна и императивна: описываешь **как** делать, а не **что** получить. С ростом условий и трансформаций — вложенные циклы, промежуточные списки, трудночитаемый код. Stream API (Java 8) приносит декларативный стиль: описываешь цепочку трансформаций, Java выполняет её оптимально.

```java
// Императивно:
List<String> result = new ArrayList<>();
for (User user : users) {
    if (user.getAge() >= 18) {
        result.add(user.getName().toUpperCase());
    }
}

// Декларативно:
List<String> result = users.stream()
    .filter(u -> u.getAge() >= 18)
    .map(u -> u.getName().toUpperCase())
    .collect(Collectors.toList());
```

## 2. Аналогия

Stream — это **конвейер на заводе**. Сырьё (коллекция) подаётся на вход. Каждая станция (промежуточная операция) обрабатывает и передаёт дальше. Конечная станция (терминальная операция) производит готовый продукт. Конвейер **ленивый**: станции молчат, пока не запущен финальный этап.

## 3. Как работает

### Промежуточные vs терминальные операции:
| Тип | Возвращает | Выполняется | Примеры |
|-----|-----------|-------------|---------|
| **Промежуточная** | `Stream<T>` | Лениво (при terminal) | `filter`, `map`, `flatMap`, `sorted`, `distinct`, `limit` |
| **Терминальная** | Результат / void | Сразу | `collect`, `forEach`, `count`, `findFirst`, `anyMatch`, `reduce` |

```java
list.stream()
    .filter(x -> x > 0)     // промежуточная — ещё не выполнена
    .map(x -> x * 2)         // промежуточная — ещё не выполнена
    .collect(toList());       // терминальная — ЗАПУСКАЕТ весь конвейер
```

### map vs flatMap — ключевое отличие:

**`map`** — трансформирует каждый элемент **1 → 1**:
```java
// String → Integer
List<Integer> lengths = List.of("hello", "world").stream()
    .map(String::length)     // "hello" → 5, "world" → 5
    .collect(toList());      // [5, 5]

// List<String> → List<String[]>
List<String[]> arrays = List.of("a b", "c d").stream()
    .map(s -> s.split(" "))  // "a b" → ["a","b"]
    .collect(toList());      // [["a","b"], ["c","d"]]
```

**`flatMap`** — трансформирует каждый элемент **1 → Stream**, затем **разворачивает** в один поток:
```java
// List<String> → Stream<String> (развёрнутый)
List<String> words = List.of("a b", "c d").stream()
    .flatMap(s -> Arrays.stream(s.split(" "))) // "a b" → Stream("a","b")
    .collect(toList());      // ["a", "b", "c", "d"]

// List<List<Integer>> → List<Integer>
List<Integer> flat = List.of(List.of(1,2), List.of(3,4)).stream()
    .flatMap(Collection::stream)
    .collect(toList());      // [1, 2, 3, 4]
```

**Правило:** если `map` возвращает `Stream` — нужен `flatMap`, чтобы не получить `Stream<Stream<T>>`.

### Функциональные интерфейсы:
| Интерфейс | Сигнатура | Применение |
|-----------|-----------|------------|
| `Predicate<T>` | `T → boolean` | `filter()` |
| `Function<T, R>` | `T → R` | `map()` |
| `Consumer<T>` | `T → void` | `forEach()` |
| `Supplier<T>` | `() → T` | `orElseGet()` |
| `BiFunction<T, U, R>` | `T, U → R` | `reduce()` |
| `UnaryOperator<T>` | `T → T` | `map()` с тем же типом |

```java
// Лямбда — это реализация функционального интерфейса
Predicate<String> isLong = s -> s.length() > 5;
Function<String, Integer> toLen = String::length; // method reference
```

## 4. Глубже — Optional и повторное использование

### Optional — как правильно использовать:
```java
// Создание:
Optional<String> opt1 = Optional.of("value");      // NPE если null
Optional<String> opt2 = Optional.ofNullable(value); // null → empty
Optional<String> opt3 = Optional.empty();

// Использование:
opt.orElse("default")           // значение или default
opt.orElseGet(() -> compute())  // lazy — вычислять только если пусто
opt.orElseThrow(NotFoundException::new) // или бросить исключение
opt.map(String::toUpperCase)    // трансформировать если есть
opt.filter(s -> s.length() > 3) // фильтровать
opt.ifPresent(System.out::println) // action если есть

// Антипаттерны:
opt.get()            // ❌ NoSuchElementException если пусто — бессмысленно
if (opt.isPresent()) { opt.get(); } // ❌ то же что null-check, теряется смысл
void method(Optional<String> param) // ❌ Optional не для параметров методов
class User { Optional<String> name; } // ❌ не для полей класса
```

**Optional — для возвращаемых значений**, когда отсутствие значения — нормальный сценарий:
```java
Optional<User> findById(Long id) {
    return userRepository.findById(id); // Spring Data возвращает Optional
}
```

### Повторное использование Stream:
```java
Stream<String> stream = list.stream();
stream.count();  // терминальная — stream закрыт
stream.count();  // IllegalStateException: stream has already been operated upon or closed
```
Stream — одноразовый. Создавать из источника заново: `list.stream()`.

### Параллельные стримы:
```java
list.parallelStream()
    .filter(...)
    .collect(toList()); // ForkJoinPool.commonPool()
```
**Когда использовать:** только CPU-intensive операции над большими коллекциями. Не для IO, не для shared mutable state.

**Почему осторожно:** все параллельные стримы JVM используют **один общий** `ForkJoinPool.commonPool()`. Долгие операции (DB-запросы, HTTP) заблокируют пул для всего приложения. Для долгих операций — отдельный `ExecutorService`.

```java
// Можно явно переключаться:
stream.parallel()    // сделать параллельным
stream.sequential()  // обратно последовательным

// Порядок в parallelStream не гарантирован!
// forEachOrdered() — сохраняет порядок, но снижает параллелизм
```

### IntStream, LongStream, DoubleStream — примитивные стримы:
```java
// Зачем нужны: обычный Stream<T> — только объекты → autoboxing/unboxing
// IntStream работает с int напрямую, без накладных расходов

IntStream.range(1, 5)            // 1, 2, 3, 4 (не включая 5)
IntStream.rangeClosed(1, 5)      // 1, 2, 3, 4, 5 (включая 5)
IntStream.of(1, 3, 5)

// Специальные терминальные методы только у числовых стримов:
IntStream.of(1, 2, 3, 4, 5)
    .sum()    // 15
    .average() // OptionalDouble(3.0)
    .min()     // OptionalInt(1)
    .max()     // OptionalInt(5)
    .count()   // 5

// Преобразование:
Stream<String> stream = ...;
stream.mapToInt(String::length)    // Stream<String> → IntStream
      .boxed()                      // IntStream → Stream<Integer>

// IntStream → обычный стрим:
IntStream.range(0, 5).mapToObj(i -> "item_" + i).collect(toList());
```
Аналогичны `LongStream` и `DoubleStream`. Для `byte`, `short`, `float` специализированных стримов нет.

### Collectors — основные методы:
```java
// Сбор в коллекцию
.collect(Collectors.toList())
.collect(Collectors.toSet())
.collect(Collectors.toUnmodifiableList())  // Java 10

// Группировка
.collect(Collectors.groupingBy(User::getDepartment))
// → Map<String, List<User>>

.collect(Collectors.groupingBy(User::getDepartment, Collectors.counting()))
// → Map<String, Long>

// Разбивка по условию
.collect(Collectors.partitioningBy(u -> u.getAge() >= 18))
// → Map<Boolean, List<User>>

// Слияние строк
.collect(Collectors.joining(", "))
.collect(Collectors.joining(", ", "[", "]")) // "[a, b, c]"

// Статистика
.collect(Collectors.summarizingInt(User::getAge))
// → IntSummaryStatistics: count, sum, min, max, average
```

## 5. Связи с другими концепциями

- [[Generics]] — `Stream<T>`, `Function<T,R>` — всё на дженериках
- [[ArrayList vs LinkedList]] — `.stream()` работает на любом `Collection`
- [[Многопоточность основы]] — `parallelStream()` использует ForkJoinPool

## 6. Ответ на собесе (2 минуты)

> "Stream API — декларативный способ обрабатывать коллекции. Вместо цикла описываешь цепочку трансформаций: `filter → map → collect`. Stream ленивый — промежуточные операции не выполняются до вызова терминальной.
>
> **map vs flatMap** — самый частый вопрос. `map` трансформирует каждый элемент 1:1. Если `map` возвращает Stream — получишь `Stream<Stream<T>>`, что почти всегда не то что нужно. `flatMap` трансформирует 1 → Stream и **разворачивает** результат в один поток. Пример: список предложений — `flatMap(s -> Arrays.stream(s.split(" ")))` — даст все слова плоским списком.
>
> **Функциональные интерфейсы:** лямбды — это реализации интерфейсов с одним методом. `Predicate` для `filter`, `Function` для `map`, `Consumer` для `forEach`, `Supplier` для ленивого создания.
>
> **Optional:** использую для возвращаемых значений там, где отсутствие — нормально. Главное правило: не вызывать `get()` напрямую — только `orElse`, `orElseGet`, `orElseThrow`, `map`. Не использую Optional как параметр метода или поле класса.
>
> **Stream одноразовый:** после вызова терминальной операции стрим закрыт, повторный вызов — `IllegalStateException`."

## Шпаргалка

| Концепция | Тип | Пример |
|-----------|-----|--------|
| `filter` | Промежуточная | `filter(x -> x > 0)` |
| `map` | Промежуточная, 1→1 | `map(String::length)` |
| `flatMap` | Промежуточная, 1→Stream | `flatMap(s -> Arrays.stream(...))` |
| `collect` | Терминальная | `collect(Collectors.toList())` |
| `count/findFirst` | Терминальная | Запускает весь конвейер |
| **Lazy** | Промежуточные не выполняются | До вызова terminal |
| **One-time** | Повторное использование | `IllegalStateException` |
| **Optional** | Для return value | `orElse`, `map`, `orElseThrow` |
| **IntStream** | Без autoboxing | `range()`, `sum()`, `average()` |
| **parallelStream** | ForkJoinPool.commonPool() | Только CPU-intensive, не IO |
| **groupingBy** | Collector | `Map<K, List<T>>` |
| **joining** | Collector | `"[a, b, c]"` |

**Связи:**
- [[Generics]]
- [[ArrayList vs LinkedList]]
- [[Многопоточность основы]]
