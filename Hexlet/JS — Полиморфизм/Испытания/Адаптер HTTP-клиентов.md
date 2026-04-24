---
tags: [hexlet, ispytanie, javascript, oop]
source: "JS — Полиморфизм"
---

# Адаптер HTTP-клиентов

## Задание

#  JavaScript: Адаптер HTTP-клиентов 

JS: Полиморфизм 7 сообщений

Начать испытание 

В JavaScript для запросов по сети обычно используется один из HTTP-клиентов - _fetch_ или _axios_. Они появились в разное время и имеют разные интерфейсы и форматы ответов. В этом упражнении нам предстоит разработать свой адаптер над этими клиентами. Его интерфейс будет от _axios_ , а формат ответов от _fetch_.

> **Важно** : решите это упражнение без использования классов
    
    
    import createHttpClient from './src/index.js';
    
    const httpClient = createHttpClient('axios');
    // клиент создаётся как инстанс axios
    const instance = httpClient({ baseURL: 'http://localhost:8080' }); // axios.create(config)
    // клиент содержит методы, подобно axios
    const response = await instance.post('/students', { username: 'hello', password: 'world' }); // axios.post(url, data)
    // get-запрос с query string на http://site.com/user?username=hello
    const userNames = await instance.get('/students', { params: { partOfName: 'hel' } }); // axios.get(url, params)
    // ошибки с сайта не выбрасываются, а считаются валидным ответом. Как в fetch
    const failedRequest = await instance.post('/students', { username: 'foo' }, { returnUsers: true }); // axios.post(url, data, params)
    
    // ответы от клиента подобны fetch
    console.log(response.ok); // => true
    console.log(response.status); // => 201
    console.log(userNames.ok); // => true
    console.log(userNames.status); // => 200
    await userNames.json(); // ['hello']
    
    console.log(failedRequest.ok); // => false
    console.log(failedRequest.status); // => 400
    await failedRequest.text(); // "Не указано имя или пароль"
    

## src/index.js

Реализуйте и экспортируйте по умолчанию функцию, возвращающую адаптер HTTP-клиента по его названию.

## src/axiosAdapter.js

Реализуйте обработчик ответа для _axios_ и два метода HTTP-клиента: `post`, `patch`.

Обработчик ответа должен возвращать объект, аналогичный ответу _fetch_ , со следующими свойствами:

  * `ok` \- результат выполнения запроса
  * `status` \- код HTTP-ответа
  * `json()` \- функция, возвращающая Promise. После его разрешения отдаётся JSON-ответ ресурса (body)
  * `text()` \- функция, возвращающая Promise. После его разрешения отдаётся текстовый ответ ресурса (body)



## src/fetchAdapter.js

Реализуйте обработчик параметров запроса для _fetch_ и два метода HTTP-клиента: `post`, `patch`.

Каждый метод принимает параметры запроса по интерфейсу _axios_ , необходимо взять из него нужные данные, корректно сформировать query string, body и устанавливать правильный HTTP-метод.

### Подсказки

В коде оставлены комментарии, которые помогут в решении.

Документация:

  * Документация fetch на MDN
  * Документация axios
  * Документация node-fetch
  * Fetch в уроке "AJAX"

## Моё решение

```js
// напиши решение здесь
```
