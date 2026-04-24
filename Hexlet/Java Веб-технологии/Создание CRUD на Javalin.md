---
tags: [java, web, http, hexlet]
source: "Java Веб-технологии"
---

# Создание CRUD на Javalin

  * Что такое CRUD
  * Как работают контроллеры



Несмотря на огромное число разнообразных сайтов, практически всю веб-разработку можно свести к CRUD-операциям. В этом уроке мы познакомимся с ними подробнее.

## Что такое CRUD

CRUD — это широко распространенный термин, означающий четыре стандартные операции над любой сущностью. Рассмотрим такой пример:

  * Создание (_Create_) — регистрация пользователя
  * Чтение (_Read_) — просмотр профиля пользователями сайта или в административном интерфейсе
  * Обновление (_Update_) — Обновление личных данных, смена электронной почты или пароля
  * Удаление (_Delete_) — удаление данных



Точно так же можно расписать действия над любыми другими ресурсами: фотографиями пользователя, его друзьями, сообщениями и так далее. Чтобы создать полный CRUD, нужно выполнить следующие действия:

  * Создать сущность в коде (как правило, это класс)
  * Добавить таблицу в базу
  * Написать тесты для проверки обработчиков
  * Добавить обработчики
  * Добавить шаблоны



Ниже мы пройдемся по всему процессу создания CRUD пользователя за исключением работы с базой данных и тестов.

Начнем с **роутинга**. Полный CRUD пользователя включает минимум семь маршрутов. Их может быть больше, потому что любое действие может повторяться более одного раза:

Метод | Маршрут | Шаблон | Описание  
---|---|---|---  
GET | /users | users/index.jte | Список пользователей  
GET | /users/{id} | users/show.jte | Профиль пользователя  
GET | /users/build | users/build.jte | Форма создания нового пользователя  
POST | /users |  | Создание нового пользователя  
GET | /users/{id}/edit | users/edit.jte | Форма редактирования пользователя  
PATCH/PUT | /users/{id} |  | Обновление пользователя  
DELETE | /users/{id} |  | Удаление пользователя  
  
Такое соглашение об именовании маршрутов изначально появилось во фреймворке Ruby On Rails, а затем его адаптировали во многих других. Здесь мы его используем из-за его универсальности и понятности.

## Как работают контроллеры

CRUD-операции объединяют маршруты и их обработчики в логические блоки вокруг каких-то сущностей — например, CRUD курсов, упражнений, уроков, статей в блоге и так далее. Такая структура позволяет разбить приложение на файлы так, чтобы его было удобно поддерживать. В веб-разработке принято объединять обработчики в **контроллеры** – классы, которые содержат в себе обработчики сущностей.

Работая с Javalin, мы можем добавлять контроллеры как классы, потому что фреймворк по умолчанию умеет работать с ними. Чтобы лучше понять тему, разберем упрощенный пример такого класса управления пользователями: 
    
    
    package org.example.hexlet.controller;
    
    import static io.javalin.rendering.template.TemplateUtil.model;
    
    import org.example.hexlet.NamedRoutes;
    import org.example.hexlet.dto.users.UserPage;
    import org.example.hexlet.dto.users.UsersPage;
    import org.example.hexlet.model.User;
    import org.example.hexlet.repository.UserRepository;
    
    import io.javalin.http.Context;
    import io.javalin.http.NotFoundResponse;
    
    public class UsersController {
        public static void index(Context ctx) {
            var users = UserRepository.getEntities();
            var page = new UsersPage(users);
            ctx.render("users/index.jte", model("page", page));
        }
    
        public static void show(Context ctx) {
            var id = ctx.pathParamAsClass("id", Long.class).get();
            var user = UserRepository.find(id)
                    .orElseThrow(() -> new NotFoundResponse("Entity with id = " + id + " not found"));
            var page = new UserPage(user);
            ctx.render("users/show.jte", model("page", page));
        }
    
        public static void build(Context ctx) {
            ctx.render("users/build.jte");
        }
    
        public static void create(Context ctx) {
            var name = ctx.formParam("name");
            var email = ctx.formParam("email");
            var password = ctx.formParam("password");
    
            var user = new User(name, email, password);
            UserRepository.save(user);
            ctx.redirect(NamedRoutes.usersPath());
        }
    
        public static void edit(Context ctx) {
            var id = ctx.pathParamAsClass("id", Long.class).get();
            var user = UserRepository.find(id)
                    .orElseThrow(() -> new NotFoundResponse("Entity with id = " + id + " not found"));
            var page = new UserPage(user);
            ctx.render("users/edit.jte", model("page", page));
        }
    
    
        public static void update(Context ctx) {
            var id = ctx.pathParamAsClass("id", Long.class).get();
    
            var name = ctx.formParam("name");
            var email = ctx.formParam("email");
            var password = ctx.formParam("password");
    
            var user = UserRepository.find(id)
                    .orElseThrow(() -> new NotFoundResponse("Entity with id = " + id + " not found"));
            user.setName(name);
            user.setEmail(email);
            user.setPassword(password);
            UserRepository.save(user);
            ctx.redirect(NamedRoutes.usersPath());
        }
    
        public static void destroy(Context ctx) {
            var id = ctx.pathParamAsClass("id", Long.class).get();
            UserRepository.delete(id);
            ctx.redirect(NamedRoutes.usersPath());
        }
    }
    

Этот контроллер не учитывает валидацию, пагинацию и множество других деталей, которыми всегда обрастает реальное приложение. Сейчас нам важнее сфокусироваться на самой концепции.

Как мы выяснили выше, **контроллер** — это класс, в котором каждый обработчик описан статическим методом, принимающим на вход контекст. Полный CRUD включает в себя реализацию семи методов, но все зависит от задачи — иногда могут понадобиться не все методы, иногда приходится добавлять какие-то более специфические обработчики.

Теперь нужно поправить роутинг. Описание роутинга с добавлением контроллеров становится проще для восприятия: 
    
    
    app.get("/users", UsersController::index);
    app.get("/users/{id}", UsersController::show);
    app.get("/users/build", UsersController::build);
    app.post("/users", UsersController::create);
    app.get("/users/{id}/edit", UsersController::edit);
    app.patch("/users/{id}", UsersController::update);
    app.delete("/users/{id}", UsersController::destroy);
    

Когда стоит переходить на использование контроллеров? Практически в любой ситуации контроллеры не вносят сложности, но значительно помогают при расширении кода. Они улучшают навигацию по проекту и делают роутинг гораздо более понятным.

* * *

#### Самостоятельная работа

  1. Выполните шаги из урока на своем компьютере
  2. Приведите маршруты в соответствие с таблицей в уроке
  3. Выделите обработчики в отдельный контроллер и поправьте роутинг
  4. Сделайте то же самое для сущности курсов
  5. Залейте изменения на GitHub



* * *

#### Дополнительные материалы

  1. Javalin CRUD Контроллер
