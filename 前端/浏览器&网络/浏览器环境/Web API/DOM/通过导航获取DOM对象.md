# 通过导航获取DOM对象
> Last Format Time：6/21/2026 17:22:15

---
## 导航属性
通过这些链接我们可以在 DOM 节点之间移动。
![[Pasted image 20260619171526.png]]

### documentElement、body和head
最顶层的树节点可以直接作为 `document` 的属性来使用：
- `<html>` = `document.documentElement` 最顶层的 document 节点是 `document.documentElement`。这是对应 `<html>` 标签的 DOM 节点
- `<body>` = `document.body` 另一个被广泛使用的 DOM 节点是 `<body>` 元素 —— `document.body`
- `<head>` = `document.head` `<head>` 标签可以通过 `document.head` 访问

![[Pasted image 20260619171914.png]]

### childNodes
`childNodes`是一个一个类数组的可迭代对象：
1. 我们可以使用 `for..of` 来迭代它：
```javascript
for (let node of document.body.childNodes) {
  alert(node); // 显示集合中的所有节点
}
```

2. 无法使用数组的方法，因为它不是一个数组：
```javascript
alert(document.body.childNodes.filter); // undefined（这里没有 filter 方法！）
```

集合的性质所得到的第一个结果很不错。第二个结果也还可以忍受，因为如果我们想要使用数组的方法的话，我们可以使用 `Array.from` 方法来从集合创建一个“真”数组：
```javascript
alert( Array.from(document.body.childNodes).filter ); // function
```

**`childNodes` 集合包括了所有直接子节点，包括文本节点**：
![[Pasted image 20260619172505.png]]

##### 特点
- DOM 集合是只读的。DOM 集合，甚至可以说本章中列出的 **所有** 导航（navigation）属性都是只读的。
我们不能通过类似 `childNodes[i] = ...` 的操作来替换一个子节点。
修改子节点需要使用其它方法。我们将会在下一章中看到它们。

- DOM 集合是实时的。除小部分例外，几乎所有的 DOM 集合都是 **实时** 的。换句话说，它们反映了 DOM 的当前状态。
如果我们保留一个对 `elem.childNodes` 的引用，然后向 DOM 中添加/移除节点，那么这些节点的更新会自动出现在集合中。

- 不要使用 `for..in` 来遍历集合。可以使用 `for..of` 对集合进行迭代。`for..in` 循环遍历的是所有可枚举的（enumerable）属性。集合还有一些“额外的”很少被用到的属性，通常这些属性也是我们不期望得到的：
```html
<body>
<script>
  // 显示 0，1，length，item，values 及其他。
  for (let prop in document.body.childNodes) alert(prop);
</script>
</body>
```

### firstChild，lastChild
**`firstChild` 和 `lastChild` 属性是访问第一个和最后一个子元素的快捷方式。** 它们只是简写。如果元素存在子节点，那么下面的脚本运行结果将是 true：
```javascript
elem.childNodes[0] === elem.firstChild
elem.childNodes[elem.childNodes.length - 1] === elem.lastChild
```

这里还有一个特别的函数 `elem.hasChildNodes()` 用于检查节点是否有子节点。

### nextSibling、previousSibling与parentNode
下一个兄弟节点在 `nextSibling` 属性中，上一个是在 `previousSibling` 属性中。可以通过 `parentNode` 来访问父节点：
```javascript
// <body> 的父节点是 <html>
alert( document.body.parentNode === document.documentElement ); // true

// <head> 的后一个是 <body>
alert( document.head.nextSibling ); // HTMLBodyElement

// <body> 的前一个是 <head>
alert( document.body.previousSibling ); // HTMLHeadElement
```

---
## 纯元素导航
上面列出的导航（navigation）属性引用 **所有类型的** 节点。例如，在 `childNodes` 中我们可以看到文本节点，元素节点，甚至包括注释节点（如果它们存在的话）。

但是对于很多任务来说，我们并不想要文本节点或注释节点。我们希望操纵的是代表标签的和形成页面结构的**元素节点**。
![[Pasted image 20260619195141.png]]

所以，让我们看看更多只考虑 **元素节点** 的导航链接（navigation link）。这些链接和我们在上面提到过的类似：
- `children` —— 仅那些作为元素节点的子代的节点。
- `firstElementChild`，`lastElementChild` —— 第一个和最后一个子元素。
- `previousElementSibling`，`nextElementSibling` —— 兄弟元素。
- `parentElement` —— 父元素。

![[Pasted image 20260619195032.png]]

---
## 其他导航属性
某些类型的 DOM 元素可能会提供特定于其类型的其他属性。

**`<table>`** 元素支持 (除了上面给出的，之外) 以下属性:
- `table.rows` —— `<tr>` 元素的集合。
- `table.caption/tHead/tFoot` —— 引用元素 `<caption>`，`<thead>`，`<tfoot>`。
- `table.tBodies` —— `<tbody>` 元素的集合（根据标准还有很多元素，但是这里至少会有一个 —— 即使没有被写在 HTML 源文件中，浏览器也会将其放入 DOM 中）。

**`<thead>`，`<tfoot>`，`<tbody>`** 元素提供了 `rows` 属性：
- `tbody.rows` —— 表格内部 `<tr>` 元素的集合。

**`<tr>`：**
- `tr.cells` —— 在给定 `<tr>` 中的 `<td>` 和 `<th>` 单元格的集合。
- `tr.sectionRowIndex` —— 给定的 `<tr>` 在封闭的 `<thead>/<tbody>/<tfoot>` 中的位置（索引）。
- `tr.rowIndex` —— 在整个表格中 `<tr>` 的编号（包括表格的所有行）。

**`<td>` 和 `<th>`：**
- `td.cellIndex` —— 在封闭的 `<tr>` 中单元格的编号。

用法示例：
```html
<table id="table">
  <tr>
    <td>one</td><td>two</td>
  </tr>
  <tr>
    <td>three</td><td>four</td>
  </tr>
</table>

<script>
  // 获取带有 "two" 的 td（第一行，第二列）
  let td = table.rows[0].cells[1];
  td.style.backgroundColor = "red"; // highlight it
</script>
```