# Rendering & Performance

---
## 浏览器渲染流程
浏览器将 DOM 和 CSS 转换为屏幕画面，可以简化为四个主要阶段：
```
DOM + CSSOM
     ↓
Style（样式计算）
     ↓
Layout（布局）
     ↓
Paint（绘制）
     ↓
Composite（合成）
```

|阶段|作用|
|---|---|
|Style|根据 CSS 规则、层叠、继承等机制计算元素样式|
|Layout|根据布局规则计算元素的位置、尺寸等几何信息|
|Paint|生成背景、文字、边框、阴影等绘制内容|
|Composite|将不同绘制内容或合成层组合成最终画面|

注意：

- 这是简化的逻辑模型，并不是每次更新都会执行全部阶段
- Paint（绘制）与 Rasterization（光栅化）可以进一步区分
- Stacking Context（层叠上下文）不等于 Compositing Layer（合成层）

## CSS 属性变化对应的渲染成本
不同 CSS 属性发生变化时，触发的渲染工作可能不同

|类型|典型渲染路径|CSS 属性|
|---|---|---|
|布局相关|Style → Layout → Paint → Composite|`width`、`height`、`top`|
|绘制相关|Style → Paint → Composite|`background-color`、`box-shadow`|
|合成相关|Composite 为主|`transform`、`opacity`|

以上是典型情况，实际是否能够跳过布局或绘制，取决于浏览器实现和合成优化条件

### left 与 transform
```
/* 方案一：改变布局相关的几何信息 */
.box {
  position: relative;
  left: 100px;
}

/* 方案二：仅进行视觉变换 */
.box {
  transform: translateX(100px);
}
```

二者都能让元素视觉上向右移动，但底层机制不同：

- `left`：通常需要布局相关处理。

- `transform`：不改变元素在正常文档流中的布局位置，满足条件时可以通过合成器完成更新。


核心：视觉位置发生变化，不代表布局位置一定发生变化。

因此，实现纯视觉移动动画时，通常优先考虑 `transform`。

---
## Reflow 与 Repaint
### Reflow 回流 / 重新布局 / 重排
元素几何信息发生变化，需要重新计算受影响元素的布局

常见触发原因：

- 修改 `width`、`height`

- 修改影响布局的字体、内容

- 增删影响布局的 DOM 元素

- 容器尺寸发生变化


### Repaint 重绘
元素视觉内容发生变化，需要重新绘制相关内容，但不一定重新布局

例如：
```
.box {
  background-color: red;
}
```

通常只需要重绘，不需要重新布局

传统说法“回流一定引起重绘”不够严谨，现代浏览器具有缓存、局部更新和合成优化机制，布局变化不代表所有受影响的像素都必须重新光栅化

---
## 批量布局机制
浏览器通常不会在每次修改 DOM 或 CSS 后立即执行 Layout，而是尽量将多次变动合并，在合适的时机统一计算
```
box.style.width = "200px";
box.style.height = "300px";
box.style.padding = "20px";
```

以上三次修改通常不需要立即执行三次 Layout

---
## 强制同步布局（Forced Synchronous Layout）
当浏览器存在尚未完成的布局更新，而 JavaScript 又需要最新的布局信息时，可能迫使浏览器立即执行 Layout
```
box.style.width = "200px"; // 写：使布局信息失效

console.log(box.offsetWidth); // 读：可能强制同步布局
```

执行过程：
```
修改布局相关样式
      ↓
布局信息失效（Layout Invalidation）
      ↓
读取最新几何信息
      ↓
Forced Synchronous Layout
      ↓
返回测量结果
```

### 常见布局读取 API

|API|作用|
|---|---|
|`offsetWidth / offsetHeight`|读取布局宽高，包含 padding、border|
|`offsetTop / offsetLeft`|读取元素的偏移位置|
|`clientWidth / clientHeight`|读取内部尺寸，包含 padding，不包含 border|
|`getBoundingClientRect()`|获取元素相对于视口的边界矩形|
|`scrollWidth / scrollHeight`|获取滚动内容尺寸|
|`getComputedStyle()`|获取计算样式，特定情况下可能触发布局|

注意：调用这些 API 不一定触发 Layout，关键取决于布局信息是否已失效，以及读取操作是否需要最新结果。

---
## 布局抖动（Layout Thrashing）
布局抖动是指 JavaScript 反复交替读写布局相关信息，导致浏览器多次执行不必要的同步布局。

### 交替读写
```
const boxes = document.querySelectorAll(".box");

boxes.forEach((box) => {
  const width = box.offsetWidth; // 读
  box.style.width = `${width + 10}px`; // 写
});
```

可能产生：
```
Read → Write → Layout
Read → Write → Layout
Read → Write → Layout
...
```

### 批量读取，再批量写入
```
const boxes = [...document.querySelectorAll(".box")];

// 统一读取
const widths = boxes.map((box) => box.offsetWidth);

// 统一修改
boxes.forEach((box, index) => {
  box.style.width = `${widths[index] + 10}px`;
});
```

这样可以减少读写交替引起的强制布局

原则：Read First, Write Later（先读后写）

---
## requestAnimationFrame 与布局
`requestAnimationFrame`（rAF）会在浏览器下一次重绘前执行回调，适合安排动画与视觉更新。

但 rAF 不会自动消除强制同步布局
```
requestAnimationFrame(() => {
  box.style.width = "200px";

  // 仍然可能触发强制同步布局
  console.log(box.offsetWidth);
});
```

因为 rAF 回调执行时，并不代表当前帧已经完成 Layout。

正确优化方向仍然是尽量将布局读取安排在写入之前。

---
## 合成层（Compositing Layer）
合成层是浏览器内部用于组织和独立处理部分页面内容的渲染结构

浏览器可以将部分内容独立光栅化，之后在 Composite（合成）阶段复用这些内容，而不必每次重新布局和绘制
```
Style
  ↓
Layout
  ↓
Paint
  ↓
Rasterization（光栅化）
  ↓
Composite（合成）
```

其中：

- Rasterization（光栅化）：将绘制内容转换为像素数据
- Composite（合成）：组合不同的绘制内容，生成最终画面

对于满足合成优化条件的动画，浏览器可以复用已有内容，仅更新变换或透明度等合成信息。

## GPU 加速与合成优化
GPU（Graphics Processing Unit，图形处理器）擅长并行图形计算，可以参与浏览器的光栅化、合成等过程。

GPU 加速不等于仅合成动画（Compositor-only Animation）。

在 Chromium 的简化模型中：

|Main Thread（主线程）|Compositor Thread（合成线程）|
|---|---|
|JavaScript 执行|管理和组织合成工作|
|Style 样式计算|协调光栅化|
|Layout 布局|更新合成变换|
|Paint 相关工作|组合画面|

合成动画在满足条件时，可以由合成器独立推进，减少对主线程逐帧执行的依赖

### CSS 动画与 JavaScript 动画
```
.box {
  transition: transform 300ms;
}

.box:hover {
  transform: translateX(100px);
}
```

上述动画有机会由合成器独立执行。

但如果通过 JavaScript 的 `requestAnimationFrame` 逐帧修改 `transform`，每一帧仍需要主线程执行 JS

因此，动画性能取决于：

- 修改了什么 CSS 属性

- 是否能够使用合成优化

- 动画是否需要主线程逐帧参与

---
## will-change
`will-change` 用于提前告知浏览器某些属性即将变化，让浏览器有机会提前进行渲染优化
```
.box {
  will-change: transform;
}
```

它可能促使浏览器提前调整合成策略，但不是强制开启 GPU 加速的命令

### 不能滥用

- 可能增加 GPU / 图形内存消耗。

- 可能增加合成层管理成本。

- 可能产生额外的渲染资源开销。

- 可能提前创建 Stacking Context，影响层叠行为。


例如：
```
/* 不推荐：无差别为大量元素添加 */
.card {
  will-change: transform;
}
```

如果页面存在几百个卡片，浏览器可能为大量实际上不需要动画的元素保留额外资源

使用原则：默认不添加，确实存在性能问题时再考虑，并通过 Performance 验证效果

另外：
```
transform: translateZ(0);
```

也不能被当作现代浏览器中可靠的“强制 GPU 加速开关”

---
## CSS Containment（CSS 包含机制）
CSS Containment 用于限制元素内部变化对外部布局、绘制等计算的影响，帮助浏览器缩小渲染工作范围。

通过 `contain` 属性声明包含边界。

### 四种包含机制

|属性值|作用|
|---|---|
|`layout`|布局包含，隔离部分内外布局影响|
|`paint`|绘制包含，限制后代内容的绘制范围|
|`size`|尺寸包含，计算容器内在尺寸时忽略后代的尺寸贡献|
|`style`|样式包含，限制 CSS 计数器等特定样式效果|

```
.box {
  contain: layout;
}
```

注意：

- `contain: layout` 会建立独立格式化上下文和 Stacking Context，并为绝对定位、固定定位后代建立包含块。

- `contain: paint` 可能裁剪溢出内容，例如 Tooltip、Dropdown。

- `contain: size` 可能导致自动尺寸无法由子元素撑开，需要适当设置尺寸。

- `contain: style` 不是 CSS 样式作用域隔离，不等于 CSS Modules 或 Shadow DOM。


### 组合值
```
/* layout + paint + style */
.box {
  contain: content;
}

/* size + layout + paint + style */
.box {
  contain: strict;
}
```

`strict` 包含尺寸隔离，使用时尤其需要考虑容器尺寸。

---
## content-visibility（内容可见性）

`content-visibility` 允许浏览器跳过暂时不需要的内容渲染，从而减少样式计算、布局和绘制开销。

|值|作用|
|---|---|
|`visible`|默认值，正常渲染|
|`hidden`|跳过后代内容渲染|
|`auto`|由浏览器根据内容是否与用户当前操作相关，决定是否跳过内部渲染|

### content-visibility: auto
```
.article {
  content-visibility: auto;
}
```

对于长页面中距离视口较远、当前不相关的内容，浏览器可以跳过其内部渲染。

当用户滚动到附近时，再执行必要的渲染工作。

注意：`auto` 不意味着所有视口外元素都会被跳过。 浏览器还会考虑焦点、选择状态等因素。

### 与 display: none 的区别

|`display: none`|`content-visibility: auto`|
|---|---|---|
|DOM 是否保留|是|是|
|是否保留布局占位|否|通常保留容器占位|
|是否跳过渲染|是|根据相关性决定|
|页面内搜索|隐藏内容不可正常搜索定位|可以搜索定位|
|主要用途|隐藏元素|按需渲染优化|

---
## contain-intrinsic-size（内在尺寸替代）
当 `content-visibility: auto` 跳过内部布局时，浏览器可能无法根据子元素计算容器的自然尺寸

如果跳过时的占位尺寸与实际尺寸差距过大，可能造成滚动条变化、页面跳动。

可以提供替代尺寸：
```
.article {
  content-visibility: auto;
  contain-intrinsic-size: auto 500px;
}
```

含义：

- 初次没有实际尺寸记录时，使用 `500px` 作为替代尺寸。

- 已记录实际尺寸时，可以复用此前的尺寸。


也可以仅针对块轴设置：
```
.article {
  content-visibility: auto;
  contain-intrinsic-block-size: auto 500px;
}
```

其中 `500px` 是估计值，应尽量接近内容实际尺寸。

## content-visibility 与 Virtual List
两者都能优化长列表，但作用层次不同

|content-visibility|Virtual List|
|---|---|---|
|DOM 节点数量|不减少|减少|
|React 挂载数量|不减少|减少|
|浏览器渲染成本|可以降低|可以降低|
|实现复杂度|较低|较高|
|适用场景|长文章、大型页面区块|海量数据列表|

例如：
```
.item {
  content-visibility: auto;
  contain-intrinsic-size: auto 80px;
}
```

即使页面存在 10,000 个 DOM 节点，`content-visibility` 也不会自动移除其中的节点，只是让浏览器跳过部分不相关内容的渲染。

而虚拟列表通过只挂载可见区域及附近的节点，直接减少 DOM 数量。

结论：`content-visibility` 是浏览器渲染优化，Virtual List 是 DOM 数量优化，二者不能简单互相替代。

## Chrome DevTools 性能诊断
使用 Chrome DevTools → Performance 观察：

- `Recalculate Style`：样式重新计算

- `Layout`：布局计算

- `Paint`：绘制操作

- `Composite`：合成相关工作

- `Forced Reflow`：强制同步布局相关诊断

- `Frames`：查看帧耗时、卡顿

React Profiler 用于分析 React 组件更新，Chrome Performance 用于分析浏览器执行 JavaScript、Layout、Paint 等工作的耗时




---
## CLS（Cumulative Layout Shift，累积布局偏移）
CLS 是 [[Core Web Vitals 核心网页指标]]之一，用于衡量页面的视觉稳定性，即用户没有预期到的可见元素位置变化

例如：图片加载后突然撑开容器，把下方按钮挤走

先录制网页，找到布局偏移，找到影响指标的元素：
![[Pasted image 20261016161136.png]]

### CLS 计算方式
单次布局偏移得分：

- Impact Fraction（影响比例）：发生偏移的可见元素在移动前后覆盖区域的并集，占视口面积的比例。
- Distance Fraction（距离比例）：受影响元素的最大移动距离，占视口最大尺寸的比例。


CLS 并不是所有布局偏移分数的简单相加，而是采用 Session Window（会话窗口） 机制：

- 相邻偏移间隔小于 1 秒时，可以归入同一窗口。
- 一个窗口最多持续 5 秒。
- CLS 取累计得分最高的窗口。


### CLS 评价标准

|CLS|评价|
|---|---|
|≤ 0.1|良好|
|> 0.1 且 ≤ 0.25|需要改进|
|> 0.25|较差|

注意：

- CLS 不统计所有布局变化。
- 符合条件的点击、键盘等离散用户输入后 500ms 内发生的布局偏移，通常不计入 CLS。
- 滚动、鼠标移动不适用这一豁免规则。
- `transform` 产生的视觉移动通常不计入 CLS。

### CLS 常见原因与优化
##### 图片没有预留尺寸
```
<!-- 提前声明图片宽高比 -->
<img
  src="/banner.jpg"
  width="1200"
  height="600"
  alt="Banner"
/>
```

```
img {
  max-width: 100%;
  height: auto;
}

/* 或者使用 */
.banner {
  aspect-ratio: 2 / 1;
}
```

提前预留空间，避免图片加载后撑开布局。

##### 异步内容导致布局跳动
React 项目中常见问题：
```
if (isLoading) {
  return <div>Loading...</div>;
}

return <ActivityCard data={data} />;
```

Loading 与实际内容高度相差较大，数据加载后可能造成 Layout Shift。

优化方案：

- 使用 Skeleton（骨架屏）
- 预留接近真实内容的空间
- 尽量保持加载前后组件的布局尺寸一致


```
.activity-container {
  min-height: 300px;
}
```

##### Web Font 加载
网络字体与后备字体的字形宽度、行高不同，切换字体可能导致文本重新换行，引发布局偏移
```
@font-face {
  font-family: "MyFont";
  src: url("/font.woff2") format("woff2");
  font-display: optional;
}
```

`font-display: optional` 可以减少后期字体切换，但可能导致当前页面始终使用后备字体。

##### 布局属性动画
```
/* 可能涉及 Layout */
.box {
  transition: top 300ms;
}

/* 纯视觉移动优先 */
.box {
  transition: transform 300ms;
}
```

`transform` 不改变正常布局中的位置，通常也不会产生 CLS

但是否使用 `transform`，仍需要根据实际布局需求决定
