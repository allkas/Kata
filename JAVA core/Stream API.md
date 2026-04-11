---
tags: [java, streams, functional]
---
# Stream API
## 1. Промежуточные/терминальные операции
- **Промежуточные** — возвращают Stream (filter, map, flatMap).
- **Терминальные** — возвращают результат (collect, forEach, count).
- Stream ленивый — выполняется только при вызове терминальной.
## 2. map vs flatMap
- **map** — преобразует каждый элемент в другой (1 → 1).
- **flatMap** — преобразует каждый элемент в Stream и объединяет (1 → много).
```java
// map: List<List<String>> -> List<Stream<String>>
// flatMap: List<List<String>> -> List<String>
```
## 3. Функциональные интерфейсы, лямбды

- Predicate<T> — test()
    
- Function<T,R> — apply()
    
- Consumer<T> — accept()
    
- Supplier<T> — get()
    

Лямбда — краткая запись анонимного метода.

## 4. Optional

Контейнер, который может содержать null. Использовать для возврата значений, а не полей.

## 5. Можно ли повторно использовать Stream?

Нет. Stream можно использовать только один раз.

**Связи:**

- [[Контракт equals и hashCode]]
    
- [[Generics]]