# 通过搜索获取DOM元素

| 方法名                      | 搜索方式         | 可以在元素上调用？     | 实时的？ |
| ------------------------ | ------------ | ------------- | ---- |
| `querySelector`          | CSS-selector | ✔             | ❌    |
| `querySelectorAll`       | CSS-selector | ✔             | ❌    |
| `getElementById`         | `id`         | 只能在document上调 | ❌    |
| `getElementsByName`      | `name`       | 只能在document上调 | ✔    |
| `getElementsByTagName`   | tag or `'*'` | ✔             | ✔    |
| `getElementsByClassName` | class        | ✔             | ✔    |


---
## 通过ID
如果一个元素有 `id` 特性（attribute），那我们就可以使用 `document.getElementById(id)` 方法获取该元素，无论它在哪里：
```html
<div id="elem">
  <div id="elem-content">Element</div>
</div>

<script>
  // 获取该元素
  let elem = document.getElementById('elem');

  // 将该元素背景改为红色
  elem.style.background = 'red';
</script>
```

此外，还有一个通过 `id` 命名的全局变量，它引用了元素（不推荐使用）：
```html
<div id="elem">
  <div id="elem-content">Element</div>
</div>

<script>
  // elem 是对带有 id="elem" 的 DOM 元素的引用
  elem.style.background = 'red';

  // id="elem-content" 内有连字符，所以它不能成为一个变量
  // ...但是我们可以通过使用方括号 window['elem-content'] 来访问它
</script>
```

……除非我们声明一个具有相同名称的 JavaScript 变量，这个新声明的变量优先：
```html
<div id="elem"></div>

<script>
  let elem = 5; // 现在 elem 是 5，而不是对 <div id="elem"> 的引用

  alert(elem); // 5
</script>
```

- 请不要使用以 id 命名的全局变量来访问元素。在实际开发中，`document.getElementById` 是首选方法。

- `id` 必须是唯一的。如果有多个元素都带有同一个 `id`，那么使用它的方法的行为是不可预测的，例如 `document.getElementById` 可能会随机返回其中一个元素。因此，请遵守规则，保持 `id` 的唯一性。

- 只有 `document.getElementById`，没有 `anyElem.getElementById`。`getElementById` 方法只能被在 `document` 对象上调用。它会在整个文档中查找给定的 `id`。

---
## querySelectorAll
到目前为止，最通用的方法是 `elem.querySelectorAll(css)`，它返回 `elem` 中与给定 CSS 选择器匹配的所有元素。查找所有为最后一个子元素的 `<li>` 元素：
```html
<ul>
  <li>The</li>
  <li>test</li>
</ul>
<ul>
  <li>has</li>
  <li>passed</li>
</ul>
<script>
  let elements = document.querySelectorAll('ul > li:last-child');

  for (let elem of elements) {
    alert(elem.innerHTML); // "test", "passed"
  }
</script>
```

这个方法确实功能强大，因为可以使用任何 CSS 选择器。也可以使用伪类

CSS 选择器的伪类，例如 `:hover` 和 `:active` 也都是被支持的。例如，`document.querySelectorAll(':hover')` 将会返回鼠标指针正处于其上方的元素的集合（按嵌套顺序：从最外层 `<html>` 到嵌套最多的元素）。

---
## querySelector
`elem.querySelector(css)` 调用会返回给定 CSS 选择器的第一个元素。

换句话说，结果与 `elem.querySelectorAll(css)[0]` 相同，但是后者会查找 **所有** 元素，并从中选取一个，而 `elem.querySelector` 只会查找一个。因此它在速度上更快，并且写起来更短。

---
## matches
[elem.matches(css)](https://dom.spec.whatwg.org/#dom-element-matches) 不会查找任何内容，它只会检查 `elem` 是否与给定的 CSS 选择器匹配。它返回 `true` 或 `false`。

当我们遍历元素（例如数组或其他内容）并试图过滤那些我们感兴趣的元素时，这个方法会很有用：
```html
<a href="http://example.com/file.zip">...</a>
<a href="http://ya.ru">...</a>

<script>
  // 不一定是 document.body.children，还可以是任何集合
  for (let elem of document.body.children) {
    if (elem.matches('a[href$="zip"]')) {
      alert("The archive reference: " + elem.href );
    }
  }
</script>
```

---
## closest
元素的祖先（ancestor）是：父级，父级的父级，它的父级等。祖先们一起组成了从元素到顶端的父级链。

`elem.closest(css)` 方法会查找与 CSS 选择器匹配的最近的祖先。`elem` 自己也会被搜索。

换句话说，方法 `closest` 在元素中得到了提升，并检查每个父级。如果它与选择器匹配，则停止搜索并返回该祖先：
```html
<h1>Contents</h1>

<div class="contents">
  <ul class="book">
    <li class="chapter">Chapter 1</li>
    <li class="chapter">Chapter 2</li>
  </ul>
</div>

<script>
  let chapter = document.querySelector('.chapter'); // LI

  alert(chapter.closest('.book')); // UL
  alert(chapter.closest('.contents')); // DIV

  alert(chapter.closest('h1')); // null（因为 h1 不是祖先）
</script>
```

---
## getElementsBy*
大多已经成为了历史，因为 `querySelector` 功能更强大，写起来更短。仍然可以在旧脚本中找到这些方法：
- `elem.getElementsByTagName(tag)` 查找具有给定标签的元素，并返回它们的集合。`tag` 参数也可以是对于“任何标签”的星号 `"*"`。
- `elem.getElementsByClassName(className)` 返回具有给定CSS类的元素。
- `document.getElementsByName(name)` 返回在文档范围内具有给定 `name` 特性的元素。很少使用。

例如：
```javascript
// 获取文档中的所有 div
let divs = document.getElementsByTagName('div');
```

让我们查找 table 中的所有 `input` 标签：
```html
<table id="table">
  <tr>
    <td>Your age:</td>

    <td>
      <label>
        <input type="radio" name="age" value="young" checked> less than 18
      </label>
      <label>
        <input type="radio" name="age" value="mature"> from 18 to 50
      </label>
      <label>
        <input type="radio" name="age" value="senior"> more than 60
      </label>
    </td>
  </tr>
</table>

<script>
  let inputs = table.getElementsByTagName('input');

  for (let input of inputs) {
    alert( input.value + ': ' + input.checked );
  }
</script>
```

不要忘记字母 `"s"`！

新手开发者有时会忘记字符 `"s"`。也就是说，他们会调用 `getElementByTagName` 而不是 `getElementsByTagName`。

`getElementById` 中没有字母 `"s"`，是因为它只返回单个元素。但是 `getElementsByTagName` 返回的是元素的集合，所以里面有 `"s"`。

它返回的是一个集合，不是一个元素！

新手的另一个普遍的错误是写：
```javascript
// 行不通
document.getElementsByTagName('input').value = 5;
```

这是行不通的，因为它需要的是一个 input 的 **集合**，并将值赋（assign）给它，而不是赋值给其中的一个元素。

我们应该遍历集合或通过对应的索引来获取元素，然后赋值，如下所示：
```javascript
// 应该可以运行（如果有 input）
document.getElementsByTagName('input')[0].value = 5;
```

查找 `.article` 元素：
```html
<form name="my-form">
  <div class="article">Article</div>
  <div class="long article">Long article</div>
</form>

<script>
  // 按 name 特性查找
  let form = document.getElementsByName('my-form')[0];

  // 在 form 中按 class 查找
  let articles = form.getElementsByClassName('article');
  alert(articles.length); // 2, found two elements with class "article"
</script>
```

---
## 实时的集合
所有的 `"getElementsBy*"` 方法都会返回一个 **实时的（live）** 集合。这样的集合始终反映的是文档的当前状态，并且在文档发生更改时会“自动更新”。

在下面的例子中，有两个脚本。
1. 第一个创建了对 `<div>` 的集合的引用。截至目前，它的长度是 `1`。
2. 第二个脚本在浏览器再遇到一个 `<div>` 时运行，所以它的长度是 `2`。

```html
<div>First div</div>

<script>
  let divs = document.getElementsByTagName('div');
  alert(divs.length); // 1
</script>

<div>Second div</div>

<script>
  alert(divs.length); // 2
</script>
```

相反，`querySelectorAll` 返回的是一个 **静态的** 集合。就像元素的固定数组。

如果我们使用它，那么两个脚本都会输出 `1`：
```html
<div>First div</div>

<script>
  let divs = document.querySelectorAll('div');
  alert(divs.length); // 1
</script>

<div>Second div</div>

<script>
  alert(divs.length); // 1
</script>
```

现在我们可以很容易地看到不同之处。在文档中出现新的 `div` 后，静态集合并没有增加。

---
## 总结
有 6 种主要的方法，可以在 DOM 中搜索元素节点：

| 方法名                      | 搜索方式         | 可以在元素上调用？ | 实时的？ |
| ------------------------ | ------------ | --------- | ---- |
| `querySelector`          | CSS-selector | ✔         | -    |
| `querySelectorAll`       | CSS-selector | ✔         | -    |
| `getElementById`         | `id`         | -         | -    |
| `getElementsByName`      | `name`       | -         | ✔    |
| `getElementsByTagName`   | tag or `'*'` | ✔         | ✔    |
| `getElementsByClassName` | class        | ✔         | ✔    |

目前为止，最常用的是 `querySelector` 和 `querySelectorAll`，但是 `getElement(s)By*` 可能会偶尔有用，或者可以在旧脚本中找到。

此外：
- `elem.matches(css)` 用于检查 `elem` 与给定的 CSS 选择器是否匹配。
- `elem.closest(css)` 用于查找与给定 CSS 选择器相匹配的最近的祖先。`elem` 本身也会被检查。

让我们在这里提一下另一种用来检查子级与父级之间关系的方法，因为它有时很有用：
- 如果 `elemB` 在 `elemA` 内（`elemA` 的后代）或者 `elemA==elemB`，`elemA.contains(elemB)` 将返回 true。

---
## 标签统计
- `document.querySelectorAll('*')`![[Pasted image 20260619201749.png]]
- `document.getElementsByTagName('*')`![[Pasted image 20260619201902.png]]
- `$$('*')`，可在浏览器控制台使用。在某些现代浏览器的开发者工具（如 Chrome DevTools 的 Console）中，`$$` 被作为一个内置的辅助函数提供，此时 `$$('*')` 同样等同于 `document.querySelectorAll('*')`。![[Pasted image 20260619201642.png]]
- `document.all`，已废弃，不建议使用![[Pasted image 20260619201717.png]]