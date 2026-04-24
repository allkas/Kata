---
tags: [java, string, immutable, core]
sources: [CORE 1 Вопросы технических собеседований.pdf]
---

# Иммутабельность String

## 1. Проблема — зачем это существует?

Строки используются везде: имена, пути, URL, пароли, ключи в коллекциях. Если бы `String` был изменяемым — одно место в коде могло бы тихо изменить строку, которую используют десять других мест. Immutability устраняет весь этот класс багов и даёт бонусы: кэширование hashCode, потокобезопасность и String Pool.

## 2. Аналогия

**Immutable объект** — как напечатанная книга. Ты можешь прочитать её, скопировать, сделать новое издание с изменениями — но саму книгу не можешь исправить ручкой. Любое «изменение» создаёт **новую книгу**.

**Mutable объект** — как Word-документ на общем диске. Кто угодно может отредактировать его в любой момент, и ты не знаешь, что документ изменился.

## 3. Как работает

### Почему String immutable:
1. **Безопасность** — пароли, URL, пути к классам (`ClassLoader`) не изменятся после передачи
2. **String Pool** — одну строку можно безопасно шарить между разными объектами
3. **HashCode кэшируется** — вычисляется один раз, потом хранится в поле (String — идеальный ключ HashMap)
4. **Потокобезопасность** — неизменяемые объекты не требуют синхронизации

### String Pool:
```java
String a = "hello";          // из пула
String b = "hello";          // тот же объект из пула
String c = new String("hello"); // новый объект в heap, НЕ из пула

a == b;       // true  (одна ссылка)
a == c;       // false (разные объекты)
a.equals(c);  // true  (одинаковое содержимое)

String d = c.intern(); // явно поместить в пул
a == d; // true
```
String Pool находится в **Heap** (с Java 7+, до этого — в PermGen).

### StringBuilder vs StringBuffer:
| | StringBuilder | StringBuffer |
|---|---|---|
| **Потокобезопасность** | Нет | Да (synchronized) |
| **Скорость** | Быстрее | Медленнее |
| **Появился** | Java 5 | Java 1.0 |
| **Когда** | Однопоточный код | Многопоточный (редко нужен) |

**Правило:** всегда `StringBuilder`. `StringBuffer` нужен только в многопоточном контексте — и даже тогда лучше переосмыслить дизайн.

**Конкатенация в цикле — антипаттерн:**
```java
// Плохо: создаёт N промежуточных строк
String result = "";
for (String s : list) result += s; // O(n²)

// Хорошо:
StringBuilder sb = new StringBuilder();
for (String s : list) sb.append(s); // O(n)
String result = sb.toString();
```
Компилятор оптимизирует `+` в StringBuilder только вне цикла.

## 4. Глубже — как написать свой immutable-класс

**5 правил:**

```java
public final class ImmutableOrder {          // 1. final — запрет наследования
    private final String id;                 // 2. все поля private final
    private final List<String> items;        // мутабельное поле — особая осторожность

    public ImmutableOrder(String id, List<String> items) {
        this.id = id;
        this.items = new ArrayList<>(items); // 3. защитная копия в конструкторе
    }

    public String getId() { return id; }     // 4. только геттеры, никаких сеттеров

    public List<String> getItems() {
        return Collections.unmodifiableList(items); // 5. защитная копия в геттере
    }
}
```

**Правило 1 — `final class`:** без этого подкласс мог бы добавить мутабельные поля и нарушить контракт.

**Правило 3 — защитная копия в конструкторе:**
```java
List<String> mutableList = new ArrayList<>(Arrays.asList("a", "b"));
ImmutableOrder order = new ImmutableOrder("1", mutableList);
mutableList.add("c"); // без защитной копии — изменит items внутри order!
```

**Правило 5 — защитная копия в геттере:**
```java
order.getItems().add("hack"); // без защиты — изменит внутренний список
// с Collections.unmodifiableList() — UnsupportedOperationException
```

## 5. Связи с другими концепциями

- [[Контракт equals и hashCode]] — String immutable → hashCode кэшируется → идеальный ключ
- [[Garbage Collector JVM]] — String Pool в Heap, GC управляет памятью под строки
- [[Многопоточность основы]] — immutable объекты не требуют синхронизации

## 6. Ответ на собесе (2 минуты)

> "String immutable — не случайность, это осознанное дизайн-решение с несколькими бенефитами.
>
> **Безопасность:** строки используют как ключи в classpath, URL, пароли. Если бы они были изменяемыми, после проверки безопасности кто-то мог бы тихо поменять путь к файлу.
>
> **String Pool:** JVM кэширует строковые литералы. `'hello'` и `'hello'` — это один и тот же объект в памяти. Это работает только потому, что строка не изменится.
>
> **HashCode:** вычисляется один раз и кэшируется в поле. String — идеальный ключ для HashMap.
>
> **Про StringBuilder:** для конкатенации в цикле всегда использую `StringBuilder`. Конкатенация через `+` создаёт промежуточные строки — это O(n²). `StringBuilder` — O(n). `StringBuffer` — синхронизированная версия, но в 2024 году нужна крайне редко.
>
> **Immutable-класс** — пять правил: `final class`, все поля `private final`, только геттеры, и самое важное — **защитные копии** для мутабельных полей (коллекций, массивов) и в конструкторе, и в геттере. Без этого класс технически final, но содержимое коллекции изменить можно."

## Шпаргалка

| Концепция | Суть | Деталь |
|-----------|------|--------|
| **String immutable** | Безопасность, пул, кэш hashCode | Поле `value` — `private final byte[]` |
| **String Pool** | Литералы шарятся в heap | `"a" == "a"` → true; `new String("a") == "a"` → false |
| **StringBuilder** | Изменяемая строка, не потокобезопасен | Для цикла и конкатенации |
| **StringBuffer** | Синхронизированный StringBuilder | Редко нужен |
| **Immutable-класс** | 5 правил | `final class` + `final fields` + защитные копии |

**Связи:**
- [[Контракт equals и hashCode]]
- [[Garbage Collector JVM]]
- [[Многопоточность основы]]
