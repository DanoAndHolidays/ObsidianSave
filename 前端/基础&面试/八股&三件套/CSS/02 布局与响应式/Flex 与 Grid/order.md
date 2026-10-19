# order
`order` 属性改变 flex 子元素在主轴上的**视觉排列顺序**。默认值为 0，值越小越靠前（可为负数）。仅改变视觉顺序，不改变 DOM 结构和文档流。不影响屏幕阅读器（朗读顺序仍按 DOM）

```css
.item:first-child { order: 1; }  /* 移到后面 */
.item:last-child  { order: -1; } /* 移到前面 */
```
