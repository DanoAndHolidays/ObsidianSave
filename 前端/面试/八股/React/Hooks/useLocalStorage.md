# useLocalStorage
> Last Format Time：6/15/2026 11:46:35

---
## 代码
```tsx
import { useState, useEffect } from 'react';

function useLocalStorage(key, initialValue) {
  // 1. 使用函数式初始化，避免每次渲染都读取 localStorage
  const [storedValue, setStoredValue] = useState(() => {
    try {
      // SSR 兼容：判断 window 是否存在
      if (typeof window === 'undefined') return initialValue; 
      
      const item = window.localStorage.getItem(key);
      // 如果本地有值则解析，否则返回默认值
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.warn(`读取 ${key} 失败:`, error);
      return initialValue;
    }
  });

  // 2. 监听状态变化，自动同步到 localStorage
  useEffect(() => {
    try {
      if (typeof window !== 'undefined') {
        window.localStorage.setItem(key, JSON.stringify(storedValue));
      }
    } catch (error) {
      console.error(`保存 ${key} 失败:`, error);
    }
  }, [key, storedValue]);

  return [storedValue, setStoredValue];
}
```

---
## 与lodash.debounce()的区别
这两种方式代表了 React 生态和传统 JavaScript 中两种截然不同的防抖设计哲学。我们可以从以下几个维度来深入剖析它们的区别：

### 核心机制的差异
- **`useDebounce`（状态驱动）**：正如你所说，它是通过对**状态（State）本身**进行防抖来实现的。它并不直接包裹你的业务逻辑函数，而是拦截了数据的更新。只有当数据在指定延迟内没有发生变化时，才会触发 `setState`。业务逻辑（如发起请求）通常放在 `useEffect` 中，通过监听这个“防抖后的状态”来触发。
- **`lodash.debounce`（函数驱动）**：它是通过**闭包（Closure）**将一个普通函数包裹起来，返回一个新的函数。这个新函数内部维护了自己的定时器和状态。当你调用这个新函数时，它会在内部延迟执行原始的业务逻辑函数。

### 在 React 中的典型用法对比
- **`useDebounce` 的用法**：通常用于“数据流”的防抖。你只需要把输入框的值传给它，然后在 `useEffect` 中监听它的返回值即可。这种写法非常符合 React 的声明式编程范式。
- **`lodash.debounce` 的用法**：通常用于“事件处理函数”的防抖。你需要把它包裹住你的回调函数（如 `onChange` 或 `onClick`），并且**必须**配合 `useCallback` 或 `useMemo` 使用，以确保返回的防抖函数引用是稳定的。如果在组件函数体内直接调用 `_.debounce`，每次渲染都会创建一个新的防抖函数，导致内部定时器不断被重置，防抖就会彻底失效。

### 适用场景的侧重
- **`useDebounce`**：更适合处理**需要最终状态**的场景，比如搜索框输入、表单校验、窗口大小调整后的重新布局等。它天然与 React 的状态更新机制绑定。
- **`lodash.debounce`**：除了能处理上述场景，还更适合处理**纯函数调用**的防抖。此外，Lodash 的实现更为底层和强大，它支持 `leading`（首次立即执行）、`trailing`（结束后执行）、`maxWait`（最大等待时间，这本质上就是节流）以及 `cancel` / `flush` 等高级控制能力，这些是简单的 `useDebounce` 难以直接提供的。

**总结来说：** `useDebounce` 是**“让数据等一等再更新”**，它是 React 状态管理思维的延伸；而 `lodash.debounce` 是**“让函数等一等再执行”**，它是经典 JavaScript 性能优化手段在 React 中的应用。两者没有绝对的优劣，只有适用场景的不同。