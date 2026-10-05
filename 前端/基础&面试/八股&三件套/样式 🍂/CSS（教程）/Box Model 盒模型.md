# Box Model 盒模型
> Last Format Time：10/6/2026 02:27:25

CSS 的盒模型主要包括以下两种，可通过 [box-sizing](https://developer.mozilla.org/zh-CN/docs/Web/CSS/box-sizing) 属性进行配置：

- `content-box`：标准盒模型，默认属性，width 只包含 content，padding 和 border会自己在加上去，最终的宽度会大于等于 width
- `border-box`：IE盒模型（怪异盒模型）width 包含 (content、padding、border)


---
## CSS 布局的基本对象是 Box
浏览器布局时，并不是直接对 DOM Element 进行布局，而是元素根据 CSS 生成 **Box（盒）**，真正参与布局的是这些 Box：
```text
DOM Element
→ CSS
→ Box Tree
→ Layout
```

因此：
```text
Element ≠ Box
DOM Tree ≠ Box Tree
```

一个元素通常会生成 Box，但不是绝对一一对应，例如 `display: contents`。

---
## Box Model
一个普通盒模型包含：
```text
margin
└─ border
   └─ padding
      └─ content
```

其中：

- `content box`：内容区域
- `padding box`：content + padding
- `border box`：content + padding + border
- `margin`：盒子外部空间，不属于 border box

背景默认会绘制到 padding 区域，margin 本身没有背景

### `box-sizing`
##### `content-box`
默认：
```text
box-sizing: content-box;
```

此时：
```text
width = content width

最终 border box 宽度
= width + padding-left/right + border-left/right
```

例如：
```text
width: 300px;
padding: 20px;
border: 5px solid;
```

最终 border box：
```text
300 + 40 + 10 = 350px
```

##### `border-box`
项目中通常使用：
```text
box-sizing: border-box;
```

此时：
```text
width = border box width
```

即：
```text
content + padding + border = width
```

例如：
```text
width: 300px;
padding: 20px;
border: 5px solid;
```

content width：
```text
300 - 40 - 10 = 250px
```

常见全局配置：
```text
html {
  box-sizing: border-box;
}

*,
*::before,
*::after {
  box-sizing: inherit;
}
```


#####  `width` 不等于最终视觉宽度
更准确的理解：
```text
width
→ 参与 sizing algorithm
→ 得到 used size
→ 结合 box-sizing / padding / border
→ 得到最终 Box
```

例如百分比：
```text
width: 50%;
```

必须结合 containing block 的尺寸才能得到最终 used width，所以`width` 是尺寸计算过程的输入，不一定等于元素最终实际占据的宽度。

### Padding 与 Margin
`padding`：

- 属于元素自身 Box
- 位于 content 与 border 之间
- 背景通常覆盖 padding

`margin`：

- 位于 border box 外部
- 描述 Box 与周围布局之间的空间
- 不属于 border box
- 在普通流中可能发生 margin collapsing

Margin Collapse 后面结合 **Normal Flow / Formatting Context** 再系统学习。


### 核心 mental model
```text
Element
↓
生成 Box
↓
Box Model 决定盒子的组成
↓
display 决定 Box 如何参与布局
↓
Formatting Context 决定布局算法
↓
得到最终尺寸和位置
```