假设代码是这样：

```tsx
<tr
  onClick={(event) => {
    console.log("tr 点击");
  }}
>
  <td>
    <button
      onClick={(event) => {
        console.log("button 点击");
      }}
    >
      Archive
    </button>
  </td>
</tr>
```

你点击 `button` 后，默认会发生下面这些事情。

## 1. 浏览器确定真正点击的元素

用户点击的是按钮，所以：

```ts
event.target
```

是这个 `button`。

事件路径大致是：

```text
button
  ↑
td
  ↑
tr
  ↑
tbody
  ↑
table
  ↑
body
  ↑
html
```

## 2. 先执行 button 的点击处理器

因为事件最先到达真正被点击的按钮：

```tsx
<button onClick={...}>
```

所以先打印：

```text
button 点击
```

在按钮处理器内部：

```ts
event.target        // button
event.currentTarget // button
```

这里二者相同，因为：

* `target`：真正被点击的元素；
* `currentTarget`：当前正在执行哪个元素的事件处理器。

当前正在执行按钮处理器，所以 `currentTarget` 也是按钮。

## 3. 事件继续向父元素冒泡

按钮处理器执行完以后，如果没有调用：

```ts
event.stopPropagation();
```

事件就会继续向上。

经过 `td`。如果 `td` 没有 `onClick`，就什么也不执行。

接着到达 `tr`。

## 4. 执行 tr 的点击处理器

然后执行：

```tsx
<tr onClick={...}>
```

打印：

```text
tr 点击
```

此时在 `tr` 的处理器中：

```ts
event.target        // button
event.currentTarget // tr
```

注意，虽然事件已经冒泡到了 `tr`，但是 `event.target` 不会变。

它始终记录：

> 最开始真正点击的是谁。

所以完整输出顺序是：

```text
button 点击
tr 点击
```

## 加上 `closest("button")` 后

现在行处理器这样写：

```tsx
const handleRowClick = (
  event: React.MouseEvent<HTMLTableRowElement>,
) => {
  const target = event.target as HTMLElement;

  if (target.closest("button")) {
    return;
  }

  console.log("进入详情");
};
```

点击按钮时，流程还是一样的。

### 第一步：执行按钮处理器

```text
button 点击
```

### 第二步：冒泡到 tr

`tr` 的处理器依然会执行。

进入这里：

```ts
const target = event.target as HTMLElement;
```

因为最初点击的是按钮，所以：

```ts
target === button
```

接着执行：

```ts
target.closest("button")
```

浏览器从 `target` 自己开始检查：

```text
button 本身是不是 button？
```

答案是“是”，所以直接返回这个按钮元素：

```ts
HTMLButtonElement
```

于是：

```ts
if (target.closest("button")) {
  return;
}
```

条件成立，行处理器提前结束。

因此：

```ts
console.log("进入详情");
```

不会执行。

最终效果：

```text
button 点击
tr 的处理器也进入了
但 tr 检查出点击来自 button
tr 提前 return
没有进入详情
```

## 它不是阻止了 tr 的事件

这一点最关键：

```ts
if (target.closest("button")) return;
```

并没有阻止事件冒泡。

`tr` 的事件处理器实际上已经被调用了。

只是调用之后，里面的业务逻辑主动退出：

```ts
return;
```

可以用日志验证：

```tsx
const handleRowClick = (
  event: React.MouseEvent<HTMLTableRowElement>,
) => {
  console.log("已经进入 tr 处理器");

  const target = event.target as HTMLElement;

  if (target.closest("button")) {
    console.log("点击来自按钮，取消跳转");
    return;
  }

  console.log("进入详情");
};
```

点击按钮时输出：

```text
button 点击
已经进入 tr 处理器
点击来自按钮，取消跳转
```

所以：

* `stopPropagation()`：让 `tr` 处理器根本不执行。
* `closest("button") + return`：`tr` 处理器执行，但跳过详情逻辑。

## 使用 stopPropagation 时

按钮改成：

```tsx
<button
  onClick={(event) => {
    event.stopPropagation();
    console.log("button 点击");
  }}
>
  Archive
</button>
```

点击后：

```text
button 点击
```

`tr` 的处理器不会执行。

流程是：

```text
点击 button
→ 执行 button onClick
→ stopPropagation
→ 停止向 tr 冒泡
→ tr onClick 不执行
```

## 两种方案对比

### `closest` 方案

```tsx
const handleRowClick = (
  event: React.MouseEvent<HTMLTableRowElement>,
) => {
  const target = event.target as HTMLElement;

  if (target.closest("button")) return;

  handleNavigateDetail();
};
```

实际顺序：

```text
button 处理器执行
tr 处理器执行
tr 判断点击来自 button
tr 提前 return
```

### `stopPropagation` 方案

```tsx
<button
  onClick={(event) => {
    event.stopPropagation();
    handleArchive();
  }}
>
  Archive
</button>
```

实际顺序：

```text
button 处理器执行
事件停止冒泡
tr 处理器不执行
```

## 一个完整例子

```tsx
function TableRow() {
  const handleRowClick = (
    event: React.MouseEvent<HTMLTableRowElement>,
  ) => {
    console.log("1. 进入 tr 处理器");

    const target = event.target as HTMLElement;

    console.log("2. target 是", target.tagName);
    console.log("3. currentTarget 是", event.currentTarget.tagName);

    if (target.closest("button")) {
      console.log("4. 点击来自按钮，不跳详情");
      return;
    }

    console.log("4. 进入详情");
  };

  const handleButtonClick = () => {
    console.log("0. 执行按钮操作");
  };

  return (
    <table>
      <tbody>
        <tr onClick={handleRowClick}>
          <td>项目名称</td>

          <td>
            <button onClick={handleButtonClick}>
              Archive
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  );
}
```

点击按钮时：

```text
0. 执行按钮操作
1. 进入 tr 处理器
2. target 是 BUTTON
3. currentTarget 是 TR
4. 点击来自按钮，不跳详情
```

点击普通单元格时：

```text
1. 进入 tr 处理器
2. target 是 TD
3. currentTarget 是 TR
4. 进入详情
```

所以你可以这样记：

```text
按钮先处理
↓
事件冒泡到行
↓
行通过 event.target 知道最初点的是按钮
↓
closest("button") 判断成立
↓
行主动放弃跳转
```
