# useReducer
> Last Format Time：9/16/2026 19:24:51

*这个玩意呢，几乎没有人用啊*

`useReducer` 可以理解成：**把一组相关的 state 修改逻辑集中到一个函数里管理**。

如果 `useState` 是：

> “我要直接告诉 React，新状态是什么。”

那么 `useReducer` 更像：

> “我要告诉 React，发生了什么事情；至于状态怎么变化，交给 reducer 决定。”

---
## 最基本的结构
```tsx
const [state, dispatch] = useReducer(reducer, initialState);
```

有三个核心东西：

```tsx
state
dispatch
reducer
```

它们的关系是：

```text
用户操作
   ↓
dispatch(action)
   ↓
reducer(state, action)
   ↓
返回新的 state
   ↓
组件重新渲染
```

比如：

```tsx
import { useReducer } from "react";

function reducer(state, action) {
  switch (action.type) {
    case "increment":
      return { count: state.count + 1 };

    case "decrement":
      return { count: state.count - 1 };

    default:
      return state;
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, {
    count: 0,
  });

  return (
    <>
      <p>{state.count}</p>

      <button onClick={() => dispatch({ type: "increment" })}>
        +1
      </button>

      <button onClick={() => dispatch({ type: "decrement" })}>
        -1
      </button>
    </>
  );
}
```


# 2. 这里到底发生了什么？

先看这一句：

```tsx
const [state, dispatch] = useReducer(reducer, {
  count: 0,
});
```

初始化之后：

```tsx
state = {
  count: 0
}
```

然后点击：

```tsx
dispatch({
  type: "increment",
});
```

`dispatch` 并不是直接修改 state。

它相当于告诉 React：

```text
发生了一个 increment 事件。
```

React 接下来调用：

```tsx
reducer(
  { count: 0 },
  { type: "increment" }
);
```

进入：

```tsx
case "increment":
  return {
    count: state.count + 1,
  };
```

得到：

```tsx
{
  count: 1
}
```

React 保存这个新 state，然后触发组件重新渲染。

所以最关键的一句话是：

> `dispatch` 描述“发生了什么”，`reducer` 决定“状态怎么变”。


# 3. reducer 是什么

Reducer 本质就是一个普通函数：

```tsx
function reducer(state, action) {
  return newState;
}
```

输入：

```text
旧 state
+
action
```

输出：

```text
新 state
```

即：

```text
(state, action) => newState
```

例如：

```tsx
function reducer(state, action) {
  if (action.type === "increment") {
    return {
      count: state.count + 1,
    };
  }

  return state;
}
```

它本身并不是什么 React 特有的神奇东西。

就是一个：

**旧状态 → 根据事件计算 → 新状态**

的函数。


# 4. action 又是什么？

`action` 就是你传给 `dispatch()` 的东西。

例如：

```tsx
dispatch({
  type: "increment",
});
```

这里：

```tsx
{
  type: "increment"
}
```

就是 action。

一般约定写成：

```tsx
{
  type: "xxx",
  ...
}
```

但其实 React 并不强制。

甚至你写：

```tsx
dispatch("increment");
```

也可以：

```tsx
function reducer(state, action) {
  if (action === "increment") {
    return {
      count: state.count + 1,
    };
  }

  return state;
}
```

只是项目里通常采用：

```tsx
{
  type: "xxx"
}
```

因为以后方便携带数据。


# 5. action 携带数据

比如一个计数器，不只是 `+1`，而是：

```text
+5
+10
+100
```

可以：

```tsx
dispatch({
  type: "increment",
  payload: 5,
});
```

reducer：

```tsx
function reducer(state, action) {
  switch (action.type) {
    case "increment":
      return {
        count: state.count + action.payload,
      };

    default:
      return state;
  }
}
```

于是：

```tsx
dispatch({
  type: "increment",
  payload: 5,
});
```

相当于：

```text
发生了 increment
增加值为 5
```

最终：

```tsx
count + 5
```


# 6. `useReducer` 真正适合的地方

单纯：

```tsx
const [count, setCount] = useState(0);
```

你完全没必要换 `useReducer`。

`useReducer` 更适合这种状态：

```tsx
const [form, setForm] = useState({
  username: "",
  password: "",
  loading: false,
  error: null,
  success: false,
});
```

然后你可能开始出现：

```tsx
setForm(...);
setForm(...);
setForm(...);
```

各种地方都在修改它。

例如登录流程：

```text
开始登录
    ↓
loading = true
error = null

登录成功
    ↓
loading = false
success = true

登录失败
    ↓
loading = false
error = xxx
```

这时候 `useReducer` 就很舒服。


# 7. 一个更实际的例子

```tsx
type State = {
  username: string;
  loading: boolean;
  error: string | null;
};

const initialState: State = {
  username: "",
  loading: false,
  error: null,
};
```

Reducer：

```tsx
function reducer(state: State, action) {
  switch (action.type) {
    case "username_change":
      return {
        ...state,
        username: action.value,
      };

    case "login_start":
      return {
        ...state,
        loading: true,
        error: null,
      };

    case "login_success":
      return {
        ...state,
        loading: false,
      };

    case "login_error":
      return {
        ...state,
        loading: false,
        error: action.error,
      };

    default:
      return state;
  }
}
```

组件：

```tsx
function Login() {
  const [state, dispatch] = useReducer(
    reducer,
    initialState
  );

  const handleLogin = async () => {
    dispatch({
      type: "login_start",
    });

    try {
      await login(state.username);

      dispatch({
        type: "login_success",
      });
    } catch {
      dispatch({
        type: "login_error",
        error: "登录失败",
      });
    }
  };

  return (
    <>
      <input
        value={state.username}
        onChange={(e) =>
          dispatch({
            type: "username_change",
            value: e.target.value,
          })
        }
      />

      <button onClick={handleLogin}>
        {state.loading ? "登录中..." : "登录"}
      </button>

      {state.error && <p>{state.error}</p>}
    </>
  );
}
```

你会发现组件里不再大量写：

```tsx
setState(prev => ({
  ...
}));
```

而是变成：

```tsx
dispatch({
  type: "login_start",
});
```

从语义上特别清楚：

```text
发生了什么？
→ 开始登录了
```

至于：

```text
loading 应该改成什么？
error 应该改成什么？
```

组件不用管，全部交给 reducer。


# 8. `useState` 和 `useReducer` 最大区别

比如：

```tsx
setUser({
  ...user,
  loading: true,
  error: null,
});
```

这是在描述：

> 状态怎么修改。

而：

```tsx
dispatch({
  type: "login_start",
});
```

描述的是：

> 发生了什么事情。

这其实是 `useReducer` 最大的设计价值。

```text
useState

事件
 ↓
直接计算新状态
 ↓
setState(newState)
```

而：

```text
useReducer

事件
 ↓
dispatch(action)
 ↓
reducer
 ↓
统一计算新状态
```


# 9. 为什么叫 Reducer？

你如果学过：

```tsx
array.reduce()
```

会发现它俩思想几乎一样。

例如：

```tsx
const result = array.reduce(
  (state, item) => {
    return newState;
  },
  initialState
);
```

Reducer 的核心模式就是：

```text
旧值 + 输入
      ↓
    新值
```

React reducer：

```tsx
(state, action) => newState
```

数组 reduce：

```tsx
(accumulator, currentValue) => newAccumulator
```

其实是一类东西。


# 10. reducer 有个很重要的要求：纯函数

不要这么写：

```tsx
function reducer(state, action) {
  state.count++;

  return state;
}
```

因为你直接修改了原对象。

应该：

```tsx
function reducer(state, action) {
  return {
    ...state,
    count: state.count + 1,
  };
}
```

也就是：

```text
旧 state

{ count: 0 }
     │
     │ 不修改它
     ↓

创建新对象

{ count: 1 }
```

这一点和你之前接触的 React **不可变更新** 是完全一致的。


# 11. TypeScript 里推荐这么写

这是前端项目里比较常见的一种写法：

```tsx
type State = {
  count: number;
};

type Action =
  | {
      type: "increment";
      value: number;
    }
  | {
      type: "decrement";
      value: number;
    }
  | {
      type: "reset";
    };

function reducer(
  state: State,
  action: Action
): State {
  switch (action.type) {
    case "increment":
      return {
        count: state.count + action.value,
      };

    case "decrement":
      return {
        count: state.count - action.value,
      };

    case "reset":
      return {
        count: 0,
      };
  }
}
```

这时候 TypeScript 很聪明。

进入：

```tsx
case "increment":
```

以后，它知道：

```tsx
action
```

一定是：

```tsx
{
  type: "increment";
  value: number;
}
```

所以：

```tsx
action.value
```

自动有类型。

这是 TS 的**可辨识联合类型 Discriminated Union**。


# 12. `useReducer` 还有第三个参数

完整签名可以写成：

```tsx
useReducer(
  reducer,
  initialArg,
  init
);
```

例如：

```tsx
const [state, dispatch] = useReducer(
  reducer,
  10,
  (initialCount) => ({
    count: initialCount,
  })
);
```

最终初始化：

```tsx
state = {
  count: 10,
};
```

这里第三个参数：

```tsx
init
```

是一个**惰性初始化函数**。

适合初始化 state 比较复杂的时候。

大部分时候你只需要：

```tsx
useReducer(reducer, initialState);
```

就够了。


# 13. 什么时候该用 `useReducer`

你可以先记一个非常实用的判断：

**简单独立状态 → `useState`**

```tsx
const [open, setOpen] = useState(false);
```

```tsx
const [name, setName] = useState("");
```

**多个状态彼此有关，修改规则比较多 → `useReducer`**

例如：

```text
表单状态
复杂弹窗
拖拽编辑器
购物车
页面筛选器
状态机
多步骤流程
```

尤其当你发现代码里开始大量出现：

```tsx
setState(prev => ({
  ...prev,
  xxx: ...
}));
```

并且不同事件要同时修改多个字段：

```tsx
loading
error
data
status
selectedId
```

通常就可以考虑 `useReducer`。

---
## 最后把它压缩成一个模型
你只要记住这四个东西：

```tsx
const [state, dispatch] =
  useReducer(reducer, initialState);
```

然后：

```tsx
dispatch({
  type: "发生了什么",
});
```

交给：

```tsx
function reducer(state, action) {
  // 根据“发生了什么”
  // 决定状态怎么变化

  return newState;
}
```

整个过程：

```text
           dispatch
              │
              ▼
用户操作 ──> action
              │
              ▼
      reducer(state, action)
              │
              ▼
          newState
              │
              ▼
          React 重渲染
```

所以从设计思想上看，`useReducer` 并不是一个“更高级的 useState”，而是**把「事件」和「状态变化规则」分离开来**。这才是理解 `useReducer` 最重要的一点。
