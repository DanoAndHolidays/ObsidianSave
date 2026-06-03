# HMR
Webpack 的热更新（Hot Module Replacement，简称 HMR）让你在开发时修改代码，浏览器能**立即看到效果，且不刷新页面、不丢失状态**（比如 React 组件的 state 或输入框的内容）。它的核心是：**在运行时动态替换、添加或删除模块，无需完整刷新**。

下面分步骤解释 Webpack HMR 的原理。

---

## 1. 整体架构

HMR 需要三个角色的配合：
- **Webpack 编译器**（服务端）：监听文件变化，重新编译发生变化的模块。
- **HMR Server**（一般集成在 webpack-dev-server 中）：负责将编译后的更新推送给客户端。
- **HMR Runtime**（客户端）：在浏览器中运行，接收更新，并执行模块的热替换逻辑。

---

## 2. 工作流程

### ① 启动阶段
- 启动 `webpack-dev-server`（或配合 `webpack-dev-middleware` + 后端服务）。
- Webpack 会向构建好的 `bundle.js` 中注入 HMR Runtime 代码，并通过 WebSocket 与服务器建立持久连接。

### ② 文件修改
你修改了某个源文件（比如 `Component.jsx`）并保存。

### ③ 重新编译（增量）
- Webpack 检测到文件变动，从入口开始重新构建**变更的模块及其依赖**（不是全量构建）。
- 构建完成后，生成一个 **更新清单（manifest，包含更新的 chunk id 和 hash）** 以及一个或多个 **更新补丁（update chunk，包含新的模块代码）**。

### ④ 通知客户端
HMR Server 通过 WebSocket 将 `hash` 和 `ok` 事件发送给客户端，告诉它：“有新版本可用”。

### ⑤ 客户端请求更新
HMR Runtime 收到通知后，会向服务器发起 HTTP 请求，获取 `[hash].hot-update.json`（更新清单）和对应的 `[chunkId].[hash].hot-update.js`（新的模块代码）。

### ⑥ 模块热替换
- HMR Runtime 拿到新模块代码后，会用新的模块替换旧的模块。
- 替换后，会递归地向上冒泡，调用模块或其父模块的 `module.hot.accept` 回调，让开发者有机会**重新执行模块的逻辑**（比如重新渲染 React 组件，或重新绑定事件）。
- 如果没有任何模块接受该更新，HMR 会降级为刷新整个页面。

---

## 3. 关键细节：`accept` 与 `dispose`

为了让 HMR 能够无状态地替换模块，Webpack 提供了两个钩子（Hook）：

### `module.hot.accept(dependencies, callback)`
- 声明当前模块接受哪些依赖模块的更新。
- 当这些依赖被替换时，会执行 `callback`，用来**重新执行模块代码，让新逻辑生效**。

```javascript
// 示例：React 组件热更新
if (module.hot) {
  module.hot.accept('./MyComponent', () => {
    // 重新渲染 MyComponent
    const NewComponent = require('./MyComponent').default;
    ReactDOM.render(<NewComponent />, document.getElementById('root'));
  });
}
```

### `module.hot.dispose(callback)`
- 在旧模块被移除前执行，用于清理副作用（如清除定时器、取消事件订阅、保存状态等），避免内存泄漏。

---

## 4. 为什么能不刷新页面？

传统刷新会销毁所有 JavaScript 运行环境，HMR 则**只替换模块函数**。模块内部的局部变量（比如 React 组件 `state`）能否保留，取决于开发者的实现：
- **React Fast Refresh**（取代之前的 react-hot-loader）能智能合并 state，做到“无刷新保留组件状态”。
- 如果手动写 `accept` 回调完全重新渲染组件，状态可能会丢失；但可以先把旧组件的状态提取出来，传给新组件。

---

## 5. HMR 的局限性

- **仅适用于开发环境**：生产环境会禁用 HMR，因为热替换需要额外的运行时和冗余代码。
- **不是所有模块都能热替换**：比如修改 `webpack.config.js` 本身，或者修改了 Vuex 的 store 结构，可能需要手动处理。
- **依赖模块的接受链**：如果某个模块没有声明 `accept`，更新会冒泡到它的父模块，直到被某个 `accept` 处理，否则触发页面刷新。

---

## 6. 简化版时序图

```
开发者修改文件
    ↓
Webpack 编译变更模块 → 生成 hot-update 文件
    ↓
HMR Server 通过 WebSocket 推送 `hash`
    ↓
浏览器端 HMR Runtime 请求 hot-update.json 和 .js
    ↓
HMR Runtime 用新模块替换旧模块
    ↓
调用 accept 回调 → 应用新逻辑，保留页面状态
```

---

## 总结

Webpack HMR 的本质是：**基于文件监听 + 增量编译 + WebSocket 通知 + 运行时模块替换**。它让你在开发时获得接近“即时反馈”的体验，同时保持应用状态。掌握这些原理，不仅能更好理解 webpack-dev-server 的配置（比如 `hot: true`），也能帮你解决热更新失效的问题（比如检查是否正确使用了 `accept` 或使用了支持 HMR 的框架封装）。