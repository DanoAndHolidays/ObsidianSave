# Agent 对话输入框设计
> Last Format Time：9/16/2026 19:24:50

标准 Agent 输入框通常使用：
```html
<form>
  <textarea></textarea>
  <button type="submit">Send</button>
</form>
```

核心职责：
```text
textarea → 负责输入与键盘行为
form     → 负责统一提交
button   → 负责触发提交
```

发送逻辑只保留一份，统一放在 `form submit` 中，一个标准实现：
```tsx
function ChatInput() {
  const [value, setValue] = useState("");
  const [isSending, setIsSending] = useState(false);

  const submit = async () => {
    const message = value.trim();

    if (!message || isSending) return;

    setValue("");
    setIsSending(true);

    try {
      await sendMessage(message);
    } finally {
      setIsSending(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    submit();
  };

  const handleKeyDown = (
    e: React.KeyboardEvent<HTMLTextAreaElement>
  ) => {
    if (e.key !== "Enter") return;

    // 中文/日文等输入法正在组合文本
    if (e.nativeEvent.isComposing) {
      return;
    }

    // Shift + Enter：换行
    if (e.shiftKey) {
      return;
    }

    // Enter：阻止 textarea 默认换行
    e.preventDefault();

    // 统一触发表单提交
    e.currentTarget.form?.requestSubmit();
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="给 Agent 发送消息..."
        rows={1}
      />

      <button
        type="submit"
        disabled={!value.trim() || isSending}
      >
        发送
      </button>
    </form>
  );
}
```

---
## 键盘规则
```text
Enter          → 发送
Shift + Enter  → 换行
IME Enter      → 只确认输入法，不发送
```

典型实现：
```tsx
const handleKeyDown = (
  e: React.KeyboardEvent<HTMLTextAreaElement>
) => {
  if (e.key !== "Enter") return;

  // 中文/日文输入法正在组词
  if (e.nativeEvent.isComposing) return;

  // Shift + Enter 保留 textarea 默认换行
  if (e.shiftKey) return;

  // 阻止 Enter 默认换行
  e.preventDefault();

  e.currentTarget.form?.requestSubmit();
};
```

`isComposing` 很重要，否则中文输入法按 Enter 选词时可能误发送。

---
## 为什么使用 `requestSubmit()`
不要让 textarea 直接调用：
```tsx
sendMessage();
```

而是：
```tsx
e.currentTarget.form?.requestSubmit();
```

这样键盘发送和按钮发送都走：
```text
Enter / 点击 Send
        ↓
    form submit
        ↓
   handleSubmit
        ↓
   sendMessage()
```

避免出现两套发送逻辑。

---
## Submit
```tsx
const handleSubmit = (e: React.FormEvent) => {
  e.preventDefault();

  const message = value.trim();

  if (!message) return;

  sendMessage(message);
};
```

一般还需要防止：
```text
空字符串发送
重复发送
发送状态冲突
```

---
## 为什么用 `keydown`
Enter 的默认换行发生前需要调用：
```tsx
e.preventDefault();
```

所以更适合使用：
```tsx
onKeyDown
```

而不是 `keyup`。

---
## 不建议在整个 form 上监听 Enter
Agent 输入区域以后可能包含：
```text
textarea
附件
模型选择
工具选择
Mention
Slash Command
```

如果直接在 `form.onKeyDown` 拦截 Enter，可能误伤其他组件，推荐：
```text
textarea → 定义 Enter 行为
form     → 处理 Submit
```

---
## Textarea 自动高度
常见设计：
```text
1 行
↓
逐渐增高
↓
达到最大高度
↓
内部滚动
```

例如：
```tsx
const handleInput = (
  e: React.FormEvent<HTMLTextAreaElement>
) => {
  const el = e.currentTarget;

  el.style.height = "auto";
  el.style.height =
    Math.min(el.scrollHeight, 200) + "px";
};
```

```css
textarea {
  resize: none;
  max-height: 200px;
  overflow-y: auto;
}
```

---
## Agent 的发送状态
Agent 通常不是简单的 Send：
```text
idle       → Send
submitting → 等待
streaming  → Stop
error      → 可重试
```

生成过程中可以把 Send 替换成 Stop：
```tsx
<button type="button" onClick={stopGeneration}>
  Stop
</button>
```

注意 `Stop` 应设置：
```tsx
type="button"
```

防止误触发表单提交。

---
## 最终 Mental Model
```text
┌─────────────────────────────┐
│ textarea                    │
│                             │
│ Enter       → Submit        │
│ Shift+Enter → Newline       │
│ IME Enter   → Confirm       │
│                             │
│ Tools              Send/Stop│
└─────────────────────────────┘
              ↓
            form
              ↓
           submit
              ↓
        sendMessage()
```

核心原则：
```text
textarea 管键盘语义
form 管提交
发送逻辑只有一份
```

这版已经比较适合直接放进你的前端笔记里了。