---
tags: [javascript, objects, hexlet]
source: "JS — Объекты"
---

# Создание новых объектов и spread

Поверхностное копирование (clone) и слияние (merge) можно объединить в одну операцию. Это позволяет обновлять объекты в функциональном стиле, другими словами, мы создаем новые объекты на основе старых, вместо их обновления. Подробнее с такими задачами мы познакомимся ближе к концу профессии, когда пойдет речь про фреймворки. Ниже пример такой операции: 
    
    
    const user = { name: 'Tirion', email: 'support@hexlet.io', age: 44 };
    const data = { name: 'Tirion 2', age: 33 };
    
    // Новый объект с данными user дополненными данными из data
    const copyOfUser = Object.assign({}, user, data);
    

В современном JavaScript добавили специальный оператор, который позволяет выполнять ту же задачу немного короче и, главное, нагляднее. Он называется **spread оператор** (на русском его так и называют «спред-оператор»). Простое поверхностное копирование с помощью спреда: 
    
    
    // Поверхностное копирование
    const copyOfUser = { ...user };
    // Object.assign({}, user);
    

https://repl.it/@hexlet/js-objects-spread-operator-using

Spread оператор – это три точки перед именем переменной (или константы), внутри определения объекта. Он раскладывает соответствующий объект внутри нового объекта. С его помощью можно получить только копию, он не может изменять существующие объекты.

С помощью spread оператора легко расширять новые объекты дополнительными данными: 
    
    
    const user = { name: 'Vasya', age: 11 };
    
    const newUser = { ...user, married: true, age: 25 };
    // Возраст поменялся
    console.log(newUser); // => { name: 'Vasya', married: true, age: 25 }
    

https://repl.it/@hexlet/js-objects-spread-operator-construction

Всё, что появляется с правой стороны спреда, будет иметь приоритет при слиянии, аналогично тому как работает `Object.assign()`. В свою очередь всё что слева — имеет более низкий приоритет: 
    
    
    const user = { name: 'Vasya', age: 11 };
    
    const newUser = { age: 25, married: true, ...user };
    // Возраст остался тем же
    console.log(newUser); // => { name: 'Vasya', married: true, age: 11 }
    

Свойства могут одновременно появляться как слева, так и справа от этого оператора: 
    
    
    const user = { name: 'Vasya', age: 11 };
    
    const newUser = { age: 25, ...user, married: true };
    // Возраст остался тем же
    console.log(newUser); // => { name: 'Vasya', married: true, age: 11 }
    

Сам спред оператор может использоваться в рамках одного объекта любое количество раз: 
    
    
    const user = { name: 'Vasya', married: true, age: 25 };
    const user2 = { name: 'Irina', surname: 'Petrova' };
    
    const mergedObject = { ...user, ...user2 };
    console.log(mergedObject);
    // => { name: 'Irina', married: true, age: 25, surname: 'Petrova' }
    
    // В обратном порядке
    const mergedObject2 = { ...user2, ...user };
    console.log(mergedObject2);
    // => { name: 'Vasya', surname: 'Petrova', married: true, age: 25 }
    

https://repl.it/@hexlet/js-objects-spread-operator-merge-with-same-keys

Наконец, можно объединить и новые свойства и несколько спредов вместе: 
    
    
    const user = { name: 'Irina', age: 25, married: false };
    const user2 = { name: 'Petya', surname: 'Ivanov' };
    
    const newUser = { ...user, married: true, ...user2 };
    console.log(newUser);
    // => { name: 'Petya', age: 25, married: true, surname: 'Ivanov' }
    

https://repl.it/@hexlet/js-objects-spread-operator-flexible
