剪贴板 **Clipboard** **API** 提供了响应剪贴板命令（剪切、复制和粘贴）与异步读写系统剪贴板的能力。从权限 [Permissions API](https://developer.mozilla.org/zh-CN/docs/Web/API/Permissions_API) 获取权限之后，才能访问剪贴板内容；如果用户没有授予权限，则不允许读取或更改剪贴板内容。

该 API 被设计用来取代使用 [`document.execCommand()`](https://developer.mozilla.org/zh-CN/docs/Web/API/Document/execCommand) 的剪贴板访问方式。

通过 `Clipboard API` 可以获取剪切板中内容，但需要获取到 `clipboard-read` 的权限，以下是关于读取剪贴板内容的代码：

```javascript
// 是否能够有读取剪贴板的权限
// result.state == "granted" || result.state == "prompt"
const result = await navigator.permissions.query({ name: "clipboard-read" }) 

// 获取剪贴板内容
const text = await navigator.clipboard.readText()
```

> 注: 该方法在 `devtools` 中不生效

### 禁止复制
---
有 CSS 和 JS 两种方法禁止复制，以下任选其一或结合使用

使用 CSS 如下：
```css
user-select: none;
```

使用 JS 如下，监听 `selectstart` 事件，禁止选中。
当用户选中一片区域时，将触发 `selectstart` 事件，Selection API 将会选中一片区域。禁止选中区域即可实现页面文本不可复制。
```javascript
document.body.onselectstart = e => {    e.preventDefault();} document.body.oncopy = e => {    e.preventDefault();}
```