---
tags: [javascript, react, frontend, hexlet]
source: "JS — React"
---

# Children_html

UI-элементы имеют иерархическую структуру. Например, компонент _card_ в Bootstrap: 
    
    
    <div class="card">
      <img class="card-img-top" src="..." alt="Card image cap">
      <div class="card-body">
        <h4 class="card-title">Card title</h4>
        <p class="card-text">
          Some quick example text to build on the card title and make up the bulk of the card's content.
        </p>
        <a href="#" class="btn btn-primary">Go somewhere</a>
      </div>
    </div>
    

Блок карточки может содержать внутри себя картинку и тело. Тело, в свою очередь, может состоять из заголовка и текста, а текст может быть чем угодно. То же самое применимо как к самым простым элементам самого HTML, например, тегу `<div>`, так и к остальным компонентам Bootstrap, таким как модальные окна и навигация.

HTML соответствует природе UI и естественным образом позволяет создавать композиции элементов за счёт вкладывания тегов друг в друга. Точно так же работает и JSX. Пока эта возможность использовалась в курсе только для встроенных компонентов. Теперь пора научиться повторять подобное поведение в самописных компонентах. В качестве примера взят компонент `<Alert />` из Bootstrap.

В примере выше обязательной частью является только основной _div_. Содержимое зависит от конкретной ситуации. Подставляется оно с помощью свойства _children_.

Обратите внимание на то, что компонент стал использоваться как парный тег в JSX: 
    
    
    const vdom = (
      <Alert>
        <p>Whenever you need to, be sure to use margin utilities to keep things nice and tidy.</p>
      </Alert>
    );
    

Все, что находится между открывающим и закрывающим тегом, попадает внутрь пропса _children_.

Но будьте бдительны: тип данных свойства _children_ зависит от содержимого. В простейшем случае, когда тег используется как одиночный `<div />`, это свойство будет равно `undefined`: 
    
    
    class App extends React.Component {
      render() {
        const { children } = this.props;
        return (
          <div>
            {children}
          </div>
        );
      }
    }
    
    const vdom = <App />; // В children попадет undefined
    

Если этим содержимым является строка, то именно она окажется внутри _children_. Правда, после некоторой обработки. JSX удаляет пробельные символы с начала и конца строки, включая пустые строки. Следующие примеры будут отображены одинаково: 
    
    
    <div>Hello World</div>
    
    <div>
      Hello World
    </div>
    
    <div>
      Hello
      World
    </div>
    
    <div>
    
      Hello World
    </div>
    

Любой одиночный дочерний компонент также будет представлен сам собой в _children_ : 
    
    
    class App extends React.Component {
      render() {
        const { children } = this.props;
        return (
          <div>
            {children}
          </div>
        );
      }
    }
    
    const vdom = <App>some text</App>; // в children попадет одиночный текстовый элемент "some text"
    

Во всех остальных случаях `children` будет содержать массив: 
    
    
    class App extends React.Component {
      render() {
        const { children } = this.props;
        return (
          <div>
            {children}
          </div>
        );
      }
    }
    
    const vdom = <App>
      <div>one</div>
      <div>two</div>
    </App>; // в children попадет массив элементов <div>one</div> и <div>two</div>
    

Если внимательно посмотреть на документацию React, то можно увидеть следующее определение _children_ : "children are an opaque data structure" (свойство `children` — непрозрачная структура данных). Другими словами, нельзя однозначно полагаться на тип этого пропса, так как снаружи можно передать всё что угодно.

Подобное поведение может приводить к трудно находимым ошибкам. Например, проверка `this.props.children.length` — это не всегда количество детей. Если `children` это одиночный элемент, например строка, то свойство `length` вернет длину этой строки. 
    
    
    class MyComponent extends React.Component {
      render() {
        const { children } = this.props
        return <p>Count: {children.length}</p>
      }
    }
    
    // <p>Count: 4</p>
    <MyComponent>Text</MyComponent>
    

Именно поэтому React предоставляет набор функций, предназначенных для манипулирования пропсом `children`. Все они доступны в `React.Children`. Эти функции знают про особенности работы `children`, сами проверяют тип и делают нужные проверки в зависимости от типа данных.

**React.Children.map()**

Из урока про обработку коллекций вы можете вспомнить, что при работе со списком каждому элементу нужно установить проп `key`. Если этого не сделать в случае с `React.Children.map`, React не выбросит предупреждение. Так сделано намеренно, поскольку у потомков обычно нет уникальных идентификаторов.

**React.Children.count()**

Чтобы получить количество детей, нужно использовать метод `React.Children.count()`. В него передается `children`. Узлы, которые не являются DOM-элементами, будут проигнорированы: 
    
    
    class ChildrenCounter extends React.Component {
      render() {
        const { children } = this.props
        return <p>Count: {React.Children.count(children)}</p>
      }
    }
    
    // Count: 1
    <ChildrenCounter>
      Second!
    </ChildrenCounter>
    
    // Count: 2
    <ChildrenCounter>
      <p>First</p>
      <ChildComponent />
    </ChildrenCounter>
    
    // Count: 2
    <ChildrenCounter>
      {() => <h1>First!</h1>} // будет пропущено, поскольку не является dom-элементом
      Second!
      <p>Third!</p>
    </ChildrenCounter>
    

Кроме перечисленного выше, бывает необходимо обработать дочерние элементы перед выводом, изменив часть в пропсе. Конечно же, напрямую этого сделать нельзя, ведь пропсы неизменяемы. Такого поведения можно добиться, клонируя элементы функцией `React.cloneElement()`. 
    
    
    const ChildComponent = props => {
      return <div style={props.style}>{props.children}</div>;
    };
    
    class ParentComponent extends React.Component {
      render() {
        const enhancedChildren = React.Children.map(this.props.children, child => {
          // Клонируем каждый дочерний элемент, добавляя или изменяя его пропсы
          return React.cloneElement(child, {style: {...child.props.style, color: "red"}});
        });
    
        return (
          <div>
            {enhancedChildren}
          </div>
        );
      }
    }
    
    // Использование ParentComponent где-то в приложении:
    // <ParentComponent>
    //   <ChildComponent style={{fontSize: '14px'}}>Текст 1</ChildComponent>
    //   <ChildComponent style={{fontSize: '16px'}}>Текст 2</ChildComponent>
    // </ParentComponent>
    

## Композиция компонентов

Иерархия компонентов во многом закладывает структуру приложения. То, как вы распределите приложение на компоненты, определит кодовую базу вашего проекта.

Есть несколько советов как разбивать приложение на компоненты:

  * выделите части интерфейса в приложении, которые имеют осмысленный функционал. Например: навигационная панель, боковое меню, окно чата и т.д. Каждую такую часть приложения можно выделить в отдельный компонент. Такое разбиение интерфейса на составляющие части заложит основу компонентной базы
  * если какие-то элементы повторяются, то их тоже лучше выделить в отдельный компонент для переиспользования. Например, это могут быть Button и InputField
  * рассматривайте компоненты как чистые функции. Пропсы, как и параметры в чистых функциях, не изменяются в компонентах, в React это важное правило
