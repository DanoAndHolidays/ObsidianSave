# DOM文档对象模型
> Last Format Time：6/21/2026 17:22:15

[https://developer.mozilla.org/zh-CN/docs/Web/API/Document](https://developer.mozilla.org/zh-CN/docs/Web/API/Document)

---
## 标签简介
HTML 文档的主干是标签（tag）。根据文档对象模型（DOM），每个 HTML 标签都是一个对象（节点）。嵌套的标签是闭合标签的“子标签（children）”。标签内的文本也是一个对象。

所有这些对象都可以通过 JavaScript 来访问，我们可以使用它们来修改页面。例如，`document.body` 是表示 `<body>` 标签的对象。

运行这段代码会使 `<body>` 保持 3 秒红色状态:
```javascript
document.body.style.background = 'red'; // 将背景设置为红色

setTimeout(() => document.body.style.background = '', 3000); // 恢复回去
```

在这，我们使用了 `style.background` 来修改 `document.body` 的背景颜色，但是还有很多其他的属性，例如：
- `innerHTML` —— 节点的 HTML 内容。
- `offsetWidth` —— 节点宽度（以像素度量）
- ……等。

### 节点与其类型、结构
让我们从下面这个简单的文档（document）开始：
```html
<!DOCTYPE HTML>
<html>
  <head>
    <title>About elk</title>
  </head>
  <body>
    The truth about elk.
  </body>
</html>
```

DOM 将 HTML 表示为标签的树形结构。它看起来如下所示：
![[Pasted image 20260618174943.png]]
每个树的节点都是一个对象：
- 标签被称为 **元素节点**（或者仅仅是元素），并形成了树状结构：`<html>` 在根节点，`<head>` 和 `<body>` 是其子项，等。
- 元素内的文本形成 **文本节点**，被标记为 `＃text`。一个文本节点只包含一个字符串。它没有子项，并且总是树的叶子。
- 注释，**comment**节点：![[Pasted image 20260618175751.png]]

**HTML 中的所有内容，甚至注释，都会成为 DOM 的一部分。** 
甚至 HTML 开头的 `<!DOCTYPE...>` 指令也是一个 DOM 节点。它在 DOM 树中位于 `<html>` 之前。![[Pasted image 20260619171132.png]]

一共有 [12 种节点类型](https://dom.spec.whatwg.org/#node)。实际上，我们通常用到的是其中的 4 种：
1. `document` —— DOM 的“入口点”。
2. 元素节点 —— HTML 标签，树构建块。
3. 文本节点 —— 包含文本。空格和换行符都是完全有效的字符，就像字母和数字。![[Pasted image 20260619215908.png]]在图中可以看到，就连格式化的时候的回车也是节点中一部分，无论是head还是body中的![[Pasted image 20260619215827.png]]请注意文本节点中的特殊字符：
	- 换行符：`↵`（在 JavaScript 中为 `\n`）
	- 空格：`␣`
4. 注释 —— 有时我们可以将一些信息放入其中，它不会显示，但 JS 可以从 DOM 中读取它。
![[Pasted image 20260619165459.png]]

只有两个顶级排除项：
1. 由于历史原因，`<head>` 之前的空格和换行符均被忽略。
2. 如果我们在 `</body>` 之后放置一些东西，那么它会被自动移动到 `body` 内，并处于 `body` 中的最下方，因为 HTML 规范要求所有内容必须位于 `<body>` 内。所以 `</body>` 之后不能有空格。

在其他情况下，一切都很简单 —— 如果文档中有空格（就像任何字符一样），那么它们将成为 DOM 中的文本节点，而如果我们删除它们，则不会有任何空格。

---
## 自动修正
如果浏览器遇到格式不正确的 HTML，它会在形成 DOM 时自动更正它。

例如，顶级标签总是 `<html>`。即使它不存在于文档中 — 它也会出现在 DOM 中，因为浏览器会创建它。对于 `<body>` 也是一样。

例如，如果一个 HTML 文件中只有一个单词 “Hello”，浏览器则会把它包装到 `<html>` 和 `<body>` 中，并且会添加所需的 `<head>`，DOM 将会变成下面这样：
![[Pasted image 20260618175415.png]]

在生成 DOM 时，浏览器会自动处理文档中的错误，关闭标签等：
```html
<p>Hello
<li>Mom
<li>and
<li>Dad
```

![[Pasted image 20260618175505.png]]

表格是一个有趣的“特殊的例子”。按照 DOM 规范，它们必须具有 `<tbody>` 标签，但 HTML 文本可能会忽略它。然后浏览器在创建 DOM 时，自动地创建了 `<tbody>`。

对于 HTML：
```html
<table id="table"><tr><td>1</td></tr></table>
```

DOM 结构会变成：
![[Pasted image 20260618175600.png]]

`<tbody>` 出现了。我们应该记住这一点，以免在使用表格时，对这种情况感到惊讶。
