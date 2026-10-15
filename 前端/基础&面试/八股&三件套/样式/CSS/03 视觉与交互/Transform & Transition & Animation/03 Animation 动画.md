# Animation 动画

---
## 核心模型
CSS Animation 用于根据**时间轴（Timeline）和关键帧（Keyframes）**，让元素的 CSS 属性随时间变化

与 Transition 的区别：

|对比|Transition|Animation|
|---|---|---|
|核心机制|样式状态变化时进行过渡|根据关键帧和时间轴执行|
|触发|通常需要样式状态发生变化|应用动画后即可自动执行|
|中间状态|连接起点与终点|支持多个关键帧|
|循环|无内置循环配置|支持无限循环|
|场景|Hover、展开、收起|Loading、入场、多阶段动画|

**Animation 的运行模型：**

1. 浏览器找到 `@keyframes` 定义

2. 创建动画，确定持续时间、延迟、执行次数等

3. 根据时间轴计算当前时间进度

4. 通过 Timing Function（缓动函数）计算插值进度

5. 根据属性的插值规则计算当前 CSS 值

6. 将得到的动画样式用于当前帧的渲染


---
## 定义关键帧
```
@keyframes move {
  0% {
    transform: translateX(0);
  }

  50% {
    transform: translateX(200px);
  }

  100% {
    transform: translateX(0);
  }
}

.box {
  animation: move 2s linear infinite;
}
```

- `0%`：动画起始进度
- `50%`：动画进行到一半
- `100%`：动画结束进度

- `from` 等价于 `0%`，`to` 等价于 `100%`

- 百分比表示动画进度，不表示 CSS 属性变化量的百分比
- 不要求必须声明 `0%` 和 `100%`；缺失时，相关属性通常使用元素的基础样式作为端点

**注意：** `@keyframes` 只是定义动画，必须通过 `animation-name` 将其应用到元素上

---
## Animation 核心属性

|属性|作用|默认值|
|---|---|---|
|`animation-name`|动画名称|`none`|
|`animation-duration`|每轮动画持续时间|`0s`|
|`animation-timing-function`|缓动函数|`ease`|
|`animation-delay`|开始前的延迟|`0s`|
|`animation-iteration-count`|执行次数|`1`|
|`animation-direction`|执行方向|`normal`|
|`animation-fill-mode`|动画前后的样式填充|`none`|
|`animation-play-state`|运行或暂停|`running`|

### animation-direction

- `normal`：每轮从 0% → 100%
- `reverse`：每轮从 100% → 0%
- `alternate`：正向、反向交替
- `alternate-reverse`：反向、正向交替


```
.box {
  animation: move 2s infinite alternate;
}
```

### animation-fill-mode
控制动画在执行前的延迟阶段、执行结束后如何应用关键帧样式

|值|效果|
|---|---|
|`none`|不在动画执行前后额外应用关键帧样式|
|`forwards`|结束后继续应用结束位置的关键帧样式|
|`backwards`|延迟阶段应用起始位置的关键帧样式|
|`both`|两种效果都有|

```
.box {
  opacity: 0.5;
  animation: fadeIn 2s 1s both;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

默认正向运行时：

- 0～1s：应用 `opacity: 0`。
- 1～3s：逐渐变成 `opacity: 1`。
- 3s 之后：继续应用 `opacity: 1`。


注意：

- `forwards` 保留的是动画效果，并不会修改原始 CSS 声明。
- 使用 `reverse`、`alternate` 时，实际起始和结束关键帧取决于方向和迭代次数。
- 不应该把 `forwards` 当成管理组件永久状态的工具。


### animation-play-state
```
.box {
  animation: spin 2s linear infinite;
}

.box:hover {
  animation-play-state: paused;
}
```

`paused` 暂停动画，`running` 恢复动画。

暂停不会重置动画进度。

### animation 简写
```
.box {
  animation: move 2s ease-in 0.5s infinite alternate both;
}
```

对应：
```
animation-name: move;
animation-duration: 2s;
animation-timing-function: ease-in;
animation-delay: 0.5s;
animation-iteration-count: infinite;
animation-direction: alternate;
animation-fill-mode: both;
```

**简写中的第一个时间值是 duration，第二个是 delay。**

---
## Timing Function
[[02 Transition 过度]]
### cubic-bezier()
### steps()：阶梯函数
### 关键帧之间的缓动函数
**Timing Function 是在相邻关键帧区间分别应用的，不一定作用于整个动画的完整时间范围。**
```
@keyframes move {
  0% {
    transform: translateX(0);
    animation-timing-function: ease-in;
  }

  50% {
    transform: translateX(100px);
    animation-timing-function: ease-out;
  }

  100% {
    transform: translateX(200px);
  }
}
```

- 0%～50%：使用 `ease-in`。

- 50%～100%：使用 `ease-out`。

一般而言，一个关键帧上的时间函数作用于从该关键帧开始的后续关键帧区间。

---
## Interpolation
不同 CSS 属性具有不同的动画类型（Animation Type）

|类型|说明|
|---|---|
|Not animatable|不能参与动画|
|Discrete|离散切换|
|By computed value|按计算值及对应数据类型进行插值|
|Repeatable list|按列表项目匹配并插值|

### 数值插值
```
@keyframes fade {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

数值按照进度计算中间值。

### 颜色插值
```
@keyframes colorChange {
  from { background-color: red; }
  to { background-color: blue; }
}
```

颜色通过对应的颜色插值规则计算中间值，不能一概理解成 RGB 通道简单平均。

### Transform 插值
```
@keyframes move {
  from {
    transform: translateX(0) rotate(0deg);
  }

  to {
    transform: translateX(200px) rotate(90deg);
  }
}
```

浏览器可能分别插值匹配的变换函数，也可能需要使用变换矩阵分解等方式处理。

### 离散动画
```
@keyframes change {
  from { font-family: Arial; }
  to { font-family: Georgia; }
}
```

`font-family` 无法连续插值，因此会在特定进度发生切换。

普通离散插值通常在 50% 处切换，但某些属性存在特殊规则。

---
## 多个 Animation 组合
### 多动画运行
一个元素可以同时运行多个动画，使用逗号分隔。每个动画可以具有独立的持续时间、缓动函数和播放次数
```
.box {
  animation:
    move 2s ease infinite,
    fade 1s linear infinite;
}
```

- 不同属性：可以同时动画，互不冲突。

- 相同属性：默认使用 `replace` 合成方式，通常由动画列表中靠后的动画覆盖前面的效果。

- `transform` 是一个完整属性，`translateX()` 和 `rotate()` 默认不会自动合并。


### animation-composition
控制多个动画对同一 CSS 属性的合成方式。

|属性值|作用|
|---|---|
|`replace`|替换底层值，默认行为|
|`add`|在底层效果上添加动画效果|
|`accumulate`|对支持累积的值进行累积合成|

```
.box {
  animation:
    move 2s infinite,
    rotate 2s infinite;

  animation-composition: replace, add;
}
```

注意：`add` 和 `accumulate` 的具体行为取决于属性值类型，两者不是简单的数值相加。

工程实践： 如果只是组合平移和旋转，也可以让父元素负责平移、子元素负责旋转，避免属性冲突。

---
## Animation 生命周期事件
CSS Animation 提供四种事件：

|事件|触发时机|
|---|---|
|`animationstart`|动画开始|
|`animationiteration`|完成一次迭代并继续下一次|
|`animationend`|动画正常结束|
|`animationcancel`|动画中途被取消|

```
element.addEventListener("animationend", (event) => {
  console.log(event.animationName);
  console.log(event.elapsedTime);
});
```

其中：

- `animationName`：触发事件的动画名称。
- `elapsedTime`：动画已经运行的时间，单位为秒，不包含暂停时间。


注意：

- `infinite` 动画不会自然触发 `animationend`。

- 动画取消时，不会触发正常结束的 `animationend`。

- 多个动画可以分别触发事件。

- 动画事件会冒泡，需要时可以检查 `event.target === event.currentTarget`。


### React 中的动画生命周期
React 控制 DOM 是否存在，CSS 负责动画执行。

例如退出动画：
```
const [exiting, setExiting] = useState(false);

return (
  <div
    className={exiting ? "exit" : "enter"}
    onAnimationEnd={(e) => {
      if (
        e.target === e.currentTarget &&
        exiting &&
        e.animationName === "fade-out"
      ) {
        onRemove();
      }
    }}
  >
    <button onClick={() => setExiting(true)}>
      关闭
    </button>
  </div>
);
```

正确流程：

设置退出状态 → 播放退出动画 → 动画结束 → React 卸载组件。

不要直接把组件从 JSX 中移除，否则退出动画没有机会播放。

另外，动画可能被禁用或取消，实际工程中需要提供清理兜底，不能完全依赖 `animationend`。

---
## CSS 动画与浏览器渲染性能
### 浏览器渲染流程
简化模型：`Style → Layout → Paint → Composite`

|阶段|作用|
|---|---|
|Style|计算样式|
|Layout（布局）|计算元素几何尺寸和位置|
|Paint（绘制）|绘制文字、背景、边框等内容|
|Composite（合成）|将图层组合成最终画面|

不同 CSS 属性的变化，可能触发不同的渲染工作。

|属性|常见更新成本|
|---|---|
|`width`、`height`、`left`、`top`|Layout + Paint + Composite|
|`background-color`、`box-shadow`|Paint + Composite|
|`transform`、`opacity`|有机会只执行 Composite|

以上是典型情况，并不是所有浏览器或所有场景都严格如此

### transform 和 opacity
```
/* 通常涉及 Layout */
.box {
  left: 100px;
}

/* 通常不会引起普通布局重新计算 */
.box {
  transform: translateX(100px);
}
```

`transform` 改变的是元素的视觉变换效果，不会改变它在普通文档流中占据的布局空间。

浏览器可能利用合成层，对已经绘制好的内容直接进行变换，从而跳过重复的 Layout 和 Paint。

但需要注意：

- `transform` 不一定创建独立合成层。

- `transform` / `opacity` 不保证始终只执行 Composite。

- 合成层存在内存和 GPU 资源成本。

- `scale()` 只改变视觉尺寸，不会推动周围元素重新布局。


结论：位移、缩放、旋转、淡入淡出等视觉动画，优先考虑 `transform` 和 `opacity`。

---
## will-change
`will-change` 是性能提示属性，用于告诉浏览器某个属性即将变化，便于提前准备优化。
```
.box {
  will-change: transform, opacity;
}
```

它可能促使浏览器提前建立合成层或进行其他优化，但不保证一定创建合成层。

不能滥用：

- 可能增加内存消耗。

- 可能增加图层管理开销。

- 大量元素使用可能使性能下降。


工程原则：

1. 先实现动画并测试性能。

2. 确认确实存在性能问题。

3. 在验证有效后，对少量必要元素使用 `will-change`。

4. 对临时动画，可以提前添加提示，并在动画结束后移除。

---
## Web Animations API（WAAPI）
WAAPI 是浏览器原生的 JavaScript 动画 API，允许通过 `Element.animate()` 创建动画实例并控制其生命周期。
```
const animation = element.animate(
  [
    { opacity: 0, transform: "translateX(0)" },
    { opacity: 1, transform: "translateX(100px)" },
  ],
  {
    duration: 1000,
    easing: "ease-in-out",
    fill: "forwards",
  }
);
```

### Animation 对象
```
animation.play();        // 播放
animation.pause();       // 暂停
animation.reverse();     // 反向播放
animation.finish();      // 立即完成
animation.cancel();      // 取消

animation.playbackRate = 2;
animation.currentTime = 500;
```

### Promise 生命周期
```
try {
  await animation.finished;
  console.log("动画完成");
} catch {
  console.log("动画被取消");
}
```

- `finished`：动画完成时兑现的 Promise。

- 如果尚未完成的动画被 `cancel()`，`finished` 会以 `AbortError` 拒绝。


### commitStyles()
```
await animation.finished;

animation.commitStyles();
animation.cancel();
```

`commitStyles()` 将当前动画样式提交为元素的内联样式。

注意：

- `fill: forwards` 只是持续保留动画效果，不等于永久修改原始 CSS。

- `commitStyles()` 会修改 inline style。

- React 项目中应避免与 React 管理的样式状态发生冲突。

---
## 动画性能调试与可访问性
使用 Chrome DevTools 的 Performance 面板观察：

- 动画是否掉帧。

- Layout / Paint 是否过于频繁或耗时。

- 主线程是否存在长任务。

- 修改动画属性后，性能是否改善。


另外，使用 `prefers-reduced-motion` 尊重用户的减少动态效果偏好：
```
@media (prefers-reduced-motion: reduce) {
  .decorative-animation {
    animation: none;
    transition: none;
  }
}
```

对于必要的交互反馈，可以保留更温和的效果，而不是一律取消
