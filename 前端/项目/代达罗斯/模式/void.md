# void
> Last Format Time：8/13/2026 15:14:02

---
## 使用 void 忽略 Promise 返回值
导航通常返回 Promise。前面加 `void` 表示“我明确选择忽略这个返回值”，也能满足部分 no-floating-promises 规则。它不会捕获失败，也不会让操作更安全；需要根据结果继续处理时使用 `await`，需要错误反馈时使用 `await` 或 `.catch(...)`。

```ts
    handleCreateKeyDown: (event) => {
      // ============================================================
      // 📝 第1题（5分，文件 1/3）：把键盘意图映射到已有动作
      // ============================================================
      // 📍 上下文：创建团队输入框会把 keydown 事件交给这里。
      // 🎯 行为：Enter 发起创建，Escape 清错并退出创建面板。
      // 📥 已知：event.key、get().handleCreateTeamClick、set。
      // 📤 产出：两个互不混淆的按键分支。
      // 🧭 路线：1. 判断 Enter 并调用已有异步动作；2. 判断 Escape 并收起面板。
      // ⚠️ 边界：事件回调不能返回创建 Promise 给 React。
      // 💡 可用 API：void、get、set。
      // ✅ 自检：普通按键无副作用；Escape 同时清除旧错误。
      // ✏️ 你的代码：

      console.log("event", event)
      if (event.key === "Enter") {
        void get().handleCreateTeamClick()
      } else if (event.key === "Escape") {
        get().handleCloseCreateClick()
      }
    },
```

这里的 `void` 是 **JavaScript 的一元运算符**，作用是：

> 执行后面的表达式，但主动忽略它的返回值，整个表达式的结果固定为 `undefined`。

你这段代码大概率完整形式是：

```ts
const handlePublish = useCallback(() => {
  void form.handleSubmit((values) => {
    if (form.formState.isDirty) {
      persistDraft(values, publishRevision);
      return;
    }
  })();
}, [form, persistDraft, publishRevision]);
```

重点在最后的 `()`：

```ts
void form.handleSubmit(callback)();
```

可以拆成：

```ts
const submitHandler = form.handleSubmit(callback);
const promise = submitHandler();

void promise;
```

---
## 为什么加 `void`
React Hook Form 的 `handleSubmit` 返回一个提交处理函数，而执行这个函数通常会返回 `Promise<void>`：

```ts
const submitHandler = form.handleSubmit(callback);

submitHandler(); // 返回 Promise<void>
```

如果项目开启了 ESLint 的 `@typescript-eslint/no-floating-promises`，直接调用可能会警告：

```ts
submitHandler();
// Promise 没有被 await、return 或 catch
```

加上 `void` 是在明确告诉代码检查工具：

```ts
void submitHandler();
```

意思是：

> 我知道这里返回了 Promise，但我就是不等待它，也不使用它的结果。

它类似于：

```ts
submitHandler().catch((error) => {
  // 处理错误
});
```

但二者并不完全等价：`void` **不会处理 Promise 的异常**，只是忽略返回值。

---
## 特别注意最后的 `()`
下面两段含义完全不同：

```ts
void form.handleSubmit(callback);
```

这段只调用了 `handleSubmit` 来创建提交函数，**没有真正执行表单提交**。

而：

```ts
void form.handleSubmit(callback)();
```

最后多了一个 `()`，才是真正执行提交函数。

因此可以这样理解：

```ts
form.handleSubmit(callback)
// 生成提交函数

form.handleSubmit(callback)()
// 立即执行生成的提交函数

void form.handleSubmit(callback)()
// 立即执行，同时忽略其 Promise 返回值
```

在你的代码中，`void` 主要是为了处理“异步函数返回的 Promise 没有被使用”的类型检查或 ESLint 警告。
