---
tags: [sql, database, hexlet]
source: "SQL — Оконные функции"
---

# MIN и MAX

Видео может быть заблокировано из-за расширений браузера. В статье вы найдете решение этой проблемы.

  * Выводы



В этом уроке мы изучим оконные версии функций `MIN()` и `MAX()`. Они выполняют ту же роль, что и в случае с агрегатными функциями.

Соответственно, здесь окно тоже параметризуется так же, как и в предыдущих наших случаях.

Функции `MIN()` и `MAX()` возвращают минимальное и максимальное значение в окне. Они используются для поиска **экстремумов** — то есть граничных значений исследуемых признаков.

Чтобы найти экстремумы, мы берем необходимое нам поле. К нему мы добавляем еще одно счетное поле, в котором используем ключевое слово `MIN()` или `MAX()`, а дальше — ставим окно в разрезе и по сортировке.

Представим, что нам нужно не просто посчитать максимальный чек за день, но и вывести его для каждого конкретного значения. То есть рядом с конкретным чеком на 10 рублей нужно положить максимальный чек за этот день — 50 рублей.

Это нужно, чтобы дальше нам было удобнее эти цифры друг с другом сравнивать, выполнять с ними арифметические действия, считать проценты и так далее. То есть для этих целей мы их просто поставим друг рядом с другом, а потом уже будем считать. Для этого используем ключевое слово `MAX()`.

Абсолютно таким же образом мы можем посчитать минимальный чек за день и поставить его рядом с каждым конкретным чеком. Разница только в ключевом слове — здесь мы используем `MIN()`.

Предположим, нам бы хотелось посчитать не просто максимум и минимум продаж по регионам, а что-то интереснее
    
    
    SELECT
        sh.region,
        c.category,
        min(s.price * s.quantity) AS min_amount,
        max(s.price * s.quantity) AS max_amount
    FROM
        sales AS s
    LEFT JOIN customer AS c
        ON
            s.customer_id = c.customer_id
    LEFT JOIN shop AS sh
        ON
            s.shop_id = sh.shop_id
    GROUP BY sh.region, c.category;

region | category | min_amount | max_amount  
---|---|---|---  
Moscow | with discount cards | 1 | 9  
Kaliningrad | with discount cards | 1 | 6  
Tver | with discount cards | 2 | 9  
Novosibirsk | with discount cards | 1 | 6  
Vladivostok | without discount card | 1 | 6  
Saint-Petersburg | without discount card | 1 | 8  
  
View on DB Fiddle
    
    
    SELECT
        s.id,
        s.sale_date,
        s.price,
        s.quantity,
        sh.region,
        c.category,
        (price * quantity) AS amount,
        min(s.price * s.quantity) OVER (PARTITION BY sh.region, c.category) AS min_amount,
        max(s.price * s.quantity) OVER (PARTITION BY sh.region, c.category) AS max_amount
    FROM
        sales AS s
    LEFT JOIN customer AS c
        ON
            s.customer_id = c.customer_id
    LEFT JOIN shop AS sh
        ON
            s.shop_id = sh.shop_id
    ORDER BY id;

id | sale_date | price | quantity | region | category | amount | min_amount | max_amount  
---|---|---|---|---|---|---|---|---  
1 | 2023-01-01T00:00:00.000Z | 4 | 1 | Moscow | with discount cards | 4 | 1 | 9  
2 | 2023-01-01T00:00:00.000Z | 2 | 2 | Moscow | with discount cards | 4 | 1 | 9  
3 | 2023-01-01T00:00:00.000Z | 1 | 1 | Moscow | with discount cards | 1 | 1 | 9  
4 | 2023-01-01T00:00:00.000Z | 2 | 1 | Moscow | with discount cards | 2 | 1 | 9  
5 | 2023-01-02T00:00:00.000Z | 3 | 1 | Moscow | with discount cards | 3 | 1 | 9  
…​ |  |  |  |  |  |  |  |   
  
View on DB Fiddle

Можем видеть, что минимальные и максимальные значения для регионов повторяются для простых версий функций `MIN()` и `MAX()`.

В следующий запрос добавили сортировку по `sale_date` и значения _min_ и _max_ изменились - теперь группировка идет и по дате.
    
    
    SELECT
        s.id,
        s.sale_date,
        s.price,
        s.quantity,
        sh.region,
        c.category,
        (price * quantity) AS amount,
        min(s.price * s.quantity) OVER (PARTITION BY sh.region, c.category ORDER BY s.sale_date) AS min_amount,
        max(s.price * s.quantity) OVER (PARTITION BY sh.region, c.category ORDER BY s.sale_date) AS max_amount
    FROM
        sales AS s
    LEFT JOIN customer AS c
        ON
            s.customer_id = c.customer_id
    LEFT JOIN shop AS sh
        ON
            s.shop_id = sh.shop_id
    ORDER BY id;

id | sale_date | price | quantity | region | category | amount | min_amount | max_amount  
---|---|---|---|---|---|---|---|---  
1 | 2023-01-01T00:00:00.000Z | 4 | 1 | Moscow | with discount cards | 4 | 1 | 4  
2 | 2023-01-01T00:00:00.000Z | 2 | 2 | Moscow | with discount cards | 4 | 1 | 4  
3 | 2023-01-01T00:00:00.000Z | 1 | 1 | Moscow | with discount cards | 1 | 1 | 4  
4 | 2023-01-01T00:00:00.000Z | 2 | 1 | Moscow | with discount cards | 2 | 1 | 4  
5 | 2023-01-02T00:00:00.000Z | 3 | 1 | Moscow | with discount cards | 3 | 1 | 4  
…​ |  |  |  |  |  |  |  |   
  
View on DB Fiddle

## Выводы

  * Оконные версии функций `MIN()` и `MAX`() в SQL позволяют находить минимальное и максимальное значение в столбце или группе значений. В комбинации с оконными функциями, они могут использоваться для выполнения различных аналитических задач.

  * При использовании оконных функций `MIN()` и `MAX`() не требуется группировка данных, что позволяет выполнять аналитические операции без изменения структуры запроса.

  * Оконные функции `MIN()` и `MAX`() могут быть полезны при определении ранжирования данных, вычислении разницы между текущим значением и минимальным/максимальным в окне, а также при поиске экстремальных значений внутри группы данных.

  * При использовании оконных функций `MIN()` и `MAX`() необходимо учитывать порядок сортировки данных в окне, так как это влияет на результаты операций `MIN()` и `MAX`().
