---
tags: [java, collections, core]
sources: [CORE 2 Вопросы технических собеседований.pdf]
---

# ArrayList vs LinkedList

## 1. Проблема — зачем это существует?

Обычный массив имеет фиксированный размер. Нужна структура, которая растёт динамически и при этом предсказуемо работает для разных сценариев: случайный доступ, вставка в середину, работа как очередь. Одна реализация не подходит под всё — поэтому в Java Collections есть несколько.

## 2. Аналогия

**ArrayList** — пронумерованные места в кинотеатре. Хочешь место №42 — идёшь прямо к нему, O(1). Но если пришёл человек и нужно вставить его в середину — все остальные сдвигаются, O(n).

**LinkedList** — очередь людей, держащихся за руки. Чтобы найти 42-го — нужно считать с начала, O(n). Но вставить человека в начало/конец — просто добавляешь его в цепочку, O(1).

## 3. Как работает

### ArrayList — динамический массив:
```
[elem0][elem1][elem2][elem3][null][null][...]
 ^                           ^
 size=4                      capacity=16
```
- Элементы хранятся **подряд в памяти** — cache-friendly
- `get(index)` — прямое обращение по индексу, O(1)
- `add(index, e)` — сдвиг элементов вправо, O(n)
- `remove(index)` — сдвиг влево, O(n)

**Расширение capacity:**
```java
// При заполнении:
newCapacity = oldCapacity + (oldCapacity >> 1); // * 1.5
// Пример: 10 → 15 → 22 → 33 → ...
// Копирование всех элементов в новый массив: Arrays.copyOf()
```
- Начальная capacity = 10 (при `new ArrayList()`)
- Рекомендация: если размер известен — `new ArrayList<>(initialCapacity)` чтобы избежать копирований

### LinkedList — двусвязный список:
```
null ← [prev|A|next] ↔ [prev|B|next] ↔ [prev|C|next] → null
        head                                  tail
```
- Каждый узел: данные + ссылки на предыдущий и следующий
- Нет случайного доступа по индексу — O(n) traversal
- Вставка/удаление у краёв: O(1) — просто меняем ссылки
- Дополнительная память: ~40 байт на узел vs ~4-8 байт в ArrayList

## 4. Глубже — Big O и практика

### Сравнение сложности:
| Операция | ArrayList | LinkedList | Примечание |
|----------|-----------|------------|------------|
| `add(e)` — в конец | **O(1)** амортизированно | **O(1)** | ArrayList иногда O(n) при resize |
| `add(i, e)` — в середину | O(n) | O(n) | LL нужно дойти до позиции |
| `get(i)` | **O(1)** | O(n) | Главное преимущество AL |
| `remove(i)` | O(n) | O(n) | AL — сдвиг; LL — traversal |
| `remove(Object)` | O(n) | O(n) | Обе: нужно найти элемент |
| `addFirst/addLast` | O(n) / O(1) | **O(1)** | LL — как Deque |
| `contains` | O(n) | O(n) | Обе: линейный поиск |

### Когда что выбирать:
**ArrayList — когда:**
- Частый доступ по индексу (`get(i)`)
- Добавление в конец
- Итерация по всем элементам (cache-friendly)
- Нужна меньше память

**LinkedList — когда:**
- Частые вставки/удаления в **начале** списка
- Реализация очереди/двухсторонней очереди

**Важный нюанс:** в 99% случаев `ArrayList` лучше. LinkedList выигрывает только при **частых** операциях у краёв. Для очереди лучше использовать `ArrayDeque` — быстрее LinkedList из-за локальности памяти.

```java
// Вместо LinkedList как очереди:
Deque<String> queue = new ArrayDeque<>(); // быстрее и эффективнее
```

## 5. Итераторы: fail-fast и fail-safe

### Fail-fast — "быстрый" итератор:
```java
List<String> list = new ArrayList<>(List.of("a", "b", "c"));
for (String s : list) {
    list.remove(s); // ConcurrentModificationException!
}
// for-each использует Iterator → ArrayList обнаруживает modCount изменение
```
**Механика:** при изменении коллекции инкрементируется `modCount`. Iterator сохраняет значение при создании и сравнивает при каждом `next()`. Несоответствие → `ConcurrentModificationException`.

Как правильно удалять при итерации:
```java
// Способ 1: Iterator.remove()
Iterator<String> it = list.iterator();
while (it.hasNext()) {
    if (it.next().equals("b")) it.remove(); // OK — удаляет через тот же итератор
}

// Способ 2: removeIf (Java 8)
list.removeIf(s -> s.equals("b"));

// Способ 3: fail-safe коллекция
List<String> safe = new CopyOnWriteArrayList<>(list);
for (String s : safe) {
    safe.remove(s); // OK — итерирует по копии
}
```

### Fail-safe — "умный" итератор:
`CopyOnWriteArrayList` и `ConcurrentHashMap` — итератор работает на копии данных. Не бросает `ConcurrentModificationException`, но **может не видеть свежих изменений** (слабая консистентность).

### Iterator vs Enumeration:
| | Iterator | Enumeration |
|---|---|---|
| **Добавлен** | Java 1.2 | Java 1.0 |
| **Методы** | `hasNext()`, `next()`, `remove()` | `hasMoreElements()`, `nextElement()` |
| **Удаление** | Есть | Нет |
| **Поведение** | fail-fast | fail-safe |
| **Применение** | Все современные коллекции | Только legacy: Vector, Hashtable |

Предпочитать Iterator — Enumeration устарел.

### Comparable vs Comparator:
```java
// Comparable — ВНУТРИ класса, естественный порядок
class Person implements Comparable<Person> {
    String name; int age;
    @Override
    public int compareTo(Person other) {
        return Integer.compare(this.age, other.age); // сортировка по возрасту
    }
}
List<Person> people = ...;
Collections.sort(people); // использует compareTo

// Comparator — ВНЕ класса, кастомный порядок
Comparator<Person> byName = Comparator.comparing(Person::getName);
Comparator<Person> byAgeDesc = Comparator.comparingInt(Person::getAge).reversed();
people.sort(byName);
people.sort(byAgeDesc);
// Можно несколько сортировок для одного класса
```

`compareTo` / `compare`: отрицательное → элемент раньше, положительное → позже, 0 → равны.

## 6. Связи с другими концепциями

- [[Устройство HashMap]] — сравнение структур данных коллекций
- [[Generics]] — `ArrayList<T>` параметризован
- [[Stream API]] — `list.stream()` одинаково работает с обеими реализациями
- [[Многопоточность основы]] — `CopyOnWriteArrayList`, `ConcurrentHashMap` для fail-safe в многопоточности

## 7. Ответ на собесе (2 минуты)

> "ArrayList — это динамический массив: элементы хранятся подряд в памяти. Доступ по индексу — O(1), это главное преимущество. Вставка в середину — O(n) из-за сдвига. При заполнении расширяется в 1.5 раза через копирование — амортизированно это O(1) для `add` в конец.
>
> LinkedList — двусвязный список: каждый узел хранит данные и ссылки на соседей. Вставка/удаление у краёв — O(1). Но доступ по индексу — O(n), нужно идти с начала. Плюс каждый узел тратит ~40 байт на ссылки.
>
> **На практике:** я почти всегда выбираю ArrayList. Он cache-friendly, меньше памяти потребляет, и даже вставка в середину на реальных данных часто быстрее LinkedList из-за лучшей локальности памяти (CPU cache).
>
> LinkedList выгоден только для очень частых вставок у краёв — но даже тогда я предпочту `ArrayDeque`, который реализует Deque и быстрее LinkedList.
>
> **Частый вопрос на собесе:** зачем `add(index, e)` у LinkedList O(n), если вставка O(1)? Потому что сначала нужно дойти до нужной позиции — это O(n) traversal, и только потом O(1) вставка."

## 8. Шпаргалка

| | ArrayList | LinkedList |
|---|---|---|
| **Структура** | Массив | Двусвязный список |
| **get(i)** | **O(1)** | O(n) |
| **add(конец)** | O(1) амортизированно | O(1) |
| **add(середина)** | O(n) | O(n) |
| **Память** | ~4-8 байт/элемент | ~40 байт/узел |
| **Расширение** | × 1.5 при заполнении | Не нужно |
| **Лучше для** | Чтение по индексу, итерация | Вставка у краёв |
| **Альтернатива** | — | `ArrayDeque` для очереди |
| **fail-fast** | ✅ `ConcurrentModificationException` | ✅ |
| **fail-safe** | `CopyOnWriteArrayList` | `ConcurrentLinkedDeque` |

**Comparable vs Comparator:**
| | Comparable | Comparator |
|---|---|---|
| **Где** | Внутри класса | Вне класса |
| **Метод** | `compareTo()` | `compare()` |
| **Сортировок** | Одна (естественная) | Много |
| **Пример** | `String`, `Integer` | `Comparator.comparing(...)` |

**Связи:**
- [[Устройство HashMap]]
- [[Generics]]
- [[Stream API]]
- [[Многопоточность основы]]
