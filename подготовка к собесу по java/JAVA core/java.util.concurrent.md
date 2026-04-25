---
tags: [java, multithreading, concurrency, collections]
sources: [Kata 32 вопроса по многопоточности.pdf]
---

# java.util.concurrent

## 1. Проблема — зачем это существует?

`synchronized` и `wait/notify` — низкоуровневые примитивы: сложны в использовании, легко ошибиться, плохо масштабируются. `java.util.concurrent` (JUC, Java 5+) — высокоуровневые concurrency-утилиты: потокобезопасные коллекции, синхронизаторы, пулы потоков. Позволяют писать корректный конкурентный код, не изобретая велосипед.

## 2. Аналогия

`synchronized` — как вручную управлять светофором на перекрёстке. JUC — как готовые правила дорожного движения: светофоры (ReentrantLock), разметка (ConcurrentHashMap), перекрёстки с круговым движением (Semaphore), ожидание всех машин до отъезда (CountDownLatch).

## 3. Как работает

### Конкурентные коллекции

#### ConcurrentHashMap
```java
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
map.put("key", 1);    // потокобезопасно
map.get("key");
map.computeIfAbsent("key", k -> expensiveCompute(k)); // атомарно
```

**Java 7:** сегментная блокировка (16 сегментов по умолчанию) — разные сегменты не блокируют друг друга.  
**Java 8:** блокировка на уровне бакета (CAS + synchronized на корзину) — ещё меньше конкуренции.

| | `HashMap` | `Collections.synchronizedMap` | `ConcurrentHashMap` |
|---|---|---|---|
| **Потокобезопасность** | Нет | Да (весь map) | Да (на уровне бакета) |
| **Параллельные чтения** | Нет | Нет (блок на весь map) | Да (без блокировки) |
| **null-ключ** | ✅ | ✅ | ❌ |
| **Производительность** | Высокая | Низкая | Высокая |

**Итерация fail-safe:** итератор `ConcurrentHashMap` не бросает `ConcurrentModificationException`, но может не видеть свежих изменений (слабая консистентность).

#### CopyOnWriteArrayList
```java
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
list.add("item"); // создаёт новую копию массива при каждом изменении
for (String s : list) {
    list.remove(s); // OK — итерируем по snapshot, не по текущему массиву
}
```
**Стратегия:** при каждом `add/remove/set` создаётся новая копия массива. Читатели работают со старым snapshot без блокировки.

**Когда использовать:** много читателей, редкие записи (подписчики событий, конфиги). Дорого при частых записях — O(n) на каждый `add`.

#### BlockingQueue
```java
BlockingQueue<String> queue = new LinkedBlockingQueue<>(100); // ёмкость 100

// Производитель — блокируется если очередь полна
queue.put("task");        // блокирует
queue.offer("task", 1, TimeUnit.SECONDS); // с таймаутом

// Потребитель — блокируется если очередь пуста
String task = queue.take(); // блокирует
String task2 = queue.poll(1, TimeUnit.SECONDS); // с таймаутом
```

| Реализация | Особенности |
|-----------|-------------|
| `LinkedBlockingQueue` | Опционально ограниченная, linked nodes |
| `ArrayBlockingQueue` | Ограниченная (обязательно), array-based, fair опция |
| `PriorityBlockingQueue` | Неограниченная, порядок по Comparator |
| `SynchronousQueue` | Нет буфера — каждый put блокирует до take |

---

### Locks — java.util.concurrent.locks

#### ReentrantLock
```java
ReentrantLock lock = new ReentrantLock();
ReentrantLock fairLock = new ReentrantLock(true); // справедливая (FIFO) — медленнее

lock.lock();
try {
    // критическая секция
} finally {
    lock.unlock(); // ВСЕГДА в finally!
}

// Попытка захвата с таймаутом (нет у synchronized!)
if (lock.tryLock(100, TimeUnit.MILLISECONDS)) {
    try { ... }
    finally { lock.unlock(); }
}
```

**ReentrantLock vs synchronized:**
| | `synchronized` | `ReentrantLock` |
|---|---|---|
| **Попытка с таймаутом** | Нет | `tryLock(timeout)` |
| **Прерываемое ожидание** | Нет | `lockInterruptibly()` |
| **Справедливость** | Нет | `new ReentrantLock(true)` |
| **Несколько Condition** | Нет (один wait-set) | `lock.newCondition()` |
| **Сложность** | Низкая | Выше (нужен finally) |

#### ReadWriteLock
```java
ReadWriteLock rwLock = new ReentrantReadWriteLock();
Lock readLock  = rwLock.readLock();
Lock writeLock = rwLock.writeLock();

// Много читателей одновременно
readLock.lock();
try { return data; }
finally { readLock.unlock(); }

// Только один писатель, все читатели блокируются
writeLock.lock();
try { data = newData; }
finally { writeLock.unlock(); }
```
**Когда использовать:** много читателей, редкие записи (кэш, конфигурация). Чтения не блокируют друг друга.

#### Condition
```java
ReentrantLock lock = new ReentrantLock();
Condition notFull  = lock.newCondition();
Condition notEmpty = lock.newCondition();

// Producer:
lock.lock();
try {
    while (isFull()) notFull.await();   // ждать "не полно"
    add(item);
    notEmpty.signal();                  // сигнал "не пусто"
} finally { lock.unlock(); }

// Consumer:
lock.lock();
try {
    while (isEmpty()) notEmpty.await(); // ждать "не пусто"
    T item = remove();
    notFull.signal();                   // сигнал "не полно"
} finally { lock.unlock(); }
```
`Condition` — замена `wait/notify` с разделением на отдельные очереди ожидания. Точечные сигналы без лишних пробуждений.

---

### Синхронизаторы

#### CountDownLatch
```java
int workerCount = 5;
CountDownLatch latch = new CountDownLatch(workerCount);

for (int i = 0; i < workerCount; i++) {
    executor.submit(() -> {
        doWork();
        latch.countDown(); // уменьшить счётчик на 1
    });
}
latch.await(); // заблокировать до 0
System.out.println("Все завершили!");
```
**Одноразовый** — сброс невозможен. Применение: ждать старта N сервисов, ждать завершения N задач.

#### CyclicBarrier
```java
int parties = 3;
CyclicBarrier barrier = new CyclicBarrier(parties, () -> {
    System.out.println("Все добрались до барьера!"); // runnable при достижении
});

// Каждый поток:
barrier.await(); // ждать пока все N потоков не достигнут барьера
```
**Многоразовый** — после срабатывания сбрасывается. Применение: фазовые алгоритмы, симуляции (все потоки синхронизируются между шагами).

#### CountDownLatch vs CyclicBarrier:
| | `CountDownLatch` | `CyclicBarrier` |
|---|---|---|
| **Использование** | Одноразово | Многоразово (cyclic) |
| **Кто считает** | Любой поток (countDown) | Только ожидающие потоки (await) |
| **Ждёт** | Главный поток ждёт других | Все потоки ждут друг друга |
| **Barrieraction** | Нет | Да (runnable при достижении) |

#### Phaser
```java
Phaser phaser = new Phaser(3); // 3 участника

// Поток завершил фазу:
phaser.arriveAndAwaitAdvance(); // ждать всех остальных

// Динамическое добавление/удаление участников:
phaser.register();    // добавить участника
phaser.arriveAndDeregister(); // завершить и уйти
```
**Гибкий аналог CyclicBarrier** с поддержкой динамического числа участников и вложенных фаз.

#### Exchanger
```java
Exchanger<String> exchanger = new Exchanger<>();

// Поток A:
String fromB = exchanger.exchange("данные от A");

// Поток B:
String fromA = exchanger.exchange("данные от B");
// Оба получают данные друг друга
```
Синхронная точка встречи двух потоков для обмена данными. Применение: конвейерная обработка, тесты.

---

## 4. Глубже — что важно знать

### Когда что использовать:
| Задача | Инструмент |
|--------|-----------|
| Потокобезопасный счётчик | `AtomicInteger` / `LongAdder` |
| Потокобезопасный Map | `ConcurrentHashMap` |
| Потокобезопасный List (много читателей) | `CopyOnWriteArrayList` |
| Producer-Consumer очередь | `BlockingQueue` |
| Ждать завершения N задач | `CountDownLatch` |
| Синхронизировать N потоков по фазам | `CyclicBarrier` / `Phaser` |
| Ограничить параллелизм (N потоков) | `Semaphore` |
| Взаимоисключение с tryLock / fairness | `ReentrantLock` |
| Много читателей, редкие записи | `ReadWriteLock` |
| Раздельные условия ожидания | `Condition` |

### ConcurrentHashMap — важные детали:
```java
// computeIfAbsent — атомарная операция:
map.computeIfAbsent("key", k -> new ArrayList<>()).add(item); // безопасно

// merge — атомарное обновление:
map.merge("key", 1, Integer::sum); // если нет — put(1), если есть — sum

// getOrDefault:
int count = map.getOrDefault("key", 0);
```

---

## 5. Связи с другими концепциями

- [[Многопоточность основы]] — volatile, synchronized, Atomic — фундамент для JUC
- [[CompletableFuture и пулы потоков]] — ExecutorService, ForkJoinPool
- [[ArrayList vs LinkedList]] — CopyOnWriteArrayList как fail-safe альтернатива
- [[Устройство HashMap]] — ConcurrentHashMap vs HashMap

## 6. Ответ на собесе (2 минуты)

> "java.util.concurrent — набор готовых утилит для конкурентного кода поверх примитивов synchronized/wait.
>
> **ConcurrentHashMap** — потокобезопасный HashMap с блокировкой на уровне бакета (Java 8). Параллельные чтения без блокировки, null-ключи не поддерживаются. `computeIfAbsent`, `merge` — атомарные составные операции.
>
> **BlockingQueue** — реализует Producer-Consumer: `put` блокирует если полно, `take` блокирует если пусто. Удобнее wait/notify.
>
> **CountDownLatch** — одноразовый счётчик. Один поток ждёт `await()`, другие декрементируют `countDown()`. Типично: дождаться инициализации всех компонентов.
>
> **CyclicBarrier** — многоразовый барьер: N потоков ждут друг друга, затем все продолжают синхронно. Подходит для фазовых алгоритмов.
>
> **ReentrantLock** — замена synchronized с дополнениями: `tryLock(timeout)`, `lockInterruptibly()`, fair-режим, несколько `Condition`.
>
> **ReadWriteLock** — оптимизация для read-heavy сценариев: много читателей одновременно, писатель — эксклюзивно."

## Шпаргалка

| Утилита | Применение | Ключевое |
|---------|-----------|----------|
| `ConcurrentHashMap` | Потокобезопасный Map | Блокировка на бакет, no null keys |
| `CopyOnWriteArrayList` | Много читателей | Копия при записи, fail-safe итерация |
| `BlockingQueue` | Producer-Consumer | put/take блокируют |
| `ReentrantLock` | Взаимоисключение | tryLock, fair, Condition |
| `ReadWriteLock` | Read-heavy | Параллельные чтения |
| `Semaphore(N)` | Ограничение параллелизма | N разрешений одновременно |
| `CountDownLatch` | Ждать N событий | Одноразовый, countDown + await |
| `CyclicBarrier` | Синхронизация N потоков по фазам | Многоразовый, все ждут друг друга |
| `Exchanger` | Обмен данными двух потоков | Синхронная точка встречи |
| `Phaser` | Динамическое число участников | Гибкий CyclicBarrier |

**Связи:**
- [[Многопоточность основы]]
- [[CompletableFuture и пулы потоков]]
- [[ArrayList vs LinkedList]]
- [[Устройство HashMap]]
