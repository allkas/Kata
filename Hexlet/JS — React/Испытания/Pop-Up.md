---
tags: [hexlet, ispytanie, javascript, react, frontend]
source: "JS — React"
---

# Pop-Up

## Задание

#  JavaScript: Pop-Up 

JS: React 7 сообщений

Начать испытание 

Это довольно простое задание, но оно хорошо демонстрирует удобство модульности компонентов.

В веб-разработке есть такое понятие как всплывающие окна Pop-Up. Их использование может быть очень разным, это могут быть всплывающие подсказки или даже элементы меню. В этом задании вам нужно реализовать форму регистрации, при наведении курсора на поле, должно всплывать окно с описанием поля. Для всплывающих окон используйте библиотеку reactjs-popup.

Файл _fields.js_ содержит поля, импортируйте их в компонент и используйте для отрисовки. Каждое поле в форме должно иметь _label_ , текст всплывающей подсказки содержится в _description_.

Пример формы:
    
    
    <div id="container" class="container m-3">
      <div class="col-5">
        <h1 class="my-4">Регистрация</h1>
        <form class="">
          <div class="mb-3">
            <label class="form-label" for="firstName">Имя</label>
            <input
              aria-describedby="popup-1"
              type="text"
              id="firstName"
              class="form-control"
            />
          </div>
          <div class="mb-3">
            <label class="form-label" for="lastName">Фамилия</label>
            <input
              aria-describedby="popup-2"
              type="text"
              id="lastName"
              class="form-control"
            />
          </div>
          <div class="mb-3">
            <label class="form-label" for="email">Email</label>
            <input
              aria-describedby="popup-3"
              type="email"
              id="email"
              class="form-control"
            />
          </div>
          <div class="mb-3">
            <label class="form-label" for="password">Пароль</label>
            <input
              aria-describedby="popup-4"
              type="password"
              id="password"
              class="form-control"
            />
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
      </div>
    </div>
    

## Подсказки

  * Документация reactjs-popup

## Моё решение

```js
// напиши решение здесь
```
