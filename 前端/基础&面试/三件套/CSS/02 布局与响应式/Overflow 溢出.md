# Overflow 溢出
`overflow` 是 CSS 中用于控制元素内容超出容器边界时，浏览器应该如何处理的属性。

正常情况下，浏览器会尽量根据内容确定元素尺寸。但当元素尺寸受到约束，或者内容本身无法正常换行时，就可能出现溢出（Overflow）。

例如：
```html
<div class="box">
  <div class="content">这是一段非常长的内容……</div>
</div>
```

```css
.box {
  width: 250px;
  height: 100px;
  border: 2px solid black;
}

.content {
  height: 200px;
}
```

这里子元素的高度是 `200px`，而父容器只有 `100px`。

默认情况下，内容并不会被截断，而是继续显示在容器外面，因为：
```css
overflow: visible; /* 默认值 */
```

---
## overflow 属性值

|   |   |
|---|---|
|取值|行为|
|`visible`|默认值，溢出内容继续显示|
|`hidden`|裁剪内容，不显示滚动条，但可以通过程序等方式滚动|
|`clip`|直接裁剪，不支持滚动|
|`auto`|需要时允许滚动，通常在溢出时显示滚动条|
|`scroll`|始终建立滚动容器，传统滚动条通常始终占位或显示|

### 允许溢出
```css
.box {
  overflow: visible;
}
```

内容超出容器仍然可能显示，也不会因为这个属性而建立滚动容器。

注意：溢出内容可见，不意味着它一定不会被外层祖先裁剪。

### 隐藏溢出
```css
.box {
  overflow: hidden;
}
```

这个属性非常常见，例如用于裁剪图片或圆角卡片。

但一个容易忽略的知识点是：`overflow: hidden` 并不意味着完全禁止滚动。

它仍然可以形成滚动容器，只是没有用户直接操作的滚动条。
```
const box = document.querySelector(".box");

box.scrollTop = 100;
box.scrollTo({ top: 100 });
```

上述代码仍然可以使隐藏的内容滚动到可视区域。键盘焦点进入被隐藏的子元素，也可能触发滚动。

### 直接裁剪
```css
.box {
  overflow: clip;
}
```

与 `hidden` 不同：

- 不建立滚动容器。

- 不支持通过 `scrollTop` 等方式滚动。

- 不会仅因为这个属性而创建 BFC。

### 按需滚动
```css
.list {
  height: 300px;
  overflow: auto;
}
```

这是实际项目中非常常见的写法。

例如一个消息列表，消息少时正常显示，消息多时在容器内部滚动，而不会无限撑开页面。

### 始终使用滚动容器
```css
.list {
  height: 300px;
  overflow: scroll;
}
```

即使内容没有溢出，容器仍然具有滚动机制。

与 `auto` 的主要区别在于滚动条呈现策略。但在使用覆盖式滚动条的系统中，`scroll` 也不保证你能始终看到滚动条。

---
## overflow-x 与 overflow-y
`overflow` 实际上是两个属性的简写：

- `overflow-x`：水平方向的溢出处理。
- `overflow-y`：垂直方向的溢出处理。

```css
.box {
  overflow-x: hidden;
  overflow-y: auto;
}

/* 等价于 */
.box {
  overflow: hidden auto;
}
```

### X/Y 轴不是完全独立的
来看一个例子：

```
.box {
  overflow-x: visible;
  overflow-y: auto;
}
```

你可能认为：

- X 轴：允许内容溢出。
- Y 轴：允许滚动。

但实际上，`overflow-x: visible` 的计算值会变成 `auto`。

也就是说，最终相当于：
```
.box {
  overflow-x: auto;
  overflow-y: auto;
}
```

这是 CSS 的计算值规则：当一个轴使用 `hidden`、`scroll`、`auto` 之一时，另一个轴的 `visible` 会计算为 `auto`，`clip` 则会计算为 `hidden`。

这个知识和你之前学习的 Specified Value → Computed Value 正好能够串起来：你声明的值，不一定就是最终计算值。


---
## overflow 与 BFC 的关系
你之前学过 BFC（Block Formatting Context，块级格式化上下文），这里有一个重要联系。

对于满足适用条件的块容器：
```css
.box {
  overflow: hidden;
}
```

会创建新的 BFC。

规则可以归纳成：

|overflow 值|是否创建 BFC|
|---|---|
|`visible`|否|
|`hidden`|是|
|`clip`|否|
|`auto`|是|
|`scroll`|是|

这里说的是由 `overflow` 属性本身引起的 BFC，不排除元素因其他条件已经形成 BFC。

为什么滚动容器需要创建 BFC？

因为 BFC 会隔离内部的浮动布局等行为，避免容器滚动时反复受到外部浮动元素的影响。

以前经常使用：
```
.parent {
  overflow: hidden;
}
```

来包含浮动元素。

但现代 CSS 中，如果只是希望创建 BFC，通常更推荐：
```
.parent {
  display: flow-root;
}
```

这样可以明确表达创建独立格式化上下文的意图，又不会引入多余的裁剪行为。

---
## 常见问题
### Flex 子元素不能正常滚动
这是很典型的项目问题。
```html
<div class="layout">
  <header>Header</header>
  <main>很多很多内容...</main>
</div>
```

```css
.layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

header {
  height: 60px;
  flex-shrink: 0;
}

main {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
}
```

这里的关键是：
```
min-height: 0;
```

Flex Item 默认的自动最小尺寸可能受内容影响，使子元素不愿意缩小，从而导致外层布局被撑开。

对于需要滚动的 Flex Item，`overflow: auto` 本身也会影响自动最小尺寸的计算；显式设置 `min-height: 0` 则能清晰保证该元素允许收缩。对于横向 Flex 布局，同样经常使用 `min-width: 0`。

这在后台管理系统、聊天页面、左右分栏布局中很常见。

### overflow: hidden 会影响 sticky
```css
.wrapper {
  overflow: hidden;
}

.header {
  position: sticky;
  top: 0;
}
```

`position: sticky` 会根据最近的相关滚动容器确定其吸附参照。

而 `overflow: hidden` 也会建立滚动机制，即使这个容器没有实际滚动。

因此，`.header` 可能不再按照你预期的页面滚动发生吸附。

如果 `.wrapper` 只是为了裁剪内容，可以考虑：
```
.wrapper {
  overflow: clip;
}
```

这也是现代 `clip` 相较于 `hidden` 的实际价值之一。

### 动态滚动条导致布局抖动
```
.list {
  overflow-y: auto;
  scrollbar-gutter: stable;
}
```

`scrollbar-gutter: stable` 可以为传统滚动条预留空间，减少滚动条出现或消失时造成的布局变化。不过，对于覆盖式滚动条，它不会强制预留空间。
