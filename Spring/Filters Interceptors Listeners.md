---
tags: [spring, mvc, filter, interceptor, listener, web]
sources: [Kata Spring Framework & HTTP.pdf]
---

# Filters, Interceptors, Listeners

## 1. Проблема — зачем это существует?

Сквозная логика web-приложения — CORS, логирование, аутентификация, метрики — не должна дублироваться в каждом контроллере. Нужны точки перехвата запросов/ответов на разных уровнях стека. Spring предоставляет три механизма: Filters (Servlet-уровень), Interceptors (Spring MVC-уровень), Listeners (событийная модель). Каждый работает в своём месте и решает свои задачи.

## 2. Аналогия

Представь аэропорт:
- **Filter** — паспортный контроль на входе перед зданием. Проверяет каждого, кто входит/выходит. Не знает, куда летит пассажир.
- **Interceptor** — сотрудник у гейта. Знает рейс (какой контроллер), может пустить или задержать.
- **Listener** — диспетчер, который слушает системные события ("самолёт приземлился", "контекст запущен") и реагирует, не вмешиваясь в поток пассажиров.

## 3. Как работает

### Порядок выполнения

```
HTTP Request
    ↓
Filter 1 (pre)
Filter 2 (pre)
    ↓
DispatcherServlet
    ↓
Interceptor.preHandle()
    ↓
Controller method
    ↓
Interceptor.postHandle()    ← только при успешном ответе
    ↓
View rendering (если есть)
    ↓
Interceptor.afterCompletion() ← всегда, даже при исключении
    ↓
Filter 2 (post)
Filter 1 (post)
    ↓
HTTP Response
```

### Filter (javax.servlet.Filter / jakarta.servlet.Filter)

Работает на уровне Servlet-контейнера. Видит сырые `HttpServletRequest` / `HttpServletResponse`. Стоит **перед** `DispatcherServlet`.

```java
@Component  // или @WebFilter + @ServletComponentScan
@Order(1)   // порядок применения фильтров
public class LoggingFilter implements OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain)
            throws ServletException, IOException {

        String requestId = UUID.randomUUID().toString();
        MDC.put("requestId", requestId);

        long start = System.currentTimeMillis();
        try {
            filterChain.doFilter(request, response); // вызвать следующий фильтр/сервлет
        } finally {
            log.info("{} {} → {} ({}ms)",
                request.getMethod(), request.getRequestURI(),
                response.getStatus(), System.currentTimeMillis() - start);
            MDC.clear();
        }
    }
}
```

**`OncePerRequestFilter`** — гарантирует выполнение ровно один раз на запрос (даже при forward/include).

### Interceptor (HandlerInterceptor)

Работает внутри Spring MVC, после `DispatcherServlet`. Знает о `HandlerMethod` — какой метод контроллера вызывается.

```java
@Component
public class AuthInterceptor implements HandlerInterceptor {

    // Перед вызовом контроллера. false = прервать, не вызывать контроллер.
    @Override
    public boolean preHandle(HttpServletRequest request,
                             HttpServletResponse response,
                             Object handler) throws Exception {
        if (handler instanceof HandlerMethod method) {
            // Можно проверить аннотации метода:
            if (method.hasMethodAnnotation(RequiresAdmin.class)
                    && !currentUser().isAdmin()) {
                response.sendError(403, "Forbidden");
                return false;
            }
        }
        return true;
    }

    // После выполнения контроллера, до рендеринга View (только при успехе)
    @Override
    public void postHandle(HttpServletRequest request,
                           HttpServletResponse response,
                           Object handler,
                           ModelAndView modelAndView) throws Exception {
        if (modelAndView != null) {
            modelAndView.addObject("serverTime", LocalDateTime.now());
        }
    }

    // Всегда — после рендеринга (даже если было исключение)
    @Override
    public void afterCompletion(HttpServletRequest request,
                                HttpServletResponse response,
                                Object handler,
                                Exception ex) throws Exception {
        log.info("Request completed: {}", request.getRequestURI());
    }
}
```

**Регистрация Interceptor:**

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(authInterceptor)
                .addPathPatterns("/api/**")
                .excludePathPatterns("/api/public/**");
    }
}
```

### Listener (ApplicationListener)

Реагирует на события жизненного цикла Spring-контекста или кастомные бизнес-события. Не привязан к HTTP-запросам.

```java
// Слушатель событий контекста:
@Component
public class AppStartupListener implements ApplicationListener<ApplicationReadyEvent> {

    @Override
    public void onApplicationEvent(ApplicationReadyEvent event) {
        log.info("Application started — initializing caches...");
        cacheService.warmUp();
    }
}

// Кастомные события через ApplicationEventPublisher:
@Service
public class OrderService {

    @Autowired
    private ApplicationEventPublisher eventPublisher;

    public void createOrder(OrderDto dto) {
        Order order = orderRepository.save(dto.toOrder());
        eventPublisher.publishEvent(new OrderCreatedEvent(order)); // публикация события
    }
}

@Component
public class NotificationListener {

    @EventListener  // или implements ApplicationListener<OrderCreatedEvent>
    public void onOrderCreated(OrderCreatedEvent event) {
        notificationService.send(event.getOrder());
    }
}
```

**Стандартные события контекста:**

| Событие | Когда |
|---------|-------|
| `ContextRefreshedEvent` | Контекст инициализирован / обновлён |
| `ApplicationReadyEvent` | Приложение полностью готово к запросам |
| `ContextClosedEvent` | Контекст закрывается |
| `ApplicationFailedEvent` | Запуск провалился |

---

## 4. Глубже — что важно знать

**Filter vs Interceptor — главные отличия:**

| | Filter | Interceptor |
|---|---|---|
| **Уровень** | Servlet Container | Spring MVC |
| **Знает о Spring** | Нет (без Spring-бинов по умолчанию) | Да (полный доступ к Spring context) |
| **Знает контроллер** | Нет | Да (`HandlerMethod`) |
| **Применение** | CORS, логирование, JWT-разбор, gzip | Аутентификация на уровне MVC, добавление атрибутов в Model |
| **Исключения** | Обрабатывает сам | Обрабатывает Spring (@ControllerAdvice) |

**Когда что использовать:**
- **Filter** — когда нужно перехватить **до** Spring (Spring Security, CORS preflight, request-id добавление)
- **Interceptor** — когда нужен доступ к аннотациям контроллера или ModelAndView
- **Listener** — когда реагируешь на события, не HTTP-запросы (прогрев кэша при старте, async-нотификации)

**Spring Security — это тоже Filter:** `DelegatingFilterProxy` → `FilterChainProxy` → `SecurityFilterChain`. Именно поэтому Security работает до Interceptors.

---

## 5. Связи с другими концепциями

- [[Spring MVC DispatcherServlet]] — Filters до DispatcherServlet, Interceptors внутри
- [[Spring Security]] — SecurityFilterChain — цепочка Filters перед DispatcherServlet
- [[Spring AOP]] — Interceptors реализованы через AOP-механизмы Spring MVC

## 6. Ответ на собесе (2 минуты)

> "Три уровня перехвата в Spring.
>
> **Filter** — Servlet-уровень, стоит до DispatcherServlet. Видит сырые HttpServletRequest/Response. Не знает о Spring-бинах или контроллерах. Применяется для CORS, логирования, JWT-парсинга, rate limiting.
>
> **Interceptor** — Spring MVC-уровень, после DispatcherServlet. Три метода: preHandle (до контроллера, может вернуть false и прервать), postHandle (после контроллера, до рендеринга View), afterCompletion (всегда, даже при исключении). Знает HandlerMethod — может проверить аннотации метода. Применяется для авторизации на уровне аннотаций, добавления атрибутов в Model.
>
> **Listener** — событийная модель. Реагирует на события контекста (ApplicationReadyEvent) или кастомные бизнес-события через ApplicationEventPublisher. Не привязан к HTTP.
>
> **Порядок:** Filter → DispatcherServlet → Interceptor.preHandle → Controller → Interceptor.postHandle → Interceptor.afterCompletion → Filter."

## Шпаргалка

| | Filter | Interceptor | Listener |
|---|---|---|---|
| Уровень | Servlet | Spring MVC | Spring Context |
| Место | До DispatcherServlet | Вокруг Controller | Вне HTTP |
| Знает контроллер | Нет | Да | N/A |
| Применение | CORS, JWT, logging | MVC-авторизация, Model | Startup, события |
| Интерфейс | `OncePerRequestFilter` | `HandlerInterceptor` | `@EventListener` |

**Связи:**
- [[Spring MVC DispatcherServlet]]
- [[Spring Security]]
- [[Spring AOP]]
