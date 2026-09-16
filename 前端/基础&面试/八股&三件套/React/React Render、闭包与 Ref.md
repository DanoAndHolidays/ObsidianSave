# React Render、闭包与 Ref
> Last Format Time：9/16/2026 19:24:51

题目：
```ts
import { useEffect, useRef, useState } from "react";

export default function Counter() {
  const [count, setCount] = useState(0);

  const countRef = useRef(count);
  countRef.current = count;

  useEffect(() => {
    const timer = setInterval(() => {
      console.log("count:", countRef.current);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  return (
    <button onClick={() => setCount((c) => c + 1)}>
      count: {count}
    </button>
  );
}
```

---
## State 是每次 render 的快照
函数组件每次重新渲染，本质上都会重新执行一次组件函数。

```tsx
function Counter() {
  const [count, setCount] = useState(0);
}
```

可以理解为：
```text
render #1 → count₁ = 0
render #2 → count₂ = 1
render #3 → count₃ = 2
```

每次 render 中的 `count` 都属于当前这一次渲染。

所以：
> **State 是某一次 render 的快照，而不是一个不断被修改的普通变量。**

---
## 闭包会引用创建它的那次 render
```tsx
useEffect(() => {
  const timer = setInterval(() => {
    console.log(count);
  }, 1000);

  return () => clearInterval(timer);
}, []);
```

第一次 render：
```text
render #1
count = 0
   ↑
interval 回调闭包
```

之后即使：
```text
render #2 → count = 1
render #3 → count = 2
```

旧的 interval 回调仍然引用：
```text
render #1 的 count
```

所以一直输出：
```text
0
0
0
```

> **闭包不会自动切换到后续 render 创建的新变量。**

---
## `useEffect(..., [])` 不是“稳定函数引用”
```tsx
useEffect(fn, []);
```

`[]` 的作用是告诉 React，当依赖没有变化时，不需要重新执行这个 Effect。

因此：
```text
render #1
↓
执行 Effect
↓
创建 interval

render #2
↓
Effect 不重新执行

render #3
↓
Effect 不重新执行
```

这和 `useCallback` 不一样：
```tsx
useCallback(fn, []);
```

它控制的是函数引用是否保持稳定。

总结：
```text
useEffect(..., [])
→ 控制 Effect 是否重新执行

useCallback(..., [])
→ 控制函数引用是否重新创建
```

---
## 为什么 `useRef` 可以解决旧闭包问题？
```tsx
const countRef = useRef(count);

countRef.current = count;
```

`useRef` 的关键特点：

> **组件重新 render 时，ref 对象本身保持同一个引用。**

可以理解为：
```text
render #1 ─┐
render #2 ─┼──→ 同一个 countRef 对象
render #3 ─┘
                │
                ↓
        current: 0 → 1 → 2
```

因此旧闭包虽然是在第一次 render 创建的：
```tsx
() => {
  console.log(countRef.current);
}
```

但它保存的是同一个：
```text
countRef 对象
```

每次真正执行回调时，再读取：
```tsx
countRef.current
```

因此可以拿到最新值。

---
## State 和 Ref 的核心区别
### State
```text
render #1 → count₁ = 0
                ↑
              闭包

render #2 → count₂ = 1

render #3 → count₃ = 2
```

旧闭包一直访问：
```text
count₁
```

### Ref
```text
render #1 ─┐
render #2 ─┼──→ ref
render #3 ─┘      │
                  ↓
        { current: 0 → 1 → 2 }
```

闭包保存的是：
```text
同一个 ref 对象
```

然后运行时读取最新的：
```tsx
ref.current
```

---
## 为什么普通对象不能代替 `useRef`？
```tsx
const obj = {
  value: count,
};
```

这个对象是在组件函数内部创建的，因此每次 render 都会创建新对象：
```text
render #1 → obj₁ = { value: 0 }
render #2 → obj₂ = { value: 1 }
render #3 → obj₃ = { value: 2 }
```

第一次创建的闭包仍然引用：
```text
obj₁
```

所以还是只能看到：
```text
obj₁.value = 0
```

而 `useRef` 的区别就在于：
```text
普通对象
→ 每次 render 创建新对象

useRef
→ 每次 render 返回同一个对象
```

---
## 总结

> **State 是每次 render 的快照。**

> **Ref 是跨 render 保持 identity 不变的可变对象。**

因此 React 中很多闭包问题，本质上都可以转换成一个问题：

> **这个函数现在引用的是哪一次 render 中的变量？**