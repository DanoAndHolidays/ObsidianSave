# Grid
> Last Format Time：9/16/2026 19:24:50

[https://developer.mozilla.org/zh-CN/docs/Web/CSS/Guides/Grid_layout/Basic_concepts](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Guides/Grid_layout/Basic_concepts)

---
## 核心概念
Grid 是 CSS 的二维布局系统，可以同时控制行（Row）和列（Column）。

与 Flex 的区别：

- Flex：一维布局，主要沿主轴排列，换行后每行独立布局。
- Grid：二维布局，通过行、列构建网格，元素可以跨行、跨列。

Grid 的核心思想：先建立网格坐标系统，再决定元素如何放置、占据多少空间。

|概念|说明|
|---|---|
|Grid Container|设置 `display: grid` 的容器|
|Grid Item|直接参与 Grid 布局的子元素|
|Grid Track|两条相邻网格线之间的行或列|
|Grid Line|划分网格的线，用于定位元素|
|Grid Cell|一行与一列交叉形成的单元格|
|Grid Area|由网格线围成的矩形区域，可以跨多个 Cell|

注意：N 列对应 N + 1 条列网格线，Grid 定位依赖的是网格线，而不是单元格编号。

![[Pasted image 20261010165640.png]]

---
## 显式网格（Explicit Grid）
显式网格是开发者通过 `grid-template-columns` 和 `grid-template-rows` 主动定义的网格轨道。
```
.container {
  display: grid;

  /* 定义 3 列 */
  grid-template-columns: 100px 200px 100px;

  /* 定义 2 行 */
  grid-template-rows: 80px 80px;

  /* 行列间距 */
  gap: 10px;
}
```

即使容器中只有一个元素，显式定义的 3 列、2 行依然存在。

### Grid Line 定位
使用 `grid-column` 和 `grid-row` 指定元素的位置。
```
.item {
  /* 从第 1 条列网格线到第 3 条 */
  grid-column: 1 / 3;

  /* 从第 1 条行网格线到第 2 条 */
  grid-row: 1 / 2;
}
```

等价于：
```
.item {
  /* 从第 1 条线开始，跨越 2 列 */
  grid-column: 1 / span 2;
}
```

其中：

- `1 / 3`：起始线为 1，结束线为 3。
- `span 2`：跨越两个网格轨道。

注意：`grid-column: 1 / 3` 占据的是 2 列，而不是 3 列。

![[Pasted image 20261010165613.png]]

---
## 隐式网格（Implicit Grid）
当现有显式网格不足以容纳元素，或者元素被定位到显式网格之外时，浏览器可以自动创建新的网格轨道，这些轨道称为隐式网格。

### 隐式行的生成
```
.container {
  display: grid;

  /* 显式定义 3 列、1 行 */
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: 80px;

  gap: 10px;
}
```

假设容器中有 6 个子元素：
```
<div class="container">
  <div>A</div>
  <div>B</div>
  <div>C</div>
  <div>D</div>
  <div>E</div>
  <div>F</div>
</div>
```

默认情况下会形成：
```
显式行：  A    B    C
隐式行：  D    E    F
```

因为只显式定义了一行，所以浏览器自动创建第二行。

### 控制隐式轨道尺寸
可以通过 `grid-auto-rows` 和 `grid-auto-columns` 设置隐式轨道的尺寸。
```
.container {
  display: grid;

  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: 80px;

  /* 隐式行统一设置为 120px */
  grid-auto-rows: 120px;

  /* 隐式列统一设置为 100px */
  grid-auto-columns: 100px;
}
```

注意：

- `grid-template-rows`：控制显式行。
- `grid-auto-rows`：控制隐式行。
- `grid-template-columns`：控制显式列。
- `grid-auto-columns`：控制隐式列。

### 自动放置方向
通过 `grid-auto-flow` 控制未明确定位的元素如何自动放入网格。
```
.container {
  /* 默认：优先按行填充 */
  grid-auto-flow: row;

  /* 优先按列填充 */
  /* grid-auto-flow: column; */
}
```

`row` 表示优先沿行方向填充，`column` 表示优先沿列方向填充。必要时浏览器会创建对应的隐式轨道。

---
## 弹性轨道单位
`fr`（fraction）表示 Grid 轨道对可分配空间的弹性份额，用于实现弹性布局。
```
.container {
  width: 600px;
  display: grid;

  grid-template-columns: 100px 1fr 2fr;
  gap: 20px;
}
```

计算过程：

1. 固定列占据 100px。
2. 两个 `gap` 占据 40px。
3. 剩余空间：600 - 100 - 40 = 460px。
4. 按照 1:2 分配剩余空间。

最终：

- 第一列：100px
- 第二列：153.33px
- 第三列：306.67px

注意：`fr` 不是简单地按照比例分配整个容器空间，而是参与 Grid 轨道的弹性尺寸计算。 上述计算成立的前提是没有内容最小尺寸等额外约束。

### fr 与百分比的区别
```
/* 百分比 */
grid-template-columns: 50% 50%;

/* 弹性分配 */
grid-template-columns: 1fr 1fr;
```

假设容器宽度为 600px，`gap: 20px`：

|写法|每列宽度|总占用|
|---|---|---|
|`50% 50%`|300px|620px|
|`1fr 1fr`|290px|600px|

区别：

- `%`：相对于容器对应的尺寸计算，不会自动扣除 `gap`。
- `fr`：参与可分配空间的计算，通常会先考虑固定轨道与间距。

### 1fr 的自动最小尺寸问题
```
.container {
  display: grid;
  grid-template-columns: 200px 1fr;
}
```

这里的 `1fr` 并不意味着轨道可以无限缩小。

对于轨道尺寸计算，可以将其理解为：

```
grid-template-columns: 200px minmax(auto, 1fr);
```

由于默认最小轨道尺寸为 `auto`，Grid 需要考虑内部元素的最小尺寸贡献。

如果内部存在很长的不可换行文本等内容，轨道可能被内容撑开，导致整个 Grid 超出容器。

```
.container {
  display: grid;

  grid-template-columns: 200px minmax(0, 1fr);
}
```

其中：

- `0`：轨道允许缩小到 0，不再受到 `auto` 最小轨道尺寸的限制。
- `1fr`：按照弹性轨道规则分配空间。

注意：`minmax(0, 1fr)` 解决的是轨道被内容撑开的问题，并不代表内部内容一定不会溢出。

必要时还需要：
```
.content {
  min-width: 0;
  overflow-wrap: anywhere;
}
```

### minmax()：定义轨道尺寸范围
语法：
```
minmax(min, max)
```

用于给 Grid 轨道设置最小、最大尺寸约束。

例如：
```
.container {
  display: grid;
  grid-template-columns: minmax(200px, 1fr) 2fr;
}
```

第一列最小宽度为 200px，同时可以参与弹性空间分配。


|写法|作用|
|---|---|
|`minmax(0, 1fr)`|解除轨道的自动最小尺寸限制|
|`minmax(200px, 1fr)`|最小 200px，同时允许弹性增长|
|`minmax(150px, 300px)`|最小 150px，最大 300px|
|`minmax(min-content, 1fr)`|以内容固有最小尺寸为下限|

- `min-content`：内容在允许正常换行的情况下所需的固有最小尺寸。
- `max-content`：内容不进行可选换行时所需的固有尺寸。

```
.container {
  display: grid;
  grid-template-columns: min-content max-content;
}
```

注意：`auto` 最小轨道尺寸不总是等于 `min-content`，具体取决于网格项的尺寸约束等条件。

### repeat()：重复定义轨道
`repeat()` 用于简化重复的 Grid 轨道定义。
```
/* 等价写法 */
grid-template-columns: 1fr 1fr 1fr 1fr;

grid-template-columns: repeat(4, 1fr);
```

还可以重复一组轨道：
```
grid-template-columns: repeat(2, 100px 1fr);

/* 等价于 */
grid-template-columns: 100px 1fr 100px 1fr;
```

实际项目中的常见写法：
```
.card-list {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}
```

表示定义三列等宽的弹性轨道，同时解除轨道的自动最小尺寸限制。

```
grid-template-columns: repeat(3, 1fr);
```

它的含义是：创建三列，每列分配相同的剩余空间。

但是如果希望根据容器宽度自动确定列数呢？

就可以使用 `auto-fit`

##### auto-fit
```
.container {
  display: grid;
  grid-template-columns:
    repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}
```

拆开理解：

- `repeat()`：重复创建轨道。

- `auto-fit`：根据容器空间自动确定可容纳的轨道数量，并折叠未使用的重复轨道。

- `minmax(200px, 1fr)`：每列至少 200px，有剩余空间时允许扩大。


例如容器宽 900px，间距 20px，最多可以放下四列最小宽度为 200px 的轨道

如果只有两个子元素，`auto-fit` 会折叠多余的空轨道，然后让这两个元素伸展

`auto-fill` 也会根据容器宽度自动创建轨道，但它会保留没有元素的空轨道；`auto-fit` 则会折叠这些空轨道
![[Pasted image 20261014161159.png]]

---
## Grid 对齐机制

Grid 的对齐分为两个逻辑方向：

- `justify-*`：Inline Axis，通常对应水平方向。
- `align-*`：Block Axis，通常对应垂直方向。

注意：与 Flex 不同，Grid 的对齐方向不依赖主轴和交叉轴

|属性|作用|
|---|---|
|`justify-items`|所有 Grid Item 在各自区域内的水平对齐|
|`align-items`|所有 Grid Item 在各自区域内的垂直对齐|
|`justify-content`|整个网格轨道集合的水平对齐|
|`align-content`|整个网格轨道集合的垂直对齐|
|`justify-self`|单个 Grid Item 的水平对齐|
|`align-self`|单个 Grid Item 的垂直对齐|

以上水平、垂直方向均指通常的水平书写模式。

核心区别：

- `items`：控制所有网格项在各自 Grid Area 内的位置。
- `content`：控制整个网格轨道集合在容器内的位置。
- `self`：控制单个网格项在其 Grid Area 内的位置。

### items：网格项对齐
`justify-items` 和 `align-items` 控制 Grid Item 在其所属 Grid Area 内的对齐方式。
```
.container {
  display: grid;

  grid-template-columns: repeat(3, 120px);
  grid-template-rows: 100px;

  justify-items: center;
  align-items: center;
}

.item {
  width: 60px;
  height: 40px;
}
```

每个网格区域为 120px × 100px，Item 为 60px × 40px，因此元素会在各自区域内居中。

常见取值：

- `start`：靠逻辑起始位置。
- `end`：靠逻辑结束位置。
- `center`：居中。
- `stretch`：在尺寸条件允许时拉伸元素。

Grid Item 的 `justify-items` 和 `align-items` 初始值均为 `normal`，通常对于自动尺寸的普通元素，表现类似 `stretch`，但存在固有宽高比等例外。

##### place-items
```
.container {
  place-items: center;
}
```

等价于：
```
.container {
  align-items: center;
  justify-items: center;
}
```

如果有两个值：

```
place-items: start center;
```

表示：

- `align-items: start`
- `justify-items: center`

简写顺序：先 align，后 justify。

### content：整个网格对齐
`justify-content` 和 `align-content` 控制整个网格轨道集合在容器内的排列。
```
.container {
  display: grid;

  width: 600px;
  height: 300px;

  grid-template-columns: 100px 100px;
  grid-template-rows: 80px 80px;

  gap: 10px;

  justify-content: center;
  align-content: center;
}
```

由于轨道总宽度为 210px、总高度为 170px，小于容器尺寸，因此整个网格可以居中。

```
.container {
  display: grid;
  width: 600px;

  grid-template-columns: 1fr 1fr;
  justify-content: center;
}
```

由于 `1fr 1fr` 通常已经占满容器的可分配宽度，所以没有剩余空间可以用来移动整个网格。

`justify-content` 需要存在可分配的剩余空间，才能产生明显的对齐效果。


|属性值|作用|
|---|---|
|`start`|靠起始位置|
|`end`|靠结束位置|
|`center`|居中|
|`space-between`|首尾贴边，剩余空间分配在轨道之间|
|`space-around`|每条轨道两侧分配相等空间|
|`space-evenly`|轨道之间和两端间距相等|

##### place-content
```
.container {
  place-content: center;
}
```

等价于：
```
.container {
  align-content: center;
  justify-content: center;
}
```

### self：单个网格项对齐
`justify-self` 和 `align-self` 用于单独控制某个 Grid Item。
```
.container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: 100px;

  place-items: center;
}

.special {
  justify-self: end;
  align-self: start;
}
```

这里 `.special` 会覆盖容器给该元素设置的相应对齐效果。

可以简写为：
```
.special {
  place-self: start end;
}
```

表示在通常水平、从左到右的书写模式下，元素在自己的 Grid Area 中靠右上角对齐。


---
## Grid Template Areas：命名区域布局
`grid-template-areas` 允许通过名称定义网格区域，相比通过 Grid Line 编号定位，更适合页面级布局。
### 基本用法
```
.layout {
  display: grid;

  grid-template-columns: 200px minmax(0, 1fr);
  grid-template-rows: auto 1fr auto;

  grid-template-areas:
    "header  header"
    "sidebar main"
    "footer  footer";

  min-height: 100vh;
  gap: 16px;
}

.header {
  grid-area: header;
}

.sidebar {
  grid-area: sidebar;
}

.main {
  grid-area: main;
}

.footer {
  grid-area: footer;
}
```

对应布局：
```
┌─────────────────────┐
│       Header        │
├────────┬────────────┤
│        │            │
│Sidebar │    Main    │
│        │            │
├────────┴────────────┤
│       Footer        │
└─────────────────────┘
```

核心规则：

- 每个字符串代表一行。
- 每个名称代表一个网格单元所属的区域。
- 相同名称可以跨越多个单元格，但必须形成矩形。
- 每行的单元格数量必须一致。
- `.` 表示未命名的空单元格。

### 留空单元格
```
grid-template-areas:
  "header header"
  "sidebar main"
  ".      footer";
```

`.` 表示该位置不属于任何命名区域，但不代表这个位置不能被其他 Grid Item 使用。

### 命名区域必须是矩形
```
/* 合法 */
grid-template-areas:
  "a a b"
  "a a c";

/* 非法：a 不是矩形 */
grid-template-areas:
  "a a b"
  "a c c";
```

### Grid Areas 与响应式布局
可以结合媒体查询改变区域布局，而不修改 HTML 结构。
```
/* 桌面端 */
.layout {
  display: grid;
  grid-template-columns: 220px minmax(0, 1fr);

  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
}

/* 移动端 */
@media (max-width: 768px) {
  .layout {
    grid-template-columns: minmax(0, 1fr);

    grid-template-areas:
      "header"
      "main"
      "sidebar"
      "footer";
  }
}
```

注意：

`grid-template-areas` 只改变视觉布局，不改变 DOM 顺序。

因此，视觉顺序与键盘导航、辅助技术的阅读顺序可能不一致，不能随意用 CSS 重排具有语义意义的内容。

### Subgrid
需要让嵌套内容与父网格的轨道对齐
```

```