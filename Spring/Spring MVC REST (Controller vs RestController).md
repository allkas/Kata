---
tags: [spring, mvc, rest]
---
# Spring MVC REST
## 1. @Controller vs @RestController
- `@Controller` — возвращает имя view (MVC).
- `@RestController` = `@Controller` + `@ResponseBody` (REST API).
## 2. REST CRUD методы
| Операция | HTTP метод |
|----------|------------|
| Create | POST |
| Read (все) | GET |
| Read (один) | GET /{id} |
| Update (полное) | PUT |
| Update (частичное) | PATCH |
| Delete | DELETE |
## 3. Передача параметров фильтрации
Много параметров — через объект с `@ModelAttribute` или `@ParameterObject` (SpringDoc).
**Связи:**
- [[Разница HTTP методов]]
- [[Глобальная обработка исключений в Spring]]