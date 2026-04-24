---
tags: [java, jvm, classloader, bytecode]
sources: [CORE 1 Вопросы технических собеседований.pdf]
---

# JVM устройство и ClassLoader

## 1. Проблема — зачем это существует?

Java обещает WORA (Write Once, Run Anywhere): один и тот же `.class`-файл работает на Windows, Linux, Mac — без перекомпиляции. Это возможно благодаря промежуточному слою — JVM. Она интерпретирует байткод, а ClassLoader отвечает за загрузку и инициализацию классов в нужный момент.

## 2. Аналогия

JDK — это полная мастерская с инструментами (компилятор, отладчик, профайлер). JRE — только готовый продукт для пользователя (JVM + стандартные библиотеки). JVM — виртуальный завод, который запускает программу: ClassLoader привозит «чертежи» (классы), JIT-компилятор оптимизирует «производство» (горячий код), GC убирает мусор.

## 3. Как работает

### Иерархия JDK ⊃ JRE ⊃ JVM:

```
JDK (Java Development Kit)
└── JRE (Java Runtime Environment)
    ├── JVM (Java Virtual Machine)
    │   ├── ClassLoader
    │   ├── JIT Compiler
    │   ├── Garbage Collector
    │   └── Runtime Data Areas (Stack, Heap, Metaspace...)
    └── Standard Libraries (java.lang, java.util, ...)
+ javac, javadoc, jdb, jar... (только в JDK)
```

### Путь от исходника до выполнения:

```
Source.java
    ↓ javac (компилятор)
Source.class (байткод — платформонезависимые инструкции)
    ↓ ClassLoader (загрузка в память JVM)
Loaded Class (в Metaspace)
    ↓ Interpreter + JIT Compiler
Native Machine Code (выполнение)
```

### Три встроенных ClassLoader:

| ClassLoader | Загружает | Откуда |
|-------------|-----------|--------|
| **Bootstrap** | `java.lang.*`, `java.util.*` | `rt.jar` / `java.base` (ядро JDK) |
| **Extension (Platform)** | Расширения JDK | `lib/ext/` или `java.ext.dirs` |
| **System (Application)** | Классы приложения | `-classpath` / `CLASSPATH` |

### Три принципа ClassLoader:

**1. Delegation (делегирование):**
```
System ClassLoader получает запрос
    → делегирует Extension ClassLoader
        → делегирует Bootstrap ClassLoader
            → Bootstrap не нашёл → Extension пробует сам
                → Extension не нашёл → System загружает сам
```
Родительский ClassLoader всегда получает приоритет.

**2. Visibility (видимость):**
Child ClassLoader видит классы родителя. Родитель не видит классы child. Bootstrap видит только ядро — не видит классы приложения.

**3. Uniqueness (уникальность):**
Класс загружается только один раз в данном ClassLoader. Один `ClassLoader.loadClass("com.example.Foo")` → один объект `Class<Foo>`. Перезагрузить — только через новый ClassLoader (применяется в hot-reload, OSGi).

### JIT-компилятор:

```
Байткод
    ↓ Interpreter (медленно, но сразу)
    ↓ JIT (обнаруживает «горячий» код — часто выполняемые методы)
    ↓ Компилирует в нативный машинный код + оптимизации
    ↓ Кэш в Code Cache
```

JIT-оптимизации: inlining (вставка тела метода), loop unrolling, escape analysis (объект на Stack вместо Heap). HotSpot JVM — потому что обнаруживает «горячие точки».

### Динамическая загрузка — три шага:

```java
// 1. Loading — байткод класса читается с диска/сети в память
Class<?> clazz = Class.forName("com.example.MyPlugin");

// 2. Linking:
//    - Verification — проверка корректности байткода
//    - Preparation — выделение памяти под static-поля
//    - Resolution — разрешение символических ссылок

// 3. Initialization — выполнение static-блоков, присвоение static-полей
Object instance = clazz.getDeclaredConstructor().newInstance();
```

## 4. Глубже — нюансы

### ClassNotFoundException vs NoClassDefFoundError:

```java
// ClassNotFoundException — checked, класс не найден при Class.forName()
try {
    Class.forName("com.missing.DriverClass");
} catch (ClassNotFoundException e) { ... }

// NoClassDefFoundError — класс был при компиляции, но исчез в рантайме
// Типичная причина: неполный classpath в prod
```

### Custom ClassLoader (применения):

- **Hot-reload** в IDE и Spring DevTools: загружает обновлённый класс в новый ClassLoader
- **Изоляция плагинов**: каждый плагин — свой ClassLoader, конфликты зависимостей невозможны
- **Шифрование bytecode**: Custom ClassLoader дешифрует перед загрузкой

### Metaspace (Java 8+):

```
Java 7: PermGen (постоянное поколение) — фиксированный размер → OutOfMemoryError: PermGen
Java 8+: Metaspace — хранится в native memory, растёт динамически
         -XX:MaxMetaspaceSize=256m — ограничение (по умолчанию не ограничено)
```

## 5. Связи с другими концепциями

- [[Garbage Collector JVM]] — GC управляет Heap, Metaspace — отдельно
- [[final static внутренние классы]] — `static` поля инициализируются при загрузке класса
- [[Исключения в Java]] — `ExceptionInInitializerError` при ошибке в static-блоке

## 6. Ответ на собесе (2 минуты)

> "JDK включает JRE, JRE включает JVM. Разработчику нужен JDK (с компилятором javac), пользователю — только JRE. Java компилирует исходник в платформонезависимый байткод, JVM на каждой платформе исполняет его — это принцип WORA.
>
> **ClassLoader** загружает классы по требованию. Три встроенных: Bootstrap загружает ядро Java (java.lang, java.util), Extension — расширения JDK, System — классы приложения с classpath. Работают по принципу **делегирования**: сначала проверяет родительский ClassLoader, потом загружает сам. Это гарантирует, что `String` из приложения не затрёт `java.lang.String`.
>
> **JIT-компилятор** — ключевая оптимизация. Interpreter запускает байткод сразу, JIT обнаруживает часто вызываемые («горячие») методы и компилирует их в нативный код с оптимизациями. Поэтому Java-приложения разгоняются со временем — JIT накапливает профиль выполнения.
>
> **ClassNotFoundException vs NoClassDefFoundError:** первое — checked, класс не найден по имени строки. Второе — класс был при компиляции, но исчез в рантайме. Классика продакшна: неполный classpath."

## Шпаргалка

| Компонент | Суть | Пример |
|-----------|------|--------|
| **JDK** | JRE + компилятор + инструменты | javac, jdb, jar |
| **JRE** | JVM + стандартные библиотеки | Для запуска программ |
| **JVM** | Запускает байткод | HotSpot, GraalVM |
| **Bootstrap CL** | Ядро JDK | rt.jar / java.base |
| **System CL** | Classpath приложения | Наши классы |
| **Delegation** | Родитель первым | Bootstrap → Ext → System |
| **JIT** | Горячий код → нативный | Разгон со временем |
| **Metaspace** | Метаданные классов | Заменил PermGen (Java 8) |

**Связи:**
- [[Garbage Collector JVM]]
- [[final static внутренние классы]]
- [[Исключения в Java]]
