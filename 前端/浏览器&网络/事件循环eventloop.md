# 事件循环eventloop
## 1 浏览器进程架构
[[浏览器工作原理]]
## 2 事件循环
### 单线程
由于用户交互的特性，js==只能是单线程的==，但这产生了一些问题，我们必须等待
- 原因：避免 DOM 冲突（比如一个线程修改 DOM，另一个线程删除 DOM，会导致页面混乱）；
- 问题：单线程如果遇到耗时操作（如网络请求、定时器），会阻塞后续代码执行（页面卡住）；
- 解决方案：**异步任务 + 事件循环**（将耗时操作交给其他线程处理，主线程继续执行同步代码，后续再回调）。

### 原理

![[Pasted image 20250830154310.png]]

1. **执行栈（Call Stack）**：同步代码按顺序进入执行栈，执行完后出栈；
2. **异步任务分类**：
   - 微任务（Microtasks）：优先级高，执行栈空后立即执行所有微任务（队列清空才会执行宏任务）
     - 常见：`Promise.then/catch/finally`、`queueMicrotask()`、`process.nextTick`（Node 特有）
   - 宏任务（Macrotasks）：优先级低，微任务执行完后执行1个宏任务（然后回到微任务检查）
     - 常见：`setTimeout/setInterval`、DOM 事件（如 click）、AJAX 请求、`requestAnimationFrame`
3. **循环逻辑**：
   - 执行所有同步代码 → 执行栈空 → 执行所有微任务 → 取1个宏任务执行 → 执行栈空 → 重复上述步骤

这个过程就是**事件循环eventloop**

展开来说：渲染主线程会不断的检查任务队列中的任务，任务存在就取出一个，执行。没有任务就休眠，直到有新的任务进入队列。

这里的==宿主环境==也就是其他的线程，比如计时器任务会==调用OS中的接口==。当宿主环境的任务的执行时机到了（比如计时器时间到了，就会将回调函数包装为任务，加入对应的队列尾部。

### 微任务优先级更高
为什么微任务优先级更高？

- 微任务通常是"同步操作的后续回调"（如 Promise 执行完后的 `then`），需要尽快执行，避免数据状态不一致；
- 例如：如果微任务和宏任务优先级相同，`Promise.then` 的回调可能会被 `setTimeout` 回调阻塞，导致依赖 Promise 结果的代码出错。

### 定时准确性
js中的定时器必然不是精确的：
- 浏览器使用的宿主环境（OS的接口所提供的时间，本身就是不精确的
- setTimeout函数在5个嵌套时，每个setTimeout至少有4ms的延迟
- 宿主环境将任务加入计时队列后，若有其他优先级更高的队列不为空，也不会立刻执行
不过这些误差并不会极大地影响用户的使用体验

### 宏任务与微任务（已过时
- 同步任务：立即执行的代码（如 `let a = 1`、`fn()`），直接进入「调用栈」执行；
- 异步任务：不立即执行的代码（如 `setTimeout`、`Promise.then`、AJAX），分为两类：
  - 宏任务（MacroTask）：由浏览器/宿主环境触发（如 `script` 整体、`setTimeout`、`setInterval`、DOM 事件、AJAX 回调、`requestAnimationFrame`）；
  - 微任务（MicroTask）：由 JS 引擎自身触发（如 `Promise.then/catch/finally`、`MutationObserver`、`queueMicrotask`）；
- 任务队列：存储异步任务的回调函数，分为「宏任务队列」（多个）和「微任务队列」（一个）。


| 对比维度         | 宏任务（MacroTask）                              | 微任务（MicroTask）                              |
|------------------|--------------------------------------------------|--------------------------------------------------|
| 触发主体         | 浏览器/宿主环境（如 Chrome、Node）                | JS 引擎自身（如 V8）                              |
| 执行优先级       | 低（每个宏任务执行后，必须先清空微任务）          | 高（同步代码执行完后，立即清空所有微任务）        |
| 队列数量         | 多个（如定时器队列、DOM 事件队列、AJAX 队列）     | 一个（所有微任务共用一个队列，按顺序执行）        |
| 常见类型         | `script`、`setTimeout`、`setInterval`、DOM 事件、AJAX、`requestAnimationFrame` | `Promise.then/catch/finally`、`MutationObserver`、`queueMicrotask` |
| 设计目的         | 处理"耗时较长"或"需要宿主支持"的异步操作（如网络请求、定时器） | 处理"短耗时"的异步回调（如 Promise 状态变更），保证数据一致性（避免多次渲染） |


执行顺序：同步、微任务、宏任务
![[Pasted image 20250830155048.png]]
这种说法已经过时
W3C的说法是：
- 微队列    ：最高优先级
- 交互队列：高优先级
- 延时队列：中优先级
至少包含这三种Message队列

### 任务队列优先级
[修正说明]：浏览器任务队列按优先级排序

| 队列类型 | 优先级 | 包含任务 | 执行时机 |
|---------|--------|----------|----------|
| **微任务队列** | 最高 | Promise回调、MutationObserver | 每个宏任务结束后立即执行 |
| **交互队列** | 高 | 用户交互事件（点击、输入等） | 优先于其他宏任务 |
| **延迟队列** | 中 | setTimeout、setInterval | 定时到达后执行 |
| **普通队列** | 低 | 网络请求、I/O操作 | 按到达顺序执行 |

### 渲染阻塞与优化策略
[补充说明]：
1. **长任务拆分**：将耗时任务分解为小任务
```javascript
// 不好的做法：长任务阻塞渲染
function processLargeData() {
    // 耗时操作...
}

// 好的做法：任务拆分
function processInChunks() {
    const chunk = data.splice(0, 100);
    processChunk(chunk);
    
    if (data.length > 0) {
        // 使用setTimeout或requestIdleCallback让出主线程
        setTimeout(processInChunks, 0);
    }
}
```

2. **使用Web Workers**：将计算密集型任务移出主线程
```javascript
// 主线程
const worker = new Worker('task.js');
worker.postMessage(data);
worker.onmessage = function(event) {
    // 处理结果
};

// Worker线程（task.js）
self.onmessage = function(event) {
    const result = heavyComputation(event.data);
    self.postMessage(result);
};
```
### 性能监控实践
[补充说明]：监控长任务和渲染性能
```javascript
// 监控长任务（超过50ms的任务）
const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
        if (entry.duration > 50) {
            console.warn('长任务 detected:', entry);
        }
    }
});
observer.observe({entryTypes: ['longtask']});

// 监控帧率
let frameCount = 0;
let lastTime = performance.now();
function checkFPS() {
    frameCount++;
    const currentTime = performance.now();
    if (currentTime - lastTime >= 1000) {
        const fps = Math.round((frameCount * 1000) / (currentTime - lastTime));
        console.log('当前FPS:', fps);
        frameCount = 0;
        lastTime = currentTime;
    }
    requestAnimationFrame(checkFPS);
}
checkFPS();
```
### 面试题
![[Pasted image 20250830155930.png]]
执行顺序：（我猜 321 312
我去，第一次对了，我改什么...

正确答案：321

![[Pasted image 20250830160213.png]]
我的：11,14,12,15,13答案正确

![[Pasted image 20250830160817.png]]
答案2,3,6,p2,p1,1,4,5

![[Pasted image 20250830161443.png]]
 答案：script start，async1 start，async2 ，async1 end，setTimeout

```javascript
setTimeout(() => console.log(0));
new Promise((resolve) => {
  console.log(1);
  resolve(2);
  console.log(3);
}).then((o) => console.log(o));
 
new Promise((resolve) => {
  console.log(4);
  resolve(5);
})
  .then((o) => console.log(o))
  .then(() => console.log(6));
```
1,3,4,2,5,6,0