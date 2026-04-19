# CSS 经典面试题 45 题（完整版·修正定稿）
所有题目均已纠错、统一表述，可直接用于复习/背诵。

---

## 1 介绍一下标准的CSS盒子模型？与低版本IE的盒子模型有什么不同？
- **标准W3C盒子模型**
  元素总宽度 = `content(width设置值)` + `padding` + `border` + `margin`
  `width/height` 只设置**内容区**大小。

- **低版本IE（怪异模式）盒子模型**
  元素总宽度 = `(content + padding + border)`(width设置值) + `margin`
  `width/height` 包含**内容 + 内边距 + 边框**。

---

## 2 box-sizing属性？
用来控制元素的盒子模型解析模式，默认为 `content-box`。

- `content-box`：标准盒模型，`width/height` 只作用于内容区。
- `border-box`：怪异盒模型，`width/height` 包含内容 + padding + border。

---

## 3 CSS选择器有哪些？哪些属性可以继承？优先级？
**选择器**：
id选择器(#id)、类选择器(.class)、标签选择器(div/p/h1)、相邻兄弟选择器(h1+p)、子选择器(ul>li)、后代选择器(ul li)、通配符(*)、属性选择器(a[href])、伪类选择器(a:hover)、伪元素选择器(::before)。

**可继承属性**：
`font-size`、`font-family`、`color`、`line-height`、`text-align` 等文字文本类属性。

**不可继承属性**：
`border`、`padding`、`margin`、`width`、`height`、`background` 等。

**优先级**：
`!important` > 内联样式 > id选择器 > 类/属性/伪类 > 标签/伪元素 > 继承样式。

---

## 4 CSS优先级算法如何计算？
权重按四位数计算：千、百、十、个。

- 内联样式：1000
- id选择器：100
- 类、属性、伪类选择器：10
- 标签、伪元素选择器：1
- 通配符 `*`：0

规则：
1. `!important` 优先级最高。
2. 权重相同，后面定义的样式覆盖前面的。
3. 继承样式优先级最低。

---

## 5 CSS3新增伪类有哪些？
- `:first-of-type`、`:last-of-type`
- `:only-of-type`、`:only-child`
- `:nth-child(n)`、`:nth-of-type(n)`
- `:enabled`、`:disabled`
- `:checked`
- `:not()` 等

---

## 6 如何居中div？如何居中浮动元素？绝对定位div如何居中？
### 普通块级 div 水平居中
```css
width: 100px;
margin: 0 auto;
```

### 浮动元素居中
```css
float: left;
position: absolute;
left: 50%;
top: 50%;
transform: translate(-50%, -50%);
```

### 绝对定位元素居中（通用）
```css
position: absolute;
left: 0;
right: 0;
top: 0;
bottom: 0;
margin: auto;
```

### 现代通用居中（Flex）
```css
.parent {
  display: flex;
  justify-content: center;
  align-items: center;
}
```

---

## 7 display有哪些值？作用？
- `inline`：行内元素，不换行，宽高无效。
- `block`：块级元素，独占一行，可设宽高。
- `inline-block`：行内块，不换行且可设宽高。
- `none`：隐藏元素，不占空间。
- `list-item`：列表项。
- `table`：表格布局。
- `flex`：弹性布局。
- `grid`：网格布局。

---

## 8 position的值？
- `static`：默认，正常文档流。
- `relative`：相对定位，不脱离文档流，相对自身偏移。
- `absolute`：绝对定位，脱离文档流，相对于最近非static父级定位。
- `fixed`：固定定位，相对于视口。
- `sticky`：粘性定位，滚动到阈值后固定。

---

## 9 CSS3有哪些新特性？
1. RGBA、透明度 opacity
2. 背景增强：`background-size`、`background-origin`
3. 文字换行 `word-wrap: break-word`
4. 文字阴影 `text-shadow`
5. 自定义字体 `@font-face`
6. 圆角 `border-radius`
7. 边框图片 `border-image`
8. 盒子阴影 `box-shadow`
9. 渐变 `linear-gradient`/`radial-gradient`
10. 过渡 `transition`、动画 `animation`
11. 媒体查询、2D/3D变换 `transform`
12. 弹性布局 `flex`、网格布局 `grid`

---

## 10 解释CSS3 flexbox及适用场景？
Flex 是弹性盒布局，用于更高效地对容器内项目进行排列、对齐、分配空间。
适用场景：移动端布局、PC端响应式、导航栏、卡片列表、各种居中与自适应布局。

---

## 11 用纯CSS创建三角形的原理？
将元素宽高设为0，利用边框宽度和颜色实现三角形。
```css
width: 0;
height: 0;
border: 40px solid transparent;
border-bottom-color: red;
```

---

## 12 一个满屏品字布局如何设计？
1. 上方一个块级元素，`margin: 0 auto` 居中。
2. 下方两个盒子宽度各50%，使用 `float` 或 `flex` 并排。
3. 整体高度100vh，实现满屏品字。

---

## 13 常见的兼容性问题？
1. 浏览器默认margin/padding不一致。
2. IE6浮动双边距bug，添加 `display:inline` 解决。
3. IE浏览器Hack：`\9`、`+`、`_` 区分版本。
4. 小高度元素在IE6/7被撑高，用 `overflow:hidden` 修复。
5. Chrome 小于12px字体强制放大，用 `scale` 缩放。
6. 链接样式顺序错乱，遵循 LVHA：`link` → `visited` → `hover` → `active`。

---

## 14 为什么要初始化CSS样式？
不同浏览器对标签有默认样式，初始化可统一表现，避免布局差异。
常用：`* { margin: 0; padding: 0; box-sizing: border-box; }`

---

## 15 absolute的containing block计算方式跟正常流有什么不同？
- `static/relative`：包含块为父元素内容区。
- `absolute`：包含块为最近的 `position` 不为 static 的祖先元素。
- `fixed`：包含块为视口。
- 祖先为行内元素时，包含块为其第一行和最后一行行框的最小包围盒。

---

## 16 CSS里visibility:collapse在不同浏览器下的区别？
- 用于**普通元素**：所有浏览器表现同 `visibility:hidden`，保留空间。
- 用于**表格元素**：隐藏行/列并释放空间，效果类似 `display:none`。

---

## 17 display:none与visibility:hidden的区别？
- `display:none`：不渲染，不占空间，引发回流+重绘。
- `visibility:hidden`：隐藏但占空间，只触发重绘。

---

## 18 position跟display、overflow、float相互叠加后会怎样？
- 元素设为 `absolute/fixed` 后，`float` 失效。
- 浮动或绝对定位元素，`display` 会自动变为 `block`。
- `overflow:hidden` 可触发BFC，清除浮动影响。

---

## 19 对BFC（块级格式化上下文）的理解？
BFC是一块独立渲染区域，内部布局不影响外部。

**特点**：
1. 内部盒子垂直排列。
2. 同BFC内垂直margin会重叠。
3. BFC区域不会与浮动元素重叠。
4. 计算BFC高度时，浮动元素参与计算。

**触发条件**：
- 根元素 html
- `float` 不为 none
- `overflow` 不为 visible
- `display: inline-block / table-cell / flex`
- `position: absolute / fixed`

---

## 20 为什么会出现浮动？何时清除浮动？清除方式？
浮动使元素脱离文档流，左右排列。
会导致**父元素高度塌陷**，因此需要清除浮动。

**清除方式**：
1. 父元素设置固定高度。
2. 末尾添加空标签 `clear:both`。
3. 父元素 `overflow:hidden/auto`。
4. 伪元素清除法（推荐）：
```css
.clearfix::after {
  content: "";
  display: block;
  clear: both;
}
```

---

## 21 上下margin重合问题及解决？
相邻块级元素垂直margin会合并取最大值。
解决：给其中一个元素包裹父容器，并触发父容器为BFC（如 `overflow:hidden`）。

---

## 22 设置元素浮动后，该元素的display值是多少？
自动变为 `display:block`。

---

## 23 移动端布局用过媒体查询吗？
用过，通过 `@media` 根据屏幕宽度应用不同样式。
```css
@media screen and (max-width: 768px) {
  /* 移动端样式 */
}
```

---

## 24 使用CSS预处理器吗？
常用：Less、Sass / Scss、Stylus。
优点：支持变量、嵌套、混合、函数、模块化。

---

## 25 CSS优化、提高性能的方法有哪些？
1. 避免层级过深的选择器。
2. 减少通配符和冗余选择器。
3. 提取公共样式，避免重复。
4. 慎用 `!important`。
5. 使用类选择器，减少id和标签滥用。
6. 合理使用CSS Sprites，减少HTTP请求。
7. 压缩CSS文件。

---

## 26 浏览器是怎样解析CSS选择器的？
**从右向左解析**。
先匹配最右侧选择器，再向上逐级匹配父元素，可快速过滤无效节点，提升性能。

---

## 27 网页中应该用奇数还是偶数字体？为什么？
优先使用**偶数字号**。
Windows 点阵宋体在12、14、16px显示清晰；奇数号易模糊、稀疏。

---

## 28 margin和padding分别适合什么场景？
**margin**：
- 元素外部间距。
- 不需要背景色。
- 相邻盒子间距希望合并。

**padding**：
- 元素内部留白。
- 留白区域需要背景色。
- 希望间距不合并。

---

## 29 元素竖向百分比设定是相对于容器高度吗？
不是。
`padding-top/bottom`、`margin-top/bottom` 的百分比，**均相对于父元素宽度**。

---

## 30 全屏滚动的原理是什么？用到哪些CSS属性？
原理：外层容器高度100vh，`overflow:hidden`，内部多屏高度100%，通过 `transform` 或 `margin` 纵向切换。
用到：`overflow:hidden`、`transition`、`transform`、`height:100%`。

---

## 31 什么是响应式设计？原理？如何兼容低版本IE？
响应式设计：一套代码适配多设备（PC/手机/平板）。
原理：媒体查询 + 流式布局 + flexible / rem。
必须设置viewport：
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```
低版本IE可引入 `respond.js` 支持媒体查询。

---

## 32 视差滚动效果？
滚动时，背景层移动速度慢于前景层，形成立体层次感。
实现方式：CSS3 `background-attachment`、JS监听滚动控制 `transform`、第三方插件。

---

## 33 ::before 和 :after 双冒号与单冒号区别？
- 单冒号 `:before`：CSS2 语法，兼容所有浏览器。
- 双冒号 `::before`：CSS3 规范，用于**伪元素**，与伪类做区分。
作用：在元素内容前后插入虚拟元素，不进入DOM，常用于图标、清除浮动、装饰。

---

## 34 你对line-height如何理解？
行高是两行文字基线之间的距离。
- 单行文本垂直居中：`line-height = height`。
- 无height时，元素高度由line-height决定。
- 多行文本垂直居中可结合 `inline-block` 或flex实现。

---

## 35 怎么让Chrome支持小于12px的文字？
```css
font-size: 10px;
transform: scale(0.8);
transform-origin: left center;
```

---

## 36 让页面字体变清晰、变细用CSS怎么做？
```css
-webkit-font-smoothing: antialiased;
-moz-osx-font-smoothing: grayscale;
```

---

## 37 position:fixed在Android下无效怎么处理？
设置正确viewport，禁止用户缩放：
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0,
user-scalable=no, maximum-scale=1.0">
```

---

## 38 手动写动画最小时间间隔是多久？
多数显示器 60Hz，1秒刷新60次。
最小间隔：`1000 / 60 ≈ 16.7ms`。

---

## 39 li之间有看不见空白间隔原因与解决？
原因：HTML中li之间换行/空格被解析为文本节点，产生间隙。
解决：
1. 去掉li之间换行空格。
2. 父元素 `font-size:0`，li再恢复字号。
3. li浮动 `float:left`。

---

## 40 display:inline-block什么时候显示间隙？
1. 标签之间有空格、换行。
2. 字符间距、字号影响。
解决：移除空格、父级 `font-size:0`、使用负margin。

---

## 41 高度自适应div内，一个100px，另一个填满剩余高度？
```css
.parent {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.box1 { height: 100px; }
.box2 { flex: 1; }
```

---

## 42 png、jpg、gif、webp介绍与使用场景？
- **png**：无损压缩，支持透明，适合图标、UI。
- **jpg**：有损压缩，体积小，适合照片、大图。
- **gif**：支持动画，仅256色，适合简单动图。
- **webp**：谷歌格式，兼具有损无损与透明，体积更小，兼容性逐步完善。

---

## 43 style标签写在body前与body后区别？
- 写在 `<head>` 内：样式先加载，页面正常渲染。
- 写在 `body` 后：浏览器先渲染无样式页面，解析到CSS后重新渲染，可能出现**FOUC闪烁**。

---

## 44 overflow属性定义溢出内容如何处理？
- `visible`：默认，溢出可见。
- `hidden`：溢出隐藏。
- `scroll`：始终显示滚动条。
- `auto`：内容溢出时自动显示滚动条。

---

## 45 阐述一下CSS Sprites（精灵图）
将多个小图标合并到一张图片，通过 `background-position` 定位显示。
优点：减少HTTP请求，提升加载速度，减少图片资源数量。