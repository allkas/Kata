---
tags: [java, collections, core]
sources: [CORE 2 Вопросы технических собеседований.pdf]
---

# Устройство HashMap

## 1. Проблема — зачем это существует?

Массив даёт O(1) по индексу — но ключи не всегда числа. Список даёт поиск по любому ключу — но O(n). HashMap объединяет лучшее из обоих: превращает ключ в число через `hashCode()`, использует его как индекс в массиве и получает **O(1) в среднем** для любого типа ключа.

## 2. Аналогия

HashMap — это **библиотека с картотекой**. Каждая книга (value) хранится на полке (бакет). Полка определяется по классификатору (hashCode ключа). Когда ищешь книгу — сначала идёшь на нужную полку (по hashCode), потом сравниваешь по автору/названию (equals). Если на одной полке несколько книг с одинаковым классификатором (коллизия) — просматриваешь их по очереди.

## 3. Как работает

### Внутренняя структура:
```
HashMap<K, V>
└── Node<K,V>[] table   ← массив бакетов (по умолчанию 16)
    ├── bucket[0]: null
    ├── bucket[1]: Node(key1, val1) → Node(key2, val2)  ← цепочка при коллизии
    ├── ...
    └── bucket[15]: null
```

### Алгоритм `put(key, value)`:
```
1. hash = key.hashCode() → дополнительное перемешивание
2. index = hash & (capacity - 1)  // быстрее чем %
3. если бакет[index] пуст → вставить
4. если нет → пройти цепочку, сравнить через equals()
   - нашли равный ключ → перезаписать value
   - не нашли → добавить в цепочку
5. если size > capacity * loadFactor → rehash()
```

### Ключевые константы:
| Константа | Значение | Смысл |
|-----------|----------|-------|
| `DEFAULT_INITIAL_CAPACITY` | 16 | Начальный размер массива бакетов |
| `DEFAULT_LOAD_FACTOR` | 0.75 | При 75% заполнении — расширение |
| `TREEIFY_THRESHOLD` | 8 | Цепочка → красно-чёрное дерево |
| `UNTREEIFY_THRESHOLD` | 6 | Дерево → цепочка обратно |
| `MIN_TREEIFY_CAPACITY` | 64 | Минимальный размер таблицы для treeify |

### Коллизии и дерево (Java 8+):
```
Мало элементов в бакете → LinkedList   O(n) поиск
> 8 элементов И capacity >= 64 → Red-Black Tree   O(log n) поиск
< 6 элементов → обратно в LinkedList
```
**Почему два порога (8 и 6)?** Гистерезис — чтобы избежать постоянного переключения при добавлении/удалении граничного элемента.

### Rehashing:
- `newCapacity = oldCapacity * 2` (всегда степень двойки)
- Все элементы пересчитывают позицию — O(n)
- Амортизированно редко → O(1) для `put` в среднем

## 4. Глубже — нюансы и WeakHashMap

### Collection vs Collections — частый вопрос на собесе:
- `java.util.Collection` — **интерфейс**, корень иерархии коллекций (`List`, `Set` его реализуют). Методы: `add()`, `remove()`, `size()`, `isEmpty()`.
- `java.util.Collections` — **утилитный класс** (utility class), состоит из статических методов: `Collections.sort()`, `Collections.unmodifiableList()`, `Collections.synchronizedList()`, `Collections.shuffle()`.

```java
// Collection — интерфейс
Collection<String> c = new ArrayList<>();
c.add("a"); c.remove("a");

// Collections — класс
List<Integer> nums = Arrays.asList(3, 1, 2);
Collections.sort(nums);        // сортировка
Collections.reverse(nums);     // разворот
Collections.shuffle(nums);     // перемешать
List<Integer> immutable = Collections.unmodifiableList(nums); // обёртка read-only
```

### WeakHashMap — и типы ссылок в Java:

Java имеет 4 типа ссылок:
| Тип | Класс | GC собирает когда |
|-----|-------|-------------------|
| **Strong** | обычная переменная | Никогда (пока есть ссылка) |
| **Soft** | `SoftReference<T>` | Нехватка памяти |
| **Weak** | `WeakReference<T>` | При первой же GC-итерации |
| **Phantom** | `PhantomReference<T>` | После финализации (мониторинг) |

`WeakHashMap` использует `WeakReference` для **ключей**. Когда на ключ нет других сильных ссылок — запись автоматически удаляется GC.

```java
WeakHashMap<Object, String> map = new WeakHashMap<>();
Object key = new Object();
map.put(key, "value");
System.out.println(map.size()); // 1

key = null;            // единственная сильная ссылка потеряна
System.gc();           // подсказка GC
System.out.println(map.size()); // 0 — запись исчезла!
```

**Типичный use case:** кэш, где записи должны исчезать когда объект-ключ больше не используется (без ручного управления).

### Почему нельзя использовать byte[] как ключ в HashMap:

```java
byte[] key1 = {1, 2, 3};
byte[] key2 = {1, 2, 3};

Map<byte[], String> map = new HashMap<>();
map.put(key1, "value");
map.get(key2); // null — не найдёт!
```
Проблема: массивы не переопределяют `hashCode()` и `equals()`. Оба метода унаследованы от `Object` и работают по **ссылке**, а не по содержимому. Решение: использовать `List<Byte>` или строковое представление.

### Почему HashMap выродится в список при одинаковых hashCode():

```java
// Плохая хеш-функция — всё в один бакет
class BadKey {
    @Override public int hashCode() { return 1; } // всегда 1!
    @Override public boolean equals(Object o) { ... }
}
// put O(1) → O(n); get O(1) → O(n)
```
С Java 8: если len > 8 и capacity >= 64 → treeify → O(log n). Но всё равно хуже O(1).

## 5. Глубже — null и сравнение коллекций

### Null-ключи:
| Коллекция | null-ключ | null-значение |
|-----------|-----------|---------------|
| `HashMap` | ✅ один | ✅ |
| `HashSet` | ✅ один | — |
| `LinkedHashMap` | ✅ один | ✅ |
| `TreeMap` | ❌ NPE | ✅ |
| `TreeSet` | ❌ NPE | — |

`TreeMap` требует сравнения ключей через `Comparable` / `Comparator` — null сравнивать нельзя.

### HashMap vs TreeMap vs LinkedHashMap:
| | HashMap | LinkedHashMap | TreeMap |
|---|---|---|---|
| **Порядок** | Нет | Порядок вставки | Отсортированный |
| **Сложность** | O(1) | O(1) | O(log n) |
| **Null-ключ** | Один | Один | Нет |
| **Структура** | Хеш-таблица | Хеш-таблица + двусвязный список | Красно-чёрное дерево |
| **Когда** | Быстрый поиск | LRU-кэш, итерация по порядку | Диапазонные запросы, сортировка |

### HashSet vs LinkedHashSet vs TreeSet:
| | HashSet | LinkedHashSet | TreeSet |
|---|---|---|---|
| **Порядок** | Нет | Вставки | Отсортированный |
| **Сложность** | O(1) | O(1) | O(log n) |
| **Реализация** | HashMap | LinkedHashMap | TreeMap |

**TreeMap/TreeSet требуют `Comparable` или `Comparator`:**
```java
// Comparable (натуральный порядок)
TreeSet<String> set = new TreeSet<>(); // String реализует Comparable

// Comparator (кастомный порядок)
TreeMap<Person, String> map = new TreeMap<>(
    Comparator.comparing(Person::getName)
);
```

## 6. Связи с другими концепциями

- [[Контракт equals и hashCode]] — HashMap полностью зависит от корректной реализации обоих методов
- [[Generics]] — HashMap параметризован `<K, V>`
- [[ArrayList vs LinkedList]] — сравнение структур данных, fail-fast итераторы
- [[Garbage Collector JVM]] — WeakHashMap и жизненный цикл объектов связаны с GC

## 7. Ответ на собесе (2 минуты)

> "HashMap внутри — это массив бакетов (по умолчанию 16). При `put(key, value)` вычисляется `hashCode()` ключа, из него получается индекс бакета. Если бакет пустой — вставляем. Если нет (коллизия) — проходим по цепочке и сравниваем через `equals()`.
>
> **Load factor 0.75** — компромисс между памятью и скоростью. Когда заполнено 75% бакетов, таблица удваивается и все элементы перехешируются. Это O(n), но амортизированно редко.
>
> **Java 8 нюанс:** если в одном бакете накапливается более 8 элементов (и таблица >= 64 бакетов) — цепочка превращается в красно-чёрное дерево. Поиск ухудшается с O(n) до O(log n). Назад в цепочку — при уменьшении до 6.
>
> **Про null:** HashMap принимает один null-ключ (кладётся в бакет 0). TreeMap — нет, потому что для сортировки нужно сравнивать ключи, а null не сравнивается.
>
> **Сложность:** O(1) в среднем для put/get/remove. O(n) в теоретическом худшем случае (все коллизии), O(log n) в реальном худшем с Java 8."

## 8. Шпаргалка

| Концепция | Значение | Зачем |
|-----------|----------|-------|
| **Capacity** | 16 (default) | Размер массива бакетов |
| **Load factor** | 0.75 | Порог расширения |
| **TREEIFY** | 8 элементов | Список → дерево |
| **UNTREEIFY** | 6 элементов | Дерево → список |
| **Сложность** | O(1) avg / O(log n) worst | put/get/remove |
| **null-ключ** | HashMap ✅, TreeMap ❌ | TreeMap требует сравнения |
| **LinkedHashMap** | O(1) + порядок вставки | LRU-кэш |
| **TreeMap** | O(log n) + сортировка | Диапазонные запросы |

**Collection vs Collections:**
| | `Collection` | `Collections` |
|---|---|---|
| **Тип** | Интерфейс | Утилитный класс |
| **Назначение** | Корень иерархии коллекций | Статические методы для коллекций |
| **Примеры** | `List`, `Set` реализуют | `sort()`, `shuffle()`, `unmodifiableList()` |

**WeakHashMap:**
| Тип ссылки | Когда GC собирает |
|---|---|
| Strong | Никогда (пока есть ссылка) |
| Soft | При нехватке памяти |
| Weak (`WeakHashMap`) | При первой же GC-итерации |
| Phantom | После финализации |

**Связи:**
- [[Контракт equals и hashCode]]
- [[Generics]]
- [[ArrayList vs LinkedList]]
- [[Garbage Collector JVM]]

**Hexlet:**
- [[Java Maps]]
