# React 组件卸载与 this引用
> Last Format Time：6/15/2026 11:46:35

---
## 题目
在 React 类组件中，有如下代码：
```jsx
class Demo extends React.Component {
  componentDidMount() {
    setTimeout(() => {
      console.log(this);
    }, 10000);
  }

  render() {
    return <div>Demo Component</div>;
  }
}
```

该组件挂载后，在第 5 秒时通过父组件将其卸载（从 DOM 中移除）。  
**请问：10 秒后定时器触发时，控制台打印的 `this` 是什么？为什么？**

---
## 解析分析
### 答案
打印的是**该组件实例对象本身**（即 `Demo` 组件的实例），而不会变成 `null`、`undefined`，也不会抛出异常。

### 原因详解
1. **闭包与强引用导致实例无法被回收**  
   `componentDidMount` 中使用的箭头函数没有自己的 `this`，它会捕获外层作用域的 `this`，也就是当前组件实例。这个箭头函数作为回调传递给 `setTimeout`，被定时器内部持续持有。  
   只要定时器还未触发且未被清除，这个回调函数就始终存在，而它又通过闭包强引用了组件实例。因此即使组件在第 5 秒被卸载，该实例对象**依然被定时器回调引用**，无法被垃圾回收器回收，它依然完完整整地存在于内存中。

2. **React 卸载 ≠ 销毁 JavaScript 对象**  
   React 卸载组件时，会做三件事：  
   - 将该组件对应的 DOM 节点从页面中移除；  
   - 调用 `componentWillUnmount` 生命周期方法；  
   - 清除 React 内部对组件实例的某些关联（如 fiber 节点的引用）。  
   但它**不会**将 `this` 置为 `null`，也不会调用某种“析构函数”去销毁对象。JavaScript 没有析构机制，一个对象只要还被引用，它就是“活”的。本例中组件实例被定时器回调引用，所以它依然存活，只是不再作为 React 渲染树的一部分活动。

3. **打印出的 `this` 依然完整，但已“失活”**  
   打印出的 `this` 就是原先那个组件实例，你能看到它上面的 `props`、`state`、`refs` 等属性。  
   但此时它已经脱离 React 的管理，如果你在定时器里试图调用 `this.setState()`，React 会抛出警告：*Can't perform a React state update on an unmounted component*，并且更新不会生效。

### 核心结论
定时器回调通过闭包始终持有组件实例的引用，导致实例在卸载后无法被回收。定时器触发时，`this` 仍指向那个实例对象，但该对象已不再挂载，属于”僵尸组件”。

### 编码警示
这类不清理的定时器会造成典型的内存泄漏。正确做法是在 `componentWillUnmount` 中清除定时器，从而断开对实例的引用：
```jsx
componentDidMount() {
  this.timer = setTimeout(() => {
    console.log(this);
  }, 10000);
}

componentWillUnmount() {
  clearTimeout(this.timer);
}
```