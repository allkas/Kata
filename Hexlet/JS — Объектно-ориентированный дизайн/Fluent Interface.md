---
tags: [javascript, oop, hexlet]
source: "JS — Объектно-ориентированный дизайн"
---

# Fluent Interface

Domain Specific Language (Предметно-ориентированный язык) — язык, специализированный под конкретную область применения. Структура такого языка отражает специфику решаемых с его помощью задач. Яркий пример подобного языка — библиотека jQuery, с которой знакомо большинство программистов (или хотя бы слышали о ней). С ее помощью управляют отображением и поведением веб-страниц: 
    
    
    // Вызов методов через точку в одной строчке
    // Элементу с классом box выставляется цвет текста и высота
    ('.box').css('color', '#333').height(200);
    

Здесь DSL создан с помощью Текучего интерфейса (Fluent Interface). При таком способе организации кода, обработка выглядит как цепочка подряд идущих методов. На техническом уровне есть ровно два способа создать такой интерфейс.

Первый способ основан на возврате `this` из методов, которые участвуют в построении цепочек. `this` — ссылка на тот объект, в контексте которого вызывается метод, а, следовательно, его можно возвращать как обычное значение. 
    
    
    class Collection {
      constructor(coll) {
        this.coll = coll;
      }
    
      map(fn) {
        // На коллекции вызывается метод map() массива
        this.coll = this.coll.map((element) => fn(element));
    
        return this;
      }
    
      filter(fn) {
        this.coll = this.coll.filter((element) => fn(element));
    
        return this;
      }
    
      // Возвращает саму коллекцию, а не this.
      // Этот метод всегда последний в цепочке вызовов Collection.
      all() {
        return this.coll;
      }
    }
    
    const cars = new Collection([
      { model: 'rapid', year: 2016 },
      { model: 'rio', year: 2013 },
      { model: 'mondeo', year: 2011 },
      { model: 'octavia', year: 2014 },
    ]);
    
    cars.filter((car) => car.year > 2013)
      .map((car) => car.model);
    cars.all(); // [rapid, octavia]
    

У этого способа есть один серьезный недостаток — объект изменяется. Это значит, что нельзя взять и просто так переиспользовать объект-коллекцию для разных выборок, потому что они начнут накладываться друг на друга.

На практике часто используется другой подход, с которым мы уже познакомились в прошлом курсе. Все, что нужно сделать — добавить немного функциональности в ООП, то есть возвращать не `this`, а создавать новый объект того же типа с обновленной коллекцией. 
    
    
    class Collection {
      constructor(coll) {
        this.coll = coll;
      }
    
      map(fn) {
        const newColl = this.coll.map((element) => fn(element));
    
        return new Collection(newColl);
      }
    
      filter(fn) {
        const newColl = this.coll.filter((element) => fn(element));
    
        return new Collection(newColl);
      }
    
      // Возвращает саму коллекцию, а не this.
      // Этот метод всегда последний в цепочке вызовов Collection.
      all() {
        return this.coll;
      }
    }
    
    const cars = new Collection([
      { model: 'rapid', year: 2016 },
      { model: 'rio', year: 2013 },
      { model: 'mondeo', year: 2011 },
      { model: 'octavia', year: 2014 },
    ]);
    
    const filteredCars = cars.filter((car) => car.year > 2013);
    const mappedCars = filteredCars.map((car) => car.model);
    mappedCars.all(); // [rapid, octavia]
    cars.all();
    // [
    //   { model: 'rapid', year: 2016 },
    //   { model: 'rio', year: 2013 },
    //   { model: 'mondeo', year: 2011 },
    //   { model: 'octavia', year: 2014 },
    // ]
    

Теперь каждый вызов возвращает новый объект. Такой код значительно безопаснее в использовании и позволяет без проблем переиспользовать новые коллекции. Изменение одной не приведет к автоматическому изменению всех остальных.

* * *

#### Дополнительные материалы

  1. Текучий интерфейс
  2. JS: Коллекции
