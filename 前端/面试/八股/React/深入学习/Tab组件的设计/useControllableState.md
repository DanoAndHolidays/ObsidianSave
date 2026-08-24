# useControllableState
> Last Format Time：8/24/2026 15:30:16

---
## 不能在渲染过程中调用`ref.current`的赋值
[Oxc：react/refs](https://oxc.rs/docs/guide/usage/linter/rules/react/refs.html)

Validates correct usage of refs: `ref.current` may not be read or written during render, only in event handlers and effects.

在需要稳定的函数引用的场景下，使用`useCallback(( ... )=>{ ... }, [])`，一个空依赖数组，可以保持函数引用的稳定，但是拿不到最新的值，这里可以使用ref来拿取。
