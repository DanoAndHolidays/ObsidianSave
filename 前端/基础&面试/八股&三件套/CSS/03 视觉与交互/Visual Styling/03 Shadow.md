# Shadow
CSS 阴影属于==视觉绘制效果==，不参与盒模型尺寸计算，不会改变元素布局尺寸，但可能超出元素边界并与其他内容重叠

主要有三种阴影：

- `box-shadow`：基于元素盒子的轮廓生成阴影
- `text-shadow`：基于文字字形生成阴影
- `filter: drop-shadow()`：基于渲染结果的透明度（Alpha）生成阴影

---
## box-shadow
### 基本语法
```
box-shadow: offset-x offset-y blur spread color;
```

|参数|作用|
|---|---|
|`offset-x`|水平偏移，正数向右|
|`offset-y`|垂直偏移，正数向下|
|`blur`|模糊半径，不能为负|
|`spread`|扩散半径，正数扩大、负数缩小|
|`color`|阴影颜色|

只有水平和垂直偏移是必需的，其余参数可省略
```
.card {
  box-shadow: 0 8px 16px 2px rgb(0 0 0 / 20%);
}
```

![[Pasted image 20261015114945.png]]

Blur 与 Spread 的区别：

- `blur`：控制阴影边缘的模糊程度
- `spread`：控制生成阴影的基础轮廓扩大或缩小


### inset 内阴影
默认生成外部阴影，添加 `inset` 后生成内部阴影
```
.input {
  box-shadow: inset 0 2px 4px rgb(0 0 0 / 15%);
}
```

### 多重阴影
通过逗号分隔，支持叠加多个阴影。先声明的阴影位于后声明的阴影上方
```
.card {
  box-shadow:
    0 1px 3px rgb(0 0 0 / 10%),
    0 8px 24px rgb(0 0 0 / 15%);
}
```

### 与 border-radius 的关系
`box-shadow` 基于元素的 Border Box（边框盒）轮廓生成阴影，会遵循 `border-radius` 的圆角形状
```
.card {
  border-radius: 16px;
  box-shadow: 0 8px 24px rgb(0 0 0 / 15%);
}
```

---
## text-shadow
基于文字字形生成阴影，而不是整个元素盒子
```
text-shadow: offset-x offset-y blur color;
```

相比 `box-shadow`，不支持 `spread` 和 `inset`
```
.title {
  text-shadow: 2px 2px 4px rgb(0 0 0 / 30%);
}
```

支持多重阴影，可实现文字发光效果：
```
.title {
  color: white;
  text-shadow:
    0 0 4px #38bdf8,
    0 0 12px #38bdf8,
    0 0 24px #0284c7;
}
```

继承性区别：

- `box-shadow`：不继承
- `text-shadow`：默认继承

---
## filter: drop-shadow()
`drop-shadow()` 基于元素渲染结果的 Alpha Channel（透明度通道）生成阴影，适合透明 PNG、SVG 等不规则图形
```
.logo {
  filter: drop-shadow(0 8px 12px rgb(0 0 0 / 30%));
}
```

![[Pasted image 20261015115059.png]]

与 `box-shadow` 的区别：

|特性|`box-shadow`|`drop-shadow()`|
|---|---|---|
|阴影依据|盒子轮廓|渲染结果的透明度形状|
|扩散半径|支持|不支持|
|内部阴影|支持|不支持|
|多重阴影|逗号分隔|多个函数连续书写|
|典型用途|卡片、按钮、弹窗|透明图片、SVG|

注意：`drop-shadow()` 的模糊参数与 `box-shadow` 的模糊半径定义不同，相同数值不一定产生相同效果。
