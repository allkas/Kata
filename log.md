# Log — Хронологический журнал изменений

---

## [2026-04-21] ingest | Паттерны проектирования (2.pdf)

**Источник:** `2.pdf` (GoF Design Patterns, антипаттерны, 60 страниц)

**Обновлены страницы:**
- `JAVA core/Паттерны проектирования` — добавлены: Adapter, Facade, Template Method, Chain of Responsibility; расширены таблицы "паттерны в Spring", шпаргалка, раздел "Частые ошибки"

**Созданы новые страницы:**
- `JAVA core/Антипаттерны` — God Object, Big Ball of Mud, Poltergeists, Singleton-антипаттерн, Introduced Complexity, Anemic Domain Model

**Обновлены:**
- `index.md` — обновлена строка Паттерны проектирования; добавлена Антипаттерны
- `1 Java Core MOC.md` — добавлена Антипаттерны

---

## [2026-04-21] ingest | Алгоритмы (1.pdf)

**Источник:** `1.pdf` (Kata academy, 22 страницы — 14 тем по алгоритмам и структурам данных)

**Созданы новые страницы:**
- `JAVA core/Виды сортировок` — Bubble/Insertion/Selection/Shell/Merge/Quick/Heap/Counting/Timsort; Big O таблица; Arrays.sort() в Java (Dual-Pivot Quicksort vs Timsort)
- `JAVA core/Бинарное дерево и красно-чёрное дерево` — BST инвариант, три вида обхода, BFS; 5 правил RB-tree; TreeMap/TreeSet/HashMap-бакеты
- `JAVA core/Queue Deque Stack PriorityQueue` — Queue/Deque/Stack/PriorityQueue/EnumSet; ArrayDeque vs LinkedList; offer/poll/peek vs add/remove; Top-K паттерн
- `JAVA core/Рекурсия и мемоизация` — базовый случай и шаг рекурсии, рекурсия vs итерация, мемоизация (top-down DP), bottom-up DP, жадный алгоритм

**Обновлены:**
- `index.md` — добавлены 4 новые страницы в Java Core
- `1 Java Core MOC.md` — добавлены разделы "Структуры данных" и расширен "Паттерны и алгоритмы"

---

## [2026-04-21] ingest | Spring Framework & HTTP (4.pdf)

**Источник:** `4.pdf` (Kata academy, 89 страниц — Spring Core, AOP, MVC, Security, Boot, Data, WebFlux, HTTP/REST)

**Созданы новые страницы:**
- `Spring/@Transactional и Propagation` — 7 уровней propagation, physical vs logical транзакции, rollback rules, self-invocation ловушка
- `Spring/Spring MVC DispatcherServlet` — Front Controller pattern, поток обработки запроса, HandlerMapping, @Controller vs @RestController, ResponseEntity
- `Spring/Filters Interceptors Listeners` — три уровня перехвата, порядок выполнения, OncePerRequestFilter, HandlerInterceptor, ApplicationEventPublisher
- `Spring/Spring Data Repository` — иерархия интерфейсов, метод по именованию, @Query, Pageable, save() поведение
- `Spring/Spring WebFlux` — Mono/Flux, операторы, backpressure, EventLoop/Netty, R2DBC, холодный vs горячий Publisher

**Добавлены в index.md и MOC (существовали, но не были учтены):**
- `Spring/Жизненный цикл Spring бина`
- `Spring/Spring Security`

**Обновлены:**
- `index.md` — добавлены все 7 страниц в раздел Spring
- `3 Spring MOC.md` — структурирован по разделам: Ядро, Транзакции и AOP, Web-слой, Security/Data/Boot, Реактивное

---

## [2026-04-20] ingest | Kata 32 вопроса по многопоточности (Java Multithreading)

**Источник:** `3.pdf` (Kata academy, 58 страниц, 32 вопроса)

**Обновлены существующие страницы:**
- `JAVA core/Многопоточность основы` — кардинально расширена: Thread lifecycle (6 состояний + диаграмма), Process vs Thread, Monitor/mutex (synchronized static vs non-static), wait/notify/notifyAll + Producer-Consumer pattern, Semaphore, Starvation, Data Race vs Race Condition, 4 условия Coffman для deadlock, Daemon-потоки, Thread priority, join/sleep/yield/interrupt сравнение, interrupt() vs stop(), FutureTask

**Созданы новые страницы:**
- `JAVA core/java.util.concurrent` — ConcurrentHashMap (Java 7 vs 8), CopyOnWriteArrayList, BlockingQueue (4 реализации), ReentrantLock vs synchronized, ReadWriteLock, Condition, CountDownLatch, CyclicBarrier, Phaser, Exchanger, таблица выбора инструментов

---

## [2026-04-20] ingest | CORE-2 Вопросы технических собеседований (Generics, Collections, Stream API, Java 8)

**Источник:** `методички по java/Сore-2.docx`

**Обновлены существующие страницы:**
- `JAVA core/Generics` — добавлены: raw types, diamond operator, инвариантность дженериков vs ковариантность массивов (`ArrayStoreException`), generics в исключениях (что можно/нельзя)
- `JAVA core/ArrayList vs LinkedList` — добавлены: fail-fast/fail-safe итераторы, `ConcurrentModificationException`, способы безопасного удаления при итерации, Iterator vs Enumeration, Comparable vs Comparator
- `JAVA core/Устройство HashMap` — добавлены: Collection vs Collections, WeakHashMap + 4 типа ссылок (Strong/Soft/Weak/Phantom), почему byte[] нельзя использовать как ключ, вырождение в список при одинаковых hashCode
- `JAVA core/Stream API` — добавлены: parallel streams с предупреждением о ForkJoinPool.commonPool(), IntStream/LongStream/DoubleStream (без autoboxing), Collectors детально (groupingBy, partitioningBy, joining, summarizingInt)
- `JAVA core/Отличия Java 8 и Java 11` — добавлен полный раздел Date/Time API: LocalDate/LocalTime/LocalDateTime/ZonedDateTime, Period/Duration, DateTimeFormatter

---

## [2026-04-20] ingest | CORE-1 Вопросы технических собеседований (ООП, Java internals, примитивы, сериализация)

**Источник:** `raw/CORE 1 Вопросы технических собеседований.pdf`

**Созданы новые страницы:**
- `JAVA core/Примитивные типы и обёртки` — 8 типов, autoboxing, Integer Pool [-128..127], widening/narrowing, BigDecimal
- `JAVA core/JVM устройство ClassLoader` — JDK/JRE/JVM иерархия, байткод, ClassLoader (Bootstrap/Extension/System), 3 принципа, JIT, dynamic loading
- `JAVA core/Stack vs Heap память` — фреймы вызовов, сравнение областей памяти, StackOverflowError vs OOM, Metaspace, escape analysis
- `JAVA core/Сериализация в Java` — Serializable, transient, serialVersionUID, Externalizable, shallow/deep clone, copy constructor

**Обновлены существующие страницы:**
- `JAVA core/Основы ООП` — добавлены: ассоциация/агрегация/композиция, принципы DRY/KISS/YAGNI
- `JAVA core/Контракт equals и hashCode` — добавлены: почему множитель 31, getClass() vs instanceof
- `JAVA core/Исключения в Java` — добавлены: ExceptionInInitializerError в static-блоках, детали suppressed exceptions
- `JAVA core/final static внутренние классы` — добавлены: sealed classes (Java 15+), Enum API (name/ordinal/values), типы конструкторов, порядок инициализации

---

## [2026-04-16] lint | Проверка всех файлов на наличие раздела "Ответ на собесе"

**Проверено:** 68 файлов wiki.

**Исправлены (переименован раздел "Закрытие" → "Ответ на собесе"):**
- `Микросервисы/Circuit Breaker` — раздел 6 был "Закрытие", переименован
- `Микросервисы/Декомпозиция монолита` — раздел 6 был "Закрытие", переименован
- `Микросервисы/Highload проблемы` — раздел 6 был "Закрытие", переименован

**Переписаны в полный Justin Song формат:**
- `Микросервисы/Брокеры сообщений` — был короткий stub (5 строк), полный rewrite: все 6 разделов + шпаргалка
- `Микросервисы/Чем Kafka отличается от RabbitMQ, ActiveMQ` — был в старом emoji/callout формате, полный rewrite в Justin Song

**Добавлен раздел "Ответ на собесе" (устаревшие Devops/ stubs):**
- `Devops/Maven жизненный цикл` — добавлена секция с ответом + ссылки на ИНФРАСТУКТУРА/
- `Devops/Git merge rebase` — добавлена секция с ответом + ссылки на ИНФРАСТУКТУРА/
- `Devops/Docker Kubernetes` — добавлена секция с ответом + ссылки на ИНФРАСТУКТУРА/

**Создана новая страница:**
- `Вопросы работодателю — что сделать, чтобы вы не пожалели` — как задать вопрос интервьюеру про ожидания через год

**Обновлены системные файлы:** `index.md`, `log.md`

---

*Формат записей: `## [YYYY-MM-DD] <тип> | <описание>`*
*Типы: `ingest` | `query` | `lint` | `setup`*

---

## [2026-04-14] ingest | Прочие_Реже встречающиеся вопросы технических собеседований.pdf

Источник: методичка Kata-курсов, редкие вопросы (все с freq 2/150 — ниже порога «сомнительной ценности» по самому PDF).

**Статистика из источника (все freq 2):**
- JSON-RPC, WebSocket, SOAP vs REST, Синхронное/асинхронное взаимодействие
- Паттерн Saga, Distributed Tracing (Zipkin/Jaeger)
- CI/CD (GitLab, Jenkins), Хранение паролей, PostgreSQL vs MySQL
- Разница == и equals, Отличия Java 8 и Java 11

**Переписаны в полный Justin Song формат (были в старом quote-блочном стиле):**
- `Микросервисы/Распределённые транзакции саги` — механика Saga, хореография vs оркестрация, идемпотентность шагов, eventual consistency, Camunda/Axon
- `Микросервисы/Асинхронное и сихронное взаимодействие` — temporal coupling, буферизация пиков, decoupling, Dead Letter Queue, когда оставлять sync

**Созданы новые страницы:**
- `Микросервисы/WebSocket` — handshake, STOMP в Spring, SSE как альтернатива, масштабирование через Redis Pub/Sub
- `Микросервисы/Distributed Tracing Zipkin Jaeger` — Trace/Span/TraceID, propagation headers, Zipkin vs Jaeger, sampling в prod, корреляция с логами (MDC)
- `Микросервисы/SOAP vs REST` — XML/WSDL vs JSON/OpenAPI, WS-Security, JSON-RPC поверх HTTP, gRPC как современная альтернатива SOAP
- `ИНФРАСТУКТУРА/CI CD GitLab Jenkins` — CI vs CD vs Continuous Deployment, `.gitlab-ci.yml` vs Jenkinsfile, stages/artifacts/cache, secrets, `when: manual` для prod
- `БД/Хранение паролей хеширование шифрование` — BCrypt (cost factor, встроенная соль), Argon2, атаки (rainbow table, brute force), шифрование vs хеширование vs кодирование, pepper
- `БД/PostgreSQL vs MySQL` — JSONB, PostGIS, расширения, VACUUM, когда что выбирать, Oracle для enterprise
- `JAVA core/Отличия Java 8 и Java 11` — var, HTTP Client, String API (isBlank/strip/lines/repeat), Collection.of(), модули, удалён JAXB/JAX-WS

**Уже покрыто (страницы существуют):**
- `== и equals` → `Контракт equals и hashCode` (JAVA core)

---

## [2026-04-14] ingest | DevOps И ИНФРАСТУКТУРА Вопросы технических собеседований.pdf

Источник: методичка Kata-курсов, темы: Git, Maven, Docker, Kubernetes.

**Статистика из источника (150 собеседований):**
- Git merge vs rebase — freq 18
- Жизненный цикл Maven — freq 15
- Git fetch vs pull — freq 12
- Dependency management — freq 10
- Docker vs VM — freq 10
- Dockerfile — freq 8
- Профили Maven — freq 8
- Kubernetes pod/deployment/service — freq 5
- Git cherry-pick — freq 5

**Страницы уже в полном Justin Song формате (проверены, изменений не потребовали):**
- `ИНФРАСТУКТУРА/Git merge vs rebase` — golden rule, squash, interactive rebase
- `ИНФРАСТУКТУРА/Жизненный цикл Maven` — все фазы, dependency management, scope, profiles
- `ИНФРАСТУКТУРА/Docker vs VM` — namespace/cgroups, layer caching, multi-stage build
- `ИНФРАСТУКТУРА/Git fetch vs pull` — безопасный workflow, detached HEAD

**Переписаны в полный Justin Song формат (были в старом emoji/callout стиле):**
- `ИНФРАСТУКТУРА/Dockerfile и слои образа` — freq 8 — слоевая модель, кэш инструкций, CMD vs ENTRYPOINT (exec form vs shell form), multi-stage сборка Maven→JRE, .dockerignore, non-root user
- `ИНФРАСТУКТУРА/Kubernetes pod deployment service` — freq 5 — Pod/Deployment/Service YAML, Rolling Update, readiness vs liveness probe, ConfigMap/Secret, аналогия с Service Discovery
- `ИНФРАСТУКТУРА/Git cherry-pick` — freq 5 — диапазон коммитов, cherry-pick vs merge vs rebase таблица, новый хэш при переносе, проблема дублей при последующем merge
- `ИНФРАСТУКТУРА/Dependency management` — freq 10 — nearest wins / first declared wins, `<dependencyManagement>`, BOM, exclusions, `mvn dependency:tree`
- `ИНФРАСТУКТУРА/Профили Maven` — freq 8 — активация по CLI/условию/ОС/JDK, filtering ресурсов, Maven profiles vs Spring profiles, settings.xml

---

## [2026-04-14] ingest | Тестирование Вопросы технических собеседований.pdf

Источник: методичка Kata-курсов, тема: Unit-тесты и Mockito.

**Статистика из источника (150 собеседований):**
- Чем Mock отличается от Spy — freq 10
- Как проверить, что метод вызывался (verify) — freq 5
- @Mock, @InjectMocks, @Spy — разница — freq 5
- Как тестировать void методы в Mockito — freq 2

**Все 4 страницы уже существовали с отличным контентом, но в нестандартном формате (> quote-блоки, без разделов 1–6, "Закрытие" вместо "Ответ на собесе").**

**Переписаны в полный Justin Song формат:**
- `Микросервисы/Чем Mock отличается от Spy (Mockito)` — freq 10 — критичный нюанс `when()` vs `doReturn()` для Spy, правило предпочесть Mock
- `Микросервисы/@Mock, @InjectMocks, @Spy — разница` — freq 5 — порядок внедрения InjectMocks, ловушки (без `new` для Spy, зависимость через `new` в методе)
- `Микросервисы/Как проверить, что метод вызывался (verify)` — freq 5 — полный синтаксис, ArgumentCaptor, InOrder для саг, state vs behavior verification
- `Микросервисы/Как тестировать void методы в Mockito` — freq 2 — три подхода, doX()-синтаксис, таблица когда что

---

## [2026-04-14] ingest | Архитектура и микросервисы Вопросы технических собеседований.pdf

Источник: методичка Kata-курсов, темы: микросервисы, Kafka, HTTP-методы.

**Статистика из источника (150 собеседований):**
- Микросервисы vs монолит — freq 16
- HTTP-методы: GET vs POST — freq 15
- Kafka: топики, партиции, офсеты, consumer group — freq 14
- PUT vs PATCH, идемпотентность — freq 12
- Как распределяются сообщения, гарантии доставки — freq 10
- Service Discovery / Config Server — freq 8
- Какой статус при валидации (400/409/422) — freq 8
- Circuit Breaker — freq 6 (страница уже в хорошем формате)
- Распределённые транзакции, саги — freq 5 (страница уже в хорошем формате)

**Все страницы уже существовали, но были в старом формате (emoji + callouts, без Justin Song разделов).**

**Переписаны в полный Justin Song формат (разделы 1–6 + шпаргалка):**
- `Микросервисы/Микросервисы vs монолит` — freq 16 — Strangler Pattern, модульный монолит, таблица trade-offs
- `Микросервисы/Разница HTTP методов` — freq 15 — полная таблица 7 методов, почему POST для чувствительных данных, HTTPS не спасает
- `Микросервисы/Kafka топики, партиции, офсеты, брокеры, consumer group` — freq 14 — почему append-only лог, Rebalancing, Retention policy
- `Микросервисы/PUT vs PATCH, идемпотентность HTTP-методов` — freq 12 — JSON Merge Patch vs JSON Patch, таблица когда что
- `Микросервисы/Как распределяются сообщения по партициям, гарантии доставки` — freq 10 — acks=0/1/all, ISR, idempotent producer, транзакции
- `Микросервисы/Какой статус возвращать при валидации, бизнес конфликте` — freq 8 — decision tree, retry-логика, RFC 7807
- `Микросервисы/Service Discovery Config Server` — freq 8 — лёгкий рефакторинг: добавлены разделы 1-6, self-preservation mode, Kubernetes аналоги

---

## [2026-04-14] ingest | Алгоритмы и паттерны Вопросы технических собеседований.pdf

Источник: методичка Kata-курсов, темы: алгоритмические задачи на live coding, паттерны проектирования.

**Статистика из источника (150 собеседований):**
- Найти первый неповторяющийся элемент — freq 6
- Факториал / Фибоначчи, оценка сложности — freq 5
- Вывести элементы, повторяющиеся N раз — freq 4
- Палиндром — freq 3
- Сортировка квадратов массива — freq 3
- Абстрактная фабрика vs фабричный метод — freq 2

**Созданы новые страницы (полный Justin Song формат):**
- `JAVA core/Паттерны проектирования` — GoF классификация, Singleton (DCL + enum), Builder, Factory Method, Abstract Factory, Decorator, Proxy, Strategy, Observer; паттерны в Spring
- `JAVA core/Алгоритмы на собесе` — 5 задач с кодом и Big O, таблица паттернов решения, советы по поведению на live coding
- `JAVA core/CompletableFuture и пулы потоков` — закрытие старого пробела: цепочки (thenApply/thenCompose/allOf), обработка ошибок, ExecutorService, ForkJoinPool, подбор размера пула

**Дополнительно:**
- Удалён пустой stub `PUT vs PATCH — идемпотентность HTTP-методов.md` из корня (дубль, реальная страница в `Микросервисы/`)
- Обновлены системные файлы: `index.md`, `1 Java Core MOC.md`

---

## [2026-04-13] ingest | Вопросы технических собеседований (1).pdf — мастер-список

Источник: общий мастер-список всех вопросов с частотами (150 собеседований, 29 тем).

**Действие: gap-анализ и заполнение пробелов**

Сравнён мастер-список со всеми существующими страницами wiki. Выявлены страницы-стабы и проведён полный Justin Song rewrite:

**Переписаны стабы (были 5–10 строк):**
- `JAVA core/final static внутренние классы` — freq 12/9/5 — final vs static, static nested, inner, anonymous, Builder pattern
- `Микросервисы/Unit-тесты Mockito` — обзорная страница со всей механикой (@Mock/@Spy/@InjectMocks, when/verify, void, ArgumentCaptor), ссылки на детальные страницы
- `ИНФРАСТУКТУРА/Git merge vs rebase` — freq 18 — механика merge/rebase, золотое правило, стратегии команд
- `ИНФРАСТУКТУРА/Git fetch vs pull` — freq 12 — fetch vs pull, безопасный workflow
- `ИНФРАСТУКТУРА/Жизненный цикл Maven` — freq 15 — фазы, dependency management, scope, профили
- `ИНФРАСТУКТУРА/Docker vs VM` — freq 10 — namespace/cgroups, Dockerfile слои, multi-stage build

**Завершён ingest Spring PDF (начат в предыдущей сессии):**
- `Spring/Spring MVC REST (Controller vs RestController)` — @Controller vs @RestController, CRUD-таблица со статусами, DispatcherServlet, @ModelAttribute для фильтров
- `Spring/Глобальная обработка исключений в Spring` — @RestControllerAdvice, @ExceptionHandler, ResponseEntity, сужение области, связь с AOP

**Состояние после gap-анализа:**
- Страницы с хорошим контентом в нестандартном формате (emoji/callouts): HTTP-страницы, Kafka-страницы — контент полный, формат отличается от шаблона
- Все индивидуальные страницы Mockito (Mock vs Spy, @Mock/@InjectMocks/@Spy, verify) — ХОРОШИЙ контент
- Микросервисы-страницы (Декомпозиция, Circuit Breaker, Service Discovery, vs монолит) — ХОРОШИЙ контент

---

## [2026-04-13] ingest | HIBERNATE Вопросы технических собеседований.pdf

Источник: методичка Kata-курсов, тема Hibernate/JPA.

**Обновлена существующая страница (полный Justin Song формат):**
- `БД/Проблема N+1 запросов` — механика N+1 с SQL примером, таблица дефолтов LAZY/EAGER по типу аннотации, опасность EAGER на коллекциях (Cartesian product), LIE с диаграммой жизни сессии + антипаттерн open-in-view, все 4 решения с кодом (JOIN FETCH + DISTINCT, @EntityGraph, @BatchSize, DTO), JOIN FETCH vs обычный JOIN таблица

**Обновлены системные файлы:** `index.md`

---

## [2026-04-13] ingest | SQL Вопросы технических собеседований.pdf

Источник: методичка Kata-курсов, тема SQL/Реляционные БД.

**Обновлены существующие страницы (полный Justin Song формат):**
- `JAVA core/SQL индексы JOIN нормализация` — механика B-tree (визуальная схема), composite index + правило левого префикса, covering index, таблица когда индекс вреден, JOINs с визуализацией и паттерном LEFT JOIN + IS NULL, WHERE vs HAVING с примерами, 1NF/2NF/3NF с конкретными примерами, EXPLAIN ANALYZE таблица узлов
- `БД/Транзакции уровни изоляции` — ACID каждая буква с примером кода, dirty/non-repeatable/phantom read с временными диаграммами, таблица уровней изоляции с дефолтами PostgreSQL/MySQL, MVCC, @Transactional propagation таблица, self-invocation ловушка

**Обновлены системные файлы:** `index.md`

---

## [2026-04-13] ingest | Многопоточность Вопросы технических собеседований.pdf

Источник: методичка Kata-курсов, тема Многопоточность.

**Обновлена существующая страница (полный Justin Song формат + значительное расширение):**
- `JAVA core/Многопоточность основы` — volatile (гарантии и антипаттерны), double-checked locking, volatile vs synchronized таблица, race condition/deadlock/livelock с кодом и способами избежать, CAS механика + таблица Atomic-классов, Runnable vs Callable + Future API, ThreadLocal с примерами и ловушкой утечки памяти в пуле потоков

**Обновлены системные файлы:** `index.md`

---

## [2026-04-13] ingest | CORE 2 Вопросы технических собеседований.pdf

Источник: методичка Kata-курсов, CORE 2 — Generics, Collections, Stream API.

**Обновлены существующие страницы (полный Justin Song формат):**
- `JAVA core/Generics` — PECS с примерами, type erasure детально (что нельзя делать), wildcards
- `JAVA core/Устройство HashMap` — полное покрытие всех вопросов: бакеты, rehashing, null-ключи, HashMap vs TreeMap vs LinkedHashMap, Set-коллекции, Comparable/Comparator для Tree-структур
- `JAVA core/ArrayList vs LinkedList` — Big O таблица, механика расширения capacity, ArrayDeque как альтернатива
- `JAVA core/Stream API` — map vs flatMap с примерами (freq 25), functional interfaces таблица, Optional антипаттерны, параллельные стримы

**Обновлены системные файлы:** `1 Java Core MOC.md`, `index.md`

---

## [2026-04-13] ingest | CORE 1 Вопросы технических собеседований.pdf

Источник: методичка Kata-курсов, анализ 150 собеседований Java-разработчиков.

**Создана новая страница:**
- `JAVA core/Интерфейс vs абстрактный класс` (частота 25 на собесах — критичный пробел)

**Обновлены существующие страницы (добавлены разделы: Проблема, Аналогия, Связи, Ответ на собесе, Шпаргалка):**
- `JAVA core/Основы ООП` — расширен раздел полиморфизма, добавлен override vs hide с примером
- `JAVA core/Принципы SOLID` — добавлены примеры нарушений SRP/OCP/LSP/ISP/DIP с кодом
- `JAVA core/Контракт equals и hashCode` — добавлен сценарий мутабельного ключа, полный ответ на собесе
- `JAVA core/Исключения в Java` — расширен try-with-resources (suppressed exceptions, AutoCloseable), `return` в finally
- `JAVA core/Иммутабельность String` — добавлены 5 правил immutable-класса, String Pool детали, паттерны StringBuilder
- `JAVA core/Garbage Collector JVM` — добавлена схема памяти JVM, Stack vs Heap таблица, WeakReference, диагностика OOM

**Обновлены системные файлы:** `1 Java Core MOC.md`, `index.md`

---

## [2026-04-13] setup | Инициализация LLM Wiki инфраструктуры

Создана инфраструктура для работы по паттерну LLM Wiki:
- `CLAUDE.md` — схема wiki: структура директорий, язык, шаблон страниц по методологии Justin Song, воркфлоу ingest/query/lint
- `index.md` — мастер-каталог: 51 страница по 8 разделам (Java Core, Spring, БД, Микросервисы, Kafka, HTTP/REST, Тестирование, Инфраструктура)
- `log.md` — этот файл

**Состояние wiki на момент инициализации:**
- 51 контентная страница + 6 MOC-файлов
- Методология Justin Song применена частично (Circuit Breaker — эталонный пример)
- Большинство страниц используют формат bullet-points без раздела "Ответ на собесе"
- Папка `Devops/` содержит устаревшие дубли → при следующем lint перенести в `ИНФРАСТУКТУРА/`

**Следующие шаги:**
- Добавить `raw/` директорию при первом ingest
- Постепенно привести страницы к шаблону Justin Song по мере добавления источников
