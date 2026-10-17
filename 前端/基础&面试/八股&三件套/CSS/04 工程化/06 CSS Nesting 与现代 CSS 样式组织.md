# CSS Nesting 与现代 CSS 样式组织


---
## CSS Nesting
CSS Nesting 是浏览器原生支持的 CSS 嵌套语法，可以减少重复选择器，让组件相关样式集中组织，不再需要依赖 Sass   萨斯实现基础嵌套。

```
.card {
  padding: 16px;

  .title {
    font-size: 20px;
  }

  .button {
    background: blue;

    &:hover {
      background: darkblue;
    }
  }
}
```

其中 `&` 表示当前嵌套规则关联的父级选择器。

|写法|含义|
|---|---|
|`& .title`|后代选择器|
|`& > .title`|直接子元素|
|`&:hover`|当前元素的 hover 状态|
|`&.active`|当前元素同时具有 active   活跃类|
|`& + .item`|相邻兄弟选择器|

注意：原生 CSS Nesting 与 Sass   萨斯不完全相同。

原生 CSS 不支持通过 `&__title` 拼接 BEM 类名，而 Sass 支持。

### 嵌套对 Specificity 的影响
CSS Nesting 对父级选择器列表的特指度处理类似于 `:is()`，采用列表中最高的特指度。
```
#app,
.card {
  .title {
    color: red;
  }
}
```

可以近似理解为：

```
:is(#app, .card) .title {
  color: red;
}
```

最终特指度为 `1-1-0`，即使实际匹配的是 `.card`。

因此不建议过度嵌套，否则容易增加 Specificity 和 DOM 结构耦合。

### 嵌套媒体查询
```
.card {
  display: grid;
  grid-template-columns: 1fr;

  @media (width >= 48rem) {
    grid-template-columns: repeat(2, 1fr);
  }

  @container (width >= 400px) {
    gap: 24px;
  }
}
```

可以将组件的基础样式、响应式样式集中维护。

---
## @layer
`@layer`（层叠层）用于明确不同类型样式之间的优先级，减少依赖 Specificity 和文件顺序进行覆盖的情况。

### 声明层叠顺序
```
@layer reset, base, components, utilities;
```

```
@layer reset {
  * {
    box-sizing: border-box;
  }
}

@layer components {
  .button {
    background: blue;
  }
}

@layer utilities {
  .bg-red {
    background: red;
  }
}
```

对于同一来源的普通声明：

reset < base < components < utilities  
重置<基<组件<工具

即后声明的层优先级更高。

### 核心规则

- 层叠层的优先级比较发生在 Specificity 之前。

- 同一来源的普通声明中，后声明的层优先级更高。

- 未分层的普通声明优先于所有已分层的普通声明。

- 对于 `!important` 声明，层叠层的优先级顺序反转，前面的层反而更高；已分层的重要声明也优先于未分层的重要声明。

```
@layer components {
  #app .button {
    background: blue;
  }
}

@layer utilities {
  .bg-red {
    background: red;
  }
}
```

即使 `#app .button` 特指度更高，如果元素同时匹配两个选择器，普通声明中依然是 `utilities` 层的红色生效。

核心作用：将大型项目的样式优先级管理从 Specificity 竞争转变为明确的 Layer 顺序。

---
## @scope
`@scope` 是浏览器原生提供的作用域规则，可以将选择器限制在指定的 DOM 范围内。

```
@scope (.user-card) {
  .title {
    color: blue;
  }
}
```

`.title` 只在指定的 `.user-card` 作用范围内匹配。

### 设置作用域边界
```
@scope (.article) to (.comments) {
  p {
    line-height: 1.8;
  }
}
```

- `.article`：作用域根。
- `.comments`：作用域下限。


规则不会继续匹配下限元素及其后代。

这种结构也称为 Donut Scope（甜甜圈作用域）。

`@scope` 还会参与 Scoping Proximity（作用域接近度）的层叠比较。

注意：`@scope` 不等于 Shadow DOM，它只是限制选择器匹配范围，并不会完全隔离继承、层叠或外部样式。
