`css specificity` 即 css 中关于选择器的权重，以下类型的选择器依次下降

1. 内联样式 `<div class="foo" style="color: red;"></div>` 及 `!important`(最高) 具有更高的权重1000
2. `id` 选择器，如 `#app` ，权重100
3. `class`、`attribute` 与 `pseudo-classes（伪类）` 选择器，如 `.header`、`[type="radio"]` 与 `:hover`，权重10
4. 元素选择器和伪元素选择器，如 `h1`、`p` 和 `::before`，权重1
5. 通配符选择器 `*`，组合选择器 `+ ~ >`，否定伪类选择器 `:not()` ，权重0

###  样式重复
---
BEM 式: `.home-page .home-page-btn`

```
.home-page {  .home-page-btn {  }}
```