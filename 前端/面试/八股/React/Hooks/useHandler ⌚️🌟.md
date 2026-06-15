# useHandler
> Last Format Time：6/15/2026 10:50:12

先点明核心作用：
`useHandler` 专门解决 React 里**函数频繁重新创建、useEffect/子组件不必要重复执行、闭包陷阱**问题，目标是：
1. 返回一个永远不变引用的稳定处理函数
2. 函数内部总能拿到最新的 state/props，不会被旧闭包捕获

---
## 前置知识
### useRef 两大特性
- `.current` 可变，修改不会触发组件重渲染；
- ref 对象本身在组件整个生命周期**只初始化一次**，引用永远不变。

### useCallback 特性
依赖数组不变，返回的函数引用就永远不变；依赖变了才生成新函数。

### 经典闭包陷阱场景（为什么需要这个钩子）
```jsx
const [count, setCount] = useState(0);

const onClick = () => {
  console.log(count); // 永远打印初始0，闭包锁住了旧count
  setCount(count + 1);
};

useEffect(() => {
  const timer = setInterval(onClick, 1000);
  return () => clearInterval(timer);
}, []); // 依赖空数组，onClick永远是第一次创建的旧函数
```

定时器里永远只能拿到初始 `count=0`，这就是闭包陷阱，两个 `useHandler` 都是为修复这个问题而生。

---
## useCallback + ref 版本
```jsx
import { useRef, useCallback } from 'react';

const useHandler = (cb) => {
    // 1. ref存回调，ref对象终身不变
    const cbRef = useRef(cb);
    
    // 2. 每次组件重新渲染，把最新传入的cb覆盖ref.current
    cbRef.current = cb;

    // 3. useCallback依赖空数组，stableHandler引用永久不变
    const stableHandler = useCallback((...args) => {
        // 执行时取ref里最新的cb，绕过闭包
        return cbRef.current(...args);
    }, []);

    return stableHandler;
};
```

### 分步讲解
1. `cbRef = useRef(cb)`
组件第一次渲染，把传入的回调函数存入 `cbRef.current`；ref 对象本身不会变。

2. 每次渲染执行 `cbRef.current = cb`
只要组件重渲染，父组件传进来的新 `cb` 会立刻覆盖 ref 里旧值。
ref 更新 `.current` **不会触发重渲染**，只是内存里替换了函数。

3. `useCallback(()=>{}, [])`
依赖为空，`stableHandler` 只会在组件挂载时创建**唯一一次**，后续所有渲染返回的都是同一个函数引用。

4. 调用 `stableHandler(实参)`
不会执行当初闭包绑定的旧函数，而是读取最新存在 ref 里的 `cbRef.current` 执行，自动拿到最新 state/props。

### 完整示例代码（可直接复制运行）
```jsx
import { useState, useEffect, useRef, useCallback } from 'react';

// 第一个版本
const useHandler = (cb) => {
  const cbRef = useRef(cb);
  cbRef.current = cb;

  const stableHandler = useCallback((...args) => {
    return cbRef.current(...args);
  }, []);

  return stableHandler;
};

export default function Demo1() {
  const [count, setCount] = useState(0);

  // 普通写法：每次渲染都会生成全新函数
  // const normalClick = () => setCount(prev => prev + 1);

  // 稳定函数，引用永远不变
  const stableClick = useHandler(() => {
    console.log('最新count：', count);
    setCount(count + 1);
  });

  // 定时器只需要挂载时注册一次，不会重复创建定时器
  useEffect(() => {
    const timer = setInterval(stableClick, 1000);
    return () => clearInterval(timer);
  }, [stableClick]); // stableClick引用永久不变，effect只执行一次

  return <div>计数：{count}</div>;
}
```

运行效果：每秒正常+1，控制台打印实时最新count，没有闭包卡死问题。

---
## 纯 useRef 版本（无 useCallback）
```jsx
const useHandler = (cb) => {
  const cbRef = useRef(cb);
  // 每次渲染同步更新为最新回调
  cbRef.current = cb;

  // handlerRef只初始化一次，里面固定读取cbRef.current
  const handlerRef = useRef((...args) => cbRef.current(...args));
  return handlerRef.current;
};
```

### 分步拆解
1. `cbRef.current = cb`：和上个版本完全一致，每次渲染同步更新最新回调。
2. `handlerRef = useRef((...args) => cbRef.current(...args))`
组件**仅挂载时创建一次 handlerRef**，ref 内部存储了一个固定外壳函数：
外壳函数本身永远不变，外壳内部不去捕获外面的 `cb`，而是每次调用都去读可变的 `cbRef.current`。
3. `return handlerRef.current`
返回这个外壳函数，函数引用终身不变，等价于上一个版本 `useCallback` 的效果。

### 同场景示例
```jsx
import { useState, useEffect, useRef } from 'react';

// 第二个纯ref版本
const useHandler = (cb) => {
  const cbRef = useRef(cb);
  cbRef.current = cb;

  const handlerRef = useRef((...args) => cbRef.current(...args));
  return handlerRef.current;
};

export default function Demo2() {
  const [count, setCount] = useState(0);

  const stableClick = useHandler(() => {
    console.log('最新count：', count);
    setCount(count + 1);
  });

  useEffect(() => {
    const timer = setInterval(stableClick, 1000);
    return () => clearInterval(timer);
  }, [stableClick]);

  return <div>计数：{count}</div>;
}
```

运行结果和第一个版本一模一样，定时器正常累加，无闭包陷阱。

---
## 子组件 memo 场景
父组件每次渲染都会生成新函数，传给 memo 子组件会导致子组件重复渲染，用 `useHandler` 完美解决：
```jsx
import { useState, memo, useRef } from 'react';

const useHandler = (cb) => {
  const cbRef = useRef(cb);
  cbRef.current = cb;
  const hRef = useRef((...a) => cbRef.current(...a));
  return hRef.current;
};

// 子组件memo缓存，props不变就不重渲染
const Child = memo(({ onClick }) => {
  console.log('子组件渲染了');
  return <button onClick={onClick}>子组件按钮</button>;
});

export default function Parent() {
  const [num, setNum] = useState(0);

  // 稳定函数，引用永远不变
  const handleChildClick = useHandler(() => {
    alert('当前num：' + num);
  });

  return (
    <div>
      <p>父组件num：{num}</p>
      <button onClick={() => setNum(num + 1)}>父组件+1</button>
      <Child onClick={handleChildClick} />
    </div>
  );
}
```

效果：点击父组件按钮更新 `num`，父组件重渲染，但**子组件不会打印渲染日志**，因为传给子组件的函数引用始终没变；点击子按钮依然能拿到最新的 `num`。