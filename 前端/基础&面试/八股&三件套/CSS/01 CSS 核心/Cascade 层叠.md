# Cascade 层叠
> Last Format Time：10/6/2026 02:27:25

Cascade（层叠）用于解决同一个元素、同一个 CSS 属性存在多个候选声明时，浏览器应该选择哪一个

例如：
```css
p {
    color: red;
}

.title {
    color: blue;
}

p {
    color: green;
}
```

对于：
```html
<p class="title">Hello</p>
```

浏览器需要决定最终使用哪一个 `color`。

---
## Cascade 的现代决策顺序
现代 CSS（Cascade Level 5/6）大致顺序：
```text
Origin（来源）
        │
        ▼
Importance（!important）
        │
        ▼
Cascade Layer（@layer）
        │
        ▼
Specificity（特异性）
        │
        ▼
Scoping Proximity（@scope）
        │
        ▼
Source Order（源码顺序）
```

> **Specificity 只是 Cascade 的一个步骤，不是全部。**

### Origin（来源）
CSS 来源主要有三种：
```text
User Agent（浏览器默认样式）

↓

User（用户样式）

↓

Author（开发者样式）
```

默认优先级：
```text
Author

>

User

>

User Agent
```

### Importance（重要性）
即：
```css
!important
```

例如：
```css
p {
    color: red !important;
}

.title {
    color: blue;
}
```

最终：
```text
red
```

`!important` 不是提高 Specificity，而是在 Specificity 之前参与 Cascade


### Cascade Layer（层）
现代 CSS 引入：
```css
@layer base {}
@layer components {}
@layer utilities {}
```

浏览器会先比较：
```text
Layer
```

再比较：
```text
Specificity
```

因此：
```css
@layer base {
    .title {
        color: red;
    }
}

@layer components {
    .title {
        color: blue;
    }
}
```

最终：
```text
blue
```

即使两个选择器完全相同。

### Specificity（特异性）
[[Specificty 权重]]
比较哪个选择器更具体

例如：
```css
p
```

VS

```css
.title
```

↓

```text
.title
```

获胜。

> Specificity 是 Cascade 的第四步，而不是第一步。


### Scoping Proximity
主要配合：
```css
@scope
```

多个 Scope 同时匹配时，比较哪个 Scope 离当前元素更近，目前实际项目使用较少。

### Source Order（源码顺序）
前面的比较全部相同后，后写覆盖前写

例如：
```css
.title {
    color: red;
}

.title {
    color: blue;
}
```

最终：
```text
blue
```

---
## DevTools
### Styles 面板
用于观察：
- 哪些规则参与 Cascade
- 哪条规则获胜
- 哪些规则被覆盖

被划线表示参与 Cascade，但没有获胜


### Computed 面板
用于观察浏览器最终计算后的属性值

源码：
```css
font-size: 2em;
```

Computed：
```text
40px
```

---
## 核心结论（面试 & 工程）
```text
多个 CSS 声明
        │
        ▼
Cascade（决定哪个声明获胜）
        │
        ▼
Cascaded Value
        │
        ▼
Value Computation（计算真正含义）
        │
        ▼
Computed Value
        │
        ▼
Layout（得到 Used Value）
        │
        ▼
Paint
```

1. **Cascade 负责"选规则"，Value Computation 负责"算值"。**
2. **Specificity 只是 Cascade 的一环，不等于 Cascade。**
3. **`!important` 不属于 Specificity，而是在 Specificity 之前参与比较。**
4. **`@layer` 的比较优先于 Specificity，是现代 CSS 推荐的覆盖管理方式。**
5. **Computed Value 不一定是最终布局尺寸，真正参与布局的是 Used Value。**