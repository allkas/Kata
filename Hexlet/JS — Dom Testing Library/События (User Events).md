---
tags: [javascript, testing, hexlet]
source: "JS — Dom Testing Library"
---

# События (User Events)

  * Использование
  * События
    * type
    * keyboard
    * clear
    * selectOptions



Ядро e2e-теста, это события, которые вызываются для последующей проверки работоспособности страницы. В простейших случаях для этого можно использовать стандартные события DOM, например клик по кнопке. 
    
    
    const button = screen.getByText("Start");
    button.click();
    

Как и в случае с поиском элементов, для событий в Testing Library сделана своя библиотека user-event. Связано это с тем, что действия выполняемые пользователям, в некоторых ситуациях, сложнее чем, просто вызов события на элементе.

Возьмем для примера набор текста в полях формы. Во время этого процесса вызывается множество событий разделенных во времени. В том числе потому, что человек, обычно, набирает текст постепенно. За это время вызывается череда событий, таких как `keydown`, `keypress`, `input`, `keyup`, причем для каждого символа индивидуально с определенной задержкой. Полный список улучшений:

  * Сложные взаимодействия "упакованы" в простые методы
  * Комплексные события гарантированно вызываются со всеми вложенными событиями в правильном порядке.
  * В библиотеку встроена поддержка специальных клавиш и модификаторов для имитации сложных взаимодействий



Самостоятельно имитировать подобное поведение довольно сложно, поэтому проще использовать готовые решения и Testing Library их предоставляет.

## Использование

Библиотека устроена таким образом, что она имитирует создание пользователя в виде объекта, от которого происходит вызов различных событий. Это довольно наглядно указывает на разницу между событиями самого DOM и пользовательскими событиями. 
    
    
    import "@hexlet/tic-tac-toe/public/style.css";
    import { test, expect } from "vitest";
    import { screen } from "@testing-library/dom";
    import userEvent from "@testing-library/user-event";
    
    // Импортируем игру
    import { TicTacToe } from "@hexlet/tic-tac-toe";
    
    test("main", async () => {
      // Объект для выполнения действий над элементами
      const user = userEvent.setup();
    
      // Заполняем document.body
      // Игра "разворачивает" себя в переданный элемент
      // Вызов метода start вешает обработчики
      const game = new TicTacToe(document.body);
      game.start();
    
      // Выбираем нужные элементы
      // Находим поля для ввода имен игроков
      const input1 = screen.getByLabelText("Player 1");
      const input2 = screen.getByLabelText("Player 2");
    
      // Выполняем необходимые действия
      // Вводим имена пользователей
      await user.type(input1, "user 1");
      await user.type(input2, "user 2");
    
      // Отправляем форму
      const submitButton = screen.getByText("Start Game");
      await user.click(submitButton);
    
      // Проверяем результат
      expect(document.body).toHaveTextContent("user 1, you are up!");
    });
    

Testing Library рекомендует вызывать `userEvent.setup()` до рендеринга. В примере выше рендеринг происходит на вызове `new TicTacToe(document.body)`. Даже если тестов будет несколько, совершенно нормально вызывать этот код в начале каждого теста.

Если тестов становится действительно много, то дублирования можно избежать написав `setup()` функцию таким образом: 
    
    
    function setup(jsx) {
      const user = userEvent.setup();
      const game = new TickTackToe(document.body);
      game.start();
    
      return { user, game };
    }
    
    test("render with a setup function", async () => {
      const { user, game } = setup();
      // ...
    });
    

Возможно у вас возник вопрос, а почему бы не сделать это один раз перед тестами, например в хуке `beforeAll()`. Проблема в том, что каждый тест меняет глобальное окружение `document`, поэтому устанавливать его нужно заново в каждом тесте. А использовать `beforeEach()` для сетапа не рекомендуется из-за сложностей при наличии вложенных тестов. Подробнее прочитать об этом можно в статье, в дополнительных материалах.

## События
    
    
    click(element: Element): Promise<void>
    

Все события асинхронны. Это значит что любой метод события в библиотеке _user-event_ возвращает Promise. А значит в тестах будет активно использоваться **async/await**. 
    
    
    await user.type(input1, "user 1");
    await user.click(submitButton);
    

Ниже мы разберем несколько событий из этой библиотеки. Остальные события доступны в официальной документации.

### type

Метод `type()` заполняет текстовое поле переданным значением полностью имитируя пользовательское поведение, которое включает в себя клик на поле для ввода. Поддерживает специальные клавиши, например Enter: 
    
    
    // Порождает клик на текстовом поле,
    // а затем `keydown`, `keypress`, `keyup` для Enter
    userEvent.type(input, "Hexlet{Enter}");
    

### keyboard

Если вам нужно просто симулировать нажатия клавиш на клавиатуре, то тогда используется метод `keybaord()`. В этом случае реальный эффект от его использования будет зависеть от того, где сейчас находится фокус в документе. 
    
    
    keyboard("hexlet"); // превращается в: h, e, x, l, e, t
    keyboard("{Shift>}A{/Shift}"); // превращается в: Shift(down), A, Shift(up)
    

### clear

Метод `clear()` используется для очистки редактируемого элемента. Внутри он раскладывается на фокусировку, выделение и удаление контента через браузерное меню. 
    
    
    await user.clear(screen.getByRole("textbox"));
    

### selectOptions

Метод `selectOptions()` позволяет выбрать одну или несколько опций из списка _Select_. 
    
    
    test("selectOptions", async () => {
      const user = userEvent.setup();
    
      render(
        <select multiple>
          <option value="hexlet">Hexlet</option>
          <option value="youtube">Youtube</option>
          <option value="habr">Habr</option>
        </select>
      );
    
      // В списке можно использовать как value так и label
      await user.selectOptions(screen.getByRole("listbox"), ["hexlet", "Habr"]);
    
      expect(screen.getByRole("option", { name: "Hexlet" }).selected).toBe(true);
      expect(screen.getByRole("option", { name: "Youtube" }).selected).toBe(false);
      expect(screen.getByRole("option", { name: "Habr" }).selected).toBe(true);
    });
    

* * *

#### Дополнительные материалы

  1. Официальная документация
  2. Avoid Nesting When Your Testing
