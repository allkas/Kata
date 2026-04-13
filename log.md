# Log — Хронологический журнал изменений

*Формат записей: `## [YYYY-MM-DD] <тип> | <описание>`*
*Типы: `ingest` | `query` | `lint` | `setup`*

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
