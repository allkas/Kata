---
tags: [javascript, testing, hexlet]
source: "JS — Автоматическое тестирование"
---

# Библиотека power-assert

У обычных утверждений есть мощная альтернатива: power-assert. Эта библиотека добавляет магию в привычный инструмент.

Вот пример проверки с использованием стандартного модуля _assert_ : 
    
    
    const user = {
      name: 'Madonna',
      friends: ['Kate', 'Michel'],
      email: 'madonna@example.com',
    };
    
    assert(user.name === 'Michel');
    
    // AssertionError [ERR_ASSERTION]: The expression evaluated to a falsy value:
    //  assert(user.name === 'Michel')
    

В выводе видно само утверждение и результат проверки. Но непонятно, что за объект `user` и какая у него структура. Для получения этой информации придётся включаться в отладку. Но вместо этого можно воспользоваться библиотекой _power-assert_ : 
    
    
    import assert from 'power-assert';
    
    // Весь код остаётся тем же самым
    const user = {
      name: 'Madonna',
      friends: ['Kate', 'Michel'],
      email: 'madonna@example.com',
    };
    
    // Интерфейс библиотеки power-assert на 100% совместим со встроенным модулем assert.
    assert(user.name === 'Michel');
    

И посмотреть вывод: 
    
    
    AssertionError [ERR_ASSERTION]:   # test.js:10
    
      assert(user.name === 'Michel')
             |    |    |
             |    |    false
             |    "Madonna"
             Object{name:"Madonna",friends:#Array#,email:"madonna@example.com"}
    
      --- [string] 'Michel'
      +++ [string] user.name
      @@ -1,6 +1,7 @@
       M
      -ichel
      +adonna
    

Попробуйте остановиться и внимательно изучить этот вывод. Что здесь показано? _power-assert_ облегчает отладку настолько, насколько это возможно. Он показывает значение каждого объекта и результат каждой операции, входящей в выражение, переданное в функцию _assert_. Кроме того, в конце он сравнивает строки и говорит, в чём конкретно было различие между ними.

Вот ещё один интересный пример из документации: 
    
    
    import assert from 'power-assert';
    
    const array = [1, 2, 3];
    const zero = 0;
    const two = 2;
    
    assert(array.indexOf(zero) === two);
    
    // AssertionError [ERR_ASSERTION]:   # test.js:7
    //
    //   assert(array.indexOf(zero) === two)
    //          |     |       |     |   |
    //          |     |       |     |   2
    //          |     -1      0     false
    //          [1,2,3]
    //
    //   [number] two
    //   => 2
    //   [number] array.indexOf(zero)
    //   => -1
    
    

Впечатляет? Большинство современных фреймворков не выдаёт настолько удобный вывод, насколько это делает _power-assert_. Его можно интегрировать с чем угодно, но потребуются дополнительные инструменты, чтобы получить такое отображение - это Babel / Webpack или другие библиотеки, указанные в документации. Пример использования _power-assert_ с Babel:

https://repl.it/@hexlet/js-testing-power-asserts-methods#index.test.js

* * *

#### Дополнительные материалы

  1. Что такое @@ -1,6 +1,7 @@ в выводе
