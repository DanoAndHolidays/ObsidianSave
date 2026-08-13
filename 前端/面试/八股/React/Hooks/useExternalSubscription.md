# useExternalSubscription
> Last Format Time：8/13/2026 15:14:03

[[useSyncExternalStore]]

---
## 先把嵌套写法展开
当前代码：

```tsx
useExternalSubscription(
  useCallback(() => {
    const handler = (event: MouseEvent) => {
      if (
        ref.current &&
        !ref.current.contains(event.target as Node)
      ) {
        closeMenu();
      }
    };

    if (menuOpen) {
      document.addEventListener("mousedown", handler);
    }

    return () =>
      document.removeEventListener("mousedown", handler);
  }, [closeMenu, menuOpen]),
);
```

它等价于：

```tsx
const subscribe = useCallback(() => {
  const handler = (event: MouseEvent) => {
    if (
      ref.current &&
      !ref.current.contains(event.target as Node)
    ) {
      closeMenu();
    }
  };

  if (menuOpen) {
    document.addEventListener("mousedown", handler);
  }

  return () =>
    document.removeEventListener("mousedown", handler);
}, [closeMenu, menuOpen]);

useExternalSubscription(subscribe);
```

展开以后，位置关系就清楚了：

```text
useCallback
    ↓ 返回 memoized subscribe 函数
useExternalSubscription(subscribe)
    ↓ 把 subscribe 交给
useSyncExternalStore
```

我更推荐展开后的写法来学习，因为嵌套写法容易让人误以为 `useExternalSubscription` 在 `useCallback` 里面。

实际正好相反：`useCallback(...)` 先执行，得到函数，然后这个函数作为参数传给 `useExternalSubscription(...)`。

---
## `useCallback` 到底返回了什么
这里存在两层“返回函数”，非常容易混淆。

```tsx
const subscribe = useCallback(
  () => {
    // 订阅逻辑

    return () => {
      // 清理逻辑
    };
  },
  [menuOpen],
);
```

第一层：

```tsx
useCallback(fn, deps)
```

返回的是缓存后的 `fn`，也就是 `subscribe`：

```tsx
const subscribe = fn;
```

第二层：

```tsx
subscribe()
```

当 `subscribe` 以后真正被调用时，才会返回 cleanup：

```tsx
const unsubscribe = subscribe();
```

所以关系是：

```text
useCallback(...)
    → 返回 subscribe

subscribe()
    → 注册 listener
    → 返回 unsubscribe

unsubscribe()
    → 删除 listener
```

因此，你之前说的“`useCallback` 返回的是清理函数”不准确。

准确说法是：

> `useCallback` 返回订阅函数；订阅函数被调用后，再返回清理函数。

---
## 谁真正调用了 `subscribe`
看自定义 Hook：

```tsx
export const useExternalSubscription = (
  subscribe: ExternalSubscribe,
): void => {
  const normalizedSubscribe = useCallback(
    (onStoreChange: () => void) =>
      subscribe(onStoreChange) ?? (() => undefined),
    [subscribe],
  );

  useSyncExternalStore(
    normalizedSubscribe,
    getSnapshot,
    getSnapshot,
  );
};
```

实际调用链是：

```text
组件渲染
→ useCallback 创建 subscribe
→ useExternalSubscription 接收 subscribe
→ 创建 normalizedSubscribe
→ useSyncExternalStore 接收 normalizedSubscribe
→ React 调用 normalizedSubscribe
→ normalizedSubscribe 调用 subscribe
→ subscribe 注册 mousedown
→ subscribe 返回 removeEventListener
→ useSyncExternalStore 保存这个返回函数
```

所以真正理解 cleanup 的是：

```tsx
useSyncExternalStore(normalizedSubscribe, ...)
```

`useSyncExternalStore` 的订阅协议大致是：

```ts
type Subscribe = (
  onStoreChange: () => void,
) => () => void;
```

也就是：

```text
调用 subscribe 开始订阅
subscribe 返回 unsubscribe
需要重订阅或卸载时，React 调用 unsubscribe
```

---
## `normalizedSubscribe` 为什么还要包一层
类型允许传入的 `subscribe` 不返回任何东西：

```ts
export type ExternalSubscribe = (
  onStoreChange: () => void,
) => void | (() => void);
```

但是 `useSyncExternalStore` 希望始终得到一个清理函数。

因此这里做了归一化：

```tsx
subscribe(onStoreChange) ?? (() => undefined)
```

分两种情况：

```text
subscribe 返回 cleanup
→ 使用真实 cleanup

subscribe 返回 undefined
→ 使用空函数 () => undefined
```

这样 `useSyncExternalStore` 永远可以安全调用清理函数。

在当前 `WorkspaceSwitcher` 中，订阅函数始终返回：

```tsx
() => document.removeEventListener(...)
```

所以兜底函数没有被用到。但这个自定义 Hook 还可能接收其他不返回 cleanup 的订阅函数，因此统一包了一层。

---
## `onStoreChange` 为什么没有使用
`useSyncExternalStore` 调用订阅函数时，会传入：

```tsx
onStoreChange
```

正常的外部 Store 会在数据变化时调用它：

```tsx
store.subscribe(() => {
  onStoreChange();
});
```

然后 React 会重新读取 snapshot。

但本题传入的函数没有声明参数：

```tsx
useCallback(() => {
  // ...
}, []);
```

JavaScript 允许调用函数时传入多余参数，所以：

```tsx
subscribe(onStoreChange);
```

不会报错，只是这个参数被忽略了。

而且这里的 snapshot 永远是：

```tsx
const getSnapshot = () => 0;
```

因此这个自定义 Hook 并不是真的用 `useSyncExternalStore` 同步一份外部状态，它主要借用了：

- 订阅时机；
- 重订阅机制；
- 卸载清理机制。

这里的状态更新仍然是 `closeMenu()` 修改 Zustand Store，而不是通过 `onStoreChange` 完成。

---
## 菜单打开和关闭时发生了什么
### 初次渲染：`menuOpen === false`
`useCallback` 生成一个记住 `false` 的 `subscribe₀`。

React 随后调用它：

```tsx
subscribe₀();
```

内部发生：

```text
创建 handler₀
→ menuOpen 是 false
→ 不注册 listener
→ 返回 remove(handler₀)
```

虽然没有注册，之后调用 `removeEventListener` 也没有问题；删除一个不存在的 listener 是安全的。

### 点击按钮：`menuOpen` 变成 `true`
组件重新渲染。

因为依赖发生变化：

```tsx
[closeMenu, menuOpen]
```

`useCallback` 产生新的 `subscribe₁`。

`useSyncExternalStore` 发现订阅函数变了，于是：

```text
先调用旧 unsubscribe₀
→ 再调用新 subscribe₁
→ 创建 handler₁
→ 注册 handler₁
→ 保存 unsubscribe₁
```

### 点击菜单外部
```text
document 收到 mousedown
→ handler₁ 执行
→ ref.current.contains(target) 为 false
→ closeMenu()
→ Zustand 把 menuOpen 改为 false
→ 组件重新渲染
```

这时又产生新的 `subscribe₂`。

`useSyncExternalStore` 会：

```text
调用 unsubscribe₁
→ removeEventListener("mousedown", handler₁)
→ 调用 subscribe₂
→ 因 menuOpen=false，不再注册
```

因此监听器不会累积。

---
## 为什么必须使用同一个 `handler`
正确：

```tsx
const handler = () => closeMenu();

document.addEventListener("mousedown", handler);

return () => {
  document.removeEventListener("mousedown", handler);
};
```

注册和删除使用的是同一个函数对象。

错误：

```tsx
document.addEventListener(
  "mousedown",
  () => closeMenu(),
);

return () => {
  document.removeEventListener(
    "mousedown",
    () => closeMenu(),
  );
};
```

虽然两个函数代码相同，但它们是两个不同的对象：

```tsx
(() => closeMenu()) === (() => closeMenu());
// false
```

浏览器根据“事件类型 + 函数引用”寻找需要删除的 listener。找不到原来的函数，就无法删除。

这就是“对称清理”的核心：

```text
同一个目标
+ 同一个事件类型
+ 同一个 handler 引用
+ 相同的 capture 配置
```

---
## 为什么这些 Hook 必须放在 `return` 前面
当前代码后面有提前返回：

```tsx
if (isLoading && !personal) {
  return <Loading />;
}
```

所以这些 Hook 必须写在这个分支之前：

```tsx
useExternalSubscription(
  useCallback(...),
);

if (isLoading && !personal) {
  return <Loading />;
}
```

不能写成：

```tsx
if (!isLoading) {
  useExternalSubscription(
    useCallback(...),
  );
}
```

也不能写到提前返回之后。因为不同渲染中调用的 Hook 数量和顺序可能变化，违反 Hook 规则。

正确原则是：

> Hook 始终调用，是否注册 listener 放进订阅函数内部判断。

也就是：

```tsx
if (menuOpen) {
  document.addEventListener(...);
}
```

条件控制的是副作用，不是 Hook 调用。

---
## 与 `useEffect` 对比
这段逻辑如果使用 `useEffect`，会更接近常见写法：

```tsx
useEffect(() => {
  if (!menuOpen) return;

  const handler = (event: MouseEvent) => {
    if (
      ref.current &&
      !ref.current.contains(event.target as Node)
    ) {
      closeMenu();
    }
  };

  document.addEventListener("mousedown", handler);

  return () => {
    document.removeEventListener("mousedown", handler);
  };
}, [closeMenu, menuOpen]);
```

两者的 cleanup 归属不同：

```text
useEffect
→ React 直接把 effect 回调的返回值视为 cleanup

当前代码
→ useCallback 只缓存 subscribe
→ useSyncExternalStore 调用 subscribe
→ useSyncExternalStore 把 subscribe 的返回值视为 cleanup
```

因此记忆规则不是“回调里 return 函数就是 cleanup”，而是：

> 返回函数是否属于 cleanup，取决于接收这个回调的 API 契约。

---
## 为什么依赖是这两个
```tsx
[closeMenu, menuOpen]
```

`menuOpen` 必须存在，因为订阅函数需要知道本次是否注册 listener。

如果漏掉它：

```tsx
useCallback(() => {
  if (menuOpen) {
    document.addEventListener(...);
  }
}, [closeMenu]);
```

回调可能一直记住首次渲染的 `menuOpen === false`。菜单后来打开，订阅函数引用却没有变化，监听器可能永远不会注册。这就是陈旧闭包。

`closeMenu` 也被回调使用，因此放入依赖。虽然 Zustand action 通常引用稳定，但依赖数组应根据“是否读取了外部变量”来写，而不是依赖当前实现碰巧稳定。

`ref` 不需要放进去，因为 `useRef` 返回的 ref 对象在整个组件生命周期中引用稳定；真正变化的是：

```tsx
ref.current
```

handler 执行时会读取最新的 `ref.current`。

最推荐你用下面这个展开版本建立心智模型：

```tsx
const subscribeOutsideClick = useCallback(() => {
  if (!menuOpen) return;

  const handler = (event: MouseEvent) => {
    const element = ref.current;

    if (
      element &&
      !element.contains(event.target as Node)
    ) {
      closeMenu();
    }
  };

  document.addEventListener("mousedown", handler);

  return () => {
    document.removeEventListener("mousedown", handler);
  };
}, [closeMenu, menuOpen]);

useExternalSubscription(subscribeOutsideClick);
```

这里一眼可以看出：

```text
useCallback：生产稳定的 subscribe
useExternalSubscription：消费 subscribe
useSyncExternalStore：执行 subscribe 并管理 unsubscribe
handler：处理浏览器事件
cleanup：移除 handler
```