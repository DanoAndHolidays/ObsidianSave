# Media Queries

媒体查询允许根据视口尺寸、设备特征和用户偏好应用不同样式

---
## 视口尺寸查询
```css
/* 默认单列 */
.layout {
  display: grid;
  grid-template-columns: 1fr;
}

/* 宽视口下双列 */
@media (width >= 1024px) {
  .layout {
    grid-template-columns: minmax(0, 1fr) 280px;
  }
}
```

也支持范围语法：
```css
@media (600px <= width < 1024px) {
  /* 600px ≤ 视口宽度 < 1024px */
}
```

---
## 用户偏好查询
```css
@media (prefers-reduced-motion: reduce) {
  .animated {
    animation: none;
    transition: none;
  }
}
```

可以根据用户系统设置减少非必要动画

---
## 断点 Breakpoint
断点是触发布局规则变化的临界尺寸

- 不应该机械地将 768px 当作平板、1024px 当作电脑

- 应根据内容在什么宽度下==无法保持合理布局==来选择断点

- 常用[[Mobile First⌚️]]策略：先定义适用于窄视口的基础样式，再使用 `min-width` 或范围查询逐步增强
