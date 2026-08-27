# 02 Tabs 组件库实现
> Last Format Time：8/27/2026 15:20:25

> Last Format Time：8/27/2026
> 笔记说明：从 Root、List、Trigger、Content 到焦点与选择状态，完整拆解 Tabs 组件库实现。

---
## 当前 Tabs 的整体职责划分
```text
Tabs.Root
├─ 管理 selected value
├─ controlled / uncontrolled
├─ activationMode
└─ 提供整个 Tabs 实例的 baseId

Tabs.List
├─ 收集 Trigger DOM
├─ 处理键盘事件
├─ 计算 DOM 顺序
└─ 管理 focus navigation

Tabs.Trigger
├─ 注册自身 DOM
├─ 点击切换 selected value
├─ role="tab"
├─ aria-selected
├─ tabIndex
└─ 与 Content 建立关联

Tabs.Content
├─ 根据 selected value 判断显示
├─ role="tabpanel"
└─ 与 Trigger 建立关联
```

最重要的原则：

> **Root 管状态，List 管多个 Trigger 之间的协调，Trigger 管自身行为和 DOM，Content 根据状态展示。**

---
## Collection：注册顺序不能代表 DOM 顺序
Trigger 注册：

```ts
type TriggerItem = {
  value: string;
  disabled: boolean;
  element: HTMLButtonElement;
};
```

通过：

```ts
registerTrigger(item)
```

加入 collection。

但是不能直接认为：

```ts
triggerItemsRef.current
```

的顺序就是页面上的顺序。

因为 React 中：

- 组件可能条件渲染

- 可能嵌套

- 可能 reorder

- effect 执行顺序不能作为 DOM 结构契约


因此真正进行键盘导航时，根据 DOM 排序：

```ts
items.slice().sort((a, b) => {
  const position =
    a.element.compareDocumentPosition(b.element);

  if (
    position &
    Node.DOCUMENT_POSITION_FOLLOWING
  ) {
    return -1;
  }

  if (
    position &
    Node.DOCUMENT_POSITION_PRECEDING
  ) {
    return 1;
  }

  return 0;
});
```

原则：

> **Collection 负责保存元素，DOM 决定最终视觉 / 导航顺序。**

---
## Keyboard event 的 `target` 到底是谁
假设：

```tsx
<div onKeyDown={handleKeyDown}>
  <button>Account</button>
  <button>Password</button>
</div>
```

焦点在：

```html
<button>Account</button>
```

然后用户按：

```text
ArrowRight
```

`keydown` 最开始发生在当前拥有 focus 的元素：

```text
Account button
```

然后事件冒泡到 List。

因此：

```ts
event.target
```

是：

```text
Account button
```

而：

```ts
event.currentTarget
```

是：

```text
Tabs.List 的 div
```

可以记：

```text
event.target
= 事件最初发生在哪

event.currentTarget
= 当前 handler 挂在哪
```

所以：

```ts
const currentItem = orderedItems.find(
  item => item.element === event.target
);
```

本质是在：

> 根据 keyboard event 找出当前拥有 focus 的 Trigger。

---
## 如果没有 Trigger focused 呢？
如果页面中没有具体控件获得 focus，常见情况下：

```ts
document.activeElement === document.body
```

键盘事件的 target 也可能是：

```text
body
```

如果焦点已经在 Tabs 外，例如：

```html
<input />
```

那么：

```ts
event.target === input
```

并且这个事件的冒泡路径不会经过 Tabs.List。

所以：

```tsx
<div onKeyDown={handleKeyDown}>
```

不会收到这个事件。

这也是正确行为：

> Tabs 的 Arrow 键导航只应该在焦点位于 Tabs 内部时工作。

---
## Focus 和 Selection 是两种不同状态
这是这一阶段最重要的知识点。

### Automatic Activation
方向键移动时：

```ts
nextItem.element.focus();
setValue(nextItem.value);
```

因此：

```text
focused === selected
```

例如：

```text
Account selected + focused

ArrowRight
↓

Password selected + focused
```

### Manual Activation
方向键：

```ts
nextItem.element.focus();
```

不修改：

```ts
currentValue
```

例如：

```text
Account
selected

Password
focused
```

此时：

```ts
currentValue === "account"
```

只有用户再按：

```text
Enter / Space
```

才：

```ts
setValue(currentItem.value);
```

最终 Password 成为 selected。

所以：

```text
Navigation
≠
Activation
```

---
## Manual 模式需要单独维护 roving tab stop
在 automatic 模式中，方向键移动焦点时会同时更新 selection，因此可以由：

```ts
currentValue
```

推导唯一的：

```ts
tabIndex = 0
```

但 manual 模式允许：

```text
Account selected
Password focused
```

此时 `aria-selected` 仍属于 Account，而 roving tab stop 应已经移动到 Password。因此需要单独记录最近的焦点项目，例如：

```ts
const [tabStopValue, setTabStopValue] =
  useState(currentValue)
```

方向键导航时同时执行：

```ts
setTabStopValue(nextItem.value)
nextItem.element.focus()
```

也可以直接通过 collection 命令式更新各 Trigger 的 `tabIndex`，但无论采用哪种实现，都必须保证组内只有一个 `tabIndex=0`，并让它跟随最近的组内焦点。浏览器维护真实 focus，组件维护下一次 Tab 键进入该复合控件时的入口；两者职责不同。〔CR-001〕

---
## `tabIndex` 不等于“当前是否 selected”
在 roving tabindex 模式中：

```text
aria-selected
→ 当前激活、对应面板可见的 Tab

tabIndex = 0
→ 这组 Tabs 在页面 Tab 顺序中的入口
```

automatic 模式下二者通常相同。manual 模式下可能出现：

```text
Account
selected
aria-selected = true
tabIndex = -1

Password
focused
aria-selected = false
tabIndex = 0
```

`tabIndex={-1}` 仍允许：

```ts
element.focus()
```

程序化获得焦点，但移动焦点后应同步转移组内的 `tabIndex=0`，使 roving tab stop 与最近焦点保持一致。〔CR-002〕

---
## 为什么不能简单根据 `document.activeElement` 设置 tabIndex
错误思路：

```tsx
tabIndex={
  document.activeElement === ref.current
    ? 0
    : -1
}
```

假设用户从 Tabs 移动焦点到外面的 Input：

```text
Account
Password

↓ Tab

Input focused
```

此时所有 Trigger：

```text
document.activeElement !== trigger
```

于是全部：

```text
tabIndex = -1
```

整个 Tabs 就可能从 Tab navigation 中消失。

因此：

> `document.activeElement` 只描述此刻的真实焦点；Tabs 仍需保留最近的组内 tab stop，供焦点离开后再次通过 Tab 键进入。

---
## `activationMode`
类型：

```ts
type ActivationMode =
  | "automatic"
  | "manual";
```

Root：

```tsx
<Tabs.Root
  defaultValue="account"
  activationMode="manual"
/>
```

Context：

```ts
type TabsContextValue = {
  currentValue: string;
  setValue: (next: string) => void;
  activationMode: ActivationMode;
};
```

注意这里：

```ts
activationMode?: ActivationMode
```

没必要 optional。

因为 Root 已经：

```ts
activationMode = "automatic"
```

只要 Context 存在，它就一定存在。

---
## 键盘逻辑应该按照“行为”拆分
之前的代码：

```ts
const nextItem = getNextItem(...);

if (!nextItem) return;

if (event.key === "Enter") {
  setValue(currentItem.value);
}
```

不够合理。

因为 Enter 根本不需要：

```ts
nextItem
```

应该拆成：

```text
Navigation key
→ 找 nextItem

Activation key
→ 使用 currentItem
```

例如：

```ts
const isNextKey =
  event.key === "ArrowRight";

const isActivationKey =
  event.key === "Enter" ||
  event.key === " ";
```

然后：

```ts
if (
  activationMode === "manual" &&
  isActivationKey
) {
  event.preventDefault();
  setValue(currentItem.value);
  return;
}
```

导航：

```ts
if (isNextKey) {
  event.preventDefault();

  const nextItem = getNextItem(...);

  if (!nextItem) return;

  nextItem.element.focus();

  if (activationMode === "automatic") {
    setValue(nextItem.value);
  }
}
```

最终模型：

```text
ArrowRight
│
├─ focus(next)
│
└─ automatic?
      └─ select(next)


Enter / Space
│
└─ manual?
      └─ select(current)
```

---
## `preventDefault()` 不能一上来就调用
错误：

```ts
const handleKeyDown = event => {
  event.preventDefault();

  ...
}
```

这会把所有键盘默认行为禁止掉。

例如：

```text
Tab
```

原本应该让用户离开 Tabs，但也会被阻止。

应该：

```ts
if (!isNextKey && !isActivationKey) {
  return;
}
```

只在真正接管某个按键时：

```ts
event.preventDefault();
```

原则：

> **只阻止你准备自己实现的浏览器行为。**

---
## Space 的 `event.key`
不要写：

```ts
event.key === "Space"
```

通常应该：

```ts
event.key === " "
```

也就是一个空格字符：

```ts
event.key === "Enter" ||
event.key === " "
```

---
## `id` 和 React `key` 不一样
之前容易混淆：

```text
id 重复
```

和：

```text
key 重复
```

是完全不同的问题。

### `key`
```tsx
items.map(item => (
  <Tab key={item.id} />
))
```

主要作用：

```text
React reconciliation
↓
识别兄弟组件 identity
```

一般不会出现在 DOM 中。

### `id`
```html
id="tabs-account"
```

是：

```text
DOM identity
```

用于：

- ARIA

- CSS

- `getElementById`

- selector

- fragment


同一个 document 中应该唯一。

记：

```text
key
→ React identity

id
→ DOM identity
```

---
## 为什么 `useId()` 放在 `Tabs.Root`
如果直接：

```ts
id={`tab-trigger-${value}`}
```

页面出现两套 Tabs：

```tsx
<Tabs.Root>
  <Tabs.Trigger value="account" />
</Tabs.Root>

<Tabs.Root>
  <Tabs.Trigger value="account" />
</Tabs.Root>
```

就会产生重复：

```text
tab-trigger-account
tab-trigger-account
```

因此每个 Tabs 实例需要自己的 identity：

```ts
const baseId = useId();
```

应该放在：

```tsx
Tabs.Root
```

因为它描述的是：

> 这一整套 Tabs 实例的 identity。

然后通过 Context：

```ts
type TabsContextValue = {
  baseId: string;
};
```

传给 Trigger / Content。

---
## Derived Identity
Trigger 和 Content 不需要直接相互通信。

只需要共享：

```text
baseId
+
value
+
统一生成规则
```

例如：

```ts
const triggerId =
  `${baseId}-trigger-${value}`;

const contentId =
  `${baseId}-content-${value}`;
```

Trigger：

```tsx
<button
  id={triggerId}
  aria-controls={contentId}
/>
```

Content：

```tsx
<div
  id={contentId}
  aria-labelledby={triggerId}
/>
```

这种设计可以理解为：

> **Derived Identity：通过共享数据独立推导相同的 DOM 关联。**

---
## 不要轻易把用户的 `value` 原样当 DOM id
例如：

```tsx
<Tabs.Trigger value="user profile" />
```

可能生成：

```text
xxx-trigger-user profile
```

或者：

```tsx
value="a/b?c#d"
```

某些字符放到 CSS selector 等环境中会变得麻烦。

但要注意：

```tsx
id={`${baseId}-${value}`}
```

不会因为用户输入：

```text
">
```

直接把 JSX / HTML“提前闭合”。

React 会把它当 DOM 属性值处理，并不是裸字符串拼 HTML。

真正值得注意的是：

> `value` 是业务 identity，而 DOM id 有自己的字符和 selector 使用约束，二者最好不要过度耦合。

---
## Tabs 的 ARIA 语义
### Tabs.List
```tsx
<div role="tablist">
```

表示：

> 这里是一组 Tab。

### Tabs.Trigger
应该：

```tsx
<button
  role="tab"
  aria-selected={isActive}
  id={triggerId}
  aria-controls={contentId}
  tabIndex={isTabStop ? 0 : -1}
/>
```

语义：

```text
role="tab"
→ 我是一个 Tab

aria-selected
→ 我是否被选中

aria-controls
→ 我控制哪个 TabPanel
```

在 automatic 模式下，`isTabStop` 可以和 `isActive` 同步；在 manual 模式下，`isTabStop` 必须跟随最近焦点，而 `isActive` 继续跟随 selection。〔CR-003〕

### Tabs.Content
应该：

```tsx
<div
  role="tabpanel"
  id={contentId}
  aria-labelledby={triggerId}
  hidden={!shouldShow}
>
```

注意之前写错了：

```tsx
role="tabplane"
```

正确：

```tsx
role="tabpanel"
```

关系：

```text
Trigger
aria-controls
        ↓
Content


Content
aria-labelledby
        ↓
Trigger
```

最终是双向关联：

```text
Trigger
id = trigger-account
aria-controls = content-account
        │
        ▼
Content
id = content-account
aria-labelledby = trigger-account
        │
        └──────────────→ Trigger
```

---
## `return null` 和 `hidden`
之前：

```tsx
if (!shouldShow) {
  return null;
}
```

意味着：

```text
Content unmount
```

子组件：

```tsx
<Tabs.Content>
  <ProfileForm />
</Tabs.Content>
```

切走后：

```text
ProfileForm unmount
↓
state 销毁
↓
effect cleanup
```

切回来：

```text
重新 mount
↓
state 重新初始化
↓
effect 重新执行
```


改成：

```tsx
<div hidden={!shouldShow}>
  {children}
</div>
```

意味着：

```text
组件保持 mounted
```

所以：

- 内部 state 保留

- component identity 保留

- effect 不会因为 Tab 切换而卸载


但要注意：

```text
hidden
≠ 不重新 render
```

因为：

```ts
currentValue
```

来自 Context，改变以后 Content 仍然会执行 render。

`hidden` 的核心优势不是：

> 避免 React render

而是：

> **不卸载组件，从而保留内部状态和生命周期。**

浏览器通常不会渲染带普通 `hidden` 属性的元素，因此它不参与布局；但 CSS 可以覆盖这种默认呈现。无论是否被 CSS 覆盖，React 组件仍保持 mounted，已有 effect 也不会仅因切换 `hidden` 而 cleanup。〔CR-004〕

---
## `useControllableState` 当前还有一个小问题
代码：

```ts
const wasControlledRef =
  useRef(isControlled);

useEffect(() => {
  if (
    wasControlledRef.current !==
    isControlled
  ) {
    console.warn(...);
  }
}, [isControlled]);
```

这里没有更新：

```ts
wasControlledRef.current
```

如果这个 ref 的语义是：

```text
previous isControlled
```

那么应该：

```ts
useEffect(() => {
  if (
    wasControlledRef.current !==
    isControlled
  ) {
    console.warn(
      "Component changed between controlled and uncontrolled mode."
    );
  }

  wasControlledRef.current =
    isControlled;
}, [isControlled]);
```

---
## 这一阶段最重要的整体认知
你现在的 Tabs 已经不是：

```text
点击按钮
↓
切换一个 state
```

而是多个独立系统协作：

```text
React state
│
└─ selectedValue


DOM focus
│
└─ document.activeElement / focus()


Collection
│
└─ Trigger DOM + metadata


Keyboard event
│
└─ event.target 找当前 Trigger


Roving tabindex
│
└─ 控制 Tab 键入口


Activation Mode
│
├─ automatic
└─ manual


DOM identity
│
└─ useId + value


ARIA
│
├─ tablist
├─ tab
└─ tabpanel
```

其中最值得记住的几个设计原则：

> **1. Selection 属于 React state，focus 首先属于 DOM。**

> **2. 不要为了方便重复维护两个 source of truth。**

> **3. `aria-selected` 跟随 selection；roving `tabIndex=0` 跟随最近的组内焦点。**〔CR-005〕

> **4. Keyboard navigation 和 activation 是两种行为。**

> **5. Collection 保存元素，真正顺序由 DOM 决定。**

> **6. `event.target` 让父级 List 可以通过事件冒泡判断当前是哪一个 Trigger。**

> **7. ARIA 不只是加 `role`，还需要建立组件间的语义关系。**

> **8. `hidden` 与 unmount 最大的区别在于 component state / lifecycle 是否保留。**

> **9. Root 非常适合承担“组件实例级 identity”和共享状态的所有权。**

到这里，你这一轮实际上已经把一个简单 Tabs 推进到了一个相当接近真实 Headless UI / Component Library 内部设计的模型。

---
## 内容审核变更记录
### CR-001｜事实纠错
- 日期：8/25/2026
- 位置：`Manual 模式需要单独维护 roving tab stop`
- 原内容：浏览器已经维护真实 focus，因此当前 Tabs 没有必要单独保存 `focusedValue`。
- 调整后：automatic 模式可由 selection 推导 tab stop；manual 模式需要以 state 或命令式 DOM 更新单独维护最近的 roving tab stop。
- 原因：manual 模式下 focus 与 selection 可以分离，仅依赖 selection 会让 `tabIndex=0` 留在旧的选中项。
- 依据：[WAI-ARIA APG：Managing Focus in Composites Using a Roving tabindex](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/#kbd_roving_tabindex)
### CR-002｜事实纠错
- 日期：8/25/2026
- 位置：`tabIndex 不等于“当前是否 selected”`
- 原内容：manual 模式中焦点移到 Password 后，Account 仍为 `tabIndex=0`、Password 为 `tabIndex=-1`，并称其完全合法。
- 调整后：`aria-selected` 继续跟随 Account，但 `tabIndex=0` 应转移到获得焦点的 Password。
- 原因：roving tabindex 要求移动焦点时同步更新组内唯一的 Tab 顺序入口。
- 依据：[WAI-ARIA APG：Managing Focus in Composites Using a Roving tabindex](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/#kbd_roving_tabindex)
### CR-003｜代码修正
- 日期：8/25/2026
- 位置：`Tabs 的 ARIA 语义` 中 `Tabs.Trigger`
- 原内容：`tabIndex={isActive ? 0 : -1}`
- 调整后：`tabIndex={isTabStop ? 0 : -1}`，并说明 automatic 与 manual 模式的推导差异。
- 原因：原代码把 Tab 顺序入口永久绑定到 selection，无法正确表达 manual activation。
- 依据：[WAI-ARIA APG：Tabs Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/)；[WAI-ARIA APG：Managing Focus in Composites Using a Roving tabindex](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/#kbd_roving_tabindex)
### CR-004｜事实纠错
- 日期：8/25/2026
- 位置：`return null 和 hidden`
- 原内容：`hidden` 不一定不发生 layout。
- 调整后：普通 `hidden` 元素通常不渲染且不参与布局，但 CSS 可以覆盖默认呈现；React 组件仍保持 mounted。
- 原因：原描述混淆了 HTML 的默认渲染行为与 React 组件是否卸载。
- 依据：[MDN：HTML hidden 全局属性](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/hidden)
### CR-005｜事实纠错
- 日期：8/25/2026
- 位置：`这一阶段最重要的整体认知` 第 3 条
- 原内容：`tabIndex=0` 表示 Tab navigation 的入口，不等于当前一定 focused。
- 调整后：`aria-selected` 跟随 selection，roving `tabIndex=0` 跟随最近的组内焦点。
- 原因：原总结遗漏了 manual activation 下必须分离 selection 与 roving tab stop 的约束。
- 依据：[WAI-ARIA APG：Tabs Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/)

