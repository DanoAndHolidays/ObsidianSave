# contenteditable属性
> Last Format Time：9/18/2026 00:43:42

#渡一

`contenteditable` 是 HTML 全局属性，可以让普通元素变成可编辑区域。

```html
<div contenteditable="true">
  这段内容可以编辑
</div>
```

---
## 常见值
`contenteditable` 是 **枚举属性（enumerated attribute）**，不是普通 boolean 属性：
```html
<div contenteditable="true">可编辑</div>
<div contenteditable="false">不可编辑</div>
<div contenteditable="plaintext-only">只允许纯文本编辑</div>
```

子元素默认会继承父元素的编辑状态：
```html
<div contenteditable="true">
  可以编辑

  <span contenteditable="false">
    这里不可编辑
  </span>
</div>
```

---
## 和 input / textarea 的区别
`input`、`textarea` 是原生表单控件，`contenteditable` 只是让普通 DOM 元素具有编辑能力

```html
<div contenteditable="true"></div>
```

它不会因为设置了 `name` 就自动参与表单提交，需要手动读取：
```js
editor.textContent
editor.innerHTML
```

---
## textContent 和 innerHTML
```js
editor.textContent
```

只获取文本内容。

```js
editor.innerHTML
```

会保留 HTML 结构和格式，富文本编辑器通常需要处理 `innerHTML`。

---
## 编辑事件
内容修改后通常监听：

```js
editor.addEventListener("input", () => {
  console.log(editor.textContent);
});
```

更底层可以监听：

```text
beforeinput
↓
浏览器修改 DOM
↓
input
```

复杂输入还需要关注：

```text
compositionstart
compositionupdate
compositionend
```

主要用于中文输入法等 IME 场景。

---
## 核心特点
用户编辑时，是**浏览器直接修改 DOM**：
```text
用户输入
↓
浏览器编辑 DOM
↓
触发 input
```

因此它比 `<textarea>` 更灵活，但也更复杂，常见场景：
- 富文本编辑器
- Notion 类编辑器
- 可编辑标题
- 聊天输入框
- 文档编辑器
![[Pasted image 20260916234742.png]]
### React 中的注意点
React 负责根据 state 管理 DOM，而 `contenteditable` 允许浏览器直接修改 DOM：
```text
React
  ↓
 DOM
  ↑
Browser
```

两者可能产生冲突，因此不要简单把它当成普通受控 `<input>` 使用：
```jsx
<div contentEditable>
  {content}
</div>
```

---
## 安全问题
如果保存：
```js
editor.innerHTML
```

并重新插入页面，需要注意 **XSS**，用户生成的 HTML 应经过清洗（sanitization）后再渲染。
