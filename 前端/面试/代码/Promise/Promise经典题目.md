# Promise经典题目
### 事件循环与输出顺序
这道题考察同步代码、微任务（Promise）和宏任务（setTimeout）的执行优先级。
```javascript
console.log('start');

setTimeout(() => {
    console.log('setTimeout');
}, 0);

Promise.resolve().then(() => {
    console.log('promise1');
}).then(() => {
    console.log('promise2');
});

console.log('end');
```

答案：
```node
[Running] node "g:\Save\Grogramming\Test\index.js"
start
end
promise1
promise2
setTimeout
```

---
### Promise 的状态不可变性 🌟
🌟表示不会
这道题考察 Promise 内部状态的流转规则。
```javascript
const p = new Promise((resolve, reject) => {
    resolve('Success');
    reject('Error');
});

p.then(value => console.log(value))
 .catch(error => console.log(error));
```

_思考点：控制台会输出什么？为什么 `reject` 没有生效？_
答案：状态已经转换为了fulfill，不会再rejected了，打印为Success，catch不会调用

```js
const p = new Promise((resolve, reject) => {
    resolve('Success')
    reject('Error')
})

p.then((value) => console.log(value), (error) => console.log(error))
```

改成这样是一样的，原因同上。Promise 的状态一旦确定为 fulfilled ，就不会再改变。即使后面调用了 reject ，也会被忽略。打印为Success

---
### async/await 中的错误捕获
在实际业务中，如何优雅地处理异步请求的错误是非常核心的能力。
```javascript
async function getData() {
    try {
        const data = await Promise.reject('出错了');
        console.log(data);
    } catch (error) {
        console.log('捕获到:', error);
    }
}
getData();
```

_思考点：这段代码的输出是什么？除了 `try/catch`，你还能想到其他处理方式吗（提示：`.catch`）？_

答案：
捕获到: 出错了

```js
async function getData() {
    const data = await Promise.reject('出错了').catch(error => {
        console.log('捕获到:', error)
        return error  // 可选：返回默认值让代码继续执行
    })
    console.log(data)
}
getData()
```

---
### 手撕进阶版 Promise.all
其他位置有
`myPromiseAll`：
```javascript
function myPromiseAll(promises) {
    // 请在这里补充你的实现逻辑

    let fulfilledNum = 0
    const n = promises.length
    let ans = Array(n).fill(null)

    return new Promise((resolve, reject) => {
        promises.forEach((promise, index) => {
            Promise.resolve(promise)
                .then((res) => {
                    ans[index] = res
                    fulfilledNum++
                    if (fulfilledNum === n) resolve(ans)
                })
                .catch((err) => {
                    reject(err)
                })
        })
    })
}

// 测试用例：
myPromiseAll([Promise.resolve(1), Promise.resolve(2), Promise.resolve(3)])
    .then(console.log)
    .catch(console.error)
// [ 1, 2, 3 ]
```

_思考点：你需要确保所有的 Promise 都成功后按原顺序返回结果数组；只要有一个失败，就立即 reject。_

---
### 手写支持链式调用的 Promise
**题目要求：** 实现一个 `MyPromise`，必须满足以下核心规范：

1. 状态只能从 `pending` -> `fulfilled` 或 `rejected`，且不可逆。
2. `then` 方法必须返回一个**新的 Promise**，以支持链式调用。
3. 如果 `then` 的回调返回的是普通值，直接传递给下一个 `then`；如果返回的是 Promise，则等待其执行完毕后再传递结果（值的穿透与异步解析）。
4. 必须处理微任务异步执行（使用 `queueMicrotask` 或 `setTimeout` 模拟）。

**参考答案：**
```javascript
class MyPromise {
    constructor(executor) {
        this.state = 'pending';
        this.value = undefined;
        this.reason = undefined;
        this.onFulfilledCallbacks = [];
        this.onRejectedCallbacks = [];

        const resolve = (value) => {
            if (this.state === 'pending') {
                this.state = 'fulfilled';
                this.value = value;
                // 异步执行所有暂存的成功回调
                this.onFulfilledCallbacks.forEach(fn => fn());
            }
        };

        const reject = (reason) => {
            if (this.state === 'pending') {
                this.state = 'rejected';
                this.reason = reason;
                // 异步执行所有暂存的失败回调
                this.onRejectedCallbacks.forEach(fn => fn());
            }
        };

        try {
            executor(resolve, reject);
        } catch (err) {
            reject(err);
        }
    }

    then(onFulfilled, onRejected) {
        // 参数穿透：如果不传回调，默认透传值或抛出错误
        onFulfilled = typeof onFulfilled === 'function' ? onFulfilled : value => value;
        onRejected = typeof onRejected === 'function' ? onRejected : reason => { throw reason };

        const promise2 = new MyPromise((resolve, reject) => {
            const handleCallback = (callback, arg) => {
                queueMicrotask(() => { // 保证异步执行
                    try {
                        const x = callback(arg);
                        resolvePromise(promise2, x, resolve, reject);
                    } catch (err) {
                        reject(err);
                    }
                });
            };

            if (this.state === 'fulfilled') {
                handleCallback(onFulfilled, this.value);
            } else if (this.state === 'rejected') {
                handleCallback(onRejected, this.reason);
            } else {
                // pending 状态，先暂存回调
                this.onFulfilledCallbacks.push(() => handleCallback(onFulfilled, this.value));
                this.onRejectedCallbacks.push(() => handleCallback(onRejected, this.reason));
            }
        });

        return promise2;
    }
}

// 核心：解析 then 回调的返回值，决定新 Promise 的状态
function resolvePromise(promise2, x, resolve, reject) {
    if (promise2 === x) {
        return reject(new TypeError('Chaining cycle detected'));
    }
    if (x instanceof MyPromise) {
        x.then(resolve, reject);
    } else {
        resolve(x);
    }
}
```

---
### 异步任务并发控制器 (Concurrency Limit)
其他位置有
**题目要求：** 实现一个 `asyncPool(limit, tasks)` 函数。

- `limit`：最大并发数。
- `tasks`：返回 Promise 的函数数组。
- **核心逻辑**：始终保持当前正在运行的任务数不超过 `limit`。当有任务完成时，立即从队列中取出下一个任务执行，直到所有任务完成。

**参考答案：**
```javascript
async function asyncPool(limit, tasks) {
    const results = [];
    const executing = new Set();
	
    for (const [index, task] of tasks.entries()) {
        // 包装任务，记录索引以便按顺序存入结果
        const p = task().then(res => {
            results[index] = res;
        });
        
        executing.add(p);
        
        // 核心：当执行中的任务数达到上限时，等待最快完成的那个任务
        if (executing.size >= limit) {
            await Promise.race(executing);
        }
        
        // 清理已完成的任务
        p.finally(() => executing.delete(p));
    }
	
    // 等待剩余未完成的任务
    await Promise.all(executing);
    return results;
}

// 测试用例
const tasks = Array.from({ length: 5 }, (_, i) => () => 
    new Promise(resolve => setTimeout(() => resolve(i), Math.random() * 1000))
);
asyncPool(2, tasks).then(console.log); // [0, 1, 2, 3, 4]
```

---
### 带重试机制与超时控制的请求包装器
**题目要求：** 实现 `retryWithTimeout(asyncFn, maxRetries, timeout)`。

1. 如果 `asyncFn` 在 `timeout` 毫秒内未完成，直接抛出超时错误，并触发重试。
2. 如果 `asyncFn` 抛出异常，自动重试，直到达到 `maxRetries` 次。
3. 建议加入**指数退避**（Exponential Backoff）策略，避免瞬间压垮服务器。

**参考答案：**
```javascript
async function retryWithTimeout(asyncFn, maxRetries = 3, timeout = 2000) {
    let retries = 0;

    while (retries < maxRetries) {
        try {
            // 使用 Promise.race 实现超时控制
            const timeoutPromise = new Promise((_, reject) =>
                setTimeout(() => reject(new Error(`Timeout after ${timeout}ms`)), timeout)
            );
	        // 这里使用race也太巧妙了吧
            const result = await Promise.race([asyncFn(), timeoutPromise]);
            return result; // 成功则直接返回
            
        } catch (err) {
            retries++;
            console.warn(`Attempt ${retries} failed: ${err.message}`);
            
            if (retries >= maxRetries) {
                throw new Error(`Max retries (${maxRetries}) exceeded. Last error: ${err.message}`);
            }
            
            // 指数退避 + 随机抖动：避免惊群效应
            const delay = Math.min(1000 * Math.pow(2, retries), 10000) + Math.random() * 1000;
            await new Promise(r => setTimeout(r, delay));
            // await new Promise(r => setTimeout(r, 1000));
        }
    }
}
```

---
### 红绿灯循环控制
**题目要求：** 红灯亮 3 秒，绿灯亮 2 秒，黄灯亮 1 秒，依次无限循环打印。

- **核心难点**：利用 `async/await` 将异步串行化，写出同步代码般的可读性，彻底告别 `.then()` 嵌套地狱。

**参考答案：**
```javascript
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function trafficLight() {
    while (true) {
        console.log('🔴 红灯亮');
        await sleep(3000);
        
        console.log('🟢 绿灯亮');
        await sleep(2000);
        
        console.log('🟡 黄灯亮');
        await sleep(1000);
    }
}

trafficLight();
```

---
### 面试官视角点评
1. **链式 Promise**：不要死记硬背几百行代码，重点讲清楚 `resolvePromise` 这个辅助函数的作用，它是处理“返回值可能是 Promise”的核心枢纽。
2. **并发控制**：`Promise.race` 配合 `Set` 清理是目前的最佳实践。如果你能提到“为什么不用 `for...of` 直接 `await`（那是串行）”或者“为什么不用 `Promise.all`（无法限制并发）”，会非常加分。
3. **重试超时**：一定要提**指数退避**和**随机抖动**。这是区分“玩具代码”和“生产级代码”的关键细节。
4. **红绿灯**：这题看似简单，但考察的是你对 `async/await` 本质的理解——它只是语法糖，底层依然是 Promise 和微任务队列。写得越简洁，说明你越熟练。