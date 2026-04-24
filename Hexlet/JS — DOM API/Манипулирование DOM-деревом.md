---
tags: [javascript, dom, browser, hexlet]
source: "JS — DOM API"
---

# Манипулирование DOM-деревом

  * innerHTML
  * Создание узлов
  * Вставка
  * Старый API
  * Клонирование



DOM-дерево может изменяться, когда браузер уже выполнил его рендеринг. Именно этот факт позволяет создавать интерактивные приложения.

В этом уроке мы обсудим, как манипулировать DOM-деревьями и какие преимущества мы можем при этом получить.

## innerHTML

Самый простой способ обновить часть DOM — это свойство `innerHTML`: 
    
    
    <ul>
      <li>item 1</li>
      <li>item 2</li>
    </ul>
    
    
    
    const body = document.body;
    console.log(body);
    // <ul><li>item 1</li><li>item 2</li></ul>
    
    body.innerHTML = '<b>make</b> love';
    console.log(body.innerHTML);
    // <b>make</b> love
    
    console.log(body.childNodes);
    // [b, text]
    

Значение этого свойства полностью заменяет потомков элемента, на котором мы его вызвали. Весь HTML, находящийся внутри, анализируется и становится частью дерева.

Представьте, что мы пытаемся вставить обычный текст, в котором потенциально содержится HTML. Это повышает вероятность XSS-атак, поэтому мы должны использовать другое свойство - `textContent`.

Свойство `textContent` работает практически идентично, оно также заменяет всех потомков. Основное различие между этими свойствами заключается в том, что `textContent` рассматривает содержимое как обычный текст в любом случае, даже если там есть HTML: 
    
    
    document.body.textContent = '<b>make</b> love';
    console.log(document.body.innerHTML);
    // Все специальные символы оказываются замененными
    // "&lt;b&gt;make&lt;/b&gt; love"
    

Свойство `innerHTML` работает со строками. Это удобно, только если мы работаем со статическим представлением DOM. Для динамического формирования хорошо подходят специальные функции.

## Создание узлов
    
    
    // Создаем текстовый узел
    const textNode = document.createTextNode('life is life');
    
    // Создаем элемент p
    const pEl = document.createElement('p');
    
    // Добавляем textNode в конец списка childNodes элемента pEl
    pEl.append(textNode);
    // pEl.textContent = 'life is life';
    
    const el = document.createElement('div');
    el.append(pEl);
    
    console.log(el);
    // <div><p>life is life</p></div>
    

Код, создающий DOM динамически, похож на матрешку. После создания одни элементы все время вкладываются в другие. Так выглядит код, который конструирует деревья в любом языке.

## Вставка

ParentNode.prepend() добавляет переданный узел первым потомком в `ParentNode`: 
    
    
    const div = document.createElement('div');
    div.innerHTML = '<span>Hexlet</span>';
    
    const el = document.createElement('p');
    el.textContent = 'prepend';
    div.prepend(el);
    // <div>
    //   <p>prepend</p>
    //   <span>Hexlet</span>
    // </div>
    

ParentNode.append() добавляет переданный узел последним потомком в `ParentNode`: 
    
    
    const div = document.createElement('div');
    div.innerHTML = '<span>Hexlet</span>';
    
    const el = document.createElement('p');
    el.textContent = 'append';
    div.append(el);
    // <div>
    //   <span>Hexlet</span>
    //   <p>append</p>
    // </div>
    

childNode.before(...nodes) – вставляет `nodes` в список потомков родительского узла `childNode` прямо перед `childNode`: 
    
    
    const div = document.createElement('div');
    div.innerHTML = '<span>Hexlet</span>';
    // Должен быть вставлен в DOM-дерево
    document.body.append(div);
    
    const el = document.createElement('p');
    el.textContent = 'content';
    div.before(el);
    // <p>content</p>
    // <div>
    //   <span>Hexlet</span>
    // </div>
    

childNode.after(...nodes) – вставляет `nodes` в список потомков родительского узла `childNode` сразу после `childNode`: 
    
    
    const div = document.createElement('div');
    div.innerHTML = '<span>Hexlet</span>';
    // Должен быть вставлен в DOM-дерево
    document.body.append(div);
    
    const el = document.createElement('p');
    el.textContent = 'content';
    div.after(el);
    // <div>
    //   <span>Hexlet</span>
    // </div>
    // <p>content</p>
    

node.replaceWith(...nodes) – вставляет `nodes` вместо `node`. Сама `node` пропадает из DOM-дерева, но остается доступной в коде: 
    
    
    const div = document.createElement('div');
    div.innerHTML = '<span>Hexlet</span>';
    // Должен быть вставлен в DOM-дерево
    document.body.append(div);
    
    const el = document.createElement('p');
    el.textContent = 'content';
    div.replaceWith(el);
    // В DOM-дереве вместо div остался p
    // <p>content</p>
    

Element.remove() удаляет текущий узел.

Создание элемента не добавляет сразу этот элемент на страницу. Например, `document.createElement('div')` просто создаст объект элемента `div`. При этом этот объект не будет частью DOM-дерева. Поэтому нужно вставить этот объект в дерево, если нужно добавить его на страницу.

## Старый API

Описанные выше функции появились не так давно. Большая часть кода написана с использованием других функций, список которых ниже:

  * `parent.appendChild(el)` – добавляет `el` в конец списка потомков
  * `parent.insertBefore(el, nextElSibling)` – добавляет `el` в список потомков `parent` перед `nextElSibling`
  * `parent.removeChild(el)` – удаляет `el` из потомков `parent`
  * `parent.replaceChild(newEl, el)` – заменяет `el` на `newEl`



## Клонирование

Иногда нам нужно создать элемент, похожий на существующий. Конечно, это можно сделать вручную, скопировав свойства одного элемента в свойства другого. Но есть и более простой способ: 
    
    
    const newEl = el.cloneNode(true);
    

Значение `true` показывает, что мы создаем **глубокую копию** — то есть копию данного элемента со всеми его потомками.
