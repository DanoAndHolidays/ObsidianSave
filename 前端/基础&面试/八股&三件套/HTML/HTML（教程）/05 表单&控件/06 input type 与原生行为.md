# 06 input type 与原生行为
> Last Format Time：9/16/2026 19:24:51

[[form和input]]

`input` 的 `type` 不只是决定外观，还会影响：
- 数据语义
- 浏览器原生校验
- 输入 UI
- 移动端键盘
- 表单提交行为

根据“数据是什么”选择 `type`，而不是根据“看起来像什么”选择。

---
## 常见 input type
### text
```html
<input type="text">
```

普通单行文本。不写 `type` 时，默认基本等同于 `text`。


### password
```html
<input type="password">
```

只是在 UI 上隐藏输入内容，不会加密密码。

```js
input.value
```

仍然可以拿到真实值，真正的传输安全依赖 HTTPS 等机制。

### email
```html
<input type="email">
```

表示邮箱，浏览器可以提供：
- email 格式验证
- 适合邮箱输入的移动端键盘
- 更好的自动填充支持

格式错误时可能出现：
```js
input.validity.typeMismatch === true
```

### number
```html
<input type="number">
```

表示“数值”，可以搭配：
```html
min
max
step
```

不要因为内容全是数字，就使用 `number`，手机号、验证码等本质是字符串，不是数学数值。

### tel
```html
<input type="tel">
```

表示电话号码，电话号码不应该使用：
```html
<input type="number">
```

因为：
- 可能存在前导 `0`
- 可能包含 `+`
- 本质不是用于数学运算的数值

### url
```html
<input type="url">
```

表示 URL，浏览器可以提供 URL 格式验证。

### search
表示搜索输入框，数据上和 text 类似，但提供搜索语义，浏览器也可能提供清除按钮等原生 UI。

```html
<input type="search">
```

### checkbox
```html
<input
  type="checkbox"
  name="agreement"
  value="yes"
>
```

特点：
- 可以多个同时选中
- 每个 checkbox 相互独立

提交行为非常重要：
```text
选中：
agreement=yes

未选中：
通常根本不提交该字段
```

所以：
```text
unchecked ≠ false
```

而是：
```text
unchecked → 字段通常不存在
```

如果不写 `value`：
```html
<input type="checkbox" name="agreement">
```

选中时默认 value 通常是：
```text
on
```

建议显式写 `value`。

### checked
```html
<input type="checkbox" checked>
```

表示默认选中。

```js
input.checked
```

表示当前是否选中。

### radio
```html
<input
  type="radio"
  name="gender"
  value="male"
>

<input
  type="radio"
  name="gender"
  value="female"
>
```

相同 `name` 的 radio 会组成一个 radio group，同一组通常只能选中一个。

```text
name 相同 → 互斥
name 不同 → 可以同时选中
```

提交时只提交选中的 value：
```text
gender=male
```

### date
```html
<input type="date">
```

浏览器通常提供日期选择器，提交值通常类似：
```text
2026-09-14
```

即：
```text
YYYY-MM-DD
```

可以配合：
```html
min
max
```

### time
```html
<input type="time">
```

```text
14:30
```

### datetime-local
```html
<input type="datetime-local">
```

表示：
```text
本地日期 + 本地时间
```

例如：
```text
2026-09-14T23:30
```

 `datetime-local` 本身不包含时区信息。

### file
```html
<input type="file">
```

用于让用户选择文件，限制类型：
```html
<input
  type="file"
  accept="image/*"
>
```

允许多个：
```html
<input
  type="file"
  multiple
>
```

浏览器不会允许 JS 随意读取用户电脑上的文件，必须由用户主动选择。

### hidden
```html
<input
  type="hidden"
  name="userId"
  value="123"
>
```

特点：
```text
页面不显示
但会参与表单提交
```

注意：

> hidden 只是“看不见”，不是“安全”。

用户可以通过 DevTools 修改其值，因此服务端不能信任 hidden 字段。

### submit
```html
<button type="submit">
  提交
</button>
```

触发表单提交，也可以：
```html
<input type="submit" value="提交">
```

通常更推荐 `<button>`，因为内部内容更灵活。

### reset
```html
<button type="reset">
  重置
</button>
```

恢复表单的默认值，不是简单全部清空。

### button
```html
<button type="button">
  打开弹窗
</button>
```

没有默认提交行为，表单中的普通 UI 按钮建议明确写：
```html
type="button"
```

否则 `<button>` 默认可能作为 submit。

### inputmode
`inputmode` 主要告诉移动端：

> 应该提供什么类型的虚拟键盘。

例如验证码：
```html
<input
  type="text"
  inputmode="numeric"
>
```

验证码：
```text
001234
```

本质是字符串，因此不应该用 `number`。

核心区别：

```text
type
→ 描述数据语义
→ 影响校验和浏览器行为

inputmode
→ 提示使用什么输入键盘
```
