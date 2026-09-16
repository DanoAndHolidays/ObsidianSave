# props是普通对象
> Last Format Time：9/16/2026 19:24:51

对，**React 传给组件的 props，本质上就是一个普通的 JavaScript 对象。**

比如：

```jsx
function App() {
  return <User name="Dano" age={20} />;
}
```

你可以近似理解为 React 在调用组件时做了：

```js
User({
  name: "Dano",
  age: 20,
});
```

所以：

```jsx
function User(props) {
  console.log(props);
}
```

这里的 `props` 大概就是：

```js
{
  name: "Dano",
  age: 20
}
```

---
## 但要注意一个很重要的点
**每次组件重新渲染时，函数组件都会重新执行，于是你这一次拿到的是“这次渲染对应的 props 对象”。**

例如：

```jsx
function Child(props) {
  console.log(props);
  return null;
}
```

父组件：

```jsx
function App() {
  const [count, setCount] = useState(0);

  return <Child count={count} />;
}
```

第一次：

```js
props = {
  count: 0
}
```

点击更新后，再次执行 `Child`：

```js
props = {
  count: 1
}
```

你可以把它理解成：

```js
// 第一次渲染
Child({
  count: 0
});

// 第二次渲染
Child({
  count: 1
});
```

这也是理解 **React 闭包问题** 的关键。

比如：

```jsx
function Child(props) {
  const handleClick = () => {
    console.log(props.count);
  };

  // ...
}
```

第一次渲染实际上类似：

```js
const props1 = {
  count: 0
};

const handleClick1 = () => {
  console.log(props1.count);
};
```

第二次渲染：

```js
const props2 = {
  count: 1
};

const handleClick2 = () => {
  console.log(props2.count);
};
```

所以不是同一个 `props` 对象里的 `count` 被修改成了 `1`，而更适合认为：

```text
第一次渲染
props1 -> { count: 0 }
            ↑
       handleClick1 闭包

第二次渲染
props2 -> { count: 1 }
            ↑
       handleClick2 闭包
```

这和你前面问的闭包其实正好连起来了：

> **React 每次渲染都会产生一套新的局部变量，包括新的 props、state 局部值和函数。闭包捕获的是某一次渲染里的那套变量。**

再补一个细节：`props` 虽然是普通对象，但在 React 的编程模型里应该把它当成**只读对象**。

不要这样：

```jsx
function Child(props) {
  props.name = "Tom"; // ❌
}
```

而应该由父组件重新传：

```jsx
<Child name="Tom" />
```

所以一句话记忆：

> **props 本质是普通 JS 对象，但它代表“某一次渲染的输入快照”，组件不应该修改它。**
