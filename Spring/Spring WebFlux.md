---
tags: [spring, webflux, reactive, reactor, flux, mono]
sources: [Kata Spring Framework & HTTP.pdf]
---

# Spring WebFlux — реактивное программирование

## 1. Проблема — зачем это существует?

Классический Spring MVC — блокирующий: поток (thread) заблокирован пока ждёт ответа от БД, внешнего API, файловой системы. При 1000 одновременных запросов нужно 1000 потоков — дорого (1-2 MB памяти каждый, switching overhead). WebFlux решает это через **неблокирующий I/O**: один поток обслуживает сотни соединений, не блокируясь в ожидании.

## 2. Аналогия

**Блокирующая модель (MVC):** официант в ресторане берёт заказ, идёт на кухню, ждёт (блокируется) пока приготовят, несёт обратно. Один официант — один стол одновременно.

**Реактивная модель (WebFlux):** официант берёт заказ, оставляет кухне номерок, обслуживает следующий стол. Когда кухня готова — сигнализирует. Один официант — много столов параллельно.

## 3. Как работает

### Модели программирования

**Push vs Pull:**
- **Pull (императивный):** код запрашивает данные, ждёт (`userRepository.findById(id)` → блокировка)
- **Push (реактивный):** код подписывается на источник, данные приходят когда готовы — код реагирует

### Flux и Mono — два типа издателей

```
Mono<T>  — 0 или 1 элемент (как Optional, но асинхронный)
Flux<T>  — 0..N элементов (как Stream, но асинхронный)
```

```java
// Mono — один пользователь:
Mono<User> userMono = userRepository.findById(1L);

// Flux — список пользователей:
Flux<User> usersFlux = userRepository.findAll();

// Создание:
Mono.just("value")           // из значения
Mono.empty()                 // пустой
Mono.error(new RuntimeException("oops")) // с ошибкой
Flux.just(1, 2, 3)           // из нескольких значений
Flux.fromList(list)          // из коллекции
Flux.range(1, 10)            // диапазон чисел
```

### Операторы

```java
// map — синхронное преобразование:
Mono<UserDto> dto = userRepository.findById(1L)
    .map(user -> userMapper.toDto(user));

// flatMap — асинхронное преобразование (возвращает Publisher):
Mono<OrderDto> order = userRepository.findById(1L)
    .flatMap(user -> orderRepository.findByUserId(user.getId()))
    .map(orderMapper::toDto);

// filter:
Flux<User> active = userRepository.findAll()
    .filter(User::isActive);

// collectList — собрать Flux в Mono<List>:
Mono<List<User>> listMono = userRepository.findAll().collectList();

// zipWith — объединить два Publisher:
Mono<Pair<User, Profile>> combined = userMono
    .zipWith(profileMono)
    .map(tuple -> Pair.of(tuple.getT1(), tuple.getT2()));

// onErrorReturn — значение при ошибке:
Mono<User> safe = userRepository.findById(id)
    .onErrorReturn(User.anonymous());

// retry:
Mono<String> withRetry = httpClient.get()
    .retry(3);

// defaultIfEmpty:
Mono<User> orDefault = userRepository.findById(id)
    .defaultIfEmpty(User.guest());
```

### Backpressure

Backpressure — механизм управления потоком: потребитель (subscriber) сигнализирует издателю (publisher) сколько элементов он готов принять. Предотвращает переполнение.

```java
// Subscriber с backpressure:
Flux.range(1, 1000)
    .subscribe(new BaseSubscriber<Integer>() {
        @Override
        protected void hookOnSubscribe(Subscription subscription) {
            request(10); // запросить 10 элементов
        }

        @Override
        protected void hookOnNext(Integer value) {
            process(value);
            request(1); // запросить ещё один
        }
    });

// Стратегии при переполнении буфера:
Flux.range(1, 1000)
    .onBackpressureDrop()    // отбросить элементы которые не успели обработать
    .onBackpressureBuffer(100) // буферизировать до 100 элементов
    .onBackpressureError()   // бросить исключение при переполнении
```

### Реактивный контроллер (WebFlux)

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping("/{id}")
    public Mono<UserDto> getUser(@PathVariable Long id) {
        return userRepository.findById(id)
            .map(userMapper::toDto)
            .switchIfEmpty(Mono.error(new UserNotFoundException(id)));
    }

    @GetMapping
    public Flux<UserDto> getAllUsers() {
        return userRepository.findAll()
            .map(userMapper::toDto);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<UserDto> createUser(@RequestBody Mono<CreateUserRequest> request) {
        return request
            .flatMap(req -> userRepository.save(req.toUser()))
            .map(userMapper::toDto);
    }

    // Server-Sent Events — стриминг:
    @GetMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<UserDto> streamUsers() {
        return userRepository.findAll()
            .delayElements(Duration.ofSeconds(1)); // по одному в секунду
    }
}
```

### EventLoop и Netty

WebFlux по умолчанию использует **Netty** как embedded server (вместо Tomcat):

```
Netty EventLoop:
- Небольшой пул потоков (по умолчанию = количество CPU)
- Каждый поток — EventLoop: обрабатывает события (прочитать данные, записать ответ)
- Никакой блокировки в EventLoop-потоке!

Потоки: CPU * 2 (например, 8 CPU → 16 потоков)
Соединений: тысячи (неблокирующий I/O)
```

**Критическое правило:** **никогда не блокировать в реактивном pipeline!**

```java
// ПЛОХО — блокировка в EventLoop:
Mono<User> findUser(Long id) {
    User user = userRepository.findById(id).block(); // блокирует поток!
    return Mono.just(user);
}

// ХОРОШО — всё через reactive operators:
Mono<User> findUser(Long id) {
    return reactiveUserRepository.findById(id); // R2DBC, не JPA
}

// Если нужна блокирующая операция — перенести в отдельный scheduler:
Mono<Result> withBlocking = Mono.fromCallable(() -> blockingService.call())
    .subscribeOn(Schedulers.boundedElastic()); // пул для blocking IO
```

### WebFlux vs Spring MVC — когда что

| | Spring MVC | Spring WebFlux |
|---|---|---|
| **Модель** | Блокирующая (thread-per-request) | Неблокирующая (event loop) |
| **Потоки** | Много (Tomcat: 200 default) | Мало (Netty: CPU * 2) |
| **Пропускная способность** | Ограничена числом потоков | Высокая (I/O bound) |
| **Задержка** | Выше при большой нагрузке | Ниже при большой нагрузке |
| **БД** | JPA, JDBC | R2DBC (реактивный JDBC) |
| **Кривая обучения** | Пологая | Крутая |
| **Когда** | CRUD, умеренная нагрузка | Высокая I/O нагрузка, стриминг |

---

## 4. Глубже — что важно знать

**Холодный vs горячий Publisher:**
- **Cold** (по умолчанию): pipeline не выполняется без подписчика. Каждый subscriber получает все элементы с начала.
- **Hot**: Publisher работает независимо от подписчиков (WebSocket, SSE). Новые subscriber получают только новые элементы.

```java
// Сделать Hot из Cold:
Flux<String> cold = Flux.just("a", "b", "c");
ConnectableFlux<String> hot = cold.publish();
hot.connect(); // начать публикацию
```

**`block()` и `blockFirst()` — антипаттерн в веб-контексте.** Используй только в тестах или в `main()`. В EventLoop-потоке вызов `block()` → `BlockingOperationNotSupportedException`.

**R2DBC вместо JPA:** Spring WebFlux требует реактивного доступа к данным. JPA/Hibernate — блокирующие по природе, несовместимы с EventLoop. R2DBC — реактивный драйвер для реляционных БД.

```java
// ReactiveCrudRepository (Spring Data R2DBC):
public interface UserRepository extends ReactiveCrudRepository<User, Long> {
    Flux<User> findByActive(boolean active);
    Mono<User> findByEmail(String email);
}
```

---

## 5. Связи с другими концепциями

- [[Spring Boot]] — `spring-boot-starter-webflux` подключает WebFlux + Netty
- [[Spring MVC DispatcherServlet]] — альтернатива: WebFlux не использует DispatcherServlet (использует `DispatcherHandler`)
- [[Spring Data Repository]] — в WebFlux используется `ReactiveCrudRepository`, не `JpaRepository`

## 6. Ответ на собесе (2 минуты)

> "Spring WebFlux — реактивный стек Spring для неблокирующих приложений. Проблема MVC: каждый запрос занимает поток на время ожидания БД/сети — при 1000 запросах нужно 1000 потоков. WebFlux использует EventLoop: небольшой пул потоков (по CPU), каждый обрабатывает события без блокировки.
>
> **Два типа:** `Mono<T>` — 0 или 1 элемент. `Flux<T>` — 0..N элементов. Это реактивные `Publisher` (Project Reactor). Операции через операторы: `map` (синхронное), `flatMap` (асинхронное), `filter`, `zip`.
>
> **Backpressure:** потребитель контролирует скорость получения данных от издателя — предотвращает переполнение.
>
> **Когда WebFlux:** высокая I/O-нагрузка, стриминг (SSE, WebSocket), микросервисы с цепочкой внешних вызовов. Для обычного CRUD с умеренной нагрузкой — MVC проще и понятнее.
>
> **Главное правило:** никогда не блокировать EventLoop-поток. Если нужна блокирующая операция — Schedulers.boundedElastic()."

## Шпаргалка

| Концепция | Суть | Аналогия |
|-----------|------|---------|
| **Mono\<T\>** | 0 или 1 элемент | Async Optional |
| **Flux\<T\>** | 0..N элементов | Async Stream |
| **map** | Синхронное преобразование | T → R |
| **flatMap** | Async преобразование | T → Publisher\<R\> |
| **backpressure** | Потребитель управляет скоростью | Клапан |
| **EventLoop** | Один поток, много соединений | Официант с номерком |
| **Cold Publisher** | Не работает без подписчика | Видео по запросу |
| **Hot Publisher** | Работает независимо | Прямой эфир |
| **block()** | Антипаттерн в EventLoop | Блокирует поток |
| **R2DBC** | Реактивный JDBC | Вместо JPA в WebFlux |

**Связи:**
- [[Spring Boot]]
- [[Spring MVC DispatcherServlet]]
- [[Spring Data Repository]]
