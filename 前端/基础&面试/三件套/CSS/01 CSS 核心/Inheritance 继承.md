假设我们有这样一段 HTML：
```HTML
<div class="article">
  <h2>文章标题</h2>
  <p>这是一段文字 <span>重点内容</span></p>
</div>
```

我们希望整个文章区域的文字都是红色：
```css
.article {
  color: red;
}
```

虽然 `h2`、`p`、`span` 没有直接设置 `color`，但它们的文字依然可以呈现红色

这是因为 `color` 是一个默认可继承的属性

如果 CSS 没有继承机制，我们就必须给每一个子元素分别设置文本颜色、字体等属性，代码会非常冗余

因此，继承主要解决的是：让子元素自动复用父元素某些属性的值，减少重复声明，并保持视觉风格一致

---
## 核心模型
CSS 继承（Inheritance）指的是：

> 当某个元素没有通过层叠获得某个属性的值时，对于默认可继承的属性，浏览器会使用父元素该属性的计算值（Computed Value）。

这里有三个关键点：

- 继承通常发生在父子元素之间，并且可以逐级向后代传播

- 继承的是父元素属性的==计算值==，不是父元素的 CSS 声明文本

- 继承属于 CSS 属性值确定过程，并不参与选择器特指度竞争

### 继承与层叠
回忆之前学习的 CSS 属性值阶段：
![[Pasted image 20261019232644.png]]

理解这段 CSS：
```css
.parent {
  color: red;
}

.child {
  color: blue;
}
```

```html
<div class="parent">
  <p class="child">Hello CSS</p>
</div>
```

对于 `.child` 的 `color`，它自己存在匹配的 `color: blue` 声明，Cascade 已经选出了 `blue`，所以不需要通过继承获得颜色

继承不会和元素自身匹配到的 CSS 声明比特指度

哪怕父元素使用了：
```css
.parent {
  color: red !important;
}
```

子元素的 `color: blue` 仍然可以生效，因为父元素上的 `!important` 不会跨元素参与子元素的层叠竞争。

### 计算值
例如：
```css
.parent {
  font-size: 20px;
}

.child {
  font-size: inherit;
}
```

子元素继承的是父元素 `font-size` 的计算值，即 `20px`

如果父元素声明：
```
.parent {
  font-size: 1.5em;
}
```

假设父元素自身计算出的字体大小是 `24px`，那么子元素继承得到的是 `24px`，而不是重新把 `1.5em` 计算一次。

这也是 CSS 继承模型中非常重要的一条规则

---
## 可以继承 CSS 属性
CSS 属性分成两大类：默认可继承属性与默认不可继承属性

|默认可继承|默认不可继承|
|---|---|
|`color`|`width`、`height`|
|`font-family`|`margin`、`padding`|
|`font-size`、`font-weight`|`border`|
|`line-height`|`background-color`|
|`text-align`|`display`|
|`visibility`|`position`|
|`letter-spacing`|`overflow`|
|`cursor`|`opacity`|

注意，这只是常见属性的分类，不是完整清单。

可以用一个经验规律帮助记忆：

- 文字、字体、排版类属性：通常可以继承
- 盒模型、布局、背景类属性：通常不能继承

但最终还是以每个属性的规范定义为准

---
## 控制继承
CSS 提供了几个全局关键字（CSS-wide Keywords），可以控制属性值的确定方式

### 强制继承
无论属性默认是否可继承，都可以显式使用 `inherit`
```css
.parent {
  border: 2px solid red;
}

.child {
  border: inherit;
}
```

虽然 `border` 默认不继承，但子元素使用 `inherit` 后，可以继承父元素相应的边框属性值。

### 使用属性初始值
```css
.parent {
  color: red;
}

.child {
  color: initial;
}
```

`initial` 表示使用 CSS 规范定义的属性初始值，而不继承父元素的红色。

注意：`initial` 不是恢复浏览器为 HTML 元素定义的默认样式。例如 `display: initial` 的结果是 `inline`，而不是恢复 `div` 常见的 `block`。

### 根据属性是否可继承自动决定
这是最值得掌握的关键字：
```css
.child {
  color: unset;
  margin: unset;
}
```

- `color` 默认可继承，所以 `unset` 等价于 `inherit`。
- `margin` 默认不可继承，所以 `unset` 等价于 `initial`。

### 回退到较低优先级来源的样式
例如：
```css
button {
  all: revert;
}
```

`revert` 会根据层叠来源回退样式，使浏览器默认样式等较低优先级来源的声明有机会生效。

它和 `initial` 不同，不是简单设置成规范初始值。

另外还有 `revert-layer`，用于回退当前层叠层中的声明。这个和我们之前学的 `@layer` 有关。

|关键字|含义|
|---|---|
|`inherit`|使用父元素的计算值|
|`initial`|使用属性规范初始值|
|`unset`|可继承就继承，否则使用初始值|
|`revert`|根据层叠来源回退|
|`revert-layer`|回退当前层中的声明|
