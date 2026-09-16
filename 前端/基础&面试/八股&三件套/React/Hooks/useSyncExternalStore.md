# useSyncExternalStore
> Last Format Time：8/13/2026 15:14:03

[https://zh-hans.react.dev/reference/react/useSyncExternalStore](https://zh-hans.react.dev/reference/react/useSyncExternalStore)

*有点诡异了，这里是通过zustand的set来更新的，重新渲染，然后就把这个钩子运行起来了
Zustand 更新导致重新渲染；重新渲染又导致 `useSyncExternalStore` 调整 DOM 订阅。*

[https://zh-hans.react.dev/reference/react/useSyncExternalStore](https://zh-hans.react.dev/reference/react/useSyncExternalStore) 我阅读了这篇文档，我理解了这个hook的作用，是用来将一些react外部的状态更新接入react的渲染更新流程的，但是我们这里使用的getSnapshot均是返回一个数字，也就是每次的快照都是一样的，这怎么能够触发更新呢

你的判断完全正确：

> `getSnapshot()` 永远返回 `0`，所以这个 `useSyncExternalStore` 不可能因为“快照变化”触发组件更新。

这里的组件更新来自 Zustand 的 `useStore`。`useSyncExternalStore` 只是被“借用”来管理订阅和清理的生命周期。

---
## 标准的 `useSyncExternalStore`
标准模型是：

```tsx
const snapshot = useSyncExternalStore(
  subscribe,
  getSnapshot,
);
```

运行过程：

```text
外部 Store 变化
→ subscribe 保存的 onStoreChange 被调用
→ React 再次执行 getSnapshot()
→ 将新旧 snapshot 用 Object.is 比较
→ 不相等才触发重新渲染
```

例如：

```tsx
const subscribe = (onStoreChange: () => void) => {
  store.addListener(onStoreChange);

  return () => {
    store.removeListener(onStoreChange);
  };
};

const getSnapshot = () => store.value;
```

假设：

```text
旧 snapshot = 1
新 snapshot = 2
Object.is(1, 2) = false
→ 重新渲染
```

如果始终返回 `0`：

```text
旧 snapshot = 0
新 snapshot = 0
Object.is(0, 0) = true
→ 不重新渲染
```

这是 React 官方文档描述的核心机制：[useSyncExternalStore](https://zh-hans.react.dev/reference/react/useSyncExternalStore)。

---
## 本项目没有使用这条更新链
项目实现：

```tsx
const getSnapshot = () => 0;

useSyncExternalStore(
  normalizedSubscribe,
  getSnapshot,
  getSnapshot,
);
```

而且组件提供的订阅函数没有使用 `onStoreChange`：

```tsx
useCallback(() => {
  const handler = () => {
    closeMenu();
  };

  document.addEventListener("mousedown", handler);

  return () => {
    document.removeEventListener("mousedown", handler);
  };
}, [closeMenu, menuOpen]);
```

完整调用时，其实是：

```tsx
normalizedSubscribe(onStoreChange)
→ subscribe(onStoreChange)
```

但是 `subscribe` 声明时没有参数：

```tsx
() => {
  // ...
}
```

JavaScript 允许传入多余参数，所以 `onStoreChange` 被直接忽略了。

因此这里有两个原因导致它不会触发 React 更新：

1. `onStoreChange` 从来没有调用；
2. 即使调用，`getSnapshot()` 也始终是 `0`，React 会认为状态没变化。

---
## 那么菜单为什么仍然会更新
因为组件已经通过 Zustand 的 `useStore` 订阅了 `menuOpen`：

```tsx
const menuOpen = useStore(
  switcherStore,
  (state) => state.menuOpen,
);
```

真正的更新流程是：

```text
外部 mousedown
→ document handler 执行
→ closeMenu()
→ Zustand set({ menuOpen: false })
→ Zustand 通知 useStore
→ useStore 触发 WorkspaceSwitcherContent 重新渲染
```

可以把两条链路彻底分开：

```text
负责组件更新：

closeMenu()
→ Zustand Store 改变
→ useStore 收到通知
→ React 重新渲染


负责 listener 生命周期：

组件重新渲染
→ useCallback 因 menuOpen 变化产生新 subscribe
→ useSyncExternalStore 清理旧 subscribe
→ 调用新 subscribe
→ 添加或不添加 document listener
```

也就是说：

> Zustand 更新导致重新渲染；重新渲染又导致 `useSyncExternalStore` 调整 DOM 订阅。

不是 `useSyncExternalStore` 导致这次重新渲染。

---
## 为什么常量快照下订阅仍然会执行
虽然快照永远不变，`useSyncExternalStore` 仍然需要建立订阅。

React 会调用：

```tsx
normalizedSubscribe(onStoreChange);
```

然后保存它返回的 unsubscribe：

```tsx
const unsubscribe =
  normalizedSubscribe(onStoreChange);
```

当订阅函数的引用改变，或者组件卸载时，React 调用：

```tsx
unsubscribe();
```

因此本项目借用了它的两个能力：

- 挂载或订阅函数变化时调用 `subscribe`；
- 重订阅或卸载时调用 `unsubscribe`。

但没有使用它的核心能力：

- 读取外部状态快照；
- 根据快照变化触发重新渲染。

---
## `menuOpen` 改变时的完整过程
假设菜单最初关闭。

### 第一次渲染
```text
menuOpen = false
→ useCallback 得到 subscribe₀
→ useSyncExternalStore 调用 subscribe₀
→ 不添加 mousedown listener
→ 保存 unsubscribe₀
```

### 用户打开菜单
点击按钮执行 Zustand action：

```text
handleToggleClick()
→ Zustand 把 menuOpen 改成 true
→ useStore 触发重新渲染
```

重新渲染时：

```text
menuOpen 从 false 变成 true
→ useCallback 依赖变化
→ 得到新的 subscribe₁
→ normalizedSubscribe 也变了
→ useSyncExternalStore 调用 unsubscribe₀
→ 再调用 subscribe₁
→ 添加 mousedown listener
→ 保存 unsubscribe₁
```

### 点击菜单外部
```text
mousedown handler
→ closeMenu()
→ Zustand 把 menuOpen 改成 false
→ useStore 触发重新渲染
→ useCallback 得到 subscribe₂
→ useSyncExternalStore 调用 unsubscribe₁
→ removeEventListener
→ 调用 subscribe₂
→ 因为 menuOpen=false，不再注册 listener
```

所以这里存在一个前提：

> `menuOpen` 必须已经通过其他方式让组件重新渲染。

当前这个“其他方式”就是 Zustand 的 `useStore`。

如果删掉：

```tsx
const menuOpen = useStore(
  switcherStore,
  (state) => state.menuOpen,
);
```

同时组件也不再订阅任何会随 `closeMenu()` 改变的状态，那么 `closeMenu()` 后组件可能不会重新渲染，订阅函数也不会更新，旧 listener 就可能继续存在。

---
## 这里的设计是否合理
它能正常工作，但不属于 `useSyncExternalStore` 最典型的用途。更准确地说，它把 `useSyncExternalStore` 当作了一个“订阅生命周期管理器”。

对于 `document.addEventListener`，普通 `useEffect` 会更直接：

```tsx
useEffect(() => {
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
```

这里语义非常明确：

```text
依赖变化
→ 先执行旧 effect cleanup
→ 再执行新 effect
```

而当前封装是：

```text
依赖变化
→ subscribe 引用变化
→ useSyncExternalStore 退订旧函数
→ 再订阅新函数
```

二者在当前场景下得到相似的 listener 生命周期，但概念不同。

---
## 最重要的结论
你可以这样记：

```text
useStore
负责：Zustand 状态变化 → React 重新渲染

useCallback
负责：menuOpen 不变时保持 subscribe 函数引用稳定

useExternalSubscription
负责：把 subscribe 适配给 useSyncExternalStore

useSyncExternalStore
在这里负责：调用 subscribe 和 unsubscribe
不负责：根据外部快照触发更新

getSnapshot = () => 0
意味着：这个订阅永远没有可观察的状态变化
```

所以你提出的疑问不是遗漏了什么隐藏机制，而是准确发现了：

> 这段代码只借用了 `useSyncExternalStore` 的订阅/退订生命周期，没有使用它的快照更新能力。


核心关系可以先压缩成一句话：

> `useCallback` 负责生成一个稳定的“订阅函数”，`useExternalSubscription` 把这个订阅函数交给 `useSyncExternalStore` 管理；真正把返回值当 cleanup 的是 `useSyncExternalStore`，不是 `useCallback`。