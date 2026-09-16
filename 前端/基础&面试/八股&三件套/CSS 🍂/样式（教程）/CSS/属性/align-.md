https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/align-content

https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/align-items

可以把这三个属性理解成：**一个管“多行整体”，一个管“一整行里的所有子项”，一个管“单独某个子项”**。

|属性|作用对象|控制什么|常见使用场景|
|---|---|---|---|
|`align-content`|多行 / 多轨道整体|多行之间怎么分布|`flex-wrap` 后有多行；Grid 有多行|
|`align-items`|容器内所有子项|每个子项在交叉轴上的对齐|一整排元素统一居中、顶部、底部|
|`align-self`|单个子项|覆盖自己的 `align-items`|某一个元素想单独对齐|

---
## `align-items`：统一控制所有子项
例如：

```css
.container {
  display: flex;
  height: 200px;

  align-items: center;
}
```

```text
┌──────────────────────────┐
│                          │
│    [A]   [B]   [C]       │
│                          │
└──────────────────────────┘
```

三个元素都在**交叉轴**上居中。

最常见场景就是：

```css
display: flex;
align-items: center;
```

例如导航栏：

```text
[logo]   首页   产品   [头像]
```

让不同高度的内容垂直居中。

---
## `align-self`：某一个元素特殊处理
假设：

```css
.container {
  display: flex;
  height: 200px;

  align-items: center;
}

.b {
  align-self: flex-end;
}
```

结果：

```text
┌──────────────────────────┐
│                          │
│    [A]         [C]       │
│          [B]             │
└──────────────────────────┘
```

A、C 继承：

```css
align-items: center;
```

但是 B 自己：

```css
align-self: flex-end;
```

所以它会覆盖容器给它的统一规则。

可以理解成：

```text
align-items
    ↓
所有孩子统一规则

align-self
    ↓
某一个孩子：“我不一样”
```

因此优先级关系可以简单记成：

```text
align-self > align-items
```

当然这里说的是**对这个子项最终对齐行为的覆盖关系**，不是 CSS specificity。


# align-
> Last Format Time：9/16/2026 19:24:50

这个最容易和 `align-items` 搞混。

关键点：

> `align-content` 控制的不是元素，而是“行”。

例如 Flex：

```css
.container {
  display: flex;
  flex-wrap: wrap;

  height: 300px;

  align-content: center;
}
```

假设元素换成了三行：

```text
[A][B][C]
[D][E][F]
[G][H]
```

`align-content: center` 控制的是：

```text
┌─────────────────────────┐
│                         │
│ [A][B][C]               │
│ [D][E][F]               │
│ [G][H]                  │
│                         │
└─────────────────────────┘
```

也就是：

> 把这 **三行作为一个整体** 放到中间。

如果：

```css
align-content: space-between;
```

就类似：

```text
┌─────────────────────────┐
│ [A][B][C]               │
│                         │
│ [D][E][F]               │
│                         │
│ [G][H]                  │
└─────────────────────────┘
```

所以它处理的是：

```text
行
行
行
```

之间的空间。


# 最关键的区别

假设有：

```text
第一行：[A] [B] [C]

第二行：[D] [E]
```

那么：

### `align-items`
关注：

```text
[A] [B] [C]
 ↑   ↑   ↑

[D] [E]
 ↑   ↑
```

也就是：

> **每一行里面，元素怎么对齐。**


### `align-self`
关注：

```text
[A] [B] [C]
     ↑
   只改 B
```

也就是：

> **某一个元素怎么对齐。**


### `align-content`
关注：

```text
[A][B][C]  ← 第一行
     ↕
[D][E]     ← 第二行
```

也就是：

> **这些行整体怎么排列。**


# 为什么 `align-content` 经常没效果？

因为它通常需要两个条件：

### ① 必须存在“多行”
例如 Flex：

```css
display: flex;
flex-wrap: wrap;
```

如果只有：

```text
[A][B][C]
```

就一行。

那么你写：

```css
align-content: space-between;
```

基本没有意义，因为：

> 只有一行，你让“行与行之间”怎么分布？


### ② 交叉轴必须还有多余空间
例如：

```css
.container {
  height: 300px;
}
```

三行内容总共只有：

```text
150px
```

那么还有：

```text
150px
```

剩余空间可以让 `align-content` 分配。

如果容器高度刚刚好：

```text
┌─────────────┐
│ 第一行       │
│ 第二行       │
│ 第三行       │
└─────────────┘
```

没有额外空间，也就看不出明显效果。


# Flex 中最好这样记

假设：

```css
.container {
  display: flex;
  flex-direction: row;
}
```

那么：

```text
                  主轴 →
┌─────────────────────────┐
│                         │
│      [A] [B] [C]        │
│                         │
└─────────────────────────┘
            ↓
          交叉轴
```

因此：

```text
justify-content
    ↓
主轴上的整体排列

align-items
    ↓
所有元素在交叉轴上的对齐

align-self
    ↓
单个元素在交叉轴上的对齐

align-content
    ↓
多行在交叉轴上的排列
```

可以浓缩成：

```text
justify-content → 一行整体怎么排

align-items   → 每个元素怎么对齐
align-self    → 某个元素怎么对齐
align-content → 多行怎么对齐
```

---
## 一句话笔记版

> **`align-items` 管所有 item，`align-self` 管单个 item，`align-content` 管多行 content。**
> 
> `align-content` 只有在存在多行/多轨道并且容器有剩余空间时才比较明显；`align-self` 会覆盖当前元素从 `align-items` 得到的对齐方式。