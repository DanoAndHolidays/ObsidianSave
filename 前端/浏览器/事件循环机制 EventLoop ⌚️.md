# 事件循环机制 EventLoop ⌚️
> Last Format Time：9/16/2026 19:24:53

> Last Format Time：2026-09-03

---
## 浏览器进程架构
[[浏览器工作原理 ⌚️]]

---
## 一、先纠正几个常见说法
### JavaScript 不是“只能单线程”
更准确的说法是：

- **同一个 JavaScript 执行上下文（agent）中的代码通常遵循 run-to-completion**：一段正在执行的 JavaScript 不会被另一段 JavaScript 插入执行；
- 浏览器的**主线程**通常同时负责页面 JavaScript、DOM、样式计算、布局、绘制、用户交互等工作，因此主线程上的长任务会阻塞页面；
- JavaScript 可以通过 `Web Worker`、`SharedWorker`、`Service Worker`、`Worklet` 等机制在其他执行上下文中运行。它们不能直接操作主页面 DOM，通常通过消息通信；
- 所以，“JavaScript 只能是单线程的”不准确；应理解为：**一个执行上下文内的 JavaScript 按顺序执行，浏览器可以存在多个执行上下文和线程**。

单线程模型的价值不是因为“用户交互必然要求单线程”，而是因为它让同一个执行上下文中的状态变化具有可预测的顺序，避免了多个 JavaScript 执行流同时修改同一 DOM 状态所带来的同步问题。

### 异步不等于“把所有工作交给其他线程”
浏览器会把网络、计时器、用户输入等能力交给宿主环境处理；宿主环境可能使用操作系统能力、线程池、内核事件通知或其他实现方式。JavaScript 代码本身只需要在合适的时候处理宿主环境安排的回调。

因此更准确的流程是：

```text
调用 Web API / 宿主 API
        ↓
宿主环境等待条件满足
        ↓
将回调作为 task，或将 Promise reaction 作为 microtask
        ↓
事件循环在合适的时机执行
```

---
## 二、事件循环的核心模型
![[Pasted image 20250830154310.png]]

### 执行栈（Call Stack）
同步代码按调用关系进入执行栈。当前栈帧执行结束后出栈；只有当前 JavaScript 执行结束、调用栈清空后，宿主环境才有机会继续处理下一步。

### Task 与 Microtask
规范使用的术语主要是 **task** 和 **microtask**。中文资料常把 task 叫作“宏任务（macrotask）”，这个词便于面试交流，但并不是 HTML 标准中的正式分类。

##### 常见 task
- 初始脚本、模块脚本的执行；
- 用户代理异步派发的用户交互事件；
- `setTimeout` / `setInterval` 到期后的回调；
- `MessageChannel`、`postMessage` 等消息回调；
- `XMLHttpRequest` 的 `load`、`error` 等事件回调；
- 其他由宿主环境安排的任务。

##### 常见 microtask
- `Promise.then/catch/finally` 注册的 reaction；
- `queueMicrotask()`；
- `MutationObserver` 回调；
- `async` 函数中每个 `await` 之后的 continuation（后续执行）。

`fetch()` 返回的是 Promise：网络完成由宿主环境处理，而开发者通过 `fetch(...).then(...)` 观察到的 `.then` 回调属于 microtask。不能笼统地把“AJAX”作为一种队列类型。

### 一次典型的浏览器事件循环迭代
可以用下面的心智模型理解浏览器主线程：

```text
取出一个可运行的 task
        ↓
执行 task 中的 JavaScript（直到调用栈清空）
        ↓
执行 microtask checkpoint：持续清空 microtask 队列
        ↓
浏览器在合适的时机更新渲染、执行动画帧回调
        ↓
进入下一轮，选择下一个可运行的 task
```

注意：

- 不是“所有宏任务排成一个严格的全局 FIFO 队列”；HTML 标准允许不同 task source 使用不同队列，用户代理可以根据情况选择下一个可运行任务；
- 浏览器没有一个由规范固定的“交互队列 > 定时器队列 > 网络队列”的统一优先级表。浏览器可能会进行调度优化，但不能把某个浏览器的实现策略当成 Web 标准保证；
- microtask checkpoint 会持续执行到队列为空。microtask 中新加入的 microtask 会在下一个 task 之前继续执行；
- 如果 microtask 不断产生新的 microtask，可能造成 microtask 饥饿，使后续 task、用户交互和渲染迟迟得不到机会。

### `requestAnimationFrame` 不应简单归为宏任务
`requestAnimationFrame()` 是“请求浏览器在下一次合适的绘制前调用回调”的渲染相关 API。它不是普通的 `setTimeout`，也不应直接塞进“宏任务队列”这一栏。更适合把它理解为：

```text
下一次更新渲染时机到来
        ↓
执行 requestAnimationFrame 回调
        ↓
浏览器继续渲染 / 绘制
```

具体的渲染时机受页面可见性、显示器刷新率、浏览器调度和页面性能影响，不能假定它固定为每秒 60 次。

---
## 三、不要把“同步、微任务、宏任务”理解成固定的三条优先级队列
面试题中常用下面的简化模型：

```text
当前 task 中的同步代码
        ↓
microtask checkpoint（清空微任务）
        ↓
后续 task（例如 setTimeout）
```

它对大多数基础题有帮助，但它不是完整的浏览器调度规范。尤其要避免以下错误结论：

- “W3C 规定交互队列一定比定时器队列优先”；
- “所有网络回调都有一个统一的 AJAX 队列”；
- “`requestAnimationFrame` 就是宏任务”；
- “微任务优先级高，所以它不会阻塞渲染”。

微任务虽然通常会在下一 task 前被清空，但**清空微任务本身也会占用主线程**。大量或递归 microtask 同样会阻塞渲染。

---
## 四、定时器并不精确
`setTimeout(fn, delay)` 的 `delay` 不是“保证在 delay 毫秒后执行”，而是一个最小等待意图。回调至少要等到：

1. 计时器条件满足；
2. 回调被宿主环境安排为可运行 task；
3. 事件循环选中该 task；
4. 主线程没有被前面的长任务占用。

因此下面的代码中，`setTimeout` 不会打断当前同步代码：

```js
setTimeout(() => console.log('timer'), 0)

const start = performance.now()
while (performance.now() - start < 100) {
  // 阻塞主线程约 100ms
}

console.log('sync end')
```

通常会先输出 `sync end`，之后才有机会输出 `timer`。

### 嵌套计时器的 4ms 限制
HTML Standard 规定：当计时器嵌套层级超过 5，且请求的延迟小于 4ms 时，延迟会被设置为至少 4ms。通俗地说，连续嵌套的第 6 层及之后，不能依赖 0ms 定时器持续高速执行。

这只是规范中的一个限制。浏览器还可能因为后台标签页、页面不可见、系统资源、节流策略等原因进一步延迟定时器。因此不要使用 `setTimeout` 作为精确计时器；需要动画同步时优先考虑 `requestAnimationFrame`，需要高精度业务调度时应使用时间戳校正实际经过的时间。

---
## 五、长任务与渲染阻塞
页面主线程还要处理输入、样式、布局和绘制。一个 task 执行太久，会导致：

- 用户输入响应变慢；
- 页面无法及时绘制；
- 动画掉帧；
- 其他 task 和 microtask 延迟执行。

通常把主线程上持续超过 50ms 的任务称为 **Long Task**。优化方向：

### 拆分长任务
```js
function processInChunks(data) {
  const chunk = data.splice(0, 100)
  processChunk(chunk)

  if (data.length > 0) {
    // 让出主线程，再继续处理
    setTimeout(() => processInChunks(data), 0)
  }
}
```

`setTimeout` 只是示例。实际项目也可以根据目标选择 `MessageChannel`、`scheduler.postTask`（需考虑兼容性）或 `requestIdleCallback`。拆分的关键是**定期让出主线程**，而不是机械地认为 0ms 一定立即执行。

### 使用 Web Worker
```js
// 主线程
const worker = new Worker('task.js')
worker.postMessage(data)
worker.onmessage = (event) => {
  // 处理结果
}

// task.js
self.onmessage = (event) => {
  const result = heavyComputation(event.data)
  self.postMessage(result)
}
```

Worker 适合计算密集型工作，但不能直接访问主页面 DOM；主线程与 Worker 之间通常通过 `postMessage` 传输数据。

### 监控 Long Task
```js
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.warn('Long Task:', entry.duration, entry)
  }
})

observer.observe({ entryTypes: ['longtask'] })
```

`longtask` 条目通常用于监控主线程长任务。实际使用时仍应结合浏览器兼容性和业务监控方案。

---
## 六、Promise 的 executor 是同步执行的
```js
new Promise((resolve) => {
  console.log('promise1')
  resolve()
}).then(() => {
  console.log('promise2')
})
```

输出顺序：

```text
promise1    // 同步
promise2    // microtask
```

原因：

- `new Promise()` 创建 Promise 时，会立即同步调用 executor；
- `.then()` 注册的回调不会在当前同步代码中立即执行，而是在 Promise settled 后排入 Promise reaction job，浏览器中通常表现为 microtask；
- `resolve()` 只负责改变 Promise 的状态，不会同步调用 `.then()` 回调。

因此不能认为“Promise 里面的代码都是异步的”。executor 里的代码是同步的，`.then/catch/finally` 回调才是异步衔接点。

---
## 七、`async` 函数与 `await`
### `async` 函数调用时，首次 `await` 之前的代码可以同步执行
```js
async function fn() {
  console.log('A')
}

fn()
console.log('B')
```

输出：

```text
A
B
```

`async` 函数总是返回 Promise，但这不代表函数体从第一行开始就异步执行。没有 `await` 时，函数体可以完整同步执行，然后以 Promise 形式返回结果。

### `await` 会暂停当前 async 函数
```js
async function async1() {
  console.log('async1 start')

  await async2()

  console.log('async1 end')
}

async function async2() {
  console.log('async2')
}
```

执行 `await async2()` 时可以这样理解：

1. 先同步求值 `async2()`，所以 `async2` 函数中 `await` 之前的代码会立即执行；
2. `await` 会把返回值转换为 Promise，并暂停 `async1`；
3. Promise settle 后，`await` 后的 continuation 会在后续 microtask 中恢复执行。

下面的 `.then` 只是建立心智模型，并不表示引擎把源码简单改写成这一段：

```js
Promise.resolve(async2()).then(() => {
  console.log('async1 end')
})
```

即使等待的是普通值，`await` 后的代码也会在异步 continuation 中执行，而不会继续留在当前同步调用栈中。

### async 函数总是返回 Promise
```js
async function async2() {
  console.log('async2')
}

const result = async2()
// result 是 Promise，最终 fulfilled 的值是 undefined
```

可以把它理解为“函数同步执行到返回点，并把结果包装成 Promise”，但不要把 `async2()` 与 `Promise.resolve(undefined)` 当成同一个 Promise 对象；重点是它们的最终完成值相近，而对象身份并不相同。

---
## 八、微任务的顺序
### 同一个 microtask queue 按入队顺序处理
在同一个事件循环和同一个 microtask checkpoint 中，已排队的 microtask 通常按 FIFO 顺序执行：

```js
console.log('script start')

queueMicrotask(() => console.log('microtask 1'))
Promise.resolve().then(() => console.log('microtask 2'))

console.log('script end')
```

输出：

```text
script start
script end
microtask 1
microtask 2
```

需要注意，真正决定顺序的是“何时入队”，不是代码看起来属于哪一种 API。`await` 的 continuation、Promise reaction 和 `queueMicrotask` 可能交错入队。

### microtask 中产生的新 microtask 会追加到队尾
```js
queueMicrotask(() => {
  console.log('microtask 1')
  queueMicrotask(() => console.log('microtask 3'))
})

queueMicrotask(() => console.log('microtask 2'))
```

输出：

```text
microtask 1
microtask 2
microtask 3
```

事件循环会继续处理 microtask，直到队列清空，因此新 microtask 会在下一个 task 之前执行。

---
## 九、综合示例：`async`、Promise 与 `setTimeout`
```js
async function async1() {
  console.log('async1 start')

  await async2()

  console.log('async1 end')

  Promise.resolve().then(() => {
    console.log('after async1 end')
  })
}

async function async2() {
  console.log('async2')
}

console.log('script start')

setTimeout(() => console.log('setTimeout'), 0)

async1()

new Promise((resolve) => {
  console.log('promise1')
  resolve()
}).then(() => {
  console.log('promise2')
})

console.log('script end')
```

在浏览器和 Node.js 的常见实现中，输出为：

```text
script start
async1 start
async2
promise1
script end
async1 end
promise2
after async1 end
setTimeout
```

### 分析
同步阶段先输出：

```text
script start
async1 start
async2
promise1
script end
```

此时可以认为：

- `await async2()` 已经同步调用了 `async2()`；
- `async1` 在 `await` 处暂停，等待 continuation；
- `promise2` 的 Promise reaction 已经排队；
- `setTimeout` 已经注册，但它的回调属于后续 task。

微任务阶段：

1. `async1 end` 先恢复执行；
2. 执行 `async1 end` 时，又把 `after async1 end` 的 Promise reaction 加入队尾；
3. 接着执行原先已经排队的 `promise2`；
4. 最后执行新加入的 `after async1 end`。

微任务清空后，才有机会执行 `setTimeout` 对应的 task。

---
## 十、做执行顺序题的可靠步骤
```text
① 明确运行环境：浏览器还是 Node.js

② 从上到下执行当前 task 中的同步代码
   - 普通函数调用：同步
   - Promise executor：同步
   - async 函数首次 await 之前：通常同步

③ 记录入队顺序
   - Promise.then/catch/finally：microtask
   - queueMicrotask：microtask
   - await 后续：microtask continuation
   - setTimeout/setInterval：后续 task

④ 当前 task 结束后，清空 microtask queue
   - 新产生的 microtask 继续追加到队尾
   - 直到队列为空

⑤ 再考虑后续 task、渲染时机和 requestAnimationFrame

⑥ 如果题目涉及 process.nextTick、I/O、close、setImmediate，切换到 Node.js 的事件循环模型，不能直接套浏览器口诀
```

一句话记忆：

> **当前 task 的同步代码先执行；Promise reaction、`queueMicrotask` 和 `await` 后续进入 microtask；microtask 清空后，才会处理后续 task。`requestAnimationFrame` 属于渲染时机，不能简单等同于宏任务。**

---
## 十一、浏览器与 Node.js 的边界
- `process.nextTick` 是 Node.js API，浏览器没有它；
- Node.js 还会区分 `process.nextTick` 队列、Promise microtask，以及 timers、poll、check 等事件循环阶段；
- 在 Node.js 中，`process.nextTick` 往往会在 Promise microtask 之前处理，因此不能把 Node.js 的所有顺序题直接套用浏览器模型；
- 本笔记前面的模型主要用于解释**浏览器主线程**和 Web API。

---
## 参考资料
- [HTML Standard：Event loops](https://html.spec.whatwg.org/multipage/webappapis.html#event-loops)
- [HTML Standard：Timers](https://html.spec.whatwg.org/multipage/timers-and-user-prompts.html#timers)
- [MDN：Using microtasks in JavaScript with queueMicrotask()](https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API/Microtask_guide)
- [MDN：In depth: Microtasks and the JavaScript runtime environment](https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API/Microtask_guide/In_depth)
- [MDN：async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)
- [Node.js：The Node.js Event Loop](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick)

---
## 个人练习记录（以下内容仅作题目记录，不作为规范结论）
![[Pasted image 20250830155930.png]]

执行顺序：（我猜 321 312）

我去，第一次对了，我改什么...

正确答案：321

![[Pasted image 20250830160213.png]]

我的：11,14,12,15,13，答案正确

![[Pasted image 20250830160817.png]]

答案：2,3,6,p2,p1,1,4,5

![[Pasted image 20250830161443.png]]

原记录答案：script start，async1 start，async2，async1 end，setTimeout

```js
setTimeout(() => console.log(0))

new Promise((resolve) => {
  console.log(1)
  resolve(2)
  console.log(3)
}).then((o) => console.log(o))

new Promise((resolve) => {
  console.log(4)
  resolve(5)
})
  .then((o) => console.log(o))
  .then(() => console.log(6))
```

正确输出：

```text
1
3
4
2
5
6
0
```
