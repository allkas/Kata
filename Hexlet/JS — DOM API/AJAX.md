---
tags: [javascript, dom, browser, hexlet]
source: "JS — DOM API"
---

# AJAX

  * XMLHttpRequest
  * Fetch
  * URL
  * HTTP access control (CORS)



Манипуляции с DOM-деревом делают наши сайты более живыми. Но все же их недостаточно для создания автономных виджетов или полноценных приложений с бэкендом (Single Page Application).

Многие сервисы дают возможность использовать разные виджеты. Возьмем для примера виджет погоды.

Работает это так: в свой HTML-документ вы вставляете код, предоставленный сервисом. Далее этот код подгружает сам виджет и периодически обращается за необходимыми данными на сервер. Это может происходить в тот момент, когда пользователь виджета нажимает на кнопку «Показать погоду на следующую неделю», ведь это требует новых данных.

Ключевая технология в этой истории — механизм для выполнения HTTP-запросов прямо из браузера. Именно его называют **AJAX** , что расшифровывается как _Asynchronous JavaScript and XML_. Несмотря на название, эта технология работает не только с XML.

## XMLHttpRequest

До появления HTML5, браузеры предоставляли специальный объект `XMLHttpRequest`: 
    
    
    // Пример типового запроса с использованием XMLHttpRequest
    // Просто для ознакомления
    
    const request = new XMLHttpRequest();
    request.onreadystatechange = () => {
      if (request.readyState == 4 && request.status == 200) {
        document.getElementById('demo').innerHTML = request.responseText;
      }
    };
    request.open('GET', '/api/v1/articles/152.json', true);
    request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    request.send();
    

Работать с ним было крайне неудобно, поэтому все использовали обертку, созданную в рамках библиотеки JQuery. Подробнее об этом будет в уроке, посвященном JQuery.

## Fetch

С появлением стандарта HTML5 появился новый механизм для HTTP-запросов: 
    
    
    // Пример типового запроса с использованием fetch
    // const promise = fetch(url[, options]);
    fetch('/api/v1/articles/152.json')
      .then((response) => {
        console.log(response.status); // => 200
        console.log(response.headers.get('Content-Type'));
        return response.json();
       })
      .then((article) => {
        console.log(article.title); // => 'Как использовать fetch?'
      })
      .catch(console.error);
    

Как видно, `fetch` — это функция, возвращающая промис. Работать с ней удобно и приятно. А еще благодаря полифилам, можно не переживать, что какой-то браузер не поддерживает этот механизм.

Обратите внимание, что `response.json` тоже возвращает промис. Данные можно получать не только с помощью `json`. Еще можно использовать функции `blob`, `text`, `formData` и `arrayBuffer`.

Отправка формы POST-запросом: 
    
    
    const form = document.querySelector('form');
    
    fetch('/users', {
      method: 'POST',
      body: new FormData(form),
    });
    

Отправка формы как json: 
    
    
    fetch('/users', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: 'Hubot',
        login: 'hubot',
      })
    })
    

При всех своих преимуществах `fetch` — это довольно низкоуровневый механизм. Например, при работе с JSON нам придется самостоятельно выставлять заголовки и делать разные манипуляции с данными, которые можно было бы автоматизировать.

На практике это привело к созданию различных библиотек, которые работают схожим образом, но дают гораздо больше возможностей. Причем многие из этих библиотек изоморфные, то есть работают одинаково и в браузере, и на сервере. Одна из самых популярных библиотек — это axios.

## URL

Клеить строчки для работы с путями или URL-адресами — это плохая идея. Можно легко ошибиться и приходится выполнять работу, которую может выполнять машина.

С одной стороны, всегда можно воспользоваться сторонними библиотеками, которых достаточно много. Но с другой стороны, в браузерах уже есть встроенный для этого механизм. Для старых браузеров его обычно добавляют полифилами: 
    
    
    const url = new URL('../cats', 'http://www.example.com/dogs');
    console.log(url.hostname); // => www.example.com
    console.log(url.pathname); // => /cats
    
    url.hash = 'tabby';
    console.log(url.href); // => http://www.example.com/cats#tabby
    
    url.pathname = 'démonstration.html';
    console.log(url.href); // => http://www.example.com/d%C3%A9monstration.html
    

Что особенно приятно, `fetch` умеет работать с объектом `URL` напрямую: 
    
    
    const response = await fetch(new URL('http://www.example.com/démonstration.html'));
    

А вот как можно работать с query-параметрами: 
    
    
    // https://some.site/?id=123
    const parsedUrl = new URL(window.location.href);
    console.log(parsedUrl.searchParams.get('id')); // => 123
    parsedUrl.searchParams.append('key', 'value');
    console.log(parsedUrl.toString()); // => https://some.site/?id=123&key=value
    

## HTTP access control (CORS)

В отличие от бэкенда, HTTP-запросы на клиенте могут использоваться злоумышленниками для кражи данных. Поэтому браузеры контролируют, куда и как делаются запросы.

Подробно об этом механизме можно прочитать тут

* * *

#### Дополнительные материалы

  1. Что такое API
  2. Протокол HTTP
  3. HTTP API
