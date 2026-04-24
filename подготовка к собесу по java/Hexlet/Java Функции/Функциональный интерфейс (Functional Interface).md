---
tags: [java, functional, hexlet]
source: "Java Функции"
---

# Функциональный интерфейс (Functional Interface)

В Java все реализуется через классы, даже если снаружи так не кажется. Лямбда-функции — не исключение. Чтобы определять лямбда-функции и создавать методы для работы с ними, нужно разобраться с функциональными интерфейсами. Об этом мы и поговорим в нашем уроке.

Функциональный интерфейс — это интерфейс с единственным абстрактным методом. Он "под капотом" используется как тип для соответствующих ему лямбда-функций. Создадим для примера такой интерфейс: 
    
    
    @FunctionalInterface
    public interface Transformer {
        // Имя метода может быть любым
        // Количество параметров может быть любым
        String apply(String input);
    }
    

Теперь мы можем определять лямбда-функции, соответствующие этому интерфейсу, записывать их в переменные и вызывать. 
    
    
    public class LambdaDemo {
        public static void main(String[] args) {
            Transformer upperCaseTransformer = (input) -> input.toUpperCase();
            var result = upperCaseTransformer.apply("hello");
            System.out.println(result); // Outputs: HELLO
        }
    }
    

Из кода выше мы видим, что лямбда-функция это объект, где методом является определение лямбда-функции. Это значит, что мы без проблем можем описывать их в параметрах методов. 
    
    
    public class LambdaDemo {
        // Метод, который принимает лямбду как параметр
        public static String transform(Transformer fn, String param) {
            return fn.apply(param);
        }
    
        public static void main(String[] args) {
            var result = LambdaDemo.transform((input) -> input.toUpperCase(), "hello");
            System.out.println(result); // Outputs: HELLO
        }
    }
    

https://replit.com/@hexlet/java-functions-interface

Некоторые ситуации использования лямбда-функций настолько распространенные, что функциональные интерфейсы для них встроили прямо в Java. В большинстве случаев вы будете встречаться с ними не напрямую, а через код, в котором они уже задействованы. Часть этих интерфейсов мы рассмотрим в будущих уроках.

* * *

#### Дополнительные материалы

  1. Функциональные интерфейсы
