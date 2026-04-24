---
tags: [java, jdbc, sql, database, hexlet]
source: "Java JDBC — Работа с базой данных"
---

# Конструкция try-with-resources

Посмотрите на код ниже и попробуйте разобраться, что с ним не так: 
    
    
    var sql = "INSERT INTO users (username, phone) VALUES ('tommy', '123456789')";
    var statement = conn.createStatement();
    statement.executeUpdate(sql);
    statement.close();
    

Этот код написан из предположения, что вызов `statement.executeUpdate(sql)` никогда не приведет к ошибке. А что произойдет, если ошибка случится? Тогда возникнет исключение, и метод `statement.close()` никогда не будет вызван для текущего стейтмента.

Такая ситуация не должна происходить, поэтому нужно делать закрытие в блоке `finally`: 
    
    
    var sql = "INSERT INTO users (username, phone) VALUES ('tommy', '123456789')";
    Statement statement = null;
    try {
        statement = conn.createStatement();
        statement.executeUpdate(sql);
    } finally {
        statement.close();
    }
    

Теперь стейтмент правильно закроется, даже если возникнет ошибка. В теории это выглядит нормально, но на практике за этим сложно уследить. Программисты регулярно забывают добавлять блок `finally`.

Это настолько большая проблема, что создатели Java добавили конструкцию **try-with-resources**. Она позволяет автоматически закрывать объекты, которые реализуют интерфейс `java.lang.AutoCloseable` — это делают все объекты, подразумевающие закрытие.

Рассмотрим тот же пример, но с автоматическим закрытием: 
    
    
    var sql = "INSERT INTO users (username, phone) VALUES ('tommy', '123456789')";
    try (var statement = conn.createStatement()) {
        statement.executeUpdate(sql);
    }
    

Эта конструкция использует точно такое же ключевое слово, как и обработка исключений, но работает немного по-другому. Она отличается синтаксически: в этом случае после `try` идут скобки, в которых выполняется выражение, открывающее соединение. Теперь посмотрим на пример из предыдущего урока, переписанный под автоматическое закрытие: 
    
    
    package io.hexlet;
    
    import java.sql.DriverManager;
    import java.sql.SQLException;
    
    public class Application {
        public static void main(String[] args) throws SQLException {
            // Соединение с базой данных тоже нужно отслеживать
            try (var conn = DriverManager.getConnection("jdbc:h2:mem:hexlet_test")) {
    
                var sql = "CREATE TABLE users (id BIGINT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(255), phone VARCHAR(255))";
                try (var statement = conn.createStatement()) {
                    statement.execute(sql);
                }
    
                var sql2 = "INSERT INTO users (username, phone) VALUES ('tommy', '123456789')";
                try (var statement2 = conn.createStatement()) {
                    statement2.executeUpdate(sql2);
                }
    
                var sql3 = "SELECT * FROM users";
                try (var statement3 = conn.createStatement()) {
                    var resultSet = statement3.executeQuery(sql3);
                    while (resultSet.next()) {
                        System.out.println(resultSet.getString("username"));
                        System.out.println(resultSet.getString("phone"));
                    }
                }
            }
        }
    }
    

* * *

#### Самостоятельная работа

  1. Перепишите код нашего приложения с учетом автоматического закрытия, используя конструкцию _try-with-resources_
  2. Залейте изменения на GitHub



* * *

#### Дополнительные материалы

  1. Официальная документация
