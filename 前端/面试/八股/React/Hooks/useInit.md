# useInit
> Last Format Time：8/13/2026 15:14:03

```ts
import { useRef } from "react";

export const useInit = <T>(initFunc: () => T): T => {
  const valueRef = useRef<{ value: T } | null>(null);

  if (!valueRef.current) {
    valueRef.current = { value: initFunc() };
  }

  return valueRef.current.value;
};

```

提问这是不是一个单例模式：

不算严格意义上的“单例模式”，但**思想上有点像“每个组件实例内部只初始化一次”**。

这段代码：

```ts
export const useInit = <T>(initFunc: () => T): T => {
  const valueRef = useRef<{ value: T } | null>(null);

  if (!valueRef.current) {
    valueRef.current = { value: initFunc() };
  }

  return valueRef.current.value;
};
```

核心效果是：

> 对于**同一个组件实例**，`initFunc()` 初始化出来的值，在后续 render 中始终复用。

比如：

```tsx
function UserPage() {
  const store = useInit(() => {
    console.log("创建 store");
    return createStore();
  });

  return <div>...</div>;
}
```

组件第一次 render：

```text
valueRef.current
      ↓
     null

于是：
initFunc()
   ↓
createStore()
   ↓
valueRef.current = { value: storeA }
```

之后组件因为 state 更新重新 render：

```text
valueRef.current
      ↓
{ value: storeA }
```

于是不会再执行：

```ts
initFunc()
```

而是直接：

```ts
return storeA;
```

所以：

```text
第一次 render
    │
    ▼
createStore()
    │
    ▼
  storeA
    │
    ├──────────┐
    ▼          ▼
render 2     render 3
    │          │
    ▼          ▼
 storeA      storeA
```

---
## 为什么它不是真正的单例模式？
传统单例一般是：

```ts
let instance: Store | null = null;

function getStore() {
  if (!instance) {
    instance = createStore();
  }

  return instance;
}
```

这意味着整个应用：

```text
组件 A ─┐
组件 B ─┼──> 同一个 store
组件 C ─┘
```

只有一个全局实例。

而你的 `useInit` 是：

```tsx
function App() {
  return (
    <>
      <User />
      <User />
    </>
  );
}
```

两个 `<User />` 是两个 React 组件实例，因此：

```text
User #1
  useRef
    ↓
 storeA

User #2
  useRef
    ↓
 storeB
```

也就是：

```ts
storeA !== storeB
```

所以更准确地说，这是：

> **组件实例级别的惰性初始化（lazy initialization）+ 持久化缓存。**

你也可以把它理解成：

> “每个组件实例自己的 singleton”。

但不要把它和真正的全局 Singleton Pattern 混为一谈。

---
## 为什么不用普通变量？
如果写：

```tsx
function User() {
  const store = createStore();

  return ...
}
```

每次 render：

```text
render 1 → storeA
render 2 → storeB
render 3 → storeC
```

每次都会创建新对象。

而 `useRef`：

```ts
const valueRef = useRef(...)
```

特点是：

```text
组件第一次 render
       ↓
创建 ref
       ↓
后续 render
       ↓
继续使用同一个 ref
```

所以非常适合保存这种：

```ts
store
class instance
service
controller
manager
```

例如 Zustand 经常会出现类似写法：

```tsx
const store = useInit(() =>
  createMcpSetupPageStore(dependencies)
);
```

目的就是：

> **这个 Provider 活着多久，这个 store 就活多久；Provider 重新 render 时不要重新创建 store。**


还有一个很重要的细节：`initFunc()` **最好不要产生外部副作用**。尤其开发环境的 React Strict Mode 下，React 可能为了检查纯函数问题而重复执行初始化相关逻辑，因此不要在这里做类似：

```ts
useInit(() => {
  fetch("/api/create-user"); // ❌
  localStorage.setItem(...); // 不推荐
  sendAnalytics();           // ❌

  return something;
});
```

创建普通对象/store 则很合适：

```ts
useInit(() => createStore()); // ✅
```

一句话总结：

**它不是“整个程序只有一个实例”的单例模式，而是利用 `useRef` 实现“同一个 React 组件实例生命周期内只初始化并复用一个值”。**
