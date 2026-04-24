---
tags: [spring, mvc, dispatcherservlet, web]
sources: [Kata Spring Framework & HTTP.pdf]
---

# Spring MVC DispatcherServlet

## 1. Проблема — зачем это существует?

В классическом Servlet API каждый URL обрабатывается отдельным сервлетом: `OrderServlet`, `UserServlet`, `PaymentServlet`. Для каждого — отдельная конфигурация, отдельная логика парсинга параметров, сериализации ответа. Spring MVC централизует всё через **Front Controller**: один сервлет принимает все запросы, а дальше делегирует нужному контроллеру.

## 2. Аналогия

`DispatcherServlet` — как рецепция крупного отеля. Все гости (запросы) входят через одну дверь (один сервлет). Рецепционист (DispatcherServlet) смотрит на запрос и решает: этого гостя — в ресторан (OrderController), того — в спа (UserController). Он не готовит еду сам — только маршрутизирует.

## 3. Как работает

### Front Controller Pattern — обработка запроса

```
HTTP Request
    ↓
DispatcherServlet
    ↓
HandlerMapping        ← Какой контроллер обработает?
    ↓
HandlerAdapter        ← Как вызвать контроллер?
    ↓
@Controller / @RestController
    ↓ (Model + ViewName) или ResponseBody
ViewResolver          ← Найти шаблон по имени (для MVC с Views)
    ↓
View                  ← Отрендерить (Thymeleaf, JSP)
    ↓
HTTP Response
```

### HandlerMapping

`HandlerMapping` определяет какой контроллер обрабатывает запрос:

```java
@RestController
@RequestMapping("/api/orders")
public class OrderController {

    @GetMapping("/{id}")           // GET /api/orders/42
    public OrderDto getOrder(@PathVariable Long id) { ... }

    @PostMapping                   // POST /api/orders
    public OrderDto createOrder(@RequestBody CreateOrderRequest req) { ... }

    @PutMapping("/{id}")           // PUT /api/orders/42
    public OrderDto updateOrder(@PathVariable Long id,
                                 @RequestBody UpdateOrderRequest req) { ... }

    @DeleteMapping("/{id}")        // DELETE /api/orders/42
    public void deleteOrder(@PathVariable Long id) { ... }

    @GetMapping                    // GET /api/orders?status=active&page=0
    public Page<OrderDto> getOrders(
            @RequestParam(defaultValue = "active") String status,
            Pageable pageable) { ... }
}
```

### @Controller vs @RestController

| | `@Controller` | `@RestController` |
|---|---|---|
| **Состав** | `@Component` | `@Controller` + `@ResponseBody` |
| **Возвращает** | Имя View (строка) → ViewResolver | Объект → Jackson → JSON |
| **Применение** | Server-side rendering (Thymeleaf, JSP) | REST API |

```java
// @Controller — возвращает имя шаблона:
@Controller
public class PageController {
    @GetMapping("/dashboard")
    public String dashboard(Model model) {
        model.addAttribute("user", currentUser());
        return "dashboard";  // ViewResolver найдёт /templates/dashboard.html
    }
}

// @RestController — возвращает JSON:
@RestController
public class ApiController {
    @GetMapping("/api/users/{id}")
    public UserDto getUser(@PathVariable Long id) {
        return userService.findById(id);  // → ObjectMapper → JSON
    }
}
```

### Model, ModelMap, ModelAndView

Для server-side rendering:

```java
@Controller
public class ReportController {

    // Model — интерфейс, Spring передаёт реализацию:
    @GetMapping("/report")
    public String report(Model model) {
        model.addAttribute("data", reportService.getReport());
        return "report";  // view name
    }

    // ModelAndView — вместе view + данные:
    @GetMapping("/report2")
    public ModelAndView report2() {
        ModelAndView mav = new ModelAndView("report");
        mav.addObject("data", reportService.getReport());
        return mav;
    }
}
```

### Аннотации параметров методов

```java
@PostMapping("/orders/{id}/status")
public ResponseEntity<OrderDto> updateStatus(
        @PathVariable Long id,                           // из URI /orders/42/status
        @RequestParam String newStatus,                  // ?newStatus=active
        @RequestHeader("X-Request-Id") String requestId, // заголовок
        @RequestBody StatusUpdateRequest body,           // тело запроса (JSON)
        @Valid @ModelAttribute CreateForm form,          // HTML-форма
        HttpServletRequest rawRequest) {                 // сырой запрос

    return ResponseEntity.ok(orderService.updateStatus(id, newStatus));
}
```

### ResponseEntity

```java
@GetMapping("/{id}")
public ResponseEntity<OrderDto> getOrder(@PathVariable Long id) {
    return orderService.findById(id)
        .map(ResponseEntity::ok)                                  // 200 OK + body
        .orElse(ResponseEntity.notFound().build());              // 404 Not Found
}

@PostMapping
public ResponseEntity<OrderDto> createOrder(@RequestBody CreateOrderRequest req) {
    OrderDto created = orderService.create(req);
    URI location = URI.create("/api/orders/" + created.getId());
    return ResponseEntity.created(location).body(created);       // 201 Created
}
```

---

## 4. Глубже — что важно знать

**ViewResolver:** для @Controller-приложений Spring MVC ищет шаблон по имени. Например, `InternalResourceViewResolver` добавляет prefix `/WEB-INF/views/` и suffix `.jsp`. `ThymeleafViewResolver` ищет в `classpath:/templates/`.

**MessageConverter:** `@RestController` использует `HttpMessageConverter` для сериализации. `MappingJackson2HttpMessageConverter` — для JSON (Jackson). Если клиент шлёт `Accept: application/xml`, Spring выберет XML-конвертер (если есть).

**Exception handling:** необработанные исключения из контроллеров перехватывает `@ControllerAdvice` с `@ExceptionHandler`. Без него DispatcherServlet вернёт 500.

**`@RequestMapping` на уровне класса:** задаёт базовый путь; аннотации методов уточняют:

```java
@RestController
@RequestMapping("/api/v1/users")
public class UserController {
    @GetMapping("/{id}")  // /api/v1/users/{id}
    @PostMapping          // /api/v1/users
}
```

---

## 5. Связи с другими концепциями

- [[Spring Core IoC DI]] — все Controllers, Services, Repositories — Spring бины
- [[Filters Interceptors Listeners]] — Filters стоят до DispatcherServlet, Interceptors — после
- [[Spring Security]] — SecurityFilterChain перехватывает запросы до DispatcherServlet
- [[Глобальная обработка исключений в Spring]] — @ControllerAdvice перехватывает исключения после контроллера

## 6. Ответ на собесе (2 минуты)

> "Spring MVC реализует паттерн **Front Controller**: один `DispatcherServlet` принимает все HTTP-запросы. Поток обработки: DispatcherServlet → HandlerMapping (какой контроллер?) → HandlerAdapter (как вызвать?) → Controller → ViewResolver (для MVC с шаблонами).
>
> **@Controller vs @RestController:** @RestController = @Controller + @ResponseBody. @Controller возвращает имя View, которое ViewResolver превращает в HTML. @RestController возвращает объект, Jackson сериализует его в JSON.
>
> **Аннотации маппинга:** @GetMapping, @PostMapping, @PutMapping, @DeleteMapping — специализации @RequestMapping. Параметры метода: @PathVariable (из URI), @RequestParam (из query string), @RequestBody (тело запроса).
>
> **ResponseEntity** — полный контроль над ответом: статус, заголовки, тело. Используем когда нужен 201 Created с Location или 404 без тела.
>
> Spring Security (если подключён) стоит перед DispatcherServlet как цепочка фильтров."

## Шпаргалка

| Компонент | Роль | Ключевое |
|-----------|------|---------|
| **DispatcherServlet** | Front Controller | Один сервлет, все запросы |
| **HandlerMapping** | URL → Controller | `@RequestMapping` |
| **HandlerAdapter** | Вызов контроллера | `@PathVariable`, `@RequestBody` |
| **ViewResolver** | Имя → шаблон | Только для @Controller |
| **@Controller** | Server-side rendering | Возвращает имя View |
| **@RestController** | REST API | = @Controller + @ResponseBody → JSON |
| **ResponseEntity** | Полный контроль ответа | Статус + заголовки + тело |

| Аннотация параметра | Откуда берёт данные |
|--------------------|-------------------|
| `@PathVariable` | `/users/{id}` — из URI |
| `@RequestParam` | `?name=value` — query string |
| `@RequestBody` | JSON/XML тело запроса |
| `@RequestHeader` | HTTP-заголовок |
| `@ModelAttribute` | HTML-форма (multipart) |

**Связи:**
- [[Spring Core IoC DI]]
- [[Filters Interceptors Listeners]]
- [[Spring Security]]
- [[Глобальная обработка исключений в Spring]]
