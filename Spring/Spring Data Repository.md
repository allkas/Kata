---
tags: [spring, data, jpa, repository]
sources: [Kata Spring Framework & HTTP.pdf]
---

# Spring Data Repository

## 1. Проблема — зачем это существует?

Типичный репозиторий повторяет один и тот же шаблон: `save`, `findById`, `findAll`, `delete` — десятки строк boilerplate для каждой сущности. Spring Data JPA устраняет это через иерархию интерфейсов: объявляешь интерфейс, Spring генерирует реализацию. Запросы по соглашению об именовании методов или через `@Query` — без SQL/HQL вручную для типовых случаев.

## 2. Аналогия

Spring Data — как шаблонный договор в юридической фирме. Не нужно писать каждый договор с нуля — берёшь стандартный шаблон (`JpaRepository`) и заполняешь специфику (тип сущности, кастомные методы). Юрист (Spring) сам составляет полный текст по правилам.

## 3. Как работает

### Иерархия интерфейсов

```
Repository<T, ID>                     ← маркерный интерфейс (Spring Data Commons)
    ↓
CrudRepository<T, ID>                 ← CRUD: save, findById, findAll, delete
    ↓
PagingAndSortingRepository<T, ID>     ← + findAll(Sort), findAll(Pageable)
    ↓
JpaRepository<T, ID>                  ← + flush, saveAndFlush, deleteAllInBatch, getById
    ↓
SimpleJpaRepository<T, ID>            ← конкретная реализация (генерируется Spring)
```

### CrudRepository — основные методы

```java
public interface CrudRepository<T, ID> extends Repository<T, ID> {
    <S extends T> S save(S entity);              // INSERT или UPDATE
    <S extends T> Iterable<S> saveAll(Iterable<S>);
    Optional<T> findById(ID id);
    boolean existsById(ID id);
    Iterable<T> findAll();
    Iterable<T> findAllById(Iterable<ID> ids);
    long count();
    void deleteById(ID id);
    void delete(T entity);
    void deleteAll();
}
```

### JpaRepository — дополнительно

```java
public interface JpaRepository<T, ID> extends PagingAndSortingRepository<T, ID> {
    List<T> findAll();                              // возвращает List, а не Iterable
    List<T> findAll(Sort sort);
    Page<T> findAll(Pageable pageable);

    void flush();                                   // синхронизировать Persistence Context с БД
    <S extends T> S saveAndFlush(S entity);         // save + немедленный flush

    void deleteAllInBatch();                        // DELETE FROM table (одним запросом)
    void deleteAllByIdInBatch(Iterable<ID> ids);

    T getById(ID id);                               // LazyReference (throws если не найден)
    T getReferenceById(ID id);                      // Spring Data 3+, аналог getById
}
```

### Пример собственного репозитория

```java
@Repository  // опционально — Spring Data сам это делает
public interface UserRepository extends JpaRepository<User, Long> {

    // Метод по соглашению об именовании:
    Optional<User> findByEmail(String email);
    List<User> findByLastNameOrderByFirstNameAsc(String lastName);
    List<User> findByAgeGreaterThan(int age);
    boolean existsByEmail(String email);

    // @Query — JPQL:
    @Query("SELECT u FROM User u WHERE u.email = :email AND u.active = true")
    Optional<User> findActiveByEmail(@Param("email") String email);

    // @Query — нативный SQL:
    @Query(value = "SELECT * FROM users WHERE created_at > :date",
           nativeQuery = true)
    List<User> findRecentUsers(@Param("date") LocalDateTime date);

    // Модифицирующий запрос:
    @Modifying
    @Transactional
    @Query("UPDATE User u SET u.active = false WHERE u.lastLoginAt < :date")
    int deactivateOldUsers(@Param("date") LocalDateTime date);
}
```

### Метод по соглашению об именовании

Spring генерирует SQL по имени метода:

| Ключевое слово | Пример | SQL |
|----------------|--------|-----|
| `findBy` | `findByName(String)` | `WHERE name = ?` |
| `findByAnd` | `findByNameAndAge(String, int)` | `WHERE name = ? AND age = ?` |
| `findByOr` | `findByNameOrEmail(String, String)` | `WHERE name = ? OR email = ?` |
| `findByLike` | `findByNameLike(String)` | `WHERE name LIKE ?` |
| `findByContaining` | `findByNameContaining(String)` | `WHERE name LIKE %?%` |
| `findByGreaterThan` | `findByAgeGreaterThan(int)` | `WHERE age > ?` |
| `findByBetween` | `findByAgeBetween(int, int)` | `WHERE age BETWEEN ? AND ?` |
| `findByIsNull` | `findByDeletedAtIsNull()` | `WHERE deleted_at IS NULL` |
| `findByOrderBy` | `findByNameOrderByAgeDesc(String)` | `... ORDER BY age DESC` |
| `countBy` | `countByActive(boolean)` | `SELECT count(*) WHERE active = ?` |
| `deleteBy` | `deleteByEmail(String)` | `DELETE WHERE email = ?` |

### Pagination и Sorting

```java
// Pageable — задаёт страницу и размер:
Pageable pageable = PageRequest.of(0, 20, Sort.by("lastName").ascending());
Page<User> page = userRepository.findAll(pageable);

page.getContent();         // List<User> — элементы текущей страницы
page.getTotalElements();   // общее количество записей
page.getTotalPages();      // общее количество страниц
page.getNumber();          // номер текущей страницы (0-based)
page.hasNext();            // есть ли следующая страница
```

```java
// REST endpoint с пагинацией:
@GetMapping("/users")
public Page<UserDto> getUsers(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "20") int size,
        @RequestParam(defaultValue = "id") String sortBy) {

    Pageable pageable = PageRequest.of(page, size, Sort.by(sortBy));
    return userRepository.findAll(pageable).map(userMapper::toDto);
}
```

---

## 4. Глубже — что важно знать

**`save()` — INSERT или UPDATE?** Spring Data проверяет: если `entity.id == null` → `persist()` (INSERT). Если `id != null` → `merge()` (SELECT + UPDATE или INSERT). Это означает: при `save(entityWithId)` Hibernate выполнит SELECT первым.

**`getById()` vs `findById()`:** `findById()` → SELECT сразу, возвращает `Optional`. `getById()` → возвращает lazy proxy, SQL выполняется при первом обращении к полям. Если сущность не найдена — `EntityNotFoundException` при обращении.

**`@Modifying` без `@Transactional`:** модифицирующий `@Query` требует транзакцию. Можно поставить `@Transactional` на репозиторий, но лучше — на сервис, который вызывает метод.

**Projection:** вместо полной сущности можно вернуть часть полей:

```java
// Interface-based projection:
public interface UserSummary {
    String getFirstName();
    String getEmail();
}

List<UserSummary> findByActive(boolean active, Class<UserSummary> type);
// или:
List<UserSummary> findSummaryByActive(boolean active);
```

**`flush()` vs `saveAndFlush()`:** `save()` синхронизирует с Persistence Context (Hibernate знает об изменении), но SQL уходит в БД только при commit или `flush()`. `saveAndFlush()` = `save()` + `flush()` — полезно когда нужно увидеть изменения сразу в той же транзакции.

---

## 5. Связи с другими концепциями

- [[Spring Core IoC DI]] — репозитории — Spring-бины, инжектируются в сервисы
- [[Транзакции уровни изоляции]] — `@Transactional` на сервисном слое управляет транзакциями репозиториев
- [[Проблема N+1 запросов]] — Spring Data не решает N+1 автоматически; нужны JOIN FETCH или @EntityGraph
- [[Spring Boot]] — `spring-boot-starter-data-jpa` настраивает всё автоматически

## 6. Ответ на собесе (2 минуты)

> "Spring Data JPA — это слой абстракции над JPA, который устраняет boilerplate. Иерархия интерфейсов:
>
> `Repository` (маркер) → `CrudRepository` (save/find/delete) → `PagingAndSortingRepository` (пагинация, сортировка) → `JpaRepository` (flush, deleteInBatch, getById).
>
> Конкретную реализацию (`SimpleJpaRepository`) Spring генерирует сам — объявляю только интерфейс.
>
> **Методы по соглашению об именовании:** `findByEmailAndActive(String, boolean)` → Spring разбирает имя и генерирует JPQL. Для сложных запросов — `@Query` с JPQL или нативным SQL.
>
> **`save()`:** если id == null → INSERT (persist), если id != null → SELECT + UPDATE (merge). `saveAndFlush()` дополнительно делает flush в текущей транзакции.
>
> **Pagination:** `findAll(PageRequest.of(0, 20, Sort.by("name")))` → возвращает `Page<T>` с элементами, общим количеством, информацией о страницах."

## Шпаргалка

| Интерфейс | Добавляет |
|-----------|-----------|
| `CrudRepository` | save, findById, findAll, delete, count |
| `PagingAndSortingRepository` | findAll(Sort), findAll(Pageable) |
| `JpaRepository` | flush, saveAndFlush, deleteAllInBatch, getReferenceById |

| Метод | Поведение |
|-------|-----------|
| `save(entity)` | id == null → INSERT; id != null → merge (SELECT + UPDATE) |
| `findById(id)` | SELECT сразу, возвращает Optional |
| `getReferenceById(id)` | Lazy proxy, SQL при первом обращении |
| `saveAndFlush()` | save + немедленный flush в БД |
| `deleteAllInBatch()` | Один DELETE без загрузки сущностей |

**Связи:**
- [[Spring Core IoC DI]]
- [[Транзакции уровни изоляции]]
- [[Проблема N+1 запросов]]
- [[Spring Boot]]
