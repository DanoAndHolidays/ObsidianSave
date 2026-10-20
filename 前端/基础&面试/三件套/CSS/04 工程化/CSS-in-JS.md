styled-components 是 React 生态中非常经典的 CSS-in-JS 样式方案。

简单来说，它允许你在 JavaScript / TypeScript 文件中编写 CSS，并将这些样式封装成 React 组件。

你之前学过 CSS Modules，可以把 styled-components 理解为另一种解决组件样式管理问题的技术。

---
## 使用
先安装：
```sh
npm install styled-components
```

来看一个 React + TypeScript 的例子：
```tsx
import styled from "styled-components";

// 定义带样式的 React 组件
const Button = styled.button`
  padding: 10px 20px;
  background-color: #1677ff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;

  &:hover {
    background-color: #4096ff;
  }
`;

export default function App() {
  return <Button>点击按钮</Button>;
}
```

这里需要理解三个知识点：

- `styled.button`：创建一个带有样式的 React 组件，最终渲染为原生 `<button>`。

- 反引号 `` `...` ``：使用 JavaScript 的标签模板字面量（Tagged Template Literal），向 `styled` 传入 CSS。

- `&:hover`：表示当前组件生成的 CSS 类的悬停伪类。

注意：styled-components 并不是直接将样式写入 HTML 的 `style` 属性，而是生成 CSS 规则和对应的 className

---
## 和 CSS Modules 的区别
假设我们需要实现一个按钮

CSS Modules
```tsx
import styles from "./Button.module.css";

function Button() {
  return (
    <button className={styles.button}>
      点击按钮
    </button>
  );
}
```

```css
/* Button.module.css */
.button {
  background: #1677ff;
  color: white;
}
```

styled-components
```tsx
import styled from "styled-components";

const Button = styled.button`
  background: #1677ff;
  color: white;
`;

function App() {
  return <Button>点击按钮</Button>;
}
```

对比一下：

|特性|CSS Modules|styled-components|
|---|---|---|
|技术分类|CSS Modules|CSS-in-JS|
|样式编写|独立 CSS 文件|JS/TS 文件|
|样式隔离|编译时类名转换|自动生成类名|
|动态样式|切换类名、CSS 变量|直接使用 Props|
|运行时开销|通常较小|通常有额外开销|
|主题支持|CSS 变量等|ThemeProvider|

---
## 动态样式
假设我们要实现两种按钮：主按钮是蓝色，危险按钮是红色
```tsx
import styled from "styled-components";

interface ButtonProps {
  $danger?: boolean;
}

const Button = styled.button<ButtonProps>`
  padding: 10px 20px;
  color: white;

  background: ${(props) => props.$danger ? "red" : "blue"};
`;

export default function App() {
  return (
    <>
      <Button>普通按钮</Button>
      <Button $danger>危险按钮</Button>
    </>
  );
}
```

这里的核心是：
```tsx
background: ${(props) => props.$danger ? "red" : "blue"};
```

通过 JavaScript 表达式，根据 React Props 动态决定样式。

另外，`$danger` 前面的 `$` 是 styled-components 的 Transient Props 机制，表示这是仅供样式使用的属性，不需要透传给真实 DOM

---
## 底层原理
- 可以把它的工作过程理解成：
	
	- 编写 styled.button 模板
	
	- 解析 CSS 和动态 Props
	
	- 生成 CSS `.abc123 { ... }`
	
	- 生成 className `class="abc123"`
	
	- 浏览器应用 CSS 样式


- 它与 CSS Modules 最核心的底层区别在于：
	
	- CSS Modules 主要在构建阶段转换类名，输出 CSS。
	
	- styled-components 通常在运行时根据组件和 Props 生成、缓存并注入 CSS 规则（也支持 SSR 样式收集）。


这也解释了为什么 styled-components 通常==存在额外的运行时==成本。


优点：

- 组件和样式放在一起，方便封装和维护。

- 自动生成类名，减少样式命名冲突。

- 与 React Props 结合方便。

- 支持主题系统、样式继承、伪类、媒体查询等。


缺点：

- 存在额外的 JavaScript 运行时成本。

- 频繁变化的动态样式可能产生大量 CSS 规则。

- SSR、React Server Components 等环境需要关注兼容和配置问题。

- 过度封装可能导致组件层级复杂。

还有一个常见注意点：不要在 React 函数组件内部定义 styled-components，否则每次渲染都可能重新创建组件，影响性能。
