# useCallback
> Last Format Time：9/16/2026 19:24:51

`useCallback(..., [])` 空依赖会使React 会一直返回第一次创建出来的那个函数引用，以后的渲染不会更新


如果一个函数只在 Effect 中使用，优先把它定义到 Effect 内部，而不是为了依赖数组专门使用 `useCallback`。

