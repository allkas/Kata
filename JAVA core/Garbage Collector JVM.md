---
tags: [java, jvm, memory, gc]
---
# Garbage Collector JVM
## 1. Память JVM (heap, stack)
- **Stack** — примитивы, ссылки на объекты, локальные переменные (per-thread).
- **Heap** — все объекты, делится на молодое (Eden, S0, S1) и старое поколение.
## 2. Виды GC, когда объект недостижим
- **Minor GC** — в молодом поколении.
- **Major GC** — в старом.
- **Full GC** — везде.
Объект недостижим, если нет ссылок от корней (стек, статические поля, JNI).
## 3. WeakReference / SoftReference / WeakHashMap
- **SoftReference** — удаляется при нехватке памяти (кэш).
- **WeakReference** — удаляется при ближайшем GC.
- **WeakHashMap** — ключи WeakReference, удаляются при GC.
## 4. OutOfMemoryError, StackOverflowError
- **OutOfMemoryError** — нет памяти в heap.
- **StackOverflowError** — переполнение стека (глубокая рекурсия).
**Связи:**
- [[Иммутабельность String]]
- [[Многопоточность основы]]