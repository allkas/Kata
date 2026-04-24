---
tags: [sql, database, hexlet]
source: "SQL — Оконные функции"
---

# FIRST_VALUE и LAST_VALUE

Видео может быть заблокировано из-за расширений браузера. В статье вы найдете решение этой проблемы.

  * Выводы



Оконные функции `FIRST_VALUE` и `LAST_VALUE` являются аналитическими функциями в SQL, которые позволяют получить первое и последнее значение внутри заданного окна (окна определяются с помощью оператора OVER). Эти функции часто используются для анализа данных внутри группировок или упорядоченных наборов данных.

Функция `FIRST_VALUE` возвращает первое значение внутри заданного окна, а функция `LAST_VALUE` \- последнее значение. Обе функции принимают два обязательных параметра: выражение (столбец или выражение) и ORDER BY (определяющий порядок строк внутри окна).

Пример использования `FIRST_VALUE` и `LAST_VALUE`:
    
    
    SELECT
        s.id,
        s.sale_date,
        s.price,
        s.quantity,
        sh.region,
        c.category,
        (s.quantity * s.price) AS sale_amount,
        FIRST_VALUE(s.price * s.quantity)
            OVER (PARTITION BY sh.region ORDER BY s.sale_date)
        AS frst_value,
        LAST_VALUE(s.price * s.quantity)
            OVER (PARTITION BY sh.region ORDER BY s.sale_date)
        AS lst_value
    FROM sales AS s
    LEFT JOIN customer AS c ON s.customer_id = c.customer_id
    LEFT JOIN shop AS sh ON s.shop_id = sh.shop_id
    ORDER BY s.id;

id | sale_date | price | quantity | region | category | sale_amount | frst_value | lst_value  
---|---|---|---|---|---|---|---|---  
1 | 2023-01-01T00:00:00.000Z | 4 | 1 | Moscow | with discount cards | 4 | 4 | 4  
2 | 2023-01-01T00:00:00.000Z | 2 | 2 | Moscow | with discount cards | 4 | 4 | 4  
3 | 2023-01-01T00:00:00.000Z | 1 | 1 | Moscow | with discount cards | 1 | 4 | 1  
4 | 2023-01-01T00:00:00.000Z | 2 | 1 | Moscow | with discount cards | 2 | 4 | 2  
5 | 2023-01-02T00:00:00.000Z | 3 | 1 | Moscow | with discount cards | 3 | 4 | 3  
…​ |  |  |  |  |  |  |  |   
  
View on DB Fiddle

Это позволяет нам сравнить сумму продажи с первой или последней продажей в регионе

## Выводы

  * Оконные функции `FIRST_VALUE` и `LAST_VALUE` используются в SQL для получения первого и последнего значения из определенного столбца внутри окна.

  * `FIRST_VALUE` возвращает первое значение в окне в соответствии с порядком сортировки, а `LAST_VALUE` возвращает последнее значение.

  * Обе функции могут быть использованы в комбинации с другими оконными функциями, такими как ROW_NUMBER или RANK, для более гибкого анализа данных.

  * `FIRST_VALUE` и `LAST_VALUE` могут быть полезны при работе с временными рядами, анализе трендов или при необходимости найти первое и последнее значение в группе данных.
