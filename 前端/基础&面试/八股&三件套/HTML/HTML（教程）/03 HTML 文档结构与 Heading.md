# 03 HTML 文档结构与 Heading
> Last Format Time：9/16/2026 19:24:51

---
## HTML 文档骨架
```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>页面标题</title>
</head>
<body>
</body>
</html>
```

核心 mental model：
```text
DOCTYPE
→ 决定浏览器使用标准模式解析

html
→ HTML 文档根元素

head
→ 描述“这份文档”的 metadata（元数据）

body
→ 文档实际内容
```

### `<!doctype html>`
- 不是 HTML 标签，而是 document type declaration（文档类型声明）。
- 现代 HTML 中最重要的作用：让浏览器进入 Standards Mode（标准模式）。
- 缺失或错误的 DOCTYPE 可能触发 Quirks Mode（怪异模式）。
- 不要只理解成“声明 HTML5”。

### `<html>`
HTML 的根元素：
```text
Document
└── html
    ├── head
    └── body
```

DOM 中：
```js
document.documentElement // <html>
document.head
document.body
```

`document` 对象和 `<html>` 元素不是同一个东西。

### lang
表示页面的主要自然语言，不是字符编码

```html
<html lang="zh-CN">
```

作用包括：
- Screen Reader（屏幕阅读器）选择发音规则
- 翻译工具识别语言
- 拼写检查
- 搜索引擎理解页面语言

局部语言可以覆盖：
```html
<span lang="en">Accessibility</span>
```

### `<head>` 与 `<body>`
```text
head
→ 关于文档的信息

body
→ 文档实际内容
```

### `<meta>`
`<meta>` 是 HTML 中用于声明 document metadata（文档元数据）的元素，通常放在 `<head>` 中。它不会作为页面正文直接渲染，而是向浏览器、搜索引擎等提供关于当前文档的信息，例如字符编码、viewport、description、robots 等。

按照什么字符编码解释 HTML 字节，编码错误可能产生乱码。通常尽早声明 UTF-8

```html
<meta charset="UTF-8" />
```

用于配置移动端 viewport（视口）

```text
width=device-width
→ 布局视口与设备 CSS 宽度对应

initial-scale=1.0
→ 初始缩放比例为 1
```

```html
<meta
  name="viewport"
  content="width=device-width, initial-scale=1.0"
/>
```

它是现代响应式页面的基础配置，但不是“自动实现移动端适配”。

```html
<meta name="description" content="...">
```

### `<title>`
```html
<title>React 学习笔记</title>
```

表示 document title（文档标题），常用于：
- 浏览器标签页
- 书签
- 浏览历史
- 搜索结果标题的重要来源之一

与 `<h1>` 不同：
```text
<title>
→ 整份 document 的名字

<h1>
→ body 内容中的主标题
```

---
## Heading 的核心 mental model
Heading≠字体大小
Heading=内容在 document hierarchy（文档层级）中的位置

例如：
```html
<h1>JavaScript 教程</h1>

<h2>函数</h2>

<h3>箭头函数</h3>
<h3>普通函数</h3>

<h2>Promise</h2>
```

表达的是：
```text
JavaScript 教程
├── 函数
│   ├── 箭头函数
│   └── 普通函数
└── Promise
```


HTML 负责：
```text
它是什么 / 层级是什么
```

CSS 负责：
```text
它长什么样
```

所以完全可以：
```css
h1 { font-size: 18px; }
h2 { font-size: 30px; }
```

语义层级仍然是：
```text
h1 > h2
```

---
##  h1 ~ h6
Heading level 表达内容层级：
```text
h1
→ 页面主主题

h2
→ h1 下的一级子主题

h3
→ h2 下的子主题
```

重点：
level = 结构层级，不是 = 业务重要程度

---
## Document outline
Practical mental model：把页面所有 Heading 单独抽出来，应该大致能看懂页面内容是怎么组织的。

例如：
```text
商品详情
├── 商品介绍
├── 参数
└── 用户评价
    ├── 好评
    └── 差评
```

Heading 是页面信息结构的重要组成部分。

不要依赖浏览器根据 `<section>` 自动推断 Heading level。

---
## 一个页面能不能多个 `h1`
HTML 并不禁止多个 `<h1>`，多个 `h1` 不是语法错误。但实际项目通常推荐一个页面保持一个清晰的主 `h1`。因为它最自然地表达这个页面主要是在讲什么

例如：
```html
<h1>前端开发工程师</h1>
```

不要依赖自动产生“局部 h1 被降级”的效果。

```html
<section>
  <h1>...</h1>
</section>
```

真实项目中显式写层级更可靠：
```html
<h1>首页</h1>

<section>
  <h2>新闻</h2>
</section>
```

---
## Heading 能不能跳级
浏览器允许但通常应该避免：
```html
<h2>函数</h2>
<h4>箭头函数</h4>
```

它表达出的结构类似，hierarchy（层级结构）不清晰：
```text
函数
└── ???
    └── 箭头函数
```

---
## `section` / `article` 与 Heading
### `section`
```text
section
→ 一个有明确主题的内容区域
```

因此通常会自然拥有一个 Heading：
```html
<section>
  <h2>用户评价</h2>
</section>
```

不是用了 section必须强行塞一个 h2

正确因果关系是这里存在一个明确主题 → 可以使用 section → Heading 用来表达这个主题

如果根本没有主题，这里可能根本不应该使用 `section`：
```html
<section>
  <button>保存</button>
  <button>取消</button>
</section>
```

可能只是：
```html
<div>
  <button>保存</button>
  <button>取消</button>
</div>
```

### `article`
可以独立理解 / 独立复用的完整内容

可以单独理解 ≠ 一定需要 article

例如 KPI：
```text
今日访问量：12,430
新增用户：532
```

可能更适合：
```html
<dl>
  <dt>今日访问量</dt>
  <dd>12,430</dd>
</dl>
```

---
## 视觉标题 ≠ Heading
判断标准：它是否给下面一块内容定义了一个主题？

例如这里“姓名”不是 Heading，而是表单控件标签：
```text
姓名
[input]
```

```html
<label for="name">姓名</label>
<input id="name" />
```

关系：
```text
Heading
→ 给内容区域命名

label
→ 给表单控件命名
```

---
## Sidebar Heading
例如：
```html
<h1>React 文档</h1>

<aside>
  <h2>文档导航</h2>
</aside>

<main>
  <h2>Hooks</h2>
</main>
```

两个 `h2` 不冲突：
```text
React 文档
├── 文档导航
└── Hooks
```

同级 Heading 表示结构等级相近，不是业务重要性一样

尤其 Sidebar 等固定区域，更重要的是保持整体结构和跨页面一致性。Heading hierarchy 不是“看到前一个 h2，就机械 +1 写 h3”。


---
## Modal Heading
不要因为 Modal 浮在最上面 z-index 很高就使用 `<h1>`，视觉层级和 Heading hierarchy 无关，同样也不要机械认为：Modal 从某个 h2 下面打开 → Modal 必须 h3

Modal 是独立的交互区域，其标题需要：
- 合适的 Heading 语义
- 合适的 dialog accessible name（无障碍名称）

例如：
```html
<div
  role="dialog"
  aria-labelledby="dialog-title"
>
  <h2 id="dialog-title">删除成员</h2>
</div>
```

具体 Heading level 应根据页面和组件结构设计，而不是根据 z-index 或打开位置决定。

---
## React reusable component 中的 Heading
危险设计：
```tsx
function CardTitle({ children }) {
  return <h3>{children}</h3>;
}
```

第一次使用可能正确：
```text
h1 首页
└── h2 推荐文章
    └── h3 React Fiber
```

换个位置：
```text
h1 首页
└── h2 技术
    └── h3 React
        └── h4 React Fiber
```

如果 Heading level 由使用上下文决定，就应该让调用方拥有控制权。常见 API：
```tsx
<Card.Title level={4} />
```

或：
```tsx
<Card.Title as="h4" />
```

或：
```tsx
<Card.Title asChild>
  <h4>React Fiber</h4>
</Card.Title>
```

但如果组件语义位置本身固定，例如：
```tsx
<PageTitle />
```

它的 contract 就是页面主标题，那么内部固定，就是完全合理的：
```tsx
<h1>
```

---
## Visually Hidden Heading
有时视觉设计不需要显示标题，但结构上仍然需要 Heading：
```html
<section>
  <h2 class="sr-only">搜索结果</h2>
  ...
</section>
```

其中：
```text
sr-only
→ 视觉用户看不到
→ Screen Reader 仍可以访问
```

核心不可视 ≠ 不存在

但：
```css
display: none;
```

或：
```html
aria-hidden="true"
```

通常会连辅助技术一起隐藏。

也不要为了“无障碍”到处增加没有实际结构意义的隐藏 Heading，否则会污染 Heading Navigation。

---
## SEO 与 Heading
不要理解成：
```text
h1 = SEO 权重最高
h2 = 次高
多塞关键词 = 排名上涨
```

正确 mental model：
```text
Heading
→ 描述页面 topic（主题）
→ 描述内容 structure（结构）
→ 帮助搜索引擎理解页面
```

因此正确使用 Heading 本质上是写出清晰的信息结构，而不是进行 SEO 玄学操作。

---
## 常见 Heading 错误
### 为了字号选标签
```html
<h5>Card Title</h5>
```

因为 h5 默认比较小。

### 所有视觉标题都用 div
```html
<div class="text-3xl">商品详情</div>
```

导致原生 Heading 语义丢失。

### Heading 跳级
```html
<h1>...</h1>
<h4>...</h4>
```

通常导致 hierarchy 不清晰。

### Logo 当 h1
```html
<h1>Company Logo</h1>
```

把品牌重要性误认为文档层级。

### 到处使用 h1
```html
<h1>Logo</h1>
<h1>商品名</h1>
<h1>相关推荐</h1>
```

即使不一定语法非法，也基本失去了 hierarchy。

### reusable component 写死 Heading level
```tsx
function Card() {
  return <h2>...</h2>;
}
```

组件复用到其他层级后容易破坏文档结构。

### 把 label 当 Heading
```html
<h3>姓名</h3>
<input />
```

正确语义通常是：
```html
<label>姓名</label>
```

### 为 section 强行补 Heading
错误 mental model：
```text
section 必须有 h2
```

正确：
```text
这里本来就是一个明确主题区域
→ section
→ Heading 自然表达它的主题
```

---
## 最终 mental model
判断 Heading 时不要问：
```text
这行字多大？
它看起来重不重要？
设计稿是不是标题样式？
```

而要问：
```text
它是否给下面一块内容命名？

它在 document hierarchy 中是谁的子主题？

它与哪些内容同级？

如果把所有 Heading 单独抽出来，
还能不能看懂这个页面的结构？
```

核心公式：
```text
Heading
=
document hierarchy 中的内容标题节点
```

而不是：
```text
Heading
=
字体大小等级
```

HTML 语义判断的核心始终是：
```text
“这个东西是什么？”
```

而不是：
```text
“这个东西长什么样？”
```