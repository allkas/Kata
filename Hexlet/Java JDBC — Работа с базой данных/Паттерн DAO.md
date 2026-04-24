---
tags: [java, jdbc, sql, database, hexlet]
source: "Java JDBC — Работа с базой данных"
---

# Паттерн DAO

Работать напрямую с JDBC в коде не очень удобно из-за большого количества низкоуровневых деталей и повторяющегося шаблонного кода. Кроме того, нам постоянно приходится преобразовывать данные в одну и в другую сторону.

Чтобы решить эту проблему, можно скрыть работу с базой за какой-то абстракцией. Один из вариантов такой изоляции называют **DAO** (_Data Access Object_).

Концепция DAO очень проста. Она сводится к созданию класса под каждую таблицу в базе данных. В классе реализуются методы, которые сохраняют, удаляют или ищут сущности в этой таблице. Когда речь идет о пользователях, наш класс DAO может выглядеть так: 
    
    
    import java.sql.Connection;
    import java.sql.SQLException;
    // Тут еще импорт класса User
    
    public class UserDAO {
        private Connection connection;
    
        public UserDAO(Connection conn) {
            connection = conn;
        }
    
        public void save(User user) throws SQLException {
            // Если пользователь новый, выполняем вставку
            // Иначе обновляем
            if (user.getId() == null) {
                var sql = "INSERT INTO users (username, phone) VALUES (?, ?)";
                try (var preparedStatement = connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
                    preparedStatement.setString(1, user.getName());
                    preparedStatement.setString(2, user.getPhone());
                    preparedStatement.executeUpdate();
                    var generatedKeys = preparedStatement.getGeneratedKeys();
                    // Если идентификатор сгенерирован, извлекаем его и добавляем в сохраненный объект
                    if (generatedKeys.next()) {
                        // Обязательно устанавливаем id в сохраненный объект
                        user.setId(generatedKeys.getLong(1));
                    } else {
                        throw new SQLException("DB have not returned an id after saving an entity");
                    }
                }
            } else {
                // Здесь код обновления существующей записи
            }
        }
    
        // Возвращается Optional<User>
        // Это упрощает обработку ситуаций, когда в базе ничего не найдено
        public Optional<User> find(Long id) throws SQLException {
            var sql = "SELECT * FROM users WHERE id = ?";
            try (var stmt = connection.prepareStatement(sql)) {
                stmt.setLong(1, id);
                var resultSet = stmt.executeQuery();
                if (resultSet.next()) {
                    var username = resultSet.getString("username");
                    var phone = resultSet.getString("phone");
                    var user = new User(username, phone);
                    user.setId(id);
                    return Optional.of(user);
                }
                return Optional.empty();
            }
        }
    }
    

Метод `save()` в этом классе не только сохраняет данные в базу, но и изменяет переданный объект, устанавливая внутри него идентификатор. Зачем это нужно? Код приложения работает с объектом, а не с базой напрямую. Соответственно, любые изменения в базе должны отражаться на объекте.

Если бы мы не установили идентификатор после сохранения пользователя, то не смогли бы:

  * Формировать ссылки — например, ссылку на редактирование пользователя
  * Сравнивать объекты друг с другом
  * Отличать существующих пользователей от новых, которых мы еще не сохранили в базу данных
  * Обеспечить работу кода так, чтобы полноценная версия `save()` проверяла наличие идентификатора и выполняла обновление данных, если его нет



Метод `find()` возвращает `Optional`, а не просто найденный объект. Это помогает избежать возврата `null` в тех случаях, когда запись не найдена. Возврат `null` требовал бы от программиста постоянно помнить о проверке на существование объекта и выполнять ее: 
    
    
    // Если забыть сделать проверку, можно получить NullPointerException
    if (user != null) {
        // Тут логика
    }
    

По такому же принципу построен Spring Boot, с которым мы познакомимся в другом курсе. Рассмотрим еще несколько примеров использования DAO: 
    
    
    var conn = /* Устанавливаем соединение с базой данных */
    var dao = new UserDAO(conn);
    
    var user = new User("Maria", "888888888");
    user.getId(); // null
    dao.save(user);
    user.getId(); // Здесь уже выводится какой-то id
    
    // Возвращается Optional<User>
    var user2 = dao.find(user.getId()).get();
    user2.getId() == user.getId(); // true
    

* * *

#### Самостоятельная работа

  1. Выполните шаги из урока на своем компьютере
  2. Перепишите код нашего приложения, используя DAO для таблицы пользователей. Чтобы это сделать, создайте класс `User`, который будет представлять пользователя
  3. Добавьте в наш DAO еще один метод, который сможет удалять пользователей из таблицы по их идентификатору
  4. Залейте изменения на GitHub



* * *

#### Дополнительные материалы

  1. Паттерн DAO
