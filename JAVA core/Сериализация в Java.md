---
tags: [java, core, serialization, cloning]
sources: [CORE 1 Вопросы технических собеседований.pdf]
---

# Сериализация в Java

## 1. Проблема — зачем это существует?

Объекты в памяти — это временное состояние: выключили JVM — всё исчезло. Для передачи объектов по сети, сохранения на диск или в кэш нужно преобразовать граф объектов в байтовый поток. Сериализация решает именно это — и в обратном направлении (десериализация) восстанавливает объект из байтов.

## 2. Аналогия

Сериализация — как упаковка мебели для переезда. Разбираешь (сериализуешь) диван на части, кладёшь в коробки (байты), везёшь в новую квартиру, собираешь обратно (десериализуешь). `transient`-поля — это то, что не везёшь: личные ключи, кэшированные значения, которые в новом месте всё равно пересчитаются.

## 3. Как работает

### Serializable — маркерный интерфейс:

```java
import java.io.Serializable;

public class User implements Serializable {
    private static final long serialVersionUID = 1L; // версия класса

    private String name;           // сериализуется
    private int age;               // сериализуется
    private transient String password; // НЕ сериализуется (sensitive data)
    private static int count;      // НЕ сериализуется (static не принадлежит объекту)
}
```

### Запись и чтение:

```java
// Сериализация (объект → байты)
try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("user.ser"))) {
    oos.writeObject(user);
}

// Десериализация (байты → объект)
try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream("user.ser"))) {
    User restoredUser = (User) ois.readObject();
    // password == null (transient), name и age восстановлены
}
```

### 4 шага сериализации:

1. JVM проверяет, что класс реализует `Serializable`
2. Записывает метаданные класса (имя, `serialVersionUID`)
3. Рекурсивно сериализует все нетранзиентные нестатические поля
4. Поля-объекты тоже должны быть `Serializable` — иначе `NotSerializableException`

### serialVersionUID:

```java
private static final long serialVersionUID = 1L;
```

- JVM сравнивает UID класса в байтовом потоке с UID текущего класса
- Если не совпадают → `InvalidClassException`
- Если не объявлен явно → JVM вычисляет автоматически по структуре класса
- **Лучшая практика:** объявлять явно, чтобы контролировать совместимость версий

### Externalizable — ручная сериализация:

```java
public class FastUser implements Externalizable {
    private String name;
    private int age;

    // Обязательный конструктор без аргументов для десериализации!
    public FastUser() {}

    @Override
    public void writeExternal(ObjectOutput out) throws IOException {
        out.writeUTF(name);
        out.writeInt(age);
        // Полный контроль: пишем только нужное
    }

    @Override
    public void readExternal(ObjectInput in) throws IOException, ClassNotFoundException {
        name = in.readUTF();
        age = in.readInt();
    }
}
```

| | `Serializable` | `Externalizable` |
|--|----------------|-----------------|
| **Управление** | JVM автоматически | Полный ручной контроль |
| **Производительность** | Медленнее | Быстрее |
| **Конструктор** | Не вызывается при десериализации | Обязан быть без аргументов |
| **Применение** | Большинство случаев | Критичная производительность |

## 4. Глубже — клонирование

### Shallow Clone (поверхностное копирование):

```java
class Order implements Cloneable {
    String id;
    List<Item> items; // ссылка на список

    @Override
    public Object clone() throws CloneNotSupportedException {
        return super.clone(); // Cloneable — маркерный интерфейс
    }
}

Order original = new Order();
Order copy = (Order) original.clone();

// copy.id != original.id (примитив/String — скопированы)
// copy.items == original.items (!) — одна и та же коллекция!
copy.items.add(newItem); // изменяет и original!
```

**Shallow clone** копирует примитивы и ссылки, но не объекты, на которые ссылаются.

### Deep Clone (глубокое копирование):

```java
// Вариант 1: Copy constructor (предпочтительный)
class Order {
    String id;
    List<Item> items;

    public Order(Order other) {
        this.id = other.id;
        this.items = new ArrayList<>(other.items); // новый список
    }
}

// Вариант 2: через сериализацию (все вложенные объекты должны быть Serializable)
public static <T extends Serializable> T deepCopy(T object) {
    try {
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        new ObjectOutputStream(bos).writeObject(object);
        ByteArrayInputStream bis = new ByteArrayInputStream(bos.toByteArray());
        return (T) new ObjectInputStream(bis).readObject();
    } catch (Exception e) {
        throw new RuntimeException(e);
    }
}
```

### clone() — проблемы метода Object:

```java
// clone() объявлен в Object как protected
// Нужно переопределить как public и бросить CloneNotSupportedException
// Без implements Cloneable → CloneNotSupportedException при вызове super.clone()
```

Джошуа Блох в «Effective Java» рекомендует **copy constructor** или **фабричный метод** вместо `Cloneable` — интерфейс считается плохо спроектированным.

## 5. Связи с другими концепциями

- [[Контракт equals и hashCode]] — при клонировании важно, чтобы копия удовлетворяла контракту equals
- [[Иммутабельность String]] — String не нуждается в deep copy (иммутабелен)
- [[Паттерны проектирования]] — паттерн Prototype использует клонирование

## 6. Ответ на собесе (2 минуты)

> "Сериализация — преобразование объекта в байтовый поток для сохранения или передачи. `Serializable` — маркерный интерфейс, без методов. JVM автоматически сериализует все нетранзиентные нестатические поля.
>
> **`transient`** — помечаем поля, которые не нужно сохранять: пароли, кэши, вычислимые значения. **`serialVersionUID`** — версия класса для контроля совместимости при десериализации; лучше объявлять явно.
>
> **`Externalizable`** даёт полный контроль над форматом — пишем и читаем вручную. Быстрее `Serializable`, требует публичный конструктор без аргументов.
>
> **Клонирование:** `clone()` по умолчанию — shallow copy: примитивы копируются, объекты — только ссылки. Это источник багов: изменение коллекции в копии меняет оригинал. Для deep copy предпочитаю copy constructor — явно, понятно, без магии. `Cloneable` считается плохо спроектированным (Effective Java), я его избегаю."

## Шпаргалка

| Концепция | Суть | Ловушка |
|-----------|------|---------|
| **Serializable** | Маркерный интерфейс | Все поля-объекты тоже должны быть Serializable |
| **transient** | Поле не сериализуется | После десериализации = null (0, false) |
| **serialVersionUID** | Версия для совместимости | Без явного объявления = риск IncompatibleClassException |
| **Externalizable** | Ручной контроль | Обязателен no-arg конструктор |
| **Shallow clone** | Копирует ссылки | Мутирование копии = мутирование оригинала |
| **Deep clone** | Copy constructor / сериализация | Все вложенные объекты должны быть Serializable |

**Связи:**
- [[Контракт equals и hashCode]]
- [[Иммутабельность String]]
- [[Паттерны проектирования]]
