# Slot
> Last Format Time：8/24/2026 15:33:00

```tsx
import React, { cloneElement, forwardRef, ReactElement } from 'react'

import { mergeProps } from '../lib/mergeProps'
import { composeRefs } from '../lib/composeRefs'

type SlotProps = {
  children: ReactElement<any>
  onClick?: React.MouseEventHandler<HTMLElement>
  [key: string]: any
}

export const Slot = forwardRef<HTMLElement, SlotProps>(function Slot(
  { children, ...slotProps },
  forwardedRef,
) {
  const element = React.Children.only(children)

  return cloneElement(element, {
    ...mergeProps(slotProps, element.props),
    ref: composeRefs(forwardedRef, element.ref),
  })
})

```

可以，给你整理成适合直接记笔记的版本。

---
## React Slot / asChild
### Slot 是什么
`Slot` 的核心作用：

> **自己不创建 DOM，而是把自身的 props、行为和 ref 合并到唯一的子元素上。**

例如：

```tsx
<Slot
  role="tab"
  className="tabs-trigger"
>
  <a href="/account" className="link">
    Account
  </a>
</Slot>
```

最终不是：

```html
<slot>
  <a />
</slot>
```

而是直接：

```html
<a
  href="/account"
  role="tab"
  class="tabs-trigger link"
>
  Account
</a>
```

实现上主要依赖：

```ts
React.cloneElement()
```

---
## `asChild` 的意义
组件默认：

```tsx
<Tabs.Trigger>
  Account
</Tabs.Trigger>
```

可以自己渲染：

```html
<button>Account</button>
```

但：

```tsx
<Tabs.Trigger asChild>
  <a href="/account">
    Account
  </a>
</Tabs.Trigger>
```

希望底层 DOM 由用户决定。

常见实现：

```tsx
const Comp = asChild ? Slot : "button";

return (
  <Comp {...triggerProps}>
    {children}
  </Comp>
);
```

因此：

```text
asChild = false
→ Trigger 自己创建 button

asChild = true
→ Trigger 使用 Slot
→ Slot 把 Trigger 能力注入 child
```

所以 `asChild` 的本质不是简单的：

> “换一个 HTML 标签”

而是：

> **保留组件行为和语义，同时把 DOM 元素所有权交给使用者。**

---
## 为什么不能直接 `return children`
这样：

```tsx
if (asChild) {
  return children;
}
```

虽然不会创建额外 DOM，但会导致组件自身提供的能力全部丢失：

```text
role
aria-*
tabIndex
id
onClick
onKeyDown
ref
className
style
...
```

因此必须把这些能力合并进 child。

---
## Slot 的核心流程
基本结构：

```tsx
function Slot({
  children,
  ...slotProps
}) {
  const child =
    React.Children.only(children);

  const mergedProps =
    mergeProps(
      slotProps,
      child.props
    );

  return React.cloneElement(
    child,
    mergedProps
  );
}
```

流程：

```text
Slot props
+
Child props
↓
mergeProps
↓
cloneElement
↓
得到新的 Child
↓
最终只渲染 Child DOM
```

---
## Props 不能全部简单覆盖
最简单：

```ts
{
  ...slotProps,
  ...childProps
}
```

意味着：

> child 普通 props 优先于 Slot props。

例如：

```tsx
<Slot tabIndex={0}>
  <a tabIndex={-1} />
</Slot>
```

最终：

```tsx
tabIndex={-1}
```

这种策略可以理解为：

```text
Slot 提供默认能力
Child 可以显式覆盖
```

但有几种 props 不能直接覆盖：

```text
event handler
ref
className
style
```

需要特殊 merge。

---
## Event Handler 合并
例如：

```tsx
<Slot onClick={internalOnClick}>
  <a onClick={userOnClick} />
</Slot>
```

不能让其中一个覆盖另一个，而应该 compose：

```ts
function composeEventHandlers<E extends Event>(
  userHandler?: (event: E) => void,
  internalHandler?: (event: E) => void,
) {
  return (event: E) => {
    userHandler?.(event);

    if (!event.defaultPrevented) {
      internalHandler?.(event);
    }
  };
}
```

执行顺序：

```text
user handler
↓
用户可以 preventDefault()
↓
检查 event.defaultPrevented
↓
internal handler
```

为什么用户 handler 要先执行？

因为这允许使用者：

```ts
event.preventDefault();
```

取消组件库内部行为。

注意：

```ts
preventDefault()
```

本身只会阻止浏览器默认行为，并不会自动阻止其他 JS 函数执行。

是组件库主动定义：

```ts
if (!event.defaultPrevented) {
  internalHandler();
}
```

因此 `defaultPrevented` 在这里成为一种 **用户取消内部行为的 escape hatch**。

---
## 通用事件合并
不应该只处理：

```ts
onClick
```

因为还可能有：

```text
onKeyDown
onFocus
onBlur
onPointerDown
onMouseEnter
...
```

所以可以通过：

```ts
/^on[A-Z]/
```

识别 React Event Handler。

注意不要写：

```ts
/^on[A-z]/
```

因为 ASCII 中 `A-z` 还会包含一些特殊字符。

基本规则：

```ts
if (
  /^on[A-Z]/.test(propName) &&
  typeof childValue === "function" &&
  typeof slotValue === "function"
) {
  mergedProps[propName] =
    composeEventHandlers(
      childValue,
      slotValue
    );
}
```

其中：

```text
child handler = user handler
slot handler  = internal handler
```

---
## Ref 合并
Slot 自己需要 DOM：

```ts
internalRef
```

用户也可能需要：

```ts
userRef
```

不能二选一。

应该让两个 ref 都指向同一个 DOM：

```text
        DOM
       /   \
      ↓     ↓
internal   user
ref        ref
```

React ref 有两种常见形式。

对象 ref：

```ts
const ref = useRef(null);

ref.current = node;
```

Callback ref：

```tsx
ref={(node) => {
  // ...
}}
```

因此可以：

```ts
function composeRefs<T>(
  ...refs: Array<
    React.Ref<T> | undefined
  >
) {
  return (node: T | null) => {
    refs.forEach((ref) => {
      if (typeof ref === "function") {
        ref(node);
      } else if (ref) {
        ref.current = node;
      }
    });
  };
}
```

最终：

```tsx
ref={composeRefs(
  internalRef,
  userRef
)}
```

React 只接收到一个 callback ref，但内部把 DOM 同时分发给两个 ref。

---
## className 合并
不能：

```ts
...slotProps,
...childProps
```

直接覆盖，否则其中一个 class 会丢失。

应该拼接：

```ts
const className = [
  slotProps.className,
  childProps.className,
]
  .filter(Boolean)
  .join(" ");
```

例如：

```text
Slot:
tabs-trigger

Child:
my-link

最终:
tabs-trigger my-link
```

---
## style 合并
style 是对象，因此：

```ts
const style = {
  ...slotProps.style,
  ...childProps.style,
};
```

child 优先：

```ts
slot:
{
  color: "red",
  fontSize: 16
}

child:
{
  color: "blue"
}
```

最终：

```ts
{
  color: "blue",
  fontSize: 16
}
```

---
## `mergeProps`
整体规则可以整理成：

```ts
function mergeProps(
  slotProps: Record<string, any>,
  childProps: Record<string, any>,
) {
  const mergedProps = {
    ...slotProps,
    ...childProps,
  };

  for (const propName in childProps) {
    const slotValue =
      slotProps[propName];

    const childValue =
      childProps[propName];

    if (
      /^on[A-Z]/.test(propName) &&
      typeof slotValue === "function" &&
      typeof childValue === "function"
    ) {
      mergedProps[propName] =
        composeEventHandlers(
          childValue,
          slotValue,
        );
    } else if (
      propName === "style"
    ) {
      mergedProps[propName] = {
        ...slotValue,
        ...childValue,
      };
    } else if (
      propName === "className"
    ) {
      mergedProps[propName] = [
        slotValue,
        childValue,
      ]
        .filter(Boolean)
        .join(" ");
    }
  }

  return mergedProps;
}
```

最终规则：

```text
普通 props
→ child 覆盖 slot

event handlers
→ child + slot
→ child 先执行

className
→ 拼接

style
→ object merge
→ child 优先

ref
→ composeRefs
```

---
## Slot 最重要的设计思想
可以把 Slot 理解成：

```text
DOM ownership
→ Child

Behavior ownership
→ Parent component / Slot
```

例如：

```tsx
<Tabs.Trigger asChild>
  <a />
</Tabs.Trigger>
```

DOM 是用户决定的：

```html
<a>
```

但 Tabs 仍然负责：

```text
role
aria-selected
aria-controls
tabIndex
事件
focus management
ref
```

因此 Slot 实际解决的是：

> **如何在不控制 DOM 类型的情况下，仍然把组件库的行为和语义组合到用户元素上。**

这也是 Radix `Slot` / `asChild` 这类设计最核心的价值。
