---
tags: [spring, core, ioc, di, beans]
sources: [Kata Spring Framework & HTTP.pdf]
---

# Spring Core IoC DI

## 1. Проблема — зачем это существует?

В классическом коде объекты сами создают свои зависимости: `new Service(new Repository(new DataSource(...)))`. Это приводит к жёсткой связанности: изменить реализацию → переписать всех зависимых. IoC инвертирует управление: контейнер создаёт объекты и внедряет зависимости, а не объекты сами себя собирают. Код становится тестируемым, заменяемым и декларативным.

## 2. Аналогия

IoC — как HR-отдел в компании. Разработчик не бегает сам искать коллег (не делает `new`). Он описывает, какие специалисты ему нужны (интерфейсы/аннотации), а HR (IoC-контейнер) находит подходящих людей и подключает их к команде (DI). Разработчик работает с готовой командой, не зная, кто именно и откуда.

## 3. Как работает

### IoC vs DI

**IoC (Inversion of Control)** — принцип: контейнер управляет жизненным циклом объектов, а не объекты управляют собой.

**DI (Dependency Injection)** — реализация IoC: зависимости передаются объекту извне (через конструктор, сеттер, поле).

```
IoC — это «ЧТО» (контейнер управляет)
DI  — это «КАК» (зависимости передаются внутрь)
DI — частный случай IoC
```

### BeanDefinition

`BeanDefinition` — метаданные о бине в контейнере: какой класс, какой scope, lazy или нет, какие зависимости, методы init/destroy.

```java
// Что хранит BeanDefinition (упрощённо):
// - beanClass: UserService.class
// - scope: singleton
// - lazyInit: false
// - initMethodName: "init"
// - destroyMethodName: "cleanup"
// - dependsOn: ["dataSource"]
```

### BeanFactory vs ApplicationContext

| | `BeanFactory` | `ApplicationContext` |
|---|---|---|
| **Инициализация бинов** | Ленивая (при первом запросе) | Жадная (при старте, для singleton) |
| **MessageSource (i18n)** | Нет | Да |
| **Event publishing** | Нет | Да (`ApplicationEventPublisher`) |
| **AOP-интеграция** | Ручная | Автоматическая |
| **@Autowired** | Нет (нужен пост-процессор) | Да |
| **Применение** | Встраиваемые системы | Все реальные приложения |

`ApplicationContext` расширяет `BeanFactory` и добавляет 4 ответственности:
1. **MessageSource** — интернационализация
2. **ApplicationEventPublisher** — события (publish/subscribe)
3. **ResourceLoader** — загрузка ресурсов (classpath, file, URL)
4. **AOP-интеграция** — автоматическое создание прокси

### BeanPostProcessor

`BeanPostProcessor` — хук, позволяющий модифицировать бин после создания:

```java
public interface BeanPostProcessor {
    Object postProcessBeforeInitialization(Object bean, String beanName);
    Object postProcessAfterInitialization(Object bean, String beanName);
}
```

**Примеры BeanPostProcessor в Spring:**
- `AutowiredAnnotationBeanPostProcessor` — обрабатывает `@Autowired`
- `CommonAnnotationBeanPostProcessor` — обрабатывает `@PostConstruct`, `@PreDestroy`
- `AbstractAdvisorAutoProxyCreator` — создаёт AOP-прокси

### BeanFactoryPostProcessor

`BeanFactoryPostProcessor` — хук для модификации **метаданных** (`BeanDefinition`) до создания бинов:

```java
public interface BeanFactoryPostProcessor {
    void postProcessBeanFactory(ConfigurableListableBeanFactory beanFactory);
}
```

`PropertySourcesPlaceholderConfigurer` — стандартный `BeanFactoryPostProcessor`, подставляющий `${property}` значения.

```
BeanFactoryPostProcessor  →  работает с BeanDefinition (до создания бинов)
BeanPostProcessor         →  работает с готовыми бинами (после создания)
```

### Способы DI

```java
// 1. Constructor injection (рекомендуемый)
@Service
public class UserService {
    private final UserRepository repository; // final — нельзя изменить

    @Autowired // с 1 конструктором можно опустить
    public UserService(UserRepository repository) {
        this.repository = repository;
    }
}

// 2. Setter injection
@Service
public class UserService {
    private UserRepository repository;

    @Autowired
    public void setRepository(UserRepository repository) {
        this.repository = repository;
    }
}

// 3. Field injection (не рекомендуется — плохо тестируется)
@Service
public class UserService {
    @Autowired
    private UserRepository repository;
}
```

**Почему constructor injection лучше:**
- Зависимость `final` — нельзя переприсвоить
- NPE невозможен — объект без зависимости не создастся
- Тестируется без Spring (`new UserService(mockRepo)`)

### @Autowired vs @Resource vs @Inject

| | `@Autowired` | `@Resource` | `@Inject` |
|---|---|---|---|
| **Стандарт** | Spring | JSR-250 (Java EE) | JSR-330 |
| **Стратегия по умолчанию** | By type | By name | By type |
| **Fallback** | By name (с @Qualifier) | By type | By name (с @Named) |
| **Required** | `@Autowired(required=false)` | Нет | `@Nullable` |
| **Поддержка** | Spring | Spring + Jakarta EE | Spring + CDI |

```java
@Autowired                          // по типу UserRepository
private UserRepository repository;

@Resource(name = "primaryRepo")     // по имени "primaryRepo"
private UserRepository repository;

@Inject                             // по типу (JSR-330)
private UserRepository repository;
```

### @Qualifier и @Primary

```java
// Два бина одного типа:
@Bean("fastCache")
public CacheService fastCacheService() { ... }

@Bean("slowCache")
public CacheService slowCacheService() { ... }

// @Qualifier — явно указать имя бина:
@Autowired
@Qualifier("fastCache")
private CacheService cache;

// @Primary — бин по умолчанию когда нет @Qualifier:
@Bean
@Primary
public CacheService defaultCache() { ... }
```

**Приоритет разрешения:** `@Qualifier` > `@Primary` > имя поля

### @Value и SpEL

```java
@Component
public class Config {
    // Из application.properties:
    @Value("${server.port:8080}")       // значение по умолчанию 8080
    private int serverPort;

    // SpEL — вычисление выражения:
    @Value("#{systemProperties['user.home']}")
    private String userHome;

    @Value("#{T(Math).PI}")             // статический метод
    private double pi;

    @Value("#{userService.adminEmail}") // значение из другого бина
    private String adminEmail;
}
```

`${}` — placeholder из properties-файла. `#{}` — SpEL-выражение.

### @ComponentScan

```java
@Configuration
@ComponentScan(
    basePackages = "com.example",           // сканировать пакет
    basePackageClasses = UserService.class, // или класс как маркер
    excludeFilters = @ComponentScan.Filter(
        type = FilterType.ANNOTATION,
        classes = Repository.class          // исключить @Repository
    )
)
public class AppConfig { }
```

### @Bean vs @Component

| | `@Bean` | `@Component` |
|---|---|---|
| **Где ставится** | На метод в `@Configuration` | На класс |
| **Управление** | Явное (ты пишешь код создания) | Автоматическое (Spring создаёт) |
| **Когда использовать** | Сторонние классы (нельзя добавить аннотацию) | Свои классы |

```java
// @Bean — для сторонних классов:
@Bean
public ObjectMapper objectMapper() {
    return new ObjectMapper().findAndRegisterModules();
}

// @Component — для своих классов:
@Service
public class UserService { ... }
```

`@Service`, `@Repository`, `@Controller` — специализации `@Component` (дополнительная семантика + обработка).

### @Conditional и @Profile

```java
// @Profile — активировать бин для конкретного профиля:
@Bean
@Profile("dev")
public DataSource h2DataSource() { ... }

@Bean
@Profile("prod")
public DataSource postgresDataSource() { ... }

// Активация: spring.profiles.active=prod

// @Conditional — произвольное условие:
public class OnLinuxCondition implements Condition {
    public boolean matches(ConditionContext ctx, AnnotatedTypeMetadata meta) {
        return ctx.getEnvironment().getProperty("os.name").contains("Linux");
    }
}

@Bean
@Conditional(OnLinuxCondition.class)
public LinuxService linuxService() { ... }
```

**Spring Boot @ConditionalOnXxx:**

| Аннотация | Условие |
|-----------|---------|
| `@ConditionalOnClass(X.class)` | Класс X есть на classpath |
| `@ConditionalOnMissingBean(X.class)` | Бин типа X не определён |
| `@ConditionalOnProperty("feature.enabled")` | Свойство задано/истинно |
| `@ConditionalOnExpression("#{...}")` | SpEL-выражение истинно |
| `@ConditionalOnWebApplication` | Это web-приложение |

### Инъекция в static поля (workaround)

```java
// static поля не могут иметь @Autowired напрямую:
@Component
public class DateUtils {
    private static ClockService clockService;

    @Autowired // на setter — Spring вызовет его после создания бина
    public void setClockService(ClockService clockService) {
        DateUtils.clockService = clockService;
    }
}
```

---

## 4. Глубже — что важно знать

**Circular dependency:** если бин A зависит от B, а B от A через constructor injection — ошибка при старте. Решение: один из них через setter injection или `@Lazy`.

**@Configuration vs @Component для @Bean:** в `@Configuration` методы `@Bean` проксируются (вызов `methodA()` из `methodB()` → возвращает существующий бин). В `@Component` — прямой вызов метода (создаст новый объект). Рекомендуется всегда использовать `@Configuration`.

---

## 5. Связи с другими концепциями

- [[Жизненный цикл Spring бина]] — как контейнер создаёт и уничтожает бины
- [[Spring Boot]] — @SpringBootApplication включает @ComponentScan и @EnableAutoConfiguration
- [[Spring AOP]] — BeanPostProcessor создаёт AOP-прокси (@Transactional, @Cacheable)
- [[Транзакции уровни изоляции]] — @Transactional работает через AOP-прокси IoC-контейнера

## 6. Ответ на собесе (2 минуты)

> "IoC — принцип: контейнер управляет созданием объектов, не объекты сами. DI — конкретный механизм IoC: зависимости передаются извне. DI — частный случай IoC.
>
> **ApplicationContext** — основной контейнер Spring. Расширяет BeanFactory, добавляя события, i18n, AOP-интеграцию. BeanFactory — ленивая инициализация; ApplicationContext — жадная (singleton создаются при старте).
>
> **BeanDefinition** — метаданные о бине (класс, scope, init-метод). BeanFactoryPostProcessor обрабатывает их до создания бинов — например, `PropertySourcesPlaceholderConfigurer` подставляет `${...}`. BeanPostProcessor работает с готовыми бинами — например, `AutowiredAnnotationBeanPostProcessor` обрабатывает `@Autowired`.
>
> **@Autowired** — инъекция по типу (Spring). @Resource — по имени (JSR-250). @Inject — по типу (JSR-330).
>
> **Constructor injection** предпочтителен: зависимость final, NPE невозможен, тестируется без контейнера.
>
> **@Qualifier** > **@Primary** > имя поля — порядок приоритета при разрешении нескольких бинов одного типа."

## Шпаргалка

| Концепция | Суть | Ключевое |
|-----------|------|---------|
| **IoC** | Контейнер управляет созданием | Инверсия управления |
| **DI** | Зависимости передаются извне | Частный случай IoC |
| **BeanDefinition** | Метаданные о бине | class, scope, init-метод |
| **BeanFactory** | Базовый контейнер | Ленивая инициализация |
| **ApplicationContext** | Полный контейнер | События, i18n, AOP |
| **BeanFactoryPostProcessor** | До создания бинов | Модифицирует BeanDefinition |
| **BeanPostProcessor** | После создания бинов | Модифицирует готовый бин |
| **@Autowired** | By type (Spring) | Нужен @Qualifier если несколько |
| **@Resource** | By name (JSR-250) | Fallback → by type |
| **@Qualifier** | Уточнить бин по имени | Приоритет > @Primary |
| **@Primary** | Бин по умолчанию | Приоритет < @Qualifier |
| **@Value("${}")** | Из properties | Placeholder |
| **@Value("#{}") ** | SpEL-выражение | Вычисляется динамически |
| **@Profile** | Бин для профиля | spring.profiles.active=prod |
| **@Conditional** | Произвольное условие | @ConditionalOnClass и др. |

**Связи:**
- [[Жизненный цикл Spring бина]]
- [[Spring Boot]]
- [[Spring AOP]]
- [[Транзакции уровни изоляции]]
