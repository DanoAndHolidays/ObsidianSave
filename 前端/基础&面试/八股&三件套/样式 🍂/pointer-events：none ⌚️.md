# pointer-events：none ⌚️
> Last Format Time：9/16/2026 19:24:50

[[事件冒泡、捕获与委托 ⌚️]]

元素仍然存在、仍然显示，但在鼠标 / 触摸 / Pointer 的命中测试（hit testing）中会被跳过：
```css
pointer-events: none;
```

可以理解为：
```text
鼠标
 ↓
当前元素 pointer-events: none
 ↓
跳过它
 ↓
寻找下面真正可以接收事件的元素
```

---
## 设置后的效果：点击会“穿透”
元素本身通常不能再直接成为这些 Pointer 事件的目标：
- `click`
- `mousedown`
- `mouseup`
- `mousemove`
- `pointerdown`
- `pointerup`
- hover 相关交互
- 拖拽相关交互

例如：
```css
.overlay {
  pointer-events: none;
}
```

即使 `.overlay` 视觉上盖在按钮上：
```text
overlay
   ↓ 跳过

button
   ↓
真正接收到点击
```

---
## 不等于 `disabled`
```css
button {
  pointer-events: none;
}
```

只表示鼠标无法命中这个按钮，并不代表按钮真的处于 disabled 状态。

例如键盘仍可能：
```text
Tab
 ↓
button 获得焦点

Enter
 ↓
触发按钮行为
```

---
## 不等于“阻止事件冒泡”
假设：
```html
<div class="parent">
  <button class="child">Click</button>
</div>
```

```css
.parent {
  pointer-events: none;
}

.child {
  pointer-events: auto;
}
```

如果点击 `child`：
```text
child
 ↓
parent
 ↓
document
```

事件仍然可以冒泡经过 `parent`。

`pointer-events: none` 只是让元素自己不能通过 hit testing 成为事件目标，不代表它彻底收不到任何事件。

---
## `cursor` 可能失效
例如：
```css
button {
  pointer-events: none;
  cursor: not-allowed;
}
```

`cursor: not-allowed` 可能不会显示。

原因是鼠标命中测试直接跳过了 button，实际 hover 的是下面的元素。

如果需要这种效果，可以把 cursor 放在外层：
```css
.wrapper {
  cursor: not-allowed;
}

button {
  pointer-events: none;
}
```

---
## 常见使用场景
适合：
```text
装饰层
SVG / icon
Tooltip
视觉特效层
不希望拦截点击的 absolute 元素
```


---
## 和其他 CSS 属性的区别
|属性|可见|占布局|鼠标点击|键盘交互|
|---|--:|--:|--:|--:|
|`pointer-events: none`|✅|✅|❌|可能仍然可以|
|`opacity: 0`|❌|✅|✅|✅|
|`visibility: hidden`|❌|✅|❌|❌|
|`display: none`|❌|❌|❌|❌|
|`disabled`|✅|✅|❌|具有真正的禁用语义|
