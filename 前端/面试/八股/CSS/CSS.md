# CSS
### 【Q009】如何实现一个元素的水平垂直居中 ⌚️
**已知宽高**：
```css
/* 方案1：absolute + margin 负值 */
.parent { position: relative; }
.child { position: absolute; top: 50%; left: 50%; margin-left: -50px; margin-top: -50px; width: 100px; height: 100px; }

/* 方案2：absolute + margin auto (推荐) */
.child { position: absolute; top: 0; left: 0; right: 0; bottom: 0; margin: auto; width: 100px; height: 100px; }
```

虽然 justify-content 的值很丰富，但在日常开发中，90% 的布局场景使用 flex-start、center、space-between 和 space-evenly 就完全足够了。其他的值通常用于处理一些特殊的国际化排版（如 RTL 语言）或极端的溢出兼容场景。

**未知宽高**：
```css
/* 方案3：absolute + transform */
.child { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); }

/* 方案4：Flexbox (最常用) */
.parent { display: flex; justify-content: center; align-items: center; }

/* 方案5：Grid */
.parent { display: grid; place-items: center; }

/* 方案6：行内元素 */
.parent { text-align: center; line-height: 200px; }
```

### 【Q017】css 如何实现左侧固定300px，右侧自适应的布局
```css
/* 方案1：float */
.left { float: left; width: 300px; }
.right { margin-left: 300px; }

/* 方案2：absolute */
.parent { position: relative; }
.left { position: absolute; left: 0; width: 300px; }
.right { margin-left: 300px; }

/* 方案3：Flexbox */
.parent { display: flex; }
.left { flex: 0 0 300px; width: 300px; }
.right { flex: 1; }

/* 方案4：Grid */
.parent { display: grid; grid-template-columns: 300px 1fr; }

/* 方案5：calc */
.left { float: left; width: 300px; }
.right { float: right; width: calc(100% - 300px); }
```

### 【Q034】如何实现一个 loading 动画
```css
/* 旋转圆环 */
@keyframes spin {
  to { transform: rotate(360deg); }
}
.loader {
  width: 40px; height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* 弹跳点 */
@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}
.dot { display: inline-block; width: 12px; height: 12px; border-radius: 50%; background: #333; animation: bounce 1.4s infinite ease-in-out both; }
.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }
```

### 【Q175】如何使用 css 写一个魔方
用 3D 变换 + 多个面构建（核心思路）：每个面是一个 div，通过 `transform: rotateX/Y/Z` 和 `translateZ` 定位到立方体各面中心。需要 `perspective` 配合 `transform-style: preserve-3d`，然后旋转整个立方体容器来展示魔方效果。最终可使用 CSS 变量映射颜色面。

### 【Q178】如何使用 css 写一个有 3D 效果的立方体
```css
.cube {
  width: 200px; height: 200px;
  position: relative;
  transform-style: preserve-3d;
  transform: rotateX(-30deg) rotateY(30deg);
}
.face {
  position: absolute;
  width: 200px; height: 200px;
  opacity: 0.8;
}
.front  { transform: translateZ(100px); }
.back   { transform: rotateY(180deg) translateZ(100px); }
.right  { transform: rotateY(90deg) translateZ(100px); }
.left   { transform: rotateY(-90deg) translateZ(100px); }
.top    { transform: rotateX(90deg) translateZ(100px); }
.bottom { transform: rotateX(-90deg) translateZ(100px); }
```
六个面通过 `rotate` 确定朝向 + `translateZ(100px)`（半边长）移出中心。父容器设置 `perspective` 和 `transform-style: preserve-3d`。

### 【Q184】有没有使用过 css variable，它解决了哪些问题
**CSS 变量（自定义属性）**：`--color: red;`，使用 `var(--color)`

**解决的问题**：
1. **统一主题切换**：修改根变量一键换肤
2. **减少重复**：颜色/间距等全局值定义一次，处处引用
3. **动态修改**：JS 通过 `el.style.setProperty('--color', 'blue')` 更新变量
4. **继承和作用域**：在任意选择器中定义，子元素继承
5. **与预处理器的区别**：CSS 变量是运行时（非编译时），可以动态计算
6. **组合使用**：`var(--n, 10px)` 默认值、`calc(var(--n) * 2)` 计算

### 【Q185】谈谈你对 styled-component 的看法
**优点**：
1. **真正的 CSS-in-JS**：样式和组件在一起，删除组件即删除所有样式
2. **自动作用域**：不会有样式冲突
3. **动态样式**：基于 props 动态生成样式
4. **支持主题**：ThemeProvider 全局主题
5. **自动厂商前缀**：类似 Autoprefixer
6. **SSR 支持**：服务端渲染样式收集

**缺点**：
1. 运行时开销（新版本支持编译时提取）
2. 包体积增大
3. JS Bundle 中包含 CSS
4. 调试困难（生成的类名不可读）
5. 与原生 CSS 工具链差异大（不能用 PostCSS 等传统工具）

### 【Q190】使用 CSS 如何画一个三角形
```css
/* 利用 border 宽度 + 透明色实现 */
.triangle {
  width: 0;
  height: 0;
  border-left: 50px solid transparent;
  border-right: 50px solid transparent;
  border-bottom: 100px solid red;
  /* 修改 border-bottom 方向即可改变三角形朝向 */
}
/* 不同方向 */
.up    { border-bottom: 50px solid red;    border-left/right: 50px solid transparent; }
.down  { border-top: 50px solid red;       border-left/right: 50px solid transparent; }
.left  { border-right: 50px solid red;     border-top/bottom: 50px solid transparent; }
.right { border-left: 50px solid red;      border-top/bottom: 50px solid transparent; }
```

### 【Q279】display: inline 的元素设置 margin 和 padding 会生效吗
- **margin**：左右生效，上下**不生效**
- **padding**：左右生效且占据空间，上下**部分生效**——元素内容的背景/边框扩展但**不占据实际布局空间**（即不会撑开父元素的行高，可能会和相邻行重叠）
- **border**：与 padding 行为类似
原因：inline 元素布局在一行中，上下高度由 line-height 和 vertical-align 控制，不扩展行内空间。

### 【Q280】html 的默认 display 属性是多少
HTML 元素的默认 display 取决于元素类型：
- **块级元素**（div、p、h1-h6、section、header、footer、ul、ol、form 等）：`display: block`
- **行内元素**（span、a、strong、em、i、b、label 等）：`display: inline`
- **行内块元素**（img、input、textarea、select、button 等）：`display: inline-block`
- **表格类**：`display: table`、`table-row`、`table-cell` 等
- **列表项**：`display: list-item`
- **隐藏元素**：`display: none`（head、script、style、meta 等）

### 【Q281】响应式布局需要注意哪一些
[[响应式布局&移动端优先 ⌚️]]
1. **视口 meta 标签**：`<meta name="viewport" content="width=device-width, initial-scale=1">`
2. **媒体查询断点**：移动优先设计（min-width），合理断点（576, 768, 992, 1200）
3. **弹性单位**：使用 %/vw/vh/rem/em，避免固定 px 宽度
4. **Flexbox/Grid 布局**：更容易实现自适应
5. **图片响应式**：`max-width: 100%; height: auto;`，`srcset`/`picture` 元素
6. **字体大小**：使用 rem/em，考虑不同设备可读性
7. **触摸友好**：按钮/链接最小 44x44px，间距合适
8. **隐藏/显示内容**：不同设备展示不同内容
9. **容器查询（Container Queries）**：基于容器而非视口做响应（现代方案）

### 【Q282】对一个非定长宽的块状元素如何做垂直水平居中
```css
/* 方案1：Flexbox（推荐） */
.parent { display: flex; justify-content: center; align-items: center; }

/* 方案2：Grid */
.parent { display: grid; place-items: center; }

/* 方案3：absolute + transform */
.parent { position: relative; }
.child { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); }

/* 方案4：table-cell（不推荐，但古老兼容性好） */
.parent { display: table-cell; text-align: center; vertical-align: middle; width: 500px; height: 500px; }
```

### 【Q306】如何实现左右固定，中间自适应布局
```css
/* 方案1：Flexbox (推荐) */
.container { display: flex; }
.left { width: 200px; }
.middle { flex: 1; }
.right { width: 200px; }

/* 方案2：Grid */
.container { display: grid; grid-template-columns: 200px 1fr 200px; }

/* 方案3：float + margin（HTML 结构需要 right 在 middle 前） */
.left { float: left; width: 200px; }
.right { float: right; width: 200px; }
.middle { margin: 0 200px; }

/* 圣杯布局 / 双飞翼布局（传统 float 方案，省略具体代码） */
```

### 【Q307】如何实现表格单双行条纹样式
```css
/* 使用 :nth-child 伪类选择器 */
tr:nth-child(odd) { background-color: #f2f2f2; }   /* 奇数行 */
tr:nth-child(even) { background-color: #ffffff; }   /* 偶数行 */

/* 或 */
tr:nth-child(2n) { background-color: #f2f2f2; }
tr:nth-child(2n+1) { background-color: #ffffff; }
```

### 【Q309】简述下 css specificity
**CSS 优先级（Specificity）** 计算规则（由高到低）：
1. **!important**：最高优先级（尽量少用）
2. **行内样式**（style 属性）：(1,0,0,0)
3. **ID 选择器**：(0,1,0,0) 每个 ID +1
4. **类选择器/属性选择器/伪类**：(0,0,1,0) 每个 class/[attr]/:pseudo +1
5. **元素选择器/伪元素**：(0,0,0,1) 每个 element/::pseudo +1
6. **通配符**：* 为 (0,0,0,0)，无贡献

**同优先级时后声明的生效**。比较时从左到右逐位比较。

### 【Q315】'+' 与 '~' 选择器有什么不同
- **'+' 相邻兄弟选择器**：只选中**紧跟在后面**的第一个兄弟元素。`h1 + p` 选中紧跟在 h1 后的第一个 p。
- **'~' 通用兄弟选择器**：选中**后面所有**兄弟元素。`h1 ~ p` 选中 h1 后面的所有 p 兄弟。

两者都只能选中**后面的**兄弟元素（CSS 不能向前选择）。

### 【Q317】有哪些 css 属性不能展示动画效果
**不能被 transition/animation 动画化的属性**：
- `display`（从 none→block 无动画）
- `visibility`（可以动画，但是离散的）
- `background-image`（渐变→渐变不能平滑过渡，但可用多个/伪元素模拟）
- `font-family`
- `position`
- `overflow`
- `white-space`
- `text-align`
- `flex-direction`、`grid-template-*`

**可动画的属性类型**：数值（opacity, width, color, transform）、颜色（color, background-color）、变换（transform 函数的矩阵计算）。

### 【Q319】css 动画与 js 动画哪个性能更好
**一般 CSS 动画性能更好**，但不是绝对的：

**CSS 动画优势**：
- 浏览器可将其交给 GPU 处理（transform、opacity 触发合成层）
- JS 主线程阻塞时 CSS 动画不受影响
- 代码简洁

**JS 动画优势（requestAnimationFrame）**：
- 更灵活的控制（暂停、回退、动态曲线）
- 复杂物理效果（如弹跳、碰撞）
- IE 兼容性更好

**关键**：选择 transform/opacity 做动画（不管 CSS 还是 JS），避免触发 layout（width/height/left/top 等改变几何的属性），这些属性只在合成阶段，性能最好。

### 【Q321】css 中属性选择器及类选择器的权重哪个高
**相同权重**。属性选择器 `[type="text"]` 和类选择器 `.class` 都是 (0,0,1,0)，平级。具体规定：属性选择器、类选择器和伪类选择器权重相同。后声明的生效。

### 【Q324】为什么会发生样式抖动
**样式抖动（Layout Jank / CLS）** 的原因：
1. **异步加载的内容尺寸未知**：图片/广告/iframe 加载后撑开布局
2. **Web 字体加载后文本重排**：FOUT/FOIT
3. **动态注入内容**：JS 修改 DOM 导致重排
4. **动画使用了非合成属性**：改变 width/height/left/top 触发重排

**解决方案**：
- 图片设置 `width/height` 或 `aspect-ratio` 预留空间
- 字体使用 `font-display: fallback/optional`
- 动画使用 `transform`/`opacity`
- 使用 `will-change` 或 `transform: translateZ(0)` 创建合成层

### 【Q334】position: sticky 如何工作，适用于哪些场景
**工作原理**：元素在滚动到指定偏移量前表现为 `relative`，到达阈值后固定表现为 `fixed`。需要指定 `top/bottom/left/right` 中至少一个值。粘性定位相对于最近的滚动祖先（overflow: scroll/auto/hidden 的元素）生效。

**适用场景**：
- 表格固定表头
- 侧边栏跟随滚动
- 长列表中字母索引（通讯录）
- 分类标题粘性顶栏

```css
.header { position: sticky; top: 0; z-index: 10; }
```

### 【Q335】什么是层叠上下文 (stacking context)，谈谈对它的理解
层叠上下文是 HTML 中元素在 Z 轴上排列的三维概念。决定元素覆盖顺序的不是简单的 z-index 值大小。形成层叠上下文的常见条件：
- 根元素（HTML）
- `position: relative/absolute/fixed` + `z-index` 不为 auto
- `opacity` < 1
- `transform`、`filter`、`perspective` 不为 none
- `isolation: isolate`
- `will-change` 指定了上述属性
- 容器使用 `display: flex|grid` + `z-index` 不为 auto

**层叠顺序**（从下到上）：background → 负 z-index → block 盒 → float → inline → z-index: auto/0 → 正 z-index

### 【Q336】你用 css 实现过什么不错的效果
开放题，可以举例：
- 骨架屏加载动画（带 shimmer 效果）
- 3D 卡片翻转动画
- 纯 CSS 的 tooltip/下拉菜单
- 视差滚动效果
- 自定义 Checkbox/Switch 样式
- 渐变边框按钮
- 毛玻璃效果（backdrop-filter）
- CSS 实现音频可视化动效
- 滚动进度条指示器

### 【Q337】你做前端有多少时间花在写 css 上
开放题。建议回答结合实际项目情况（还原设计稿、响应式、动画等），不固定比例。可以提一下真实项目中 CSS 的难点在哪里，以及如何协作（设计规范、组件库、样式系统）。

### 【Q339】伪类与伪元素有什么区别
- **伪类（`:`单冒号）**：选择处于**特定状态**的元素（一个）。如 `:hover`、`:focus`、`:first-child`、`:nth-child()`。像一个"状态"
- **伪元素（`::` 双冒号）**：创建文档树中**不存在的抽象元素**。如 `::before`、`::after`、`::first-line`、`::selection`。像一个"元素"
- 现代浏览器都支持 `::before/::after`，旧 CSS2.1 用 `:before`（向后兼容）

### 【Q364】css 如何匹配前N个子元素及最后N个子元素
```css
/* 前N个 */
:nth-child(-n+3) { }  /* 前3个 */
/* 最后N个 */
:nth-last-child(-n+3) { }  /* 最后3个 */

/* 排除前N个（从第N+1个开始） */
:nth-child(n+4) { }  /* 第4个开始 */

/* 限制范围，第2到第5个之间 */
:nth-child(n+2):nth-child(-n+5) { }
```

### 【Q370】如何使用 CSS 实现网站的暗黑模式 (Dark Mode)
```css
/* 方案1：prefers-color-scheme（自动跟随系统） */
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1a1a1a;
    --text: #e0e0e0;
  }
}

/* 方案2：CSS 类切换（手动开关更灵活） */
:root[data-theme="dark"] {
  --bg: #1a1a1a;
  --text: #e0e0e0;
}
document.documentElement.setAttribute('data-theme', 'dark');

/* 方案3：结合两种 */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme]) { /* 默认跟随系统 */ }
}
```

### 【Q444】介绍 CSS 隐藏页面中某个元素的几种方法
1. `display: none`：从渲染树移除，不占空间，事件失效
2. `visibility: hidden`：不可见但**占据空间**，事件失效
3. `opacity: 0`：视觉透明但占据空间，**可交互**（仍能点击）
4. `width: 0; height: 0; overflow: hidden;`：收缩为零
5. `position: absolute; left: -9999px;`：移到屏幕外
6. `clip-path: circle(0)`：裁剪为 0
7. `transform: scale(0)`：缩放到 0
8. `hidden` 属性（HTML 标准）等价于 `display: none`

### 【Q465】css 如何实现响应式布局大屏幕三等分、中屏幕二等分、小屏幕一等分
```css
/* 使用 Flexbox + 媒体查询 */
.row { display: flex; flex-wrap: wrap; }
.col { flex: 1 1 33.33%; }
@media (max-width: 992px) { .col { flex: 1 1 50%; } }
@media (max-width: 576px) { .col { flex: 1 1 100%; } }

/* 使用 Grid（更简洁） */
.row { display: grid; grid-template-columns: repeat(3, 1fr); }
@media (max-width: 992px) { .row { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 576px) { .row { grid-template-columns: 1fr; } }

/* 不使用媒体查询（现代简洁方式） */
.row { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }
```

### 【Q468】前端开发中如何进行多主题配置
```css
/* 1. CSS 变量 + data 属性 */
:root { --bg: white; --text: black; }
[data-theme="dark"] { --bg: #1a1a1a; --text: #e0e0e0; }
[data-theme="blue"] { --bg: #e8f4fd; --text: #1a3a5c; }

/* 2. JS 切换主题 */
function setTheme(name) {
  document.documentElement.setAttribute('data-theme', name);
  localStorage.setItem('theme', name);
}

/* 3. 预处理器（编译时多主题） */
// Less/Sass 的变量 + 编译多份 CSS 文件

/* 4. CSS-in-JS 方案：styled-components ThemeProvider */
```

### 【Q471】如何自定义滚动条的样式
```css
/* WebKit 浏览器（Chrome/Safari/Edge） */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 4px; }
::-webkit-scrollbar-thumb { background: #888; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #555; }

/* Firefox */
* { scrollbar-width: thin; scrollbar-color: #888 #f1f1f1; }
```

### 【Q478】如何实现容器中子元素三个三列布局，子元素两个则两列布局
```css
/* 方案1：Grid + auto-fit（推荐） */
.container { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }

/* 方案2：Flexbox + :has()（现代方案） */
.container { display: flex; flex-wrap: wrap; }
.item { flex: 1 1 calc(100% / 3); }
/* 有2个子元素时：:has(.item:last-child:nth-child(2)) 下改 width */
```

### 【Q481】网站设置字体时，如何设置优先使用系统默认字体
```css
/* 各平台最优字体栈 */
body {
  font-family:
    /* macOS/iOS */
    -apple-system, BlinkMacSystemFont,
    /* Windows */
    "Segoe UI",
    /* Android */
    Roboto,
    /* Linux */
    "Helvetica Neue", Arial,
    /* 通用无衬线 */
    sans-serif;
}
```
比写 `Arial` 更优：利用各系统的原生 UI 字体（SF Pro、Segoe UI、Roboto），无需下载，渲染快，用户熟悉。

### 【Q485】写 CSS 时如何避免命名样式冲突
1. **CSS Modules**：`import styles from './App.module.css'`，类名自动哈希
2. **CSS-in-JS**：styled-components、Emotion 等自动生成唯一类名
3. **BEM 命名法**：`.block__element--modifier`
4. **Scoped CSS**（Vue）：`<style scoped>` 组件内样式隔离
5. **Shadow DOM**：完全样式隔离
6. **命名空间前缀**：`.myapp-header`、`.myapp-footer`
7. **CSS @layer**：分层的优先级控制

### 【Q492】CSS 如何设置方格背景
```css
/* 方案1：linear-gradient 相交叉 */
.grid-bg {
  background:
    linear-gradient(90deg, rgba(0,0,0,0.1) 1px, transparent 1px),
    linear-gradient(rgba(0,0,0,0.1) 1px, transparent 1px);
  background-size: 20px 20px;
}

/* 方案2：conic-gradient（棋盘格） */
.checkerboard {
  background: conic-gradient(#eee 90deg, #ccc 90deg 180deg, #eee 180deg 270deg, #ccc 270deg);
  background-size: 40px 40px;
}

/* 方案3：SVG data-uri 背景 */
```

### 【Q496】如何更好地给元素设置 z-index
1. **建立 z-index 体系**：定义变量如 header(100)、modal(200)、tooltip(300)
2. **避免 z-index 竞赛**（不要随便 `z-index: 9999`）
3. **理解层叠上下文**：z-index 只在同一个层叠上下文中比较
4. **使用 isolation: isolate** 创建新的层叠上下文，不污染全局
5. **让 z-index 语义化**：低值用于普通内容，高值用于悬浮层
6. 不要用超大随机 z-index 值解决覆盖问题

### 【Q504】画一个 100x100 的方框，其中文字可以正常换行，文字过多超过方框显示滚动条
```css
.box {
  width: 100px;
  height: 100px;
  overflow: auto;         /* 超出显示滚动条 */
  word-wrap: break-word;  /* 长单词或 URL 可以换行 */
  word-break: break-all;  /* 任意字符处都可换行（确保换行） */
}
```
HTML：`<div class="box">很多很长的文字...</div>`

### 【Q506】Grid 布局如何实现类似 flex: row-reverse
```css
/* Grid 没有 row-reverse，但可以： */
/* 方案1：direction: rtl（会影响文本方向） */
.grid { direction: rtl; }

/* 方案2：手动排列（已知列数） */
.grid { grid-template-columns: repeat(4, 1fr); }
/* 用负 margin 或 order 反转子元素 */

/* 方案3：使用 grid-column 手动计算位置 */
```

### 【Q516】HTML 标签有哪些行内元素
a、span、strong、em、b、i、u、s、del、ins、sub、sup、small、mark、code、kbd、samp、var、cite、q、abbr、time、label、br、img（实为 inline-block）、input（inline-block）、select、textarea、button

### 【Q517】CSS如何设置一行超出显示省略号
```css
.ellipsis {
  white-space: nowrap;      /* 不换行 */
  overflow: hidden;         /* 超出隐藏 */
  text-overflow: ellipsis;  /* 显示省略号 */
}
```

### 【Q518】CSS如何设置多行超出显示省略号
```css
.multiline-ellipsis {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;    /* 显示几行 */
  overflow: hidden;
  text-overflow: ellipsis;
}
/* 非 WebKit 需要降级方案（max-height + line-height 伪元素遮罩等） */
```

### 【Q525】flex 布局中 order 有何作用
`order` 属性改变 flex 子元素在主轴上的**视觉排列顺序**。默认值为 0，值越小越靠前（可为负数）。仅改变视觉顺序，不改变 DOM 结构和文档流。不影响屏幕阅读器（朗读顺序仍按 DOM）。

```css
.item:first-child { order: 1; }  /* 移到后面 */
.item:last-child  { order: -1; } /* 移到前面 */
```

### 【Q526】flex 布局中 align-content 与 align-items 有何区别
- **align-items**：沿**交叉轴**对齐**单行内**的 flex 子元素。每行独立处理。
- **align-content**：仅当有多行（flex-wrap: wrap）且有空闲空间时生效，决定**多行**在交叉轴上的分布方式（类似 justify-content 但作用于交叉轴）。

单行时 align-content 不生效。

### 【Q531】子元素垂直居中，并且该子元素的长度/宽度为父容器宽度(width)一半的正方形
```css
.parent {
  width: 100%;
  position: relative;
}
.child {
  width: 50%;               /* 父元素宽度一半 */
  aspect-ratio: 1 / 1;      /* 1:1 保持正方形 */
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
/* 或用 flex：设置 child 为 absolute 脱标，或使用 padding-bottom 方案 */
```

### 【Q532】简述 css 中 position 的值
- **static**：默认值，普通文档流，top/left/z-index 无效
- **relative**：相对自身原位置偏移，保留原空间
- **absolute**：绝对定位，脱离文档流，相对最近的定位祖先（非 static），不保留空间
- **fixed**：视口固定定位，始终在屏幕固定位置
- **sticky**：滚动到阈值后固定，相对最近的可滚动容器

### 【Q533】什么是 BFC
**BFC（Block Formatting Context，块级格式化上下文）** 是 CSS 布局中的一个隔离区域，其内部的布局完全独立于外部。

**形成条件**：
- float 不为 none
- position: absolute/fixed
- display: inline-block / flex / grid / flow-root
- overflow 不为 visible

**作用**：
1. **清除浮动**：BFC 包含浮动子元素（不会高度塌陷）
2. **防止外边距重叠**：两个相邻 BFC 的 margin 不合并
3. **防止文字环绕**：避免 float 元素周围的文字环绕

### 【Q534】CSS 如何实现固定长宽比的元素
```css
/* 方案1：aspect-ratio（现代方案） */
.box { width: 100%; aspect-ratio: 16 / 9; }

/* 方案2：padding-bottom %（经典方案，相对于宽度） */
.box { position: relative; width: 100%; padding-bottom: 56.25%; /* 9/16 */ }
.box-inner { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }

/* 方案3：vw/vh 单位（针对视口） */
```

### 【Q535】rem、em、vw、vh 的值各是什么意思
- **rem**：相对根元素（html）的 font-size。常用于响应式布局，改根字号=全局缩放。
- **em**：相对当前元素/父元素的 font-size（自身有 font-size 则用自身，否则继承父元素）。常用于组件内部间距按字号等比。
- **vw**：视口宽度的 1%，100vw = 全屏宽。响应式全屏布局用。
- **vh**：视口高度的 1%，100vh = 全屏高。全屏背景/首屏用。
- **vmin**：vw 和 vh 中较小的那个
- **vmax**：vw 和 vh 中较大的那个
- **svh|lvh|dvh**（新增）：解决移动端浏览器地址栏收放导致的视口变化

### 【Q536】normalize.css 与 reset.css 又何区别
- **reset.css**：把**所有**浏览器默认样式"归零"（把 h1, p, ul, ol 等都设为相同的 margin:0; padding:0），消除各浏览器差异，提供完全干净的画布。
- **normalize.css**：**修正**浏览器差异化，保留有用的默认样式（h1 仍是更大字体）。修复各浏览器的 bug，同时保证交互一致性。比 reset 更温和。
- 现代化项目倾向 Normalize（或现代 Reset 如 CSS Remedy、sanitize.css）。

### 【Q537】line-height 的值分别取2, 2em, 200%有什么区别?
关键在于**继承机制**的不同：
- **纯数字（2）**：最推荐。子元素继承时直接继承这个**比例**（不是计算后的 px）。子元素 line-height = 自身 font-size * 2
- **em（2em）**：基于当前元素的 font-size 计算出一个 px 值，子元素**继承计算后的 px 值**（固定值），不管自身 font-size 多大
- **百分比（200%）**：行为与 em 完全一样，基于当前元素的 font-size 计算 px，子元素继承固定的 px 值

**结论**：用纯数字（推荐），可保证子元素 line-height 与自身 font-size 保持比例。

### 【Q547】某元素的 fontSize: 2rem; lineHeight: 1.5em; 此时 lineHeight 为多少像素
设 html 的 font-size = 16px：
- fontSize: 2rem = 32px（2 × 16px）
- lineHeight: 1.5em = 1.5 × 32px = **48px**

因为 em 基于**当前元素自身的 font-size**（这里是 32px）。

### 【Q553】Grid 布局的优势在哪里
1. **真正的二维布局**：同时控制行和列（Flexbox 本质上是一维）
2. **语义化的布局代码**：定义父容器结构，子元素自动排列
3. **grid-template-areas**：可视化布局，代码即设计稿
4. **强大的函数**：repeat、minmax、auto-fit/auto-fill 实现自适应
5. **间距 gap**：行和列间距原生支持
6. **对齐能力丰富**：justify/align items/content/self
7. **隐式网格**：自动创建行/列
8. **层叠**：Grid 元素可以在同一个 cell 中叠加（用同一个 row/column）

### 【Q557】如何实现三列均分布局
```css
/* 方案1：Flexbox */
.row { display: flex; }
.col { flex: 1; }  /* 三个子元素均分 */

/* 方案2：Grid */
.row { display: grid; grid-template-columns: repeat(3, 1fr); }

/* 方案3：百分比 */
.col { float: left; width: 33.33%; }

/* 方案4：calc */
.col { width: calc(100% / 3); }
```

### 【Q563】什么是媒体查询，JS 可以监听媒体查询吗
**CSS 媒体查询**：根据设备特征（视口宽度、分辨率、方向、配色方案等）应用 CSS 规则：
```css
@media (max-width: 768px) { /* 移动端样式 */ }
```

**JS 监听媒体查询**：
```javascript
const mq = window.matchMedia('(max-width: 768px)');
mq.addEventListener('change', (e) => {
  if (e.matches) { /* 匹配到了 */ }
});
// 或一次性检查
if (mq.matches) { /* ... */ }
```

### 【Q564】z-index: 999 元素一定会置于 z-index: 0 元素之上吗
**不一定**。z-index 只在**同一个层叠上下文中**比较。如果 z-index: 999 的元素在一个 z-index: 0 的层叠上下文中（例如其父容器 opacity < 1 或 transform 不为 none），999 的子元素仍可能被 z-index: 0 的元素覆盖。此外，层叠上下文的层级有嵌套隔离：子元素的 z-index 只在其父层叠上下文中参与排序。

### 【Q608】请简介 CSS 的盒模型
盒模型描述了元素在页面中的空间占据方式，由内到外：**content → padding → border → margin**

- **标准盒模型（content-box）**：`width` = content 宽度。元素实际宽 = width + padding + border + margin
- **替代盒模型（border-box）**：`width` = content + padding + border。更直观，"我设置了 200px 宽就是 200px"
- `box-sizing: border-box` 现代项目基本都用这个（在 Reset CSS 中统一设置）

### 【Q620】CSS 有哪些选择器
- **基础选择器**：`*`（通用）、`div`（标签）、`.class`（类）、`#id`（ID）
- **属性选择器**：`[attr]`、`[attr="val"]`、`[attr^=""]`（开头）、`[attr$=""]`（结尾）、`[attr*=""]`（包含）
- **组合选择器**：`div p`（后代）、`div > p`（子代）、`h1 + p`（相邻兄弟）、`h1 ~ p`（通用兄弟）
- **伪类选择器**：`:hover`、`:focus`、`:first-child`、`:nth-child()`、`:not()`、`:is()`、`:where()`、`:has()`
- **伪元素选择器**：`::before`、`::after`、`::first-line`、`::first-letter`、`::selection`、`::placeholder`

### 【Q621】CSS 有哪些伪类与伪元素选择器
**常见伪类**：
- 动态：`:hover`、`:focus`、`:active`、`:visited`、`:link`
- 结构：`:first-child`、`:last-child`、`:nth-child(n)`、`:nth-of-type()`、`:first-of-type`、`:only-child`、`:empty`
- 表单：`:checked`、`:disabled`、`:enabled`、`:required`、`:valid`、`:invalid`
- 其他：`:not()`、`:is()`、`:where()`、`:has()`、`:root`、`:target`、`:lang()`

**常见伪元素**：
- `::before`、`::after`（最常用）
- `::first-line`、`::first-letter`
- `::selection`（用户选中文本样式）
- `::placeholder`（输入框占位文本样式）
- `::marker`（列表项标记样式）

### 【Q654】css加载会阻塞DOM树的解析和渲染吗
- **CSS 不会阻塞 DOM 解析**：HTML 解析和 CSS 加载并行进行，但 DOM 构建完不会立刻渲染——必须等 CSSOM 完成（CSS 是渲染阻塞资源）
- **CSS 会阻塞页面渲染**：浏览器必须构建 CSSOM 树才能渲染，未加载完 CSS 会"白屏"
- **CSS 会阻塞 JS 执行**：JS 可能查询样式，所以必须等 CSSOM 构建完才执行 JS
- **结论**：CSS 放在 head 中、提取首屏关键 CSS 内联、异步加载非关键 CSS（media 属性欺骗法）

### 【Q669】在 CSS 中，使用 rem 作为单位有何缺点
1. **级联依赖**：rem 依赖根元素 html 的 font-size，若被意外修改（如某个 CSS 框架修改了它），整个页面布局崩溃
2. **计算困难**：px→rem 计算繁琐（设计稿 px / rootSize），需要 PostCSS 插件（postcss-pxtorem）
3. **小数点精度问题**：计算结果可能产生小数点像素，不同浏览器对小数渲染不同
4. **第三方组件不兼容**：UI 组件库默认用 px，引入后需要适配；Chrome 最小 12px 限制让小字号 rem 失效
5. **复杂嵌套下的计算问题**：em 有类似问题更严重，rem 相对较好但 em 的嵌套雪崩在 rem 中不存在

### 【Q695】Flex 布局中的 flex-basis 与 width 有何区别
- **flex-basis**：flex 元素在主轴上的**初始基本尺寸**。优先级高于 width（同一方向时）。设为 `auto` 则用 width。
- **width**：普通的宽度属性。
- **关键区别**：
  1. flex-basis 只在 flex 容器中生效
  2. flex-basis: auto 与 width 相同，但 flex-basis: 0 与 width: 0 不同，前者配合 flex-grow 做均分更准确（从 0 开始分配剩余空间）
  3. 主轴为 row 时 flex-basis 与 width 同方向；主轴为 column 时 flex-basis 与 height 同方向
  4. 简写 `flex: 1` = `flex: 1 1 0`（basis 为 0），`flex: auto` = `flex: 1 1 auto`

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

在 CSS 中，标准盒模型（也叫 `content-box`）其实就是浏览器**默认**的盒模型状态，通常不需要特意去设置。

如果你想确保某个元素使用的是标准盒模型，可以通过 `box-sizing` 属性进行明确指定：

```css
.element {
  box-sizing: content-box; /* 设置为标准盒模型 */
}
```

为了让你更清楚两者的区别，这里做一个简单的对比：

- **标准盒模型 (`content-box`)**：你给元素设置的 `width` 和 `height` **仅仅包含内容区（content）**。元素的实际占用宽度 = `width` + `padding` + `border`。
- **怪异盒模型 (`border-box`)**：你给元素设置的 `width` 和 `height` **已经包含了内容区、内边距（padding）和边框（border）**。这会让尺寸计算更符合直觉，也是现代响应式布局中极力推荐的设置。

💡 为什么通常不推荐使用标准盒模型做布局？
结合你之前问到的“响应式布局”，使用标准盒模型 (`content-box`) 很容易踩坑。

举个最典型的例子：如果你希望一个盒子的宽度占满屏幕的 100%，并且左右各有 10px 的内边距。

- **在标准盒模型下**：`width: 100%; padding: 0 10px;`。此时盒子的实际总宽度变成了 `100% + 20px`，这多出来的 20px 会直接撑破父容器，导致页面出现难看的横向滚动条。
- **在怪异盒模型下**：`width: 100%; padding: 0 10px; box-sizing: border-box;`。此时内边距会向内挤压内容区，盒子的总宽度依然完美保持在 100%。

因此，在现代前端开发（尤其是移动端和响应式开发）中，大家通常会在 CSS 的最开始，通过通配符将所有元素统一设置为怪异盒模型，以避免繁琐的尺寸计算和布局溢出问题：

```css
/* 现代前端开发的标准起手式 */
*, *::before, *::after {
  box-sizing: border-box;
}
```

当然，标准盒模型也有它的用武之地。比如当你希望元素的定位（`top`, `left` 等）严格相对于内容区，而不受边框或内边距变化的影响时，保留默认的 `content-box` 会更方便。但在绝大多数常规布局场景下，`border-box` 都是更省心、更稳健的选择。

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