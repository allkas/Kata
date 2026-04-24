---
tags: [java, oop, classes, hexlet]
source: "Java Классы"
---

# Lombok

  * Решение с Lombok
  * @ToString
  * @EqualsAndHashCode



В Java разработчики часто сталкиваются с необходимостью написания повторяющегося шаблонного кода. К таким элементам относятся конструкторы, геттеры и сеттеры. Это может приводить к значительному увеличению объема кода, особенно в больших проектах.

Рассмотрим класс `Post`. Он содержит пять полей, включающих стандартные конструкторы и методы доступа. Это типичный пример шаблонного кода, который встречается во многих классах. 
    
    
    import java.time.LocalDate;
    
    public class Post {
        private Long id;
        private Long authorId;
        private String slug;
        private String name;
        private String body;
        private LocalDate createdAt;
    
        // Конструктор по умолчанию
        public Post() {
        }
    
        // Конструктор со всеми полями
        public Post(Long id, Long authorId, String slug, String name, String body, LocalDate createdAt) {
            this.id = id;
            this.authorId = authorId;
            this.slug = slug;
            this.name = name;
            this.body = body;
            this.createdAt = createdAt;
        }
    
        public Long getId() {
            return id;
        }
    
        public void setId(Long id) {
            this.id = id;
        }
    
        public Long getAuthorId() {
            return authorId;
        }
    
        public void setAuthorId(Long authorId) {
            this.authorId = authorId;
        }
    
        public String getSlug() {
            return slug;
        }
    
        public void setSlug(String slug) {
            this.slug = slug;
        }
    
        public String getName() {
            return name;
        }
    
        public void setName(String name) {
            this.name = name;
        }
    
        public String getBody() {
            return body;
        }
    
        public void setBody(String body) {
            this.body = body;
        }
    
        public LocalDate getCreatedAt() {
            return createdAt;
        }
    
        public void setCreatedAt(LocalDate createdAt) {
            this.createdAt = createdAt;
        }
    }
    

Мы еще не написали ничего полезного, но класс уже занимает больше 70 строк. А что будет когда у нас будет 20 полей или 30? Для прикладного кода это вполне нормально. При этом самих классов сотни и тысячи. Некоторых разработчиков такая ситуация устраивает, так как редактор сам генерирует весь нужный код, но некоторые все равно хотели бы избавиться от шаблонного кода и даже не генерировать его.

## Решение с Lombok

Сама Java не позволяет так сделать, но позволяет Lombok. Lombok – это библиотека, которая позволяет убрать шаблонный код при создании классов. Возьмем класс из примера выше и перепишем его с использованием Lombok. Вот что у нас получится. 
    
    
    import java.time.LocalDate;
    
    import lombok.AllArgsConstructor;
    import lombok.Getter;
    import lombok.NoArgsConstructor;
    import lombok.Setter;
    
    @Getter
    @Setter
    @NoArgsConstructor
    @AllArgsConstructor
    public class Post {
        private Long id;
        private Long authorId;
        private String slug;
        private String name;
        private String body;
        private LocalDate createdAt;
    }
    

Размер класса сократился до примерно 10 строк, хотя то что мы получили – это всего лишь визуальное сокращение кода. Во время исполнения этот код будет заменен на обычный класс Java со всеми нужными методами.

Самое необычное в коде выше это блок кода над классом: 
    
    
    import lombok.AllArgsConstructor;
    import lombok.Getter;
    import lombok.NoArgsConstructor;
    import lombok.Setter;
    
    @Getter
    @Setter
    @NoArgsConstructor
    @AllArgsConstructor
    

То, что мы здесь видим, называется аннотациями. Аннотации в Java это тоже код. Они начинаются с символа _@_ за которым идет имя аннотации. Аннотации могут сопровождаться параметрами в стиле, похожем на вызов функций. 
    
    
    @Annotation(key=value)
    // определение какого-нибудь класса
    

То что мы увидели выше, называется аннотациями класса. Встречаются и другие аннотации, привязанные к свойствам, методам и даже параметрам методов. Со временем мы разберемся со всеми видами и будем их активно использовать в своем коде не только в связке с Lombok.

Сами по себе аннотации на код никак не влияют. Аннотации лишь добавляют информацию к классу, которую затем может прочитать и использовать другой код. В нашем случае это будет делать плагин Lombok для Gradle, который подключается к проекту таким образом: 
    
    
    plugins {
        id("io.freefair.lombok") version "8.4"
    }
    

Lombok встраивается в процесс компиляции, во время которой он "наполняет" классы необходимыми методами. Из-за этого, помимо gradle-плагина, для поддержки Lombok понадобится добавить плагин в используемый редактор. Подробнее установка Lombok описана на официальном сайте.

За что отвечает каждая аннотация выше?

  * `@Getter`: Генерирует стандартные геттеры для всех полей класса.
  * `@Setter`: Генерирует стандартные сеттеры для всех полей класса.
  * `@NoArgsConstructor`: Генерирует пустой конструктор. Используется только тогда, когда определен хотя бы один не пустой конструктор.
  * `@AllArgsConstructor`: Генерирует конструктор со всеми полями. Поля в конструкторе перечислены в том же порядке, в котором они определены в классе.



## @ToString

`@toString` еще одна полезная аннотация, которая генерирует метод `toString()` добавляя в него все не статические поля класса. 
    
    
    import lombok.ToString;
    
    @ToString
    // Остальные аннотации
    public class User {
        private String name;
        private int age;
        private String email;
    }
    

Использование и вывод: 
    
    
    var user = new User("John Doe", 30, "john.doe@example.com");
    System.out.println(user);
    // => User(name=John Doe, age=30, email=john.doe@example.com)
    

## @EqualsAndHashCode

Аннотация `@EqualsAndHashCode` генерирует методы `equals()` и `hashCode()` соответственно. По умолчанию, в эти методы включаются все не статические поля класса. Пример с пользователем. 
    
    
    import lombok.EqualsAndHashCode;
    
    @EqualsAndHashCode
    // Остальные аннотации
    public class Person {
        private String name;
        private int age;
        private String email;
    }
    

Использование: 
    
    
    var person1 = new Person("John Doe", 30, "john.doe@example.com");
    var person2 = new Person("John Doe", 30, "john.doe@example.com");
    
    System.out.println(person1.equals(person2)); // true
    System.out.println(person1.hashCode()); // hashCode of person1
    System.out.println(person2.hashCode()); // hashCode of person2 (идентичен с person1)
    

Если поведение необходимо изменить, то `@EqualsAndHashCode` позволяет это сделать описав те поля, которые нужно явно включить или исключить. Предположим что мы хотим сравнивать пользователей только на основе email, тогда код примет следующий вид: 
    
    
    @EqualsAndHashCode(onlyExplicitlyIncluded = true)
    public class Person {
        private String name;
        private int age;
    
        @EqualsAndHashCode.Include
        private String email;
    }
    

* * *

#### Дополнительные материалы

  1. Установка Lombok
