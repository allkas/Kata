---
tags: [algorithms, trees, hexlet]
source: "Алгоритмы на деревьях"
---

# KD-деревья

  * Что такое KD-деревья
  * Как устроено KD-дерево
  * Операции над KD-деревом
  * Выводы



Одна из самых популярных практических задач в современном программировании — это **поиск ближайших соседей**. Например, поиск ближайших соседей встречается в медицине. Так строятся прогнозные модели заболеваемости, в которых оцениваются контакты в ближайшем окружении заболевшего:

На рисунке выше вы можете увидеть координатную плоскость, на которой расположены:

  * «Заболевшие» красные точки

  * «Здоровые» синие точки

  * «Опасные зоны» — розовые окружности вокруг красных точек




Синяя точка подвергается риску заболеть, если она входит в опасную зону — располагается слишком близко к красной точке. Другими словами, чтобы синяя точка не заболела, расстояние между ней и красной точкой должно быть выше **порогового значения**.

В этом примере задача сводится к поиску синих точек с высоким риском заболеть. Один из способов решения такой задачи — это кластеризация на основе методов машинного обучения. Но есть и альтернатива — это **KD-деревья** , о которых мы и поговорим в этом уроке.

## Что такое KD-деревья

**KD-деревья** — это дерево, вершины которого представлены в форме точек в некоторой  -мерной системе координат. Еще их называют _K-dimensional trees_ или « -мерные деревья».

В этом курсе мы рассматриваем только KD-деревья в двумерном пространстве. Но с его помощью можно вычислять ближайшего соседа и на более сложных системах координат. Например, так выглядит трехмерное дерево:

Обратим внимание, что эффективность поиска ближайших соседей в KD-дереве снижается при больших значениях  .

В качестве правила обычно принимают, что число вершин в дереве должно быть намного больше значения  . Если это правило не соблюдать, то алгоритм поиска на основе KD-дерева будет работать с почти той же скоростью, что и обычный последовательный поиск.

## Как устроено KD-дерево

Чтобы изучить строение KD-дерева, возьмем для примера 13 точек в двумерной системе координат:

Чтобы построить по ним дерево, мы будем руководствоваться следующим алгоритмом:

  1. Выберем ось в наборе данных

  2. Найдем на этой оси **медианное значение числа точек**. Для двумерного пространства это значит, что справа и слева от значения должно быть одинаковое число точек. Если у нас четное число точек, то можно левое подпространство сделать больше правого

  3. Проведем линию, которая разделит пространство на две части

  4. Изменим ось и нарисуем свою медиану для каждого нового подпространства




Пройдя эти четыре шага, мы выполним первое **разделение** дерева. Далее мы повторяем все шаги до тех пор, пока точек больше не останется.

Посмотрим, как разделение работает на нашем примере — двумерном KD-дереве с 13 точками:

**Этап 1**. Разделим пространство на основании оси  :

**Этап 2**. Выполним второе разделение на основании оси  :

**Этап 3**. Продолжаем разделение, пока это возможно:

**Этап 4**. Строим итоговое дерево, исходя из разделения пространства:

На последнем рисунке видно, что получившееся дерево аналогично сбалансированному бинарному дереву. Разница только в том, что в качестве полезной нагрузки в KD-дереве хранится точка с координатами.

В таком случае JavaScript-код узла будет выглядеть так:
    
    
    class KDTreeNode {
        constructor(obj, dimension, parent) {
            this.obj = obj;
            this.dimension = dimension;
            this.right = null;
            this.left = null;
            this.parent = parent;
        }
    
    }

Java
    
    
    class KDTreeNode {
        List<Map<String, Integer>> obj;
        List<String> dimension;
        KDTreeNode right;
        KDTreeNode left;
        KDTreeNode parent;
    
        KDTreeNode(List<Map<String, Integer>> obj, List<String> dimension, KDTreeNode parent) {
            this.parent = parent;
            this.obj = obj;
            this.dimension = dimension;
        }
    }

Python
    
    
    class KDTreeNode:
        def __init__(self, obj, dimension, parent):
            self.obj = obj
            self.dimension = dimension
            self.right = None
            self.left = None
            self.parent = parent

PHP
    
    
    <?php
    class KDTreeNode {
        public $obj;
        public array $dimension;
        public ?self $right = null;
        public ?self $left = null;
        public self $parent;
    
        public function __construct($obj, $dimension, $parent) {
            $this->parent = $parent;
            $this->obj = $obj;
            $this->dimension = $dimension;
        }
    }

## Операции над KD-деревом

Основное отличие KD-дерева можно увидеть при работе с методом, который отвечает за построение дерева из массива точек:
    
    
    class KDTreeNode {
      // ...
    
        static buildTree(points, depth, dimensions, parent) {
            let dim = depth % dimensions.length;
            let median, node;
    
            if (points.length === 0) {
                return null;
            }
            if (points.length === 1) {
                return new KDTreeNode(points[0], dim, parent);
            }
    
            points.sort(function(a, b) {
                return a[dimensions[dim]] - b[dimensions[dim]];
            });
    
            median = Math.floor(points.length / 2);
            node = new KDTreeNode(points[median], dim, parent);
    
            node.left = KDTreeNode.buildTree(points.slice(0, median), depth + 1, dimensions, node);
            node.right = KDTreeNode.buildTree(points.slice(median + 1), depth + 1, dimensions, node);
    
            return node;
        }
    }

Java
    
    
    class KDTreeNode {
        // ...
    
        public static KDTreeNode buildTree(
            List<Map<String, Integer>>points, int depth, List<String> dimensions, KDTreeNode parent) {
                var dim = depth % dimensions.size(); // Здесь выбираем, на какой оси проводим разбиение пространства
                int median;
                KDTreeNode node;
    
                if (points.size() == 0) {
                    return null;
                }
                if (points.size() == 1) {
                    return new KDTreeNode(points.get(0), dim, parent);
                }
    
                points.sort((a, b) -> a.get(dimensions.get(dim)) - b.get(dimensions.get(dim)));
    
                median = points.size() / 2; // Выбираем медиану и добавляем ее в дерево
                node = new KDTreeNode(points.get(median), dim, parent);
    
                // Правое и левое подпростанство продолжаем делить рекурсивно
                node.left = KDTreeNode.buildTree(points.subList(0, median), depth + 1, dimensions, node);
                node.right = KDTreeNode.buildTree(points.subList(median + 1, points.size()), depth + 1, dimensions, node);
    
                return node;
    
            }
    }

Python
    
    
    @staticmethod
    def build_tree(points, depth, dimensions, parent):
        dim = depth % len(dimensions)
        if len(points) == 0:
            return None
        if len(points) == 1:
            return KDTreeNode(points[0], dim, parent)
        points.sort(key=lambda point: point[dimensions[dim]])
        median = len(points) // 2
        node = KDTreeNode(points[median], dim, parent)
        node.left = KDTreeNode.build_tree(points[:median], depth+1, dimensions, node)
        node.right = KDTreeNode.build_tree(points[median+1:], depth+1, dimensions, node)
        return node

PHP
    
    
    <?php
    
    class KDTreeNode
    {
        // ...
    
        public static function buildTree($points, $depth, $dimensions, $parent)
        {
            // Здесь выбираем, на какой оси проводим разбиение пространства
            $dim = $depth % count($dimensions);
            $median;
            $node;
    
            if (count($points) == 0) {
                return null;
            }
            if (count($points) == 1) {
                return new KDTreeNode($points[0], $dim, $parent);
            }
    
            usort($points, function($a, $b) use ($dimensions, $dim) {
                return $a[$dimensions[$dim]] - $b[$dimensions[$dim]];
            });
    
            // Выбираем медиану и добавляем ее в дерево
            $median = count($points) / 2;
            $node = new KDTreeNode($points[$median], $dim, $parent);
    
            // Правое и левое подпростанство продолжаем делить рекурсивно
            $node->left = self::buildTree(array_slice($points, 0, $median), $depth + 1, $dimensions, $node);
            $node->right = self::buildTree(array_slice($points, $median + 1, count($points)), $depth + 1, $dimensions, $node);
    
            return $node;
        }
    }

Вызвать построение дерева можно при помощи следующего примера:
    
    
    const points = [
        {x: 1, y: 2},
        {x: 3, y: 4},
        {x: 5, y: 6},
        {x: 7, y: 8}
    ];
    
    const tree = KDTreeNode.buildTree(points, 0, ["x", "y"], null);

Java
    
    
    List<Map<String, Integer>> points = new ArrayList<>();
    points.add(Map.of("x", 1, "y", 1));
    points.add(Map.of("x", 3, "y", 4));
    points.add(Map.of("x", 5, "y", 6));
    points.add(Map.of("x", 7, "y", 8));
    
    List<String> dimensions = List.of("x", "y");
    
    KDTreeNode tree = KDTreeNode.buildTree(points, 0, dimensions, null);

Python
    
    
    points = [
        {"x": 1, "y": 2},
        {"x": 3, "y": 4},
        {"x": 5, "y": 6},
        {"x": 7, "y": 8},
    ]
    
    tree = KDTreeNode.buildTree(points, 0, ["x", "y"], None)

PHP
    
    
    <?php
    $points = [
      ["x" => 1, "y" => 1],
      ["x" => 3, "y" => 4],
      ["x" => 5, "y" => 6],
      ["x" => 7, "y" => 8]
    ];
    
    $dimensions = ["x", "y"];
    
    $tree = KDTreeNode::buildTree($points, 0, $dimensions, null);

Структура KD-дерева не отличается от бинарного дерева. Поэтому методы удаления и поиска узлов работают так же, как в бинарном дереве:
    
    
    class KDTreeNode {
      // ...
    
        insertNode(value) {
            this.insertNodeHelper(value, this);
        }
    
        insertNodeHelper(value, parentNode) {
            if (value[this.dimension] < parentNode.obj[parentNode.dimension]) {
                if (parentNode.left === null) {
                    parentNode.left = new KDTreeNode(
                        value,
                        this.dimension,
                        parentNode,
                    );
                } else {
                    this.insertNodeHelper(value, parentNode.left);
                }
            }
            if (value[this.dimension] >= parentNode.obj[parentNode.dimension]) {
                if (parentNode.right === null) {
                    parentNode.right = new KDTreeNode(
                        value,
                        this.dimension,
                        parentNode,
                    );
                } else {
                    this.insertNodeHelper(value, parentNode.right);
                }
            }
        }
    }

Java
    
    
    class KDTreeNode {
        // ...
        public void insertNode(Map<String, Integer> value) {
            insertNode(value, this);
        }
    
        private void insertNode(Map<String, Integer> value, KDTreeNode parent) {
            if (value.get(dimension) < parentNode.obj.get(parentNode.dimension)){
                if (parentNode.left == null){
                    parentNode.left = new KDTreeNode(value, dimension, parentNode);
                }
                else {
                    insertNode(value, parentNode.left);
                }
            }
            if (value[this.dimension] < parentNode.obj[parentNode.dimension]){
                if (parentNode.right == null) {
                    parentNode.right = new KDTreeNode(value, this.dimension, parentNode);
                }
                else {
                    this.#insertNode(value, parentNode.right);
                }
            }
        }
    }

Python
    
    
    def insertNode(self, value):
        return self._insertNode(value, self)
    
    def _insertNode(self, value, parentNode):
        if value[parentNode.dimension] < parentNode.obj[parentNode.dimension]:
            if parentNode.left is None:
                parentNode.left = KDTreeNode(value, parentNode.dimension, parentNode)
            else:
                self._insertNode(value, parentNode.left)
        if value[parentNode.dimension] >= parentNode.obj[parentNode.dimension]:
            if parentNode.right is None:
                parentNode.right = KDTreeNode(value, parentNode.dimension, parentNode)
            else:
                self._insertNode(value, parentNode.right)

PHP
    
    
    class KDTreeNode
    {
        // ...
    
        public function insertNode($value)
        {
            $this->insertNodeRecursive($value, $this);
        }
    
        private function insertNodeRecursive($value, $parentNode) {
            if ($value[$this->dimension] < $parentNode->obj[$parentNode->dimension]) {
                if ($parentNode->left == null) {
                    $parentNode->left = new KDTreeNode($value, $this->dimension, $parentNode);
                } else {
                    $this->insertNodeRecursive($value, $parentNode->left);
                }
            }
            if ($value[$this->dimension] >= $parentNode->obj[$parentNode->dimension]) {
                if ($parentNode->right == null) {
                    $parentNode->right = new KDTreeNode($value, $this->dimension, $parentNode);
                } else {
                    $this->insertNodeRecursive($value, $parentNode->right);
                }
            }
        }
    }
    
    
    class KDTreeNode {
      // ...
    
        removeNode(value) {
            this.#removeNodeHelper(value, this);
        }
    
        #removeNodeHelper(value, node) {
            if (node === null) {
                return null; // Узел не найден, возвращаем null
            }
    
            if (value[this.dimension] < node.obj[node.dimension]) {
                node.left = this.removeNodeHelper(value, node.left);
            } else if (value[this.dimension] > node.obj[node.dimension]) {
                node.right = this.removeNodeHelper(value, node.right);
            } else {
                // Узел найден
                if (node.left === null) {
                    return node.right; // Узел имеет только правого потомка
                } else if (node.right === null) {
                    return node.left; // Узел имеет только левого потомка
                }
    
                // Узел имеет обоих потомков
                let original = node;
                node = node.right;
                while (node.left) {
                    node = node.left;
                }
    
                node.right = this.#removeMin(original.right);
                node.left = original.left;
            }
            return node;
        }
    
        #removeMin(node) {
            if (node.left === null) {
                return node.right; // Если нет левого потомка, возвращаем правого потомка
            }
            node.left = this.removeMin(node.left); // Рекурсивно вызываем removeMin для левого потомка
            return node;
        }
    }

Java
    
    
    class KDTreeNode {
        // ...
    
        public void removeNode(Map<String, Integer> value) {
            removeNode(value, this);
        }
    
        private KDTreeNode removeNode(Map<String, Integer> value, KDTreeNode node) {
            if (node == null) {
                return null;
            }
    
            if (value.get(this.dimension) < node.obj.get(this.dimension)) {
                node.left = this.removeNode(node.left, value);
            }
            else if (value.get(this.dimension) > node.obj.get(this.dimension)) {
                node.right = this.removeNode(node.right, value);
            }
            else {
                if (node.left == null) {
                    return node.right;
                }
                if (node.right == null) {
                    return node.left;
                }
            }
    
            KDTreeNode original = node;
            node = node.right;
            while (node.left != null) {
                node = node.left;
            }
    
            node.right = removeMin(original.right);
            node.left = original.left;
        }
    }

Python
    
    
    def removeNode(self, value):
      return self._removeNode(value, self)
    
    def _removeNode(self, value, node):
      if node is None:
        return None
    
      if value[self.dimension] < node.obj[self.dimension]:
        node.left = self._removeNode(value, node.left)
      elif value[self.dimension] > node.obj[self.dimension]:
          node.right = self._removeNode(value, node.right)
      else:
          if node.left is None:
              return node.right
          if node.right is None:
              return node.left
    
      original = node
      node = node.right
      while node.left:
          node = node.left
    
      node.right = self._removeMin(original.right)
      node.left = original.left

PHP
    
    
    <?php
    class KDTreeNode
    {
        // ...
    
        public function removeNode($value)
        {
            return $this->removeNodeRecursive($value, $this);
        }
    
        private function removeNodeRecursive($value, $node)
        {
            if ($node == null) return null;
    
            if ($value$this->dimension < $node->obj[$this->dimension]) {
                $node->left = $this->removeNodeRecursive($value, $node->left);
            } else if ($value[$this->dimension] > $node->obj[$this->dimension]) {
                $node->right = $this->removeNodeRecursive($value, $node->right);
            } else {
                if ($node->left == null) return $node->right;
                if ($node->right == null) return $node->left;
    
                $original = $node;
                $node = $node->right;
    
                while ($node->left) {
                    $node = $node->left;
                }
    
                $node->right = $this->removeMin($original->right);
                $node->left = $original->left;
            }
        }
    }

Еще одной отличительной особенностью KD-дерева считается реализация метода поиска ближайшего соседа:
    
    
    class KDTreeNode {
      // ...
    
        metric(point1, point2) {
            return Math.sqrt(
                Math.pow(point1.x - point2.x, 2) + Math.pow(point1.y - point2.y, 2),
            );
        }
    
        nearestSearch(point, node, bestNodes, maxNodes) {
            if (node === null) {
                return; // Достигнут конец дерева
            }
    
            let dimension = this.dimension;
            let ownDistance = this.metric(point, node.obj);
            let linearPoint = {};
            let linearDistance;
            let bestChild, otherChild;
    
            for (let i = 0; i < this.dimension.length; i++) {
                if (i === this.dimension) {
                    linearPoint[this.dimension[i]] = point[this.dimension[i]];
                } else {
                    linearPoint[this.dimension[i]] = node.obj[this.dimension[i]];
                }
            }
    
            linearDistance = this.metric(linearPoint, node.obj);
    
            if (
                bestNodes.length < maxNodes ||
                ownDistance < bestNodes[bestNodes.length - 1][1]
            ) {
                if (bestNodes.length === maxNodes) {
                    bestNodes.pop(); // Удаляем последний элемент, если массив лучших узлов уже заполнен
                }
                bestNodes.push([node.obj, ownDistance]); // Добавляем текущий узел в массив лучших узлов
                bestNodes.sort((a, b) => a[1] - b[1]); // Сортируем массив лучших узлов по расстоянию
            }
    
            if (
                bestNodes.length < maxNodes ||
                Math.abs(linearDistance) < bestNodes[bestNodes.length - 1][1]
            ) {
                if (linearDistance < 0) {
                    bestChild = node.right;
                    otherChild = node.left;
                } else {
                    bestChild = node.left;
                    otherChild = node.right;
                }
                this.nearestSearch(point, bestChild, bestNodes, maxNodes); // Рекурсивно ищем в ближайшем поддереве
                if (Math.abs(linearDistance) < bestNodes[bestNodes.length - 1][1]) {
                    this.nearestSearch(point, otherChild, bestNodes, maxNodes); // Поиск в другом поддереве, если необходимо
                }
            }
        }
    }

https://replit.com/@hexlet/algorithms-trees-kd-js#index.js

Java
    
    
    class KDTreeNode {
        // ...
    
        public KDTreeNode nearestSearch(Map<String, Integer> point, KDTreeNode node) {
            KDTreeNode bestChild;
            var dimension = dimensions.get(node.get("dimension"));
            var ownDistance = metric(point, node.obj),
            linearPoint = new HashMap<String, Integer>();
            double linearDistance;
            KDTreeNode otherChild;
            int i;
    
            for (var i = 0; i < dimensions.length(); i += 1) {
                if (i == node.dimension) {
                    linearPoint.put(dimensions.get(i), point.get(dimensions.get(i)));
                } else {
                    linearPoint.put(dimensions.get(i), node.obj.get(dimensions.get(i)));
                }
            }
    
            linearDistance = metric(linearPoint, node.obj);
    
            if (node.right == null && node.left == null) {
                if (bestNodes.size() < maxNodes || ownDistance < bestNodes.get(0).get(1)) {
                    this.saveNode(node, ownDistance);
                }
                return;
            }
    
            if (node.right == null) {
                bestChild = node.left;
            } else if (node.left == null) {
                bestChild = node.right;
            } else {
                if (point.get(dimension) < node.obj.get(dimension)) {
                    bestChild = node.left;
                } else {
                    bestChild = node.right;
                }
            }
    
            nearestSearch(point, bestChild);
    
            if (bestNodes.size() < maxNodes || ownDistance < bestNodes.get(0).get(1)) {
                this.saveNode(node, ownDistance);
            }
    
            if (bestNodes.size() < maxNodes || Math.abs(linearDistance) < bestNodes.get(0).get(1)) {
                if (bestChild == node.left) {
                    otherChild = node.right;
                } else {
                    otherChild = node.left;
                }
                if (otherChild != null) {
                    nearestSearch(point, otherChild);
                }
            }
        }
    }

Python
    
    
    def nearestSearch(point, node):
      bestChild = None
      dimension = dimensions[node.dimension]
      ownDistance = metric(point, node.obj)
      linearPoint = {}
      linearDistance = 0
      otherChild = None
    
      for i in range(len(dimensions)):
          if i == node.dimension:
              linearPoint[dimensions[i]] = point[dimensions[i]]
          else:
              linearPoint[dimensions[i]] = node.obj[dimensions[i]]
    
      linearDistance = metric(linearPoint, node.obj)
    
      if node.right == None and node.left == None:
          if bestNodes.qsize() < maxNodes or ownDistance < bestNodes.queue[0][1]:
              saveNode(node, ownDistance)
          return
    
      if node.right == None:
          bestChild = node.left
      elif node.left == None:
          bestChild = node.right
      else:
          if point[dimension] < node.obj[dimension]:
              bestChild = node.left
          else:
              bestChild = node.right
    
      nearestSearch(point, bestChild)
    
      if bestNodes.qsize() < maxNodes or ownDistance < bestNodes.queue[0][1]:
          saveNode(node, ownDistance)
    
      if bestNodes.qsize() < maxNodes or abs(linearDistance) < bestNodes.queue[0][1]:
          if bestChild == node.left:
              otherChild = node.right
          else:
              otherChild = node.left
          if otherChild != None:
              nearestSearch(point, otherChild)

PHP
    
    
    <?php
    
    class KDTreeNode
    {
        private function nearestSearch($point, $node)
        {
            $bestChild = null;
            $dimension = $dimensions[$node->dimension];
            $ownDistance = metric($point, $node->obj);
            $linearPoint = [];
            $linearDistance = null;
            $otherChild = null;
    
            for ($i = 0; $i < count($dimensions); $i += 1) {
                if ($i === $node->dimension) {
                    $linearPoint[$dimensions[$i]] = $point[$dimensions[$i]];
                } else {
                    $linearPoint[$dimensions[$i]] = $node->obj[$dimensions[$i]];
                }
            }
    
            $linearDistance = metric($linearPoint, $node->obj);
    
            if ($node->right === null && $node->left === null) {
                if (count($bestNodes) < $maxNodes || $ownDistance < $bestNodes[0][1]) {
                    $this->saveNode($node, $ownDistance);
                }
                return;
            }
    
            if ($node->right === null) {
                $bestChild = $node->left;
            } elseif ($node->left === null) {
                $bestChild = $node->right;
            } else {
                if ($point[$dimension] < $node->obj[$dimension]) {
                    $bestChild = $node->left;
                } else {
                    $bestChild = $node->right;
                }
            }
    
            $this->nearestSearch($point, $bestChild);
    
            if (count($bestNodes) < $maxNodes || $ownDistance < $bestNodes[0][1]) {
                $this->saveNode($node, $ownDistance);
            }
    
            if (count($bestNodes) < $maxNodes || abs($linearDistance) < $bestNodes[0][1]) {
                if ($bestChild === $node->left) {
                    $otherChild = $node->right;
                } else {
                    $otherChild = $node->left;
                }
                if ($otherChild !== null) {
                    $this->nearestSearch($point, $otherChild);
                }
            }
        }
    }

## Выводы

В этом уроке мы познакомились с KD-деревьями, которые помогают организовать хранение пространственных данных. KD-деревья — это основная альтернатива методам машинного обучения при решении кластеризационных задач.

Поиск ближайших соседей — это одна из популярных задач, стоящих перед программистами. Результаты ее решения нужны в медицине, геологии, картографии и прочих прикладных областях, связанных с кластеризацией пространственных объектов.
