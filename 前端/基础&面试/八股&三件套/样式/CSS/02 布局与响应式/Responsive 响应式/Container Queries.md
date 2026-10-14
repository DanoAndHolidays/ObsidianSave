# Container Queries
允许 CSS 根据祖先查询容器的尺寸等条件，为后代元素应用不同样式，

与媒体查询（Media Queries）的区别：

|对比|Media Queries|Container Queries|
|---|---|---|
|查询对象|视口、设备特征、用户偏好等|符合条件的祖先查询容器|
|主要用途|页面级响应式|组件级响应式|
|典型场景|页面断点、整体布局切换|卡片、侧边栏、可复用组件|

---
## 基本使用
容器尺寸查询分为两个步骤：

1. 使用 `container-type` 声明查询容器
2. 使用 `@container` 根据容器尺寸调整后代样式

```css
.wrapper {
  container-type: inline-size;
}

.card {
  display: flex;
  flex-direction: column;
}

/* 根据祖先查询容器的宽度切换布局 */
@container (width >= 400px) {
  .card {
    flex-direction: row;
  }
}
```

### container-type

|值|含义|
|---|---|
|`normal`|默认值，不建立尺寸查询容器，但仍支持部分其他容器查询|
|`inline-size`|支持行内轴尺寸查询|
|`size`|支持行内轴和块轴尺寸查询|

- `inline-size` 在普通水平书写模式下对应宽度。

- `size` 还允许查询高度，但两个轴都会受到尺寸约束，可能影响内容驱动的尺寸计算。

- **通常优先使用** `container-type: inline-size`**。

尺寸约束（Size Containment）用于避免子元素样式影响容器尺寸、容器尺寸又反过来影响查询结果的循环依赖。

---
## 查询容器的选择
对于未指定名称的尺寸查询，浏览器会选择==最近的==、==满足查询所需尺寸能力==的祖先查询容器
```css
.outer {
  container-type: inline-size;
  width: 1000px;
}

.inner {
  container-type: inline-size;
  width: 300px;
}

@container (width >= 500px) {
  .card {
    background: blue;
  }
}
```

如果 `.card` 位于 `.inner` 内部，则查询的是 `.inner` 的 300px，不会因为外层 `.outer` 满足条件就跳过 `.inner`，最终 `.card` 不会获得蓝色背景

### container-name
可以给查询容器命名，以指定要查询的祖先容器
```css
.outer {
  container-name: dashboard;
  container-type: inline-size;
}

@container dashboard (width >= 800px) {
  .card {
    background: blue;
  }
}
```

还可以使用简写：
```css
.outer {
  container: dashboard / inline-size;
}
```

等价于同时设置 `container-name` 和 `container-type`

---
## 容器查询单位
容器查询提供相对于查询容器尺寸的长度单位：

|单位|含义|
|---|---|
|`cqw`|查询容器宽度的 1%|
|`cqh`|查询容器高度的 1%|
|`cqi`|查询容器行内轴尺寸的 1%|
|`cqb`|查询容器块轴尺寸的 1%|
|`cqmin`|`cqi`、`cqb` 中较小的值|
|`cqmax`|`cqi`、`cqb` 中较大的值|

例如：
```css
.wrapper {
  container-type: inline-size;
}

.title {
  font-size: clamp(1rem, 4cqi, 1.5rem);
}
```

字体大小随容器行内轴尺寸变化，并限制在 `1rem` 到 `1.5rem` 之间。

注意：容器查询单位会寻找相应轴上符合条件的祖先尺寸查询容器；如果找不到，会回退到对应的小视口单位（`sv*`）。

---
## 常见注意事项
### 不能直接根据自身尺寸查询自身
```css
.card {
  container-type: inline-size;
}

@container (width >= 500px) {
  .card {
    background: red;
  }
}
```

上面的查询不会使用 `.card` 自身的尺寸，而是尝试寻找其符合要求的祖先查询容器。

正确的组件结构：
```html
<div class="wrapper">
  <div class="card">Content</div>
</div>
```

由 `.wrapper` 提供查询容器，`.card` 根据其尺寸响应。

### Container Queries 与 ResizeObserver

- **Container Queries**：CSS 声明式响应，适合调整布局和视觉样式
- **ResizeObserver**：通过 JavaScript 监听元素尺寸变化，适合需要执行 JS 逻辑的场景，例如重新绘制 Canvas 图表

### 不是所有容器查询都查询尺寸
现代容器查询还包括 Style Queries（样式查询）等能力。`container-type: normal` 不支持尺寸查询，但不代表该元素完全不能作为其他类型的查询容器
