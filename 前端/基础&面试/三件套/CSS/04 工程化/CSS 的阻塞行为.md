# CSS 的阻塞行为

CSS 加载会阻塞 DOM 树的解析和渲染吗

- **CSS 不会阻塞 DOM 解析**：HTML 解析和 CSS 加载并行进行，但 DOM 构建完不会立刻渲染——必须等 CSSOM 完成（CSS 是渲染阻塞资源）
- **CSS 会阻塞页面渲染**：浏览器必须构建 CSSOM 树才能渲染，未加载完 CSS 会"白屏"
- **CSS 会阻塞 JS 执行**：JS 可能查询样式，所以必须等 CSSOM 构建完才执行 JS
- **结论**：CSS 放在 head 中、提取首屏关键 CSS 内联、异步加载非关键 CSS（media 属性欺骗法）