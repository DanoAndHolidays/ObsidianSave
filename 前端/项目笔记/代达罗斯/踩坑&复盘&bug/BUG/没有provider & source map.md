# 没有provider & source map
> Last Format Time：8/13/2026 15:14:03

你这里的 **source map 就在你下面贴出来的这段 JavaScript 里**，并没有单独的 `.map` 文件。

inline source map（内联 Source Map）：
```js
//# sourceMappingURL=data:application/json;base64,eyJtYXBwaW5ncyI6...
```

```text
你写的 TS
mcpSetupPageStore.ts
        ↓
      Vite 转换
        ↓
浏览器真正执行的 JS
        +
内嵌在 JS 末尾的 Source Map
        ↓
Chrome DevTools 根据 Source Map
把 JS 映射回原来的 TS
```

### Source Map
你贴的代码最下面：
```js
//# sourceMappingURL=data:application/json;base64,...
```

这里的：
```text
data:application/json;base64,...
```

其实就是一个完整的 JSON，只不过进行了 Base64 编码。把它解码之后，大概就是你已经在后面看到的这个内容：
```json
{
  "mappings": "AAAA,SAAS,eAAe,...",
  "names": [],
  "sources": [
    "mcpSetupPageStore.ts"
  ],
  "version": 3,
  "sourcesContent": [
    "import { createContext, useContext } from \"react\";\r\n..."
  ]
}
```

这里面最重要的是几个字段：
```json
{
  "sources": ["mcpSetupPageStore.ts"],
  "sourcesContent": ["你的原始 TypeScript 代码"],
  "mappings": "AAAA,SAAS,..."
}
```

也就是说，**你的原始 TS 代码甚至直接被装进 Source Map 里面了。**


### 那你图里 DevTools 看到的 `mcpSetupPageStore.ts` 是什么？
你截图里 Sources 面板显示：

```text
src
└─ pages
   └─ McpSetupPage
      └─ _store
         └─ mcpSetupPageStore.ts
```

然后右边显示的是：

```ts
import { createContext, useContext } from "react";
import { createStore, type StoreApi } from "zustand";
...
```

看起来就跟你本地写的代码一模一样。

但这里要注意：

**浏览器实际上并不是直接执行这份 TypeScript。**

浏览器实际执行的是你下面贴出来的转换代码：

```js
const createContext = __vite__cjsImport0_react["createContext"];
const useContext = __vite__cjsImport0_react["useContext"];

import __vite__cjsImport0_react from "/node_modules/.vite/deps/react.js?v=4b60aafd";

import { createStore } from "/node_modules/.vite/deps/zustand.js?v=02894596";

import { createMcpSetupPageSlice }
  from "/src/pages/McpSetupPage/_store/mcpSetupPageSlice.ts";

export const createMcpSetupPageStore = (dependencies) =>
  createStore()((set, get, api) =>
    createMcpSetupPageSlice(dependencies)(set, get, api)
  );
```

Chrome 发现最后有：

```js
//# sourceMappingURL=...
```

于是：

> 哦，这个 JS 有 Source Map，我可以把它恢复成开发者原来写的 TS。

所以 DevTools 给你展示：

```ts
export type McpSetupPageStore =
  StoreApi<McpSetupPageSlice>;

export const createMcpSetupPageStore = (
  dependencies: McpSetupPageDependencies,
): McpSetupPageStore =>
  ...
```

这其实是一个 **Source Mapped Source（映射出来的源代码视图）**。


### 你的 Source Map 为什么还能直接显示完整 TS？
因为这里有：

```json
"sourcesContent": [
  "import { createContext, useContext } from \"react\";\r\n..."
]
```

这个字段非常关键。

Source Map 有两种情况。

一种只告诉浏览器：

```json
{
  "sources": ["mcpSetupPageStore.ts"]
}
```

那么浏览器还得想办法找到这个文件。

而你现在 Vite 生成的是：

```json
{
  "sources": ["mcpSetupPageStore.ts"],
  "sourcesContent": [
    "完整的 TypeScript 源码"
  ]
}
```

相当于：

```text
JS 文件
├── 编译后的 JavaScript
└── Source Map
    ├── 原始文件叫什么
    ├── 原始文件完整内容
    └── JS 每个位置对应 TS 哪个位置
```

所以 Chrome 根本不用重新去服务器获取一份 TS 文件来显示源码。


### `mappings` 又是干什么的？
这一串你看到：

```json
"mappings": "AAAA,SAAS,eAAe,kBAAkB;AAC1C,..."
```

就是 Source Map 最核心的部分。

它大概表达：

```text
生成 JS 第 1 行第 0 列
       ↓
对应
TS 第 1 行第 0 列

生成 JS 第 7 行第 15 列
       ↓
对应
TS 第 11 行第 20 列
```

实际格式当然进行了压缩，不是这么直白。

所以你打断点的时候，例如你在 DevTools 的：

```ts
const store = useContext(McpSetupPageStoreContext);
```

这一行打断点。

Chrome 会通过：

```text
Source Map
TS 23 行
    ↓
映射
JS 第 XX 行第 XX 列
```

真正给 JS 设置断点。

所以你感觉自己是在 **调试 TypeScript**，实际上浏览器还是在调试 JavaScript。


### 为什么这里没有看到 `.map` 文件？
因为 Source Map 有两种常见形式。

生产环境有时候是：

```js
//# sourceMappingURL=index.js.map
```

此时目录可能是：

```text
index.js
index.js.map
```

浏览器会请求：

```text
GET /index.js.map
```

这是 **external source map**。

但你的 Vite 开发环境现在是：

```js
//# sourceMappingURL=data:application/json;base64,...
```

也就是：

```text
JS
└── Source Map 直接塞在这里
```

所以不存在一个：

```text
mcpSetupPageStore.ts.map
```

让你去磁盘上找。


### 你这个例子特别适合理解 TS 的「类型擦除」
你前段时间问过 TypeScript 的：

```ts
import type
```

以及：

```ts
type User = z.infer<typeof UserSchema>;
```

为什么编译以后类型消失。

你这里其实已经亲眼看到结果了。

原始 TS：

```ts
import { createStore, type StoreApi } from "zustand";

import type {
  McpSetupPageDependencies
} from "./mcpSetupPageDependencies";

export type McpSetupPageStore =
  StoreApi<McpSetupPageSlice>;

export const createMcpSetupPageStore = (
  dependencies: McpSetupPageDependencies,
): McpSetupPageStore => ...
```

浏览器真正执行：

```js
import { createStore } from "/node_modules/.vite/deps/zustand.js?...";

export const createMcpSetupPageStore = (dependencies) =>
  createStore()(...);
```

你会发现：

```ts
StoreApi
McpSetupPageDependencies
McpSetupPageStore
McpSetupPageSlice 类型
```

全部消失了。

因为这些：

```ts
type
interface
泛型参数
函数参数类型
返回值类型
```

都只是 TypeScript 编译阶段的信息。

但是有趣的地方就在这里：

**它们虽然不在实际执行的 JS 中，却又出现在 DevTools 里。**

原因不是浏览器认识 TypeScript，而是：

```text
Source Map 的 sourcesContent
把原始 TS 又带给了 Chrome
```

所以整个结构其实是：

```text
                     ┌──────── 浏览器真正执行
                     ↓
mcpSetupPageStore.ts → Vite → JavaScript
        │                       │
        │                       │
        └──── Source Map ───────┘
                 ↓
        Chrome DevTools
                 ↓
       又给你显示成 TS
```

因此你截图里绿色选中的 `mcpSetupPageStore.ts`，本质上是 **Chrome 根据 Vite 提供的 Source Map 给你构造出来的原始源码视图**；真正执行的仍然是下面那份已经去掉 TypeScript 类型的 JavaScript。

---
## provider
```ts
// todo 这里的McpSetupPageStoreContext是null，导致了store的值为null，似乎是不太对？？？其他的位置也是这样写的啊

export const useMcpSetupPageStore = (): McpSetupPageStore => {
  console.log("McpSetupPageStoreContext", McpSetupPageStoreContext)
  const store = useContext(McpSetupPageStoreContext);
  console.log("store", store)
  if (!store) {
    throw new Error(
      "useMcpSetupPageStore must be used within a McpSetupPageStoreProvider",
    );
  }

  return store;
};
```

![[Pasted image 20260811145031.png]]

---
## Provider 缺失问题复盘
### 运行时现象
`McpSetupGuide` 渲染时执行：

```ts
const pageStore = useMcpSetupPageStore();
```

随后 `useMcpSetupPageStore` 从 `McpSetupPageStoreContext` 读取值：

```ts
const store = useContext(McpSetupPageStoreContext);

if (!store) {
  throw new Error(
    "useMcpSetupPageStore must be used within a McpSetupPageStoreProvider",
  );
}
```

Dialog 中打开 MCP 配置指南时，`store` 是 `null`，因此抛出错误。

### 最初的误区：`createContext(null)` 是否写错了
```ts
export const McpSetupPageStoreContext =
  createContext<McpSetupPageStore | null>(null);
```

这里的 `null` 只是 Context 的默认值，不代表 Context 永远是 `null`。

- 消费组件处于对应 Provider 的后代树中时，`useContext` 返回 Provider 的 `value`。
- 当前渲染树中找不到对应 Provider 时，`useContext` 才返回默认值 `null`。

因此问题不在 `createContext(null)`，而在于需要检查消费组件的真实渲染路径。

另外，直接打印 `McpSetupPageStoreContext` 对象容易产生误解。真正有判断价值的是组件渲染期间 `useContext(McpSetupPageStoreContext)` 的结果，以及消费组件上方是否存在同一个 Context 的 Provider。

### 定位过程：从消费点反向追踪渲染树
首先找到消费 Store 的位置：

```text
McpSetupGuide
└─ useMcpSetupPageStore()
   └─ useContext(McpSetupPageStoreContext)
```

然后搜索 `McpSetupGuide` 的所有生产代码入口，发现主要有两条路径。

##### 正常路径：MCP Setup 页面
```text
McpSetupPage
└─ McpSetupPageStoreProvider
   └─ McpSetupPageContent
      └─ McpSetupGuide
```

`McpSetupPage.tsx` 在页面 Wrapper 层提供了 Store，所以这条路径不会报错。

##### 异常路径：连接详情 Dialog
修复前的路径是：

```text
AiReviewsSettingsPageStoreProvider
└─ McpConnectionDetailsDialog
   └─ McpSetupGuide
```

这里虽然存在 `AiReviewsSettingsPageStoreProvider`，但它提供的是另一个 Context。React Context 按 Context 对象本身匹配，而不是看 Store 结构是否相似，因此它不能替代 `McpSetupPageStoreProvider`。

最终根因是：`McpSetupGuide` 跨页面复用后，Dialog 路径没有同时带上该组件依赖的 `McpSetupPageStoreProvider`。

### 为什么原有测试没有提前发现
`McpConnectionDetailsDialog.test.tsx` 在测试外层手动包了 `McpSetupPageStoreProvider`：

```tsx
<AiReviewsSettingsPageFixtureProvider>
  <McpSetupPageStoreProvider dependencies={...}>
    <McpConnectionDetailsDialog ... />
  </McpSetupPageStoreProvider>
</AiReviewsSettingsPageFixtureProvider>
```

这使测试环境和真实生产渲染树不一致。即使生产 Dialog 自己没有 Provider，测试仍然会通过，所以测试把这个缺陷遮住了。

更有效的回归测试应移除测试额外提供的 `McpSetupPageStoreProvider`，只保留生产环境真正拥有的 `AiReviewsSettingsPageFixtureProvider`。这样只有 Dialog 自己正确建立 Provider 边界时测试才会通过。

### 修复方式
在 Dialog 中使用 `McpSetupGuide` 的位置补上 `McpSetupPageStoreProvider`，并提供与页面路径相同的依赖：

```tsx
{connection.status !== "revoked" && (
  <McpSetupPageStoreProvider
    key={connection.id}
    dependencies={{
      copyText: (value) => navigator.clipboard.writeText(value),
      scheduleCopiedReset: (reset) => {
        globalThis.setTimeout(reset, 2000);
      },
      setup: connection.setup,
    }}
  >
    <McpSetupGuide setup={connection.setup} />
  </McpSetupPageStoreProvider>
)}
```

Provider 现在位于消费组件的祖先树中，`useContext` 能取得新建的 Zustand Store，原始的 `null` 错误因此消失。

### 为什么还需要 `key={connection.id}`
Provider 内使用 `useInit` 创建 Store：

```ts
const store = useInit(() => createMcpSetupPageStore(dependencies));
```

`useInit` 通过 `useRef` 保存首次创建的值。同一个 Provider 实例后续即使收到新的 `dependencies`，也不会重新创建 Store。

如果用户在 Dialog 中从连接 A 切换到连接 B，而 Provider 实例被 React 复用，Store 内闭包仍可能持有连接 A 的 `setup`。结果是界面显示连接 B，但复制按钮仍可能复制连接 A 的命令或文档地址。

```tsx
key={connection.id}
```

让连接 ID 成为 Provider 的组件身份：

```text
connection A，key=A
└─ 创建 Provider A + Store A

connection 仍为 A
└─ 复用 Provider A + Store A

connection 变为 B，key=B
├─ 卸载 Provider A + Store A
└─ 创建 Provider B + Store B
```

所以 `key` 不是直接“更新 Provider”，而是在 key 变化时让 React 卸载旧实例并挂载新实例，从而重新执行 `useInit`。

这和列表中的 `key` 是同一套 React reconciliation 机制：

- 列表中的 key 用来在增删和排序时保持每一项的正确身份。
- 这里的 key 用来在逻辑实体从连接 A 变为连接 B 时主动更换组件身份并重置 Store。

必须使用稳定的业务标识，例如 `connection.id`。不能使用 `Math.random()`，否则每次渲染都会重建 Provider，导致内部状态和副作用反复重置。

### Source Map 在这次排查中的作用
浏览器报错定位到 `mcpSetupPageStore.ts`，并不表示浏览器直接执行 TypeScript，也不表示 Source Map 导致了错误。

实际过程是：

```text
McpConnectionDetailsDialog 渲染 McpSetupGuide
→ useMcpSetupPageStore 读取不到 Provider
→ 编译后的 JavaScript 抛出错误
→ inline source map 将 JavaScript 报错位置映射回 mcpSetupPageStore.ts
→ DevTools 展示 TypeScript 原始位置
```

Source Map 只是提高了定位精度。真正的运行时根因仍然是 Provider 边界缺失。

### 本次改动审查结果
##### 已确认正确
- Dialog 中的 `McpSetupGuide` 已被正确的 `McpSetupPageStoreProvider` 包裹。
- Provider 收到了复制文本、延迟重置和当前 `setup` 三项完整依赖。
- 使用稳定的 `connection.id` 作为 key，可避免连接切换时继续使用旧 Store。
- `mcpSetupPageStore.ts` 中用于排查的 `console.log` 和 TODO 已移除。
- 目标 oxlint 检查通过。
- 三个相关单元测试通过：Dialog、Guide、Store，共 3 个测试文件、3 个测试。

##### 仍需处理
1. **Dialog 测试仍然额外包裹 Provider**

   当前测试无法证明生产路径已经修复。应移除测试外层的 `McpSetupPageStoreProvider`，让测试覆盖 Dialog 自己建立 Provider 边界的行为。

2. **缺少连接切换回归测试**

   可以先渲染连接 A，再切换为连接 B，触发复制按钮并断言复制的是连接 B 的内容，以验证 `key={connection.id}` 的实际效果。

3. **独立 Content Story 仍缺 Provider**

   `McpSetupPageContent.stories.tsx` 直接渲染 `McpSetupPageContent`，没有经过 `McpSetupPage` Wrapper，因此其中的 `McpSetupGuide` 仍可能得到 `null`。该 Story 应通过 decorator 或专用 Story Wrapper 补齐 Provider。

4. **当前文件未通过 Prettier 检查**

   `McpConnectionDetailsDialog.tsx` 中 `Intl.DateTimeFormat` 的对象缩进被一并改变。功能不受影响，oxlint 也通过，但 `prettier --check` 失败。应运行项目格式化工具恢复标准缩进，并确认新增 import 的位置符合格式化结果。

5. **全量验证存在环境阻塞**

   - `bun run check-types` 被 `vitest.config.ts` 中 `oxc` 配置与当前 Vite 类型不匹配阻塞。
   - Storybook 测试因 Vitest 版本混用、缺少若干 optimizeDeps，以及本机缺少 Playwright Chromium 而无法启动。

   这些错误不是本次 Provider 改动产生的，但意味着目前不能声称全量质量检查已经通过。

### 最终结论
这次问题不是 Zustand Store 创建失败，也不是 `createContext(null)` 或 Source Map 有问题，而是组件复用时遗漏了它的运行时上下文依赖。

排查这类问题可以固定采用下面的顺序：

```text
找到抛错的自定义 hook
→ 确认它读取哪个 Context
→ 搜索消费组件的全部渲染入口
→ 逐条画出 Provider 到 Consumer 的祖先链
→ 对比测试树与生产树是否一致
→ 对带初始化依赖的 Provider 检查实体切换和 Store 生命周期
```

核心经验是：组件能够被 import 和渲染，不代表它所依赖的 Context 也会自动随组件一起出现。复用 Context Consumer 时，必须同时设计清晰的 Provider 边界和对应的回归测试。
