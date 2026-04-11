---
tags: [testing, mockito, junit]
---
# Unit-тесты Mockito
## 1. Mock vs Spy
- **Mock** — полностью искусственный объект, методы ничего не делают.
- **Spy** — обёртка над реальным объектом, можно подменить часть методов.
## 2. Как проверить, что метод вызывался (verify)
```java
verify(mock).method(args);
verify(mock, times(2)).method(args);
verify(mock, never()).method(args);
```
## 3. @Mock, @InjectMocks, @Spy

- `@Mock` — создаёт мок.
    
- `@Spy` — создаёт шпиона.
    
- `@InjectMocks` — создаёт объект и внедряет все `@Mock` и `@Spy`.
    

**Связи:**

- [[Spring Core IoC DI]]
    
- [[Основы ООП]]