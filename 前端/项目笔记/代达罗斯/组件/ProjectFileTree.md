# ProjectFileTree
> Last Format Time：7/15/2026 16:05:36

[Linear：COD-220 Keep large repository file trees responsive](https://linear.app/code-forge-official/issue/COD-220/repositorybug%E4%BD%9C%E4%B8%BA%E4%BB%A3%E7%A0%81%E5%AE%A1%E6%9F%A5%E5%91%98%E6%88%91%E5%B8%8C%E6%9C%9B%E5%A4%A7%E5%9E%8B%E4%BB%93%E5%BA%93%E7%9A%84%E6%96%87%E4%BB%B6%E6%A0%91%E4%BF%9D%E6%8C%81%E6%B5%81%E7%95%85-keep-large-repository-file-trees)

这篇笔记记录 COD-220 的完整实现过程：为什么要改造文件树、为什么选择 `@tanstack/react-virtual`、树形数据如何转换为可虚拟化的线性列表，以及源码中的状态管理、可访问性和性能边界。

---
## 需求背景
项目详情页左侧展示 GitHub 仓库文件树。改造前的实现由 `ProjectFileTreeNode` 递归渲染自身的 `children`，并且目录节点默认展开。

这会形成两个叠加问题：
- 初始进入页面时，所有目录都展开，所有节点都会参与 React 渲染。
- 每个节点都创建真实 DOM、事件处理器、组件状态和 Effect，仓库越大，初次渲染与后续更新越慢。
- 深层目录通过递归组件嵌套，React 树和 DOM 树都很深。
- 切换选中文件等父级状态时，大量节点可能重新参与协调。

COD-220 的目标是让大型仓库的文件树保持流畅，重点降低首屏渲染量、DOM 节点数量和 React 协调成本，同时保留展开目录、选择文件、扫描文件或目录、跳转 GitHub 等现有能力。

### 性能问题的准确边界
这次方案优化的是“渲染层内存和计算量”，不是“文件树原始数据的内存占用”。`useGithubTree` 返回的完整 `GitHubFileNode[]` 仍保存在前端内存里，`collectDirectoryPaths` 也会遍历完整数据树。

因此，方案解决的是以下问题：
- 避免为全部节点创建 React 组件和 DOM。
- 避免默认展开导致首屏生成完整可见树。
- 将滚动过程中的渲染规模限制在视口附近。

如果未来瓶颈来自 GitHub Tree API 返回的数据量或完整 JSON 本身，则还需要服务端分页、按目录懒加载或分块获取，这不属于本次改造范围。

---
## 改造前的实现
改造前，展开状态存放在每一个 `ProjectFileTreeNode` 内部，并默认设为 `true`：
```tsx
const [expanded, setExpanded] = useState(true);

{isDirectory && expanded && node.children && node.children.length > 0 && (
  <div className="ml-4">
    {node.children.map((child) => (
      <ProjectFileTreeNode key={child.path} node={child} />
    ))}
  </div>
)}
```

这种写法对小型树很直观，但不适合虚拟化。虚拟列表需要知道一个连续列表的总行数、每一行的索引和尺寸，而递归组件把可见节点分散在不同层级中，虚拟化器无法统一计算滚动区高度与行位置。

另外，每个目录各自管理 `expanded`，父级无法一次得到“当前究竟有哪些节点可见”。因此本次改造首先要把展开状态提升到树组件，再把当前可见的树形结构扁平化。

---
## 技术选型
最终只新增一个运行时依赖：
```json
{
  "@tanstack/react-virtual": "^3.14.6"
}
```

### 为什么选择 TanStack Virtual
- 它只负责虚拟化计算，不强制组件结构和视觉样式，适合现有自定义文件树。
- `useVirtualizer` 可以直接接入现有滚动容器。
- 支持固定高度估算、overscan、稳定 item key 和绝对定位布局。
- 项目已经使用 TanStack Router、Query、Table 和 Start，依赖体系一致。
- 无需引入完整 Tree UI 库，现有交互、菜单、国际化和样式可以保留。

### 没有选择的方案
- 继续递归渲染并依赖 `memo`：可以减少部分重复渲染，但无法减少初始 DOM 总量。
- 手写虚拟滚动：需要自行维护滚动偏移、可见区间、overscan、总高度和边界情况，维护成本更高。
- 引入完整树组件库：会带来额外样式与行为迁移，本需求只需要解决性能问题。
- 目录懒加载：能够减少原始数据量，但需要改变接口与缓存模型，超出本次需求范围。

---
## 最终组件结构
改造后由三个文件协作：
```text
ProjectDetailPageContent.tsx
└── ProjectFileTree.tsx
    └── ProjectFileTreeNode.tsx
```

- `ProjectDetailPageContent.tsx` 负责页面数据和业务回调，只在加载成功后把文件树数据交给 `ProjectFileTree`。
- `ProjectFileTree.tsx` 负责展开状态、树形数据扁平化、虚拟列表计算和虚拟行定位。
- `ProjectFileTreeNode.tsx` 只负责单行展示与交互，不再递归渲染子节点，也不再持有目录展开状态。

这种结构符合页面组件的现有风格：页面级专用组件仍放在 `ProjectDetailPage` 目录中，并使用 PascalCase 文件名；没有在 `src/pages` 下额外引入纯 helper 文件或 colocated 测试文件。

---
## 核心数据流
整个渲染链路可以概括为：
```text
完整 GitHub 文件树 nodes
        +
展开目录集合 expandedPaths
        ↓
flattenVisibleProjectFileTree
        ↓
可见节点线性列表 visibleNodes
        ↓
useVirtualizer 计算视口附近的索引
        ↓
只渲染少量 ProjectFileTreeNode
```

展开或收起目录时，只更新 `expandedPaths`。`visibleNodes` 随之重新计算，虚拟化器再根据新的列表长度和滚动位置计算需要挂载的行。

---
## 树形数据扁平化原理
虚拟化器处理的是一维列表，因此需要把“当前可见”的树节点转换为带深度信息的数组：
```ts
type VisibleProjectFileTreeNode = {
  depth: number;
  node: GitHubFileNode;
};
```

`flattenVisibleProjectFileTree` 使用显式栈完成深度优先遍历：
```ts
const pendingNodes = [...nodes]
  .reverse()
  .map((node) => ({ depth: 0, node }));

while (pendingNodes.length > 0) {
  const current = pendingNodes.pop();
  if (!current) continue;

  visibleNodes.push(current);
  const { node, depth } = current;
  if (
    node.type !== "dir" ||
    !expandedPaths.has(node.path) ||
    !node.children
  ) continue;

  for (const child of [...node.children].reverse()) {
    pendingNodes.push({ depth: depth + 1, node: child });
  }
}
```

这里有几个关键点：
- 只有目录存在于 `expandedPaths` 时，才把它的子节点加入待处理栈。
- 根节点深度是 `0`，每进入一层目录，`depth + 1`。
- 子节点先反转再入栈，是因为栈后进先出，这样弹出顺序仍与原始数组一致。
- 使用循环和显式栈，避免用递归函数处理极深目录时占用 JavaScript 调用栈。

扁平结果同时解决两个问题：虚拟化器得到稳定的一维索引，行组件也能用 `depth` 计算视觉缩进。

---
## 展开状态管理
展开目录统一存储为 `Set<string>`，键是节点的完整 `path`：
```ts
const [expansionState, setExpansionState] = useState({
  identity: "",
  paths: new Set<string>(),
});
```

### 为什么使用 Set
- `has(path)` 判断目录是否展开，平均时间复杂度为 O(1)。
- 展开时 `add(path)`，收起时 `delete(path)`，语义直接。
- 文件路径在同一棵仓库树中天然适合作为唯一标识。

React 状态更新时不会原地修改旧集合，而是先复制：
```ts
const nextPaths = new Set(currentPaths);

if (nextPaths.has(path)) nextPaths.delete(path);
else nextPaths.add(path);
```

这保证引用发生变化，React 能可靠识别状态更新。

### 所有节点默认收起
默认展开集合是一个空集合：
```ts
const DEFAULT_EXPANDED_PATHS = new Set<string>();
```

所以首次进入仓库、切换仓库或切换分支时，只显示根层节点。用户点击某个目录后，才逐层展开它的后代。这不仅符合最终交互要求，也显著减少首屏 `visibleNodes` 的规模。

### 为什么状态带有 treeIdentity
同一个组件实例可能因为路由数据更新而展示不同仓库或分支。实现使用 `owner`、`repo` 和 `branch` 生成树身份：
```ts
const treeIdentity = JSON.stringify([owner, repo, branch]);
```

展开状态与身份绑定，可以避免从 `main` 切换到其他分支后错误沿用旧分支路径。身份变化时会执行两件事：
- 展开集合重置为空，所有节点恢复默认收起。
- 滚动容器回到顶部。

### 为什么需要 reconcileExpandedPaths
即使仓库和分支没有变化，文件树也可能刷新。`collectDirectoryPaths` 收集新树中的全部目录路径，`reconcileExpandedPaths` 只保留仍然存在的展开路径。

这避免删除或重命名目录后，状态里长期残留无效路径。`arePathSetsEqual` 用于避免内容未变化时创建新状态，从而减少无意义渲染。

---
## 虚拟列表实现
`ProjectFileTree` 把外层 `div` 作为真实滚动容器：
```tsx
const scrollRef = useRef<HTMLDivElement>(null);

<div
  ref={scrollRef}
  aria-busy={isFetching}
  className="flex-1 overflow-auto p-1.5"
>
  {/* virtual content */}
</div>
```

虚拟化器的配置如下：
```ts
const virtualizer = useVirtualizer({
  count: visibleNodes.length,
  estimateSize: () => PROJECT_FILE_TREE_ROW_HEIGHT,
  getItemKey: (index) => visibleNodes[index]?.node.path ?? index,
  getScrollElement: () => scrollRef.current,
  overscan: 12,
  useFlushSync: false,
});
```

### 配置项解析
- `count`：当前可见节点数量，而不是整棵树的节点数量。
- `estimateSize`：每行固定为 `28px`，让虚拟化器计算总高度和偏移。
- `getItemKey`：优先使用节点路径，展开或收起导致索引移动时仍能维持稳定身份。
- `getScrollElement`：指定左侧文件树容器，而不是浏览器窗口。
- `overscan: 12`：视口上下额外渲染一小段缓冲区，降低快速滚动时出现空白的概率。
- `useFlushSync: false`：避免虚拟化更新强制使用同步 flush，减少 React 19 下不必要的同步工作。

### 总高度与绝对定位
虚拟列表内部先创建一个等于完整可见列表高度的相对定位容器：
```tsx
<div
  className="relative w-full"
  style={{ height: virtualizer.getTotalSize() }}
>
```

浏览器因此能得到正确的滚动条长度。真正挂载的每一行使用绝对定位放到虚拟化器计算出的垂直位置：
```tsx
<div
  className="absolute left-0 top-0 w-full"
  style={{
    height: virtualRow.size,
    top: virtualRow.start,
  }}
>
  <ProjectFileTreeNode {...props} />
</div>
```

假设文件树容器能显示 20 行，DOM 中通常只存在这 20 行加上 overscan 缓冲，而不是存在数千或数万个节点。

---
## 单行节点源码解析
`ProjectFileTreeNode` 从递归树组件变成受控的单行组件。它接收三个与树状态有关的属性：
- `depth`：决定左侧缩进。
- `expanded`：决定目录箭头方向和 `aria-expanded`。
- `onToggleDirectory`：把展开动作交给父级统一更新。

### 固定高度与缩进
行高和缩进常量如下：
```ts
export const PROJECT_FILE_TREE_ROW_HEIGHT = 28;
const FILE_TREE_INDENT_SIZE = 16;
const FILE_TREE_BASE_PADDING = 8;
```

节点行通过深度计算缩进：
```tsx
style={{
  height: PROJECT_FILE_TREE_ROW_HEIGHT,
  paddingLeft: FILE_TREE_BASE_PADDING + depth * FILE_TREE_INDENT_SIZE,
}}
```

固定行高非常重要，因为虚拟化器的尺寸估算必须与实际布局一致。如果以后给某些节点增加换行副标题或动态高度，需要改用测量元素的方案，不能只修改 CSS。

### memo 的作用
组件使用 `memo` 包装。虚拟化已经控制了挂载数量，`memo` 进一步避免父组件更新时，对属性没有变化的已挂载行重复执行渲染。

### 点击和键盘行为
- 点击目录：调用 `onToggleDirectory(path)`。
- 点击文件：调用 `onSelectFile(path)`。
- `Enter` 或空格：执行与点击相同的行为。
- 目录收起时按 `ArrowRight`：展开目录。
- 目录展开时按 `ArrowLeft`：收起目录。
- 菜单按钮通过 `stopPropagation()` 阻止触发节点的选择或展开。

键盘处理先检查 `event.target === event.currentTarget`，避免焦点在行内菜单按钮时，按键事件冒泡后误触发行行为。

### 菜单行为
每一行仍保留“扫描文件或目录”和“在 GitHub 中打开”两个操作。菜单打开时注册 `mousedown` 监听器，点击菜单外部后关闭，并在 Effect 清理阶段移除监听器。

虚拟列表的一个自然行为是：当菜单所在行滚出 overscan 范围时，该行会卸载，菜单也会随之关闭。这与虚拟化模型一致。

---
## 可访问性改造
改造前节点使用通用的 `role="button"`。改造后补充了树组件语义：
- 容器使用 `role="tree"`。
- 每行使用 `role="treeitem"`。
- `aria-level={depth + 1}` 表示层级。
- 目录使用 `aria-expanded` 表示展开状态。
- 文件使用 `aria-selected` 表示选中状态。
- 滚动容器通过 `aria-busy` 暴露后台刷新状态。
- 行为菜单使用 `aria-haspopup="menu"`、`aria-expanded` 和 `role="menuitem"`。

当前实现让每个虚拟行都可以通过 `tabIndex={0}` 获取焦点，并支持基础的左右方向键。若后续要实现完整 WAI-ARIA Tree Pattern，还可以继续增加上下方向键移动、Home、End，以及 roving tabindex。它们不是本次性能需求的必要条件。

---
## 页面集成
`ProjectDetailPageContent` 不再直接遍历根节点并递归渲染 `ProjectFileTreeNode`，而是把树数据和业务回调交给新的容器组件：
```tsx
<ProjectFileTree
  branch={branch}
  isFetching={treeFetching}
  nodes={tree}
  owner={owner}
  repo={repo}
  selectedPath={selectedPath}
  onScan={handleQueuedScan}
  onSelectFile={handleSelectFile}
/>
```

页面继续负责加载态和错误态，`ProjectFileTree` 只在数据可用时挂载。这样虚拟化细节不会泄漏到页面主体，页面也不需要知道扁平列表、行高或 overscan。

---
## 复杂度与性能收益
设完整文件树节点数为 N，当前展开后可见节点数为 V，视口可容纳行数为 W，目录数为 D。

- `collectDirectoryPaths`：树数据变化时 O(N)，空间 O(D)。
- `flattenVisibleProjectFileTree`：展开状态变化时 O(V)，结果空间 O(V)。
- 虚拟 DOM 与真实 DOM：约 O(W + overscan)，不再是 O(V)。
- 展开状态：O(E)，E 是当前展开目录数量。
- 原始 GitHub 树数据：仍是 O(N)。

默认全部收起时，V 通常只等于根层节点数；用户逐层展开后，V 才逐步增加。即使 V 很大，虚拟化也把实际挂载的行数限制在视口附近，因此滚动和 React 协调成本更稳定。

### 性能收益来自两层限制
- 可见性限制：收起目录的后代不会进入 `visibleNodes`。
- 视口限制：进入 `visibleNodes` 的节点，也只有视口附近的少量行会生成组件和 DOM。

只做其中一层都不够：仅默认收起无法保证用户展开大目录后的滚动性能；仅虚拟化但默认全展开，会让首次扁平化列表仍包含整棵树，并失去更轻量的初始体验。

---
## 实现过程
本需求以 `develop` 为基线，在 `feature/responsive-file-tree` 分支完成。

### 建立实现边界
先确认只增加 `@tanstack/react-virtual`，不引入完整树组件库，也不扩展后端接口。

### 提取树容器职责
新增 `ProjectFileTree.tsx`，把文件树的展开状态、可见节点计算和虚拟化从页面与节点行中独立出来。

### 将节点改为受控单行组件
删除节点内部的递归 children 渲染和本地 `expanded` 状态，改为由父组件传入 `depth`、`expanded` 和 `onToggleDirectory`。

### 建立可见节点模型
实现迭代式深度优先遍历，只展开 `expandedPaths` 中目录的子节点，并保存每一行的深度。

### 接入虚拟化器
使用固定 `28px` 行高、路径稳定 key、`12` 行 overscan 和绝对定位渲染虚拟行。

### 重置与校准状态
使用仓库与分支身份隔离展开状态；树数据刷新时移除失效路径；切换身份时清空展开状态并滚动到顶部。

### 调整默认行为
将默认展开集合设为空，使所有目录初始收起。

### 对齐项目结构
页面专用组件保留在 `src/pages/ProjectDetailPage` 中，使用 PascalCase 文件名；没有把测试文件或纯 helper 文件放进当前没有此惯例的页面目录。

### 完成验证与提交
执行应用质量检查和生产构建：
```powershell
Set-Location apps/app
bun run quality
bun run build
```

质量检查中的 TypeScript、oxlint 和 Vitest 均通过；构建成功。最终提交为：
```text
4173387 feat(COD-220): virtualize large repository file trees
```

PRD 与计划文档位于被 Git 忽略的 `docs/` 路径，没有进入提交。

---
## 关键设计决策
### 为什么节点状态必须提升
虚拟行会随着滚动被卸载。如果展开状态仍存放在行组件内部，行离开视口后状态可能丢失，而且父级无法计算完整的可见列表。把状态提升到 `ProjectFileTree` 后，虚拟行只是状态的投影，挂载与卸载不会影响目录展开结果。

### 为什么 key 使用 path 而不是 index
展开目录会在列表中间插入后代，收起目录会删除一段节点。若使用 index，后续大量行的身份都会错位。使用稳定路径可以让 React 与虚拟化器正确关联节点。

### 为什么固定行高
文件树每一行布局一致，固定高度可以直接计算偏移，无需运行时测量，逻辑更简单、滚动更稳定。代价是节点内容必须单行截断，不能随内容自动增高。

### 为什么默认收起
默认收起同时改善交互聚焦和首屏性能。大型仓库往往包含多个顶层目录，用户可以按需进入目标路径，而不是在页面加载时承担整棵树的渲染成本。

---
## 已知限制与后续方向
- 完整文件树仍一次性获取并保存在内存中，超大型仓库可以进一步做目录级懒加载。
- 扁平化在展开状态变化时同步执行；若单次展开产生极大量直接可见节点，可考虑缓存子树结果或使用并发调度。
- 当前固定行高依赖 `PROJECT_FILE_TREE_ROW_HEIGHT` 与实际 CSS 始终一致。
- 当前实现提供基础树键盘交互，但还不是完整的 WAI-ARIA Tree Pattern。
- 行内菜单会随虚拟行卸载而关闭；若产品希望菜单脱离滚动行存在，可改为 Portal。
- `collectDirectoryPaths` 每次树对象变化都会遍历完整树。如果数据层频繁返回结构相同但引用不同的新数组，可以在数据层稳定引用或用版本标识减少重复计算。

---
## 涉及源码
- `apps/app/src/pages/ProjectDetailPage/ProjectFileTree.tsx`：展开状态、可见节点扁平化、虚拟化渲染。
- `apps/app/src/pages/ProjectDetailPage/ProjectFileTreeNode.tsx`：受控单行节点、菜单、键盘和 ARIA。
- `apps/app/src/pages/ProjectDetailPage/ProjectDetailPageContent.tsx`：加载态、错误态和树组件接入。
- `apps/app/package.json`：新增 `@tanstack/react-virtual`。
- `bun.lock`：依赖锁定结果。

---
## 总结
COD-220 的核心不是简单地给递归组件加 `memo`，而是改变渲染模型：先由集中式展开状态计算当前可见节点，再将树形结构转换为一维列表，最后只渲染视口附近的固定高度行。

这套设计把“树的业务语义”和“列表的渲染机制”分开：`expandedPaths` 与 `depth` 保留树结构，`visibleNodes` 与 `useVirtualizer` 负责高效展示。默认全部收起进一步缩小首屏可见集合，从而让大型仓库的文件树在不改变现有业务能力的前提下保持更稳定的响应速度。
