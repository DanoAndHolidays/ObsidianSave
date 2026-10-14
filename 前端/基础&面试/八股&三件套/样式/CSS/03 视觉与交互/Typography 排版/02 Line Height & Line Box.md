# Line Height & Line Box
行高与行盒

---
## line-height
```
.text {
  font-size: 20px;
  line-height: 40px;
}
```

需要区分：

- `font-size`：决定字体使用的 em 方框尺度
- `line-height`：决定行内盒参与行高计算的尺寸
- `line box`：行内格式化上下文中容纳一行内容的行盒

不能简单认为 `font-size: 20px` 就是可见文字高度 20px，也不能认为 `line-height: 40px` 就是在可见文字上下各添加 10px。

实际排版还涉及：

- Ascent / Descent：字体上伸与下伸度量
- Baseline：基线
- Inline Box：行内盒
- Line Box：行盒
- Half-leading：半行距

这些机制共同影响文本高度、垂直对齐以及行盒尺寸



![[Pasted image 20261014172241.png]]


CSS 文字排版需要区分：

|概念|中文|含义|
|---|---|---|
|Inline Box|行内盒|行内元素参与行内布局时产生的盒子|
|Line Box|行盒|IFC 为排列一整行内容而形成的布局区域|
|IFC|行内格式化上下文|负责行内级内容排列、换行和基线对齐的布局机制|

**核心区别：行内盒通常与元素有关，而行盒与“一行内容”有关**

行盒不是一种 `display` 类型，也没有直接对应的 HTML 元素，他是在 IFC 这种机制下产生的

---
## Inline Box 和 Line Box
[[Display 与 Box]]
### display 模型
之前学习过 `display = Outer + Inner`：

|display|Outer|Inner|与行盒的关系|
|---|---|---|---|
|`block`|block|flow|内部有行内内容时，可以形成行盒|
|`inline`|inline|flow|普通非替换元素生成 Inline Box|
|`inline-block`|inline|flow-root|整体作为原子行内级盒参与行盒|
|`flex`|block|flex|内部使用 Flex 布局|
|`inline-flex`|inline|flex|整体作为原子行内级盒参与外部行盒|
|`grid`|block|grid|内部使用 Grid 布局|
|`inline-grid`|inline|grid|整体作为原子行内级盒参与外部行盒|

需要额外区分：

- **Inline-level Box（行内级盒）**：参与外部行内布局的盒子的统称。

- **Inline Box（行内盒）**：普通非替换行内元素生成的盒子，例如 `span`。

- **Atomic Inline-level Box（原子行内级盒）**：在外部行内布局中不可拆分的整体，例如 `inline-block`、`inline-flex`。

所以，`inline-block` 虽然是行内级盒，但不是普通 Inline Box

### Line Box
例如：
```
<div>
  Hello <span>World</span> CSS
</div>
```

```
div {
  width: 300px;
}

span {
  color: red;
}
```

浏览器的处理过程：

1. `div` 生成块级盒子。

2. `div` 内部是文本和行内元素，因此建立 IFC。

3. `span` 生成行内盒；普通文本也参与行内布局。

4. IFC 根据可用宽度、换行规则等，将内容排列到 Line Box 中。

![[Pasted image 20261014180605.png]]

- `div`：生成自己的块级盒子。
- `span`：生成自己的行内盒。
- Line Box：容纳这一整行的行内级内容。

**一个 Line Box 可以容纳多个 Inline Box，而一个元素的 Inline Box 也可能因为换行被拆分成多个片段，分布在多个 Line Box 中**

---
## font-size、line-height 与行盒高度
先区分三个尺寸：

- `font-size`：决定字体使用的 em 方框尺度，不等于可见字形的真实高度。

- `line-height`：控制行内内容参与行高计算的尺寸。

- **Line Box Height**：该行全部行内级内容完成对齐后，行盒的实际布局高度。

例如：
```
.text {
  font-size: 20px;
  line-height: 40px;
}
```

对于简单的纯文本行，Line Box 通常高约 `40px`

但如果同一行出现大字号文字、图片或其他行内级盒，最终 Line Box 可能更高

**因此** `line-height` **不等于 Line Box 的绝对高度，也不是元素的** `height`

### Baseline（基线）
![[Pasted image 20261014180845.png]]

基线是文字排版的重要对齐参考线

![[Pasted image 20261014180901.png]]

字体还有两个相关度量：

- Ascent：字体基线上方的度量距离
- Descent：字体基线下方的度量距离

基线不等于字形底边，也不等于行盒底边

例如英文中的 `g`、`p`、`y` 通常有一部分延伸到基线以下

### Half-leading（半行距）
浏览器需要处理 `line-height` 与字体度量高度之间的差值
![[Pasted image 20261014180937.png]]

经典行内布局模型中：
```
Leading = line-height - (Ascent + Descent)

Half-leading = Leading / 2
```

多出的 Leading 通常平均分配到字体度量区域的上下两侧

注意：**这里比较的是字体度量，不是字形实际可见高度

---
## line-height 的继承
推荐使用无单位 `line-height`：
```
.parent {
  font-size: 20px;
  line-height: 1.5;
}

.child {
  font-size: 40px;
}
```

子元素继承倍率 `1.5`，所以自身使用的行高是：
```
40px × 1.5 = 60px
```

但百分比不一样：
```
.parent {
  font-size: 20px;
  line-height: 150%;
}

.child {
  font-size: 40px;
}
```

百分比在父元素上计算为 `30px`，子元素继承的是这个计算后的长度。

|写法|子元素继承什么|
|---|---|
|`line-height: 1.5`|倍率 `1.5`|
|`line-height: 150%`|父元素计算后的长度|
|`line-height: 1.5em`|父元素计算后的长度|

所以工程中通常优先使用无单位行高，避免子元素字号变化后继承不合适的固定长度

---
## 工程中的常见问题
### 为什么 span 设置 height 不生效？
```
span {
  display: inline;
  height: 100px;
}
```

因为它主要按照行内格式化规则参与排版，不能像块级盒子那样直接用 `height` 设置自身的布局高度。

可以改为：
```
span {
  display: inline-block;
  height: 100px;
}
```

此时它作为一个原子行内级盒参与外部行盒，其自身高度也可能影响行盒高度

### 为什么 line-height 能让单行文字看起来垂直居中？
```
.button {
  height: 40px;
  line-height: 40px;
}
```

在简单单行文本中，行盒与容器的高度恰好接近，视觉上通常可以居中

但遇到换行、图标或不同字体时，这种方式不够可靠

现代组件更推荐：
```
.button {
  min-height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
```

---
## Mental Model
把整个过程串起来：
```
display
   ↓
决定盒子的外部 / 内部显示类型
   ↓
块容器内部存在行内级内容
   ↓
建立 IFC（行内格式化上下文）
   ↓
根据可用宽度和换行规则分行
   ↓
每行形成 Line Box
   ↓
根据 line-height、字体度量、基线和行内级盒计算布局高度
   ↓
最终绘制字形（实际绘制范围可能超出行盒）
```
