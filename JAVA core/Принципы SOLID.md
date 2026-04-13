---
tags: [java, oop, design]
sources: [CORE 1 Вопросы технических собеседований.pdf]
---

# Принципы SOLID

## 1. Проблема — зачем это существует?

Без принципов код постепенно деградирует: классы обрастают обязанностями, изменение одного места ломает другие, добавить новую функцию без правки старого кода становится невозможным. SOLID — это набор правил, которые делают код **устойчивым к изменениям** и **расширяемым без переписывания**.

## 2. Аналогия

Представь кухню ресторана. **SRP**: у каждого повара одна специализация — соусы, выпечка, гриль. **OCP**: добавить новое блюдо = нанять нового повара, а не переобучать существующих. **LSP**: су-шеф может заменить шеф-повара на любой станции без сюрпризов. **ISP**: официант знает только меню своего зала, не весь ресторан. **DIP**: менеджер отдаёт заказ «повару», не конкретному человеку — можно заменить.

## 3. Как работает

| Буква | Принцип | Суть одним предложением |
|-------|---------|------------------------|
| **S** | Single Responsibility | Один класс — одна причина для изменения |
| **O** | Open/Closed | Открыт для расширения, закрыт для изменения |
| **L** | Liskov Substitution | Подкласс можно подставить вместо родителя без поломок |
| **I** | Interface Segregation | Много узких интерфейсов лучше одного толстого |
| **D** | Dependency Inversion | Зависеть от абстракций, не от конкреций |

### S — Single Responsibility
```java
// Нарушение: UserService и сохраняет, и отправляет email, и валидирует
class UserService {
    void saveUser(User u) { ... }
    void sendWelcomeEmail(User u) { ... } // чужая ответственность
    boolean validateEmail(String email) { ... } // чужая ответственность
}

// Исправление: разделить
class UserService { void saveUser(User u) { ... } }
class EmailService { void sendWelcomeEmail(User u) { ... } }
class EmailValidator { boolean validate(String email) { ... } }
```

### O — Open/Closed
```java
// Нарушение: каждый новый тип скидки — правка if-else
double discount(Order o) {
    if (o.type == PREMIUM) return 0.2;
    if (o.type == VIP) return 0.3; // правим существующий код
}

// Исправление: интерфейс + новые классы без правки старых
interface DiscountStrategy { double apply(Order o); }
class PremiumDiscount implements DiscountStrategy { ... }
class VipDiscount implements DiscountStrategy { ... }
```

### L — Liskov Substitution
**Классический пример нарушения — квадрат-прямоугольник:**
```java
class Rectangle {
    int width, height;
    void setWidth(int w) { this.width = w; }
    void setHeight(int h) { this.height = h; }
    int area() { return width * height; }
}

class Square extends Rectangle {
    @Override void setWidth(int w) { this.width = this.height = w; }  // нарушение!
    @Override void setHeight(int h) { this.width = this.height = h; } // нарушение!
}

// Клиентский код падает:
Rectangle r = new Square();
r.setWidth(5);
r.setHeight(3);
r.area(); // ожидаем 15, получаем 9 — поведение сломано
```
**Правило LSP:** подкласс не должен усиливать предусловия или ослаблять постусловия. Квадрат делает именно это — усиливает ограничение (оба размера равны).

### I — Interface Segregation
```java
// Нарушение: «толстый» интерфейс
interface Worker { void work(); void eat(); void sleep(); }
class Robot implements Worker {
    public void work() { ... }
    public void eat() { throw new UnsupportedOperationException(); } // роботы не едят
}

// Исправление:
interface Workable { void work(); }
interface Eatable { void eat(); }
class Human implements Workable, Eatable { ... }
class Robot implements Workable { ... }
```

### D — Dependency Inversion
```java
// Нарушение: зависимость от конкреции
class OrderService {
    private MySQLOrderRepository repo = new MySQLOrderRepository(); // жёсткая связь
}

// Исправление: зависимость от интерфейса (Spring DI делает это автоматически)
class OrderService {
    private final OrderRepository repo; // интерфейс

    OrderService(OrderRepository repo) { this.repo = repo; } // инъекция
}
```

## 4. Глубже — когда можно нарушить?

**DIP можно нарушить** для утилитных классов без состояния: `Math.abs()`, `Collections.sort()`, `Objects.hash()`. Нет смысла создавать интерфейс для `Math`.

**SRP** не означает «один метод». Класс может иметь много методов — главное, что все они относятся к одной **причине изменения** (stakeholder).

## 5. Связи с другими концепциями

- [[Основы ООП]] — SOLID строится на принципах ООП
- [[Интерфейс vs абстрактный класс]] — OCP, DIP, ISP завязаны на интерфейсах
- [[Spring Core IoC DI]] — Spring реализует DIP через инверсию зависимостей

## 6. Ответ на собесе (2 минуты)

> "SOLID — это пять принципов, которые решают конкретные проблемы роста кода.
>
> **S — SRP:** каждый класс должен иметь одну причину для изменения. Если `UserService` и сохраняет пользователей, и отправляет email — это два разных stakeholder'а. Разделяем на `UserService` и `EmailService`.
>
> **O — OCP:** добавлять новую функциональность через расширение, не через правку старого кода. Новый тип скидки — новый класс, реализующий интерфейс, а не новый `if` в существующем методе.
>
> **L — LSP:** подкласс должен корректно работать везде, где ожидается родитель. Классический пример нарушения — `Square extends Rectangle`: клиент устанавливает ширину 5 и высоту 3, ожидает площадь 15, получает 9. Поведение сломано.
>
> **I — ISP:** лучше несколько специализированных интерфейсов, чем один «толстый». Робот не должен реализовывать метод `eat()`.
>
> **D — DIP:** зависеть от интерфейсов, не от конкретных классов. Spring DI — это принцип DIP в действии: я инжектирую `OrderRepository`, а не `MySQLOrderRepository`.
>
> Все принципы взаимосвязаны и вместе дают код, который легко тестировать, расширять и изменять."

## Шпаргалка

| Принцип | Нарушение | Исправление |
|---------|-----------|-------------|
| **SRP** | UserService: save + email + validate | Разделить на 3 класса |
| **OCP** | `if (type==X)` в методе | Интерфейс + новые классы |
| **LSP** | Square ломает поведение Rectangle | Не наследовать Square от Rectangle |
| **ISP** | Robot реализует `eat()` с UOE | Разделить Worker на Workable, Eatable |
| **DIP** | `new MySQLRepo()` в бизнес-классе | Инжектировать интерфейс `Repository` |

**Связи:**
- [[Основы ООП]]
- [[Интерфейс vs абстрактный класс]]
- [[Spring Core IoC DI]]
