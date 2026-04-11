---
tags: [spring, ioc, di, core]
---
# Spring Core IoC DI
## 1. IoC/DI
**IoC (Inversion of Control)** — контейнер управляет объектами, а не код.
**DI (Dependency Injection)** — внедрение зависимостей через конструктор/setter/поле.
## 2. Bean scopes
| Scope | Описание |
|-------|----------|
| singleton | Один бин на контейнер (по умолчанию) |
| prototype | Новый бин при каждом запросе |
| request | На HTTP-запрос (web) |
| session | На HTTP-сессию |
| globalSession | Для портлетов |
## 3. @Component, @Service, @Repository, @Controller
- `@Component` — общий стереотип.
- `@Service` — сервисный слой (бизнес-логика).
- `@Repository` — DAO, перевод исключений в DataAccessException.
- `@Controller` — MVC контроллер.
## 4. @Autowired: куда ставить
- Поле — просто, но плохо для тестов.
- Сеттер — для опциональных зависимостей.
- **Конструктор** — рекомендовано (immutable, тестируемость, final).
## 5. Жизненный цикл бина
1. Создание
2. Внедрение зависимостей
3. `@PostConstruct` / afterPropertiesSet()
4. Использование
5. `@PreDestroy` / destroy()
## 6. Циклические зависимости
Spring решает через **setter-инъекцию** (создаёт через прокси) или `@Lazy`. Лучше перепроектировать.
**Связи:**
- [[Основы ООП]]
- [[Принципы SOLID]]