# Flex
> Last Format Time：9/16/2026 19:24:50

[https://developer.mozilla.org/zh-CN/docs/Web/CSS/Guides/Flexible_box_layout/Basic_concepts](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Guides/Flexible_box_layout/Basic_concepts)

---
## 基础
###  flex-basis
在分配剩余空间之前，元素的初始主轴尺寸是多少，在默认横向 Flex 布局中，主轴就是水平方向，因此可以近似理解为初始宽度

表示先把元素当作宽 200px，再计算剩余空间
```css
flex-basis: 200px;
```

表示分配空间时，先把元素的基础尺寸当作 0，然后主要根据 `flex-grow` 比例分配
```css
flex-basis: 0%;
```

这就是为什么两个元素都写：
```css
flex: 1;
```

通常会得到相等宽度
```css
.left {
  flex: 1;
}

.right {
  flex: 1;
}
```

效果大致是：

```text
|      left      |      right      |
|      50%       |       50%       |
```

### flex-grow
```css
flex-grow: 1;
```

表示：当父容器有剩余空间时，这个元素按什么比例扩大
```css
.container {
  display: flex;
  width: 600px;
}

.a { flex: 1 1 100px; }
.b { flex: 2 1 200px; }
.c { flex: 1 1 100px; }
```

因此，剩余的 160px 按比例分配，分别增加 40px、80px、40px
![[Pasted image 20261010160546.png]]

如果是：
```css
.a { flex: 1 1 200px; }
.b { flex: 2 1 200px; }
.c { flex: 1 1 100px; }
```

剩余 60px

|元素|flex-basis|分配空间|最终宽度|
|---|---|---|---|
|A|200px|+15px|215px|
|B|200px|+30px|230px|
|C|100px|+15px|115px|
![[Pasted image 20261010160708.png]]

虽然 B 的 `flex-grow` 是 A 的 2 倍，但最终宽度仅仅是 230px，而不是 430px

它不是直接表示宽度，而是表示==剩余空间==的分配权重

### flex-shrink
当所有 Flex Item 的基础尺寸加起来超过容器宽度时，这个元素是否允许缩小，以及按什么比例缩小
```css
.container {
  display: flex;
  width: 400px;
  gap: 20px;
}

.a { flex: 1 1 200px; }
.b { flex: 2 1 200px; }
.c { flex: 1 1 100px; }
```

三个元素的基础尺寸 500px 

两个 `gap` 共 40px，因此：FreeSpace=400-500-40=-140px 浏览器需要让三个元素总共缩小 140px

收缩权重 = flex-shrink  *  flex base size

|元素|flex-shrink|flex-basis|收缩权重|
|---|---|---|---|
|A|1|200px|200|
|B|1|200px|200|
|C|1|100px|100|

因为假如只看 `flex-shrink`，一个宽度 500px 的元素和一个宽度 20px 的元素可能被要求缩小相同的像素数，后者很容易被压到 0

![[Pasted image 20261010161658.png]]

为什么 flex-shrink: 1 仍然会撑破容器？
```html
<div className="row">
  <img className="avatar" src="/avatar.png" />
  <div className="content">
    <p className="title">
      ThisIsAnExtremelyLongUnbreakableText...
    </p>
  </div>
</div>
```

```css
.row {
  display: flex;
  width: 300px;
}

.avatar {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
}

.content {
  flex: 1;
}

.title {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
```

理论上，`.content` 应该占据剩下的 252px。

但实际可能出现一个问题：`.content` 不愿意缩小到 252px，而是被长文本撑开。

根本原因 Automatic Minimum Size（自动最小尺寸）Flex Item 默认的：
```
min-width: auto;
```

不是简单等价于 `min-width: 0`。

在主轴为水平方向时，对于某些非滚动 Flex Item，浏览器会根据内容确定自动最小宽度。这可能导致元素不能继续缩小

加个最小值，再配合内部文本的单行省略布局：
```css
.content {
  flex: 1;
  min-width: 0;
}

.title {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
```

### flex-wrap
[[Flex 布局下元素挤压问题 ⌚️]]
默认情况下：
```css
.container {
  display: flex;
  flex-wrap: nowrap;
}
```

所有 Flex Item 都尝试排列在同一条 Flex Line 内，即使需要压缩甚至发生溢出。

设置：
```css
.container {
  flex-wrap: wrap;
}
```

之后，浏览器就可以把元素放到多条 Flex Line 中。

假设换行了：
```css
.container {
  display: flex;
  flex-wrap: wrap;
  width: 500px;
  gap: 16px;
}

.item {
  flex: 1 1 200px;
}
```

三个元素的基础尺寸都是 200px

第一行可以放两个，但放不下第三个，因此第三个元素进入第二行

接下来是重点，每一行都独立进行 Flex Grow / Shrink 计算：

- 第一行：FreeSpace=500-416=84px A 和 B 各增加 42px，最终均为 242px
- 第二行只有 C：FreeSpace=500-200=300px 因此 C 最终增长到 500px


![[Pasted image 20261010164209.png]]

虽然 `flex-wrap` 让 Flexbox 能够产生多行，但它没有变成真正的二维布局系统。不同 Flex Line 之间不会自动共享列宽。

也就是说，你无法保证第一行和第二行的卡片严格对齐成统一的网格列。

这就是 Flexbox 和 Grid 的核心分界：Flexbox 是以每条线为核心的一维布局系统，Grid 则是统一管理行和列的二维布局系统。

所以，在实际项目中，导航栏、按钮组、标签组适合 Flex；要求严格行列对齐的卡片网格、仪表盘等通常更适合 Grid。

### flex 简写
[https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/flex-grow](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/flex-grow)


|写法|通常对应的展开|特点|
|---|---|---|
|`flex: 1`|`1 1 0%`|从零基础尺寸参与分配|
|`flex: auto`|`1 1 auto`|参考自身尺寸，再分配空间|
|`flex: none`|`0 0 auto`|不增长、不收缩|
|`flex: initial`|`0 1 auto`|不增长，允许收缩|

`flex: 1`：

- `flex-grow: 1`：项目可以伸展占用剩余空间，2就是占两份
- `flex-shrink: 1`：项目可以收缩防止溢出，与grow类似
- `flex-basis: 0%`：项目在分配多余空间前的初始大小，在主轴方向的初始值大小

这两个很容易混淆：
```css
flex: 1;          /* 1 1 0% */
flex: 1 1 auto;
```

忽略元素内容或 `width` 的基础尺寸倾向，优先按比例均分空间：
```css
.a {
  flex: 1;
}

.b {
  flex: 1;
}
```

即使 A 的文字更多，二者通常还是等宽。

先考虑元素自身宽度或内容尺寸，再分配剩余空间：
```css
.a {
  flex: 1 1 auto;
}

.b {
  flex: 1 1 auto;
}
```

---
## Alignment
[[Alignment💡]]
Flexbox 始终存在两个方向：

- Main Axis（主轴）：由 `flex-direction` 决定
- Cross Axis（交叉轴）：与主轴垂直

|属性|方向|作用对象|
|---|---|---|
|`justify-content`|主轴|每一行中的元素整体|
|`align-items`|交叉轴|每个 Flex Item|
|`align-self`|交叉轴|单独一个 Flex Item|
|`align-content`|交叉轴|多条 Flex Line|

### justify-content
为什么有时不生效？

例如：
```
.container {
  display: flex;
  width: 600px;
  justify-content: space-between;
}

.item {
  flex: 1;
}
```

假设有三个元素，且没有其他限制。三个元素通过 `flex-grow` 就已经分配完 600px。

剩余给 justify-content 的空间为 0，自然就没有效果
