---
tags: [spring, mvc, rest, controller]
sources: [Spring Вопросы технических собеседований.pdf]
---

# Spring MVC REST (Controller vs RestController)

## 1. Проблема — зачем это существует?

HTTP-запрос приходит в приложение. Кто его принимает? Как JSON превращается в Java-объект и обратно? Как вернуть `404` вместо `200` при ошибке? Spring MVC решает эти задачи через `DispatcherServlet` и контроллеры — центральный паттерн web-слоя.

## 2. Аналогия

`DispatcherServlet` — как ресепшн в большом офисе. Все клиенты (HTTP-запросы) приходят туда. Ресепшн смотрит на адрес назначения (URL + HTTP-метод) и направляет к нужному сотруднику (`@RequestMapping`-методу). Сотрудник выполняет работу и возвращает результат — ресепшн упаковывает его в конверт (JSON) и отправляет клиенту.

## 3. @Controller vs @RestController

```
@RestController = @Controller + @ResponseBody
```

| | `@Controller` | `@RestController` |
|--|--------------|-------------------|
| **Возвращает** | Имя View (шаблон) | Данные (JSON/XML) |
| **`@ResponseBody`** | Нужно на каждом методе | Уже включён |
| **Применение** | Server-side rendering (Thymeleaf) | REST API |
| **Пример ответа** | `"user/profile"` → Thymeleaf рендерит HTML | `User` → Jackson сериализует в JSON |

```java
// @Controller — для MVC (View-based)
@Controller
public class UserViewController {
    @GetMapping("/users/{id}")
    public String showUser(@PathVariable Long id, Model model) {
        model.addAttribute("user", userService.findById(id));
        return "user/profile"; // → templates/user/profile.html
    }
}

// @RestController — для REST API
@RestController
@RequestMapping("/api/users")
public class UserController {
    @GetMapping("/{id}")
    public UserDto getUser(@PathVariable Long id) {
        return userService.findById(id); // Jackson → {"id":1,"name":"..."}
    }
}
```

## 4. REST CRUD: HTTP-методы и статусы

| Операция | HTTP метод | URL | Статус успеха | Тело ответа |
|----------|-----------|-----|---------------|-------------|
| Создать | `POST` | `/users` | `201 Created` | созданный объект |
| Получить все | `GET` | `/users` | `200 OK` | список |
| Получить один | `GET` | `/users/{id}` | `200 OK` | объект |
| Полное обновление | `PUT` | `/users/{id}` | `200 OK` | обновлённый объект |
| Частичное обновление | `PATCH` | `/users/{id}` | `200 OK` | обновлённый объект |
| Удалить | `DELETE` | `/users/{id}` | `204 No Content` | пусто |

```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping
    public List<UserDto> getAll() {
        return userService.findAll();
    }

    @GetMapping("/{id}")
    public UserDto getById(@PathVariable Long id) {
        return userService.findById(id); // выбрасывает NotFoundException если нет
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserDto create(@RequestBody @Valid CreateUserRequest request) {
        return userService.create(request);
    }

    @PutMapping("/{id}")
    public UserDto update(@PathVariable Long id, @RequestBody @Valid UpdateUserRequest request) {
        return userService.update(id, request);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable Long id) {
        userService.delete(id);
    }
}
```

## 5. Аннотации параметров метода

| Аннотация | Откуда берёт | Пример |
|-----------|-------------|--------|
| `@PathVariable` | Из URL-пути | `/users/{id}` → `@PathVariable Long id` |
| `@RequestParam` | Из query string | `/users?page=0` → `@RequestParam int page` |
| `@RequestBody` | Из тела запроса (JSON) | `@RequestBody CreateUserRequest req` |
| `@RequestHeader` | Из HTTP-заголовка | `@RequestHeader("Authorization") String token` |

## 6. Фильтрация: как передавать много параметров

**Плохо:** `@RequestParam` на каждый параметр — сигнатура разрастается:
```java
// Антипаттерн:
@GetMapping("/search")
public List<UserDto> search(@RequestParam String name,
                            @RequestParam Integer age,
                            @RequestParam String city) { ... }
```

**Хорошо:** объединить в DTO + `@ModelAttribute`:
```java
// DTO для фильтров:
public class UserFilter {
    private String name;
    private Integer age;
    private String city;
    // getters/setters
}

@GetMapping("/search")
public List<UserDto> search(@ModelAttribute UserFilter filter) {
    // GET /search?name=Ivan&age=25&city=Moscow
    return userService.search(filter);
}
```

**Альтернатива с SpringDoc/OpenAPI:** `@ParameterObject` для корректной документации Swagger.

## 7. Как работает DispatcherServlet

```
HTTP Request
    ↓
DispatcherServlet          ← Front Controller (один на приложение)
    ↓
HandlerMapping             ← находит метод по URL + HTTP-метод
    ↓
HandlerAdapter             ← вызывает метод контроллера
    ↓
MessageConverter           ← JSON ↔ Java (Jackson по умолчанию)
    ↓
HTTP Response (JSON)
```

`@RestController` добавляет `@ResponseBody` — сигнал для `MessageConverter` сериализовать возврат метода в тело ответа, а не искать View.

## 8. Связи с другими концепциями

- [[Spring Boot]] — `spring-boot-starter-web` автоматически настраивает `DispatcherServlet` и Jackson
- [[Глобальная обработка исключений в Spring]] — `@ControllerAdvice` перехватывает исключения из контроллеров
- [[Разница HTTP методов]] — семантика GET/POST/PUT/PATCH/DELETE
- [[PUT vs PATCH, идемпотентность HTTP-методов]] — идемпотентность REST-методов

## 9. Ответ на собесе (2 минуты)

> "`@RestController` = `@Controller` + `@ResponseBody`. `@Controller` возвращает имя шаблона для View (например Thymeleaf), `@RestController` — данные, которые Jackson сериализует в JSON. Разница в одной аннотации `@ResponseBody` — она говорит Spring не искать View, а писать возврат метода прямо в тело ответа.
>
> **REST CRUD:** POST для создания (`201 Created`), GET для чтения, PUT для полного обновления, PATCH для частичного, DELETE для удаления (`204 No Content`).
>
> **Параметры:** `@PathVariable` — из пути, `@RequestParam` — из query string, `@RequestBody` — из тела. Для сложных фильтров — `@ModelAttribute` с DTO, а не десяток `@RequestParam`.
>
> **DispatcherServlet** — Front Controller: принимает все запросы, делегирует HandlerMapping (найти метод), HandlerAdapter (вызвать), MessageConverter (Jackson сериализует). Spring Boot настраивает всё это автоматически через `spring-boot-starter-web`."

## Шпаргалка

| Концепция | Суть | Деталь |
|-----------|------|--------|
| **@RestController** | @Controller + @ResponseBody | Для REST API, JSON |
| **@Controller** | View-based | Для server-side rendering |
| **POST /resource** | Create → 201 | Тело с объектом |
| **GET /resource/{id}** | Read → 200 | Объект |
| **PUT /resource/{id}** | Full update → 200 | Идемпотентный |
| **DELETE /resource/{id}** | Delete → 204 | Без тела |
| **@PathVariable** | Из URL `/users/{id}` | Обязательный |
| **@RequestParam** | Из query `?page=0` | Опциональный |
| **@ModelAttribute** | Объект из query params | Для фильтров |
| **DispatcherServlet** | Front Controller | Один на приложение |

**Связи:**
- [[Spring Boot]]
- [[Глобальная обработка исключений в Spring]]
- [[Разница HTTP методов]]
- [[PUT vs PATCH, идемпотентность HTTP-методов]]
