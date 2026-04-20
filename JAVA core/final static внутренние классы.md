---
tags: [java, keywords, inner-classes, final, static]
sources: [Вопросы технических собеседований (1).pdf]
---

# final, static, внутренние классы

## 1. Проблема — зачем это существует?

Без `final` — любой класс можно унаследовать и сломать его контракт. Без `static` — каждый вспомогательный метод требует создания объекта. Без вложенных классов — связанная логика расползается по разным файлам. Эти механизмы дают точный контроль: что неизменяемо, что принадлежит классу, а не экземпляру, и как группировать связанный код.

## 2. Аналогия

`final` — печать «Окончательно». Документ с такой печатью нельзя переписать или продолжить.

`static` — доска объявлений на двери офиса. Информация принадлежит всему офису (классу), а не конкретному сотруднику (объекту). Любой может прочитать, не заходя внутрь.

Вложенные классы — ящики стола. Маленький ящик `Iterator` находится внутри большого `ArrayList`, потому что без него не имеет смысла существовать.

## 3. Ключевое слово final

### Три применения:

```java
// 1. final class — нельзя наследовать
final class ImmutablePoint {
    final int x, y;
    // никто не расширит и не сломает гарантии
}
// Пример из JDK: String, Integer, LocalDate

// 2. final method — нельзя переопределить (но наследовать класс можно)
class BaseService {
    final void validateInput(String input) {
        // критичная валидация, которую нельзя обойти
    }
}

// 3. final переменная — нельзя переприсвоить
final int MAX = 100;        // примитив — значение неизменно
final List<String> list = new ArrayList<>();  // ссылка неизменна,
list.add("ok");             // но содержимое менять можно!
```

### final vs static:

| | `final` | `static` |
|--|---------|---------|
| **Смысл** | Неизменяемость / нерасширяемость | Принадлежит классу, не объекту |
| **Переменная** | Нельзя переприсвоить | Одна на все объекты (разделяется) |
| **Метод** | Нельзя переопределить | Вызывается без объекта |
| **Класс** | Нельзя наследовать | Вложенный класс без ссылки на внешний |
| **Комбинация** | `static final` — константа | `static final PI = 3.14159` |

```java
class Config {
    static final String DB_URL = "jdbc:postgresql://localhost/mydb"; // константа
    static int instanceCount = 0;  // счётчик, общий для всех

    Config() { instanceCount++; }  // каждый конструктор увеличивает
}

Config a = new Config();
Config b = new Config();
System.out.println(Config.instanceCount); // 2 — без объекта
```

## 4. Может ли статический класс содержать нестатические поля?

**Да.** Статический вложенный класс — это обычный класс, который просто _расположен_ внутри другого. Он не привязан к экземпляру внешнего класса, но сам по себе создаёт свои экземпляры с нестатическими полями.

```java
class Outer {
    static class Node {          // static nested class
        int value;               // нестатическое поле — OK
        Node next;               // ещё одно

        Node(int value) { this.value = value; }
    }
}

Outer.Node node = new Outer.Node(42); // без экземпляра Outer
```

Именно так устроен `LinkedList.Node` в JDK — статический вложенный класс со своими полями.

## 5. Типы вложенных классов

| Тип | Как объявить | Ссылка на внешний | Типичное применение |
|-----|-------------|-------------------|---------------------|
| **Static Nested** | `static class Inner` | Нет | Builder, Node, Entry в коллекциях |
| **Inner (non-static)** | `class Inner` | Да (`Outer.this`) | Iterator, Event listener |
| **Local** | Внутри метода | Нет | Локальная реализация интерфейса |
| **Anonymous** | `new Interface() {}` | Нет | Callback, Runnable, Comparator |

```java
class LinkedList<T> {
    // Static nested — работает без экземпляра LinkedList
    static class Node<T> {
        T data;
        Node<T> next;
    }

    // Inner — имеет доступ к полям LinkedList
    class Iterator {
        Node<T> current = head;  // head — поле LinkedList
        // ...
    }
}

// Anonymous class
Runnable r = new Runnable() {
    @Override
    public void run() { System.out.println("hello"); }
};
// В современном Java заменяется лямбдой: () -> System.out.println("hello")
```

## 6. Sealed классы (Java 15+) и Enum

### Sealed classes — контроль иерархии:

```java
// Только перечисленные классы могут расширять Shape
public sealed class Shape permits Circle, Rectangle, Triangle { }

public final class Circle extends Shape { double radius; }
public final class Rectangle extends Shape { double width, height; }
public non-sealed class Triangle extends Shape { } // Triangle снова открыт

// С switch (Java 17+, pattern matching):
double area = switch (shape) {
    case Circle c    -> Math.PI * c.radius * c.radius;
    case Rectangle r -> r.width * r.height;
    case Triangle t  -> computeTriangleArea(t);
};
// Компилятор гарантирует полноту — не нужен default
```

Модификаторы для подклассов: `final` (нельзя расширять), `sealed` (снова запечатан), `non-sealed` (открыт для всех).

### Enum — API и возможности:

```java
public enum Status {
    ACTIVE("Активен"), INACTIVE("Неактивен"), DELETED("Удалён");

    private final String displayName;

    Status(String displayName) {
        this.displayName = displayName; // конструктор — всегда private
    }

    public String getDisplayName() { return displayName; }
}

// Встроенные методы:
Status s = Status.ACTIVE;
s.name();        // "ACTIVE"   — имя константы
s.ordinal();     // 0          — порядковый номер (с 0)
s.toString();    // "ACTIVE"   — по умолчанию = name()

Status.values();                     // Status[] — все константы
Status.valueOf("INACTIVE");          // Status.INACTIVE — по имени

// Enum в switch:
switch (status) {
    case ACTIVE   -> process();
    case DELETED  -> throw new IllegalStateException();
}
```

Enum наследует `java.lang.Enum`, является `final` — нельзя наследовать.

### Порядок инициализации:

```java
class Parent {
    static { System.out.println("1. Parent static block"); }
    { System.out.println("3. Parent instance block"); }
    Parent() { System.out.println("4. Parent constructor"); }
}

class Child extends Parent {
    static { System.out.println("2. Child static block"); }
    { System.out.println("5. Child instance block"); }
    Child() { System.out.println("6. Child constructor"); }
}

new Child();
// Вывод:
// 1. Parent static block   (статика родителя — один раз при загрузке класса)
// 2. Child static block    (статика потомка — один раз)
// 3. Parent instance block (нестатика родителя — при каждом new)
// 4. Parent constructor
// 5. Child instance block
// 6. Child constructor
```

### Типы конструкторов:

| Тип | Когда создаётся | Пример |
|-----|----------------|--------|
| **Default** | Компилятор генерирует автоматически, если нет явных | `class User {}` → `User()` |
| **Parameterized** | Явно объявлен с параметрами | `User(String name, int age)` |
| **Copy constructor** | Принимает объект того же типа | `User(User other)` |

```java
class User {
    String name; int age;

    // Parameterized
    User(String name, int age) { this.name = name; this.age = age; }

    // Copy constructor (вместо clone())
    User(User other) { this.name = other.name; this.age = other.age; }
}
```

## 7. Глубже — нюансы

### final поле vs final переменная:
```java
class Order {
    final String id;      // должно быть присвоено в конструкторе
    final List<Item> items = new ArrayList<>();  // список можно менять, ссылка — нет

    Order(String id) {
        this.id = id;     // OK — один раз в конструкторе
        // this.id = "other"; // ошибка компиляции
    }
}
```

### Static и наследование:
```java
class Parent {
    static void staticMethod() { System.out.println("Parent"); }
    void instanceMethod() { System.out.println("Parent"); }
}
class Child extends Parent {
    static void staticMethod() { System.out.println("Child"); } // HIDE (не override!)
    @Override
    void instanceMethod() { System.out.println("Child"); }     // override
}

Parent obj = new Child();
obj.staticMethod();   // "Parent" — статика не полиморфна
obj.instanceMethod(); // "Child"  — динамическая диспетчеризация
```

### Builder pattern через static nested:
```java
class User {
    private final String name;
    private final String email;

    private User(Builder builder) {
        this.name = builder.name;
        this.email = builder.email;
    }

    static class Builder {      // static — создаётся без User
        private String name;
        private String email;

        Builder name(String name) { this.name = name; return this; }
        Builder email(String email) { this.email = email; return this; }
        User build() { return new User(this); }
    }
}

User user = new User.Builder().name("Alice").email("alice@example.com").build();
```

## 8. Связи с другими концепциями

- [[Основы ООП]] — override vs hide static методов
- [[Иммутабельность String]] — `final class` как гарантия неизменности
- [[Интерфейс vs абстрактный класс]] — `default` и `static` методы в интерфейсах
- [[Generics]] — `static` методы в generic-классах не видят тип T

## 9. Ответ на собесе (2 минуты)

> "`final` — три применения: `final class` нельзя наследовать (String, Integer), `final method` нельзя переопределить, `final variable` нельзя переприсвоить — но мутировать содержимое объекта можно.
>
> **final vs static:** final — про неизменяемость, static — про принадлежность классу, а не объекту. Вместе: `static final` — константа.
>
> **Статический класс содержать нестатические поля — да.** Static nested class — обычный класс, просто вложенный. Примеры в JDK: `LinkedList.Node`, `HashMap.Entry`. Создаётся без экземпляра внешнего класса.
>
> **Виды вложенных классов:** статический вложенный (Node, Builder), нестатический inner (Iterator — имеет доступ к полям внешнего), локальный (внутри метода), анонимный (`new Runnable() {}`). В современном коде анонимные классы заменяются лямбдами.
>
> **Ловушка со статикой:** статические методы не участвуют в полиморфизме. `Child.staticMethod()` при `Parent ref = new Child()` вызовет метод `Parent`."

## Шпаргалка

| Концепция | Суть | Пример |
|-----------|------|--------|
| **final class** | Нельзя наследовать | `String`, `Integer` |
| **final method** | Нельзя переопределить | Защита контракта |
| **final variable** | Нельзя переприсвоить | Ссылка, но не содержимое |
| **static final** | Константа | `MAX_SIZE = 100` |
| **static method** | Без объекта | `Math.abs()` |
| **static nested** | Вложен, нет доступа к this | Builder, Node |
| **inner class** | Доступ к полям внешнего | Iterator |
| **anonymous class** | `new Interface() {}` | Замена лямбдой |
| **static vs override** | Статика — hide, не override | Нет полиморфизма |

**Связи:**
- [[Основы ООП]]
- [[Иммутабельность String]]
- [[Интерфейс vs абстрактный класс]]
- [[Generics]]
