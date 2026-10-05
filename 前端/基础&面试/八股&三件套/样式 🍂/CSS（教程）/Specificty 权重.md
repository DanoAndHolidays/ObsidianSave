# Specificty 权重
> Last Format Time：10/6/2026 02:27:25

CSS 嵌套语法：
```text
.home-page {
  .home-page-btn {
    color: red;
  }
}
```

它表达的选择关系相当于：
```text
.home-page .home-page-btn {
  color: red;
}
```

意思是：选中 `.home-page` **里面的后代元素** `.home-page-btn`。


Specificity 用于 Cascade 中继续判断多个候选声明谁获胜，它只是 Cascade 的一个阶段，不等于完整的“CSS 优先级”。

整体位置：
```text
Origin / Importance
→ Cascade Layer
→ Specificity
→ Scoping Proximity
→ Source Order
```

因此：

- `!important` 不是提高 Specificity，而是在更早的 Cascade 阶段参与竞争。
- `@layer` 也比 Specificity 更早参与比较。
- 只有前面的 Cascade 条件打平后，才比较 Specificity。

---
## 计算模型
不要使用旧的：
```text
ID = 100
class = 10
tag = 1
```

Specificity 应理解成三个独立的列：
```text
ID - CLASS - TYPE
```

并且从左向右逐列字典序比较，而不是做普通加法：
```css
#app .card button:hover
```

计算：
```text
#app    → ID +1
.card   → CLASS +1
:hover  → CLASS +1
button  → TYPE +1

Specificity = 1-2-1
```

比较：
```text
1-0-0
>
0-100-100
```

因为首先比较 ID 列，第一列已经分出胜负，后面的数字不再考虑。


---
## 三个分类
### ID
ID selector：
```css
#app
```

得到：
```text
1-0-0
```

### CLASS
以下都属于 CLASS 这一列：
```css
.card
[data-active]
:hover
:nth-child(...)
```

即：
- class selector 类选择器
- attribute selector 属性选择器
- pseudo-class 伪类

例如：
```css
.card:hover[data-active]
```

得到：
```text
0-3-0
```

### TYPE
以下属于 TYPE：

- element/type selector 元素/类型选择器
- pseudo-element 伪元素

例如：
```css
button::before
```

得到：
```text
0-0-2
```


---
## 不增加 Specificity 的内容
通配选择器：
```css
* 0-0-0
```

组合符也不增加 Specificity：
```text
空格
>
+
~
```

例如：
```css
.main > .card + p 0-2-1
```


---
## Inline Style
行内样式：
```html
<div style="color: red">
```

可以在教学模型中理解成额外的一层：
```text
INLINE - ID - CLASS - TYPE
```

普通 selector 无法单纯依靠更高 Specificity 覆盖 normal inline style。

但 inline style 并不是脱离 Cascade 的“无敌规则”，例如 `!important` 仍可能在更早的 Cascade 阶段击败它。


---
## 特殊规则
*这玩阴真有人知道吗*
### `:is()`
`:is()` 自身不增加 Specificity。

它采用参数列表中**最高的 Specificity**：

```css
:is(.card, #app, button)
```

参数分别是：

```text
.card   → 0-1-0
#app    → 1-0-0
button  → 0-0-1
```

因此整体：

```text
1-0-0
```

即使实际匹配元素的是 `.card`，参数中存在 `#app`，整体仍然按照最高值计算。

### `:not()`
`:not()` 自身不增加 Specificity，参数贡献 Specificity。

```css
button:not(.disabled)
```

为：

```text
button     → 0-0-1
.disabled  → 0-1-0

总计 → 0-1-1
```

### `:has()`
规则与 `:is()` 类似：

```css
.card:has(img)
```

为：

```text
0-1-1
```

如果参数中出现 ID：

```css
.card:has(#selected)
```

则为：

```text
1-1-0
```

因此 `:has()` 也可能制造较高的 Specificity。

### `:where()`
`:where()` 最特殊：

> 无论参数多复杂，`:where()` 本身以及参数贡献的 Specificity 永远为 `0-0-0`。

例如：

```css
:where(#app .page .card:hover)
```

依然：

```text
0-0-0
```

因此它非常适合：

- 基础样式
    
- Reset
    
- 组件库
    
- Design System
    

可以对 DOM 结构进行约束，同时保持样式容易被覆盖。

例如：

```css
:where(.card) button {
  color: black;
}
```

只有 `button` 本身贡献：

```text
0-0-1
```

用户可以很容易通过：

```css
.my-button {
  color: red;
}
```

进行覆盖。

---
## Specificity 相同
如果：
```css
.card {
  color: red;
}

.title {
  color: blue;
}
```

两者都是：
```text
0-1-0
```

并且其它 Cascade 条件也完全一致，就继续比较 Source Order 后出现的声明获胜，因此“后写覆盖前写”只有在前面的 Cascade 条件全部打平时才成立。

---
## 工程原则
不要追求“如何写出更高的 Specificity”，而应该尽量保持 Specificity 低、稳定、可预测。

避免：
```css
#app .page .content .card .header .button {}
```

否则为了覆盖它，很容易不断增加选择器复杂度，最后演变成：
```css
!important
```

这种现象称为**Specificity War（特异性战争）**，现代工程中可以结合：

- 组件化
- CSS Modules
- `@layer`
- `:where()`

控制 Specificity。