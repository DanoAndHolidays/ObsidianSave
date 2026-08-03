# void

---
##

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
