---
tags: [sql, database, hexlet]
source: "SQL — Оконные функции"
---

# SUM, COUNT и AVG

Видео может быть заблокировано из-за расширений браузера. В статье вы найдете решение этой проблемы.

  * Выводы



Функции `SUM()`, `COUNT()`, `AVG()` в SQL используются для агрегации данных в столбцах таблицы. Когда вы используете оконные версии функций, вы указываете дополнительное оконное определение в операторе OVER. Это определение определяет, какие строки будут входить в окно для каждой строки результирующего набора данных. Например, вы можете определить окно как `PARTITION BY` для группировки строк по определенному столбцу или `ORDER BY` для упорядочивания строк внутри окна.
    
    
    SELECT
        sh.region,
        SUM(s.price * s.quantity) AS sum_value,
        AVG(s.price * s.quantity) AS avg_value
    FROM sales AS s
    LEFT JOIN customer AS c ON s.customer_id = c.customer_id
    LEFT JOIN shop AS sh ON s.shop_id = sh.shop_id
    GROUP BY sh.region;

region | sum_value | avg_value  
---|---|---  
Vladivostok | 19 | 3.1666666666666667  
Saint-Petersburg | 75 | 3.2608695652173913  
Kaliningrad | 36 | 3.6000000000000000  
Moscow | 106 | 2.8648648648648649  
Tver | 28 | 4.0000000000000000  
Novosibirsk | 53 | 3.1176470588235294  
  
View on DB Fiddle

Теперь применим оконные варианты этих функций:
    
    
    SELECT
        id,
        sale_date,
        price,
        quantity,
        (price * quantity) as value,
        region,
        c.category,
        SUM(s.price * s.quantity) OVER (PARTITION BY region) AS sum_value,
        AVG(s.price * s.quantity) OVER (PARTITION BY region) AS avg_value
    FROM sales AS s
    LEFT JOIN customer AS c ON s.customer_id = c.customer_id
    LEFT JOIN shop AS sh ON s.shop_id = sh.shop_id
    ORDER BY s.id;

id | sale_date | price | quantity | region | category | sum_value | avg_value  
---|---|---|---|---|---|---|---  
1 | 2023-01-01T00:00:00.000Z | 4 | 1 | Moscow | with discount cards | 106 | 2.8648648648648649  
2 | 2023-01-01T00:00:00.000Z | 2 | 2 | Moscow | with discount cards | 106 | 2.8648648648648649  
3 | 2023-01-01T00:00:00.000Z | 1 | 1 | Moscow | with discount cards | 106 | 2.8648648648648649  
4 | 2023-01-01T00:00:00.000Z | 2 | 1 | Moscow | with discount cards | 106 | 2.8648648648648649  
5 | 2023-01-02T00:00:00.000Z | 3 | 1 | Moscow | with discount cards | 106 | 2.8648648648648649  
…​ |  |  |  |  |  |  |   
  
View on DB Fiddle

Агрегирующие функции вычисляют значения для окон, указанных в `OVER (PARTITION BY region)`. Эти данные позволяют нам провести анализ, например была ли сумма продажи выше или ниже среднего чека по региону.

## Выводы

  1. Оконные функции позволяют выполнять агрегатные вычисления не только по всей таблице, но и в пределах определенного окна, что делает их мощным инструментом для аналитики данных

  2. При использовании оконной функции версии функции каждая строка будет иметь доступ к количеству строк в заданном окне.

  3. Для использования оконных функций `SUM()`, `COUNT()`, `AVG()` в SQL необходимо указать `OVER()` с `PARTITION BY` для определения окна, в пределах которого будет выполняться вычисление функции.
