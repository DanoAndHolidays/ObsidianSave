# AbortController ⌚️
> Last Format Time：6/12/2026 19:39:32

在 JavaScript 中，`AbortController` 是一个用于中止一个或多个异步操作（如 `fetch` 请求、事件监听器等）的控制器对象。它通过关联的 `AbortSignal` 对象来传递中止信号。

## 核心使用步骤
1. **创建控制器**：使用 `new AbortController()` 创建一个实例。
2. **获取信号**：通过控制器的 `.signal` 属性获取 `AbortSignal` 对象。
3. **传递信号**：将信号传递给支持中止的异步 API（例如 `fetch` 的 `signal` 选项）。
4. **触发中止**：在需要的时候调用控制器的 `.abort()` 方法，所有接收该信号的异步操作都会被取消。

下面通过几个常见的实际场景来具体说明：

---
## 中止 Fetch 请求
这是 `AbortController` 最常见的应用场景。当用户取消操作或请求超时时，可以避免不必要的网络资源浪费。

```javascript
const controller = new AbortController();
const signal = controller.signal;

// 发起 fetch 请求，传入 signal
fetch('https://api.example.com/data', { signal })
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => {
    // 捕获中止错误
    if (error.name === 'AbortError') {
      console.log('请求已被中止');
    } else {
      console.error('请求失败:', error);
    }
  });

// 5秒后自动中止请求
setTimeout(() => {
  controller.abort();
}, 5000);
```

---
## 自动清理事件监听器
在传统开发中，移除事件监听器需要手动调用 `removeEventListener`。使用 `AbortController` 可以非常优雅地批量清理事件。

```javascript
const controller = new AbortController();
const signal = controller.signal;

const button = document.getElementById('my-btn');
const input = document.getElementById('my-input');

// 注册事件时传入 signal 选项
button.addEventListener('click', () => console.log('按钮被点击'), { signal });
input.addEventListener('input', (e) => console.log(e.target.value), { signal });

// 当调用 abort() 时，所有通过该 signal 注册的事件监听器都会被自动移除
controller.abort();
```

---
## 在 React 组件中防止内存泄漏
在 React 的 `useEffect` 中使用 `AbortController` 是一个极佳的最佳实践。当组件在异步请求完成前被卸载时，它可以有效防止内存泄漏和“在已卸载组件上更新状态”的报错。

```jsx
import { useEffect, useState } from 'react';

function MyComponent() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const controller = new AbortController();
    
    const fetchData = async () => {
      try {
        const response = await fetch('https://api.example.com/data', { 
          signal: controller.signal 
        });
        const result = await response.json();
        setData(result);
      } catch (error) {
        // 忽略由组件卸载引起的中止错误
        if (error.name !== 'AbortError') {
          console.error('数据获取失败:', error);
        }
      }
    };

    fetchData();

    // 组件卸载时，执行清理函数，中止未完成的请求
    return () => {
      controller.abort();
    };
  }, []);

  return <div>{data ? JSON.stringify(data) : '加载中...'}</div>;
}
```

---
## 实现请求超时控制
你可以结合 `setTimeout` 和 `AbortController` 来为异步操作设置超时时间。

```javascript
function fetchWithTimeout(url, timeout = 5000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  return fetch(url, { signal: controller.signal })
    .then(response => {
      clearTimeout(timeoutId); // 请求成功，清除超时定时器
      return response;
    });
}

fetchWithTimeout('https://api.example.com/data', 3000)
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.log(err.name === 'AbortError' ? '请求超时' : err));
```

**总结：** `AbortController` 是现代 JavaScript 中管理异步操作生命周期的强大工具。无论是取消耗时的网络请求、防止组件内存泄漏，还是简化事件清理，它都提供了统一且高效的解决方案。