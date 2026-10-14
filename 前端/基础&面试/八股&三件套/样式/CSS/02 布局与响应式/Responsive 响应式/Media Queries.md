# Media Queries

---
## 响应式设计的核心模型
响应式设计（Responsive Web Design）是让布局根据可用空间和用户环境调整，而不是简单地将页面按比例缩小

常见三个层次：

|机制|作用|
|---|---|
|Flex / Grid / 内在尺寸|根据可用空间自然伸缩、换行|
|Media Queries|根据视口、用户偏好等媒体条件调整样式|
|Container Queries|根据祖先查询容器的尺寸调整组件布局|

原则：**优先利用布局系统的自适应能力，需要切换布局规则时，再使用条件查询。**

---
## Media Queries 媒体查询
媒体查询允许根据视口尺寸、设备特征和用户偏好应用不同样式

### 视口尺寸查询
```
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
```
@media (600px <= width < 1024px) {
  /* 600px ≤ 视口宽度 < 1024px */
}
```

### 用户偏好查询
```
@media (prefers-reduced-motion: reduce) {
  .animated {
    animation: none;
    transition: none;
  }
}
```

可以根据用户系统设置减少非必要动画

### 断点 Breakpoint
断点是触发布局规则变化的临界尺寸

- 不应该机械地将 768px 当作平板、1024px 当作电脑

- 应根据内容在什么宽度下==无法保持合理布局==来选择断点

- 常用[[Mobile First 移动端优先 ⌚️]]策略：先定义适用于窄视口的基础样式，再使用 `min-width` 或范围查询逐步增强
