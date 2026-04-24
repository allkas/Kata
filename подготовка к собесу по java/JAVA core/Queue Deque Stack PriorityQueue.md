---
tags: [java, collections, data-structures, queue, stack]
sources: [Kata Алгоритмы (1.pdf)]
---

# Queue, Deque, Stack, PriorityQueue

## 1. Проблема — зачем это существует?

Разные задачи требуют разного порядка обработки элементов: обработка задач по очереди (FIFO), откат операций (LIFO), обработка по приоритету (priority). Специализированные структуры данных кодируют эти семантики и обеспечивают эффективные операции добавления/извлечения.

## 2. Аналогия

- **Queue (FIFO)** — очередь в магазине: первый пришёл — первый обслужен
- **Stack (LIFO)** — стопка тарелок: последняя положенная снимается первой
- **Deque** — двусторонняя очередь: можно добавлять/брать с обоих концов (как двойные двери)
- **PriorityQueue** — VIP-очередь: сначала обслуживают самых важных, независимо от времени прихода

## 3. Как работает

### Queue — интерфейс очереди (FIFO)

```java
// Queue — интерфейс, реализации: LinkedList, ArrayDeque, PriorityQueue
Queue<String> queue = new LinkedList<>();

// Два варианта методов: бросающие исключение vs returning null/false
queue.add("first");       // исключение если full
queue.offer("second");    // return false если full (безопаснее)

queue.remove();           // исключение если пусто
queue.poll();             // return null если пусто (безопаснее)

queue.element();          // peek + исключение если пусто
queue.peek();             // просмотр без удаления, null если пусто
```

| Операция | Бросает exception | Возвращает null/false |
|----------|-------------------|-----------------------|
| Добавить | `add(e)` | `offer(e)` |
| Удалить head | `remove()` | `poll()` |
| Просмотр head | `element()` | `peek()` |

**Использование:** обработка задач в порядке поступления, BFS (поиск в ширину).

### Deque — двусторонняя очередь

`Deque` (Double Ended Queue) расширяет `Queue`. Реализации: `ArrayDeque` (рекомендуется), `LinkedList`.

```java
Deque<Integer> deque = new ArrayDeque<>();

// Добавление
deque.addFirst(1);    // в начало (как Stack.push)
deque.addLast(2);     // в конец (как Queue.offer)
deque.offerFirst(0);  // в начало (не бросает)
deque.offerLast(3);   // в конец (не бросает)

// Удаление
deque.removeFirst();  // из начала (как Queue.remove)
deque.removeLast();   // из конца (как Stack.pop)
deque.pollFirst();    // из начала, null если пусто
deque.pollLast();     // из конца, null если пусто

// Просмотр
deque.peekFirst();    // первый элемент, null если пусто
deque.peekLast();     // последний элемент, null если пусто
```

**Использование:** sliding window задачи, palindrome проверка, реализация и Stack и Queue.

### Stack — LIFO

`Stack` — устаревший класс (наследует `Vector`). **Рекомендуется** использовать `Deque` вместо него.

```java
// ПЛОХО — устаревший Stack:
Stack<Integer> stack = new Stack<>();
stack.push(1);
stack.pop();
stack.peek();

// ХОРОШО — ArrayDeque как Stack:
Deque<Integer> stack = new ArrayDeque<>();
stack.push(1);   // = addFirst
stack.pop();     // = removeFirst
stack.peek();    // = peekFirst
```

**Использование:** откат операций (undo), обход графа в глубину (DFS), проверка скобок.

```java
// Классическая задача: проверить скобки
public boolean isValid(String s) {
    Deque<Character> stack = new ArrayDeque<>();
    for (char c : s.toCharArray()) {
        if (c == '(' || c == '[' || c == '{') {
            stack.push(c);
        } else {
            if (stack.isEmpty()) return false;
            char top = stack.pop();
            if (c == ')' && top != '(') return false;
            if (c == ']' && top != '[') return false;
            if (c == '}' && top != '{') return false;
        }
    }
    return stack.isEmpty();
}
```

### PriorityQueue — очередь с приоритетом

Основана на **бинарной куче** (min-heap по умолчанию). Извлекает элементы в порядке приоритета (наименьший первым).

```java
// Min-heap (по умолчанию): минимальный элемент на верху
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
minHeap.offer(5);
minHeap.offer(1);
minHeap.offer(3);
minHeap.peek();  // 1 (минимум)
minHeap.poll();  // 1, затем 3, затем 5

// Max-heap: максимальный элемент на верху
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
maxHeap.offer(5);
maxHeap.offer(1);
maxHeap.offer(3);
maxHeap.peek();  // 5 (максимум)

// С кастомным компаратором (по длине строки):
PriorityQueue<String> byLength = new PriorityQueue<>(
    Comparator.comparingInt(String::length)
);

// Для объектов:
PriorityQueue<Task> tasks = new PriorityQueue<>(
    Comparator.comparingInt(t -> t.priority)
);
```

**Сложность операций:**
- `offer()` / `add()` — O(log n)
- `poll()` / `remove()` — O(log n)
- `peek()` — O(1)
- Поиск произвольного элемента — O(n) (не отсортирована внутри!)

**Использование:** алгоритм Дейкстры, Top-K задачи, планировщики задач.

```java
// Top-K: найти k наибольших элементов
public int[] topK(int[] nums, int k) {
    PriorityQueue<Integer> minHeap = new PriorityQueue<>();
    for (int num : nums) {
        minHeap.offer(num);
        if (minHeap.size() > k) minHeap.poll(); // удаляем минимум
    }
    // в minHeap остались k наибольших
    return minHeap.stream().mapToInt(Integer::intValue).toArray();
}
```

### EnumSet

Специализированная реализация `Set` для `enum`-значений. Внутри — битовый вектор: каждая позиция бита — один enum-константа.

```java
enum Day { MON, TUE, WED, THU, FRI, SAT, SUN }

EnumSet<Day> workdays = EnumSet.of(Day.MON, Day.TUE, Day.WED, Day.THU, Day.FRI);
EnumSet<Day> weekend  = EnumSet.complementOf(workdays);  // SAT, SUN

EnumSet<Day> all     = EnumSet.allOf(Day.class);
EnumSet<Day> empty   = EnumSet.noneOf(Day.class);
EnumSet<Day> range   = EnumSet.range(Day.MON, Day.FRI);  // MON..FRI
```

**Свойства EnumSet:**
- Все операции — O(1) (побитовые операции)
- Элементы хранятся в порядке объявления enum
- Не потокобезопасен — нужна синхронизация
- Не допускает null → `NullPointerException`
- **Всегда предпочитать** над `HashSet<MyEnum>` для enum-значений

---

## 4. Глубже — что важно знать

**`ArrayDeque` vs `LinkedList`:**

| | ArrayDeque | LinkedList |
|---|---|---|
| Память | Массив (меньше overhead) | Узлы с указателями (больше overhead) |
| Cache | Лучше (contiguous memory) | Хуже |
| Реализует | Deque | Deque, List, Queue |
| Рекомендуется | Как Stack, Queue, Deque | Когда нужен List + Queue |

**Heap vs Stack (в контексте JVM):** не путать с алгоритмическими структурами данных! В JVM:
- **Heap** — область памяти для объектов, управляется GC
- **Stack** — область памяти для фреймов вызова методов, локальных переменных

**`PriorityQueue` не отсортирована:** внутри — heap, не отсортированный массив. `iterator()` не гарантирует порядок. Только `poll()` даёт элементы в порядке приоритета.

**Очередь и `equals/hashCode`:** `Queue` и `Deque` не переопределяют `equals` и `hashCode` — используют идентичность ссылок (наследуют от `Object`).

---

## 5. Связи с другими концепциями

- [[Бинарное дерево и красно-чёрное дерево]] — PriorityQueue реализована на binary heap; TreeMap/TreeSet — на Red-Black Tree
- [[Устройство HashMap]] — HashMap vs TreeMap vs LinkedHashMap — разные Map-реализации
- [[Алгоритмы на собесе]] — Stack нужен для DFS, Queue — для BFS
- [[Виды сортировок]] — Heapsort использует heap (PriorityQueue-принцип)
- [[Stack vs Heap память]] — Stack/Heap JVM ≠ Stack/Heap алгоритмические структуры

## 6. Ответ на собесе (2 минуты)

> "Queue — интерфейс, FIFO. Основные реализации: `LinkedList` и `ArrayDeque`. Методы: `offer/poll/peek` (безопасные, возвращают null) vs `add/remove/element` (бросают исключение).
>
> **Deque** — двусторонняя очередь, расширяет Queue. `ArrayDeque` — рекомендуемая реализация и для Queue, и для Stack.
>
> **Stack** — устаревший класс, рекомендую `Deque`. LIFO: `push/pop/peek`.
>
> **PriorityQueue** — min-heap по умолчанию. Самый маленький элемент на верху. `offer/poll` — O(log n), `peek` — O(1). Для max-heap: `Comparator.reverseOrder()`. Использую для Top-K задач и алгоритма Дейкстры.
>
> **EnumSet** — специализированный Set для enum, побитовые операции O(1). Всегда предпочитаю его над HashSet для enum-значений."

## Шпаргалка

| Структура | Порядок | Реализация | Особенность |
|-----------|---------|-----------|-------------|
| Queue | FIFO | LinkedList, ArrayDeque | offer/poll безопасны |
| Stack | LIFO | ArrayDeque (рекомендуется) | push/pop/peek |
| Deque | FIFO + LIFO | ArrayDeque | Оба конца |
| PriorityQueue | По приоритету | Binary heap | Min-heap по умолчанию |
| EnumSet | Порядок enum | Битовый вектор | O(1) все операции |

| Метод | Throws exception | Returns null/false |
|-------|------------------|--------------------|
| Добавить | `add(e)` | `offer(e)` |
| Удалить | `remove()` | `poll()` |
| Просмотр | `element()` | `peek()` |

**Связи:**
- [[Бинарное дерево и красно-чёрное дерево]]
- [[Устройство HashMap]]
- [[Алгоритмы на собесе]]
- [[Stack vs Heap память]]
