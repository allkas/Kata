---
tags: [hexlet, java, испытание]
source: "Java Стримы"
---

# IP конвертер

## Задание

Все испытания

#  Java: IP конвертер 

Java: Стримы 1 сообщение

Начать испытание 

## scr/main/java/io/hexlet/App.java

В классе `App` реализуйте публичные статические методы `ipToDec()` и `decToIp()`, которые преобразовывают представление IP-адреса из десятичного формата с точками в 32-битное число в десятичной форме и обратно.

Метод `ipToDec()` принимает на вход строку и должен возвращать число типа `long`. А метод `decToIp()` наоборот: принимает на вход число типа `long`, а возвращает строку.
    
    
    App.ipToDec("128.32.10.1"); // 2149583361
    App.ipToDec("0.0.0.0"); // 0
    App.ipToDec("255.255.255.255"); // 4294967295
    
    App.decToIp(2149583361L); // "128.32.10.1"
    App.decToIp(0L); // "0.0.0.0"
    App.decToIp(4294967295L); // "255.255.255.255"
    

### Подсказки

  * IPv4
  * Используйте метод `Integer.parseInt()` для перевода строки в необходимую систему счисления
  * Изучите возможности метода `Integer.toString()`
  * Дополнительно можно использовать метод StringUtils.leftPad() из библиотеки Apache Commons
  * В решении вам может пригодиться метод `Util.chunk()`, который разбивает строку на массив подстрок определенной длинны:


    
    
      // Первый параметр - строка, второй - размер группы
      String[] result = Util.chunk("abcdef", 2);
      System.out.println(Arrays.toString(result)); // ["ab", "cd", "ef"];
    

Этот метод уже определен в упражнении

## Код

**App.java**
```java
package io.hexlet;

import java.util.stream.Stream;
import java.util.stream.Collectors;
import org.apache.commons.lang3.StringUtils;

class App {
    // BEGIN (write your solution here)
    
    // END
}
```

**Util.java**
```java
package io.hexlet;

class Util {
    public static String[] chunk(String text, int chunkSize) {
        return text.split("(?<=\\G.{" + chunkSize + "})");
    }
}
```

## Моё решение

```java
// напиши решение здесь
```
