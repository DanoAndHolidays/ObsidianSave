# 3 context
> Last Format Time：8/24/2026 15:30:15

---
## `useContext` 订阅的是整个 Context
假设：

```tsx
<TabsContext.Provider
  value={{
    currentValue,
    setValue,
    activationMode,
    baseId,
  }}
>
```

而：

```tsx
function TabsList() {
  const {
    setValue,
    activationMode,
  } = useTabsContext();
}
```

即使 `TabsList` **没有使用 `currentValue`**，当：

```ts
currentValue
// account → password
```

发生变化时，它仍然会重新 render。

原因是 `useContext` 不是 selector：

```text
❌ 订阅 TabsContext.setValue
❌ 订阅 TabsContext.activationMode

✅ 订阅整个 TabsContext value
```

只要 Provider 的：

```ts
value
```

发生变化，Context consumer 就会收到更新。

---
## Context value 看的是引用
例如：

```tsx
<TabsContext.Provider
  value={{
    currentValue,
    setValue,
  }}
>
```

即使：

```ts
currentValue
setValue
```

都没变，只要 `TabsRoot` 因其他原因重新 render：

```ts
{
  currentValue,
  setValue,
}
```

也是一个新对象。

即：

```ts
oldContextValue === newContextValue
// false
```

所以可能产生额外 Context propagation。

---
## `useMemo` 能解决什么？
可以写：

```ts
const contextValue = useMemo(
  () => ({
    currentValue,
    setValue,
    activationMode,
    baseId,
  }),
  [
    currentValue,
    setValue,
    activationMode,
    baseId,
  ]
);
```

它能避免：

```text
Root 因其他原因 render
↓
Context 数据实际上没变
↓
却创建一个新的 {}
↓
consumer 被额外通知
```

但是如果：

```ts
currentValue
```

真的：

```text
account → password
```

那么 dependency 改了：

```text
currentValue 改变
↓
useMemo 重新计算
↓
Context value 改变
↓
consumer 仍然 render
```

所以：

> `useMemo` 只能避免“值没变但对象引用变了”的额外传播，不能阻止真正的 Context 状态更新。

---
## 两条不同的 render 传播路径
这是这一部分最重要的知识。

```text
                   组件为什么 render？
                         │
              ┌──────────┴──────────┐
              ↓                     ↓
       Parent → Child         Context → Consumer
```

### Parent → Child
父组件：

```tsx
function Parent() {
  return <Child />;
}
```

Parent render 时，普通情况下 Child 也会执行。

这条路径主要考虑：

```ts
memo()
```

以及稳定 props。


### Context → Consumer
```tsx
function Child() {
  const value = useContext(SomeContext);
}
```

Provider value 变化：

```text
Provider value changed
↓
Child 是 consumer
↓
Child render
```

这里即使：

```ts
memo(Child)
```

也不能阻止 Context 自身的更新。

所以：

```text
memo
```

和：

```text
Context 拆分
```

解决的是不同问题。

---
## 为什么拆 Context 有意义？
原本：

```ts
type TabsContextValue = {
  currentValue: string;
  setValue: (...) => void;
  activationMode: ActivationMode;
  baseId: string;
};
```

其中：

```text
currentValue
→ 高频变化

setValue
→ 基本稳定

activationMode
→ 基本稳定

baseId
→ 稳定
```

如果全部放在一起：

```text
currentValue 改变
↓
整个 Context value 改变
↓
所有 TabsContext consumers 都受到通知
```

所以可以拆：

```ts
TabsValueContext
TabsActionsContext
TabsConfigContext
```

例如：

```text
TabsValueContext
→ currentValue

TabsActionsContext
→ setValue

TabsConfigContext
→ activationMode
→ baseId
```

这样 `TabsList` 如果只消费：

```ts
TabsActionsContext
TabsConfigContext
```

那么 `currentValue` 改变时，就不会因为 **ValueContext propagation** 被通知。

所以有一个非常重要的结论：

> **Context 的粒度决定 Context 更新传播的粒度。**

---
## 为什么 Actions Context 通常很稳定？
你自己的：

```ts
setValue
```

是：

```ts
const setValue = useCallback(
  (...) => {
    ...
  },
  []
);
```

因此跨 render：

```ts
oldSetValue === newSetValue
// true
```

而：

```ts
currentValue
```

会不断：

```text
account
→ password
→ security
```

因此：

```text
Value Context
→ 高频更新

Actions Context
→ 低频甚至不更新
```

这就是：

> **state / actions 分离**

经常有价值的原因。

---
## 但是还有一个容易忽略的坑
虽然：

```ts
setValue
```

稳定：

```ts
oldSetValue === newSetValue
```

但：

```tsx
<ActionsContext.Provider
  value={{ setValue }}
>
```

这里：

```ts
{ setValue }
```

每次还是一个新对象：

```ts
{ setValue } === { setValue }
// false
```

所以可以直接：

```ts
const TabsActionsContext =
  createContext<
    ((value: string) => void) | null
  >(null);
```

然后：

```tsx
<TabsActionsContext.Provider value={setValue}>
```

或者：

```ts
const actions = useMemo(
  () => ({ setValue }),
  [setValue]
);
```

再：

```tsx
<ActionsContext.Provider value={actions}>
```

所以还要再记一句：

> **函数引用稳定，不代表包含这个函数的新对象也稳定。**
