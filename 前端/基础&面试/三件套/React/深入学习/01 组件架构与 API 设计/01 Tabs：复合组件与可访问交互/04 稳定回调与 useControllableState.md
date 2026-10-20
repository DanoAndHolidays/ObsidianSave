# 04 稳定回调与 useControllableState
> Last Format Time：9/16/2026 19:24:52

> Last Format Time：2026-08-28
> Status：已完成
> 笔记说明：稳定回调、受控/非受控状态和 useControllableState 的设计边界。

---
## Render 阶段与 ref
通常不应在 render 期间读取或写入 `ref.current`。React 期望组件 render 保持纯函数特征；render 可能被重复、暂停或丢弃，而 ref 修改不会随被丢弃的 render 自动回滚。可预测的一次性延迟初始化是官方文档明确给出的例外。

需要保存“最近一次已经提交的值”时，应在 effect 或 layout effect 中同步 ref：
```tsx
function useLatest<T>(value: T) {
  const ref = useRef(value);

  useLayoutEffect(() => {
    ref.current = value;
  }, [value]);

  return ref;
}
```

---
## 稳定回调与最新值
`useCallback(fn, [])` 可以保持函数引用稳定，但函数会闭包捕获首次 render 的值。若回调需要稳定 identity，同时必须读取最近一次已提交的值，可以组合 `useLatest`：
```tsx
function useStableCallback<TArgs extends unknown[], TResult>(
  callback: (...args: TArgs) => TResult,
) {
  const callbackRef = useLatest(callback);

  return useCallback((...args: TArgs) => {
    return callbackRef.current(...args);
  }, []);
}
```

这个模式适合需要稳定订阅函数或事件回调的场景；普通组件逻辑仍应优先使用正确的依赖数组，而不是用 ref 绕过依赖检查。

---
## 在 `useControllableState` 中的用途
受控组件通常需要：
- 根据 `value !== undefined` 判断当前是否受控
- 非受控时更新内部 state
- 两种模式都调用最新的 `onChange`
- 开发环境中提示受控与非受控模式切换

稳定回调可以减少 Context value 或订阅 API 因函数 identity 变化产生的额外更新，但不能替代受控状态的唯一数据源设计。

---
## 参考资料
- [React：useRef](https://react.dev/reference/react/useRef)
- [Oxc：react/refs](https://oxc.rs/docs/guide/usage/linter/rules/react/refs.html)
