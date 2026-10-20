# CLS 累积布局偏移
[[Core Web Vitals 核心网页指标]]

**C**umulative **L**ayout **S**hift，累积布局偏移

**样式抖动（Layout Jank / CLS）** 的原因：

1. **异步加载的内容尺寸未知**：图片/广告/iframe 加载后撑开布局
2. **Web 字体加载后文本重排**：FOUT/FOIT
3. **动态注入内容**：JS 修改 DOM 导致重排
4. **动画使用了非合成属性**：改变 width/height/left/top 触发重排

**解决方案**：

- 图片设置 `width/height` 或 `aspect-ratio` 预留空间
- 字体使用 `font-display: fallback/optional`
- 动画使用 `transform`/`opacity`
- 使用 `will-change` 或 `transform: translateZ(0)` 创建合成层
