# Lable
> Last Format Time：7/14/2026 20:56:57

---
## 分析
这个组件里的 `ref`，是 React 中一个非常经典的用法——**`forwardRef` 转发 ref**。

我们先看完整代码：

```tsx
export const Label = forwardRef<
  HTMLLabelElement,
  LabelHTMLAttributes<HTMLLabelElement>
>(
  ({ className, ...props }, ref) => (
    <label
      ref={ref}
      className={cn("text-sm font-medium", className)}
      {...props}
    />
  ),
);
```

我们重点只看 `ref`。

---
## 一、为什么普通组件不能接收 ref？
假设你先这样写一个组件：

```tsx
function Label(props: LabelHTMLAttributes<HTMLLabelElement>) {
  return <label {...props} />;
}
```

别人使用的时候：

```tsx
const labelRef = useRef<HTMLLabelElement>(null);

<Label ref={labelRef} />
```

React 会直接报错（或者提示）：

> Function components cannot be given refs.

因为：

**ref 默认只能绑定到 DOM 元素或者 class 组件。**

例如：

```tsx
<label ref={labelRef}></label>
```

这里没问题。

但是

```tsx
<Label ref={labelRef} />
```

React 根本不知道：

> 这个 ref 应该给 Label 自己？  
> 还是 Label 里面的 `<label>`？

所以函数组件默认是不接收 ref 的。

---
## 二、forwardRef 就是解决这个问题
`forwardRef` 的作用就是：

> **允许父组件把 ref 传进来，然后你决定把它放到哪里。**

可以理解成：

```text
父组件
   │
   │ ref
   ▼
Label组件
   │
   │ forwardRef
   ▼
<label>
```

也就是说：

```text
父组件
↓

const ref = useRef()

↓

<Label ref={ref}/>

↓

forwardRef 接收到 ref

↓

<label ref={ref}/>
```

最终：

```text
ref.current
```

指向的是：

```text
<label>
```

这个 DOM。

---
## 三、这里的 ref 参数是哪来的？
很多人第一次都会疑惑：

```tsx
({ className, ...props }, ref)
```

为什么第二个参数就是 ref？

因为：

```tsx
function Label(props: LabelHTMLAttributes<HTMLLabelElement>) {
  return <label {...props} />;
}
```

React 会自动调用你的函数：

```tsx
function Label(props: LabelHTMLAttributes<HTMLLabelElement>) {
  return <label {...props} />;
}
```

所以：

```tsx
function Label(props: LabelHTMLAttributes<HTMLLabelElement>) {
  return <label {...props} />;
}
```

和普通组件：

```tsx
function Label(props: LabelHTMLAttributes<HTMLLabelElement>) {
  return <label {...props} />;
}
```

不同。

---
## 四、这个 ref 最终有什么用？
例如：

父组件：

```tsx
function Label(props: LabelHTMLAttributes<HTMLLabelElement>) {
  return <label {...props} />;
}
```

打印出来：

```tsx
function Label(props: LabelHTMLAttributes<HTMLLabelElement>) {
  return <label {...props} />;
}
```

也就是说：

```tsx
function Label(props: LabelHTMLAttributes<HTMLLabelElement>) {
  return <label {...props} />;
}
```

就是：

```tsx
function Label(props: LabelHTMLAttributes<HTMLLabelElement>) {
  return <label {...props} />;
}
```

DOM 节点。

于是你可以：

```tsx
function Label(props: LabelHTMLAttributes<HTMLLabelElement>) {
  return <label {...props} />;
}
```

或者：

```tsx
function Label(props: LabelHTMLAttributes<HTMLLabelElement>) {
  return <label {...props} />;
}
```

或者：

```tsx
const labelRef = useRef<HTMLLabelElement>(null);

<Label ref={labelRef} />
```

等等。

虽然 `<label>` 本身一般不会 `focus()`，但对于 `<input>`、`<textarea>` 等组件，这种模式非常常见。

---
## 五、forwardRef 的泛型是什么意思？
这里有两个泛型：

```tsx
const labelRef = useRef<HTMLLabelElement>(null);

<Label ref={labelRef} />
```

第一个：

```tsx
const labelRef = useRef<HTMLLabelElement>(null);

<Label ref={labelRef} />
```

表示：

> ref 指向什么。

也就是说：

```tsx
const labelRef = useRef<HTMLLabelElement>(null);

<Label ref={labelRef} />
```

类型就是：

```tsx
const labelRef = useRef<HTMLLabelElement>(null);

<Label ref={labelRef} />
```

所以才有：

```tsx
const labelRef = useRef<HTMLLabelElement>(null);

<Label ref={labelRef} />
```

这些属性都有提示。


第二个：

```tsx
const labelRef = useRef<HTMLLabelElement>(null);

<Label ref={labelRef} />
```

表示：

> props 的类型。

也就是说：

```tsx
const labelRef = useRef<HTMLLabelElement>(null);

<Label ref={labelRef} />
```

这些都是合法的。

如果写：

```tsx
const labelRef = useRef<HTMLLabelElement>(null);

<Label ref={labelRef} />
```

TS 就会报错。

---
## 六、为什么这里又写了 `<label ref={ref}>`
这一句就是 **真正完成转发**。

```tsx
const labelRef = useRef<HTMLLabelElement>(null);

<Label ref={labelRef} />
```

如果你删掉：

```tsx
<label ref={labelRef}></label>
```

变成：

```tsx
<label ref={labelRef}></label>
```

那么：

```tsx
<label ref={labelRef}></label>
```

虽然不会报错（因为用了 `forwardRef`），

但是：

```tsx
<label ref={labelRef}></label>
```

永远都是：

```tsx
<label ref={labelRef}></label>
```

因为你根本没有把它交给任何 DOM。

---
## 七、整个流程图
```tsx
<label ref={labelRef}></label>
```

所以：

```tsx
<label ref={labelRef}></label>
```

实际上就是：

```tsx
<label ref={labelRef}></label>
```

---
## 八、为什么很多组件库都这样写？
像 shadcn/ui、Radix UI 等组件库，大量组件都会采用这种模式：

```tsx
<label ref={labelRef}></label>
```

原因是：**让封装后的组件在使用体验上尽可能和原生元素一致**。

例如：

```tsx
<label ref={labelRef}></label>
```

虽然 `Input` 是你封装的组件，但父组件仍然可以直接拿到内部的 `<input>` DOM，进行聚焦、测量、滚动定位等操作。这也是很多可复用组件推荐使用 `forwardRef` 的原因。

---
## 具体实现
```tsx
<Label ref={labelRef} />
```