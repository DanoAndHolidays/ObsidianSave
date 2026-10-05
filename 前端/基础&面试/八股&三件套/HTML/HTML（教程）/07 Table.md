# 07 Table
> Last Format Time：10/6/2026 02:27:25

`<table>` 用于表示具有行列关系的二维结构化数据，table 用于数据关系，不用于页面布局。

布局应该交给 CSS，而不是为了排版去滥用 `<table>`。

---
## 基本结构
```html
<table>
  <thead>
    <tr>
      <th scope="col">姓名</th>
      <th scope="col">年龄</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Dano</td>
      <td>22</td>
    </tr>
  </tbody>

  <tfoot>
    <tr>
      <th scope="row">总计</th>
      <td>1 人</td>
    </tr>
  </tfoot>
</table>
```

常见元素：

- `table`：整个表格
- `thead`：表头区域
- `tbody`：主体数据区域
- `tfoot`：汇总、统计区域
- `tr`：table row，行
- `th`：table header，表头单元格
- `td`：table data，普通数据单元格
- `caption`：整张表格的标题

---
## `th` 和 `td`
`td` 表示普通数据，`th` 表示**描述其他数据的表头单元格**。

```html
<th>姓名</th>
<td>Dano</td>
```

不要把 `th` 理解成“加粗版 td”。加粗、居中只是浏览器默认样式，真正区别是**语义**。

判断使用 `th` 还是 `td`，看这个单元格是不是在描述其他数据，而不是看它是否位于第一行。

所以 `th` 也可以出现在 `tbody`：
```html
<tr>
  <th scope="row">Dano</th>
  <td>90</td>
</tr>
```

---
## `thead / tbody / tfoot`
它们用于对表格中的行进行语义分组。

```text
table
├─ thead   表头
├─ tbody   主体数据
└─ tfoot   汇总数据
```

`tbody` 本质上是一个 **row group（行组）**，一个 table 可以存在多个 `tbody`。

工程中推荐显式写出：
```html
<table>
  <tbody>
    ...
  </tbody>
</table>
```

不要依赖浏览器自动修正表格结构。React 中也建议显式提供 `tbody`，避免 React 描述的结构与最终 DOM 结构产生差异。

---
## Table 的结构限制
`table` 内部不是像 `div` 一样可以随便嵌套。

错误：
```html
<table>
  <div>
    <tr>
      <td>Hello</td>
    </tr>
  </div>
</table>
```

更合理：
```html
<table>
  <tbody>
    <tr>
      <td>
        <div>Hello</div>
      </td>
    </tr>
  </tbody>
</table>
```

---
## `caption`
`caption` 用来描述**整张表是什么**。

```html
<table>
  <caption>2026 年员工信息</caption>
</table>
```

它和普通的：
```html
<h2>2026 年员工信息</h2>
```

不完全相同，`caption` 和当前 table 存在明确的语义关联，对可访问性也有帮助。

---
## `colspan`
`colspan` 表示横向跨列。

```html
<th colspan="2">成绩</th>
```

表示这个单元格占据两列，例如：
```text
| 姓名 |    成绩    |
|      | 数学 | 英语 |
```

---
## `rowspan`
`rowspan` 表示纵向跨行。

```html
<td rowspan="2">前端组</td>
```

例如：
```text
| 前端组 | Dano |
|        | Tom  |
```

被 `rowspan` 占据的位置，在下一行不需要再次创建对应的 `td/th`。

---
## 多级表头
例如：
```html
<thead>
  <tr>
    <th rowspan="2">姓名</th>
    <th colspan="2">2026</th>
  </tr>

  <tr>
    <th>Q1</th>
    <th>Q2</th>
  </tr>
</thead>
```

对应：
```text
| 姓名 |    2026    |
|      | Q1 | Q2    |
```

多级表头本质仍然是在描述二维数据之间的关系。

---
## `scope`
`scope` 用来明确 `th` 描述的数据范围。
常见值：
```html
scope="col"
scope="row"
scope="colgroup"
scope="rowgroup"
```

含义：
```text
col      → 当前列的标题
row      → 当前行的标题
colgroup → 一组列的标题
rowgroup → 一组行的标题
```

最常用：
```html
<th scope="col">年龄</th>

<th scope="row">Dano</th>
```

对于简单表格，推荐显式写：
```html
<th scope="col">
<th scope="row">
```

这样可以让表头和数据之间的关系更加明确。

---
## 表格可访问性
视觉用户可以直接根据行列位置理解数据。

屏幕阅读器则需要知道：

```text
当前数据
对应哪个行标题
对应哪个列标题
```

例如：

```html
<tr>
  <th scope="row">Dano</th>
  <td>90</td>
</tr>
```

如果列标题是：

```html
<th scope="col">数学</th>
```

那么 `90` 的语义就是：

```text
Dano + 数学 → 90
```

因此合理使用：

- `th`
    
- `scope`
    
- `caption`
    

对于表格可访问性很重要。

---
## `headers` + `id`
对于非常复杂、不规则的表格，可以通过：
```html
id
headers
```

显式关联表头和数据。

```html
<th id="math">数学</th>
<th id="dano">Dano</th>

<td headers="dano math">90</td>
```

表示：
```text
90
→ Dano
→ 数学
```

但简单表格没必要使用。一般：
```text
简单表格
→ th + scope

复杂、不规则表格
→ 必要时 id + headers
```

---
## React 动态表格
动态生成表格时，`rowspan` 对应的单元格通常只应该生成一次。

例如：
```jsx
{group.users.map((user, index) => (
  <tr key={user}>
    {index === 0 && (
      <th rowSpan={group.users.length}>
        {group.name}
      </th>
    )}

    <td>{user}</td>
  </tr>
))}
```

因为 `rowSpan` 已经占据了后续行对应的位置，不应该每一行重复创建。
