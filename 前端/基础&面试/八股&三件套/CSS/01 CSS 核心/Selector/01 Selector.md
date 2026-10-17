# Selector
> Last Format Time：10/17/2026 02:27:25

CSS 选择器（Selector）是一种用于描述哪些 DOM 元素应被匹配的模式（Pattern）

---
## Basic Selectors

### Type Selector
也叫元素选择器，根据 HTML 元素名称匹配

### Class Selector
根据元素的 `class` 属性匹配

### ID Selector
根据元素的 `id` 属性匹配

### Universal Selector
通配选择器，`*` 表示匹配任何元素类型

### 属性选择器
[[02 属性选择器]]

### 伪类与伪元素
[[03 伪类和伪元素💡]]

---
## Compound Selector
在一个元素上叠加多个条件的写法叫复合选择器（Compound Selector）

例如：
```css
div.card { }             /* div 元素，同时具有 card 类 */
.card.active { }         /* 同时具有两个类 */
input[type="text"] { }   /* input 元素，且 type="text" */
button:hover { }         /* button 元素，且处于 hover 状态 */
```

这些选择器都是在描述同一个元素必须满足的条件

`.card .active` 两个元素之间存在后代关系，这个并不是复合选择器，他是个使用组合器的复杂选择器：
```
<div class="card">
  <span class="active">A</span>

  <div>
    <span class="active">B</span>
  </div>
</div>

<span class="active">C</span>
```

匹配所有拥有 `active` 类，并且存在某个祖先元素具有 `card` 类的元素。

### Combinators 组合器

| 写法      | 最终选中 | 关系要求                                    |
| ------- | ---- | --------------------------------------- |
| `A B`   | `B`  | `B` 是 `A` 的后代，可以跨越任意多层 DOM 层级，不要求直接父子关系 |
| `A > B` | `B`  | `B` 是 `A` 的直接子元素                        |
| `A + B` | `B`  | `B` 紧跟在同级的 `A` 后面                       |
| `A ~ B` | `B`  | `B` 位于同级的 `A` 后面                        |

例如 `.body + .hint` 选中紧跟 `.body` 的 `.hint`；`.hint:has(+ .action)` 则选中**后面紧跟 `.action` 的 `.hint`**。`+` 判断元素是否相邻时，不把两者间的文字或换行当作隔开的元素。

### Descendant Combinator 子代组合器
空格
```
.card h3 {
  color: red;
}
```

含义：匹配祖先元素中存在 `.card` 的所有 `h3` 元素
```
<div class="card">
  <h3>A ✅</h3>
  <section>
    <h3>B ✅</h3>
  </section>
</div>
<h3>C ❌</h3>
```

### Child Combinator 子代组合器
```
.card > h3 {
  color: red;
}
```

含义：匹配直接父元素具有 `.card` 类的 `h3` 元素。

依然使用上面的 HTML：
```
<div class="card">
  <h3>A ✅</h3>
  <section>
    <h3>B ❌</h3>
  </section>
</div>
```

### Next-sibling Combinator 相邻兄弟组合器
`+`

兄弟元素（Sibling Elements），指的是拥有同一个父元素的元素，例如：
```
<div>
  <h3>标题</h3>
  <p>A</p>
  <p>B</p>
</div>
```

这里 `h3`、第一个 `p`、第二个 `p` 都是兄弟元素

现在使用：
```
h3 + p {
  color: red;
}
```

匹配结果：
```
<div>
  <p>C ❌</p>
  <h3>标题</h3>
  <p>A ✅</p>
  <p>B ❌</p>
</div>
```

因为 `+` 要求右侧匹配的元素紧挨着左侧元素之后，并且两者具有相同的父元素。

有两个重要细节：

- 方向固定：`h3 + p` 匹配的是 `h3` 后面的 `p`，不是前面的
- 紧邻指相邻的元素节点，中间的空格、换行等文本节点不会破坏这种关系

### Subsequent-sibling Combinator 后续兄弟组合器
`~`
```
h3 ~ p {
  color: red;
}
```

```
<div>
  <p>A ❌</p>
  <h3>标题</h3>
  <p>B ✅</p>
  <span>其他内容</span>
  <p>C ✅</p>
</div>
```

这里 `~` 匹配的是：在 `h3` 之后、与它拥有同一个父元素的所有 `p` 元素，不要求紧邻

与 `+` 不同，`~` 可以跨越其他兄弟元素

不过要特别注意：
```
<div>
  <h3>标题</h3>
  <section>
    <p>A ❌</p>
  </section>
  <p>B ✅</p>
</div>
```

`h3 ~ p` 只匹配 B，A 虽然出现在 `h3` 之后，但 A 和 `h3` 并不是兄弟元素


### 易错点
认为 `>` 的特指度比空格更高 ❌
```
.card > h3 { color: red; }
.card h3 { color: blue; }
```

这两个选择器的特指度都是 `0-1-1`

`>` 和空格组合器本身都不增加特指度

因此，对于同时匹配两条规则的 `h3`，如果其他层叠条件相同，后面的蓝色声明胜出

匹配条件更严格，不代表特指度更高

---

这个选择器组，第一个是指向了所有 HTML 元素 `<h1>`。

cssCopy

```text
h1 {
}
```

它也包含了一个 class 的选择器：

cssCopy

```text
.box {
}
```

亦或，一个 id 选择器：

cssCopy

```text
#unique {
}
```



## 选择器列表
```text
h1 {
  color: blue;
}

.special {
  color: blue;
}
```

可以将它们组合起来，在它们之间加上一个逗号，变为选择器列表。

```text
h1, .special {
  color: blue;
}
```

空格可以在逗号前或后，你可能还会发现如果每个选择器都另起一行，会更好读些。

```text
h1,
.special {
  color: blue;
}
```



---
## 函数伪类（Functional pseudo-classes）
- `:is(A, B)`：匹配符合 `A` 或 `B` 的元素。
- `:where(A, B)`：匹配语义与 `:is()` 相同，但自身及参数对 specificity 的贡献为零，适合容易被覆盖的基础样式。
- `:not(A)`：匹配不符合 `A` 的元素。
- `:has(关系)`：根据关联元素是否存在来匹配**当前元素**。

例如 `.field:has(> input[aria-invalid="true"])` 给含有错误输入框的 `.field` 加样式；其中 `>` 要求输入框是直接子元素。`:is()`、`:not()`、`:has()` 的 specificity 由参数中最高者决定；`!important` 和 `@layer` 不属于 specificity。

---
## 状态、结构与伪元素
- `.field:focus-within`：自身或内部元素获得焦点时匹配外层。
- `button:focus-visible`：浏览器判断需要显示焦点提示时匹配按钮，不能简单等同于“键盘操作”。
- `li:nth-child(2)`：检查元素在**所有同级元素**中的位置。
- `li:nth-child(2 of :not([hidden]))`：先限定参与计数的同级元素，再取第二个。

伪类用 `:` 表示匹配条件；伪元素通常用 `::` 表示元素的特定部分或生成内容。例如 `.hint::before` 可添加装饰，重要信息仍应写在 HTML 中。
