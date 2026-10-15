# Transition 过度
当 CSS 属性的值发生变化时，浏览器在起始值和目标值之间生成平滑的过渡效果

核心流程：样式状态变化 → 确定起始值与目标值 → 根据时间函数计算进度 → 属性插值 → 完成过渡

注意：

- Transition 本身不负责触发样式变化，`:hover`、class 切换等才是触发来源
- Transition 负责计算中间值，不需要 JavaScript 每帧手动更新
- 不是所有 CSS 属性都支持连续插值

```
.box {
  opacity: 1;
  transition: opacity 300ms;
}

.box:hover {
  opacity: 0.5;
}
```

通常把 `transition` 放在==基础状态==上，保证进入和离开时都能平滑过渡

## Transition 属性
`transition` 是以下五个属性的简写：

|属性|作用|默认值|
|---|---|---|
|`transition-property`|指定参与过渡的属性|`all`|
|`transition-duration`|持续时间|`0s`|
|`transition-timing-function`|变化速度曲线|`ease`|
|`transition-delay`|开始前的延迟|`0s`|
|`transition-behavior`|控制离散属性能否参与过渡|`normal`|

```
.box {
  transition:
    opacity 300ms ease 100ms,
    transform 200ms ease-out;
}
```

表示：

- `opacity` 延迟 `100ms`，再过渡 `300ms`
- `transform` 立即开始，持续 `200ms`

## Timing Function（时间函数）

|函数|特点|
|---|---|
|`linear`|匀速变化|
|`ease`|先加速后减速，默认值|
|`ease-in`|慢 → 快|
|`ease-out`|快 → 慢|
|`ease-in-out`|慢 → 快 → 慢|
|`cubic-bezier()`|自定义缓动曲线|
|`steps()`|阶梯式跳变|

### cubic-bezier()
```
.box {
  transition: transform 300ms
    cubic-bezier(0.25, 0.1, 0.25, 1);
}
```

![[Pasted image 20261015212959.png]]

`cubic-bezier(x1, y1, x2, y2)` 定义==三次贝塞尔曲线==

- 起点 P0 固定为 `(0,0)`。
- 终点 P3 固定为 `(1,1)`。
- P1、P2 为两个控制点。
- X 轴表示时间进度，Y 轴表示变化进度。
- `x1`、`x2` 必须在 `0～1`，`y1`、`y2` 可以超出该范围。

注意：曲线描述的是变化进度，不是元素实际的运动轨迹。

### steps()
```
.box {
  transition: transform 1s steps(4, end);
}
```

将变化进度拆成四次跳变。

- `start`：每个区间开始时跳变
- `end`：每个区间结束时跳变


适用于逐帧动画、精灵图等场景。

## Interpolation（插值）
插值是浏览器根据起始值、目标值和变化进度计算中间值的过程

不同属性具有不同的动画类型：

|属性|插值方式|
|---|---|
|`opacity`|数值插值|
|`width: 100px → 200px`|长度插值|
|`background-color`|颜色插值|
|`transform`|变换插值|
|`display`|离散变化|

例如：
```
.box {
  width: 100px;
  transition: width 1s linear;
}

.box:hover {
  width: 200px;
}
```

经过 `500ms` 时，宽度的理想中间值为 `150px`

而 `display` 不支持连续插值。现代 CSS 可以通过 `transition-behavior: allow-discrete` 让部分离散属性参与过渡，但其值依旧是在特定时刻切换，而不是连续变化

---
## 工程实践总结笔记
### 避免滥用 transition: all
```
/* 不推荐 */
.box {
  transition: all 300ms;
}

/* 推荐 */
.box {
  transition:
    opacity 200ms ease,
    transform 300ms ease;
}
```

`transition: all` 会让所有符合过渡条件的属性变化都可能参与过渡

主要问题：

- 容易产生非预期动画
- 后续修改样式可能意外引入过渡
- 如果涉及 `width`、`height` 等布局属性，可能产生额外布局计算


推荐明确声明需要过渡的属性，而不是直接使用 `all`

### height: auto 的过渡
传统 CSS Transition 无法直接在 `0px` 和 `auto` 之间连续插值，因为 `auto` 不是固定的长度数值。

现代 CSS 支持使用 `interpolate-size`：
```
.panel {
  interpolate-size: allow-keywords;
  height: 0;
  overflow: hidden;
  transition: height 300ms;
}

.panel.open {
  height: auto;
}
```

注意浏览器兼容性。

还可以使用 Grid 实现折叠面板：
```
.panel {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 300ms;
}

.panel > .content {
  min-height: 0;
  overflow: hidden;
}

.panel.open {
  grid-template-rows: 1fr;
}
```

### Transition 的中断与反向
Transition 执行过程中，如果目标样式发生变化，浏览器可以中断当前过渡，从当前动画值附近向新目标值过渡。

对于反向过渡，浏览器还有专门的时间缩短规则，并不是每次都重新执行完整的 `duration`。

特别注意：React 如果直接卸载 DOM，原有的退出过渡可能无法显示。

### Transition 与浏览器渲染性能
浏览器渲染流水线：

`Style → Layout → Paint → Composite`

|属性|典型性能影响|
|---|---|
|`width` / `height`|可能触发 Layout、Paint、Composite|
|`background-color`|通常涉及 Paint|
|`transform`|通常可以进行合成优化|
|`opacity`|通常可以进行合成优化|

工程建议：

- 视觉移动使用 `transform: translate()`。

- 视觉缩放使用 `transform: scale()`。

- 淡入淡出使用 `opacity`。

- 真正改变布局尺寸时仍然使用相应布局属性。


`transform` 不会像修改普通布局尺寸那样推动周围元素重新布局。

`will-change` 可以提供优化提示，但不应滥用，可能增加内存消耗。

### Transition 相关事件

|事件|含义|
|---|---|
|`transitionrun`|过渡创建|
|`transitionstart`|过渡正式开始|
|`transitionend`|正常结束|
|`transitioncancel`|过渡取消|

```
element.addEventListener("transitionend", (event) => {
  if (event.propertyName === "opacity") {
    console.log("opacity 过渡结束");
  }
});
```

注意：

- 一个元素的多个过渡属性可能分别产生事件。
- Transition 被取消时不能依赖 `transitionend` 一定触发。
- React 中要考虑组件卸载、过渡中断、持续时间为零等边界情况。

核心结论：Transition 负责样式变化过程中的插值与时间控制，动画性能最终还取决于所修改的 CSS 属性及浏览器渲染行为。
