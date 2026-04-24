---
tags: [javascript, testing, hexlet]
source: "JS — Dom Testing Library"
---

# Запросы (Queries)

  * getByLabelText
  * getByRole
  * getAllBy
  * queryBy && queryAllBy
  * Дополнительные методы поиска
    * Расширенное сопоставление текста
  * testid
  * Алгоритм выбора поискового метода



При взаимодействии с документом, в тесте, нам понадобится постоянно выбирать элементы для выполнения над ними действий или проверок. Это можно сделать в тестах стандартными браузерными средствами через `querySelector()`: 
    
    
    test("should show login form", () => {
      document.body.innerHTML = '<p class="someclass">Hexlet</p>';
    
      const input = document.querySelector(".someclass");
    });
    

Но у такого способа есть ряд серьезных недостатков:

  1. Если ничего не вернется, то Testing Library никак не сможет помочь в отладке. Мы просто получим ошибку попытки работы с `null`, в дальнейшем коде. 
         
         const element = document.querySelector(".no_exists");
         element.value; // Ошибка если element null
         

  2. Если мы выбираем элемент, который появляется асинхронно, после какого-то предыдущего действия, например отправки формы, то его может не оказаться в DOM, так как прошло слишком мало времени. Придется самостоятельно организовывать режим ожидания изменений в DOM. 
         
         // Отправляем форму
         // После этого ожидаем появление элемента
         // Но он может не успеть появиться
         const element = document.querySelector(".no_exists");
         

  3. Такой способ поиска приводит к сильной завязке на внутреннюю структуру документа, к которым относятся классы. Это порождает хрупкие тесты. 
         
         // Класс обычно связан с представлением, его могут поменять
         // и все продолжит работать
         const element = document.querySelector(".no_exists");
         




По этим причинам, Testing Library предоставляет большой набор собственных методов. Эти методы работают с видимой частью документа, а сами запросы базируются не на классах или идентификаторах, а на названиях, ролях элементов и в крайнем случае на специальном атрибуте `data-testid`.

## getByLabelText

В тесте игры _крестики-нолики_ проверяется первый экран, а для этого нужно выбрать поля для ввода. В Testing Library эту задачу можно выполнить с помощью метода `getByLabelText()` объекта `screen`, который, внутри себя, обращается к `document`. Этот метод, исходя из названия, ищет элемент формы, связанный с лейблом, содержащим переданный текст. 
    
    
    test("main", async () => {
      const game = new TicTacToe(document.body);
      game.start();
    
      // <label for="player1">Player 1</label>
      // <input type="text" placeholder="enter name" name="player1" id="player1" class="input-field" />
      const input1 = screen.getByLabelText("Player 1");
      // <label for="player2">Player 1</label>
      // <input type="text" placeholder="enter name" name="player2" id="player1" class="input-field" />
      const input2 = screen.getByLabelText("Player 2");
    
      // Остальная часть теста
    });
    

В отличие от `querySelector()`, если ничего не будет найдено, метод `getByLabelText()` выбросит исключение, а в терминале отобразиться текущий HTML. Хотя скорее всего, его будет слишком много и для отладки понадобится _vitest-preview_. 
    
    
    # Пример с ошибкой: screen.getByLabelText("Player 3");
     FAIL  __tests__/main.spec.ts > check game
    TestingLibraryElementError: Unable to find a label with the text of: Player 3
    
    Ignored nodes: comments, script, style
    <body>
      <div>
    
    
        <h1
          class="header"
        >
          Tic Tac Toe
        </h1>
    # Тут еще много вывода
    

## getByRole

Другой способ выполнить эту же задачу состоит в использовании метода `getByRole()`. Сначала посмотрим на пример, а потом разберем как он работает. 
    
    
    const input1 = screen.getByRole("textbox", { name: /Player 1/i });
    const input2 = screen.getByRole("textbox", { name: /Player 2/i });
    

Метод `getByRole()` ищет элементы на базе их роли в соответствии с ARIA, частью системы доступности, которая описывает роли и атрибуты элементов интерфейса.

Это наиболее универсальный способ поиска элементов, с которыми можно взаимодействовать. К его преимуществам можно отнести вывод в случае ошибок. Testing Library показывает какие роли вообще есть в документе: 
    
    
    TestingLibraryElementError: Unable to find an accessible element with the role "textbox" and name `/Player 1/i`
    
    Here are the accessible roles:
    
      heading:
    
      Name "Tic Tac Toe":
      <h1
        class="header"
      />
    
      --------------------------------------------------textbox:
    
      Name "":
      <input
        class="input-field"
        name="player1"
        placeholder="enter name"
        type="text"
      />
    
      Name "":
      <input
        class="input-field"
        name="player2"
        placeholder="enter name"
        type="text"
      />
    
      --------------------------------------------------
      button:
    
      Name "Start Game":
      <input
        class="submit-btn"
        type="submit"
        value="Start Game"
      />
    
      --------------------------------------------------button:
    
      Name "Clear Board":
      <button
        class="replay-btn"
        value="replay"
      />
    

## getAllBy

У каждого метода `getBy` есть альтернативный вариант `getAllBy`. Как следует из названия, эти методы возвращают коллекции, если мы ищем больше одного элемента. 
    
    
    const inputs = screen.getByRole("textbox");
    screen.debug(inputs);
    

Выведет в терминал: 
    
    
    TestingLibraryElementError: Found multiple elements with the role "textbox"
    
    Here are the matching elements:
    
    Ignored nodes: comments, script, style
    <input
      class="input-field"
      id="player1"
      name="player1"
      placeholder="enter name"
      type="text"
    />
    
    Ignored nodes: comments, script, style
    <input
      class="input-field"
      id="player2"
      name="player2"
      placeholder="enter name"
      type="text"
    />
    

Если не было найдено ни одного элемента, то будет выброшено исключение

## queryBy && queryAllBy

В некоторых ситуациях бывает нужно продолжить работу, даже если не было найдено ни одного элемента, например при проверке, что элемент в DOM дереве не найден или пропал из него после определенных действий. В таком случае вместо методов `getBy` и `getByAll` используются методы `queryBy` и `queryAllBy`. Это единственное их отличие. 
    
    
    const submitButton = screen.queryByText('submit')
    expect(submitButton).toBeNull() // не найден
    
    const submitButtons = screen.queryAllByText('submit')
    expect(submitButtons).toHaveLength(0)
    

Чтобы не запутаться, посмотрите на эту табличку:

Метод | Без совпадений | 1 совпадение | > 1 совпадения  
---|---|---|---  
getBy | throw | return | throw  
queryBy | null | return | throw  
getAllBy | throw | array | array  
queryAllBy | [] | array | array  
  
## Дополнительные методы поиска

Но это еще не все, помимо методов перечисленных выше, Testing Library предоставляет пачку других:

  * `getByPlaceholderText()` \- поиск по плейсхолдеру
  * `getByText()` \- поиск по текстовому содержимому элемента
  * `getByDisplayValue()` \- поиск по текущему значению в элементе, например, тексту в форме
  * `getByAltText()` \- поиск по тексту в атрибуте `alt` у картинок
  * `getByTitle()` \- поиск по тексту в атрибуте `title`



### Расширенное сопоставление текста

Большая часть этих методов умеет работать не только со строками. Например, в эти методы можно передавать регулярные выражения: 
    
    
    screen.getByText(/World/) // поиск подстроки
    screen.getByText(/world/i) // поиск подстроки игнорируя регистр
    screen.getByText(/Hello W?oRlD/i) // поиск по паттерну
    

Еще один вариант, это кастомная проверка через передачу функции: 
    
    
    screen.getByText((content, element) => content.startsWith('Hello'))
    

## testid

Особняком стоит метод `getByTestId()`. Он используется в том случае, когда до элемента нельзя или неудобно добираться любым другим способом. Для его работы нужно добавить атрибут `data-testid` в тот элемент, который мы ищем. 
    
    
    <div data-testid="custom-element" />
    

После этого заработает поиск: 
    
    
    const element = screen.getByTestId("custom-element");
    

В отличие от классов и других элементов связанных с HTML, _testid_ используется только для тестов, поэтому хрупкость подобных тестов ниже. Несмотря на это, использовать _testid_ стоит только в крайних случаях, потому что он удаляет нас от работы со страницей в режиме пользователя.

Подход с _testid_ пригодится для тестирования игры крестики-нолики. Когда мы доходим до поля с игрой, то каждая клетка это просто ячейка в табличке (визуально). У этих ячеек нет специального значения и к ним просто так не обратиться. Поэтому в этом случае логично добавить _testid_ : 
    
    
    <div class="board__container">
      <div class="board__cell">
        <div class="letter" data-testid="cell-1"></div>
      </div>
      <div class="board__cell">
        <div class="letter" data-testid="cell-2"></div>
      </div>
      <div class="board__cell">
        <div class="letter" data-testid="cell-3"></div>
      </div>
    
      <div class="board__cell">
        <div class="letter" data-testid="cell-4"></div>
      </div>
      <div class="board__cell">
        <div class="letter" data-testid="cell-5"></div>
      </div>
      <div class="board__cell">
        <div class="letter" data-testid="cell-6"></div>
      </div>
    
      <div class="board__cell">
        <div class="letter" data-testid="cell-7"></div>
      </div>
      <div class="board__cell">
        <div class="letter" data-testid="cell-8"></div>
      </div>
      <div class="board__cell">
        <div class="letter" data-testid="cell-9"></div>
      </div>
    </div>
    

А сам тест игры будет выглядеть так: 
    
    
    // Заполнили форму и нажали "начать игру"
    
    await user.click(screen.getByTestId('cell-6'))
    expect(document.body).toHaveTextContent('user 2, you are up!')
    
    await user.click(screen.getByTestId('cell-5'))
    expect(document.body).toHaveTextContent('user 1, you are up!')
    
    await user.click(screen.getByTestId('cell-3'))
    await user.click(screen.getByTestId('cell-2'))
    await user.click(screen.getByTestId('cell-9'))
    
    expect(document.body).toHaveTextContent('Congratulations user 1')
    expect(document.body).toHaveTextContent('You are our winner!')
    

## Алгоритм выбора поискового метода

При выборе методов запросов в Testing Library, имеет смысл придерживаться рекомендацией создателей библиотеки, чтобы обеспечить надежные и легко поддерживаемые тесты. Ниже приведен алгоритм для выбора методов запросов:

  1. Используйте методы с приоритетом доступности (**ByRole** , **ByLabelText** , **ByPlaceholderText** , **ByText**).

     * Эти методы имитируют то, как пользователи взаимодействуют с приложением.
     * **ByRole** : Используйте, когда элемент имеет определенную роль (например, кнопка, заголовок). `javascript const button = screen.getByRole("button", { name: /submit/i }); `
     * **ByLabelText** : Используйте для элементов формы, связанных с метками. `javascript const input = screen.getByLabelText(/username/i); `
     * **ByPlaceholderText** : Используйте для элементов формы с атрибутом placeholder. `javascript const input = screen.getByPlaceholderText(/enter your name/i); `
     * **ByText** : Используйте для элементов, которые содержат текст. `javascript const link = screen.getByText(/learn more/i); `
  2. Используйте методы с пониженным приоритетом (**ByDisplayValue** , **ByAltText** , **ByTitle**)

     * Эти методы также имитируют пользовательское взаимодействие, но менее предпочтительны, чем предыдущие.
     * **ByDisplayValue** : Используйте для элементов формы, отображающих определенное значение. `javascript const input = screen.getByDisplayValue(/john doe/i); `
     * **ByAltText** : Используйте для изображений с атрибутом `alt`. `javascript const image = screen.getByAltText(/profile picture/i); `
     * **ByTitle** : Используйте для элементов с атрибутом `title`. `javascript const tooltip = screen.getByTitle(/tooltip text/i); `
  3. Используйте методы с еще более низким приоритетом (ByTestId)

     * Эти методы менее предпочтительны, так как они не имитируют взаимодействие пользователя и могут затруднять поддержку тестов.
     * **ByTestId** : Используйте только в крайнем случае, если нет других вариантов. `javascript const customElement = screen.getByTestId("custom-element"); `



Следуя этому алгоритму, ваши тесты будут надежными, поддерживаемыми и ориентированными на пользовательское взаимодействие.

* * *

#### Дополнительные материалы

  1. Официальная документация
