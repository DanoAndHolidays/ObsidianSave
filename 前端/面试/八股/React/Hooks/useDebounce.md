# useDebounce
> Last Format Time：6/15/2026 10:50:12

---
## code
```tsx
import { useState, useEffect } from 'react';

function useDebounce(value, delay = 500) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    // 1. 设置定时器，在 delay 毫秒后更新防抖值
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    // 2. 清理函数：如果在 delay 之前有新值输入，取消之前的定时器
    // 这是防抖的核心机制
    return () => {
      clearTimeout(timer);
    };
  }, [value, delay]); // 依赖原始值和延迟时间

  return debouncedValue;
}
```

---
## 使用
```tsx
function SearchInput() {
  const [query, setQuery] = useState('');
  // 延迟 500ms 更新
  const debouncedQuery = useDebounce(query, 500); 

  useEffect(() => {
    if (debouncedQuery.trim()) {
      console.log('发起搜索请求:', debouncedQuery);
      // 在这里执行 fetch 请求...
    }
  }, [debouncedQuery]); // 注意：依赖的是防抖后的值

  return (
    <input
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      placeholder="输入搜索关键词..."
    />
  );
}
```