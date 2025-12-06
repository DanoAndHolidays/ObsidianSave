# 更新State中的数组
## 在没有 mutation 的前提下更新数组 [](https://zh-hans.react.dev/learn/updating-arrays-in-state#updating-arrays-without-mutation "Link for 在没有 mutation 的前提下更新数组")

在 JavaScript 中，数组只是另一种对象。[同对象一样](https://zh-hans.react.dev/learn/updating-objects-in-state)，**你需要将 React state 中的数组视为只读的**。这意味着你不应该使用类似于 `arr[0] = 'bird'` 这样的方式来重新分配数组中的元素，也不应该使用会直接修改原始数组的方法，例如 `push()` 和 `pop()`。

相反，每次要更新一个数组时，你需要把一个**新**的数组传入 state 的 setting 方法中。为此，你可以通过使用像 `filter()` 和 `map()` 这样不会直接修改原始值的方法，从原始数组生成一个新的数组。然后你就可以将 state 设置为这个新生成的数组。

下面是常见数组操作的参考表。当你操作 React state 中的数组时，你需要避免使用左列的方法，而首选右列的方法：

| |避免使用 (会改变原始数组)|推荐使用 (会返回一个新数组）|
|---|---|---|
|添加元素|`push`，`unshift`|`concat`，`[...arr]` 展开语法（[例子](https://zh-hans.react.dev/learn/updating-arrays-in-state#adding-to-an-array)）|
|删除元素|`pop`，`shift`，`splice`|`filter`，`slice`（[例子](https://zh-hans.react.dev/learn/updating-arrays-in-state#removing-from-an-array)）|
|替换元素|`splice`，`arr[i] = ...` 赋值|`map`（[例子](https://zh-hans.react.dev/learn/updating-arrays-in-state#replacing-items-in-an-array)）|
|排序|`reverse`，`sort`|先将数组复制一份（[例子](https://zh-hans.react.dev/learn/updating-arrays-in-state#making-other-changes-to-an-array)）|

或者，你可以[使用 Immer](https://zh-hans.react.dev/learn/updating-arrays-in-state#write-concise-update-logic-with-immer) ，这样你便可以使用表格中的所有方法了。

## 数组的常见操作

### 更新对象数组中对象的属性

这里要使用`map()`与展开运算符来实现：

```js
import { useState } from 'react';

const initialProducts = [{
  id: 0,
  name: 'Baklava',
  count: 1,
}, {
  id: 1,
  name: 'Cheese',
  count: 5,
}, {
  id: 2,
  name: 'Spaghetti',
  count: 2,
}];

export default function ShoppingCart() {
  const [
    products,
    setProducts
  ] = useState(initialProducts)

  function handleIncreaseClick(productId) {
    setProducts(products.map(product => {
      if (product.id === productId) {
        return {
          ...product,
          count: product.count + 1
        };
      } else {
        return product;
      }
    }))
  }

  return (
    <ul>
      {products.map(product => (
        <li key={product.id}>
          {product.name}
          {' '}
          (<b>{product.count}</b>)
          <button onClick={() => {
            handleIncreaseClick(product.id);
          }}>
            +
          </button>
        </li>
      ))}
    </ul>
  );
}
```

### 向数组中插入元素

使用扩展运算符与`slice()`

```js
  function handleClick() {
    const insertAt = 1; // 可能是任何索引
    const nextArtists = [
      // 插入点之前的元素：
      ...artists.slice(0, insertAt),
      // 新的元素：
      { id: nextId++, name: name },
      // 插入点之后的元素：
      ...artists.slice(insertAt)
    ];
    setArtists(nextArtists);
    setName('');
  }
```

### 替换数组中的元素

基本的思想和修改对象数组一样‘

```js
function handleIncrementClick(index) {
    const nextCounters = counters.map((c, i) => {
      if (i === index) {
        // 递增被点击的计数器数值
        return c + 1;
      } else {
        // 其余部分不发生变化
        return c;
      }
    });
    setCounters(nextCounters);
  }
```

### 添加与删除数组中的内容

```js
setArtists( // 替换 state  
	[ // 是通过传入一个新数组实现的  
		...artists, // 新数组包含原数组的所有元素  
		{ id: nextId++, name: name } // 并在末尾添加了一个新的元素  
	]  
);
```

删除使用`filter()`实现

### 使用Immer实现

```js
import { useState } from 'react';
import { useImmer } from 'use-immer';
import AddTodo from './AddTodo.js';
import TaskList from './TaskList.js';

let nextId = 3;
const initialTodos = [
  { id: 0, title: 'Buy milk', done: true },
  { id: 1, title: 'Eat tacos', done: false },
  { id: 2, title: 'Brew tea', done: false },
];

export default function TaskApp() {
  const [todos, setTodos] = useImmer(
    initialTodos
  );

  function handleAddTodo(title) {
    setTodos(draft=>{
      draft.push({
        id: nextId++,
        title: title,
        done: false
      });
    }
      
    )
  }

  function handleChangeTodo(nextTodo) {
    // const todo = todos.find(t =>
    //   t.id === nextTodo.id
    // );
    // todo.title = nextTodo.title;
    // todo.done = nextTodo.done;

    setTodos(draft=>{
      const test=draft.find(t=>t.id===nextTodo.id)
      test.title=nextTodo.title
      test.done=nextTodo.done
      
    })
  }

  function handleDeleteTodo(todoId) {
    // const index = todos.findIndex(t =>
    //   t.id === todoId
    // );
    // todos.splice(index, 1);

    setTodos(draft=>{
      const index = draft.findIndex(t =>
       t.id === todoId
     );

      draft.splice(index,1)
    })
  }
// ...
```