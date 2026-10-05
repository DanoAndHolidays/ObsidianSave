# Pipeline 管道
> Last Format Time：10/6/2026 02:27:25

这类题通常有两种常见含义：
1. **串行管道**：上一个异步任务的结果，作为下一个任务的输入。
2. **任务队列**：多个异步任务按顺序执行，保证同一时刻只跑一个。

面试里最常写的是第 2 种，我先给你这个版本。

```js
class Pipeline {
  constructor() {
    this.queue = [];
    this.running = false;
  }

  add(task) {
    // task 必须是一个返回 Promise 的函数
    this.queue.push(task);
    this.run();
    return this;
  }

  async run() {
    if (this.running) return;
    this.running = true;

    while (this.queue.length) {
      const task = this.queue.shift();
      try {
        await task();
      } catch (err) {
        console.error("task failed:", err);
      }
    }

    this.running = false;
  }
}
```

使用方式：
```js
const pipeline = new Pipeline();

pipeline.add(async () => {
  console.log("task1 start");
  await new Promise(r => setTimeout(r, 1000));
  console.log("task1 end");
});

pipeline.add(async () => {
  console.log("task2 start");
  await new Promise(r => setTimeout(r, 500));
  console.log("task2 end");
});
```

执行结果一定是：
```js
task1 start
task1 end
task2 start
task2 end
```

如果题目要求的是“前一个任务的返回值传给下一个任务”，那就写成这个版本：
```js
function pipeline(tasks, initialValue) {
  return tasks.reduce((prevPromise, task) => {
    return prevPromise.then(task);
  }, Promise.resolve(initialValue));
}
```

例子：
```js
pipeline(
  [
    async (v) => v + 1,
    async (v) => v * 2,
    async (v) => `result: ${v}`,
  ],
  1
).then(console.log); // result: 4
```

这个写法的核心就一句话：
**用 `Promise.then()` 或 `async/await` 把多个异步任务串起来。**
如果你把题目原文贴出来，我可以直接按那道题的要求给你写完整答案。