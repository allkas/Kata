---
tags: [java, multithreading, async, concurrency]
sources: []
---

# CompletableFuture и пулы потоков

## 1. Проблема — зачем это существует?

`Future` (Java 5) позволял запустить задачу асинхронно, но не позволял составлять цепочки вычислений, комбинировать несколько асинхронных результатов или обрабатывать ошибки без блокировки. `future.get()` блокирует поток — всё преимущество асинхронности теряется. `CompletableFuture` (Java 8) решает это: можно выстраивать пайплайн из шагов, комбинировать результаты нескольких задач и обрабатывать ошибки декларативно.

## 2. Аналогия

`Future` — как заказ в ресторане с официантом, который стоит у стола и ждёт, пока на кухне приготовят блюдо. Бесполезно занят.

`CompletableFuture` — как СМС-уведомление: "Когда будет готово — позвони". Официант идёт обслуживать другие столики, а когда блюдо готово — автоматически запускается следующий шаг.

## 3. Как работает

### Создание

```java
// Запустить задачу асинхронно (в ForkJoinPool.commonPool() по умолчанию)
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    return fetchFromDatabase(); // выполняется в отдельном потоке
});

// Запустить без возвращаемого значения
CompletableFuture<Void> voidFuture = CompletableFuture.runAsync(() -> {
    sendEmail(); // fire-and-forget
});

// Указать свой Executor (рекомендуется в продакшене)
ExecutorService executor = Executors.newFixedThreadPool(10);
CompletableFuture<String> future = CompletableFuture.supplyAsync(
    () -> fetchFromDatabase(), executor
);
```

---

### Цепочки — thenApply / thenCompose / thenAccept

```java
// thenApply — трансформация результата (как map в Stream)
CompletableFuture<Integer> lengthFuture = CompletableFuture
    .supplyAsync(() -> "Hello World")    // → CF<String>
    .thenApply(String::toUpperCase)      // → CF<String>
    .thenApply(String::length);          // → CF<Integer>

// thenCompose — цепочка из двух async операций (как flatMap)
// Используй когда следующий шаг тоже возвращает CompletableFuture
CompletableFuture<Order> orderFuture = CompletableFuture
    .supplyAsync(() -> findUser(userId))             // → CF<User>
    .thenCompose(user -> findOrder(user.getId()));   // → CF<Order> (не CF<CF<Order>>!)

// thenAccept — терминальный шаг (результат не нужен)
CompletableFuture
    .supplyAsync(() -> fetchData())
    .thenAccept(data -> saveToCache(data));  // → CF<Void>
```

**thenApply vs thenCompose:**

| | thenApply | thenCompose |
|---|---|---|
| **Функция возвращает** | Обычное значение T | CompletableFuture\<T\> |
| **Аналог в Stream** | `map` | `flatMap` |
| **Когда использовать** | Синхронная трансформация | Следующий шаг тоже асинхронный |

---

### Комбинирование нескольких Future

```java
// thenCombine — объединить результаты двух независимых Future
CompletableFuture<User> userFuture     = fetchUserAsync(userId);
CompletableFuture<Account> accountFuture = fetchAccountAsync(userId);

CompletableFuture<String> result = userFuture.thenCombine(
    accountFuture,
    (user, account) -> user.getName() + " | balance: " + account.getBalance()
);

// allOf — ждать завершения ВСЕХ (без результатов)
CompletableFuture<Void> all = CompletableFuture.allOf(future1, future2, future3);
all.join(); // блокирует до завершения всех

// anyOf — вернуть результат ПЕРВОГО завершённого
CompletableFuture<Object> first = CompletableFuture.anyOf(future1, future2, future3);
```

---

### Обработка ошибок

```java
// exceptionally — обработать исключение, вернуть дефолт
CompletableFuture<String> safe = CompletableFuture
    .supplyAsync(() -> fetchFromRemoteApi())
    .exceptionally(ex -> {
        log.error("API failed: {}", ex.getMessage());
        return "default value"; // продолжаем с дефолтом
    });

// handle — обработать и успех, и ошибку в одном месте
CompletableFuture<String> handled = CompletableFuture
    .supplyAsync(() -> fetchFromRemoteApi())
    .handle((result, ex) -> {
        if (ex != null) return "fallback";
        return result.toUpperCase();
    });

// whenComplete — side-effect (логирование) без изменения результата
CompletableFuture
    .supplyAsync(() -> process())
    .whenComplete((result, ex) -> {
        if (ex != null) metrics.incrementErrors();
        else metrics.incrementSuccess();
    });
```

---

### ExecutorService — пулы потоков

```java
// Фиксированный пул — подходит для CPU-интенсивных задач
ExecutorService fixedPool = Executors.newFixedThreadPool(
    Runtime.getRuntime().availableProcessors() // CPU-bound: N потоков = N ядер
);

// Кэширующий пул — для I/O-интенсивных задач (создаёт потоки по мере нужды)
ExecutorService cachedPool = Executors.newCachedThreadPool(); // осторожно: может создать тысячи потоков!

// Scheduled пул — для задач по расписанию
ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);
scheduler.scheduleAtFixedRate(() -> checkHealth(), 0, 30, TimeUnit.SECONDS);

// Правильное завершение пула
fixedPool.shutdown();                     // перестать принимать новые задачи
fixedPool.awaitTermination(30, TimeUnit.SECONDS); // ждать завершения текущих
```

**Важно:** всегда завершать `ExecutorService`, иначе JVM не остановится (потоки из пула — не daemon-потоки).

---

### ForkJoinPool — для рекурсивного параллелизма

```java
// ForkJoinPool.commonPool() используется CompletableFuture по умолчанию
// Размер = Runtime.getRuntime().availableProcessors() - 1

// Собственная задача через RecursiveTask
class SumTask extends RecursiveTask<Long> {
    private final int[] arr;
    private final int lo, hi;
    static final int THRESHOLD = 1000;

    @Override
    protected Long compute() {
        if (hi - lo <= THRESHOLD) {
            // базовый случай — считаем напрямую
            long sum = 0;
            for (int i = lo; i < hi; i++) sum += arr[i];
            return sum;
        }
        int mid = (lo + hi) / 2;
        SumTask left  = new SumTask(arr, lo, mid);
        SumTask right = new SumTask(arr, mid, hi);
        left.fork();                        // запустить left в другом потоке
        return right.compute() + left.join(); // right — в текущем, затем ждём left
    }
}
```

---

## 4. Глубже — что важно знать

**Future vs CompletableFuture:**

| | Future | CompletableFuture |
|---|---|---|
| **Получить результат** | `get()` — блокирует | `thenApply()` — не блокирует |
| **Цепочки** | Нет | Да (`thenApply`, `thenCompose`) |
| **Комбинирование** | Нет | `allOf`, `anyOf`, `thenCombine` |
| **Обработка ошибок** | `try/catch` вокруг `get()` | `exceptionally`, `handle` |
| **Завершение вручную** | Нет | `complete(value)`, `completeExceptionally()` |

**Нотация с потоками — что выполняется где:**

```java
CompletableFuture
    .supplyAsync(() -> step1(), executor1)    // executor1
    .thenApplyAsync(r -> step2(r), executor2) // executor2
    .thenApply(r -> step3(r))                 // тот же поток, что завершил step2
    .thenAcceptAsync(r -> step4(r));          // ForkJoinPool.commonPool()
```

- `thenApply` — в потоке, завершившем предыдущий шаг (или вызывающем потоке, если уже завершён)
- `thenApplyAsync` — в отдельном потоке (commonPool или указанный Executor)

**Подбор размера пула:**

| Тип задач | Формула | Пример |
|-----------|---------|--------|
| CPU-bound | N ядер (или N+1) | Математические вычисления |
| I/O-bound | N ядер × (1 + время_ожидания/время_CPU) | HTTP-запросы, DB |

Для I/O задач можно использовать 10–100 потоков на ядро, т.к. большинство времени поток ждёт.

**Типичные ошибки:**
- Использовать `future.get()` вместо `thenApply` — блокирует поток, убивает асинхронность
- Не передавать свой `Executor` — `commonPool` делится на всё приложение, можно заблокировать другие задачи
- Не завершать `ExecutorService.shutdown()` — утечка потоков
- Использовать `newCachedThreadPool()` под нагрузкой — создаст тысячи потоков, OOM

## 5. Связи с другими концепциями

- [[Многопоточность основы]] — volatile, synchronized, AtomicReference — фундамент для понимания CompletableFuture
- [[Spring Core IoC DI]] — `@Async` в Spring использует CompletableFuture + ThreadPoolTaskExecutor
- [[Circuit Breaker]] — Resilience4j декорирует CompletableFuture для отказоустойчивости
- [[Highload проблемы]] — правильный размер пула потоков — ключ к масштабированию под нагрузку

## 6. Ответ на собесе (2 минуты)

`CompletableFuture` — это монада для асинхронных вычислений, появившаяся в Java 8. Главное отличие от `Future`: не нужно блокировать поток на `get()` — вместо этого описываем цепочку шагов, и каждый шаг запускается автоматически, как только предыдущий завершится.

Для трансформации результата — `thenApply` (как `map` у Stream). Если следующий шаг сам возвращает `CompletableFuture` — `thenCompose` (как `flatMap`). Для параллельного выполнения независимых задач — `allOf` чтобы дождаться всех, или `anyOf` для первого результата.

Обработка ошибок: `exceptionally` — поймать исключение и вернуть дефолт. `handle` — обработать и успех, и ошибку в одном блоке.

Важно всегда передавать свой `Executor` в продакшене: дефолтный `ForkJoinPool.commonPool` разделяется на всё приложение и имеет размер N-1 ядер — легко заблокировать другие задачи.

## Шпаргалка

| Метод | Аналог | Когда использовать |
|-------|--------|-------------------|
| `supplyAsync` | — | Запустить задачу, вернуть значение |
| `runAsync` | — | Запустить задачу, без возврата |
| `thenApply` | Stream.map | Синхронная трансформация |
| `thenCompose` | Stream.flatMap | Следующий шаг тоже async |
| `thenCombine` | zip | Два независимых результата |
| `allOf` | join all | Ждать завершения всех |
| `anyOf` | first | Первый завершившийся |
| `exceptionally` | catch | Дефолт при ошибке |
| `handle` | catch + map | Ошибка или успех в одном |

**Связи:**
- [[Многопоточность основы]]
- [[Spring Core IoC DI]]
- [[Circuit Breaker]]
- [[Highload проблемы]]
