# Border & Outline

---
## Border
Border 是 CSS 盒模型的一部分，会==参与==元素==尺寸计算==
```
.box {
  border: 2px solid red;
}
```

简写包含三个属性：

- `border-width`：边框宽度
- `border-style`：边框样式，默认 `none`，所以不设置不会有边框
- `border-color`：边框颜色

注意：

- `box-sizing: content-box`：Border 会增加元素的边框盒尺寸 [[Box Model 盒模型]]
- `box-sizing: border-box`：Border 包含在指定的宽高中，会挤占内容区域
- `border: none`：边框不占据空间
- `border: 2px solid transparent`：边框透明，但仍然占据 2px 的空间

---
## Outline
Outline 是绘制在元素边界周围的==视觉轮廓==，不参与盒模型尺寸计算，不影响布局
```
.button {
  outline: 2px solid royalblue;
  outline-offset: 4px;
}
```

其中 `outline-offset` 控制轮廓相对边框的偏移量，可以为负值

### Border 与 Outline 的区别

|特性|Border|Outline|
|---|---|---|
|属于盒模型|是|否|
|参与尺寸计算|是|否|
|可以分别设置四边|是|否|
|支持圆角|`border-radius`|通常跟随元素圆角|
|典型用途|元素边界|焦点提示、视觉强调|

### focus-visible

- `:focus`：元素获得焦点
- `:focus-visible`：元素获得焦点，且浏览器判断==需要显示焦点提示==

```
.button:focus-visible {
  outline: 2px solid royalblue;
  outline-offset: 3px;
}
```

`:focus-visible` 不完全等于键盘触发，它由浏览器的启发式规则决定

不要随意使用 `outline: none` 移除焦点提示，否则可能影响键盘操作的可访问性

---
## border-radius
`border-radius` 用于定义盒子边界的圆角形状
```
.box {
  border-radius: 20px;
}
```

圆角不一定是圆弧，也可以使用椭圆半径：
```
.box {
  /* 水平半径 / 垂直半径 */
  border-radius: 40px / 20px;
}
```

百分比半径相对于对应盒子的宽度和高度计算：
```
.circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}
```

当盒子宽高相等时，`50%` 可以形成圆形；宽高不等时通常形成椭圆

### 圆角与裁剪

- `border-radius` 定义边框外边缘的圆角形状
- 背景也会按照对应区域的圆角进行绘制或裁剪
- 子元素不会仅仅因为父元素设置了 `border-radius` 就自动被裁剪

```
.card {
  border-radius: 16px;
  overflow: hidden;
}
```

`overflow: hidden` 可以裁剪超出的子元素，但也可能裁掉阴影、下拉菜单等内容

---
## 渐变边框
`border-color` 不能直接设置 `linear-gradient()`，实际工程中常使用 透明边框 + 多层背景 实现渐变圆角边框：
```
.card {
  border: 2px solid transparent;
  border-radius: 16px;

  background:
    linear-gradient(white, white) padding-box,
    linear-gradient(135deg, #6366f1, #ec4899) border-box;
}
```

实现原理：

1. 透明 Border 为渐变边框预留空间

2. 第一层背景裁剪到 Padding Box，覆盖元素内部

3. 第二层渐变背景绘制到 Border Box

4. 第一层覆盖第二层内部区域，只露出边框区域的渐变

5. `border-radius` 负责圆角形状
