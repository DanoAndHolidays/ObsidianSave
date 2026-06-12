# Vue

### 【Q011】vue3.0 中为什么要使用 Proxy，它相比以前的实现方式有什么改进
- **Vue2（Object.defineProperty）**：
  - 需要递归遍历所有属性添加 getter/setter
  - 无法监听新增/删除属性（需要 Vue.set/Vue.delete）
  - 不能监听数组索引赋值和 length 修改，需要重写数组方法
- **Vue3（Proxy）**：
  - Proxy 代理整个对象，不需要递归遍历
  - 天然支持属性新增/删除
  - 天然支持数组索引操作
  - 惰性响应（只在访问深层对象时递归代理，无需初始化遍历全部属性）
  - 性能更好

### 【Q089】vue 中 v-if 和 v-show 的区别是什么
- **v-if**：真正的条件渲染，false 时**完全不渲染** DOM 元素（DOM 节点不存在）。切换开销大（重建/销毁），适合运行时条件很少变化的场景。
- **v-show**：总是渲染 DOM 元素，只是切换 `display: none`。切换开销小，适合频繁切换的场景。

### 【Q090】vue 中 computed 的原理是什么
computed 基于**惰性求值**和**依赖收集**：
1. 创建 computed 时内部为每一个计算属性创建一个 Watcher（或 Vue3 中的 effect）
2. 计算属性的 getter 被调用时，将当前 Watcher 收集到该计算依赖的响应式数据的 Dep 中
3. 依赖数据变化时通知计算属性的 Watcher 标记为脏（dirty = true）
4. 再次访问计算属性时，如果是脏数据则重新计算，否则返回缓存值

### 【Q091】vue-loader 的实现原理是什么
Vue Loader 是一个 Webpack Loader：
1. 解析 .vue 单文件组件的 `<template>`、`<script>`、`<style>` 块
2. 对每个块应用不同的 loader：template→vue-template-compiler（编译成 render 函数）、script→babel/ts-loader、style→css-loader+postcss-loader
3. 将编译后的内容组合成一个 ES module，导出 Vue 组件选项对象
4. 支持 scoped CSS（通过 data-xxx 属性 + 属性选择器实现样式隔离）

### 【Q450】Vue 中 nextTick 的实现原理是什么
Vue 的 DOM 更新是**异步**的。nextTick 将回调放入微任务队列（优先 Promise.then，降级使用 MutationObserver → setImmediate → setTimeout），在当前 DOM 更新周期结束后执行。利用 JS 事件循环：宏任务 → 清空微任务的所有回调就是 nextTick 的执行时机。

```javascript
// Vue3 中用 Promise 实现微任务
const resolvedPromise = Promise.resolve();
function nextTick(fn) { return fn ? resolvedPromise.then(fn) : resolvedPromise; }
```

