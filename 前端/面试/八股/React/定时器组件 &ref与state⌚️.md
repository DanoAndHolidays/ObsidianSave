# 定时器组件 &ref与state⌚️
## 定时器组件
```js
import { useState, useRef, useEffect } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(10)

  // 不能使用let ，因为 React 每次渲染都会重新执行组件函数
  const timerRef = useRef<number | null>(null)
  //   useRef 的特点 ：
  // - 值存储在组件 外部 （React 管理的内存中）
  // - 每次渲染不重置，持久保存
  // - 改变 ref.current 不会触发重新渲染

  // 什么时候用 let ：
  // - 只在单次渲染内使用的临时变量
  // - 不需要在事件处理器中保持引用的值

  useEffect(() => {
    // useEffect 的返回值（return 函数）称为清理函数
    return () => {
      if (timerRef.current) {
        // 确保计时器被清除，防止内存泄漏
        clearInterval(timerRef.current)
      }
    }
  }, [])

  function startTimer() {
    if (timerRef.current) return


    // 为什么能省略 ：
    // - setInterval 是全局函数，挂载在 window 对象上
    // - 在浏览器环境， window.setInterval === setInterval
    // - 省略写更简洁

    // 为什么有时会加 window ：
    // - 代码更显式，明确是全局函数
    // - 避免与局部变量/函数冲突
    // - 部分老代码或类型声明不清楚时，加上更安全
    
    // 直接写 setInterval 没问题。
    timerRef.current = window.setInterval(() => {
      setCount((num) => {
        if (num <= 1) {
          stopTimer()
          return 0
        }
        return num - 1
      })
    }, 1000)
  }

  function stopTimer() {
    if (timerRef.current) {
      // 1. 防止重复启动 - startTimer 可以检查 if (timerRef.current) 避免创建多个计时器
      // 2. 状态明确 - null 表示计时器已停止，非 null 表示正在运行
      // clearInterval 本身只是停止计时器，但不清理引用。设置 null 是为了代码逻辑更清晰。

      // 但是我记得好像不是这样的呢？？？
      clearInterval(timerRef.current)
      timerRef.current = null
    }
  }

  return (
    <>
      <div>{count}</div>
      <button type="button" onClick={startTimer}>
        start
      </button>
      <button type="button" onClick={stopTimer}>
        stop
      </button>
    </>
  )
}

export default App
```

---
## ref与state
在 React 中，`ref` 和 `state` 是两种用于管理数据和组件行为的机制，但它们的核心作用和使用场景有着本质的区别。简单来说：**State（状态）用于驱动 UI 的更新，而 Ref（引用）则是绕过常规数据流的“逃生舱”，主要用于直接操作 DOM 或存储不触发重渲染的数据**。

以下是它们各自的具体使用场景及对比：

### State（状态）的使用场景
当组件需要维护随时间变化、响应用户输入或其他动态交互的数据，并且这些数据的变化需要反映到界面上时，就应该使用 State。

1. **表单与用户输入控制**：例如捕获受控输入框的值、搜索栏的内容等。
2. **交互式 UI 切换**：如弹窗（Modal）的显示/隐藏、下拉菜单的展开、按钮的禁用状态等。
3. **动态样式与内容渲染**：根据状态值改变文本颜色、动态加载并展示列表数据等。
4. **计数器与进度**：如点赞数、购物车商品数量等需要在界面上实时更新的数值。

### Ref（引用）的使用场景
Ref 提供了一种直接访问底层 DOM 节点或组件实例的方式，或者作为组件内部的一个“持久化便签”来记录信息。

1. **直接操作 DOM 元素**：
    - **焦点管理**：在页面加载或特定事件后自动聚焦输入框、选中文本。
    - **媒体控制**：手动播放/暂停视频或音频元素。
    - **测量与动画**：获取元素的尺寸（宽高）、滚动位置，或直接修改 DOM 样式以触发动画效果。
2. **集成第三方非 React 库**：当需要使用 D3.js、jQuery 等直接操作 DOM 的外部库时，通过 ref 将真实的 DOM 节点传递给它们。
3. **存储不影响渲染的可变值**：
    - **定时器与连接 ID**：保存 `setInterval` 的 ID、WebSocket 连接或 AbortController，以便后续清除，且不需要为此引发界面重绘。
    - **缓存与快照**：保存上一次的 Props/State 值（常用于比较前后变化）、统计组件的渲染次数、防抖逻辑中的最新值等。

### State 与 Ref 的核心区别总结
|特性|State (`useState`)|Ref (`useRef`)|
|:--|:--|:--|
|**是否触发重新渲染**|✅ 是|❌ 否（静默更新）|
|**如何更新值**|必须通过 setter 函数（如 `setState`）|直接修改 `.current` 属性|
|**主要用途**|驱动 UI 更新，保持视图与数据同步|访问 DOM、存储定时器/外部对象、缓存前一个值|
|**设计哲学**|声明式编程（React 核心思想）|命令式编程（处理特殊交互的补充手段）|

**💡 最佳实践建议：**  
在绝大多数情况下，应优先使用 React 的声明式编程模型（即通过 State 和 Props 来控制 UI）。只有当你确实需要跳出 React 抽象层去直接操作 DOM，或者存储完全不需要参与界面渲染的辅助变量时，才使用 Ref。滥用 Ref 会破坏代码的可预测性和可维护性。