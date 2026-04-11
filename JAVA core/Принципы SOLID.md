---
tags: [java, oop, design]
---
# Принципы SOLID
## 1. Расшифровка каждого
| Буква | Принцип | Суть |
|-------|---------|------|
| S | Single Responsibility | Один класс — одна причина для изменения |
| O | Open/Closed | Открыт для расширения, закрыт для изменения |
| L | Liskov Substitution | Подклассы должны заменять родителя без изменений |
| I | Interface Segregation | Много специализированных интерфейсов лучше одного общего |
| D | Dependency Inversion | Зависимость от абстракций, а не конкреций |
## 2. Пример нарушения LSP
```java
class Rectangle {
    void setWidth(int w) { width = w; }
    void setHeight(int h) { height = h; }
}
class Square extends Rectangle {
    void setWidth(int w) { width = height = w; }
    void setHeight(int h) { width = height = h; }
}
```
Клиент, ожидающий Rectangle, сломается на Square (изменение обеих сторон).

## 3. Single Responsibility, Open/Closed

- **SRP** — класс UserService отвечает только за пользователей.
    
- **OCP** — добавить новую валидацию через интерфейс Validator, не меняя старый код.
    

## 4. Когда можно нарушить Dependency Inversion?

При работе со статическими утилитными классами (Math, Collections) — осознанно нарушаем ради простоты.

## 5. Interface Segregation

Плохо: интерфейс Worker с методами work(), eat(), sleep().  
Хорошо: Workable, Eatable, Sleepable отдельно.

**Связи:**

- [[Основы ООП]]
    
- [[Spring Core IoC DI]]