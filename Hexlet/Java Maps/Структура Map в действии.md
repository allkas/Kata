---
tags: [java, collections, hashmap, hexlet]
source: "Java Maps"
---

# Структура Map в действии

Одна из самых простых и показательных задач при работе с `HashMap` это подсчет слов в предложении. В этой задаче формируется `Map`, в котором ключ — это слово из предложения, а значение — это количество раз, которое слово встретилось в тексте.

Для реализации этой задачи понадобится выполнить следующие шаги:

  1. Разбить предложение на список слов.
  2. Инициализировать `HashMap` в который мы будем складывать слова и частоту их употребления.
  3. Обойти список слов и добавить их в `HashMap`, в котором ключом будет само слово, а значением количество упоминаний. Если ключ встречается первый раз, то значением будет единица, иначе нужно текущее значение увеличивать на единицу.


    
    
    var text = "one two three two one one four";
    // Разбивает строку на части по разделителю
    var words = text.split(" ");
    
    var wordsFrequency = new HashMap<String, Integer>();
    for (var word : words) {
        if (wordsFrequency.containsKey(word)) {
            var count = wordsFrequency.get(word);
            wordsFrequency.put(word, count + 1);
        } else {
            wordsFrequency.put(word, 1);
        }
    }
    System.out.println(wordsFrequency);
    // => {four=1, one=3, two=2, three=1}
    

Этот код можно упростить так, что в нем не будет условных конструкций. Для этого понадобится метод `getOrDefault()`. 
    
    
    var text = "one two three two one one four";
    var words = text.split(" ");
    
    var wordsFrequency = new HashMap<String, Integer>();
    for (var word : words) {
        var count = wordsFrequency.getOrDefault(word, 0);
        wordsFrequency.put(word, count + 1);
    }
    System.out.println(wordsFrequency);
    

Формирование `Map` во время обхода какого-то списка, достаточно распространенная задача в программировании. Несмотря на разницу в данных и условиях, общая концепция создания и наполнения `Map` остается одинаковой.

Для более глубокого понимания темы мы рекомендуем просмотреть видео лекцию, которая является дополнительным материалом к данному курсу:
