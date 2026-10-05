# Display 与 Box
> Last Format Time：10/6/2026 02:27:25

---
## Element 与 Box
CSS 真正参与布局的是 **Box（盒）**，而不是直接对 DOM Element 布局。

```text
DOM Tree
↓ CSS
Box Tree
↓
Layout
```

因此：
```text
Element ≠ Box
DOM Tree ≠ Box Tree
```

一个元素通常会生成 Box，但并非严格一一对应，例如后续的 `display: contents`

---
## 核心模型
https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/display#%E8%AF%AD%E6%B3%95

现代 CSS 中，`display` 可以拆成两个维度：
```text
display
├─ outer display type
└─ inner display type
```

### Outer Display Type
决定当前 Box 自己如何参与父元素的布局。

主要关注：
```text
block
inline
```

### Inner Display Type
决定当前 Box 内部的子元素按照什么布局算法排列。

主要包括：
```text
flow
flow-root
flex
grid
```

因此可以理解为：
```text
outer → 我怎么和兄弟元素布局
inner → 我的孩子怎么布局
```

```css
/* 预组合值 */
display: block;
display: inline;
display: inline-block;
display: flex;
display: inline-flex;
display: grid;
display: inline-grid;
display: flow-root;

/* 盒子抑制 */
display: none;
display: contents;

/* 多关键字语法 */
display: block flex;
display: block flow;
display: block flow-root;
display: block grid;
display: inline flex;
display: inline flow;
display: inline flow-root;
display: inline grid;

/* 其他值 */
display: table;
display: table-row; /* 所有的 table 元素都有等效的 CSS display 值 */
display: list-item;

/* 全局值 */
display: inherit;
display: initial;
display: revert;
display: revert-layer;
display: unset;
```

---
## `block`
```text
display: block;
```

可以理解为：
```text
outer = block
inner = flow
```

在普通流中通常：

- 在 block axis 上依次排列
- 默认使用可用宽度
- 前后表现为换行

但“独占一行”只是普通流中的典型表现，不是 `block` 的完整定义，元素最终如何布局还取决于父级建立的 formatting context

### `display: block` 不等于 BFC
错误：
```text
display: block
=
建立 BFC
```

`display: block` 更准确是：
```text
block flow
```

它使用普通 Flow Layout。

普通 `display: block`：
```text
不一定建立新的 BFC
```

而：
```text
display: flow-root;
```

可理解为：
```text
block flow-root
```

它会建立新的 Block Formatting Context。

因此：
```text
display: block
→ block flow
→ 普通 Flow

display: flow-root
→ block flow-root
→ 新 BFC
```

BFC 后续在 Formatting Context 章节继续深入

---
## `inline`
```text
display: inline;
```

可以理解为：
```text
outer = inline
inner = flow
```

普通 inline box 会参与 **Inline Formatting Context（行内格式化上下文）**，像文字一样在行中排列。

例如：
```text
Hello <span>CSS</span> World
```

整体会参与同一个行内布局。

对于普通 non-replaced inline：
```text
width / height
```

不会像普通 block box 一样直接控制盒子尺寸。

但不能简单说 inline 不能设置 margin / padding / border，更准确：

- 水平方向 padding / margin 可以影响布局
- padding / border 可以绘制
- vertical margin 不会像 block margin 那样正常推动行布局
- width / height 对普通 non-replaced inline 不按 block sizing 方式生效

具体原因后续结合 IFC 学习。

---
##  `inline-block`
```text
display: inline-block;
```

可以理解为：
```text
outer = inline
inner = flow-root
```

因此它：
```text
对外 → 像 inline 一样参与行内布局
对内 → 是一个独立的布局容器
```

所以可以：

- 与其他内容排在同一行
- 正常设置 `width`
- 正常设置 `height`

---
## Flex / Grid
### `display: flex`
```text
outer = block
inner = flex
```

元素自己作为 block-level box 参与父布局；它的子元素使用 Flexbox 算法布局。

### `display: inline-flex`
```text
outer = inline
inner = flex
```

与 `flex` 的区别主要在 **外部布局方式**，内部都是 Flexbox。

同理：
```text
grid
→ outer = block
→ inner = grid

inline-grid
→ outer = inline
→ inner = grid
```

---
## `display: none`
`display: none` 的核心不是“盒子被隐藏”，而是：

> 元素及其后代不生成用于布局的 Box。

mental model：

```text
DOM Tree
   ↓
CSS
   ↓
Box Tree
   ↓
Layout
```

`display: none`：

```text
DOM 中存在
Box Tree 中不存在
不参与 Layout
不占空间
```

因此父元素 `display: none` 时，即使子元素写：

```text
.child {
  display: block;
}
```

子元素仍不会生成布局盒。

和其他隐藏方式区别：

```text
display: none
DOM 有
Box 无
不占空间

visibility: hidden
DOM 有
Box 有
占空间
内容不可见

opacity: 0
DOM 有
Box 有
占空间
整体透明
```

---
##  `contents`
`display: contents`：Element 仍然存在于 DOM，但它自身生成的 Box 被移除，子元素继续生成 Box，例如：
```text
<div class="grid">
  <div class="wrapper">
    <div>A</div>
    <div>B</div>
  </div>
</div>
```

正常 Box Tree：
```text
grid box
└── wrapper box
    ├── A box
    └── B box
```

```text
.wrapper {
  display: contents;
}
```

变为：
```text
grid box
├── A box
└── B box
```

DOM Tree 不变：
```text
grid
└── wrapper
    ├── A
    └── B
```

所以要牢记：
```text
Element !== Box
```

### `display: contents` 对 CSS 的影响
它删除的是元素自己的 Box，而不是 DOM Element，因此：
```text
.wrapper {
  display: contents;

  color: red;
  padding: 20px;
  border: 1px solid;
  background: yellow;
}
```

结果：
```text
color       ✅ 可以继承给子元素

padding     ❌ 没有自己的 Box
border      ❌ 没有自己的 Box
background  ❌ 没有自己的 Box
```

以下机制仍基于 DOM Tree：
```text
Selector Matching
Inheritance
Event Propagation
```

因此 `display: contents` 不等价于删除 DOM 节点。

工程中也不要把它简单当成“删除 wrapper”，特别是具有重要语义 / Accessibility 作用的元素要谨慎使用。

---
## 常见 display 的统一理解
|display|Outer|Inner|
|---|---|---|
|`block`|block|flow|
|`inline`|inline|flow|
|`inline-block`|inline|flow-root|
|`flex`|block|flex|
|`inline-flex`|inline|flex|
|`grid`|block|grid|
|`inline-grid`|inline|grid|

核心记忆：
```text
block / inline
→ 自己如何参与父布局

flow / flow-root / flex / grid
→ 自己内部如何布局 children
```

---
## Replaced Element 替换元素
其内部实际内容不由普通 CSS Formatting Model 排版，CSS 主要控制它生成的 Box。

典型：
```text
<img>
<video>
<iframe>
<embed>
```

例如：
```text
<img src="cat.jpg">
```

图片内部并不是：
```text
<img>
  DOM 内容
</img>
```

图片资源自身负责内容表现，CSS 负责：
```text
位置
宽高
边距
边框
布局参与方式
```

### Replaced Element 尺寸
不能简单背 inline 元素不能设置 width / height。更准确，普通 non-replaced inline 和 replaced inline 的尺寸规则不同

例如：
```text
span {
  width: 200px;
}
```

普通 inline `span` 不会像 block 那样直接受到 `width` 控制

但：
```text
img {
  width: 200px;
}
```

即使 `<img>` 默认以内联级方式参与布局，仍然可以正常设置尺寸

### Intrinsic Dimensions
替换元素通常可以携带自身尺寸信息，例如原图：
```text
1920 × 1080
```

浏览器可以知道：
```text
natural width
natural height
natural aspect ratio
```

这些属于 Intrinsic Size / Intrinsic Dimensions：内在尺寸

后续关系：
```text
Replaced Element
       ↓
Intrinsic Size
       ↓
Intrinsic Sizing
       ↓
Flex / Grid Sizing
```

后续会继续学习：
```text
min-content
max-content
fit-content
```

### Replaced Element 与 `display: contents`
对于普通元素：
```text
自己的 Box 删除
↓
children 的 Box 继续存在
```

但 `<img>` 等 replaced element 没有普通 DOM children 可以继续参与布局。

因此这类元素对：
```text
display: contents;
```

存在特殊处理，一般是改成：
```text
display: none;
```

不要理解成：
```text
删除 img Box
然后把图片内容提升出来
```

图片内容本身并不是普通 child box。

---
## Blockification 块化
某些布局环境会修改元素的 outer display type，使其变成 `block`。


### Flex / Grid 中的 Blockification
例如：
```html
<div class="parent">
  <span>Hello</span>
</div>
```

```css
.parent {
  display: flex;
}
```

`span` 原本：
```text
display: inline

outer = inline
inner = flow
```

但它成为：
```text
Flex Item
```

之后发生 blockification：
```text
inline flow
↓
block flow
```

因此 Flex 里的 `span` 可以表现得不再像普通 inline box

### `inline-flex` 的 Blockification
```text
.child {
  display: inline-flex;
}
```

可以拆成：
```text
outer = inline
inner = flex
```

如果它成为 Flex / Grid Item：
```text
inline flex
↓ blockification
block flex
```

inner layout 保持：
```text
flex
```

主要修改：
```text
outer display type
```

因此：
```text
inline-flex
↓
flex
```

可以通过 outer / inner model 统一理解，而不是死记规则

### 常见触发 Blockification 的情况
重点掌握：
```text
Flex Item
Grid Item
float
absolute positioning
```

这些场景可能导致 `display` 的 computed value 被修正，这也和 CSS Value Pipeline 接上：
```text
declared
→ cascaded
→ specified
→ computed
→ used
→ actual
```

例如：
```text
.child {
  display: inline;
  position: absolute;
}
```

specified：
```text
inline
```

但经过 blockification 后：
```text
computed outer display
→ block
```

Specified Value 不一定等于 Computed Value





---
## Mental Model
以后看到：
```text
.container {
  display: flex;
}
```

不要只理解为：
```text
开启 Flex
```

而应该理解成：
```text
.container
│
├─ 自己怎么参与父布局？
│  └─ block
│
└─ children 怎么布局？
   └─ flex
```

`display` 本质上是 Box Model 与 Formatting Context 之间的连接点

```text
                Element
                   │
                display
                   ↓
              Box Generation
                   │
        ┌──────────┴──────────┐
        │                     │
    是否生成 Box         生成什么 Box
        │                     │
 none / contents        outer + inner
                              │
                  ┌───────────┴───────────┐
                  ↓                       ↓
            Outer Display           Inner Display
                  │                       │
           如何参与父布局           children 怎么布局
                  │                       │
          block / inline        flow / flex / grid
                                          │
                                          ↓
                                Formatting Context
```

另外还存在：
```text
Specified Display
       ↓
布局环境修正
       ↓
Blockification 等 Fixup
       ↓
Computed Display
```

```text
display: none
→ Element 在 DOM
→ 不生成 Box

display: contents
→ Element 在 DOM
→ 自己不生成 Box
→ children 继续生成 Box

Replaced Element
→ 内部内容不由普通 CSS Formatting Model 控制
→ 如 img / video / iframe
→ 常有 intrinsic dimensions

Blockification
→ 修改 outer display type
→ inline → block
→ 常见于 Flex / Grid Item、absolute、float

display: inline-flex
→ inline flex

display: flex
→ block flex

display: inline-grid
→ inline grid

display: grid
→ block grid

display: block
→ block flow
→ 不等于建立 BFC

display: flow-root
→ block flow-root
→ 建立新的 BFC
```

`display` 不只是控制“块级还是行内”，它实际上同时参与：
```text
Box 是否生成
+
Box 如何参与父布局
+
子元素采用哪种布局模型
+
某些布局环境下的 display 自动修正
```

因此完整模型是：
```text
Element
→ Box Generation
→ Outer / Inner Display Type
→ Formatting Context
→ Layout
```
