---
tags: [java, generics, hexlet]
source: "Java Дженерики"
---

# Wildcard для спецификации подтипов

Дженерики позволяют нам работать однообразно с любым типом данных, но иногда возникает задача создать дженерик для определенного набора типов. Возьмем для примера задачу поиска среднего значения для списка чисел. Для `Integer` реализация метода выглядит так: 
    
    
    public class Application {
        public static Double average(List<Integer> numbers) {
            // Double
            var sum = 0.0;
            for (var number : numbers) {
                sum += number;
            }
    
            return sum / numbers.size();
        }
    
        public static void main(String[] args) {
            var numbers = List.of(1, 2, 3, 4, 5);
            System.out.println(average(numbers)); // => 3.0
        }
    }
    

Если сделать из метода `average()` дженерик, то он не сработает, так как тип `T` будет `Object`, для которого операция сложения не определена. 
    
    
    public static <T> Double average(List<T> numbers) {
        var sum = 0.0;
        for (var number : numbers) {
            // The operator += is undefined for the argument type(s) double, T
            sum += number;
        }
    
        return sum / numbers.size();
    }
    

Для подобных задач в Java есть механизм _Wildcard_ , с его помощью можно уточнить типы, с которыми работает дженерик. В нашем случае и `Integer` и `Double` являются подтипами `Number`, а значит мы можем написать так: `List<? extends Number>`. В таком случае в метод попадут только числа, какими бы они не были, а типом параметра `numbers` станет `List<Number>`. 
    
    
    public static <T> Double average(List<? extends Number> numbers) {
        var sum = 0.0;
        for (var number : numbers) {
            sum += number;
        }
    
        return sum / numbers.size();
    }
    

Обновленный код почти работает. Он все еще выдает ошибку _The operator += is undefined for the argument type(s) double, Number_ , так как во время сложения получается что тип переменной `sum` это `Double`, а тип переменной `number` \- `Number`. Эта задача решается за счет метода `doubleValue()` определенного у `Number`, который любое число преобразует в `Double`. Рабочий код: 
    
    
    public static <T> Double average(List<? extends Number> numbers) {
        var sum = 0.0;
        for (var number : numbers) {
            sum += number.doubleValue();
        }
    
        return sum / numbers.size();
    }
    

Wildcard не часто используется в прикладном коде, но часто используется в библиотеках. Поэтому его нужно знать на начальном этапе, хотя бы для того, чтобы читать документацию и понимать что там написано.

Для более глубокого понимания темы мы рекомендуем просмотреть видео лекцию, которая является дополнительным материалом к данному курсу:
