---
tags: [java, functional, hexlet]
source: "Java Функции"
---

# Методы Compute в Map

  * compute()
  * computeIfAbsent()
  * computeIfPresent()



`forEach()` не единственный метод в `Map`, работающий с лямбда-функциями. Кроме него есть набор методов _compute_. Они позволяют вычислять значение динамически, базируясь на том, существует ли запрашиваемый ключ в коллекции или нет.

## compute()

Метод `compute()` обновляет значение ключа в `Map`, на основе логики, заданной внутри лямбда-функции. Эта лямбда-функция получает на вход текущее значение ключа, выполняет с ним необходимые операции и возвращает новое значение. 
    
    
    import java.util.List;
    import java.util.HashMap;
    
    public class WordCountExample {
        public static void main(String[] args) {
            var words = List.of("apple", "banana", "apple", "orange", "banana", "apple");
            var wordCount = new HashMap<String, Integer>();
    
            words.forEach((word) -> {
                // Для данной задачи key не используется
                wordCount.compute(word, (key, count) -> count == null ? 1 : count + 1);
            });
    
            System.out.println(wordCount); // => {orange=1, banana=2, apple=3}
        }
    }
    

В примере выше, метод `compute()` вызывается для каждого слова из списка. Лямбда-функция принимает на вход ключ и значение, которое является количеством повторений слова в списке. Дальше в зависимости от того, первый ли раз встречается это слово или нет, изменяется количество повторений. Без `compute()` нам бы пришлось написать код похожий на этот: 
    
    
    words.forEach((word) -> {
        var count = wordCount.get(word);
        wordCount.put(word, count == null ? 1 : count + 1);
    });
    

Здесь мы встречаемся с интересной особенностью сокращенной версии лямбда-функции. В примерах выше не прописан явно возврат, но он выполняется, иначе значение было бы невозможно использовать. Возврат, в сокращенной версии лямбда-функции, выполняется автоматически. Полная версия выглядела бы так: 
    
    
    wordCount.compute(word, (key, count) -> {
        return count == null ? 1 : count + 1;
    });
    

## computeIfAbsent()

Метод `computeIfAbsent()` отличается от `compute()`, тем, что лямбда вызывается только в том случае, если ключа в коллекции до этого не было. С его помощью, например, реализуется кеш, специальное хранилище, которое хранит данные, полученные в результате выполнения тяжелой операции. Это позволяет экономить ресурсы на повторных запросах, которые проходят уже без вычисления. 
    
    
    import java.util.Map;
    import java.util.HashMap;
    
    public class CacheExample {
        private static Map<String, Integer> cache = new HashMap<>();
    
        public static int computeExpensiveOperation(String key) {
            // Симулируем тяжелую операцию
            return key.length();
        }
    
        public static int getValue(String key) {
            return cache.computeIfAbsent(key, (k) -> CacheExample.computeExpensiveOperation(k));
        }
    
        public static void main(String[] args) {
            System.out.println(getValue("hello")); // => 5
            System.out.println(getValue("java"));  // => 4
            System.out.println(getValue("hello")); // => 5 (получено из кеша, вычисление не выполняется)
        }
    }
    

## computeIfPresent()

Метод `computeIfPresent()` отличается от `compute()` тем, что лямбда вызывается только в том случае, если ключ уже был добавлен в коллекцию. Ниже пример кода, который применяет скидку к товарам, находящимся внутри коллекции без проверки того, есть ли они там на самом деле: 
    
    
    import java.util.HashMap;
    
    public class DiscountExample {
        public static void main(String[] args) {
            var prices = new HashMap<String, Double>();
            prices.put("T-shirt", 20.0);
            prices.put("Jeans", 40.0);
    
            // Применяет 10% скидку только если такой товар существует
            prices.computeIfPresent("Jeans", (key, value) -> value * 0.9);
    
            // Ничего не происходит, так как такого товара нет
            prices.computeIfPresent("Socks", (key, value) -> value * 0.9);
    
            System.out.println(prices); // => {T-shirt=20.0, Jeans=36.0}
        }
    }
    

* * *

#### Дополнительные материалы

  1. Метод compute()
  2. Метод computeIfAbsent()
  3. Метод computeIfPresent()
