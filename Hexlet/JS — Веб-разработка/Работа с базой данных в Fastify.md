---
tags: [javascript, web, hexlet]
source: "JS — Веб-разработка"
---

# Работа с базой данных в Fastify

  * Установка зависимостей
  * Настройка подключения
  * Начальная структура базы данных
  * Пример операций: список, создание и просмотр
    * Добавление записи
    * Извлечение списка
    * Извлечение одной записи
    * Добавление записи
    * Обновление записи
    * Удаление записи
  * Итог



Данные приложения, которыми мы пользовались в уроках этого курса, хранятся в обычных переменных. Это было удобно для того, чтобы не отвлекаться на взаимодействие с базой и сфокусироваться на особенностях работы веба. Теперь, когда мы привыкли к фреймворку и понимаем принципы создания приложений на нем, можно включать работу с реальной базой данных.

Чтобы начать хранить и извлекать данные из базы, нам нужно выполнить несколько действий:

  1. Подключить пакеты, необходимые для работы с базой данных;
  2. Настроить подключение к базе данных и дать к нему доступ из приложения;
  3. Создать начальную структуру базы данных с нужными таблицами;
  4. Переписать методы репозиториев так, чтобы они работали с данными через базу



## Установка зависимостей

Для простоты, мы будем использовать базу данных sqlite3 с хранением в памяти. Этого достаточно в обучении, но в реальном окружении уже понадобится поставить PostgreSQL или его аналог. 
    
    
    npm i sqlite3
    

## Настройка подключения
    
    
    import sqlite3 from 'sqlite3';
    
    const db = new sqlite3.Database(':memory:');
    

В примере выше мы создаем базу данных в памяти с помощью параметра `':memory:'`. База данных в памяти — это значит, что база данных будет существовать только в операционной памяти компьютера пока работает сервер. Когда сервер остановится, база данных исчезнет. После создания базы данных, у нас оказывается переменная `db` через которую мы будем работать с базой.

## Начальная структура базы данных

Так как в нашем случае база данных создается при старте приложения, то и ее инициализацию мы будем делать там же, во время старта. Для запросов в базу данных объект `db` предоставляет метод `run()`. Есть еще один полезный метод `serialize()` — этот метод обеспечивает что все запросы к базе данных выполняться последовательно. Этот метод принимает колбек, внутри которой выполняется вся работа: 
    
    
    db.serialize(() => {
      db.run(`
        CREATE TABLE courses (
          id INTEGER PRIMARY KEY,
          name VARCHAR(255) NOT NULL,
          description TEXT
        );
      `);
    
      db.run(`
        CREATE TABLE cars (
          id INTEGER PRIMARY KEY,
          make VARCHAR(255) NOT NULL,
          model VARCHAR(255) NOT NULL
        );
      `);
    });
    

В примере выше в метод `serialize()` передается функция, внутри которой выполняются запросы с помощью метода `run()`. В метод передаются обычные SQL-запросы. Для удобства чтения мы разделили на несколько строк каждый запрос.

## Пример операций: список, создание и просмотр

### Добавление записи

Библиотека предоставляет множество разных методов для работы с базой данных. Разберем некоторые из них на примерах. Начнем с добавления записей в базу данных: 
    
    
    const courses = [
      { id: 1, title: 'JavaScript', description: 'Курс по языку программирования JavaScript' },
      { id: 2, title: 'Fastify', description: 'Курс по фреймворку Fastify' },
    ];
    
    const stmt = db.prepare('INSERT INTO courses VALUES (?, ?, ?)');
    
    courses.forEach((course) => {
      stmt.run(course.id, course.title, course.description);
    });
    
    stmt.finalize();
    

Метод `prepare()` позволяет подготовить SQL-запрос, а затем выполнить его с подстановкой значений. Это бывает особенно полезно, когда нужно выполнить несколько запросов с разными данными. В нашем примере мы подставляем значения из массива и добавляем несколько строк в базу. Затем вызывается метод `finalize()` завершающий операции добавления.

### Извлечение списка

Для извлечения списка можно использовать метод `all()`. Вторым параметром метод принимает колбек, в который передается ошибка, если что-то пошло не так и сами данные: 
    
    
    app.get('/courses', (req, res) => {
      db.all('SELECT * FROM courses', (error, data) => {
        const templateData = {
          courses: data,
          error,
        };
        res.view('courses/index', templateData);
      });
    });
    

### Извлечение одной записи

Для извлечения записи можно воспользоваться методом `get()`: 
    
    
    app.get('/courses/:id', (req, res) => {
      const { id } = req.params;
      db.get(`SELECT * FROM courses WHERE id = ${id}`, (err, data) => {
        const templateData = {
          course: data,
          error,
        };
        res.view('courses/show', templateData);
      });
    });
    

### Добавление записи

Добавление данных в базу данных можно реализовать с помощью метода `run()`. Этот метод можно использовать для внесения изменений в базу данных: 
    
    
    app.post('/courses/:id', (req, res) => {
      const { id } = req.params;
      const { title, description } = req.body;
      const stmt = db.prepare('INSERT INTO courses(title, description) VALUES (?, ?)');
      stmt.run([title, description], function (error) {
        if (error) {
          const templateData = {
            error,
            course: { title, description },
          };
          res.view('courses/new', templateData);
          return;
        }
        res.redirect(`/courses/${this.lastID}`);
      });
    });
    

При добавлении записи бывают ситуации, когда нам нужно получить новые данные. Например, идентификатор добавленного ресурса, который используется в адресе редиректа. Для этого можно воспользоваться свойством `this.lastID` в колбеке. Обратите внимание, что используется обычная функция, объявленная через `function`. Если использовать стрелочную функцию, то контекст будет неверным.

### Обновление записи

Обновление записи, так же используем метод `run()`: 
    
    
    app.patch('/courses/:id', (req, res) => {
      const { id } = req.params;
      const { title, description } = req.body;
      db.run(`UPDATE courses SET
        title = "${title}",
        description = "${description}"
        WHERE id = ${id};
      `, (err) => {
        if (err) {
          res.send(err);
          return;
        }
        res.redirect('/courses');
      });
    });
    

### Удаление записи

И для удаления можно так же использовать метод `run()`: 
    
    
    app.delete('/courses/:id', (req, res) => {
      const { id } = req.params;
      db.run(`DELETE FROM courses WHERE id = ${id};`, (err) => {
        if (err) {
          res.send(err);
          return;
        }
        res.redirect('/courses');
      });
    });
    

## Итог

Итоговый пример: 
    
    
    import fastify from 'fastify';
    import sqlite3 from 'sqlite3';
    import view from '@fastify/view';
    import pug from 'pug';
    import formbody from '@fastify/formbody';
    
    const app = fastify();
    const port = 3000;
    
    const db = new sqlite3.Database(':memory:');
    
    const prepareDatabase = () => {
      db.serialize(() => {
        db.run(`
          CREATE TABLE courses (
            id INT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT
          );
        `);
      });
    
      const courses = [
        { id: 1, title: 'JavaScript', description: 'Курс по языку программирования JavaScript' },
        { id: 2, title: 'Fastify', description: 'Курс по фреймворку Fastify' },
      ];
    
      const stmt = db.prepare('INSERT INTO courses VALUES (?, ?, ?)');
    
      courses.forEach((course) => {
        stmt.run(course.id, course.title, course.description);
      });
    
      stmt.finalize();
    };
    
    prepareDatabase();
    
    await app.register(formbody);
    await app.register(view, { engine: { pug } });
    
    app.get('/courses', (req, res) => {
      db.all('SELECT * FROM courses', (error, data) => {
        const templateData = {
          courses: data,
          error,
        };
        res.view('courses/index', templateData);
      });
    });
    
    app.post('/courses/:id', (req, res) => {
      const { id } = req.params;
      const { title, description } = req.body;
      const stmt = db.prepare('INSERT INTO courses(title, description) VALUES (?, ?)');
      stmt.run([title, description], function (error) {
        if (error) {
          const templateData = {
            error,
            course: { title, description },
          };
          res.view('/course/new', templateData);
          return;
        }
        res.redirect(`/courses/${this.lastID}`);
      });
    });
    
    app.get('/courses/:id', (req, res) => {
      const { id } = req.params;
      db.get(`SELECT * FROM courses WHERE id = ${id}`, (err, data) => {
        const templateData = {
          course: data,
          error,
        };
        res.view('courses/show', templateData);
      });
    });
    
    app.patch('/courses/:id', (req, res) => {
      const { id } = req.params;
      const { title, description } = req.body;
      const stmt = db.prepare('UPDATE courses SET title = ?, description = ? WHERE id = ?');
      stmt.run([title, description, id], (error) => {
        if (error) {
          const templateData = {
            error,
            course: { title, description },
          };
          res.view('courses/edit', templateData);
          return;
        }
        res.redirect('/courses');
      });
    });
    
    app.delete('/courses/:id', (req, res) => {
      const { id } = req.params;
      const stmt = db.prepare('DELETE FROM courses WHERE id = ?');
      stmt.run(id, (err) => {
        if (err) {
          res.send(err);
          return;
        }
        res.redirect('/courses');
      });
    });
    
    app.listen({ port }, () => {
      console.log(`Example app listening on port ${port}`);
    });
    

* * *

#### Самостоятельная работа

  1. Проделайте все шаги из урока у себя на компьютере на примере сущности курсов. Внесите в свое приложение и репозиторий курсов изменения, так, чтобы репозитории работали с базой данных
  2. Сделайте то же самое для сущности пользователя
  3. Залейте изменения на GitHub



* * *

#### Дополнительные материалы

  1. База данных sqlite3
