https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/align-content

https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/align-items


|属性|作用对象|控制什么|常见使用场景|
|---|---|---|---|
|`align-content`|多行 / 多轨道整体|多行之间怎么分布|`flex-wrap` 后有多行；Grid 有多行|
|`align-items`|容器内所有子项|每个子项在交叉轴上的对齐|一整排元素统一居中、顶部、底部|
|`align-self`|单个子项|覆盖自己的 `align-items`|某一个元素想单独对齐|

---
## align-items
统一控制所有子项，例如：
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

三个元素都在**交叉轴**上居中。`align-items: center` 再让每一个 ==Flex Item== 在自身所属的 Flex Line 内居中

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
## align-self
某一个元素特殊处理，假设：
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

所以它会覆盖容器给它的统一规则，当然这里说的是**对这个子项最终对齐行为的覆盖关系**，不是 CSS specificity。

---
## align-content
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

把这 **三行作为一个整体** 放到中间

`align-content: space-between` 把两条 Flex Line 分布到容器的交叉轴两端

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

所以它处理的是行之间的关系：
```text
行
行
行
```
