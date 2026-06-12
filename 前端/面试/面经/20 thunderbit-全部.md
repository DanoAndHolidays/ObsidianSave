# 20 thunderbit-全部
> Last Format Time：6/12/2026 21:03:57

*6/12/26 【理由】原文将「一面」「二面」「逐行拆解两个 useHandler 钩子」并列写成 H1，违反 H1 唯一原则。
原内容：`# 一面` / `# 二面` / `# 逐行拆解两个 useHandler 钩子，附带完整可运行示例`*

## 一面
电话面试：
- react卸载的问题
- 箭头函数与普通函数的区别
- callapplybind的区别

---
## 二面
6/11/26

### useHandler 实现题
```js
const A = (props) => {
    const [state, setState] = useState({ b: 1 })
    const handler = useHandler((event) => {
        console.log(props.a)
        console.log(state.b)
    })
    return <button onClick={handler}>click me</button>
}

// handler 引用稳定不变，每次执行获取到的 props、state 都是最新的

const useHandler = (cb) => {
    // 在这里实现你的代码
}
```

### 删除数组中多个元素
```js
// 通过函数删除一个数组中多个元素，传入的参数为目标数组，以及索引（多个索引，数组形式）。
// [2,4,5,6] [1,3] => [2,5]

const remove = (list, indexList) => {
    if (list.length === 0) return []
    return list.filter((value, index) => {
        if (indexList.indexOf(index) !== -1) {
            return false
        }
        return true
    })
}
console.log(remove([2, 4, 5, 6], [1, 3]))
console.log(remove([2, 4, 5], [1, 2]))
```

### 异步执行顺序
```js
async function async1() {
    // 1
    console.log('async1 start')

    await async2()

    // 5
    console.log('async1 end')

    Promise.resolve().then(() => {
        // 7
        console.log('after async1 end')
    })
}

async function async2() {
    // 2
    console.log('async2')
}

// 0
console.log('script start')

// 8
setTimeout(() => console.log('setTimeout'), 0)

async1()

new Promise((resolve) => {
    // 3
    console.log('promise1')
    resolve()

}).then(() => {
    // 6
    console.log('promise2')

})

// 4
console.log('script end')
```

---
## 逐行拆解两个 useHandler 钩子（附带完整可运行示例）
先点明核心作用：
`useHandler` 专门解决 React 里**函数频繁重新创建、useEffect/子组件不必要重复执行、闭包陷阱**问题，目标是：
1. 返回一个永远不变引用的稳定处理函数
2. 函数内部总能拿到最新的 state/props，不会被旧闭包捕获

### 前置知识铺垫（必须先懂）
##### useRef 两大特性
- `.current` 可变，修改不会触发组件重渲染；
- ref 对象本身在组件整个生命周期**只初始化一次**，引用永远不变。

##### useCallback 特性
依赖数组不变，返回的函数引用就永远不变；依赖变了才生成新函数。

##### 经典闭包陷阱场景（为什么需要这个钩子）
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

### 第一个实现：useCallback + ref 版本
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

##### 分步讲解
1. `cbRef = useRef(cb)`
组件第一次渲染，把传入的回调函数存入 `cbRef.current`；ref 对象本身不会变。

2. 每次渲染执行 `cbRef.current = cb`
只要组件重渲染，父组件传进来的新 `cb` 会立刻覆盖 ref 里旧值。
ref 更新 `.current` **不会触发重渲染**，只是内存里替换了函数。

3. `useCallback(()=>{}, [])`
依赖为空，`stableHandler` 只会在组件挂载时创建**唯一一次**，后续所有渲染返回的都是同一个函数引用。

4. 调用 `stableHandler(实参)`
不会执行当初闭包绑定的旧函数，而是读取最新存在 ref 里的 `cbRef.current` 执行，自动拿到最新 state/props。

##### 完整示例代码（可直接复制运行）
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

### 第二个实现：纯 useRef 版本（无 useCallback）
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

##### 分步拆解
1. `cbRef.current = cb`：和上个版本完全一致，每次渲染同步更新最新回调。
2. `handlerRef = useRef((...args) => cbRef.current(...args))`
组件**仅挂载时创建一次 handlerRef**，ref 内部存储了一个固定外壳函数：
外壳函数本身永远不变，外壳内部不去捕获外面的 `cb`，而是每次调用都去读可变的 `cbRef.current`。
3. `return handlerRef.current`
返回这个外壳函数，函数引用终身不变，等价于上一个版本 `useCallback` 的效果。

##### 同场景示例
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

### 两个实现横向对比
| 方案 | 依赖API | 原理 | 优缺点 |
|------|--------|------|--------|
| useCallback + ref | useRef + useCallback | 用useCallback锁定外层函数引用不变，内部跳转ref取最新cb | 语义更贴合React官方API，可读性强 |
| 双层useRef | 两个useRef | 外层ref存最新业务回调，内层ref存固定转发外壳函数 | 少一个Hook调用，体积更小，底层原理更纯粹 |

##### 共同点（核心逻辑完全一致）
1. 都通过 ref 的可变 `.current` 绕开 React 渲染闭包；
2. 返回的处理函数引用永久稳定，不会重复生成；
3. 无论组件重渲染多少次，调用时都能拿到最新的 state、props；
4. 放到 `useEffect` 依赖数组、传给 memo 子组件，都不会触发多余执行/重渲染。

### 再举一个子组件 memo 场景例子（实际业务高频用法）
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

### 总结一句话通俗解释
两个钩子都是搞了一层「中间人仓库（ref.current）」：
1. 每次渲染都把最新的业务函数放进仓库；
2. 对外只暴露一个永远不变的固定转发函数；
3. 别人调用这个固定函数时，它自动去仓库拿最新的真实函数执行；
既保证了函数引用稳定，又彻底避开了 React 闭包陷阱。
只是一个用 `useCallback` 做固定外壳，一个用第二层 `useRef` 做固定外壳，底层思路没有区别。
