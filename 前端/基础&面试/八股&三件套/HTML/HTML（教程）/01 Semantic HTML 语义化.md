# 01 Semantic HTML 语义化
> Last Format Time：9/16/2026 19:24:51

*这玩意儿，面试的时候真能考吗？虽然我相信功夫在平时，但是在国内这么浮躁的就业市场，真有人看这种已经死去的东西吗*

HTML 描述这个内容是什么、在文档中扮演什么角色。因此：

- 有明确语义 → 使用对应的 HTML semantic element
- 只是为了包一层结构、分组、布局 → 使用 `div`

不要为了“看起来更语义化”而滥用 `section`、`article` 等标签。

---
## div
`div` 是没有额外语义的通用容器。

适合：
- 分组
- DOM 结构
- 布局容器
- JS 操作节点
- 没有更合适语义元素的场景

```html
<div class="card-wrapper">
  ...
</div>
```

---
## main
表示当前页面最主要、最核心的内容。一般只有一个

例如：
```html
<body>
  <header>...</header>

  <main>
    页面主要内容
  </main>

  <footer>...</footer>
</body>
```

mental model：
```text
Page
├── Header
├── Main     ← 用户访问当前页面主要为了这里
└── Footer
```

---
## article
可以独立存在、独立理解的一份完整内容。

判断方式，把这一块从当前页面单独拿出去，它还能成立吗？

如果可以，通常适合 `article`。

常见：
- 博客文章
- 新闻
- 论坛帖子
- 评论
- 社交动态
- 独立内容卡片

```html
<article>
  <h2>React 19 发布</h2>
  <p>...</p>
</article>
```

---
## section
 文档或内容中的一个明确主题区域 / 章节。

例如：
```html
<article>
  <h1>React Fiber</h1>

  <section>
    <h2>为什么需要 Fiber</h2>
  </section>

  <section>
    <h2>Fiber Tree</h2>
  </section>
</article>
```

---
## header
`header` 不等于页面最顶部。表示当前页面或当前内容区域的介绍性 / 头部内容。因此一个页面可以有多个 `header`：
```html
<body>
  <header>
    网站 Header
  </header>

  <main>
    <article>
      <header>
        <h1>React Fiber</h1>
        <p>作者信息</p>
      </header>
    </article>
  </main>
</body>
```

可以同时存在：
```text
页面 header
article header
```

---
## footer
和 `header` 类似。

---
## nav
承担导航功能的一组链接区域。

例如：
```html
<nav>
  <a href="/">首页</a>
  <a href="/blog">博客</a>
  <a href="/about">关于</a>
</nav>
```

不是页面里出现链接就需要 `nav`，普通正文链接：
```html
<p>
  查看
  <a href="/docs">React 文档</a>
</p>
```

不需要包 `nav`。判断标准：这一组链接是不是承担导航功能？

---
## aside
与主要内容相关，但不是当前内容主线的补充内容。

例如：
```html
<main>
  <article>
    文章正文
  </article>

  <aside>
    推荐文章
  </aside>
</main>
```

可以理解为：
```text
Main Content
    │
    └── Aside
        相关但非主线
```

典型：
- 推荐内容
- 作者榜
- 相关链接
- 补充说明
- Sidebar

---
## 一个完整例子
```html
<body>
  <header>
    <nav>
      <a href="/">首页</a>
      <a href="/articles">文章</a>
    </nav>
  </header>

  <main>
    <article>
      <header>
        <h1>深入理解 React Fiber</h1>
        <p>发布时间：2026-09-04</p>
      </header>

      <section>
        <h2>为什么需要 Fiber</h2>
        <p>...</p>
      </section>

      <section>
        <h2>Fiber Tree</h2>
        <p>...</p>
      </section>

      <footer>
        作者：Dano
      </footer>
    </article>

    <aside>
      <h2>相关推荐</h2>
    </aside>
  </main>

  <footer>
    © 2026
  </footer>
</body>
```

结构：
```text
Page
├── header
│   └── nav
│
├── main
│   ├── article
│   │   ├── header
│   │   ├── section
│   │   ├── section
│   │   └── footer
│   │
│   └── aside
│
└── footer
```

---
## React Component 与 HTML Semantic 不要混淆
React Component 描述的是：
```text
程序结构
状态
行为
逻辑复用
组件职责
```

HTML Semantic 描述的是：
```text
文档结构
内容角色
浏览器语义
Accessibility 语义
```

例如：
```jsx
<Card />
```

是一个有意义的 React Component。

但它内部完全可能只是：
```html
<div>
  ...
</div>
```

因为 HTML 本身未必存在对应的 `card` 语义。
