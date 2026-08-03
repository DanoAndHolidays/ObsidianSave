# Flex与Grid布局
> Last Format Time：6/12/2026 20:14:29 

## Flex布局
### flex: 1的含义
[https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/flex-grow](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/flex-grow)
`flex: 1` 是 `flex-grow: 1`、`flex-shrink: 1`、`flex-basis: 0%` 的简写：
- `flex-grow: 1`：项目可以伸展占用剩余空间，2就是占两份
- `flex-shrink: 1`：项目可以收缩防止溢出，与grow类似
- `flex-basis: 0%`：项目在分配多余空间前的初始大小，在主轴方向的初始值大小

`flex: 1` 是 `flex` 简写属性，完整包含三个值：

```css
flex: flex-grow flex-shrink flex-basis;
```

所以：

```css
flex: 1;
```

通常等价于：

```css
flex: 1 1 0%;
```

三个属性分别是：

## 1. `flex-grow`

```css
flex-grow: 1;
```

表示：**当父容器有剩余空间时，这个元素按什么比例扩大。**

例如：

```html
<div class="container">
  <div class="a">A</div>
  <div class="b">B</div>
</div>
```

```css
.container {
  display: flex;
}

.a {
  flex-grow: 1;
}

.b {
  flex-grow: 2;
}
```

如果父容器剩余 300px：

* A 分到 100px
* B 分到 200px

因为比例是：

```text
1 : 2
```

它不是直接表示宽度，而是表示**剩余空间的分配权重**。

---

## 2. `flex-shrink`

```css
flex-shrink: 1;
```

表示：**当父容器空间不够时，这个元素是否允许缩小，以及按什么比例缩小。**

例如：

```css
.a {
  flex-shrink: 1;
}

.b {
  flex-shrink: 0;
}
```

空间不足时：

* A 可以被压缩
* B 不允许被压缩

Tailwind 中：

```tsx
shrink       // flex-shrink: 1
shrink-0     // flex-shrink: 0
```

你之前看到的：

```tsx
flex-shrink-0
```

就是不允许该元素因 Flex 空间不足而缩小。

需要注意，实际缩小量不仅与 `flex-shrink` 有关，也和元素原本的尺寸有关，并不总是简单按 `1:2` 减少像素。

---

## 3. `flex-basis`

```css
flex-basis: 0%;
```

表示：**在分配剩余空间之前，元素的初始主轴尺寸是多少。**

在默认横向 Flex 布局中，主轴就是水平方向，因此可以近似理解为初始宽度。

```css
flex-basis: 200px;
```

表示先把元素当作宽 200px，再计算剩余空间。

而：

```css
flex-basis: 0%;
```

表示分配空间时，先把元素的基础尺寸当作 0，然后主要根据 `flex-grow` 比例分配。

这就是为什么两个元素都写：

```css
flex: 1;
```

通常会得到相等宽度：

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

---

## `flex: 1` 的整体含义

```css
flex: 1 1 0%;
```

可以理解为：

```text
flex-grow:   1   有剩余空间时允许扩大
flex-shrink: 1   空间不足时允许缩小
flex-basis:  0%  从零基础尺寸开始按比例分配
```

所以它的核心效果是：

> 占据可用的剩余空间，并且可以随着父容器空间扩大或缩小。

---

## 和 `flex: 1 1 auto` 的区别

这两个很容易混淆：

```css
flex: 1;          /* 1 1 0% */
flex: 1 1 auto;
```

### `flex: 1`

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

### `flex: 1 1 auto`

先考虑元素自身宽度或内容尺寸，再分配剩余空间：

```css
.a {
  flex: 1 1 auto;
}

.b {
  flex: 1 1 auto;
}
```

内容较多的元素可能最终更宽。

---

## 常见简写对照

```css
flex: 1;
```

等价于：

```css
flex-grow: 1;
flex-shrink: 1;
flex-basis: 0%;
```

```css
flex: auto;
```

等价于：

```css
flex: 1 1 auto;
```

```css
flex: none;
```

等价于：

```css
flex: 0 0 auto;
```

```css
flex: 0 0 200px;
```

表示：

* 不扩大
* 不缩小
* 基础宽度为 200px

在 Tailwind 中，`flex-1` 基本就是：

```css
flex: 1 1 0%;
```


### 基础
[https://developer.mozilla.org/zh-CN/docs/Web/CSS/Guides/Flexible_box_layout/Basic_concepts](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Guides/Flexible_box_layout/Basic_concepts)

---
## Grid布局
[https://developer.mozilla.org/zh-CN/docs/Web/CSS/Guides/Grid_layout/Basic_concepts](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Guides/Grid_layout/Basic_concepts)
