---
tags: [javascript, arrays, hexlet]
source: "JS — Массивы"
---

# Spread и создание новых массивов

У rest есть компаньон – spread. Он имеет такой же синтаксис, но выполняет противоположную задачу: не сворачивает элементы, а наоборот, растягивает их. С его помощью обычно копируют или соединяют массивы.

Представьте, что нам нужно определить массив, добавив туда элементы из другого массива. Такая задача часто встречается при работе со значениями по умолчанию: 
    
    
    const frenchCities = ['paris', 'marseille'];
    const cities = ['milan', 'rome', ...frenchCities];
    // ['milan', 'rome', 'paris', 'marseille']
    
    // Массив frenchCities при этом никак не меняется
    
    // То же самое без spread
    const cities = ['milan', 'rome'].concat(frenchCities);
    

В этом случае `...` — это spread. Он растянул массив, добавив все его элементы в новый массив. Как отличить его от rest? Все дело в контексте использования. Rest появляется слева от знака равно там, где происходит деструктуризация. Spread – справа от знака равно, там где массив формируется.

В отличие от rest, spread может появляться в любой части массива. Например, мы можем дополнить исходный массив не справа, а слева: 
    
    
    const cities = [...frenchCities, 'milan', 'rome'];
    // ['paris', 'marseille', 'milan', 'rome']
    
    // То же самое без spread
    const cities = frenchCities.concat(['milan', 'rome']);
    

И даже посередине: 
    
    
    const cities = ['milan', ...frenchCities, 'rome'];
    // ['milan', 'paris', 'marseille', 'rome']
    
    // Без spread подобный код нельзя выразить одной операцией
    

Spread работает с любым количеством массивов: 
    
    
    const frenchCities = ['paris', 'marseille'];
    const italianCities = ['rome', 'milan'];
    // слияние двух массивов
    const cities = [...frenchCities, ...italianCities];
    // ['paris', 'marseille', 'rome', 'milan']
    
    // То же самое без spread
    const cities = frenchCities.concat(italianCities);
    

## Копирование массива

Spread нередко используется для копирования массива. Копирование предотвращает изменение исходного массива в том случае, когда необходимо менять его копию: 
    
    
    const frenchCities = ['paris', 'marseille'];
    const copy = [...frenchCities];
    copy.push('lyon');
    console.log(copy); // => [ 'paris', 'marseille', 'lyon' ]
    console.log(frenchCities); // => [ 'paris', 'marseille' ]
    
    // То же самое без spread
    const frenchCities = ['paris', 'marseille'];
    const copy = frenchCities.slice();
