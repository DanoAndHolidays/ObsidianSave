# Realm
> Last Format Time：9/16/2026 19:24:51

[https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Execution_model#%E5%9F%9F](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Execution_model#%E5%9F%9F)

在 JavaScript 中，使用 `instanceof Error` 进行跨环境（如跨 iframe、跨 Web Worker 或 Node.js 的 vm 模块）判断时失效，根本原因在于 **JavaScript 的多全局执行环境（Realm）隔离机制**。

---
## 每个 Realm 都有独立的构造函数
在 JavaScript 规范中，每一个独立的全局执行环境（Realm）都拥有自己的一套全局对象和内置构造函数（如 `Array`、`Date`、`Error` 等）。

`instanceof` 运算符的底层工作原理是：**检查左侧对象的原型链（prototype chain）中，是否包含右侧构造函数的 `prototype` 属性**。

当发生跨环境传递时，虽然两个环境中的构造函数名字都叫 `Error`，但它们实际上是**两个完全不同的函数对象**，它们的 `prototype` 属性也互不相等。因此，当你在主窗口中用主窗口的 `Error.prototype` 去匹配 iframe 中创建的 Error 对象的原型链时，自然无法匹配成功，最终返回 `false`。

---
## 具体代码示例
假设我们在一个主页面中嵌入了一个 iframe，并在 iframe 中抛出了一个错误，然后传递给主窗口进行判断：
```javascript
// 1. 在主窗口中创建一个 iframe
const iframe = document.createElement('iframe');
document.body.appendChild(iframe);

// 2. 在 iframe 的执行环境中创建一个 Error 对象
const iframeError = iframe.contentWindow.Error('This error comes from an iframe');

// 3. 在主窗口中进行类型判断
console.log(iframeError instanceof Error);       // 输出: false ❌ (翻车)
console.log(iframeError instanceof iframe.contentWindow.Error); // 输出: true ✅
```

---
## 原理解析
- `iframeError` 的原型链指向的是 `iframe.contentWindow.Error.prototype`。
- 主窗口中的 `Error` 是主窗口的构造函数，其 `prototype` 是 `window.Error.prototype`。
- 因为 `iframe.contentWindow.Error.prototype !== window.Error.prototype`，所以 `instanceof` 沿着原型链查找时找不到匹配项，返回了 `false`。

---
## 更好的替代方案
为了解决这种跨环境的类型检测问题，现代 JavaScript 提供了更可靠的方案：

1. **使用 `Error.isError()`（最新提案/规范）** 这是目前最推荐的跨环境 Error 检测方法，类似于 `Array.isArray()`，它不依赖原型链，而是通过内部机制判断。

```javascript
console.log(Error.isError(iframeError)); // 输出: true ✅ (完美解决)
```

2. **使用 `Object.prototype.toString.call()`** 这是一种经典的、跨环境安全的类型检测方式，通过读取对象内部的标签来判断。

```javascript
console.log(Object.prototype.toString.call(iframeError) === '[object Error]'); // 输出: true ✅
```

总结来说，`instanceof` 并非有 Bug，而是它被设计为严格依赖“当前执行环境的原型链拓扑结构”。在进行跨环境通信时，应当避免使用 `instanceof`，转而使用上述更稳健的类型检测手段。

---
## Realm 的核心组成
每一个 Realm 都拥有自己专属的“基础设施”，互不干扰。根据 ECMAScript 规范，一个 Realm 主要由以下部分组成：
- **全局对象（Global Object）**：例如浏览器环境中的 `window` 或 `globalThis`。
- **内置对象（Intrinsic Objects）**：一套与该全局对象绑定的基础构造函数和原型，如 `Object`、`Array`、`Error`、`Promise` 等。
- **全局词法环境（Global Environment）**：用于解析全局变量和标识符的作用域。
- **执行上下文（Execution Context）**：代码运行时的状态追踪（包括调用栈、`this` 绑定等）。

**关键点在于：** 即使两个 Realm 中的 `Array` 构造器功能完全一样，它们在内存中也是**两个完全不同的函数对象**，拥有各自独立的 `prototype`。

---
## 浏览器中的 Realm 实例
在浏览器环境中，Realm 与全局对象是一一对应的。以下场景都会创建独立的 Realm：
- **主页面（Top Main Realm）**：网页默认运行的 Realm。
- **iframe**：每一个 `<iframe>` 都会创建一个全新的 Realm，即使它与主页面同源。
- **Web Workers**：每个 Worker（包括 Dedicated、Shared、Service Worker）都有自己独立的 Realm。

---
## ShadowRealm API
在过去，开发者只能通过 `iframe` 或 `Web Worker` 来间接获取 Realm，这带来了沉重的 DOM 开销或通信成本。

目前，TC39 正在推进 **ShadowRealm API 提案**（目前处于 Stage 3 阶段）。它允许开发者在 JavaScript 层面直接通过 `new ShadowRealm()` 创建一个轻量级、完全隔离的 Realm，并通过 `evaluate()` 方法安全地执行字符串代码，而无需创建 iframe。这将是未来实现安全沙箱和代码隔离的终极标准方案。