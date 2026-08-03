# useTheme
当然。你只要真正理解一句话，`useContext` 就掌握一半了：

> `useContext` 用来让某个祖先组件，把数据直接提供给后代组件，避免一层一层通过 props 传递。

可以把 Context 想象成组件树里的一座“局部广播站”：

* `createContext`：创建频道
* `Provider`：广播数据
* `useContext`：接收数据

## 一、为什么需要 useContext

假设组件结构是：

```text
App
└── Layout
    └── Header
        └── UserAvatar
```

`UserAvatar` 需要当前用户信息。

如果只使用 props，就需要这样传递：

```tsx
function App() {
  const user = { name: "Dano" };

  return <Layout user={user} />;
}

function Layout({ user }) {
  return <Header user={user} />;
}

function Header({ user }) {
  return <UserAvatar user={user} />;
}

function UserAvatar({ user }) {
  return <div>{user.name}</div>;
}
```

问题是：`Layout` 和 `Header` 自己根本不用 `user`，却必须负责转交。

这叫做 **props drilling（属性逐层传递）**。

使用 Context 后，可以让 `App` 直接把数据提供给下面所有组件。

---

## 二、useContext 的三个步骤

### 第一步：创建 Context

```tsx
import { createContext } from "react";

const UserContext = createContext(null);
```

这里相当于创建了一个叫 `UserContext` 的数据频道。

注意：`UserContext` 本身不是具体数据，它只是负责标识“这是哪一种上下文”。

---

### 第二步：使用 Provider 提供数据

```tsx
function App() {
  const user = {
    name: "Dano",
    age: 18,
  };

  return (
    <UserContext.Provider value={user}>
      <Layout />
    </UserContext.Provider>
  );
}
```

`value={user}` 就是实际广播出去的数据。

只要组件位于 `UserContext.Provider` 内部，不管嵌套多深，都可以读取 `user`。

---

### 第三步：使用 useContext 读取数据

```tsx
import { useContext } from "react";

function UserAvatar() {
  const user = useContext(UserContext);

  return <div>当前用户：{user.name}</div>;
}
```

完整代码如下：

```tsx
import { createContext, useContext } from "react";

const UserContext = createContext(null);

export default function App() {
  const user = {
    name: "Dano",
    age: 18,
  };

  return (
    <UserContext.Provider value={user}>
      <Layout />
    </UserContext.Provider>
  );
}

function Layout() {
  return <Header />;
}

function Header() {
  return <UserAvatar />;
}

function UserAvatar() {
  const user = useContext(UserContext);

  return (
    <div>
      {user.name}，今年 {user.age} 岁
    </div>
  );
}
```

数据流是：

```text
UserContext.Provider
        │ value={user}
        ▼
      Layout
        ▼
      Header
        ▼
  UserAvatar
        │
        └── useContext(UserContext)
```

---

## 三、Context 中的数据怎么修改

`useContext` 负责读取数据，但它自己并不管理数据。

如果数据需要变化，通常要配合 `useState`：

```tsx
import {
  createContext,
  useContext,
  useState,
  type ReactNode,
} from "react";

type Theme = "light" | "dark";

interface ThemeContextValue {
  theme: Theme;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

export default function App() {
  const [theme, setTheme] = useState<Theme>("light");

  const toggleTheme = () => {
    setTheme(currentTheme =>
      currentTheme === "light" ? "dark" : "light"
    );
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      <Page />
    </ThemeContext.Provider>
  );
}

function Page() {
  return <ThemeButton />;
}

function ThemeButton() {
  const context = useContext(ThemeContext);

  if (context === null) {
    throw new Error("ThemeButton 必须在 ThemeContext.Provider 内使用");
  }

  const { theme, toggleTheme } = context;

  return (
    <button onClick={toggleTheme}>
      当前主题：{theme}
    </button>
  );
}
```

这里的关键点是：

```tsx
value={{ theme, toggleTheme }}
```

我们不仅把状态 `theme` 传下去了，也把修改状态的方法 `toggleTheme` 传下去了。

因此后代组件既能读取状态，也能修改状态。

当 `theme` 改变时，使用了这个 Context 的组件会自动重新渲染。React 会读取组件上方最近的 Provider，并订阅它的变化。[React 官方 useContext 文档](https://react.dev/reference/react/useContext)

---

## 四、推荐封装成自定义 Hook

每个组件都这样判断有点麻烦：

```tsx
const context = useContext(ThemeContext);

if (context === null) {
  throw new Error("...");
}
```

实际项目通常封装一个 `useTheme`：

```tsx
function useTheme() {
  const context = useContext(ThemeContext);

  if (context === null) {
    throw new Error("useTheme 必须在 ThemeProvider 内使用");
  }

  return context;
}
```

然后组件里直接使用：

```tsx
function ThemeButton() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button onClick={toggleTheme}>
      当前主题：{theme}
    </button>
  );
}
```

还可以把 Provider 本身也封装起来：

```tsx
import {
  createContext,
  useContext,
  useState,
  type ReactNode,
} from "react";

type Theme = "light" | "dark";

interface ThemeContextValue {
  theme: Theme;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>("light");

  function toggleTheme() {
    setTheme(current =>
      current === "light" ? "dark" : "light"
    );
  }

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);

  if (context === null) {
    throw new Error("useTheme 必须在 ThemeProvider 内使用");
  }

  return context;
}
```

在入口处包裹：

```tsx
function App() {
  return (
    <ThemeProvider>
      <Page />
    </ThemeProvider>
  );
}
```

任意后代组件使用：

```tsx
function Page() {
  const { theme, toggleTheme } = useTheme();

  return (
    <main>
      <p>当前主题：{theme}</p>
      <button onClick={toggleTheme}>切换主题</button>
    </main>
  );
}
```

这是实际开发中最推荐的组织方式。

---

## 五、createContext 里的默认值是什么

例如：

```tsx
const ThemeContext = createContext("light");
```

如果组件上方没有对应的 Provider：

```tsx
function Button() {
  const theme = useContext(ThemeContext);

  console.log(theme); // "light"
}
```

它会得到 `createContext` 中的默认值。

但要注意：

```tsx
<ThemeContext.Provider value={undefined}>
  <Button />
</ThemeContext.Provider>
```

这时拿到的是 `undefined`，不是默认值。

默认值只在“完全找不到 Provider”时生效。

在 TypeScript 项目中，我通常推荐：

```tsx
const ThemeContext = createContext<ThemeContextValue | null>(null);
```

然后通过自定义 Hook 检查：

```tsx
if (context === null) {
  throw new Error("useTheme 必须在 ThemeProvider 内使用");
}
```

这样如果忘记包裹 Provider，错误会非常明确。

---

## 六、多个 Provider 时读取哪一个

`useContext` 会读取组件上方距离它最近的 Provider：

```tsx
<ThemeContext.Provider value="light">
  <Header />

  <ThemeContext.Provider value="dark">
    <Content />
  </ThemeContext.Provider>
</ThemeContext.Provider>
```

结果：

```tsx
function Header() {
  const theme = useContext(ThemeContext);
  // "light"
}

function Content() {
  const theme = useContext(ThemeContext);
  // "dark"
}
```

内层 Provider 会覆盖外层 Provider，但只影响自己的后代。

这很像 JavaScript 中的作用域：

```ts
const theme = "light";

{
  const theme = "dark";
  console.log(theme); // "dark"
}
```

---

## 七、一个特别容易犯的错误

下面这样不行：

```tsx
function App() {
  const theme = useContext(ThemeContext);

  return (
    <ThemeContext.Provider value="dark">
      <div>{theme}</div>
    </ThemeContext.Provider>
  );
}
```

因为 `App` 调用 `useContext` 时，Provider 在它返回的 JSX 里面，不在 `App` 的上方。

Context 只能向下提供，不能提供给 Provider 自己所在的组件。

应该拆成：

```tsx
function App() {
  return (
    <ThemeContext.Provider value="dark">
      <Content />
    </ThemeContext.Provider>
  );
}

function Content() {
  const theme = useContext(ThemeContext);

  return <div>{theme}</div>;
}
```

---

## 八、什么时候应该使用 Context

适合放入 Context 的数据通常具有两个特点：

1. 很多不同层级的组件都需要。
2. 数据具有一定的“全局性”或“区域共享性”。

常见场景：

* 当前登录用户
* 主题色、深色模式
* 当前语言
* 用户权限
* 全局弹窗
* 表单多个子组件共享的数据
* 页面级配置

不建议什么都放 Context。

例如只有父子两层需要的数据：

```tsx
function Parent() {
  const name = "Dano";

  return <Child name={name} />;
}
```

直接传 props 更简单，不需要 Context。

可以这样判断：

> 数据只传一两层：优先 props。
> 很多层、很多组件都需要：考虑 Context。

---

## 九、性能方面要注意什么

当 Provider 的 `value` 发生变化时，读取该 Context 的组件会重新渲染。

下面每次 `App` 渲染都会产生一个新对象：

```tsx
<UserContext.Provider value={{ user, logout }}>
  <Page />
</UserContext.Provider>
```

即使 `user` 没变化，`{ user, logout }` 也是一个新的对象引用。

组件较复杂时，可以用 `useMemo` 和 `useCallback` 保持引用稳定：

```tsx
const logout = useCallback(() => {
  setUser(null);
}, []);

const contextValue = useMemo(() => {
  return {
    user,
    logout,
  };
}, [user, logout]);

return (
  <UserContext.Provider value={contextValue}>
    <Page />
  </UserContext.Provider>
);
```

不过不要一看到 Context 就急着优化。先正常编写，确认存在实际性能问题后再处理。

还有一种常见优化方式是把不同类型的数据拆成多个 Context：

```tsx
<UserContext.Provider value={user}>
  <ThemeContext.Provider value={theme}>
    <App />
  </ThemeContext.Provider>
</UserContext.Provider>
```

这样主题改变时，不会因为把所有数据塞在同一个 Context 中而影响不相关的用户组件。

---

## 十、React 19 的写法变化

为了兼容 React 18 及更早版本，我们前面使用的是：

```tsx
<ThemeContext.Provider value={theme}>
  <Page />
</ThemeContext.Provider>
```

React 19 开始，可以简写为：

```tsx
<ThemeContext value={theme}>
  <Page />
</ThemeContext>
```

两者表达的意思相同；React 18 项目继续使用 `.Provider`。[React 官方 createContext 文档](https://react.dev/reference/react/createContext)

---

## 最后总结

记住这个固定套路：

```tsx
// 1. 创建
const MyContext = createContext(defaultValue);

// 2. 提供
<MyContext.Provider value={数据}>
  <Child />
</MyContext.Provider>

// 3. 读取
const 数据 = useContext(MyContext);
```

如果数据需要修改：

```tsx
const [state, setState] = useState(...);

<MyContext.Provider value={{ state, setState }}>
  <Child />
</MyContext.Provider>
```

你可以把它牢牢记成一句话：

> `useState` 负责保存数据，Provider 负责向下提供数据，`useContext` 负责读取并订阅数据。
