---
tags: [java, streams, functional, hexlet]
source: "Java Стримы"
---

# Поиск элементов (find)

Метод `findFirst()` используется в связке с `filter()` для поиска первого элемента, соответствующего условию фильтрации. 
    
    
    var fruits = List.of("Apple", "Banana", "Apricot", "Orange", "Avocado");
    var maybeFruit = fruits.stream()
                      .filter(s -> s.startsWith("A"))
                      .findFirst();
    System.out.println(maybeFruit); // Optional[Apple]
    

Так как `findFirst()` ищет ровно один элемент, то его результатом является одно значение, а не стрим. Но в отличие от свертки, где результат это то, что находится в аккумуляторе, в случае `findFirst()` в качестве результата возвращается особый тип данных `Optional`. Что это и зачем оно нужно?

По логике кажется, что возвратом должно быть либо конкретное значение если оно найдено, либо `null`. Но в таком случае возникает необходимость постоянной проверки на наличие значения `if (value != null)`. Главная проблема в том, что если забыть сделать ее проверку, компилятор ругаться не будет, `null` является валидным значением для любых не примитивных типов. И такое постоянно происходит в тех местах, где возвратом может быть `null`. Исключение `NullPointerException` одно из самых распространенных в работающих программах на Java.

Чтобы этого не происходило в язык ввели тип `Optional`. Это тип обертка, который хранит реальное значение внутри себя предоставляя к нему доступ через различные методы. Вот как выглядит работа с этим типом: 
    
    
    // Проверяем наличие значения внутри Optional с помощью isPresent()
    if (maybeFruit.isPresent()) {
        // Получаем значение через get()
        System.out.println(maybeFruit.get()); // Apple
    } else {
        System.out.println("Ничего не нашли");
    }
    

Все это работает потому, что отсутствие значения в `Optional` не равно `null`. `Optional` создается следующим образом:

  * `Optional.empty()`: создает `Optional` в случае если значение отсутствует.
  * `Optional.of(value)`: создает `Optional` с `value` внутри.
  * `Optional.ofNullable(value)`: работает как `empty()` если значение `null`, иначе как `of()`.


    
    
    var optional = Optional.of("Hello");
    

## Основные методы Optional

  * `get()`: Возвращает значение если оно есть иначе выбрасывается исключение `NoSuchElementException`.
  * `isPresent()`: Возвращает `true` если значение представлено.
  * `orElse(defaultValue)`: Возвращает значение если оно есть иначе возвращается `defaultValue`.
  * `orElseThrow(exceptionSupplier)`: Возвращает значение, если оно существует, иначе выбрасывает исключение, созданное внутри `exceptionSupplier`.


    
    
    var fruits = List.of("Apple", "Banana", "Apricot", "Orange", "Avocado");
    var maybeFruit = fruits.stream()
                      .filter(s -> s.startsWith("C"))
                      .findFirst();
    
    var fruit1 = maybeFruit.orElse("Strawberry"); // Strawberry
    var fruit2 = maybeFruit.orElseThrow(() -> new RuntimeException("Fruit not found")); // Error
