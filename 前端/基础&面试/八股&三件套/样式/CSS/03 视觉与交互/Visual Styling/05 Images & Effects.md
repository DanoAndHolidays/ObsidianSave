# Images & Effects

---
## 图片的布局模型
`<img>`、`<video>` 等属于 [Replaced Element](https://developer.mozilla.org/zh-CN/docs/Glossary/Replaced_elements)，其内容由外部资源决定。

图片通常具有固有尺寸（Intrinsic Size）和固有宽高比（Intrinsic Aspect Ratio），需要区分：

- 元素盒子尺寸：由 CSS 的 `width`、`height` 等布局规则决定。
- 图片内容尺寸：图片资源在元素盒子内部实际呈现的尺寸。

我们发现这里有两个不同的尺寸，`object-fit` 和 `object-position` 就是用来控制图片内容如何在元素盒子中呈现，不会改变元素盒子本身的布局尺寸

---
## object-fit
`object-fit` 控制==替换元素==的内容如何适应元素的 Content Box（内容盒）

|属性值|作用|
|---|---|
|`fill`|默认值，拉伸填满容器，可能变形|
|`contain`|等比例缩放，完整显示，可能留白|
|`cover`|等比例缩放，填满容器，可能裁剪|
|`none`|不根据容器尺寸缩放内容|
|`scale-down`|在 `none` 和 `contain` 中选择较小的结果|

最常用的是 `contain` 和 `cover`
```
/* 完整显示，允许留白 */
.product-image {
  width: 300px;
  height: 300px;
  object-fit: contain;
}

/* 填满容器，允许裁剪 */
.cover-image {
  width: 300px;
  height: 300px;
  object-fit: cover;
}
```

核心区别：

- `contain`：优先保证图片内容完整
- `cover`：优先保证容器被铺满

---
## object-position
`object-position` 控制替换元素的内容在元素盒子中的对齐位置，尤其适用于 `cover` 导致的裁剪场景

默认值为 `50% 50%`，即居中
```
.avatar {
  width: 200px;
  height: 200px;
  object-fit: cover;

  /* 水平居中，垂直顶部 */
  object-position: center top;
}
```

常见写法：
```
object-position: center;
object-position: left top;
object-position: right center;
object-position: 75% 30%;
```

百分比表示图片内容上的对应百分比位置与容器对应位置对齐，而不是简单地移动容器宽度的某个百分比。

### 与背景图片的区别

|替换元素内容|CSS 背景图片|
|---|---|
|`object-fit`|`background-size`|
|`object-position`|`background-position`|
|`<img>`、`<video>` 等|`background-image`|

实际工程中，有内容语义的图片优先使用 `<img>`，纯装饰性图片可以使用 CSS 背景

---
## filter（元素滤镜）
`filter` 对元素==自身及其后代==的整体渲染结果应用视觉处理，而不只是处理背景
### 常见滤镜函数

|函数|作用|
|---|---|
|`blur(5px)`|模糊|
|`brightness(0.8)`|降低亮度|
|`contrast(1.2)`|增加对比度|
|`grayscale(1)`|完全灰度|
|`saturate(1.5)`|增加饱和度|
|`hue-rotate(90deg)`|旋转色相|
|`invert(1)`|反转颜色|
|`drop-shadow()`|根据透明度轮廓生成阴影|

支持多个滤镜组合，按照声明顺序依次执行：
```
.image {
  filter:
    brightness(0.9)
    contrast(1.1)
    saturate(1.2);
}
```

滤镜应用==顺序==可能影响最终结果，例如：
```
.card {
  filter: blur(5px);
}
```

整个卡片的渲染结果都会被模糊，包括内部文字、图标等内容。

---
## backdrop-filter（背景滤镜）
`backdrop-filter` 对==元素背后的画面==应用滤镜，而不是对元素自身内容应用滤镜

常用于实现毛玻璃（Glassmorphism）效果
```
.glass-card {
  background: rgb(255 255 255 / 30%);
  backdrop-filter: blur(16px);
}
```

这里有两个关键点：

- `backdrop-filter`：对背后画面进行模糊。
- 半透明 `background`：让处理后的背景能够透出来。

如果元素背景完全不透明，就可能遮住背后的滤镜效果

### Backdrop Root（背景滤镜根）
`backdrop-filter` 受到 Backdrop Root 的限制

当祖先元素具有某些属性，例如 `filter` 或小于 1 的 `opacity` 时，可能形成新的 Backdrop Root，使子元素无法继续对更外层的画面进行背景滤镜处理

因此毛玻璃效果不符合预期时，需要检查：

- 元素背景是否具有透明度。
- 祖先元素是否存在 `filter`、`opacity` 等影响 Backdrop Root 的属性。

---
## 滤镜与浏览器渲染
### 对 Layout 的影响
`filter` 和 `backdrop-filter` 属于视觉效果，通常不会改变元素在布局中的尺寸，也不会因为模糊范围扩大而推开相邻元素。

但滤镜可能带来额外的绘制、栅格化或合成成本

尤其是：

- 大范围 `blur()`。
- 大面积 `backdrop-filter`。
- 持续变化的复杂滤镜动画。


具体性能表现需要通过 DevTools 测量

### 对 Stacking Context 的影响
`filter` 和 `backdrop-filter` 在值不为 `none` 时，会创建 Stacking Context（层叠上下文）

另外，非 `none` 的 `filter` 通常还会为绝对定位和固定定位的后代建立 Containing Block（包含块）

因此，滤镜并不只是视觉属性，也可能影响元素内部的层叠和定位行为
