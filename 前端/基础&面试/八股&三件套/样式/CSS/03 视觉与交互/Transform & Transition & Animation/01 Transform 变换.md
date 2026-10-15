# Transform 变换
[[普通流 & 格式化上下文 & 包含块]]

`transform（变换）` 用于对元素进行平移、缩放、旋转、倾斜等视觉变换

![[Pasted image 20261015173322.png]]

核心特点：

- 不改变常规布局占位：元素仍然占据原来的布局空间，不会因为变换而推动兄弟元素
- 改变视觉几何：实际显示位置、尺寸或形状发生变化
- 可能产生视觉重叠，也可能扩大滚动溢出区域
- 变换会影响后代元素的定位参照，并可能创建 [[Stacking Context 层叠上下文 ⌚️]]

---
## 四种基本变换
![[Pasted image 20261015173346.png]]

|函数|作用|示例|
|---|---|---|
|`translate()`|平移|`translate(50px, 20px)`|
|`scale()`|缩放|`scale(1.5)`|
|`rotate()`|旋转|`rotate(45deg)`|
|`skew()`|倾斜|`skew(20deg, 10deg)`|

### translate（平移）
```
transform: translateX(100px);
transform: translateY(-50px);
transform: translate(100px, 50px);
```

坐标方向：X 正方向向右，Y 正方向向下。

百分比参考自身的变换参考盒，而不是父元素。 普通 HTML 盒子默认通常以自身 border box 为参考
```
.box {
  width: 200px;
  height: 100px;
  transform: translate(50%, 50%);
  /* 向右 100px，向下 50px */
}
```

经典绝对定位居中：
```
.parent {
  position: relative;
}

.child {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
```

- `left/top: 50%`：根据包含块尺寸计算。
- `translate(-50%, -50%)`：根据元素自身参考盒尺寸计算。

### scale（缩放）
```
transform: scale(1.5);     /* 放大 1.5 倍 */
transform: scale(2, 0.5);  /* X 放大两倍，Y 缩小一半 */
transform: scaleX(2);
transform: scaleY(0.5);
```

缩放不会改变原来的布局尺寸。

例如，布局宽度为 100px 的元素应用 `scale(2)`：
```
el.offsetWidth; // 100，布局宽度
el.getBoundingClientRect().width; // 200，视觉边界宽度
```

上述结果假设无其他变换及特殊影响。

### rotate（旋转）
```
transform: rotate(45deg);
transform: rotate(0.5turn); // 旋转半圈
```

默认围绕元素中心旋转。在常见的从左到右书写方向下，正角度表示顺时针旋转。

### skew（倾斜）
```
transform: skewX(20deg);
transform: skewY(15deg);
transform: skew(20deg, 10deg);
```

主要用于视觉装饰、特殊形状等场景。


---
## transform-origin（变换原点）
决定缩放、旋转等变换围绕哪个点进行
```
.box {
  transform-origin: center center; /* 默认：50% 50% */
  transform: rotate(45deg);
}
```

其他取值：
```
transform-origin: top left;
transform-origin: bottom right;
transform-origin: 20px 30px;
```

相同的变换，原点不同，最终视觉结果也可能不同。

---
## 多个 Transform 函数的顺序
```
/* A */
transform: translateX(100px) rotate(90deg);

/* B */
transform: rotate(90deg) translateX(100px);
```

两者结果不同，因为变换组合通常不满足交换律

---
## Transform 对布局和定位的影响
### 不改变布局占位
`translate`、`scale` 等不会让 Flex/Grid 根据变换后的视觉尺寸重新排列元素。

### 创建 Stacking Context
当 `transform` 不为 `none` 时，会创建新的层叠上下文
```
.parent {
  transform: translateX(0);
}
```

即使没有实际移动，也会创建层叠上下文

内部子元素的 `z-index` 无法直接突破祖先层叠上下文的限制

### 创建定位包含块
[[普通流 & 格式化上下文 & 包含块]]
非 `none` 的 Transform 会为 ==绝对定位（absolute）== 和 ==固定定位（fixed）== 的后代==建立包含块==
```
.parent {
  transform: translateZ(0);
}

.child {
  position: fixed;
  top: 0;
}
```

此时 `.child` 的定位参照可能变成 `.parent` 建立的包含块，而非视口

这是弹窗、悬浮元素常见的定位问题

---
## 现代 CSS 独立变换属性
传统写法：
```
.box {
  transform: translateX(20px) rotate(30deg) scale(1.2);
}
```

现代写法：
```
.box {
  translate: 20px 0;
  rotate: 30deg;
  scale: 1.2;
}
```

独立属性的优势是可以分别修改，避免覆盖其他变换：
```
.card {
  rotate: 5deg;
}

.card:hover {
  translate: 0 -6px;
  /* 不会覆盖 rotate */
}
```

注意：独立属性与 `transform` 共同使用时，应用顺序固定为：

`translate → rotate → scale → transform`

---
## Transform 与浏览器渲染性能
浏览器渲染流程可以简化为：
![[Pasted image 20261015174013.png]]

- 改变 `width`、`height` 等布局属性通常会触发布局。

- 改变 `transform`、`opacity` 通常更容易利用合成阶段进行动画优化。

- 不代表所有 Transform 动画都一定只触发 Composite。

- 不应该无脑使用 `translateZ(0)` 或 `will-change` 强制图层优化。

不过这不代表所有 Transform 变化都一定只触发 Composite，也不代表用了 `translateZ(0)` 就一定更快。是否能够合成优化，还受到浏览器实现、图层与渲染内容的影响

---
## 3D Transform（三维变换）
*下面的内容看看就好，不是特别重要*

CSS 3D Transform 在二维坐标系的基础上增加了 Z 轴（深度方向）

|坐标轴|正方向|作用|
|---|---|---|
|X|向右|水平方向|
|Y|向下|垂直方向|
|Z|朝向观察者|深度方向|

常见的 3D 变换：
```
/* 三维平移 */
transform: translateZ(100px);
transform: translate3d(20px, 30px, 100px);

/* 三维旋转 */
transform: rotateX(45deg); /* 绕 X 轴 */
transform: rotateY(45deg); /* 绕 Y 轴 */
transform: rotateZ(45deg); /* 绕 Z 轴 */

/* 绕指定方向向量旋转 */
transform: rotate3d(1, 1, 0, 45deg);
```

注意：`rotate3d(x, y, z, angle)` 的前三个参数用于确定旋转轴方向，并不是三个独立的旋转角度。

---
## Perspective（透视）
浏览器屏幕是二维的，CSS 通过透视投影模拟三维空间中的近大远小。

如果没有透视：
```
.box {
  transform: translateZ(100px);
}
```

元素沿 Z 轴移动，但不一定产生明显的视觉大小变化。

添加透视：
```
.scene {
  perspective: 800px;
}

.box {
  transform: translateZ(100px);
}
```

透视规律：

- `perspective` 值越小，透视效果越强。

- `perspective` 值越大，透视效果越弱。

- `perspective: none` 表示不应用该属性提供的透视投影。


### 两种透视写法

1. perspective 属性

```
.parent {
  perspective: 800px;
}

.child {
  transform: rotateY(45deg);
}
```

作用于子元素的 3D 变换，适合多个元素共享一个观察视角。

2. perspective() 函数

```
.child {
  transform: perspective(800px) rotateY(45deg);
}
```

透视作为当前元素 `transform` 变换列表的一部分。

两者作用范围不同，不完全等价

### perspective-origin（透视原点）
```
.parent {
  perspective: 800px;
  perspective-origin: 50% 50%;
}
```

决定透视投影的观察中心，影响消失点位置。

注意区分：

- `transform-origin`：元素的变换原点。
- `perspective-origin`：透视投影的观察中心。


---
## transform-style（三维空间保留）
决定元素的子元素是否保留三维空间关系
```
.parent {
  transform-style: preserve-3d;
}
```

|值|作用|
|---|---|
|`flat`|默认，将后代的 3D 内容扁平化|
|`preserve-3d`|使后代保留三维空间关系|

例如：
```
.scene {
  perspective: 800px;
}

.cube {
  transform-style: preserve-3d;
}

.front {
  transform: translateZ(50px);
}

.back {
  transform: rotateY(180deg) translateZ(50px);
}
```

可以通过多个面组合成立方体。

注意：部分属性可能强制将 `preserve-3d` 的实际使用效果变为 `flat`，例如 `opacity: 0.5`、`overflow: hidden`。

## backface-visibility（背面可见性）
决定元素背面朝向观察者时是否显示
```
.card {
  backface-visibility: visible; /* 默认 */
}

.card {
  backface-visibility: hidden;
}
```

典型场景：3D 翻转卡片
```
.scene {
  perspective: 800px;
}

.card {
  transform-style: preserve-3d;
  transition: transform 0.6s;
}

.scene:hover .card {
  transform: rotateY(180deg);
}

.front,
.back {
  backface-visibility: hidden;
}

.back {
  transform: rotateY(180deg);
}
```

原理：

1. 正面初始朝向观察者，背面预先旋转 180°。

2. 两个面都隐藏自己的背面。

3. 父级卡片旋转 180°。

4. 正面转到背后并隐藏，背面转向观察者并显示。

---
## Matrix（变换矩阵）
CSS 的平移、缩放、旋转等变换，本质上都可以使用矩阵表示和组合。
### 二维矩阵
```
transform: matrix(a, b, c, d, tx, ty);
```

对应的 3×3 齐次坐标矩阵：

例如：
```
/* 平移 */
transform: translate(100px, 50px);
transform: matrix(1, 0, 0, 1, 100, 50);

/* 缩放 */
transform: scale(2);
transform: matrix(2, 0, 0, 2, 0, 0);
```

### 三维矩阵
使用 4×4 齐次坐标矩阵表示：
```
transform: matrix3d(
  1, 0, 0, 0,
  0, 1, 0, 0,
  0, 0, 1, 0,
  0, 0, 0, 1
);
```

一般开发中不需要手写矩阵，只需理解：

- 2D Transform 可以通过 3×3 齐次矩阵表示。

- 3D Transform 可以通过 4×4 齐次矩阵表示。

- 多个变换通过矩阵乘法组合。

- 矩阵乘法通常不满足交换律，因此 Transform 的顺序很重要。

---
## 常见工程问题

1. `translateZ(0)` 不一定带来性能提升。

```
.box {
  transform: translateZ(0);
}
```

现代浏览器是否创建独立合成层取决于多种因素，不应该无脑使用。

2. Transform 不改变常规布局占位。

但会改变元素的视觉几何：
```
el.offsetWidth; // 布局宽度
el.getBoundingClientRect().width; // 变换后的视觉边界宽度
```

拖拽、碰撞检测、悬浮层定位时要区分这两种几何信息。

核心模型：

CSS 3D Transform 在 X、Y 坐标之外引入 Z 轴，通过矩阵组合进行几何变换，并利用 Perspective 将三维空间投影到二维屏幕上。

- `transform`：执行几何变换。

- `perspective`：提供近大远小的透视效果。

- `transform-style`：控制后代是否保留三维空间关系。

- `backface-visibility`：控制元素背面的可见性。

- `matrix()` / `matrix3d()`：变换的数学表示。
