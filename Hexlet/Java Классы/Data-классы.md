---
tags: [java, oop, classes, hexlet]
source: "Java Классы"
---

# Data-классы

Для получения данных извне и передачи их куда-то дальше в Java используются Data-классы. Обычно это связано с любыми внешними источниками данных, базой данных, HTTP, файлами. Если нам нужно получить какие-то данные, например информацию о заказе, нам придется создать класс, который описывает этот заказ. Причем сам класс не будет зависеть от того, из какого источника пришли данные. То же самое работает и в обратном направлении, если нам нужно выгрузить данные, то для этого создаются свои классы, которые содержат только необходимые поля.

Data-классы это обычные классы без поведения. Из-за этого их стараются делать неизменяемыми, или как говорят иммутабельными (immutable), для избежания случайных ошибок. В идеале у этих классов нет сеттеров, а все поля помечены как `final`, что защищает их от изменения. 
    
    
    // DTO - Data Transfer Object
    public class OrderDTO {
        private final int id;
        private final String customerName;
        private final double orderAmount;
    
        // После инициализации финальных полей их больше нельзя менять
        public OrderDTO(int id, String customerName, double orderAmount) {
            this.id = id;
            this.customerName = customerName;
            this.orderAmount = orderAmount;
        }
    
        public int getId() {
            return id;
        }
    
        public String getCustomerName() {
            return customerName;
        }
    
        public double getOrderAmount() {
            return orderAmount;
        }
    }
    

Data-классы это настолько большая часть любого приложения на Java, что в язык была внедрена новая конструкция Record (запись). Записи по своей сути Data-классы. Ниже пример того, как мы бы могли переделать наш `OrderDTO`: 
    
    
    // Неизменяемые по умолчанию и это не меняется
    public record OrderDTO(int id, String customerName, double orderAmount) {
    }
    

Запись значительно сокращает количество кода, предоставляя практически такую же функциональность. Но с небольшими отличиями. Геттеры в записях не содержат префикса _get_. 
    
    
    public class Main {
        public static void main(String[] args) {
            // Создаем экземпляры заказа
            Order order1 = new OrderDTO(12345, "Alice Smith", 250.0);
            Order order2 = new OrderDTO(67890, "Bob Johnson", 450.5);
    
            // Получаем доступ к свойствам заказа
            System.out.println("Order 1 Details:");
            System.out.println("Order ID: " + order1.id());
            System.out.println("Customer Name: " + order1.customerName());
            System.out.println("Order Amount: " + order1.orderAmount());
    
            System.out.println("Order 2 Details:");
            System.out.println("Order ID: " + order2.id());
            System.out.println("Customer Name: " + order2.customerName());
            System.out.println("Order Amount: " + order2.orderAmount());
        }
    }
    

Несмотря на синтаксическое превосходство, записи обладают рядом недостатков, которые делают их использование в качестве замены обычных классов неудобным. Сюда входят:

  * Возможность работать только в неизменяемом стиле. Нет сеттеров.
  * Только один конструктор со всеми полями.
  * Нет наследования (иногда нужно).
  * Многие библиотеки и фреймворки до сих пор не совместимы с записями.



Поэтому основным способом по-прежнему является создание обычных классов. И Lombok делает этот процесс достаточно простым. 
    
    
    @Getter
    @AllArgsConstructor
    public class OrderDTO {
        private final int id;
        private final String customerName;
        private final double orderAmount;
    }
