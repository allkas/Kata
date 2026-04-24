---
tags: [algorithms, trees, hexlet]
source: "Алгоритмы на деревьях"
---

# AST-деревья

  * Что такое AST-деревья
  * Какие операции можно проводить над AST-деревом
  * Выводы



У каждого языка программирования есть свой набор ключевых слов, с помощью которых мы определяем выражения, задаем инструкции и преобразуем входные данные в выходные.

При этом у всех современных языков программирования есть одно сходство — они разрабатываются с упором на **человекочитаемость**. Другими словами, код на таких языках должен быть понятен в первую очередь человеку, а не машине.

Современные языки с упором на человекочитаемость называются **языками высокого уровня**. Они пришли на смену языкам низкого уровня, в которых программисты подстраивали код под поведение исполнителя — того или иного процессора. Задачу усложнял еще и тот факт, что процессоры сильно отличались с точки зрения поддерживаемых команд и других важных аспектов.

Переход на языки высокого уровня развивает отрасль высоких технологий:

  * Языки высокого уровня проще изучать, поэтому снизился порог входа в отрасль для новичков

  * Появилась возможность запускать программы на разных процессорах без изменений в исходном коде, поэтому на разработку стало уходить меньше времени

  * Код стал понятнее, поэтому стало проще работать совместно — читать чужой код и набираться опыта, присоединяться к новым проектам, поддерживать и исправлять чужие программы




С другой стороны, у высокоуровневых языков есть один основной недостаток — компьютеры не умеют работать с ними напрямую. До сих пор процессоры понимают только тот набор команд, для которого его спроектировали инженеры. Программа на языке высокого уровня не запустится, если мы не переведем ее код на язык низкого уровня. Только в этом случае процессор поймет, какой набор команд нужно выполнить. За этот перевод отвечают два процесса — **компиляция** и **интерпретация**.

Разобрать код на высокоуровневом языке и превратить его в список низкоуровневых команд позволяют **AST-деревья** — структур данных, о которых мы поговорим в этом уроке.

## Что такое AST-деревья

**AST** (_Abstract Syntax Tree_) — это абстрактное синтаксическое дерево, которое работает как один из промежуточных слоев при преобразовании языков высокого уровня. AST-дерево устроено так:

  * В качестве промежуточных узлов выступают инструкции, функции, методы или операторы

  * В листовых узлах содержатся константы, переменные и имена методов, то есть входные аргументы для соответствующих промежуточных узлов




AST-дерево не учитывает синтаксические особенности языка, вроде фигурных скобок или правил оформления лямбда-выражений. Это отличает их от другой похожей структуры — деревьев разбора.

Таким образом, AST-дерево занимает промежуточную позицию между деревом разбора и внутренним представлением программы внутри конкретных компиляторов или интерпретаторов. Для примера рассмотрим небольшую программу, которая занимается перемещением блока по экрану:
    
    
    // <div id="moveMe"></div> - наш искомый блок, который будем двигать по экрану
    const moveDiv = () => {
        const div = document.getElementById("moveMe");
        if (div != null){
            div.style.position = "absolute";
            div.style.top = window.height / 2 + "px";
            div.style.left = Math.pow(2,3) + "px";
        }
        else{
            alert("Блок не найден");
        }
    }

Теперь попробуем преобразовать функцию из примера выше в дерево:

  * В узле хранится информация о выполняемом операторе языка и список дочерних узлов

  * В листовых узлах лежит сопоставление с конечными операндами выполняемого оператора

  * Дерево ориентировано по порядку выполнения операций, поэтому вершиной дерева будет самая последняя операция по порядку вызова




Соответственно, функция из нашего примера принимает такой вид:

Можно сделать вывод, что AST — это не бинарное дерево. Оно может содержать в себе узлы нескольких подвидов, чем напоминает DOM-деревья.

## Какие операции можно проводить над AST-деревом

Ранее в курсе мы описывали деревья с точки зрения структуры узла и реализации основных операций над ним — построения, поиска, вставки и удаления. Но в этом уроке мы пойдем другим путем.

Дело в том, что с AST-деревьями операции поиска, добавления и удаления возможны в теории, на практике не имеют смысла. AST-дерево может измениться только по одной причине — появилось что-то новое в исходном коде программы. Такое изменение требует не вносить правки в старое дерево, а перестраивать его заново.

Поэтому в изучении AST-деревьев мы ограничимся только определением структуры и реализацией самого построения. Структура нашего узла принимает следующий вид:
    
    
    const instructionType = { ARGUMENT: 'argument', UNARY: 'unary', MULTIPLE: 'multiple' };
    
    class ASTree {
        constructor() {
            this.instructionType = null;
            this.operator = null;
            this.children = null;
            this.value = null;
        }
    }

Python
    
    
    instruction_type = {'ARGUMENT': 'argument', 'UNARY': 'unary', 'MULTIPLE': 'multiple'}
    
    class ASTree:
        def __init__(self):
            self.instructionType = None
            self.operator = None
            self.children = None
            self.value = None

PHP
    
    
    <?php
    class ASTree
    {
        public $instructionType;
        public $operator;
        public $children;
        public $value;
    
        const ARGUMENT = 'argument';
        const UNARY = 'unary';
        const MULTIPLE = 'multiple';
    
        public function __construct()
        {
            $this->instructionType = null;
            $this->operator = null;
            $this->children = null;
            $this->value = null;
        }
    }

Java
    
    
    class ASTree {
        private enum InstructionType { ARGUMENT, UNARY, MULTIPLE }
    
        private InstructionType instructionType;
        private String operator;
        private ASTree[] children;
        private Object value;
    
        public ASTree() {
            this.instructionType = null;
            this.operator = null;
            this.children = null;
            this.value = null;
        }
    }

Чтобы определить тип хранимых в узле данных, опишем перечисление `instructionType`. Оно будет описывать инструкций языка программирования в нескольких возможных вариантах. Воспользуемся этим перечислением, чтобы заполнить дерево. Нам понадобятся следующие варианты:

  * Унарный оператор `UNARY` с одним аргументом — например, `a++`. В таком случае поле `children` содержит один элемент типа `ASTree`

  * Оператор `MULTIPLE`, принимающий несколько аргументов — например, `a == b`. В таком случае поле `children` содержит массив элементов типа `ASTree`

  * Аргумент метода `ARGUMENT`, который является определенной переменной или константой. В таком случае поле `children` не имеет значения, а в поле `value` должно храниться значение переменной или константы




Теперь опишем метод построения такого дерева:
    
    
    class ASTree {
        // ...
    
        _innerBuildAST(instruction, operator, args, value = null) {
            if (args === null && value === null) {
                throw new Error('У узла должно быть значение или дочерние узлы');
            }
            if ((args === null && instruction !== 'ARGUMENT') || (value === null && instruction === 'ARGUMENT')) {
                throw new Error('У узла указан некорректный тип');
            }
    
            this.operator = operator;
            this.instructionType = instruction;
            if (this.instructionType !== 'ARGUMENT') {
                this.value = null;
                if (this.instructionType === 'UNARY') {
                    this.children = ASTree.buildAST(args);
                }
                if (this.instructionType === 'MULTIPLE') {
                    this.children = [];
                    for (const elem of args) {
                        this.children.push(ASTree.buildAST(elem));
                    }
                }
            } else {
              this.children = null;
              this.value = value;
            }
            return this;
        }
    
        static buildAST(node) {
            const result = new ASTree();
    
            if (Array.isArray(node)) {
                const operator = node[0];
                const args = node[1];
                const instruction = Array.isArray(args) ? 'MULTIPLE' : 'UNARY';
                return result._innerBuildAST(instruction, operator, args);
            }
    
            return result._innerBuildAST('ARGUMENT', null, null, node);
        }
    }

https://replit.com/@hexlet/algorithms-trees-ast-js#index.js

Python
    
    
    class ASTree:
        def __init__(self):
            self.instructionType = None
            self.operator = None
            self.children = None
            self.value = None
    
        def _innerBuildAST(self, instruction, operator, args, value=None):
            if args is None and value is None:
                raise Exception('У узла должно быть значение или дочерние узлы')
            if (args is None and instruction != 'ARGUMENT') or (value is None and instruction == 'ARGUMENT'):
                raise Exception('У узла указан некорректный тип')
    
            self.operator = operator
            self.instructionType = instruction
            if self.instructionType != 'ARGUMENT':
                self.value = None
                if self.instructionType == 'UNARY':
                    self.children = ASTree.buildAST(args)
                if self.instructionType == 'MULTIPLE':
                    self.children = []
                    for elem in args:
                        self.children.append(ASTree.buildAST(elem))
            else:
                self.children = None
                self.value = value
            return self
    
        @staticmethod
        def buildAST(node):
            result = ASTree()
    
            if isinstance(node, list):
                operator = node[0]
                args = node[1]
                instruction = 'MULTIPLE' if isinstance(args, list) else 'UNARY'
                return result._innerBuildAST(instruction, operator, args)
    
            return result._innerBuildAST('ARGUMENT', None, None, node)

https://replit.com/@hexlet/algorithms-trees-ast-pyton#main.py

PHP
    
    
    <?php
    class ASTree {
      public $instructionType;
      public $operator;
      public $children;
      public $value;
    
      public function __construct() {
        $this->instructionType = null;
        $this->operator = null;
        $this->children = null;
        $this->value = null;
      }
    
      public function _innerBuildAST($instruction, $operator, $args, $value = null) {
        if ($args === null && $value === null) {
          throw new Exception('У узла должно быть значение или дочерние узлы');
        }
        if (($args === null && $instruction !== 'ARGUMENT') || ($value === null && $instruction === 'ARGUMENT')) {
          throw new Exception('У узла указан некорректный тип');
        }
    
        $this->operator = $operator;
        $this->instructionType = $instruction;
        if ($this->instructionType !== 'ARGUMENT') {
          $this->value = null;
          if ($this->instructionType === 'UNARY') {
            $this->children = self::buildAST($args);
          }
          if ($this->instructionType === 'MULTIPLE') {
            $this->children = [];
            foreach ($args as $elem) {
              $this->children[] = self::buildAST($elem);
            }
          }
        } else {
          $this->children = null;
          $this->value = $value;
        }
        return $this;
      }
    
      public static function buildAST($node) {
        $result = new ASTree();
    
        if (is_array($node)) {
          $operator = $node[0];
          $args = $node[1];
          $instruction = is_array($args) ? 'MULTIPLE' : 'UNARY';
          return $result->_innerBuildAST($instruction, $operator, $args);
        }
    
        return $result->_innerBuildAST('ARGUMENT', null, null, $node);
      }
    }

https://replit.com/@hexlet/algorithms-tress-ast-php#main.php

Java
    
    
    class ASTree {
        // ...
    
        private ASTree innerBuildAST(Object instruction, String operator, Object args, Object value) {
            if ((args == null && value == null) || (args != null && value != null)) {
                throw new IllegalArgumentException("У узла должно быть значение или дочерние узлы");
            }
            if ((args == null && instruction != InstructionType.ARGUMENT)
                || (value == null && instruction == InstructionType.ARGUMENT)) {
    
                throw new IllegalArgumentException("У узла указан некорректный тип");
            }
    
            this.operator = operator;
            this.instructionType = (InstructionType) instruction;
            if (this.instructionType != InstructionType.ARGUMENT) {
                this.value = null;
                if (this.instructionType == InstructionType.UNARY) {
                    this.children = new ASTree[] { buildAST(args) };
                }
                if (this.instructionType == InstructionType.MULTIPLE) {
                    this.children = new ASTree[((Object[]) args).length];
                    for (int i = 0; i < ((Object[]) args).length; i++) {
                        this.children[i] = buildAST(((Object[]) args)[i]);
                    }
                }
            } else {
                this.children = null;
                this.value = value;
            }
            return this;
        }
    
        public static ASTree buildAST(Object node) {
            ASTree result = new ASTree();
    
            if (node instanceof Object[]) {
                Object[] arr = (Object[]) node;
                String operator = (String) arr[0];
                Object args = arr[1];
                InstructionType instruction = (args instanceof Object[]) ? InstructionType.MULTIPLE : InstructionType.UNARY;
                return result.innerBuildAST(instruction, operator, args, null);
            }
    
            return result.innerBuildAST(InstructionType.ARGUMENT, null, null, node);
        }
    }

https://replit.com/@hexlet/algorithms-tress-ast-java#src/main/java/ASTree.java

Здесь мы видим подход к построению через статический метод. Он позволит нам описать входные параметры дерева в виде массива. Для наглядности возьмем такой пример:

Его можно записать так:
    
    
    ['assign',['a',['sum',[['multiply',[5,10]],['sqrt',6]]]]]

Такой способ записи программы называется польская нотация. Ее часто используют при разборе операций в различных вычислительных машинах. Сама ее структура наглядно показывает последовательность выполнения операций.

Чтобы построить дерево для нашего примера, вызовем наш класс с помощью следующей команды:
    
    
    const structure = ['assign',['a',['sum',[['multiply',[5,10]],['sqrt',6]]]]];
    console.log(ASTree.buildAST(structure));
    
    // => ASTree {
    // =>   instructionType: 'multiple',
    // =>     operator: 'assign',
    // =>       children: [
    // =>         ASTree {
    // =>           instructionType: 'argument',
    // =>           operator: null,
    // =>           children: null,
    // =>           value: 'a'
    // =>         },
    // =>         ASTree {
    // =>           instructionType: 'multiple',
    // =>           operator: 'sum',
    // =>           children: [Array],
    // =>           value: null
    // =>         }
    // =>       ],
    // =>         value: null
    // => }

Python
    
    
    structure = ['assign', ['a', ['sum', [['multiply', [5, 10]], ['sqrt', 6]]]]]
    print(ASTree.buildAST(structure))

PHP
    
    
    <?php
    $structure = ['assign', ['a', ['sum', [['multiply', [5, 10]], ['sqrt', 6]]]]];
    var_dump(ASTree::buildAST($structure));
    // => object(ASTree)#1 (4) {
    // =>   ["instructionType"]=>
    // =>   string(8) "multiple"
    // =>   ["operator"]=>
    // =>   string(6) "assign"
    // =>   ["children"]=>
    // =>   array(2) {
    // =>     [0]=>
    // =>     object(ASTree)#2 (4) {
    // =>       ["instructionType"]=>
    // =>       string(8) "argument"
    // =>       ["operator"]=>
    // =>       NULL
    // =>       ["children"]=>
    // =>       NULL
    // =>       ["value"]=>
    // =>       string(1) "a"
    // =>     }
    // =>     [1]=>
    // =>     object(ASTree)#3 (4) {
    // =>       ["instructionType"]=>
    // =>       string(8) "multiple"
    // =>       ["operator"]=>
    // =>       string(3) "sum"
    // =>       ["children"]=>
    // =>       array(2) {
    // =>         [0]=>
    // =>         object(ASTree)#4 (4) {
    // =>           ["instructionType"]=>
    // =>           string(8) "multiple"
    // =>           ["operator"]=>
    // =>           string(8) "multiply"
    // =>           ["children"]=>
    // =>           array(2) {
    // =>             [0]=>
    // =>             object(ASTree)#5 (4) {
    // =>               ["instructionType"]=>
    // =>               string(8) "argument"
    // =>               ["operator"]=>
    // =>               NULL
    // =>               ["children"]=>
    // =>               NULL
    // =>               ["value"]=>
    // =>               int(5)
    // =>             }
    // =>             [1]=>
    // =>             object(ASTree)#6 (4) {
    // =>               ["instructionType"]=>
    // =>               string(8) "argument"
    // =>               ["operator"]=>
    // =>               NULL
    // =>               ["children"]=>
    // =>               NULL
    // =>               ["value"]=>
    // =>               int(10)
    // =>             }
    // =>           }
    // =>           ["value"]=>
    // =>           NULL
    // =>         }
    // =>         [1]=>
    // =>         object(ASTree)#7 (4) {
    // =>           ["instructionType"]=>
    // =>           string(5) "unary"
    // =>           ["operator"]=>
    // =>           string(4) "sqrt"
    // =>           ["children"]=>
    // =>           object(ASTree)#8 (4) {
    // =>             ["instructionType"]=>
    // =>             string(8) "argument"
    // =>             ["operator"]=>
    // =>             NULL
    // =>             ["children"]=>
    // =>             NULL
    // =>             ["value"]=>
    // =>             int(6)
    // =>           }
    // =>           ["value"]=>
    // =>           NULL
    // =>         }
    // =>       }
    // =>       ["value"]=>
    // =>       NULL
    // =>     }
    // =>   }
    // =>   ["value"]=>
    // =>   NULL
    // => }

Java
    
    
    Object[] structure = {
        "assign", new Object[]{
            "a", new Object[]{
                "sum", new Object[]{
                    new Object[]{"multiply", 5, 10},
                    new Object[]{"sqrt", 6}
                }
            }
        }
    };
    
    ASTree.buildAST(structure);

## Выводы

В этом уроке мы познакомились со специальным видом деревьев — AST-деревьями. С их помощью можно описать полное содержимое программы без лишних деталей — комментариев, фигурных скобок, отступов и других требований к оформлению исходного кода. Основная сфера применения этих деревьев — компиляторы и интерпретаторы исходного кода, которые переводят вашу программу на машинопонятный язык.

AST-деревья не зависят от конкретного языка, поэтому их можно использовать в инструментах автоматического перевода программы на другой язык. Кроме того, GitHub Copilot и другие современные средства искусственного интеллекта могут использовать такие деревья. Они предсказывают действия разработчика, предлагают ему уже готовую реализацию будущей функции и таким образом позволяют писать качественный код гораздо быстрее.
