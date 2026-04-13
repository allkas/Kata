---
tags: [java, generics, core]
sources: [CORE 2 Вопросы технических собеседований.pdf]
---

# Generics

## 1. Проблема — зачем это существует?

До Java 5 коллекции хранили `Object`. Это значит: кладёшь строку, достаёшь `Object`, явно кастуешь, надеешься, что там строка. Компилятор не помогал — ошибки вылетали в runtime с `ClassCastException`. Generics переносят проверку типов на **этап компиляции**: положил `String` — только `String` и достанешь.

```java
// До generics
List list = new ArrayList();
list.add("hello");
list.add(42);           // компилятор молчит
String s = (String) list.get(1); // ClassCastException в runtime

// С generics
List<String> list = new ArrayList<>();
list.add("hello");
list.add(42);           // ОШИБКА КОМПИЛЯЦИИ — сразу видно
String s = list.get(0); // без каста
```

## 2. Аналогия

Generics — это **маркированные ящики** на складе. Без маркировки: кладёшь что угодно, достаёшь что угодно — надейся, что угадал. С маркировкой «только яблоки»: кладовщик (компилятор) не примет апельсин. На складе (в runtime) маркировка стирается — остаётся просто ящик.

## 3. Как работает

### Синтаксис:
```java
// Параметризованный класс
class Box<T> {
    private T value;
    Box(T value) { this.value = value; }
    T get() { return value; }
}
Box<String> box = new Box<>("hello");

// Параметризованный метод
<T> List<T> repeat(T item, int times) {
    List<T> list = new ArrayList<>();
    for (int i = 0; i < times; i++) list.add(item);
    return list;
}
```

### Wildcards:
```java
List<?>           // неизвестный тип (unbounded)
List<? extends T> // T или любой подтип T (upper bounded)
List<? super T>   // T или любой надтип T (lower bounded)
```

### PECS — Producer Extends, Consumer Super:
**Мнемоника:** если коллекция **производит** (ты читаешь из неё) — `extends`. Если **потребляет** (ты пишешь в неё) — `super`.

```java
// Producer (читаем): ? extends
void printAll(List<? extends Number> list) {
    for (Number n : list) System.out.println(n); // OK — читаем Number
    // list.add(1); — НЕЛЬЗЯ, компилятор не знает точный тип
}

// Consumer (пишем): ? super
void addNumbers(List<? super Integer> list) {
    list.add(1); list.add(2); // OK — пишем Integer
    // Integer n = list.get(0); — НЕЛЬЗЯ, получим только Object
}

// Классический пример copy: src читаем, dest пишем
static <T> void copy(List<? extends T> src, List<? super T> dest) {
    for (T item : src) dest.add(item);
}
```

## 4. Глубже — стирание типов (type erasure)

**Информация о `T` стирается в bytecode.** После компиляции `List<String>` и `List<Integer>` — один и тот же тип `List`.

```java
List<String> strings = new ArrayList<>();
List<Integer> ints = new ArrayList<>();
strings.getClass() == ints.getClass(); // true — оба просто ArrayList

// Что НЕЛЬЗЯ делать из-за type erasure:
new T();                    // нельзя — тип неизвестен в runtime
new T[10];                  // нельзя — массив дженерика
if (obj instanceof List<String>) // нельзя — только instanceof List<?>
```

**Как компилятор компенсирует стирание:**
- Вставляет явные касты там, где нужно
- Генерирует **bridge methods** при наследовании

**Как получить тип в runtime (обходной путь):**
```java
class TypedBox<T> {
    private final Class<T> type;
    TypedBox(Class<T> type) { this.type = type; }
    T cast(Object obj) { return type.cast(obj); }
}
TypedBox<String> box = new TypedBox<>(String.class);
```

## 5. Связи с другими концепциями

- [[Устройство HashMap]] — HashMap параметризован `<K, V>`
- [[ArrayList vs LinkedList]] — все коллекции используют generics
- [[Stream API]] — Stream полностью построен на generics: `Stream<T>`, `Function<T,R>`

## 6. Ответ на собесе (2 минуты)

> "Generics решают проблему типобезопасности коллекций. До Java 5 коллекция хранила `Object` — ошибки типов ловились только в runtime при касте. Generics переносят это на compile-time: `List<String>` просто не примет `Integer`.
>
> **Type erasure** — это важный нюанс: информация о параметре типа стирается при компиляции. В bytecode `List<String>` и `List<Integer>` — один и тот же `List`. Поэтому нельзя написать `new T()` или `instanceof List<String>`. Компилятор вставляет касты сам, но в runtime типа нет.
>
> **PECS** — мой способ запомнить wildcards. Если коллекция производит элементы (ты читаешь) — `? extends T`. Если потребляет (ты пишешь) — `? super T`. Классический пример: метод `copy(List<? extends T> src, List<? super T> dest)` — читаем из src, пишем в dest.
>
> На практике: использую generics везде, где хранятся данные. Unbounded wildcard `<?>` — когда тип вообще не важен, например в утилитных методах."

## Шпаргалка

| Концепция | Суть | Ограничение |
|-----------|------|-------------|
| `List<T>` | Типобезопасная коллекция | Тип известен компилятору |
| `List<?>` | Любой тип, unbounded | Только `get()` → Object |
| `? extends T` | T и подтипы (Producer) | Нельзя `add()` |
| `? super T` | T и надтипы (Consumer) | `get()` → только Object |
| **Type erasure** | T стирается в runtime | Нет `new T()`, нет `instanceof List<String>` |
| **PECS** | Producer=Extends, Consumer=Super | Мнемоника для wildcards |

**Связи:**
- [[Устройство HashMap]]
- [[ArrayList vs LinkedList]]
- [[Stream API]]
