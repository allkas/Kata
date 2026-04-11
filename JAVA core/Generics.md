---
tags: [java, generics, core]
---
# Generics
## 1. Зачем нужны
- Типобезопасность (ошибки на этапе компиляции).
- Избавление от явного кастинга.
- Обобщённые алгоритмы.
## 2. Стирание типов (type erasure)
Информация о T стирается в runtime — все обобщения становятся Object (или границей). Видно только через рефлексию полей.
## 3. PECS — Producer Extends, Consumer Super
- `? extends T` — producer (читаем T) — можно get, нельзя put.
- `? super T` — consumer (пишем T) — можно put, нельзя get (кроме Object).
```java
void copy(List<? extends T> src, List<? super T> dest) {
    for (T item : src) dest.add(item);
}
```
**Связи:**

- [[Устройство HashMap]]
    
- [[Stream API]]