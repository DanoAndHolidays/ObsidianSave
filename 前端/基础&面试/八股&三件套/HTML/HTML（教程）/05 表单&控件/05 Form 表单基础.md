# 05 Form 表单基础
> Last Format Time：9/16/2026 19:24:51

[[表单：事件和方法提交]]
[[form和input]]

`<form>` 不是“包住几个 input 的容器”，而是浏览器提供的一套原生表单系统：
```text
一组数据输入控件
→ 建立 form 归属
→ 维护当前值
→ 原生校验
→ submit / reset
→ 收集 Form Data
→ 执行默认提交
```

`<form>` 和 `<div>` 最大区别不是样式，而是 `<form>` 会参与浏览器的 Form System。

---
## 表单关联元素
`input`、`textarea`、`select`、`button` 等属于 form-associated elements（表单关联元素）。

常见情况：
```html
<form>
  <input name="username">
</form>
```

input 的 form owner（所属表单）就是这个 form。

但要记住：
```text
DOM 包含关系
≠
绝对等于 form 归属关系
```

后面 `form` 属性可以让控件显式关联其他 form。

一个页面可以有多个 `<form>`，但 **form 不能嵌套 form**。嵌套属于非法 HTML，浏览器 parser 可能忽略内部 `<form>` 标签并进行 error recovery，因此源码结构不一定等于最终 DOM。


---
## name 与 value
表单数据的核心是：
```text
name = 字段名 / key
value = 当前提交值
```

例如：
```html
<input name="username" value="Dano">
```

可以理解成产生：
```text
username=Dano
```

没有 `name`：
```html
<input value="Dano">
```

用户能看到值，JS 也能读取 `.value`，但通常不会进入 Form Data。

所以：
```text
用户看得到一个值
≠
这个值会参与表单提交
```

`value` 还要区分两个概念：
```html
<input value="Dano">
```

初始：
```text
default value = Dano
current value = Dano
```

用户输入 Alice：
```text
default value = Dano
current value = Alice
```

即：
```text
HTML value attribute / defaultValue
≠
当前 DOM .value
```

用户输入通常改变的是 current value，不会自动修改 default value。

---
## select 与 option
`<select>` 的数据模型：

```html
<select name="city">
  <option value="shanghai">上海</option>
</select>
```

如果上海被选中：

```text
select.name
+
selected option.value

→ city=shanghai
```

所以 `<select>` 是字段控件，`<option>` 提供候选值。

---
## button
在 form 中：
```html
<button>提交</button>
```

默认通常相当于：
```html
<button type="submit">提交</button>
```

三种重要类型：
```text
type="submit"
→ 提交所属 form

type="button"
→ 普通按钮，没有表单提交默认行为

type="reset"
→ 重置所属 form
```

React 项目高频坑：
```tsx
<form>
  <button onClick={openModal}>打开弹窗</button>
</form>
```

因为没有写 `type`：
```text
button 默认 submit
→ openModal()
→ 还可能提交 form
```

应该表达真实角色：
```tsx
<button type="button" onClick={openModal}>
```

不要依赖 `preventDefault()` 把一个 submit button 强行当普通按钮。

---
## 基础模型
Form Submission（表单提交）的基础模型：
```text
触发 submission
例如点击 submit / Enter / requestSubmit()
        ↓
Constraint Validation（约束验证）
        ↓
验证失败
→ invalid
→ 停止提交

验证通过
        ↓
submit event
        ↓
preventDefault()？
        ↓
否
→ 构造 Form Data
→ 执行浏览器默认提交
```

所以：
```text
click
≠
submit
```

click 是某个控件的事件。

submit 是 form 层级的行为。

---
## onSubmit
React 中通常应该：
```tsx
<form onSubmit={handleSubmit}>
  ...
  <button type="submit">登录</button>
</form>
```

而不是只写：
```tsx
<button onClick={handleSubmit}>
```

因为：
```text
onClick
= 监听这个按钮被激活

onSubmit
= 监听整个表单被提交
```

表单可能通过进入 submission：
```text
鼠标点击 submit
键盘激活 submit
Enter 隐式提交
requestSubmit()
```

所以业务逻辑通常应该挂在 form 的 `onSubmit`。

---
## 隐式提交
Enter 提交属于 implicit submission（隐式提交），不要简单理解成：
```text
Enter = 永远点击按钮
```

更准确是：
```text
在特定 form/control 条件下
Enter 表达“提交这个表单”的用户意图
```

如果存在默认 submit button，浏览器通常可能通过激活它完成隐式提交，因此它的 `click` handler 也可能执行。

---
## reset
例如：
```html
<input value="Dano">
```

用户输入：
```text
Alice
```

点击 reset：
```text
Alice
→ 恢复 default state
→ Dano
```

所以：
```text
reset
≠
clear

reset
=
恢复默认状态
```

---
## disabled
```html
<input
  name="userId"
  value="123"
  disabled
>
```

通常：
```text
不能正常交互
不能正常聚焦
不参与 Form Data
```

因此后端收不到：
```text
userId=123
```

这是高频项目坑。

基础区别：
```text
disabled
→ 禁用
→ 不提交

readonly
→ 不允许用户修改
→ 通常仍可聚焦、仍参与提交
```

详细规则后面再展开。

---
## Constraint Validation（约束验证）
```html
<input required>
```

为空时提交：
```text
Constraint Validation
→ invalid
→ submit event 不发生
→ React onSubmit 不执行
```

注意只表示必填：
```html
required
```

如果要检查邮箱格式，还需要之后学习的：
```html
type="email"
```

---
## novalidate
```html
<form novalidate>
```

表示：
```text
提交时跳过浏览器的交互式约束验证
```

它不等于：
```text
required 属性消失
input 没有 validity 状态

用户点击 submit
或发生 implicit submission
        ↓
interactive constraint validation
        ↓
逐个检查需要验证的 controls
        ↓
存在 invalid
├─ yes
│   ↓
│ invalid event
│ 浏览器报告错误
│ submission 停止
│ submit event 通常不会发生
│
└─ no
    ↓
    submit event
    ↓
    默认 submission
```

用了 React Hook Form、Formik、自定义 validator，也不会让原生 HTML Validation 自动消失。

---
## 阻止默认行为
SPA 中常见：
```tsx
function handleSubmit(e) {
  e.preventDefault();
}
```

`preventDefault()` 的含义是：
```text
阻止 submit event 对应的浏览器默认提交行为
```

通常也就是阻止：
```text
默认网络请求 / 页面导航
```

它不会删除：
```text
<form> 语义
form owner
name/value
Enter 行为
submit event
FormData
```

---
## React controlled input（受控输入）
```tsx
<input value={username} onChange={...}>
```

只意味着：
```text
current value 的 source of truth
=
React state
```

它仍然是原生 HTML form control。

所以：
```text
controlled input
≠
脱离 Native Form System
```

React 不会消灭：
```text
form ownership
submit
name/value
validation
disabled
FormData
keyboard behavior
```

---
## reset
React controlled input 和 reset 需要特别注意。

```tsx
const [username, setUsername] = useState("Dano");
```

用户改成：
```text
Alice
```

此时：
```text
React state = Alice
DOM current value = Alice
```

Native reset 想恢复默认状态，例如：
```text
Dano
```

但 React state 仍然是：
```text
Alice
```

React 后续 render 又可能把 input 控制回 Alice。

所以 controlled form reset 通常也需要：
```text
reset React state
```

核心冲突是：
```text
Native reset
→ 想管理 DOM default state

React controlled input
→ React state 管理 current value
```


最终建议你把这些区分记牢：
```text
form
≠
div

submit button
≠
普通 button

name
≠
value

default value
≠
current value

click
≠
submit

reset
≠
清空

disabled
≠
readonly

看得到 value
≠
会提交 value

button onClick
≠
form onSubmit

React controlled input
≠
脱离 Native Form

preventDefault
≠
关闭 Form
```

最核心的一句话可以记成：
```text
<form> 是浏览器的一套数据交互协议：

controls 属于谁
→ 当前值是什么
→ 是否有效
→ 是否提交
→ 提交哪些 name=value
→ 是否执行默认 submission
```
