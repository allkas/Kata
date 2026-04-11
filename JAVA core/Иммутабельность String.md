---
tags: [java, string, immutable]
---
# Иммутабельность String
## 1. Почему String неизменяемый (immutable)
1. **Кэширование** — string pool (экономия памяти).
2. **Безопасность** — пароли, URL, classpath не изменятся.
3. **Синхронизация** — неизменяемые объекты потокобезопасны.
4. **HashCode** — кэшируется, не пересчитывается.
## 2. Как написать свой immutable-класс
```java
public final class ImmutablePerson {
    private final String name;
    private final List<String> hobbies;
    
    public ImmutablePerson(String name, List<String> hobbies) {
        this.name = name;
        // защитная копия
        this.hobbies = new ArrayList<>(hobbies);
    }
    
    public List<String> getHobbies() {
        return new ArrayList<>(hobbies); // защитная копия
    }
}
```
## 3. StringBuilder vs StringBuffer

|StringBuilder|StringBuffer|
|---|---|
|Не синхронизирован|Синхронизирован|
|Быстрее|Медленнее|
|Не потокобезопасен|Потокобезопасен|
|Java 5+|С Java 1.0|

## 4. String pool

Хранит литералы. Разница:

- `"строка"` — в pool (интернируется).
    
- `new String("строка")` — всегда новый объект в heap.
    

**Связи:**

- [[Контракт equals и hashCode]]
    
- [[Garbage Collector JVM]]