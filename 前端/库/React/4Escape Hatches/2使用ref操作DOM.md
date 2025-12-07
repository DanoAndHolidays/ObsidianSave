# 使用ref操作DOM

由于 React 会自动处理更新 [DOM](https://developer.mozilla.org/docs/Web/API/Document_Object_Model/Introduction) 以匹配你的渲染输出，因此你在组件中通常不需要操作 DOM。但是，有时你可能需要访问由 React 管理的 DOM 元素 —— 例如，让一个节点获得焦点、滚动到它或测量它的尺寸和位置。在 React 中没有内置的方法来做这些事情，所以你需要一个指向 DOM 节点的 **ref** 来实现。

## 获取指向节点的 ref [](https://zh-hans.react.dev/learn/manipulating-the-dom-with-refs#getting-a-ref-to-the-node "Link for 获取指向节点的 ref")

要访问由 React 管理的 DOM 节点，首先，引入 `useRef` Hook：

```js
import { useRef } from 'react';
```

然后，在你的组件中使用它声明一个 ref：

```js
const myRef = useRef(null);
```

最后，将 ref 作为 `ref` 属性值传递给想要获取的 DOM 节点的 JSX 标签：

```js
<div ref={myRef}>
```

`useRef` Hook 返回一个对象，该对象有一个名为 `current` 的属性。最初，`myRef.current` 是 `null`。当 React 为这个 `<div>` 创建一个 DOM 节点时，React 会把对该节点的引用放入 `myRef.current`。然后，你可以从 [事件处理器](https://zh-hans.react.dev/learn/responding-to-events) 访问此 DOM 节点，并使用在其上定义的内置[浏览器 API](https://developer.mozilla.org/docs/Web/API/Element)。

```js
// 你可以使用任意浏览器 API，例如：
myRef.current.scrollIntoView();
```

```js
import { useRef } from 'react';

export default function Form() {
  const inputRef = useRef(null);

  function handleClick() {
    inputRef.current.focus();
  }

  return (
    <>
      <input 
        ref={inputRef} 
        placeholder="点击按钮聚焦到这里"
        style={{ 
          padding: '8px', 
          fontSize: '16px', 
          border: '2px solid #ccc', 
          borderRadius: '4px',
          marginRight: '10px'
        }}
      />
      <button onClick={handleClick}>
        聚焦输入框
      </button>
    </>
  );
}

```

在上面的例子中，ref 的数量是预先确定的。但有时候，你可能需要为列表中的每一项都绑定 ref ，而你又不知道会有多少项。像下面这样做**是行不通的**：

```js
<ul>
  {items.map((item) => {
    // 行不通！
    const ref = useRef(null);
    return <li ref={ref} />;
  })}
</ul>
```

这是因为 **Hook 只能在组件的顶层被调用**。不能在循环语句、条件语句或 `map()` 函数中调用 `useRef` 。

一种可能的解决方案是用一个 ref 引用其父元素，然后用 DOM 操作方法如 [`querySelectorAll`](https://developer.mozilla.org/zh-CN/docs/Web/API/Document/querySelectorAll) 来寻找它的子节点。然而，这种方法很脆弱，如果 DOM 结构发生变化，可能会失效或报错。

另一种解决方案是**将函数传递给 `ref` 属性**。这称为 [`ref` 回调](https://zh-hans.react.dev/reference/react-dom/components/common#ref-callback)。当需要设置 ref 时，React 将传入 DOM 节点来调用你的 ref 回调，并在需要清除它时传入 `null` 。这使你可以维护自己的数组或 [Map](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Map)，并通过其索引或某种类型的 ID 访问任何 ref。

```js
import { useRef, useState } from "react";

export default function CatFriends() {
  const itemsRef = useRef(null);
  const [catList, setCatList] = useState(setupCatList);

  function scrollToCat(cat) {
    const map = getMap();
    const node = map.get(cat);
    node.scrollIntoView({
      behavior: "smooth",
      block: "nearest",
      inline: "center",
    });
  }

  function getMap() {
    if (!itemsRef.current) {
      // 首次运行时初始化 Map。
      itemsRef.current = new Map();
    }
    return itemsRef.current;
  }

  return (
    <>
      <nav>
        <button onClick={() => scrollToCat(catList[0])}>Neo</button>
        <button onClick={() => scrollToCat(catList[5])}>Millie</button>
        <button onClick={() => scrollToCat(catList[8])}>Bella</button>
      </nav>
      <div>
        <ul>
          {catList.map((cat) => (
            <li
              key={cat.id}
              ref={(node) => {
                const map = getMap();
                map.set(cat, node);

                return () => {
                  map.delete(cat);
                };
              }}
            >
              <img src={cat.imageUrl} />
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}

function setupCatList() {
  const catCount = 10;
  const catList = new Array(catCount)
  for (let i = 0; i < catCount; i++) {
    let imageUrl = '';
    if (i < 5) {
      imageUrl = "https://placecats.com/neo/320/240";
    } else if (i < 8) {
      imageUrl = "https://placecats.com/millie/320/240";
    } else {
      imageUrl = "https://placecats.com/bella/320/240";
    }
    catList[i] = {
      id: i,
      imageUrl,
    };
  }
  return catList;
}
```

## 访问另一个组件的 DOM 节点 [](https://zh-hans.react.dev/learn/manipulating-the-dom-with-refs#accessing-another-components-dom-nodes "Link for 访问另一个组件的 DOM 节点")

### 陷阱

Ref 是一个脱围机制。手动操作 **其它** 组件的 DOM 节点可能会让代码变得脆弱。

你可以 [像其它 prop 一样](https://zh-hans.react.dev/learn/passing-props-to-a-component) 将 ref 从父组件传递给子组件。

```js
import { useRef } from 'react';

function MyInput({ ref }) {
  return <input ref={ref} />;
}

function MyForm() {
  const inputRef = useRef(null);
  return <MyInput ref={inputRef} />
}
```

在上面这个例子中，父组件 `MyForm` 创建了一个名为 `inputRef` 的 ref，并且将它传递给了 `MyInput` 子组件。`MyInput` 将这个 ref 传递给 `<input>`。因为 `<input>` 是一个 [内置组件](https://zh-hans.react.dev/reference/react-dom/components/common)，React 会将 ref 的 `.current` 属性设置为这个 `<input>` DOM 元素。

在 `MyForm` 中创建的 `inputRef` 现在指向 `MyInput` 返回的 `<input>` DOM 元素。在 `MyForm` 中创建的点击处理程序可以访问 `inputRef` 并且调用 `focus()` 来将焦点设置在 `<input>` 上。

## React 何时添加 refs [](https://zh-hans.react.dev/learn/manipulating-the-dom-with-refs#when-react-attaches-the-refs "Link for React 何时添加 refs")

在 React 中，每次更新都分为 [两个阶段](https://zh-hans.react.dev/learn/render-and-commit#step-3-react-commits-changes-to-the-dom)：

- 在 **渲染** 阶段， React 调用你的组件来确定屏幕上应该显示什么。
- 在 **提交** 阶段， React 把变更应用于 DOM。

通常，你 [不希望](https://zh-hans.react.dev/learn/referencing-values-with-refs#best-practices-for-refs) 在渲染期间访问 refs。这也适用于保存 DOM 节点的 refs。在第一次渲染期间，DOM 节点尚未创建，因此 `ref.current` 将为 `null`。在渲染更新的过程中，DOM 节点还没有更新。所以读取它们还为时过早。

React 在提交阶段设置 `ref.current`。在更新 DOM 之前，React 将受影响的 `ref.current` 值设置为 `null`。更新 DOM 后，React 立即将它们设置到相应的 DOM 节点。

**通常，你将从事件处理器访问 refs。** 如果你想使用 ref 执行某些操作，但没有特定的事件可以执行此操作，你可能需要一个 effect。我们将在下一页讨论 effect。

## 使用 refs 操作 DOM 的最佳实践 [](https://zh-hans.react.dev/learn/manipulating-the-dom-with-refs#best-practices-for-dom-manipulation-with-refs "Link for 使用 refs 操作 DOM 的最佳实践")

Refs 是一种脱围机制。你应该只在你必须“跳出 React”时使用它们。这方面的常见示例包括管理焦点、滚动位置或调用 React 未暴露的浏览器 API。

如果你坚持聚焦和滚动等非破坏性操作，应该不会遇到任何问题。但是，如果你尝试手动**修改** DOM，则可能会与 React 所做的更改发生冲突。

**避免更改由 React 管理的 DOM 节点。** 对 React 管理的元素进行修改、添加子元素、从中删除子元素会导致不一致的视觉结果，或与上述类似的崩溃。

但是，这并不意味着你完全不能这样做。它需要谨慎。 **你可以安全地修改 React 没有理由更新的部分 DOM。** 例如，如果某些 `<div>` 在 JSX 中始终为空，React 将没有理由去变动其子列表。 因此，在那里手动增删元素是安全的。

## 用 flushSync 同步更新 state

```js
setTodos([ ...todos, newTodo]);  
listRef.current.lastChild.scrollIntoView();
```

在 React 中，[state 更新是排队进行的](https://zh-hans.react.dev/learn/queueing-a-series-of-state-updates)。通常，这就是你想要的。但是，在这个示例中会导致问题，因为 `setTodos` 不会立即更新 DOM。因此，当你将列表滚动到最后一个元素时，尚未添加待办事项。这就是滚动总是“落后”一项的原因。

要解决此问题，你可以强制 React 同步更新（“刷新”）DOM。 为此，从 `react-dom` 导入 `flushSync` 并**将 state 更新包裹** 到 `flushSync` 调用中：

```js
flushSync(() => {
  setTodos([ ...todos, newTodo]);
});
listRef.current.lastChild.scrollIntoView();
```

这将指示 React 当封装在 `flushSync` 中的代码执行后，立即同步更新 DOM。因此，当你尝试滚动到最后一个待办事项时，它已经在 DOM 中了