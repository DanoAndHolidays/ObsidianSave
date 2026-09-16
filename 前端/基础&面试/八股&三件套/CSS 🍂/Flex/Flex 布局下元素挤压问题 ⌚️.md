# Flex 布局下元素挤压问题 ⌚️
> Last Format Time：9/16/2026 19:24:50

Flex 容器空间不足时，子元素默认：
```css
flex-shrink: 1;
```

元素会自动参与压缩

---
##  `flex-shrink`：控制是否被挤压
空间不足时，这个元素不要缩小：
```css
.item {
  flex-shrink: 0;
}
```

常见场景：
```css
.avatar {
  width: 48px;
  flex-shrink: 0;
}

.content {
  flex: 1;
  min-width: 0;
}
```

适合：
- 头像不能缩小
- 图标不能缩小
- 固定宽度侧边栏
- 按钮不能被压扁

---
## `flex-basis`：控制初始基础尺寸
表示 Flex 进行空间分配之前先把这个元素看成 `200px` 宽：
```css
.item {
  flex-basis: 200px;
}
```

会影响最终的空间计算，但它不是专门解决“禁止挤压”的。

例如，空间不足的时候依旧会被挤压：
```css
.item {
  flex-basis: 200px;
  flex-shrink: 1;
}
```

---
## `flex-wrap`：空间不够就换行
默认，所有元素强制放在一行：
```css
flex-wrap: nowrap;
```

设置：
```css
flex-wrap: wrap;
```

之后，当前行放不下的元素会进入下一行，从而避免全部元素挤在一行。

---
## 左侧固定，右侧自适应
```css
.container {
  display: flex;
}

.left {
  width: 200px;
  flex-shrink: 0;
}

.right {
  flex: 1;
  min-width: 0;
}
```

其中：
```css
flex-shrink: 0;
```

保证左侧不被压缩。

```css
flex: 1;
```

让右侧占据剩余空间。

```css
min-width: 0;
```

允许右侧真正缩小，避免长文本把 Flex 容器撑开。

---
## 面试回答模板
> Flex 容器空间不足时，Flex Item 默认 `flex-shrink: 1`，所以会发生压缩。  
> 如果某个元素不希望被压缩，可以设置 `flex-shrink: 0`。  
> `flex-basis` 用来设置元素参与 Flex 布局计算时的基础尺寸；如果布局允许换行，还可以使用 `flex-wrap: wrap`，让空间不足的元素进入下一行。
