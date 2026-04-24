---
tags: [java, streams, functional, hexlet]
source: "Java Стримы"
---

# Стандартные методы свертки (Collectors)

  * Агрегирующие функции
  * Конкатенация
  * Группировка
  * Партицирование



Обработка коллекций через стримы в основном заканчивается двумя вариантами:

  * Из стрима формируется список через `toList()`
  * Стрим сворачивается в какое-то значение через `reduce()`



Второй случай распадается на различные варианты свертки, некоторые из которых встречаются очень часто. Чтобы не делать каждый раз одно и тоже, эти варианты сверток были реализованы в утилитарном классе `Collectors` в виде статических методов. В этом уроке мы рассмотрим эти методы.

Общий принцип работы этих методов такой. В конце цепочки вызывается метод `collect()`, куда передается конкретный коллектор. Пример подсчета количества элементов стрима: 
    
    
    import java.util.stream.Collectors;
    
    var numbers = List.of(1, 2, 3, 4, 5);
    var count = numbers.stream().collect(Collectors.counting());
    System.out.println(count); // => 5
    

## Агрегирующие функции

Классическая свертка это разнообразные функции агрегации данных, такие как поиск суммы, минимального, максимального и среднего. 
    
    
    var numbers = List.of(1, 2, 3, 4, 5);
    var sum = numbers.stream()
                   .collect(Collectors.summingInt(Integer::intValue));
    System.out.println(sum); // => 15
    

Метод `summingInt()` принимает на вход один параметр, с помощью которого извлекается значение из элемента коллекции. В нашем случае мы уже работаем с нужным значением, поэтому используется метод `Integer.intValue()`, который возвращает это же число. В случае использования объектов необходимость такой реализации очевиднее: 
    
    
    var total = employees.stream()
                         .collect(Collectors.summingInt(Employee::getSalary));
                         // Если бы зарплата была типа Double
                         // .collect(Collectors.summingDouble(Employee::getSalary));
    

Точно так же мы можем посчитать среднюю зарплату. 
    
    
    var average = employees.stream()
                           .collect(Collectors.averagingInt(Employee::getSalary));
    

Для подсчета минимального и максимального понадобится добавить обертку в виде метода `Comparator`, который делает необходимое сравнение. 
    
    
    var min = employees.stream()
                       .collect(Collectors.minBy(Comparator.comparingInt(Employee::getSalary)));
    
    var max = employees.stream()
                       .collect(Collectors.maxBy(Comparator.comparingInt(Employee::getSalary)));
    

## Конкатенация

Результат стрима можно преобразовать в строку с помощью `Collectors.joining()`. 
    
    
    var list = List.of("Apple", "Banana", "Cherry");
    var result = list.stream()
                     .collect(Collectors.joining(", "));
    System.out.println(result); // => Apple, Banana, Cherry
    

При необходимости можно указать символы для оборачивания получившейся строки. 
    
    
    var list = List.of("Apple", "Banana", "Cherry");
    var result = list.stream()
                     .collect(Collectors.joining(", ", "[", "]"));
    System.out.println(result); // => [Apple, Banana, Cherry]
    

## Группировка

Самый интересный вариант использования `Collectors` это группировка значений коллекции по каким-то признакам. Если предположить что у нас есть список сотрудников, то мы можем сгруппировать его по подразделению в котором они работают. На выходе получится `Map`. 
    
    
    List<Employee> employees = Arrays.asList(
        new Employee("John Doe", "IT", 70000),
        new Employee("Jane Smith", "HR", 75000),
        new Employee("Mary Johnson", "IT", 60000),
        new Employee("Mike Wilson", "Marketing", 65000)
    );
    
    // Map<String, List<Employee>>
    var employeesByDepartment = employees.stream()
        .collect(Collectors.groupingBy(Employee::getDepartment));
    
    System.out.println(employeesByDepartment);
    // => {
    //   HR=[Employee(name=Jane Smith, department=HR, salary=75000)],
    //   IT=[Employee(name=John Doe, department=IT, salary=70000), Employee(name=Mary Johnson, department=IT, salary=60000)],
    //   Marketing=[Employee(name=Mike Wilson, department=Marketing, salary=65000)]
    // }
    

Существует и более сложная версия группировки, в которой к получившейся группе применяется дополнительная свертка. Например так можно посчитать количество слов в тексте. Ниже пример этого кода, в котором для простоты текст уже разбит на список слов. 
    
    
    var words = Arrays.asList("apple", "banana", "apple", "orange", "banana", "apple");
    
    // Map<String, Long>
    var wordCounts = words.stream()
                          .collect(Collectors.groupingBy(word -> word, Collectors.counting()));
    
    System.out.println(wordCounts); // => {orange=1, banana=2, apple=3}
    

Как работает этот код:

  * Так как в нашем списке обычные слова, а не объекты, лямбда имеет такой вид `word -> word`.
  * Вторым параметром в `Collectors.groupingBy()` передается другой метод коллектора, который выполняется независимо для каждой получившейся группы. Результат этой свертки становится значением в результирующем `Map`. В примере выше, вместо списка слов мы получаем числовое значение.



## Партицирование

Партицирование, это вариант свертки, в котором список значений делится на две группы по заданному условию. Выполняется с помощью метода `Collectors.partitioningBy()`. 
    
    
    // Map<Boolean, List<Integer>>
    var groups = numbers.stream()
                        .collect(Collectors.partitioningBy(n -> n % 2 == 0));
    // {false=[1, 3, 5, 7, 9], true=[2, 4, 6, 8, 10]}
