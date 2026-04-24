---
tags: [java, streams, functional, hexlet]
source: "Java Стримы"
---

# Отображение (map)

Базовая операция в стримах это `map()` (отображение). Она берет исходный список и формирует на его основе другой, преобразуя каждый элемент по указанным правилам. Возьмем для примера задачу со списком чисел, которые нужно округлить. Как бы мы решили эту задачу без стримов: 
    
    
    var numbers = List.of(1.2, 2.5, 3.7, 4.4, 5.9);
    
    // Список для хранения округленных чисел
    var roundedNumbers = new ArrayList<>();
    
    // Цикл для округления каждого числа и добавления его в новый список
    for (var number : numbers) {
        var rounded = Math.round(number);
        roundedNumbers.add(rounded);
    }
    
    // Вывод округленных чисел
    System.out.println(roundedNumbers); // Вывод: [1, 3, 4, 4, 6]
    

Отображение, позволяет скрыть процесс перебора и сфокусироваться на том что мы хотим получить. Выглядит это так: 
    
    
    var numbers = List.of(1.2, 2.5, 3.7, 4.4, 5.9);
    
    // Применение стрима для округления чисел и сбора их в новый список
    var roundedNumbers = numbers.stream()
                                .map(number -> Math.round(number))
                                // или проще через передачу ссылки
                                // .map(Math::round)
                                .toList();
    
    // Вывод округленных чисел
    System.out.println(roundedNumbers); // Вывод: [1, 3, 4, 4, 6]
    

Метод `map()` принимает как параметр лямбда-функцию, которая должна вернуть значение, вычисленное на базе переданного значения из исходной коллекции. Результатом может быть все что угодно. При этом отображение никогда не меняет размер коллекции, на выходе будет ровно то же, что было на входе.

Еще несколько примеров преобразований: 
    
    
    var solutions = List.of("hexlet", "chatgpt", "google", "youtube");
    
    var result1 = solutions.stream()
                                .map(solution -> solution.toUpperCase())
                                // или
                                // .map(String::toUpperCase)
                                .toList();
    // [HEXLET, CHATGPT, GOOGLE, YOUTUBE]
    
    var result2 = solutions.stream()
                                .map(String::length)
                                // тоже самое что и
                                // .map(solution -> solution.length())
                                .toList();
    // [6, 7, 6, 7]
