---
tags: [java, spring, spring-boot, hexlet]
source: "Java Корпоративные приложения на Spring Boot"
---

# Объект ResponseEntity

В некоторых ситуациях обработчики должны менять код ответа или добавлять свои заголовки. Сделать это можно с помощью возврата специального объекта `ResponseEntity`, который позволяет изменять HTTP-ответ.

Допустим, у нас есть обработчик, возвращающий список страниц `Page`. При этом мы хотим добавить заголовок `X-Total-Count`, который бы указывал на общее количество страниц: 
    
    
    @SpringBootApplication
    @RestController
    public class Application {
        private List<Page> pages = new ArrayList<Page>();
    
        public static void main(String[] args) {
            SpringApplication.run(Application.class, args);
        }
    
        @GetMapping("/pages")
        public List<Page> index() {
            return pages;
        }
    }
    

Чтобы это сделать, нам нужно импортировать `ResponseEntity`. С его помощью мы соберем ответ и вернем его наружу: 
    
    
    // Остальные импорты
    import org.springframework.http.ResponseEntity;
    
    @SpringBootApplication
    @RestController
    public class Application {
        private List<Page> pages = new ArrayList<Page>();
    
        public static void main(String[] args) {
            SpringApplication.run(Application.class, args);
        }
    
        @GetMapping("/pages")
        public ResponseEntity<List<Page>> index(@RequestParam(defaultValue = "10") Integer limit) {
            var result = pages.stream().limit(limit).toList();
    
            return ResponseEntity.ok()
                    .header("X-Total-Count", String.valueOf(pages.size()))
                    .body(result);
        }
    
        @GetMapping("/pages/{id}")
        public ResponseEntity<Page> show(@PathVariable String id) {
            var page = pages.stream()
                .filter(p -> p.getId().equals(id))
                .findFirst();
            return ResponseEntity.of(page);
        }
    }
    

Обсудим этот код подробнее. Здесь `ResponseEntity` — это билдер. Его сборка начинается с методов, определяющих код возврата: `ok()` соответствует коду 200, `created()` — коду 201 и так далее. Дальше можно задавать хедеры и передавать тело ответа.

Использование `ResponseEntity` меняет тип возвращаемого значения так, что изначальное значение оборачивается в `ResponseEntity`. Это значит, что с его введением придется работать через него целиком. Например, уже не получится просто так вернуть объект с данными, его нужно будет передавать в метод `body()`.

В работе `ResponseEntity` вам пригодится еще три метода:

  * `status()`, чтобы указать произвольный статус
  * `of()`, чтобы работать с `Optional`
  * `ok()`, который принимает тело ответа и немного укорачивает запись. Это полезно, когда не нужно вызывать дополнительные методы



* * *

#### Дополнительные материалы

  1. Официальная документация
