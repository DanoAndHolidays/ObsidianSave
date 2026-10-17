# Color
CSS 颜色系统负责定义、计算和使用颜色。现代 CSS 不仅支持 RGB、HEX 等传统格式，还支持更符合人眼感知的颜色空间、动态颜色混合以及原生深浅色主题适配

---
## Color Models
### RGB / HEX
RGB 通过红（Red）、绿（Green）、蓝（Blue）三个通道描述颜色，HEX 是常见的十六进制颜色表示方式[[16 进制转 10]]
```
color: #ff0000;
color: rgb(255 0 0);
color: rgb(255 0 0 / 50%);
```

现代 CSS 支持空格分隔的 `rgb()` 语法，使用 `/` 指定 Alpha 透明度

### HSL
HSL 通过三个通道描述颜色：

- `H`（Hue）：色相，表示颜色种类。
- `S`（Saturation）：饱和度，表示颜色鲜艳程度。
- `L`（Lightness）：亮度，0% 为黑色，100% 为白色。

```
color: hsl(220 80% 50%);
```

HSL 方便人工调整颜色，但其 Lightness 不等于人眼感知亮度，不同色相使用相同 L 值时，视觉亮度可能不同。

### OKLCH
OKLCH 是现代感知导向的颜色表示方式：

- `L`（Lightness）：感知亮度。
- `C`（Chroma）：色度，描述颜色鲜艳程度。
- `H`（Hue）：色相角度。

```
color: oklch(65% 0.18 260);
```

优势：

- 更符合人眼对亮度变化的感知。
- 更适合生成视觉上均匀的颜色梯度和设计系统色阶。
- 支持表达广色域颜色，但最终显示受到设备色域限制。

选择建议： HEX / RGB 用于普通颜色定义；HSL 方便人工调色；OKLCH 更适合设计系统及系统化色阶。

---
## Alpha 与 opacity
### Alpha
Alpha Channel（透明度通道）属于颜色值的一部分，只影响使用该颜色值的绘制部分
```
.card {
  background: rgb(59 130 246 / 50%);
}
```

背景半透明，不影响子元素的文字和图标透明度

### opacity
整个元素的透明度
```
.card {
  opacity: 0.5;
}
```

`opacity` 作用于元素及其后代的整体绘制结果。

注意：

- `opacity` 不继承，但父元素的整体透明效果会影响子元素。

- 子元素设置 `opacity: 1` 无法抵消父元素的透明效果。

- `opacity` 小于 1 时会创建 [[Stacking Context 层叠上下文 ⌚️]]

- `opacity: 0` 只是视觉不可见，元素仍然可能参与布局、接收事件和键盘焦点。


|对比|Alpha|opacity|
|---|---|---|
|作用对象|单个颜色值|整个元素绘制结果|
|影响子元素|不会直接影响|会|
|改变布局|否|否|
|创建层叠上下文|本身不会|小于 1 时会|

---
## currentColor
`currentColor` 是特殊的颜色关键字，表示当前元素 `color` 属性的计算颜色值。
```
.button {
  color: royalblue;
  border: 1px solid currentColor;
  box-shadow: 0 0 0 2px currentColor;
}
```

当 `color` 变化时，使用 `currentColor` 的属性也会跟着变化。

常见于 SVG：
```
<svg>
  <path fill="currentColor" d="..." />
</svg>
```

注意：`currentColor` 使用的是当前元素的颜色，而不是直接读取父元素颜色；只是 `color` 本身具有继承性。

---
## color-mix()（颜色混合）
`color-mix()` 可以在 CSS 中根据指定色彩空间与比例动态混合颜色
```
color: color-mix(in srgb, red 50%, blue 50%);
```

基本语法：
```
color-mix(in 色彩空间, 颜色1 比例, 颜色2 比例)
```

实际项目中可以配合 CSS Variables 生成颜色：
```
:root {
  --primary: #2563eb;
}

.card {
  /* 主题色与白色混合 */
  background: color-mix(
    in oklab,
    var(--primary) 15%,
    white
  );
}
```

还可以与透明色混合：
```
.card {
  background: color-mix(
    in srgb,
    var(--primary) 20%,
    transparent
  );
}
```

注意：

- 混合结果受到色彩空间影响。
- `srgb` 与 `oklab` 的混合结果可能不同。
- 与白色混合和降低 Alpha 不是同一回事。

---
## 深色 / 浅色主题切换
[[深色模式]]
