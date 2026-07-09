# hook 调用顺序不一致
这是 React 的一条硬性规则：每次渲染时，hooks 的调用数量、调用顺序必须完全一致。

React 内部用一个链表来追踪每个组件的 hooks 状态。它通过调用顺序来匹配每次渲染时哪个 hook，对应哪份状态，而不是通过名称或标识符。一旦某次渲染跳过一个 hook，链表索引就全错了。

出问题前的代码结构是：

```ts
  export const CrateDetailPageContent = function () {
    // hooks 1-12: useOne, useList, useBreadcrumb, useUpdate, useDelete,
    //            useEffect, useCallback × 6
    // 总共 12 个 hook 调用

    if (!crate) return <LoadingState className="py-20" />;  // ← 早期 return

    // 第 13 个 hook — 只有 crate 不为 null 时才会执行
    const boundArchetypes = useMemo(() => { ... }, [...]);

    return <div>...</div>;
  };
```

  第一次渲染（数据未加载，crate === null）：
  - React 执行 12 个 hooks → 遇到早期 return → 13 号槽位为空

  第二次渲染（数据返回，crate !== null）：
  - React 执行 12 个 hooks → 跳过早期 return → 执行第 13 个 hook (useMemo)

  React 发现第二次渲染的 hook 数量（13）与第一次（12）不一致，直接抛出：

  ▎ Rendered more hooks than during the previous render.
  
修复方式

  把 useMemo 及它所依赖的普通变量全部移到早期 return 之前：

  export const CrateDetailPageContent = function () {
    // ... 12 hooks ...

    // 普通变量（null-safe）
    const ext = (crate as Record<string, unknown>) ?? {};

    // 第 13 个 hook — 现在每次渲染都执行
    const boundArchetypes = useMemo(() => { ... }, [...]);

    // 早期 return 现在在所有 hook 之后，安全
    if (!crate) return <LoadingState className="py-20" />;

    return <div>...</div>;
  };

  当 crate 为 null 时，useMemo 的结果是一个空数组，值没被用到，但 hook 本身被调用了，链表索引保持了稳定。

  ---
  以后要注意的点

  1. 早期 return 只能放在最后一个 hook 之后

  任何 if (condition) return <JSX /> 的上面都不允许再有 useXxx() 调用。写组件时先铺完所有 hooks，再把条件渲染放在它们下面。

  2. 不要在任何条件分支内调用 hook

  // ❌ 错误
  if (someCondition) {
    useEffect(() => { ... }, []);  // 第二次渲染可能不执行
  }

  // ✅ 正确 — 把条件放进 hook 内部
  useEffect(() => {
    if (someCondition) { ... }
  }, [someCondition]);

  3. 不要在循环内调用 hook

  hook 调用次数必须固定。循环的迭代次数可能在渲染间变化。

  4. oxlint 的 react-hooks 规则有助于预防，但不完全可靠

  我们项目的 oxlint 配置已经开启了 react-hooks 相关规则。但它的静态分析有时无法追踪到通过变量间接导致的条件分歧（比如 crate 来自 hook
  返回值，lint 不一定能推断它何时为 null）。所以最终还是靠代码审查和自觉遵守这条规则。

  5. 写组件时先铺 hooks，后写 JSX 的逻辑顺序是个好习惯

  function Component() {
    // ── 第一层：路由参数、全局状态 ──
    // ── 第二层：数据获取 hooks（useOne / useList / useQuery）──
    // ── 第三层：派生计算（useMemo）──
    // ── 第四层：回调（useCallback）──
    // ── 第五层：副作用（useEffect）──
    // ── 第六层：条件渲染 / 早期 return ──  ← 永远最后
    // ── 第七层：主 JSX ──
  }

  遵循这个分层，早期 return 不可能插到 hook 前面去。