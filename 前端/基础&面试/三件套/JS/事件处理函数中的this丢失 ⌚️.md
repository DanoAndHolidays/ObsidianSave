# 事件处理函数中的this丢失 ⌚️
> Last Format Time：9/16/2026 19:24:51

![[Pasted image 20260903161139.png]]

对，你选 **B 是对的**，原因就是你说的：**`this` 丢失了，准确说是普通函数作为回调传给 `setTimeout` 后，不再保持 `onclick` 中的 `this`。**

先抓住最关键的一层：

```js
btn.onclick = function () {
  console.log(this === btn) // true
}
```

这里浏览器是以“按钮的事件处理函数”方式调用它，所以：

```js
this === btn
```

但是 B：

```js
btn.onclick = function () {
  setTimeout(function () {
    this.disabled = true
  }, 1000)
}
```

可以把它理解成：`function () { ... }` 被单独拿出来，**1 秒后由定时器调用**：

```js
function callback() {
  this.disabled = true
}

setTimeout(callback, 1000)
```

这时候它已经不是：

```js
btn.callback()
```

所以里面的 `this` **不是 btn**，自然不能正确禁用按钮。


其他三个为什么可以：

```js
// A
btn.onclick = function () {
  setTimeout(() => {
    this.disabled = true
  }, 1000)
}
```

箭头函数**没有自己的 `this`**，会沿词法作用域向外找，因此拿到外层 `onclick` 的：

```text
onclick 普通函数
this = btn
   │
   ↓ 继承
箭头函数
this = btn
```

所以 A ✅。

C 是你之前学过的经典写法：

```js
btn.onclick = function () {
  var that = this

  setTimeout(function () {
    that.disabled = true
  }, 1000)
}
```

虽然定时器里的普通函数自己的 `this` 不对，但：

```js
that === btn
```

这是通过**闭包（closure，闭包）**保存了外层变量，所以 C ✅。

D：

```js
btn.onclick = function () {
  setTimeout(
    function () {
      this.disabled = true
    }.bind(this),
    1000
  )
}
```

执行 `bind(this)` 的这一刻，外层：

```js
this === btn
```

因此相当于把回调永久绑定成：

```js
this === btn
```

所以 D ✅。

你可以把这题直接记成：

> **事件处理普通函数中的 `this` 指向触发事件的元素；但把另一个普通函数作为 `setTimeout` 回调传出去后，它不会自动继承外层的 `this`。**

解决 `this` 丢失的三个经典方案正好就是这题的 A/C/D：

```js
// 1. 箭头函数：继承外层 this
() => this.xxx

// 2. 闭包保存 this
const that = this

// 3. bind 显式绑定
function () {}.bind(this)
```

所以这道题答案就是 **B**。你说的「因为 `this` 可能丢了」方向完全正确，更精确地说是：**普通函数的 `this` 取决于调用方式，`setTimeout` 调用回调时并不是以 `btn` 作为调用者。**
