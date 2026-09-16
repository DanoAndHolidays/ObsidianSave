# 02 Native HTML 原生
> Last Format Time：9/16/2026 19:24:51

HTML Element 不只有外观：
```text
HTML Element
├─ Semantic（语义）
└─ Native Behavior（原生行为）
```

选择元素意味着同时选择浏览器提供的：
```text
semantic 语义
keyboard 键盘行为
focus 焦点
default action 默认行为
accessibility 辅助性
```

---
##  `<a>` vs `<button>`
```text
<a href>
→ Navigation（导航）
→ 用户要去某个 destination

<button>
→ Action / Command（操作）
→ 用户要对当前界面执行某个行为
```

不要根据视觉判断。

```text
长得像按钮的导航 → 仍然是 <a>
长得像链接的操作 → 仍然是 <button>
```

---
## `<a href>` 的 Native Behavior
真正的 Link：
```text
<a href="/products">Products</a>
```

浏览器知道 destination，所以可以提供：
```text
Tab focus
Enter activate
Ctrl / Cmd + Click
Middle Click
Open in new tab
Copy link address
Browser navigation
Accessibility Link semantics
```

而：
```text
div + navigate()
```

浏览器并不知道 URL 是这个元素的 destination。

---
##  `<button>` Native Behavior
Button 天生拥有：
```text
Button semantic
Tab focus
Enter activation
Space activation
disabled
Form integration
Accessibility
```

所以不能等同，就算你加了很多额外的属性，补齐了，但也只是手搓一个残疾的button：
```text
<div onClick>
```

---
## `role="button"` ≠ `<button>`
ARIA：
```text
role="button"
```

主要改变 accessibility semantic，它不会自动获得完整：
```text
keyboard behavior
activation
disabled behavior
form behavior
```

所以Native HTML 优先于自己模拟 Native HTML。

---
## `button type`
在 form 中：
```text
<button>
```

通常意味着：
```text
<button type="submit">
```

因此非提交按钮最好明确：
```text
<button type="button">
```

否则可能导致意外提交表单。

---
## `preventDefault` vs `stopPropagation`
```text
preventDefault()
→ 阻止 Browser Default Action

stopPropagation()
→ 阻止 Event Propagation
```

它们不能修复错误的 HTML Semantic。

---
## Interactive Content
常见 Interactive Elements：
```text
<a href>
<button>
<input>
<select>
<textarea>
```

一个独立 Interaction Target 对应一个独立 Interactive Element。

不要：
```text
<a>
  <button>...</button>
</a>
```

也不要：
```text
<button>
  <a>...</a>
</button>
```

---
## Clickable Card
只有一个导航目标：
```text
<a href="/article">
  <h2>...</h2>
  <p>...</p>
</a>
```

如果 Card 内还有 Save：
```text
<article>
  <a href="/article">
    ...
  </a>

  <button type="button">
    Save
  </button>
</article>
```

应该是 sibling interactions（兄弟交互），不要嵌套。

---
## React `Link` vs `navigate()`
```text
用户点击的东西本身就是 destination
→ Link
```

例如：
```text
<Link to="/users/123">
  View User
</Link>
```

而：
```text
用户执行一个 Action
↓
Action 成功后程序导航
→ navigate()
```

例如：
```text
Login
↓
请求成功
↓
navigate('/dashboard')
```

不要根据“代码里有没有 `navigate()`”判断。
