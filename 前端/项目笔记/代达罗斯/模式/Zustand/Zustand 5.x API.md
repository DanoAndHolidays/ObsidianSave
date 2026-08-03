# Zustand 5.x API
下面用一套完整的 Todo 项目，把 Zustand 从基础讲到实际项目用法。示例基于当前 Zustand 5.x API；截至 2026 年 7 月，npm 上的最新版本是 5.0.14。([NPM][1])

---

# 一、Zustand 到底解决什么问题

React 本身已经有：

```tsx
useState()
useReducer()
useContext()
```

但当状态需要跨多个组件共享时，经常出现：

```text
App
├── Header：显示用户信息
├── Sidebar：修改用户信息
└── Content
    └── UserPanel：也需要用户信息
```

使用 `useState` 时，状态通常要放到公共父组件，再通过 props 一层层传递：

```tsx
<App user={user}>
  <Header user={user} />
  <Content user={user}>
    <UserPanel user={user} />
  </Content>
</App>
```

这就是常说的 props drilling。

Zustand 的思路是，在 React 组件树之外创建一个 Store：

```text
组件 A ──读取──┐
组件 B ──修改──┼── Zustand Store
组件 C ──读取──┘
```

组件可以直接订阅 Store 中自己需要的部分，不要求在顶层包一层 Provider。`create` 返回的既是 React Hook，也附带了 `getState`、`setState`、`subscribe` 等 Store API。([Zustand 文档][2])

---

# 二、安装 Zustand

```bash
npm install zustand
```

或者：

```bash
pnpm add zustand
```

```bash
yarn add zustand
```

---

# 三、第一个 Zustand Store

先做一个计数器。

## 1. 创建 Store

新建：

```text
src/
└── stores/
    └── counter-store.ts
```

```ts
import { create } from "zustand";

interface CounterStore {
  count: number;
  increment: () => void;
  decrement: () => void;
  reset: () => void;
}

export const useCounterStore = create<CounterStore>()((set) => ({
  count: 0,

  increment: () => {
    set((state) => ({
      count: state.count + 1,
    }));
  },

  decrement: () => {
    set((state) => ({
      count: state.count - 1,
    }));
  },

  reset: () => {
    set({
      count: 0,
    });
  },
}));
```

## 2. 在组件中使用

```tsx
import { useCounterStore } from "@/stores/counter-store";

export function Counter() {
  const count = useCounterStore((state) => state.count);
  const increment = useCounterStore((state) => state.increment);
  const decrement = useCounterStore((state) => state.decrement);
  const reset = useCounterStore((state) => state.reset);

  return (
    <div>
      <p>当前数量：{count}</p>

      <button onClick={decrement}>-1</button>
      <button onClick={increment}>+1</button>
      <button onClick={reset}>重置</button>
    </div>
  );
}
```

这里最重要的代码是：

```ts
const count = useCounterStore((state) => state.count);
```

括号里的函数叫做 **selector，选择器**。

它的意思不是“获取整个 Store”，而是：

> 我只订阅 Store 中的 `count`。

当 `count` 变化时，组件重新渲染；其他状态变化时，这个组件通常不需要重新渲染。

---

# 四、理解 create、set 和 get

一个典型 Store 长这样：

```ts
const useStore = create<Store>()((set, get) => ({
  // 状态
  count: 0,

  // 操作状态的方法
  increment: () => {
    set((state) => ({
      count: state.count + 1,
    }));
  },
}));
```

拆开理解：

```ts
create<Store>()((set, get) => {
  return {
    // Store 的内容
  };
});
```

## 1. `create<Store>()`

用于创建 Store。

泛型 `Store` 描述 Store 的完整类型：

```ts
interface Store {
  count: number;
  increment: () => void;
}
```

Store 中既可以放数据，也可以放函数。

```ts
{
  count: 0,             // state
  increment: () => {},  // action
}
```

通常称为：

```text
state：状态数据
action：修改状态的方法
```

---

## 2. `set`

`set` 用于更新 Store。

### 直接更新

```ts
set({
  count: 10,
});
```

Zustand 的 `set` 默认对第一层对象进行合并，而不是替换整个 Store。([Zustand 文档][3])

假设当前 Store 是：

```ts
{
  count: 0,
  name: "Dano",
}
```

执行：

```ts
set({
  count: 10,
});
```

结果是：

```ts
{
  count: 10,
  name: "Dano",
}
```

`name` 不会消失。

### 根据旧状态更新

当新状态依赖旧状态时，要使用函数写法：

```ts
set((state) => ({
  count: state.count + 1,
}));
```

不要这样写：

```ts
set({
  count: get().count + 1,
});
```

虽然很多情况下也能工作，但函数更新能更清楚地表达“新状态依赖旧状态”，连续更新时也更加稳妥。

---

## 3. `get`

`get` 用于在 action 内读取当前 Store。

```ts
interface CounterStore {
  count: number;
  doubleCount: () => number;
}

export const useCounterStore = create<CounterStore>()((set, get) => ({
  count: 0,

  doubleCount: () => {
    return get().count * 2;
  },
}));
```

也可以用于一个 action 调用另一个 action：

```ts
interface CounterStore {
  count: number;
  increment: () => void;
  incrementTwice: () => void;
}

export const useCounterStore = create<CounterStore>()((set, get) => ({
  count: 0,

  increment: () => {
    set((state) => ({
      count: state.count + 1,
    }));
  },

  incrementTwice: () => {
    get().increment();
    get().increment();
  },
}));
```

不过，不要滥用 `get()`。简单状态计算通常直接放在一次 `set` 中更容易理解：

```ts
incrementTwice: () => {
  set((state) => ({
    count: state.count + 2,
  }));
},
```

---

# 五、Selector：Zustand 最重要的使用习惯

假设有一个用户 Store：

```ts
interface UserStore {
  name: string;
  age: number;
  theme: "light" | "dark";
  setName: (name: string) => void;
}
```

## 不推荐：订阅整个 Store

```tsx
const store = useUserStore();
```

此时组件使用了整个 Store：

```tsx
function UserName() {
  const store = useUserStore();

  return <div>{store.name}</div>;
}
```

即使只用到 `name`，`age` 或 `theme` 变化时，这个组件也可能跟着重新渲染。

## 推荐：精确订阅

```tsx
function UserName() {
  const name = useUserStore((state) => state.name);

  return <div>{name}</div>;
}
```

动作也通过 selector 获取：

```tsx
const setName = useUserStore((state) => state.setName);
```

官方文档同样推荐通过 selector 读取 Store 的属性和 action。([Zustand 文档][4])

---

# 六、一次读取多个状态

你可能想这样写：

```tsx
const { name, age } = useUserStore((state) => ({
  name: state.name,
  age: state.age,
}));
```

但这个 selector 每次都会创建一个新对象：

```ts
{
  name: state.name,
  age: state.age,
}
```

Zustand 默认通过 `Object.is` 比较 selector 的新旧结果。在 Zustand 5 中，不稳定的对象 selector 甚至可能导致无限更新问题。([Zustand 文档][5])

## 方案一：分别订阅，最推荐

```tsx
const name = useUserStore((state) => state.name);
const age = useUserStore((state) => state.age);
```

这种写法最直观。

## 方案二：使用 `useShallow`

```tsx
import { useShallow } from "zustand/react/shallow";

const { name, age } = useUserStore(
  useShallow((state) => ({
    name: state.name,
    age: state.age,
  })),
);
```

`useShallow` 会对对象的第一层属性进行浅比较。

只要：

```ts
oldResult.name === newResult.name
oldResult.age === newResult.age
```

组件就不会因为外层对象是新对象而重新渲染。

数组选择也可能需要 `useShallow`：

```tsx
const userNames = useUserStore(
  useShallow((state) => state.users.map((user) => user.name)),
);
```

---

# 七、更新不同类型的状态

## 1. 更新基本类型

```ts
interface AppStore {
  loading: boolean;
  keyword: string;
  page: number;

  setLoading: (loading: boolean) => void;
  setKeyword: (keyword: string) => void;
  nextPage: () => void;
}

export const useAppStore = create<AppStore>()((set) => ({
  loading: false,
  keyword: "",
  page: 1,

  setLoading: (loading) => {
    set({ loading });
  },

  setKeyword: (keyword) => {
    set({ keyword });
  },

  nextPage: () => {
    set((state) => ({
      page: state.page + 1,
    }));
  },
}));
```

---

## 2. 更新对象

```ts
interface User {
  name: string;
  age: number;
}

interface UserStore {
  user: User;
  updateName: (name: string) => void;
}

export const useUserStore = create<UserStore>()((set) => ({
  user: {
    name: "Dano",
    age: 24,
  },

  updateName: (name) => {
    set((state) => ({
      user: {
        ...state.user,
        name,
      },
    }));
  },
}));
```

为什么要展开：

```ts
user: {
  ...state.user,
  name,
}
```

因为 Zustand 的 `set` 只会自动合并 Store 的第一层，不会递归合并嵌套对象。([Zustand 文档][6])

错误写法：

```ts
set({
  user: {
    name: "新的名字",
  },
});
```

这会直接替换原来的 `user`，导致 `age` 丢失。

---

## 3. 更新数组

```ts
interface Todo {
  id: string;
  title: string;
  completed: boolean;
}

interface TodoStore {
  todos: Todo[];
  addTodo: (title: string) => void;
  removeTodo: (id: string) => void;
  toggleTodo: (id: string) => void;
}

export const useTodoStore = create<TodoStore>()((set) => ({
  todos: [],

  addTodo: (title) => {
    const todo: Todo = {
      id: crypto.randomUUID(),
      title,
      completed: false,
    };

    set((state) => ({
      todos: [...state.todos, todo],
    }));
  },

  removeTodo: (id) => {
    set((state) => ({
      todos: state.todos.filter((todo) => todo.id !== id),
    }));
  },

  toggleTodo: (id) => {
    set((state) => ({
      todos: state.todos.map((todo) =>
        todo.id === id
          ? {
              ...todo,
              completed: !todo.completed,
            }
          : todo,
      ),
    }));
  },
}));
```

不要直接修改旧数组：

```ts
// 不推荐
state.todos.push(todo);
return { todos: state.todos };
```

应该创建新数组：

```ts
todos: [...state.todos, todo];
```

---

## 4. Map 和 Set

更新 `Map`、`Set` 时也应该创建新实例：

```ts
set((state) => {
  const selectedIds = new Set(state.selectedIds);
  selectedIds.add(id);

  return {
    selectedIds,
  };
});
```

或者：

```ts
set((state) => ({
  selectedIds: new Set(state.selectedIds).add(id),
}));
```

官方文档明确要求更新 `Map` 和 `Set` 时创建新实例，否则引用没有变化，订阅组件可能无法察觉更新。([Zustand 文档][7])

---

# 八、完整 Todo 项目

下面做一个更接近真实项目的 Store。

## 1. 定义类型

```ts
import { create } from "zustand";

export type TodoFilter = "all" | "active" | "completed";

export interface Todo {
  id: string;
  title: string;
  completed: boolean;
  createdAt: number;
}

interface TodoState {
  todos: Todo[];
  filter: TodoFilter;
}

interface TodoActions {
  addTodo: (title: string) => void;
  removeTodo: (id: string) => void;
  toggleTodo: (id: string) => void;
  updateTodoTitle: (id: string, title: string) => void;
  clearCompleted: () => void;
  setFilter: (filter: TodoFilter) => void;
  reset: () => void;
}

type TodoStore = TodoState & TodoActions;
```

将 state 和 actions 分开定义，后期维护会比较清晰。

---

## 2. 实现 Store

```ts
const initialState: TodoState = {
  todos: [],
  filter: "all",
};

export const useTodoStore = create<TodoStore>()((set) => ({
  ...initialState,

  addTodo: (title) => {
    const normalizedTitle = title.trim();

    if (!normalizedTitle) {
      return;
    }

    const newTodo: Todo = {
      id: crypto.randomUUID(),
      title: normalizedTitle,
      completed: false,
      createdAt: Date.now(),
    };

    set((state) => ({
      todos: [...state.todos, newTodo],
    }));
  },

  removeTodo: (id) => {
    set((state) => ({
      todos: state.todos.filter((todo) => todo.id !== id),
    }));
  },

  toggleTodo: (id) => {
    set((state) => ({
      todos: state.todos.map((todo) =>
        todo.id === id
          ? {
              ...todo,
              completed: !todo.completed,
            }
          : todo,
      ),
    }));
  },

  updateTodoTitle: (id, title) => {
    const normalizedTitle = title.trim();

    if (!normalizedTitle) {
      return;
    }

    set((state) => ({
      todos: state.todos.map((todo) =>
        todo.id === id
          ? {
              ...todo,
              title: normalizedTitle,
            }
          : todo,
      ),
    }));
  },

  clearCompleted: () => {
    set((state) => ({
      todos: state.todos.filter((todo) => !todo.completed),
    }));
  },

  setFilter: (filter) => {
    set({ filter });
  },

  reset: () => {
    set(initialState);
  },
}));
```

---

## 3. 新增 Todo 组件

```tsx
import { useState, type FormEvent } from "react";
import { useTodoStore } from "@/stores/todo-store";

export function TodoForm() {
  const [title, setTitle] = useState("");

  const addTodo = useTodoStore((state) => state.addTodo);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    addTodo(title);
    setTitle("");
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={title}
        onChange={(event) => setTitle(event.target.value)}
        placeholder="输入待办事项"
      />

      <button type="submit">新增</button>
    </form>
  );
}
```

这里体现了一个重要原则：

```text
输入框当前内容：组件局部状态 useState
待办事项列表：全局状态 Zustand
```

不需要把所有状态都塞进 Zustand。

输入框的临时内容只属于 `TodoForm`，使用 `useState` 更合理。

---

## 4. Todo 列表

```tsx
import { useTodoStore } from "@/stores/todo-store";

export function TodoList() {
  const todos = useTodoStore((state) => state.todos);
  const filter = useTodoStore((state) => state.filter);
  const toggleTodo = useTodoStore((state) => state.toggleTodo);
  const removeTodo = useTodoStore((state) => state.removeTodo);

  const visibleTodos = todos.filter((todo) => {
    switch (filter) {
      case "active":
        return !todo.completed;

      case "completed":
        return todo.completed;

      case "all":
      default:
        return true;
    }
  });

  if (visibleTodos.length === 0) {
    return <p>暂无待办事项</p>;
  }

  return (
    <ul>
      {visibleTodos.map((todo) => (
        <li key={todo.id}>
          <label>
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => toggleTodo(todo.id)}
            />

            <span
              style={{
                textDecoration: todo.completed ? "line-through" : "none",
              }}
            >
              {todo.title}
            </span>
          </label>

          <button onClick={() => removeTodo(todo.id)}>删除</button>
        </li>
      ))}
    </ul>
  );
}
```

`visibleTodos` 是根据 `todos` 和 `filter` 推导出来的数据，一般没有必要单独存进 Store。

不推荐：

```ts
interface TodoStore {
  todos: Todo[];
  filter: TodoFilter;
  visibleTodos: Todo[];
}
```

因为会形成重复数据：

```text
todos 变化了
↓
还必须记得同步 visibleTodos
```

推荐只保存最原始的状态：

```text
todos
filter
```

然后在使用时推导：

```ts
const visibleTodos = todos.filter(...);
```

---

## 5. 筛选组件

```tsx
import {
  useTodoStore,
  type TodoFilter,
} from "@/stores/todo-store";

const filters: Array<{
  label: string;
  value: TodoFilter;
}> = [
  { label: "全部", value: "all" },
  { label: "未完成", value: "active" },
  { label: "已完成", value: "completed" },
];

export function TodoFilters() {
  const currentFilter = useTodoStore((state) => state.filter);
  const setFilter = useTodoStore((state) => state.setFilter);

  return (
    <div>
      {filters.map((filter) => (
        <button
          key={filter.value}
          disabled={filter.value === currentFilter}
          onClick={() => setFilter(filter.value)}
        >
          {filter.label}
        </button>
      ))}
    </div>
  );
}
```

---

## 6. 统计信息

```tsx
import { useTodoStore } from "@/stores/todo-store";

export function TodoStatistics() {
  const total = useTodoStore((state) => state.todos.length);

  const completedCount = useTodoStore(
    (state) => state.todos.filter((todo) => todo.completed).length,
  );

  return (
    <p>
      总计 {total} 项，已完成 {completedCount} 项
    </p>
  );
}
```

selector 不一定只能读取字段：

```ts
state.todos
```

也可以返回计算结果：

```ts
state.todos.filter((todo) => todo.completed).length
```

只要 selector 返回的是稳定的基本类型，就很好处理。

---

# 九、异步请求

Zustand 的 action 可以直接写成异步函数。([Zustand 文档][8])

```ts
import { create } from "zustand";

interface User {
  id: number;
  name: string;
  email: string;
}

interface UserStore {
  users: User[];
  loading: boolean;
  error: string | null;

  fetchUsers: () => Promise<void>;
}

export const useUserStore = create<UserStore>()((set) => ({
  users: [],
  loading: false,
  error: null,

  fetchUsers: async () => {
    set({
      loading: true,
      error: null,
    });

    try {
      const response = await fetch("/api/users");

      if (!response.ok) {
        throw new Error(`请求失败：${response.status}`);
      }

      const users: User[] = await response.json();

      set({
        users,
        loading: false,
      });
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "未知错误";

      set({
        loading: false,
        error: message,
      });
    }
  },
}));
```

组件中调用：

```tsx
import { useEffect } from "react";
import { useUserStore } from "@/stores/user-store";

export function UserList() {
  const users = useUserStore((state) => state.users);
  const loading = useUserStore((state) => state.loading);
  const error = useUserStore((state) => state.error);
  const fetchUsers = useUserStore((state) => state.fetchUsers);

  useEffect(() => {
    void fetchUsers();
  }, [fetchUsers]);

  if (loading) {
    return <div>加载中……</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

## Zustand 能请求接口，不代表所有请求都该用它

对于真正的服务端状态，更推荐使用 TanStack Query：

```text
用户列表、分页数据、接口缓存
→ TanStack Query

弹窗开关、当前选中项、客户端草稿
→ Zustand
```

因为服务端数据通常还涉及：

```text
缓存
重新请求
失效处理
请求去重
分页
乐观更新
```

这些不是 Zustand 的核心职责。

---

# 十、持久化 persist

假设用户刷新网页后，Todo 不应该消失，就可以使用 `persist` 中间件。

`persist` 可以把状态写入 `localStorage`，也支持其他同步或异步存储。([Zustand 文档][9])

```ts
import { create } from "zustand";
import { persist } from "zustand/middleware";

interface SettingsStore {
  theme: "light" | "dark";
  language: "zh-CN" | "en-US";

  setTheme: (theme: "light" | "dark") => void;
  setLanguage: (language: "zh-CN" | "en-US") => void;
}

export const useSettingsStore = create<SettingsStore>()(
  persist(
    (set) => ({
      theme: "light",
      language: "zh-CN",

      setTheme: (theme) => {
        set({ theme });
      },

      setLanguage: (language) => {
        set({ language });
      },
    }),
    {
      name: "settings-store",
    },
  ),
);
```

浏览器中会产生类似：

```text
localStorage
└── settings-store
```

刷新页面后，Zustand 会从存储中恢复数据，这个过程叫 hydration。

---

## 只持久化部分状态

假设 Store 中还有：

```ts
{
  theme: "dark",
  language: "zh-CN",
  sidebarOpen: true,
}
```

我们只想保存主题和语言，不想保存侧边栏是否打开：

```ts
export const useSettingsStore = create<SettingsStore>()(
  persist(
    (set) => ({
      theme: "light",
      language: "zh-CN",
      sidebarOpen: false,

      setTheme: (theme) => set({ theme }),
      setLanguage: (language) => set({ language }),
      setSidebarOpen: (sidebarOpen) => set({ sidebarOpen }),
    }),
    {
      name: "settings-store",

      partialize: (state) => ({
        theme: state.theme,
        language: state.language,
      }),
    },
  ),
);
```

`partialize` 表示：

> 从完整 Store 中选择需要持久化的字段。

不要把这些内容放进 localStorage：

```text
密码
长期有效的敏感 Token
隐私数据
体积非常大的数据
```

---

## 持久化版本迁移

假设旧数据结构是：

```ts
{
  darkMode: true
}
```

后来改成：

```ts
{
  theme: "dark"
}
```

可以设置版本并迁移：

```ts
persist(
  (set) => ({
    theme: "light" as "light" | "dark",
    setTheme: (theme: "light" | "dark") => set({ theme }),
  }),
  {
    name: "settings-store",
    version: 2,

    migrate: (persistedState, version) => {
      const oldState = persistedState as {
        darkMode?: boolean;
        theme?: "light" | "dark";
      };

      if (version === 1) {
        return {
          theme: oldState.darkMode ? "dark" : "light",
        };
      }

      return persistedState;
    },
  },
);
```

对长期运行的项目，Store 数据结构变化时，版本迁移非常重要。

---

# 十一、Redux DevTools 调试

Zustand 可以通过 `devtools` 中间件接入 Redux DevTools，查看每次状态变化。([Zustand 文档][10])

```ts
import { create } from "zustand";
import { devtools } from "zustand/middleware";

interface CounterStore {
  count: number;
  increment: () => void;
  reset: () => void;
}

export const useCounterStore = create<CounterStore>()(
  devtools(
    (set) => ({
      count: 0,

      increment: () => {
        set(
          (state) => ({
            count: state.count + 1,
          }),
          false,
          "counter/increment",
        );
      },

      reset: () => {
        set(
          {
            count: 0,
          },
          false,
          "counter/reset",
        );
      },
    }),
    {
      name: "CounterStore",
    },
  ),
);
```

这里：

```ts
set(nextState, false, "counter/increment");
```

三个参数分别可以理解为：

```ts
set(
  更新内容,
  是否替换整个 Store,
  DevTools 中显示的 action 名称,
);
```

通常第二个参数都传：

```ts
false
```

表示合并状态。

---

# 十二、同时使用 persist 和 devtools

```ts
import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";

interface AppStore {
  count: number;
  increment: () => void;
}

export const useAppStore = create<AppStore>()(
  devtools(
    persist(
      (set) => ({
        count: 0,

        increment: () => {
          set((state) => ({
            count: state.count + 1,
          }));
        },
      }),
      {
        name: "app-store",
      },
    ),
    {
      name: "AppStore",
    },
  ),
);
```

中间件本质上是对 Store 创建函数进行包装：

```text
原始 Store
↓
persist 包装
↓
devtools 包装
↓
最终 Store
```

---

# 十三、在 React 组件外访问 Store

`create` 返回的 Hook 上还挂载了 Store API。([Zustand 文档][2])

## 1. 获取当前状态

```ts
const currentState = useCounterStore.getState();

console.log(currentState.count);
```

## 2. 修改状态

```ts
useCounterStore.setState({
  count: 100,
});
```

## 3. 调用 action

```ts
useCounterStore.getState().increment();
```

## 4. 订阅变化

```ts
const unsubscribe = useCounterStore.subscribe((state, previousState) => {
  console.log("新状态", state);
  console.log("旧状态", previousState);
});

// 取消订阅
unsubscribe();
```

这种方式适合：

```text
WebSocket 回调
路由守卫
普通工具函数
浏览器事件
非 React 代码
```

但不要在组件渲染中这样读取：

```tsx
function Counter() {
  const count = useCounterStore.getState().count;

  return <div>{count}</div>;
}
```

因为 `getState()` 只是读取一次，不会订阅变化。`count` 更新后，组件不会因此自动重新渲染。

组件里应该使用：

```tsx
const count = useCounterStore((state) => state.count);
```

---

# 十四、订阅特定状态

可以使用 `subscribeWithSelector`：

```ts
import { create } from "zustand";
import { subscribeWithSelector } from "zustand/middleware";

interface PositionStore {
  x: number;
  y: number;
  setX: (x: number) => void;
  setY: (y: number) => void;
}

export const usePositionStore = create<PositionStore>()(
  subscribeWithSelector((set) => ({
    x: 0,
    y: 0,

    setX: (x) => set({ x }),
    setY: (y) => set({ y }),
  })),
);
```

只订阅 `x`：

```ts
const unsubscribe = usePositionStore.subscribe(
  (state) => state.x,
  (x, previousX) => {
    console.log("x 从", previousX, "变成", x);
  },
);
```

`y` 变化时，这个回调不会执行。`subscribeWithSelector` 就是用来订阅 Store 中特定片段的。([Zustand 文档][11])

---

# 十五、复杂嵌套对象与 Immer

假设状态很深：

```ts
interface Store {
  user: {
    profile: {
      address: {
        city: string;
      };
    };
  };
}
```

普通写法：

```ts
set((state) => ({
  user: {
    ...state.user,
    profile: {
      ...state.user.profile,
      address: {
        ...state.user.profile.address,
        city: "上海",
      },
    },
  },
}));
```

层级多时比较麻烦，可以使用 Immer。

安装：

```bash
npm install immer
```

```ts
import { create } from "zustand";
import { immer } from "zustand/middleware/immer";

interface UserStore {
  user: {
    profile: {
      address: {
        city: string;
      };
    };
  };

  updateCity: (city: string) => void;
}

export const useUserStore = create<UserStore>()(
  immer((set) => ({
    user: {
      profile: {
        address: {
          city: "北京",
        },
      },
    },

    updateCity: (city) => {
      set((state) => {
        state.user.profile.address.city = city;
      });
    },
  })),
);
```

Immer 允许你写出类似“直接修改”的代码，但实际上会帮助你生成新的不可变状态。使用 Zustand 的 Immer 中间件时，需要额外安装 `immer`。([Zustand 文档][12])

不要因为有 Immer 就把状态设计得无限嵌套。优先思考是否能将数据结构扁平化。

---

# 十六、大型项目的 Store 拆分

小项目可以：

```text
stores/
└── app-store.ts
```

中大型项目建议按业务拆分：

```text
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   ├── api/
│   │   └── auth-store.ts
│   ├── editor/
│   │   ├── components/
│   │   └── editor-store.ts
│   └── settings/
│       └── settings-store.ts
└── stores/
    └── global-ui-store.ts
```

例如：

```text
auth-store
  当前用户
  登录状态
  权限信息

editor-store
  当前选中节点
  缩放比例
  编辑器模式

global-ui-store
  全局弹窗
  Sidebar 展开状态
  Toast 配置
```

不要一开始就创建：

```ts
useGlobalStore
```

然后把所有东西都放进去：

```ts
{
  user,
  todos,
  products,
  dialogs,
  editor,
  settings,
  orders,
  comments,
  ...
}
```

这种 Store 后面会越来越难维护。

---

# 十七、Slices Pattern

如果一些状态必须存在同一个 Store，但代码又很多，可以使用 Slice 模式。官方文档提供了将多个 slice 组合成一个 Store 的模式。([Zustand 文档][13])

## 1. 创建计数 Slice

```ts
import type { StateCreator } from "zustand";

export interface CounterSlice {
  count: number;
  increment: () => void;
}

export const createCounterSlice: StateCreator<
  CounterSlice & UserSlice,
  [],
  [],
  CounterSlice
> = (set) => ({
  count: 0,

  increment: () => {
    set((state) => ({
      count: state.count + 1,
    }));
  },
});
```

## 2. 创建用户 Slice

```ts
import type { StateCreator } from "zustand";

export interface UserSlice {
  username: string;
  setUsername: (username: string) => void;
}

export const createUserSlice: StateCreator<
  CounterSlice & UserSlice,
  [],
  [],
  UserSlice
> = (set) => ({
  username: "",

  setUsername: (username) => {
    set({ username });
  },
});
```

## 3. 合并 Store

```ts
import { create } from "zustand";
import {
  createCounterSlice,
  type CounterSlice,
} from "./counter-slice";
import {
  createUserSlice,
  type UserSlice,
} from "./user-slice";

type AppStore = CounterSlice & UserSlice;

export const useAppStore = create<AppStore>()((...args) => ({
  ...createCounterSlice(...args),
  ...createUserSlice(...args),
}));
```

组件依然正常使用：

```tsx
const count = useAppStore((state) => state.count);
const username = useAppStore((state) => state.username);
```

## 什么时候使用 Slice

适合：

```text
多个模块需要原子性地一起更新
多个模块之间需要通过 get() 相互访问
希望只有一个 Store，但拆分实现文件
```

不适合为了“看起来高级”而强行使用。很多业务直接使用多个独立 Store 更简单。

---

# 十八、重置 Store

## 简单重置

```ts
interface FormStore {
  name: string;
  email: string;
  reset: () => void;
}

const initialState = {
  name: "",
  email: "",
};

export const useFormStore = create<FormStore>()((set) => ({
  ...initialState,

  reset: () => {
    set(initialState);
  },
}));
```

注意不要把 action 放在 `initialState` 里：

```ts
const initialState = {
  name: "",
  email: "",
};
```

这样 `reset` 只负责恢复数据，不影响 action。

官方也提供了基于 `getInitialState()` 的重置方式。([Zustand 文档][14])

```ts
export const useStore = create<Store>()((set, get, store) => ({
  count: 0,

  reset: () => {
    set(store.getInitialState());
  },
}));
```

---

# 十九、测试 Zustand Store

由于 Store action 本质上是普通函数，可以直接测试，不一定要渲染 React 组件。

```ts
import { beforeEach, describe, expect, it } from "vitest";
import { useCounterStore } from "./counter-store";

describe("counter store", () => {
  beforeEach(() => {
    useCounterStore.setState({
      count: 0,
    });
  });

  it("should increment count", () => {
    useCounterStore.getState().increment();

    expect(useCounterStore.getState().count).toBe(1);
  });

  it("should reset count", () => {
    useCounterStore.setState({
      count: 10,
    });

    useCounterStore.getState().reset();

    expect(useCounterStore.getState().count).toBe(0);
  });
});
```

测试前重置 Store 很重要，因为模块级 Store 会在多个测试之间共享状态。官方测试指南也重点处理了 Store 重置问题。([Zustand 文档][15])

---

# 二十、常见错误

## 错误一：每个组件都订阅整个 Store

```tsx
const store = useTodoStore();
```

推荐：

```tsx
const todos = useTodoStore((state) => state.todos);
```

---

## 错误二：selector 每次返回新对象

不推荐：

```tsx
const value = useStore((state) => ({
  count: state.count,
  name: state.name,
}));
```

推荐分别订阅：

```tsx
const count = useStore((state) => state.count);
const name = useStore((state) => state.name);
```

或者：

```tsx
const value = useStore(
  useShallow((state) => ({
    count: state.count,
    name: state.name,
  })),
);
```

---

## 错误三：直接修改数组或对象

不推荐：

```ts
set((state) => {
  state.todos.push(todo);

  return {
    todos: state.todos,
  };
});
```

推荐：

```ts
set((state) => ({
  todos: [...state.todos, todo],
}));
```

或者使用 Immer。

---

## 错误四：认为 `set` 会递归合并

```ts
set({
  user: {
    name: "Dano",
  },
});
```

这会替换整个 `user`，不会保留其他字段。

应该：

```ts
set((state) => ({
  user: {
    ...state.user,
    name: "Dano",
  },
}));
```

---

## 错误五：存储可以推导的数据

不推荐：

```ts
{
  todos,
  completedTodos,
  uncompletedTodos,
  completedCount,
}
```

只保存：

```ts
{
  todos,
}
```

使用时计算：

```ts
const completedCount = useTodoStore(
  (state) => state.todos.filter((todo) => todo.completed).length,
);
```

---

## 错误六：把所有接口数据都放进 Zustand

Zustand 可以执行异步请求，但不自动提供完整的服务端缓存管理。

一般组合是：

```text
Zustand
负责客户端状态

TanStack Query
负责服务端状态

React Hook Form
负责复杂表单状态

useState
负责组件局部状态
```

---

## 错误七：只有一个超级 Store

一开始看起来方便：

```ts
useAppStore
```

项目变大后会变成：

```text
改一个业务模块
需要进入一个几千行的 Store
```

更好的做法是按照业务边界拆分：

```text
useAuthStore
useEditorStore
useSettingsStore
useGlobalUIStore
```

---

# 二十一、推荐的日常写法

一个比较标准的 TypeScript Store：

```ts
import { create } from "zustand";

interface ExampleState {
  count: number;
  keyword: string;
}

interface ExampleActions {
  increment: () => void;
  setKeyword: (keyword: string) => void;
  reset: () => void;
}

type ExampleStore = ExampleState & ExampleActions;

const initialState: ExampleState = {
  count: 0,
  keyword: "",
};

export const useExampleStore = create<ExampleStore>()((set) => ({
  ...initialState,

  increment: () => {
    set((state) => ({
      count: state.count + 1,
    }));
  },

  setKeyword: (keyword) => {
    set({ keyword });
  },

  reset: () => {
    set(initialState);
  },
}));
```

组件中精确订阅：

```tsx
function Example() {
  const count = useExampleStore((state) => state.count);
  const increment = useExampleStore((state) => state.increment);

  return (
    <button onClick={increment}>
      {count}
    </button>
  );
}
```

---

# 二十二、最终知识地图

学习 Zustand，可以记住下面这张图：

```text
create
└── 创建 Store

set
├── set({ count: 0 })
└── set(state => ({ count: state.count + 1 }))

get
└── 在 action 内读取当前状态

selector
└── useStore(state => state.count)

middleware
├── persist
├── devtools
├── subscribeWithSelector
└── immer

Store 外部 API
├── useStore.getState()
├── useStore.setState()
└── useStore.subscribe()
```

实际开发时，最重要的是五条：

```text
1. 只把真正需要共享的状态放进 Zustand
2. 组件通过 selector 精确订阅状态
3. 更新对象、数组时保持不可变
4. set 只会自动合并第一层
5. 服务端状态优先交给 TanStack Query
```

掌握到这里，你已经可以在正常的 React 项目里正确使用 Zustand，包括 TypeScript、异步请求、持久化、性能优化和大型 Store 拆分。

[1]: https://www.npmjs.com/package/zustand?utm_source=chatgpt.com "zustand"
[2]: https://zustand.docs.pmnd.rs/reference/apis/create?utm_source=chatgpt.com "create - Zustand"
[3]: https://zustand.docs.pmnd.rs/learn/guides/updating-state?utm_source=chatgpt.com "Updating state - Zustand"
[4]: https://zustand.docs.pmnd.rs/learn/guides/auto-generating-selectors?utm_source=chatgpt.com "Auto Generating Selectors - Zustand"
[5]: https://zustand.docs.pmnd.rs/learn/guides/prevent-rerenders-with-use-shallow?utm_source=chatgpt.com "Prevent rerenders with useShallow - Zustand"
[6]: https://zustand.docs.pmnd.rs/learn/guides/immutable-state-and-merging?utm_source=chatgpt.com "Immutable state and merging - Zustand"
[7]: https://zustand.docs.pmnd.rs/learn/guides/maps-and-sets-usage?utm_source=chatgpt.com "Map and Set Usage - Zustand"
[8]: https://zustand.docs.pmnd.rs/learn/guides/beginner-typescript?utm_source=chatgpt.com "Beginner TypeScript Guide - Zustand"
[9]: https://zustand.docs.pmnd.rs/reference/middlewares/persist?utm_source=chatgpt.com "persist - Zustand"
[10]: https://zustand.docs.pmnd.rs/reference/middlewares/devtools?utm_source=chatgpt.com "devtools - Zustand"
[11]: https://zustand.docs.pmnd.rs/reference/middlewares/subscribe-with-selector?utm_source=chatgpt.com "subscribeWithSelector - Zustand"
[12]: https://zustand.docs.pmnd.rs/reference/integrations/immer-middleware?utm_source=chatgpt.com "Immer middleware - Zustand"
[13]: https://zustand.docs.pmnd.rs/learn/guides/slices-pattern?utm_source=chatgpt.com "Slices Pattern - Zustand"
[14]: https://zustand.docs.pmnd.rs/learn/guides/how-to-reset-state?utm_source=chatgpt.com "How to reset state - Zustand"
[15]: https://zustand.docs.pmnd.rs/learn/guides/testing?utm_source=chatgpt.com "Testing - Zustand"
