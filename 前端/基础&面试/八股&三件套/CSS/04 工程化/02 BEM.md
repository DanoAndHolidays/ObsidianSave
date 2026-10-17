BEM 是一种 CSS 命名和组织规范，包含三个部分：

- Block（块）：独立的组件，例如 `user-card`。
- Element（元素）：组件内部的组成部分，例如 `user-card__title`。
- Modifier（修饰符）：组件或元素的状态、变体，例如 `user-card--featured`。

---
## 命名规则
```css
.block {}
.block__element {}
.block--modifier {}
.block__element--modifier {}
```

示例：
```css
<div class="user-card user-card--featured">
  <h3 class="user-card__title">Dano</h3>
  <button class="user-card__button">Follow</button>
</div>
```

```css
.user-card {
  padding: 16px;
}

.user-card__title {
  font-size: 20px;
}

.user-card--featured {
  border: 1px solid gold;
}
```

Modifier 通常与基础类配合使用，而不是独立替代基础类。

---
### BEM 的设计原则

- 降低 DOM 结构耦合

```css
/* 推荐 */
.user-card__title {}

/* 不推荐：依赖具体 DOM 层级 */
.user-card > div > h3 {}
```

- 降低特指度（Specificity），BEM 通常使用单个 class 选择器，减少不必要的特指度竞争

```css
.page .content .user-card h3 {} /* 0-3-1 */

.user-card__title {}            /* 0-1-0 */
```

- BEM 不是真正的样式隔离，BEM 依靠命名约定减少冲突，但 CSS 仍然遵循全局选择器匹配和 Cascade（层叠）机制

### BEM 与 CSS Modules
在 React 项目中，如果已经使用 CSS Modules，通常不需要继续为所有类名添加 BEM 前缀
```css
/* UserCard.module.css */

.card {}
.title {}
.button {}
.featured {}
```

CSS Modules 会在构建时转换局部类名，减少不同模块之间的命名冲突
