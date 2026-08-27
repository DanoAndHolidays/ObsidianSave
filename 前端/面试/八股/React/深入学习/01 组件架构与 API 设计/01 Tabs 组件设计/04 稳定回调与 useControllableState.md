# 04 稳定回调与 useControllableState
> Last Format Time：8/27/2026 15:20:25

> Last Format Time：8/27/2026
> 笔记说明：稳定回调、受控/非受控状态和 useControllableState 的设计边界。

---
## Render 阶段与 ref
通常不应在 render 期间读取或写入 `ref.current`。React 期望组件 render 保持纯函数特征；render 可能被重复、暂停或丢弃，而 ref 修改不会随被丢弃的 render 自动回滚。可预测的一次性延迟初始化是官方文档明确给出的例外。〔CR-001〕

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

这个模式适合需要稳定订阅函数或事件回调的场景；普通组件逻辑仍应优先使用正确的依赖数组，而不是用 ref 绕过依赖检查。〔CR-002〕

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

---
## 内容审核变更记录
### CR-001｜事实纠错
- 日期：8/25/2026
- 位置：`Render 阶段与 ref`
- 原内容：`ref.current` 不得在 render 中读写，只能在事件处理器和 effects 中使用。
- 调整后：说明 render 阶段通常不应读写 ref，并保留可预测的一次性延迟初始化例外；已提交值应在 effect 或 layout effect 中同步。
- 原因：原描述过于绝对，遗漏了 React 官方文档允许的一次性初始化例外，也没有说明并发 render 下修改 ref 的风险。
- 依据：[React：useRef](https://react.dev/reference/react/useRef)
### CR-002｜补充说明
- 日期：8/25/2026
- 位置：`稳定回调与最新值`
- 原内容：空依赖的 `useCallback` 引用稳定但拿不到最新值，可以使用 ref。
- 调整后：补充 `useLatest` 与稳定回调的完整实现，并明确普通逻辑仍应优先使用正确依赖数组。
- 原因：原内容没有说明 ref 应在何时同步，也容易被理解成用 ref 普遍规避 Hook 依赖。
- 依据：[React：useRef](https://react.dev/reference/react/useRef)

