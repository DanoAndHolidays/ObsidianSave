# Background
CSS Background（背景）属于视觉绘制，不参与元素的布局尺寸计算

- 背景默认可以==绘制到 Border Box==，但不会延伸到 Margin 区域
- 背景图片==不会撑开==元素，与 `<img>` 不同
- 背景可以包含颜色、图片、渐变等内容
- 背景会绘制在元素内容下方，透明边框可能透出背景

---
## 背景定位与裁剪
背景涉及两个重要区域：

|属性|作用|默认值|
|---|---|---|
|`background-origin`|确定背景图片的定位区域|`padding-box`|
|`background-clip`|限制背景的绘制区域|`border-box`|

```
.box {
  background-origin: padding-box;
  background-clip: content-box;
}
```

注意：

- `background-origin` 主要作用于背景图片，不影响纯背景色的定位
- `background-clip` 同时影响背景图片和背景色
- 使用 `background-attachment: fixed` 时，`background-origin` 不再决定背景图片的定位区域


---
## 背景图片缩放
`background-size` 控制背景图片尺寸

|值|行为|
|---|---|
|`auto`|根据图片的固有尺寸、比例等确定尺寸|
|`cover`|保持比例，完全覆盖定位区域，可能裁剪|
|`contain`|保持比例，完整显示图片，可能留白|
|`100% 100%`|强制匹配定位区域尺寸，可能拉伸变形|
![[Pasted image 20261015105301.png]]

```
.hero {
  background-image: url("banner.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
```

`background-position` 决定背景图片在定位区域中的对齐位置。

>注意：`cover` 和 `contain` 不会自动关闭背景重复，通常配合 `no-repeat` 使用。

---
## 多层背景
CSS 支持为同一个元素设置多个背景图片，渐变也可以作为背景图片。

绘制顺序：==先声明==的背景图片==在上层==，后声明的在下层，`background-color` 位于最底层
```
.hero {
  background-image:
    linear-gradient(
      rgb(0 0 0 / 50%),
      transparent
    ),
    url("banner.jpg");

  background-size: cover;
  background-position: center;
}
```

常用于图片遮罩、渐变覆盖和复杂视觉效果

---
## background 简写属性
`background` 是简写属性，会重置没有显式指定的背景子属性
```
.box {
  background:
    url("image.jpg")
    center / cover
    no-repeat;
}
```

其中：

- `center`：`background-position`
- `cover`：`background-size`
- `no-repeat`：`background-repeat`

`background-size` 在简写中必须放在 `background-position` 后面，并使用 `/` 分隔。
