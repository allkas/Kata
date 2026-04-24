---
tags: [java, oop, hexlet]
source: "Java Основы ООП"
---

# Reflections

Видео может быть заблокировано из-за расширений браузера. В статье вы найдете решение этой проблемы.

  * Получение доступа к полям класса
  * Вызов методов
  * Конструкторы
  * Аннотации



Рефлексия – процесс, во время которого программа может отслеживать и модифицировать собственную структуру и поведение во время выполнения

## Получение доступа к полям класса
    
    
    User user = new User();
    System.out.println(user); // => User{id=null, name='null'}
    System.out.println(user.getClass()); // => class User
    
    // Можем получить доступ к private полям класса
    // Получаем все поля класса
    Field[] fields = user.getClass().getDeclaredFields();
    for (Field field : fields) {
        System.out.println(field);
    }
    // => private java.lang.Integer User.id
    // => private java.lang.String User.name
    
    
    // Устанавливаем значение поля name без setter-а
    try {
        Field field = user.getClass().getDeclaredField("name");
        field.setAccessible(true);
        field.set(user, "Egor");
    } catch (NoSuchFieldException | IllegalAccessException e) {
        e.printStackTrace();
    }
    System.out.println(user); // => User{id=null, name='Egor'}
    
    
    // устанавливаем значение поля id без setter-а
    try {
        Field field = user.getClass().getDeclaredField("id");
        field.setAccessible(true);
        field.set(user, 1);
    } catch (NoSuchFieldException | IllegalAccessException e) {
        e.printStackTrace();
    }
    System.out.println(user); // => User{id=1, name='Egor'}
    

## Вызов методов
    
    
    // выводим все доступные методы класса
    for (Method method: user.getClass().getMethods()) {
        System.out.println(method);
    }
    System.out.println("===========================");
    
    // выводим все методы класса
    for (Method method : user.getClass().getDeclaredMethods()) {
        System.out.println(method);
    }
    // => public void REPL.User.setId(java.lang.Integer)
    // => public java.lang.String User.getName()
    // => public java.lang.String User.toString()
    // => public void REPL.User.setName(java.lang.String)
    // => public java.lang.Integer User.getId()
    
    
    // вызов доступного метода
    try {
        Method toString = user.getClass().getDeclaredMethod("toString");
        System.out.println(toString.invoke(user));
    } catch (NoSuchMethodException | IllegalAccessException | InvocationTargetException e) {
        e.printStackTrace();
    }
    // => User{id=1, name='Egor'}
    
    // вызов недоступного метода
    
    try {
        Method getGreetingMsg = user.getClass().getDeclaredMethod("getGreetingMsg");
        getGreetingMsg.setAccessible(true);
        System.out.println(getGreetingMsg.invoke(user));
    } catch (NoSuchMethodException | IllegalAccessException | InvocationTargetException e) {
        e.printStackTrace();
    }
    // java.lang.NoSuchMethodException: User.getGreetingMsg()
    

## Конструкторы
    
    
    for (Constructor constructor: user.getClass().getConstructors()) {
        System.out.println(constructor);
    }
    // => public REPL.User()
    
    
    // Создание нового инстанса
    try {
        Class[] params = {String.class, String.class, String.class};
        Constructor constructor = user.getClass().getConstructor(params);
        User u = (User) constructor.newInstance();
        System.out.println(u);
    } catch (NoSuchMethodException | InstantiationException |
    IllegalAccessException | InvocationTargetException e) {
        e.printStackTrace();
    }
    

## Аннотации
    
    
    User user3 = new User();
    for (Field field : user3.getClass().getDeclaredFields()) {
        RandomNumber randomNumber = field.getAnnotation(RandomNumber.class);
        if (randomNumber != null) {
            Random random = new Random();
            int randomValue = random.nextInt(randomNumber.max() - randomNumber.min() + 1) + randomNumber.min();
            try {
                field.setAccessible(true);
                field.set(user3, String.valueOf(randomValue));
            } catch (IllegalAccessException e) {
                e.printStackTrace();
            }
        }
    }
    System.out.println(user3);
    

* * *

#### Дополнительные материалы

  1. Reflection API
