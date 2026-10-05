# 09 Global Attributes
> Last Format Time：10/6/2026 02:27:25

[[特性和属性（Attributes and properties）]]，这里面有一些 dataset 相关的概念
[[03 Tabs 无障碍：Roving Tabindex]]

HTML **全局属性（Global Attributes）** 可以用于大多数 HTML 元素，用来描述元素身份、状态、交互能力或内容信息。

---
## id 与 class
`id` 表示元素在当前文档中的唯一身份，同一个 `id` 不应该重复。常用于 `label for`、URL fragment、DOM 查询等。

示例：
```html
<label for="username">用户名</label>
<input id="username">
```

`class` 表示元素所属的类别，可以重复使用，一个元素也可以同时拥有多个 class。

```html
<button class="button primary large">保存</button>
```

---
## hidden
`hidden` 表示当前内容不应该被呈现。
它是布尔属性，只要属性存在就表示开启，因此 `hidden="false"` 依然是隐藏状态。

```html
<div hidden>暂时不显示</div>
```

---
## data-*
`data-*` 用于给 DOM 元素附加应用自己的简单数据：
```html
<button data-user-id="42" data-state="open">打开</button>
```

JavaScript 中通过 `dataset` 访问：
```js
button.dataset.userId // "42"
button.dataset.state  // "open"
```

命名转换：

`data-user-id` → `dataset.userId`

适合保存和当前 DOM 元素直接相关的简单状态或元数据，不适合存放大量复杂业务数据。

---
## tabindex
`tabindex` 控制元素的焦点行为。

|值|含义|
|---|---|
|`0`|可聚焦，并进入正常 Tab 顺序|
|`-1`|可通过 JS `focus()` 聚焦，但不会被 Tab 访问|
|正数|人为改变 Tab 顺序，一般避免|

```html
<div tabindex="0">可以 Tab 到这里</div>
<div tabindex="-1">只能主动 focus</div>
```

---
## Roving tabindex
常用于 Tabs、Menu 等复合组件。[[03 Tabs 无障碍：Roving Tabindex]]

整个组件中通常只有一个元素是 `tabindex="0"`，其他元素为 `-1`。

```html
<button role="tab" tabindex="-1">首页</button>
<button role="tab" tabindex="0">消息</button>
<button role="tab" tabindex="-1">设置</button>
```

Tab 键负责进入和离开组件，方向键负责组件内部焦点移动。

核心：一个 tabindex="0" + 多个 tabindex="-1"

---
## inert
`inert` 会让一个元素及其整个 DOM 子树暂时不可交互，同时退出正常焦点导航。

```html
<main inert>
  <button>保存</button>
  <input>
</main>
```

典型场景是 Modal / Dialog 打开时，让背景页面暂时不可交互。

几个容易混淆的概念：

|属性|作用|
|---|---|
|`disabled`|禁用具体支持 disabled 的控件|
|`tabindex="-1"`|单个元素退出 Tab 顺序|
|`inert`|整个 DOM 子树不可交互|
|`hidden`|内容当前不应该被呈现|

可以记成：

`hidden` → 不显示  
`inert` → 显示，但不能交互

---
## lang
`lang` 声明当前元素内容使用的语言。通常写在 `<html>` 上，并向后代继承。

```html
<html lang="zh-CN">
```

局部语言变化时可以覆盖：
```html
<span lang="en">Progressive Enhancement</span>
```

它会影响屏幕阅读器发音、翻译、拼写检查等。

---
## dir
`dir` 声明文本的书写方向。

`ltr` → 从左到右  
`rtl` → 从右到左  
`auto` → 浏览器根据内容判断

```html
<p dir="rtl">...</p>
```

`dir` 表示的是文本方向，不等于 CSS 的 `text-align`。
