
## 先建立一个整体认识

这两个 API 都和 `ref` 有关：

* `forwardRef`：**让父组件传入的 ref，穿过当前组件，绑定到内部元素上。**
* `useImperativeHandle`：**自定义父组件通过 ref 能拿到什么。**

可以先把它们理解成：

```text
父组件
  │
  │ ref
  ▼
自定义组件 Button
  │
  │ forwardRef 转发
  ▼
内部真实的 <button>
```

而 `useImperativeHandle` 会在中间加一层“接口包装”：

```text
父组件
  │
  │ ref.current
  ▼
自定义的方法对象
{
  focus(),
  click(),
  shake()
}
  │
  ▼
内部真实 DOM
```

---

# 一、ref 本身是什么

在 React 中，`ref` 通常用来保存一个对象或引用，并且修改它不会触发重新渲染。

例如获取一个真实的 `<button>` DOM：

```tsx
import { useRef } from "react";

export function App() {
  const buttonRef = useRef<HTMLButtonElement>(null);

  const handleClick = () => {
    console.log(buttonRef.current);

    buttonRef.current?.focus();
  };

  return (
    <>
      <button ref={buttonRef}>保存</button>
      <button onClick={handleClick}>让保存按钮获得焦点</button>
    </>
  );
}
```

组件挂载以后：

```ts
buttonRef.current
```

大致就是这个真实 DOM：

```html
<button>保存</button>
```

因此可以调用浏览器提供的 DOM 方法：

```ts
buttonRef.current?.focus();
buttonRef.current?.click();
buttonRef.current?.scrollIntoView();
buttonRef.current?.getBoundingClientRect();
```

React 会在 DOM 节点创建后将它放入 `ref.current`，节点卸载时通常会重新设为 `null`。([React][1])

---

# 二、为什么自定义组件需要 forwardRef

直接给原生元素传 `ref` 很简单：

```tsx
<button ref={buttonRef}>按钮</button>
```

但你的 `Button` 是自定义组件：

```tsx
<Button ref={buttonRef}>按钮</Button>
```

在 React 18 以及更早版本中，普通函数组件不能像普通 props 那样直接接收这个特殊的 `ref`：

```tsx
// React 18 下不能这样接收 ref
function Button(props) {
  return <button />;
}
```

因为父组件写下：

```tsx
<Button ref={buttonRef} />
```

父组件真正想引用的通常不是 `Button` 这个函数，而是 `Button` 内部最终渲染出来的真实 `<button>`。

所以需要 `forwardRef` 把它转发进去。

---

# 三、你代码里的 forwardRef

你的代码：

```tsx
export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      asChild = false,
      className,
      variant = "default",
      size = "default",
      ...props
    },
    ref,
  ) => {
    const ButtonPrimitive = asChild ? Slot : "button";

    return (
      <ButtonPrimitive
        {...props}
        ref={ref}
        className={cn(
          "...",
          variants[variant],
          sizes[size],
          className,
        )}
      />
    );
  },
);
```

重点是：

```tsx
forwardRef<HTMLButtonElement, ButtonProps>
```

它有两个泛型参数。

## 第一个参数：`HTMLButtonElement`

```tsx
forwardRef<HTMLButtonElement, ButtonProps>
```

表示这个组件对外暴露的 `ref`，正常情况下指向一个 `<button>` DOM。

所以父组件可以这样写：

```tsx
const buttonRef = useRef<HTMLButtonElement>(null);
```

并调用：

```tsx
buttonRef.current?.focus();
buttonRef.current?.click();
```

## 第二个参数：`ButtonProps`

表示组件接收的 props 类型：

```tsx
interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  asChild?: boolean;
  variant?: keyof typeof variants;
  size?: keyof typeof sizes;
}
```

所以整个表达式可以理解为：

```tsx
forwardRef<
  ref最终指向的类型,
  组件props的类型
>
```

也就是：

```tsx
forwardRef<HTMLButtonElement, ButtonProps>
```

---

# 四、forwardRef 的回调为什么有两个参数

普通函数组件通常只有一个参数：

```tsx
function Button(props) {
  return <button />;
}
```

经过 `forwardRef` 包装后，渲染函数有两个参数：

```tsx
forwardRef((props, ref) => {
  return <button ref={ref} />;
});
```

分别是：

```tsx
(props, ref)
```

### `props`

普通组件属性：

```tsx
<Button
  className="..."
  variant="outline"
  disabled
>
  保存
</Button>
```

这些都会进入 `props`。

### `ref`

父组件传进来的引用：

```tsx
<Button ref={buttonRef}>保存</Button>
```

这里的：

```tsx
buttonRef
```

就会成为 `forwardRef` 回调中的第二个参数：

```tsx
(props, ref) => {
  // ref 就是父组件的 buttonRef
}
```

官方定义也是：`forwardRef` 接收一个渲染函数，React 使用 `props` 和 `ref` 调用它；返回的组件可以接收 `ref`。([React][2])

---

# 五、ref 是怎么穿过你的 Button 的

父组件：

```tsx
import { useRef } from "react";
import { Button } from "./Button";

export function Page() {
  const buttonRef = useRef<HTMLButtonElement>(null);

  return (
    <>
      <Button ref={buttonRef}>
        提交
      </Button>

      <button
        onClick={() => {
          buttonRef.current?.focus();
        }}
      >
        聚焦提交按钮
      </button>
    </>
  );
}
```

传递过程如下。

## 第一步：父组件传入

```tsx
<Button ref={buttonRef}>
  提交
</Button>
```

## 第二步：forwardRef 接收到

```tsx
export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (props, ref) => {
    // 这里的 ref 就是父组件中的 buttonRef
  },
);
```

## 第三步：传给内部元素

```tsx
return <button {...props} ref={ref} />;
```

## 第四步：真实 DOM 写入 current

最终：

```ts
buttonRef.current
```

就是内部真实的：

```html
<button>提交</button>
```

因此调用：

```ts
buttonRef.current?.focus();
```

就是在调用真实按钮 DOM 的 `focus()`。

---

# 六、没有 forwardRef 会怎么样

例如：

```tsx
interface ButtonProps {
  children: React.ReactNode;
}

function Button({ children }: ButtonProps) {
  return <button>{children}</button>;
}
```

父组件希望这样使用：

```tsx
const buttonRef = useRef<HTMLButtonElement>(null);

<Button ref={buttonRef}>保存</Button>
```

在 React 18 的组件写法里，普通函数组件没有把 `ref` 接收下来，更没有把它传给内部的 `<button>`。

所以父组件无法拿到内部按钮。

使用 `forwardRef` 后：

```tsx
const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ children }, ref) => {
    return <button ref={ref}>{children}</button>;
  },
);
```

这时才建立了完整链路。

---

# 七、你的 `asChild` 和 ref

你的代码里有：

```tsx
const ButtonPrimitive = asChild ? Slot : "button";
```

当：

```tsx
asChild={false}
```

最终渲染：

```tsx
<button ref={ref} />
```

此时 `ref.current` 是：

```ts
HTMLButtonElement
```

但当：

```tsx
<Button asChild>
  <a href="/home">首页</a>
</Button>
```

`Slot` 会把 Button 的属性合并到这个 `<a>` 上。

最终真实元素更接近：

```tsx
<a href="/home" className="...">
  首页
</a>
```

这时 `ref` 实际可能指向：

```ts
HTMLAnchorElement
```

而你目前声明的是：

```tsx
forwardRef<HTMLButtonElement, ButtonProps>
```

类型上仍然告诉 TypeScript：

```ts
ref.current 是 HTMLButtonElement
```

这存在一定的类型不准确问题。

例如：

```tsx
const ref = useRef<HTMLButtonElement>(null);

<Button asChild ref={ref}>
  <a href="/home">首页</a>
</Button>
```

运行时的元素是 `<a>`，但 TypeScript 认为它是 `<button>`。

对于简单 UI 组件库，这种写法比较常见；如果要做到严格类型安全，就需要实现更复杂的多态组件类型。这里不影响理解 `forwardRef` 的核心作用：**它仍然负责把 ref 传到最终的真实元素上。**

---

# 八、`Button.displayName` 是什么

你后面写了：

```tsx
Button.displayName = "Button";
```

因为组件经过：

```tsx
forwardRef(...)
```

包装后，在 React DevTools 或错误信息中，组件名称有时不够直观。

设置：

```tsx
Button.displayName = "Button";
```

可以让开发工具更明确地显示组件名称。

它不影响组件功能，只影响调试体验。

---

# 九、React 19 中 forwardRef 的变化

需要注意版本差异。

从 React 19 开始，函数组件可以直接把 `ref` 当作 prop 接收，新组件不再必须使用 `forwardRef`；React 官方也表示 `forwardRef` 计划在未来版本中废弃。([React][3])

React 19 可以写成类似：

```tsx
interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  ref?: React.Ref<HTMLButtonElement>;
}

export function Button({
  ref,
  children,
  ...props
}: ButtonProps) {
  return (
    <button ref={ref} {...props}>
      {children}
    </button>
  );
}
```

但目前很多组件库仍然需要兼容 React 18，因此依旧大量使用：

```tsx
forwardRef(...)
```

所以你项目中的写法完全正常，而且是常见的兼容写法。

---

# 十、useImperativeHandle 是做什么的

`useImperativeHandle` 的作用是：

> 自定义父组件通过 `ref.current` 能拿到的内容。

默认情况下，你把 ref 直接传给 DOM：

```tsx
<input ref={ref} />
```

父组件拿到的是完整的 `HTMLInputElement`：

```ts
ref.current?.focus();
ref.current?.select();
ref.current?.blur();
ref.current?.style.setProperty(...);
```

但是有时候你不想把整个 DOM 暴露出去，只希望父组件能调用几个特定能力：

```ts
ref.current?.focus();
ref.current?.clear();
```

这时可以使用：

```tsx
useImperativeHandle(ref, () => ({
  focus() {},
  clear() {},
}));
```

官方将它定义为“自定义通过 ref 暴露的句柄”。([React][4])

---

# 十一、先看一个不使用 useImperativeHandle 的例子

```tsx
import { forwardRef } from "react";

interface InputProps {
  placeholder?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ placeholder }, ref) => {
    return (
      <input
        ref={ref}
        placeholder={placeholder}
      />
    );
  },
);
```

父组件：

```tsx
import { useRef } from "react";

export function Form() {
  const inputRef = useRef<HTMLInputElement>(null);

  return (
    <>
      <Input
        ref={inputRef}
        placeholder="请输入用户名"
      />

      <button
        onClick={() => {
          inputRef.current?.focus();
        }}
      >
        聚焦输入框
      </button>
    </>
  );
}
```

此时：

```ts
inputRef.current
```

就是完整的 `HTMLInputElement`。

父组件可以直接操作 DOM：

```tsx
inputRef.current?.focus();

if (inputRef.current) {
  inputRef.current.value = "";
}
```

---

# 十二、使用 useImperativeHandle 自定义能力

现在我们不希望父组件直接操作：

```ts
inputRef.current.value
```

而是希望它调用：

```ts
inputRef.current.clear();
inputRef.current.focus();
```

首先定义对外暴露的接口：

```tsx
export interface InputHandle {
  focus: () => void;
  clear: () => void;
  select: () => void;
}
```

然后实现组件：

```tsx
import {
  forwardRef,
  useImperativeHandle,
  useRef,
} from "react";

interface InputProps {
  placeholder?: string;
}

export interface InputHandle {
  focus: () => void;
  clear: () => void;
  select: () => void;
}

export const Input = forwardRef<InputHandle, InputProps>(
  ({ placeholder }, ref) => {
    const internalInputRef =
      useRef<HTMLInputElement>(null);

    useImperativeHandle(
      ref,
      () => ({
        focus() {
          internalInputRef.current?.focus();
        },

        clear() {
          if (internalInputRef.current) {
            internalInputRef.current.value = "";
          }
        },

        select() {
          internalInputRef.current?.select();
        },
      }),
      [],
    );

    return (
      <input
        ref={internalInputRef}
        placeholder={placeholder}
      />
    );
  },
);

Input.displayName = "Input";
```

父组件：

```tsx
import { useRef } from "react";
import {
  Input,
  type InputHandle,
} from "./Input";

export function Form() {
  const inputRef = useRef<InputHandle>(null);

  return (
    <>
      <Input
        ref={inputRef}
        placeholder="请输入用户名"
      />

      <button
        onClick={() => {
          inputRef.current?.focus();
        }}
      >
        聚焦
      </button>

      <button
        onClick={() => {
          inputRef.current?.clear();
        }}
      >
        清空
      </button>

      <button
        onClick={() => {
          inputRef.current?.select();
        }}
      >
        全选
      </button>
    </>
  );
}
```

注意，现在父组件中的 ref 类型变成了：

```tsx
useRef<InputHandle>(null)
```

而不再是：

```tsx
useRef<HTMLInputElement>(null)
```

因为父组件拿到的不再是 DOM，而是我们自定义的对象：

```ts
{
  focus() {},
  clear() {},
  select() {}
}
```

---

# 十三、这里为什么需要两个 ref

在刚才的例子中：

```tsx
export const Input = forwardRef<InputHandle, InputProps>(
  (props, ref) => {
    const internalInputRef =
      useRef<HTMLInputElement>(null);
  },
);
```

有两个 ref。

## 外部 ref

```tsx
ref
```

它来自父组件：

```tsx
<Input ref={inputRef} />
```

父组件最终通过它调用：

```tsx
inputRef.current?.clear();
```

## 内部 ref

```tsx
internalInputRef
```

它指向真正的 `<input>`：

```tsx
<input ref={internalInputRef} />
```

内部方法通过它操作真实 DOM：

```tsx
internalInputRef.current?.focus();
```

完整关系是：

```text
父组件的 inputRef
        │
        │ ref
        ▼
useImperativeHandle
        │
        ▼
{
  focus(),
  clear(),
  select()
}
        │
        │ 内部调用
        ▼
internalInputRef
        │
        ▼
真实的 <input>
```

---

# 十四、useImperativeHandle 的三个参数

基本语法：

```tsx
useImperativeHandle(
  ref,
  createHandle,
  dependencies,
);
```

官方 API 也是：

```tsx
useImperativeHandle(ref, createHandle, dependencies?)
```

并且这个 Hook 本身返回 `undefined`。([React][4])

## 第一个参数：`ref`

父组件传入的 ref：

```tsx
useImperativeHandle(ref, ...)
```

## 第二个参数：创建暴露对象的函数

```tsx
() => ({
  focus() {
    internalInputRef.current?.focus();
  },

  clear() {
    // ...
  },
})
```

这个函数返回什么，父组件的：

```ts
ref.current
```

就是什么。

例如：

```tsx
useImperativeHandle(ref, () => ({
  name: "Dano",
  focus() {},
}));
```

那么父组件获得：

```ts
ref.current?.name;
ref.current?.focus();
```

## 第三个参数：依赖数组

```tsx
[]
```

作用和 `useMemo`、`useEffect` 的依赖数组相似。

例如：

```tsx
useImperativeHandle(
  ref,
  () => ({
    printValue() {
      console.log(value);
    },
  }),
  [value],
);
```

当 `value` 改变时，React 会重新创建暴露给父组件的对象。

如果内部方法使用了某个会变化的 props 或 state，就应该把它加入依赖数组。

---

# 十五、依赖数组的实际例子

```tsx
interface CounterHandle {
  getCount: () => number;
  reset: () => void;
}

interface CounterProps {
  initialValue?: number;
}

const Counter = forwardRef<CounterHandle, CounterProps>(
  ({ initialValue = 0 }, ref) => {
    const [count, setCount] = useState(initialValue);

    useImperativeHandle(
      ref,
      () => ({
        getCount() {
          return count;
        },

        reset() {
          setCount(initialValue);
        },
      }),
      [count, initialValue],
    );

    return (
      <button onClick={() => setCount((n) => n + 1)}>
        当前数量：{count}
      </button>
    );
  },
);
```

这里暴露的方法使用了：

```tsx
count
initialValue
```

所以依赖数组需要写：

```tsx
[count, initialValue]
```

否则方法可能闭包住旧值，产生“父组件调用后得到过期数据”的问题。

不过这种“通过 ref 获取 React 状态”的设计通常不是首选。状态最好通过 props、回调或状态提升来传递，这里主要用来演示依赖关系。

---

# 十六、forwardRef 和 useImperativeHandle 的区别

这是最重要的区别。

## 只有 forwardRef

```tsx
const Input = forwardRef<HTMLInputElement, InputProps>(
  (props, ref) => {
    return <input ref={ref} />;
  },
);
```

父组件拿到的是：

```ts
HTMLInputElement
```

也就是整个 DOM 节点。

```ts
ref.current?.focus();
ref.current?.select();
ref.current?.blur();
```

## forwardRef 加 useImperativeHandle

```tsx
const Input = forwardRef<InputHandle, InputProps>(
  (props, ref) => {
    const inputRef = useRef<HTMLInputElement>(null);

    useImperativeHandle(ref, () => ({
      focus() {
        inputRef.current?.focus();
      },
    }), []);

    return <input ref={inputRef} />;
  },
);
```

父组件拿到的是：

```ts
InputHandle
```

只有你主动暴露的方法：

```ts
ref.current?.focus();
```

不能再直接访问：

```ts
ref.current?.style;
ref.current?.value;
```

因为你没有把这些东西暴露出去。

可以记成一句话：

> `forwardRef` 决定 ref 能不能传进来，`useImperativeHandle` 决定传进来以后，父组件最终拿到什么。

---

# 十七、Button 需要 useImperativeHandle 吗

你目前的 Button：

```tsx
<Button ref={buttonRef} />
```

父组件拿到原生按钮 DOM 已经很好用了：

```tsx
buttonRef.current?.focus();
buttonRef.current?.click();
buttonRef.current?.scrollIntoView();
```

因此一般没必要使用 `useImperativeHandle`。

也就是说，你当前这样就够了：

```tsx
<ButtonPrimitive ref={ref} />
```

只有当你希望 Button 暴露一些自定义操作时，才需要它。

例如暴露一个动画方法：

```tsx
export interface ButtonHandle {
  focus: () => void;
  shake: () => void;
}
```

组件：

```tsx
import {
  forwardRef,
  useImperativeHandle,
  useRef,
} from "react";

interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: keyof typeof variants;
  size?: keyof typeof sizes;
}

export interface ButtonHandle {
  focus: () => void;
  shake: () => void;
}

export const Button = forwardRef<
  ButtonHandle,
  ButtonProps
>(
  (
    {
      className,
      variant = "default",
      size = "default",
      ...props
    },
    ref,
  ) => {
    const buttonRef =
      useRef<HTMLButtonElement>(null);

    useImperativeHandle(
      ref,
      () => ({
        focus() {
          buttonRef.current?.focus();
        },

        shake() {
          const button = buttonRef.current;
          if (!button) return;

          button.animate(
            [
              { transform: "translateX(0)" },
              { transform: "translateX(-5px)" },
              { transform: "translateX(5px)" },
              { transform: "translateX(0)" },
            ],
            {
              duration: 200,
            },
          );
        },
      }),
      [],
    );

    return (
      <button
        {...props}
        ref={buttonRef}
        className={cn(
          "inline-flex items-center justify-center",
          variants[variant],
          sizes[size],
          className,
        )}
      />
    );
  },
);
```

父组件：

```tsx
export function Page() {
  const buttonRef = useRef<ButtonHandle>(null);

  return (
    <>
      <Button ref={buttonRef}>
        提交
      </Button>

      <button
        onClick={() => {
          buttonRef.current?.shake();
        }}
      >
        让提交按钮晃动
      </button>
    </>
  );
}
```

---

# 十八、什么时候适合用 useImperativeHandle

比较适合的场景是那些必须“命令式执行”的行为：

```tsx
ref.current?.focus();
ref.current?.scrollToTop();
ref.current?.selectAll();
ref.current?.play();
ref.current?.pause();
ref.current?.resetCanvas();
ref.current?.startAnimation();
```

例如：

* 聚焦输入框
* 滚动到某个节点
* 选中文字
* 控制音频、视频
* 控制 Canvas
* 对接第三方非 React 组件
* 触发一次动画
* 暴露富文本编辑器的命令

React 官方也建议不要过度使用 ref；它更适合聚焦、滚动、动画、文本选择等无法自然表达成 props 的命令式行为。([React][2])

---

# 十九、什么时候不应该用 useImperativeHandle

假设有一个弹窗，你可能想写：

```tsx
modalRef.current?.open();
modalRef.current?.close();
```

但在 React 中，通常更推荐通过状态控制：

```tsx
<Modal open={open} onOpenChange={setOpen} />
```

而不是：

```tsx
<Modal ref={modalRef} />

modalRef.current?.open();
```

因为第一种是声明式的：

```tsx
open={true}
```

表示“弹窗现在应该打开”。

第二种是命令式的：

```tsx
modalRef.current.open()
```

表示“立刻执行打开操作”。

对于 UI 状态，优先使用 props 和 state；对于聚焦、滚动、播放动画等一次性动作，再使用 ref。官方文档也明确建议：能够用 prop 表达的状态，通常不要改成命令式 ref 接口。([React][2])

---

# 二十、最终记忆方式

## `forwardRef`

作用：

```text
把父组件的 ref 转发给组件内部的 DOM 或子组件
```

典型写法：

```tsx
const Button = forwardRef<
  HTMLButtonElement,
  ButtonProps
>((props, ref) => {
  return <button {...props} ref={ref} />;
});
```

父组件拿到：

```ts
HTMLButtonElement
```

---

## `useImperativeHandle`

作用：

```text
自定义父组件通过 ref.current 能调用的内容
```

典型写法：

```tsx
useImperativeHandle(ref, () => ({
  focus() {
    internalRef.current?.focus();
  },
  clear() {
    // ...
  },
}), []);
```

父组件拿到：

```ts
{
  focus(),
  clear()
}
```

---

## 二者组合关系

```tsx
const Component = forwardRef<Handle, Props>(
  (props, ref) => {
    const internalRef = useRef<HTMLElement>(null);

    useImperativeHandle(ref, () => ({
      someMethod() {
        // 操作 internalRef
      },
    }), []);

    return <div ref={internalRef} />;
  },
);
```

一句话总结：

```text
forwardRef：把 ref 接进来。

useImperativeHandle：规定 ref.current 暴露什么。
```

[1]: https://react.dev/reference/react/useRef?utm_source=chatgpt.com "useRef – React"
[2]: https://react.dev/reference/react/forwardRef?utm_source=chatgpt.com "forwardRef – React"
[3]: https://react.dev/blog/2024/12/05/react-19?utm_source=chatgpt.com "React v19 – React"
[4]: https://react.dev/reference/react/useImperativeHandle?utm_source=chatgpt.com "useImperativeHandle – React"
