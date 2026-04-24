---
tags: [java, web, http, hexlet]
source: "Java Веб-технологии"
---

# Работа с базой данных в Javalin

  * Устанавливаем зависимости
  * Настраиваем подключение
  * Строим начальную структуру базы данных
  * Создаем репозиторий CarRepository
  * Рассматриваем примеры операций



Репозитории, которыми мы пользовались в уроках этого курса, хранят свои данные в обычных переменных. Это было удобно для того, чтобы не отвлекаться на взаимодействие с базой и сфокусироваться на особенностях работы веба.

Теперь мы привыкли к фреймворку и понимаем принципы создания приложений на нем, поэтому можно начинать работу с реальной базой данных.

Чтобы начать хранить и извлекать данные из базы, нам нужно выполнить несколько действий:

  1. Подключить пакеты, необходимые для работы с базой данных
  2. Настроить подключение к базе данных и дать к нему доступ из приложения
  3. Создать начальную структуру базы данных с нужными таблицами
  4. Переписать методы репозиториев так, чтобы они работали с данными через базу



В этом уроке мы проделаем все эти шаги на примере создания части CRUD для сущности `Car` с полями `make` (марка) и `model` (модель).

## Устанавливаем зависимости

Для простоты мы будем использовать базу данных H2 с хранением в памяти. Этого достаточно в обучении, но в реальном окружении уже понадобится поставить PostgreSQL или его аналог: 
    
    
    implementation("com.h2database:h2:2.2.220")
    implementation("com.zaxxer:HikariCP:5.0.1")
    

В дополнение к самой базе данных, нам понадобится пакет HikariCP. Он предоставляет пул соединений для работы в конкурентной среде, когда множество клиентов выполняют запросы одновременно. В такой ситуации одного соединения с базой данных будет недостаточно. Ниже мы увидим, как это работает.

## Настраиваем подключение

Рассмотрим такой пример: 
    
    
    package org.example.hexlet;
    
    import com.zaxxer.hikari.HikariConfig;
    import com.zaxxer.hikari.HikariDataSource;
    
    // Остальные импорты
    
    public class HelloWorld {
        public static Javalin getApp() {
            var hikariConfig = new HikariConfig();
            hikariConfig.setJdbcUrl("jdbc:h2:mem:hexlet_project;DB_CLOSE_DELAY=-1;");
    
            var dataSource = new HikariDataSource(hikariConfig);
            BaseRepository.dataSource = dataSource;
    
            var app = Javalin.create(config -> {
                config.bundledPlugins.enableDevLogging();
                config.fileRenderer(new JavalinJte());
            });
    
            // Остальной код
        }
    }
    

В примере выше мы создаем базу данных H2 с именем _hexlet_project_ и расположением в памяти. После создания базы данных мы получаем переменную `dataSource`, через которую мы будем работать с базой. Доступ к ней нам будет нужен в репозиториях, потому что запросы должны быть сосредоточенны в них.

Поэтому нам нужно создать общий базовый класс для всех репозиториев со статическим полем для хранения этой переменой. Все остальные репозитории от него наследуются: 
    
    
    package org.example.hexlet.repository;
    
    import com.zaxxer.hikari.HikariDataSource;
    
    public class BaseRepository {
        public static HikariDataSource dataSource;
    }
    

## Строим начальную структуру базы данных

В нашем случае база данных создается при старте приложения, поэтому ее инициализацию мы будем делать там же, во время старта. Для этого создадим файл с нужной схемой данных и затем добавим ее в базу данных:

  1. Добавляем файл _src/main/resources/schema.sql_ : 
         
         DROP TABLE IF EXISTS courses;
         
         CREATE TABLE courses (
             id INT PRIMARY KEY AUTO_INCREMENT,
             name VARCHAR(255) NOT NULL,
             description TEXT
         );
         
         DROP TABLE IF EXISTS cars;
         
         CREATE TABLE cars (
             id INT PRIMARY KEY AUTO_INCREMENT,
             make VARCHAR(255) NOT NULL,
             model VARCHAR(255) NOT NULL
         );
         

  2. Во время инициализации базы данных загружаем схему в базу: 
         
         public static Javalin getApp() throws Exception {
             var hikariConfig = new HikariConfig();
             hikariConfig.setJdbcUrl("jdbc:h2:mem:project;DB_CLOSE_DELAY=-1;");
         
             var dataSource = new HikariDataSource(hikariConfig);
             // Получаем путь до файла в src/main/resources
             var url = HelloWorld.class.getClassLoader().getResourceAsStream("schema.sql");
             var sql = new BufferedReader(new InputStreamReader(url))
                 .lines().collect(Collectors.joining("\n"));
         
             // Получаем соединение, создаем стейтмент и выполняем запрос
             try (var connection = dataSource.getConnection();
                     var statement = connection.createStatement()) {
                 statement.execute(sql);
             }
             BaseRepository.dataSource = dataSource;
         
             var app = Javalin.create(config -> {
                 config.bundledPlugins.enableDevLogging();
             });
         




## Создаем репозиторий CarRepository

Перейдем к созданию репозитория: 
    
    
    package org.example.hexlet.repository;
    
    import java.sql.SQLException;
    import java.sql.Statement;
    import java.util.ArrayList;
    import java.util.List;
    import java.util.Optional;
    
    import org.example.hexlet.model.Car;
    
    public class CarRepository extends BaseRepository {
        public static void save(Car car) throws SQLException {
            String sql = "INSERT INTO cars (make, model) VALUES (?, ?)";
            try (var conn = dataSource.getConnection();
                    var preparedStatement = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
                preparedStatement.setString(1, car.getMake());
                preparedStatement.setString(2, car.getModel());
                preparedStatement.executeUpdate();
                var generatedKeys = preparedStatement.getGeneratedKeys();
                // Устанавливаем ID в сохраненную сущность
                if (generatedKeys.next()) {
                    car.setId(generatedKeys.getLong(1));
                } else {
                    throw new SQLException("DB have not returned an id after saving an entity");
                }
            }
        }
    
        public static Optional<Car> find(Long id) throws SQLException {
            var sql = "SELECT * FROM cars WHERE id = ?";
            try (var conn = dataSource.getConnection();
                    var stmt = conn.prepareStatement(sql)) {
                stmt.setLong(1, id);
                var resultSet = stmt.executeQuery();
                if (resultSet.next()) {
                    var make = resultSet.getString("make");
                    var model = resultSet.getString("model");
                    var car = new Car(make, model);
                    car.setId(id);
                    return Optional.of(car);
                }
                return Optional.empty();
            }
        }
    
        public static List<Car> getEntities() throws SQLException {
            var sql = "SELECT * FROM cars";
            try (var conn = dataSource.getConnection();
                    var stmt = conn.prepareStatement(sql)) {
                var resultSet = stmt.executeQuery();
                var result = new ArrayList<Car>();
                while (resultSet.next()) {
                    var id = resultSet.getLong("id");
                    var make = resultSet.getString("make");
                    var model = resultSet.getString("model");
                    var car = new Car(make, model);
                    car.setId(id);
                    result.add(car);
                }
                return result;
            }
        }
    }
    

Принцип создания всех методов для работы с базой данных одинаковый:

  * Описываем шаблон запроса
  * Получаем соединение
  * Формируем стейтмент
  * Делаем подстановки
  * Выполняем запрос
  * Собираем результат
  * Возвращаем ответ



## Рассматриваем примеры операций

Структура контроллеров не меняется, несмотря на все изменения, которые мы сделали. Как видно на примере ниже, правильная организация абстракций и разделение по слоям приводят к тому, что изменение внутренностей не оказывает особого влияния на строение приложения: 
    
    
    package org.example.hexlet.controller;
    
    import java.sql.SQLException;
    import static io.javalin.rendering.template.TemplateUtil.model;
    
    import org.example.hexlet.dto.cars.CarPage;
    import org.example.hexlet.dto.cars.CarsPage;
    import org.example.hexlet.model.Car;
    import org.example.hexlet.repository.CarRepository;
    import org.example.hexlet.util.NamedRoutes;
    
    import io.javalin.http.Context;
    import io.javalin.http.NotFoundResponse;
    
    public class CarController {
        public static void index(Context ctx) throws SQLException {
            var cars = CarRepository.getEntities();
            var page = new CarsPage(cars);
            ctx.render("cars/index.jte", model("page", page));
        }
    
        public static void show(Context ctx) throws SQLException {
            var id = ctx.pathParamAsClass("id", Long.class).get();
            var car = CarRepository.find(id)
                    .orElseThrow(() -> new NotFoundResponse("Car with id = " + id + " not found"));
            var page = new CarPage(car);
            ctx.render("cars/show.jte", model("page", page));
        }
    
        public static void build(Context ctx) {
            ctx.render("cars/build.jte");
        }
    
        public static void create(Context ctx) throws SQLException {
            var make = ctx.formParam("make");
            var model = ctx.formParam("model");
    
            var car = new Car(make, model);
            CarRepository.save(car);
            ctx.redirect(NamedRoutes.carsPath());
        }
    }
    

* * *

#### Самостоятельная работа

  1. Проделайте все шаги из урока на своем компьютере на примере сущности курсов
  2. Перейдите в свое приложение и репозиторий курсов и внесите туда изменения так, чтобы репозитории работали с базой данных
  3. Сделайте то же самое для сущности пользователя
  4. Залейте изменения на GitHub



* * *

#### Дополнительные материалы

  1. База данных H2
  2. Пул соединений HikariCP
