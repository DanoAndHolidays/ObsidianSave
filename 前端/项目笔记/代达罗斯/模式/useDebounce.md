# useDebounce
> Last Format Time：7/14/2026 20:56:57

这里和普通的防抖函数不同，这里是要将防抖通过react hooks来实现的：

这里的是在项目中AI写的，具体的来看这里的ref是不必要的，因为使用const来声明的变量在这里是可以的：
```ts
import { useState, useEffect, useRef } from "react";

export function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);
  const timerRef = useRef<ReturnType<typeof setTimeout>>(undefined);

  useEffect(() => {
    timerRef.current = setTimeout(() => setDebounced(value), delay);

    return () => clearTimeout(timerRef.current);
  }, [value, delay]);

  return debounced;
}

```

**为什么 `useRef` 不需要？** `useEffect` 的 cleanup 函数通过闭包已经捕获了当次 effect 创建的 `timer`，每次 `value`/`delay` 变化时旧 effect 的 cleanup 会精确清除**那个** timer，新 effect 创建新 timer。整个过程不需要跨渲染持久化 timer 的引用：
```ts
import { useState, useEffect } from "react";

export const useDebounce = function<T>(value: T, delay: number = 500): T {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);

    return () => clearTimeout(timer);
  }, [value, delay]);

  return debounced;
};

```

个人默写：
```ts
import { useEffect, useState } from "react"

export const useDebounce<T> = (value: T, time: number = 300): T => {
	const [ debounced, setDebounced ] = useState(value)
	useEffect(() => {
		const timer = setTimeout(() => setDebounce(value), time)
		return () => clearTimeount(timer) 
	}, [ value, time ])

	return debounced
} 

```