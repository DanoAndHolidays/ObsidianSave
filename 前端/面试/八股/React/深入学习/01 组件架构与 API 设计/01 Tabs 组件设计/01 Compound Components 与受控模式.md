# 01 Compound Components 与受控模式
> Last Format Time：8/27/2026 15:20:25

> Last Format Time：8/27/2026
> 笔记说明：Compound Components、Controlled / Uncontrolled 模式，以及 Tabs 状态所有权的基础模型。

---
## 简单Tab组件
```tsx
import { useState } from "react";

type Tab = {
  value: string;
  label: string;
  content: React.ReactNode;
};

type TabsProps = {
  tabs: Tab[];
  defaultValue?: string;
};

export function Tabs({ tabs, defaultValue }: TabsProps) {
  const [value, setValue] = useState(defaultValue ?? tabs[0]?.value,);

  return (
    <div>
      <div>
        {tabs.map((tab) => (
          <button
            key={tab.value}
            onClick={() => setValue(tab.value)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div>
        {tabs.find((tab) => tab.value === value)?.content}
      </div>
    </div>
  );
}
```

原本最大的问题是，组件结构被压缩成了一个**数据结构**。

```tsx
<Tabs
  tabs={[
    {
      value: "account",
      label: "Account",
      content: <AccountPanel />,
    },
  ]}
/>
```

于是如果以后想加：
```tsx
icon
disabled
badge
tooltip
className
description
loading
```

 `Tab` 类型会越来越胖：
```tsx
type Tab = {
  value: string;
  label: ReactNode;
  content: ReactNode;
  icon?: ReactNode;
  disabled?: boolean;
  badge?: ReactNode;
  tooltip?: string;
  ...
};
```

---
## Compound Components
```tsx
<Tabs>
  <Tabs.List>
    <Tabs.Trigger value="account">
      <Icon />
      Account
      <Badge />
    </Tabs.Trigger>
  </Tabs.List>

  <Tabs.Content value="account">
    <AccountPanel />
  </Tabs.Content>
</Tabs>
```

把“配置数据”重新变成了 React 擅长的组件组合。

“从 JSX 就能看出结构”，用户可以自由决定组件之间插什么东西、怎么布局。

例如：
```tsx
<Tabs>
  <header>
    <h2>Settings</h2>

    <Tabs.List>
      ...
    </Tabs.List>
  </header>

  <div className="border" />

  <main>
    <Tabs.Content value="account" />
  </main>
</Tabs>
```

如果是数组 API，这种布局控制就会非常难。

所以 Compound Components 最大的价值不是“写起来高级”，而是==组件负责行为，使用者负责结构。==

---
## Controlled / Uncontrolled
### Uncontrolled
```tsx
<Tabs defaultValue="account" />
```

`defaultValue` 的意思是：
> **只告诉 Tabs 初始值是什么，之后 Tabs 自己管理。**

类似：
```tsx
const [internalValue, setInternalValue] =
  useState(defaultValue);
```

所以：
```text
defaultValue
↓
只参与初始化
↓
后续内部自己改
```

### Controlled
```tsx
<Tabs
  value={value}
  onValueChange={setValue}
/>
```

Tabs 自己不拥有当前状态，父组件才是真正的数据源。

因此：
```text
Parent state
     ↓
   value
     ↓
   Tabs
```

Trigger 点击：
```text
Tabs.Trigger
↓
onValueChange("security")
↓
Parent setValue
↓
Parent render
↓
value="security"
↓
Tabs 更新
```

所以 Controlled 模式的核心是：`value` 是唯一真相来源（source of truth）。〔CR-001〕

---
## 正确写法
```tsx
function Tabs({
  value,
  defaultValue,
  onValueChange,
  children,
}: TabsProps) {
  const [internalValue, setInternalValue] =
    useState(defaultValue);

  const isControlled = value !== undefined;

  const currentValue = isControlled
    ? value
    : internalValue;

  const handleValueChange = (nextValue: string) => {
    if (!isControlled) {
      setInternalValue(nextValue);
    }

    onValueChange?.(nextValue);
  };

  return (
    <TabsContext.Provider
      value={{
        value: currentValue,
        onValueChange: handleValueChange,
      }}
    >
      {children}
    </TabsContext.Provider>
  );
}
```

这个模型非常重要。

---
## Context 的性能
如果写：
```tsx
<TabsContext.Provider
  value={{
    value: currentValue,
    onValueChange: handleChange,
  }}
>
```

每次 Tabs render：
```tsx
{
  value,
  onValueChange
}
```

都是新对象。

于是所有消费这个 Context 的：
```tsx
Tabs.Trigger
Tabs.Content
```

都会认为 Context value 发生变化。

即使：
```tsx
currentValue
```

其实没变化。


可以：
```tsx
const contextValue = useMemo(
  () => ({
    value: currentValue,
    onValueChange: handleChange,
  }),
  [currentValue, handleChange],
);
```

但是还有一个问题：
```tsx
handleChange
```

自己每次 render 也是新函数。

所以可能还需要：
```tsx
const handleChange = useCallback(...);
```

这就开始进入性能设计了。

但是对于普通 Tabs：
```text
3 个 Trigger
3 个 Content
```

这种重新 render 通常根本不值得优化。

而且当：
```tsx
currentValue
```

真的改变时：
```text
account → security
```

所有 Trigger 和 Content 本来就需要知道当前 active tab 改了。

所以它们 render 很正常。

因此这里更成熟的判断是：

> **Context value identity 确实会造成额外 render，但在小型 Tabs 中通常不是实际性能问题，不应该为了“看起来优化”就立刻堆 useMemo/useCallback。**

这个和我们之前练的 memoization 思路就接上了。

---
## disabled
`disabled` 应属于 `Tabs.Trigger`，因为它与单个 Trigger 的交互行为强关联。〔CR-002〕

```tsx
<Tabs.Trigger
  value="billing"
  disabled
/>
```

Trigger 自己负责：

```tsx
<button disabled>
```

以及：

```text
不能点击
aria-disabled
样式
```

这属于 Trigger 自身行为。

但还有一个更深层的地方：

假设 Tabs 支持键盘：

```text
ArrowRight
↓
切换下一个 Tab
```

现在：

```text
Account
Billing(disabled)
Security
```

按右方向键时应该：

```text
Account
↓
跳过 Billing
↓
Security
```

这时候 Root 可能就需要知道：

```text
有哪些 Trigger
哪些 disabled
顺序是什么
```

因此复杂组件库里经常会出现：

```text
Trigger 自己拥有 disabled prop
        ↓
同时把自己的信息注册给 Root
```

所以：

> **prop 的所有权可以属于 Trigger，但 Root 仍然可能需要知道它。**

这个区别很重要。

---
## 内容审核变更记录
### CR-001｜流畅性
- 日期：8/25/2026
- 位置：`Controlled / Uncontrolled` 中 Controlled 小节
- 原内容：所以 Controlled 模式的核心是value 是唯一真相来源（source of truth）。
- 调整后：所以 Controlled 模式的核心是：`value` 是唯一真相来源（source of truth）。
- 原因：补齐标点并明确代码变量边界。
- 依据：无需外部依据（措辞调整）
### CR-002｜流畅性
- 日期：8/25/2026
- 位置：`disabled` 开头
- 原内容：你的判断：应该属于 Tabs.Trigger，因为它和 Trigger 强关联。✅ 我同意。
- 调整后：`disabled` 应属于 `Tabs.Trigger`，因为它与单个 Trigger 的交互行为强关联。
- 原因：移除对话式审批语气，使笔记可以独立阅读。
- 依据：无需外部依据（措辞调整）

