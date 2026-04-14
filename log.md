# Log — Хронологический журнал изменений

*Формат записей: `## [YYYY-MM-DD] <тип> | <описание>`*
*Типы: `ingest` | `query` | `lint` | `setup`*

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
