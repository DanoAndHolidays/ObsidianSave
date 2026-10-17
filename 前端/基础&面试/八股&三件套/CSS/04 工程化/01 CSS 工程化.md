# CSS 工程化
CSS 工程化主要解决大型项目中样式的隔离、复用、维护和性能问题

传统 CSS 存在以下问题：

- 全局作用域：不同组件的 CSS 可能相互影响
- 命名冲突：多个组件可能使用相同的 class
- 层叠复杂：大量选择器容易产生 Specificity（特指度）竞争
- 维护困难：修改某个组件的样式，可能意外影响其他组件
- 性能问题：可能出现冗余样式、重复规则和不必要的运行时开销

需要注意：JavaScript 模块边界不等于 CSS 作用域边界
```
// UserCard.tsx
import "./UserCard.css";

// ProductCard.tsx
import "./ProductCard.css";
```

即使两个 CSS 文件分别导入，普通 CSS 类名仍可能匹配同一文档中的其他组件

常见工程化方案：

|方案|核心思想|
|---|---|
|BEM|通过命名规范减少冲突|
|CSS Modules|构建时转换类名，实现局部类名作用域|
|CSS-in-JS|使用 JavaScript 组织和生成样式|
|Tailwind CSS|Utility-first（工具类优先），通过组合工具类构建界面|

这些方案并不完全互斥，可以组合使用
