---
tags: [java, functional, hexlet]
source: "Java Функции"
---

# Ссылки на методы (Method References)

Ссылка на метод (Method Reference) – это сокращенная форма лямбда выражения для вызова методов. То есть это синтаксический сахар, который делает код короче и проще для чтения. Рассмотрим это на примере. Представьте, что у нас есть список элементов, который мы хотим распечатать на экран. Код, выполняющий эту задачу, может выглядеть так: 
    
    
    var langs = List.of("ruby", "php", "python", "javascript");
    langs.forEach((lang) -> System.out.println(lang));
    

Этот же код можно сделать короче, передавая в метод `forEach()` ссылку на `println()`: 
    
    
    var langs = List.of("ruby", "php", "python", "javascript");
    langs.forEach(System.out::println);
    

Поначалу такой синтаксис кажется непривычным. Со временем в вашем коде будет много лямбда-функций и обработки коллекций. Вы привыкнете к синтаксису и увидите, насколько этот способ привлекателен своей лаконичностью.

Общий синтаксис ссылки на метод выглядит так: 
    
    
    Name::methodName
    

Где _Name_ может быть как объектом так и классом, в зависимости от того, ссылку на что мы хотим получить и как это будет использовано потом. Ниже варианты, которые мы можем использовать. В комментариях показаны эквиваленты с использованием лямбда-функций: 
    
    
    objectName::methodName // (v) -> objectName.methodName(v)
    ClassName::staticMethodName // (v) -> ClassName.staticMethodName(v)
    ClassName::methodName // (v) -> v.methodName()
    

Последний пример часто применяется с `Comparator` при сортировках: 
    
    
    var words = new ArrayList<>(List.of("pear", "apple", "banana"));
    
    words.sort(Comparator.comparingInt(String::length));
    // Эквивалент
    // words.sort((w1, w2) -> Integer.compare(w1.length(), w2.length()));
    System.out.println(words); // Outputs: [pear, apple, banana]
    

Больше примеров мы увидим в курсе по стримам, где подобный синтаксис встречается буквально повсеместно.

* * *

#### Дополнительные материалы

  1. Документация по Method References
