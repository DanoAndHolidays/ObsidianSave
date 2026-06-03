# 用 State 响应输入

## 📌 核心思想

React 采用**声明式**方式构建 UI，而不是像传统 DOM 操作那样使用**命令式**方式。开发者只需描述组件在不同状态下的 UI 表现，React 会自动处理如何更新界面。

### 🔁 命令式 vs 声明式

- **命令式 UI**（如原生 DOM）：
    
    - 手动控制每个元素的显示/隐藏、启用/禁用。
    - 代码复杂，容易出错，难以维护。
    - 示例：直接调用 `el.style.display = 'none'`、`button.disabled = true`。

- **声明式 UI**（React）：
    
    - 只需定义“当前状态是什么”，UI 自动匹配该状态。
    - 状态驱动视图，逻辑清晰，易于扩展和调试。

> 比喻：
> 
> - 命令式 = 坐副驾，一步步指挥司机怎么走。
> - 声明式 = 坐后排，只说“去机场”，司机自己规划路线。

## ✅ 构建响应式 UI 的 5 个步骤

#### **1. 定位组件的不同视图状态**

识别用户可能看到的所有 UI 状态，例如：

- `empty`（空输入）
- `typing`（正在输入）
- `submitting`（提交中）
- `success`（成功）
- `error`（错误）

> 建议先做“静态模拟”（Storybook 风格），用 props 控制状态，快速验证 UI。

#### **2. 确定状态变化的触发条件**

状态变化由两类输入引起：

- **人为输入**：点击、输入、导航等（需事件处理器）。
- **计算机输入**：网络响应、定时器、图片加载完成等。

画出状态转换图（状态机）有助于理清逻辑。

#### **3. 用 `useState` 表示内存中的状态**

从必要状态开始，例如：

```js
const [answer, setAnswer] = useState('');
const [error, setError] = useState(null);
const [status, setStatus] = useState('typing'); // 'typing' | 'submitting' | 'success'
```

#### **4. 删除不必要的状态变量**

避免冗余和矛盾状态：

- ❌ 不要同时用 `isEmpty` 和 `isTyping`（二者互斥）。
- ✅ 用 `answer.length === 0` 判断是否为空。
- ✅ 用单一 `status` 字段代替多个布尔值。
- ✅ 用 `error !== null` 判断是否有错误，而非单独 `isError`。

目标：**最小化、无歧义、无不可能状态**。

> 进阶：可用 `useReducer` 合并复杂状态逻辑，进一步防止无效状态。

#### **5. 连接事件处理函数**

绑定事件以更新状态：

```jsx
function handleSubmit(e) {
  e.preventDefault();
  setStatus('submitting');
  submitForm(answer)
    .then(() => setStatus('success'))
    .catch(err => {
      setError(err);
      setStatus('typing');
    });
}

function handleTextareaChange(e) {
  setAnswer(e.target.value);
}
```

表单元素受控于 state：

```jsx
<textarea
  value={answer}
  onChange={handleTextareaChange}
  disabled={status === 'submitting'}
/>
<button disabled={!answer.trim() || status === 'submitting'}>
  Submit
</button>
```

### 🧠 总结（Recap）

- 声明式编程：**描述“是什么”，而非“怎么做”**。
- 开发流程：
    1. 列出所有视觉状态；
    2. 分析状态如何变化；
    3. 用 `useState` 建模状态；
    4. 精简状态，消除冗余；
    5. 绑定事件，驱动状态更新。

### 💡 优势

- 更易维护：新增状态不会破坏现有逻辑。
- 更易测试：每个状态可独立渲染。
- 更少 bug：避免手动同步多个 UI 元素。