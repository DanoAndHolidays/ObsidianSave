# CSS Modules
CSS Modules 是一种==构建时== CSS 模块化方案，通过转换局部类名，减少不同组件之间的样式命名冲突

核心原理：构建时==类名转换== + ==JS 类名映射==
```css
/* Button.module.css */
.button {
  color: red;
}
```

```html
import styles from "./Button.module.css";

<button className={styles.button}>按钮</button>
```

构建工具可能生成：
```css
const styles = {
  button: "_button_a8d32_1"
};
```

同时把 CSS 选择器中的 `.button` 转换为 `._button_a8d32_1`

最终浏览器执行的仍然是普通 CSS，CSS Modules 不会改变浏览器的层叠和选择器匹配规则。

---
## 作用域
CSS Modules 默认会局部化类名、ID 和动画名称等，但不会隔离整个 DOM 子树

项目结构：
```
components/
├── Card/
│   ├── Card.jsx
│   └── Card.module.css
└── UserInfo/
    ├── UserInfo.jsx
    └── UserInfo.module.css
```

父组件 Card.jsx
```jsx
import styles from './Card.module.css';
import UserInfo from '../UserInfo/UserInfo';

export default function Card() {
  return (
    <div className={styles.card}>
      <h3>Card 标题</h3>
      <UserInfo />
    </div>
  );
}
```

子组件 UserInfo.jsx
```jsx
export default function UserInfo() {
  return (
    <div>
      <h3>用户信息标题</h3>
      <p>我是子组件</p>
    </div>
  );
}
```

父组件 Card.module.css
```css
.card h3 {
  color: red;
}
```

你可能希望只有 Card 自己的 `h3` 变红，而 UserInfo 中的 `h3` 不受影响

而 React 最终渲染出的 DOM 是：
```jsx
<div class="Card_card__a1b2c">
  <h3>Card 标题</h3>

  <div>
    <h3>用户信息标题</h3>
    <p>我是子组件</p>
  </div>
</div>
```

浏览器根本不知道哪个 DOM 元素属于哪个 React 组件

它只知道找到所有处于 `.Card_card__a1b2c` 元素内部的 `h3` 后代元素，并将它们设置为红色

### :global()
```css
/* 全局选择器 */
:global(.ant-modal) {
  border-radius: 12px;
}

/* 局部 + 全局组合 */
.container :global(.third-party-button) {
  margin-top: 12px;
}
```

`:global()` 是 CSS Modules 工具链提供的特殊语法，不是浏览器原生 CSS 伪类。

通常用于覆盖第三方组件的全局类名。注意 React Portal 可能导致目标元素不在局部容器的 DOM 后代中，使组合选择器失效。

---
## 样式变体与组合
### React 动态组合 class
```
.button {
  padding: 8px 16px;
}

.primary {
  background: blue;
}

.danger {
  background: red;
}
```

```
<button className={`${styles.button} ${styles[variant]}`}>
  按钮
</button>
```

基础类负责通用样式，变体类负责差异样式。

### composes 组合
```
.base {
  padding: 8px 16px;
}

.primary {
  composes: base;
  background: blue;
}
```

`styles.primary` 会同时包含 `primary` 和 `base` 对应的类名。

`composes` 不会复制 CSS 声明，而是组合类名。 属性冲突仍然由 CSS 层叠决定。

---
## CSS Modules 与 Shadow DOM

|对比|CSS Modules|Shadow DOM|
|---|---|---|
|实现机制|构建时转换类名|浏览器原生 DOM 封装|
|作用范围|局部名称映射|Shadow Tree|
|样式隔离|防止局部类名冲突|提供浏览器级样式边界|
|全局样式|仍可能影响组件|外部选择器通常无法直接匹配内部元素|
|常见场景|React 组件|Web Components|

注意：Shadow DOM 也不是完全隔离，继承属性、CSS 变量、`::part()` 等仍允许样式交互

- CSS Modules 不等于 DOM 隔离：父组件的元素选择器仍可能匹配子组件内部元素。

- CSS 变量不会自动局部化：自定义属性仍遵循正常的层叠和继承规则。

- 动画名称可以局部化：`@keyframes` 名称及其引用会被相应转换。

- TypeScript 类型检查取决于工具链：不一定能直接检测 `styles.titel` 等拼写错误。

- CSS 层叠仍然有效：CSS Modules 不会消除 Specificity、Inheritance 和 Cascade。


## React 项目组织实践
推荐组件样式就近放置：
```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   └── Button.module.css
│   └── UserCard/
│       ├── UserCard.tsx
│       └── UserCard.module.css
└── styles/
    ├── global.css
    ├── tokens.css
    └── reset.css
```

全局样式管理 Reset、主题变量和公共基础规则；CSS Modules 管理组件样式和局部变体。
