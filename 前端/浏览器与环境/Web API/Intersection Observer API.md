交叉观察器 API 允许你配置一个回调函数，当以下情况发生时会被调用：
- **目标**元素与设备视口或指定元素相交。在交叉观察器 API 中，指定元素被称为**根元素**或**根**。
- 观察器（Observer）第一次监听观察目标元素。

通常情况下，需要观察目标元素最近的可滚动祖先的交集变化，如果目标元素不是可滚动元素的后代，则需要观察设备视口的交集变化。要观察相对于设备视口的交集，请为 `root` 选项指定 `null`。请继续阅读有关交叉观察器选项的更详细说明。

无论你是使用视口还是其他元素作为根元素，API 的工作方式都是一样的，只要目标元素的可见性发生变化，与根元素的交集达到所需的程度，就会执行你提供的回调函数。

目标元素与其根元素的交集程度就是**交叉比**。它表示目标元素可见的百分比，数值介于 0.0 和 1.0 之间。

```javascript
let options = {
  root: document.querySelector("#scrollArea"),
  rootMargin: "0px",
  threshold: 1.0,
};

let observer = new IntersectionObserver(callback, options);

let target = document.querySelector("#listItem");
observer.observe(target);

// 我们为观察器设置的回调将在第一次执行，
// 它将等待我们为观察器分配目标（即使目标当前不可见）
```