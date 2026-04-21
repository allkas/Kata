---
tags: [index, system]
---

# Index — Мастер-каталог wiki

*Обновляется при каждом ingest. Читается в начале каждого сеанса для навигации.*

---

## Java Core

| Страница                             | Описание                                                                                          |
| ------------------------------------ | ------------------------------------------------------------------------------------------------- |
| [[Основы ООП]]                       | Инкапсуляция, наследование, полиморфизм, абстракция; override vs hide                             |
| [[Интерфейс vs абстрактный класс]]   | Сравнение, default-методы, когда что выбирать                                                     |
| [[Принципы SOLID]]                   | 5 принципов проектирования кода с примерами нарушений                                             |
| [[Контракт equals и hashCode]]       | Правила переопределения, связь с коллекциями                                                      |
| [[Иммутабельность String]]           | Почему String неизменяем, String Pool, StringBuilder                                              |
| [[Исключения в Java]]                | Checked vs unchecked, иерархия, best practices                                                    |
| [[final static внутренние классы]]   | Модификаторы, вложенные классы, анонимные классы                                                  |
| [[Generics]]                         | Дженерики, wildcards, PECS, type erasure                                                          |
| [[Устройство HashMap]]               | Бакеты, коллизии, load factor, дерево; HashMap vs TreeMap vs LinkedHashMap; Set-коллекции         |
| [[ArrayList vs LinkedList]]          | Структуры, Big O, расширение capacity, когда что выбирать                                         |
| [[Stream API]]                       | map/flatMap, functional interfaces, Optional, lazy evaluation                                     |
| [[Многопоточность основы]]           | Thread lifecycle, volatile/synchronized/Atomic, deadlock/livelock/starvation, Monitor, wait/notify, Semaphore, Daemon, interrupt |
| [[CompletableFuture и пулы потоков]] | CompletableFuture цепочки, ExecutorService, ForkJoinPool                                          |
| [[java.util.concurrent]]             | ConcurrentHashMap, CopyOnWriteArrayList, BlockingQueue, ReentrantLock, ReadWriteLock, CountDownLatch, CyclicBarrier, Phaser, Exchanger |
| [[Паттерны проектирования]]          | GoF: Singleton, Builder, Factory, Strategy, Observer, Decorator, Proxy                            |
| [[Алгоритмы на собесе]]              | Live coding: HashMap-задачи, два указателя, рекурсия, Big O                                       |
| [[Garbage Collector JVM]]            | GC-алгоритмы, поколения, паузы                                                                    |
| [[JVM устройство ClassLoader]]       | JDK/JRE/JVM иерархия, байткод, ClassLoader типы и принципы, JIT                                  |
| [[Stack vs Heap память]]             | Сравнение областей памяти, фреймы вызовов, ошибки OOM/SOE, Metaspace                             |
| [[Примитивные типы и обёртки]]       | 8 типов, autoboxing, Integer pool -128..127, widening/narrowing casting                            |
| [[Сериализация в Java]]              | Serializable, transient, serialVersionUID, Externalizable, shallow/deep clone                     |
| [[Отличия Java 8 и Java 11]]         | var, HTTP Client, String API, Collection.of(), модули                                             |

---

## Spring

| Страница | Описание |
|----------|----------|
| [[Spring Core IoC DI]] | Inversion of Control, Dependency Injection, BeanFactory, ApplicationContext, BeanPostProcessor |
| [[Жизненный цикл Spring бина]] | 6 шагов lifecycle, Aware-интерфейсы, @PostConstruct/@PreDestroy, scopes |
| [[Spring Boot]] | Auto-configuration, starters, embedded server, @SpringBootApplication |
| [[Spring AOP]] | Aspect-oriented programming, JDK Proxy vs CGLIB, self-invocation ловушка |
| [[Spring MVC DispatcherServlet]] | Front Controller, обработка запросов, HandlerMapping, @Controller vs @RestController |
| [[Filters Interceptors Listeners]] | Servlet-фильтры, Spring Interceptors, ApplicationEventPublisher, порядок выполнения |
| [[@Transactional и Propagation]] | Propagation levels (REQUIRED/REQUIRES_NEW/NESTED/...), rollback, physical vs logical |
| [[Spring Security]] | Filter chain, аутентификация, UserDetailsService, SecurityContextHolder, JWT |
| [[Spring Data Repository]] | Repository иерархия, @Query, метод по именованию, Pageable |
| [[Spring WebFlux]] | Реактивное программирование, Flux/Mono, backpressure, EventLoop, R2DBC |
| [[Spring MVC REST (Controller vs RestController)]] | Разница аннотаций, обработка запросов |
| [[Глобальная обработка исключений в Spring]] | @ControllerAdvice, @ExceptionHandler |

---

## Базы данных

| Страница | Описание |
|----------|----------|
| [[Транзакции уровни изоляции]] | ACID детально, dirty/non-repeatable/phantom read, уровни изоляции, @Transactional propagation, MVCC |
| [[Проблема N+1 запросов]] | N+1 механика, LAZY vs EAGER дефолты, LazyInitializationException, JOIN FETCH vs JOIN, @EntityGraph, @BatchSize |
| [[SQL индексы JOIN нормализация]] | B-tree механика, composite index, когда индекс вреден, JOINs, WHERE vs HAVING, 1NF/2NF/3NF, EXPLAIN |
| [[PostgreSQL vs MySQL]] | Сравнение, JSONB, расширения, когда что выбирать |
| [[Хранение паролей хеширование шифрование]] | BCrypt, соль, атаки, шифрование vs хеширование |

---

## Микросервисы и архитектура

| Страница | Описание |
|----------|----------|
| [[Микросервисы vs монолит]] | Сравнение, когда что выбрать |
| [[Декомпозиция монолита]] | Стратегии разбиения по доменам |
| [[Service Discovery Config Server]] | Eureka, Config Server, динамическая конфигурация |
| [[Circuit Breaker]] | Паттерн отказоустойчивости, Resilience4J, состояния |
| [[Распределённые транзакции саги]] | Saga pattern, choreography vs orchestration |
| [[Highload проблемы]] | Масштабирование, кэши, bottleneck |
| [[Асинхронное и сихронное взаимодействие]] | REST vs очереди, temporal coupling, буферизация пиков |
| [[WebSocket]] | Двустороннее соединение, STOMP, SSE, масштабирование |
| [[Distributed Tracing Zipkin Jaeger]] | Trace/Span, Zipkin vs Jaeger, sampling, observability |
| [[SOAP vs REST]] | SOAP/WSDL vs REST, JSON-RPC, gRPC сравнение |

---

## Kafka и брокеры сообщений

| Страница | Описание |
|----------|----------|
| [[Брокеры сообщений]] | Общая концепция, зачем нужны |
| [[Kafka топики, партиции, офсеты, брокеры, consumer group]] | Внутреннее устройство Kafka |
| [[Как распределяются сообщения по партициям, гарантии доставки]] | Partitioning key, at-least-once/exactly-once |
| [[Чем Kafka отличается от RabbitMQ, ActiveMQ]] | Сравнение брокеров |

---

## HTTP и REST

| Страница | Описание |
|----------|----------|
| [[Разница HTTP методов]] | GET/POST/PUT/PATCH/DELETE |
| [[PUT vs PATCH, идемпотентность HTTP-методов]] | Идемпотентность, семантика методов |
| [[Какой статус возвращать при валидации, бизнес конфликте]] | HTTP status codes: 400/409/422/404 |

---

## Тестирование (Mockito)

| Страница | Описание |
|----------|----------|
| [[Unit-тесты Mockito]] | Основы написания тестов с Mockito |
| [[Чем Mock отличается от Spy (Mockito)]] | Mock vs Spy, частичное мокирование |
| [[@Mock, @InjectMocks, @Spy — разница]] | Аннотации Mockito |
| [[Как проверить, что метод вызывался (verify)]] | verify(), times(), never() |
| [[Как тестировать void методы в Mockito]] | doNothing, doThrow, ArgumentCaptor |

---

## Инфраструктура — Docker / Kubernetes

| Страница | Описание |
|----------|----------|
| [[Docker vs VM]] | Контейнер vs виртуальная машина |
| [[Dockerfile и слои образа]] | Инструкции, multi-stage build, кэширование слоёв |
| [[Kubernetes pod deployment service]] | Pod, Deployment, Service — базовые объекты |

---

## Инфраструктура — Maven

| Страница | Описание |
|----------|----------|
| [[Жизненный цикл Maven]] | Фазы: compile, test, package, install, deploy |
| [[Dependency management]] | Транзитивные зависимости, конфликты, exclusions |
| [[Профили Maven]] | Настройка под окружения |

---

## Инфраструктура — Git

| Страница | Описание |
|----------|----------|
| [[Git merge vs rebase]] | Линейная vs историческая история, когда что |
| [[Git fetch vs pull]] | Безопасное обновление репозитория |
| [[Git cherry-pick]] | Перенос отдельных коммитов |
| [[CI CD GitLab Jenkins]] | Пайплайны, GitLab CI YAML vs Jenkinsfile |

---

## Подготовка к собеседованию — поведенческое

| Страница | Описание |
|----------|----------|
| [[Вопросы работодателю — что сделать, чтобы вы не пожалели]] | Что спросить интервьюеру в конце собеседования; вопрос про ожидания через год |

---

## Системные файлы

| Файл | Описание |
|------|----------|
| `CLAUDE.md` | Схема wiki, воркфлоу, конвенции |
| `index.md` | Этот файл — мастер-каталог |
| `log.md` | Хронологический лог изменений |
| `raw/` | Исходные документы (только чтение) |
