# 迁移转态到Reducer中
## 使用 reducer 整合状态逻辑 [](https://zh-hans.react.dev/learn/extracting-state-logic-into-a-reducer#consolidate-state-logic-with-a-reducer "Link for 使用 reducer 整合状态逻辑")

随着组件复杂度的增加，你将很难一眼看清所有的组件状态更新逻辑。

随着这个组件的不断迭代，其状态逻辑也会越来越多。为了降低这种复杂度，并让所有逻辑都可以存放在一个易于理解的地方，你可以将这些状态逻辑移到组件之外的一个称为 **reducer** 的函数中。

可以通过三个步骤将 `useState` 迁移到 `useReducer`：

1. 将设置状态的逻辑 **修改** 成 dispatch 的一个 action；
2. **编写** 一个 reducer 函数；
3. 在你的组件中 **使用** reducer。

### 第 1 步: 将设置状态的逻辑修改成 dispatch 的一个 action [](https://zh-hans.react.dev/learn/extracting-state-logic-into-a-reducer#step-1-move-from-setting-state-to-dispatching-actions "Link for 第 1 步: 将设置状态的逻辑修改成 dispatch 的一个 action")

移除所有的状态设置逻辑。只留下事件处理函数：

- `handleAddTask(text)` 在用户点击 “添加” 时被调用。
- `handleChangeTask(task)` 在用户切换任务或点击 “保存” 时被调用。
- `handleDeleteTask(taskId)` 在用户点击 “删除” 时被调用。

```js
function handleDeleteTask(taskId) {
  setTasks(tasks.filter((t) => t.id !== taskId));
}

// 修改后
function handleDeleteTask(taskId) {
  dispatch(
    // "action" 对象：
    {
      type: 'deleted',
      id: taskId,
    }
  );
}
```

action它是一个普通的 JavaScript 对象。它的结构是由你决定的，但通常来说，它应该至少包含可以表明 **发生了什么事情** 的信息。（在后面的步骤中，你将会学习如何添加一个 `dispatch` 函数。）

按照惯例，我们通常会添加一个字符串类型的 `type` 字段来描述发生了什么，并通过其它字段传递额外的信息。`type` 是特定于组件的，在这个例子中 `added` 和 `addded_task` 都可以。选一个能描述清楚发生的事件的名字！

```js
dispatch({
  // 针对特定的组件
  type: 'what_happened',
  // 其它字段放这里
});
```

### 第 2 步: 编写一个 reducer 函数 [](https://zh-hans.react.dev/learn/extracting-state-logic-into-a-reducer#step-2-write-a-reducer-function "Link for 第 2 步: 编写一个 reducer 函数")

reducer 函数就是你放置状态逻辑的地方。它接受两个参数，分别为当前 state 和 action 对象，并且返回的是更新后的 state：

```js
function yourReducer(state, action) {  
	// 给 React 返回更新后的状态
}
```

React 会将状态设置为你从 reducer 返回的状态。

在这个例子中，要将状态设置逻辑从事件处理程序移到 reducer 函数中，你需要：

1. 声明当前状态（`tasks`）作为第一个参数；
2. 声明 `action` 对象作为第二个参数；
3. 从 `reducer` 返回 **下一个** 状态（React 会将旧的状态设置为这个最新的状态）。

```js
function tasksReducer(tasks, action) {
  switch (action.type) {
    case 'added': {
      return [
        ...tasks,
        {
          id: action.id,
          text: action.text,
          done: false,
        },
      ];
    }
    case 'changed': {
      return tasks.map((t) => {
        if (t.id === action.task.id) {
          return action.task;
        } else {
          return t;
        }
      });
    }
    case 'deleted': {
      return tasks.filter((t) => t.id !== action.id);
    }
    default: {
      throw Error('未知 action: ' + action.type);
    }
  }
}
```

我们建议将每个 `case` 块包装到 `{` 和 `}` 花括号中，这样在不同 `case` 中声明的变量就不会互相冲突。此外，`case` 通常应该以 `return` 结尾。如果你忘了 `return`，代码就会 `进入` 到下一个 `case`，这就会导致错误！

### 第 3 步: 在组件中使用 reducer [](https://zh-hans.react.dev/learn/extracting-state-logic-into-a-reducer#step-3-use-the-reducer-from-your-component "Link for 第 3 步: 在组件中使用 reducer")

最后，你需要将 `tasksReducer` 导入到组件中。记得先从 React 中导入 `useReducer` Hook：

```
import { useReducer } from 'react';
```

接下来，你就可以替换掉之前的 `useState`:

```
const [tasks, setTasks] = useState(initialTasks);
```

只需要像下面这样使用 `useReducer`:

```
const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);
```

`useReducer` 和 `useState` 很相似——你必须给它传递一个初始状态，它会返回一个有状态的值和一个设置该状态的函数（在这个例子中就是 dispatch 函数）。但是，它们两个之间还是有点差异的。

`useReducer` 钩子接受 2 个参数：

1. 一个 reducer 函数
2. 一个初始的 state

它返回如下内容：

1. 一个有状态的值
2. 一个 dispatch 函数（用来 “派发” 用户操作给 reducer）

## 对比 `useState` 和 `useReducer` [](https://zh-hans.react.dev/learn/extracting-state-logic-into-a-reducer#comparing-usestate-and-usereducer "Link for this heading")

Reducer 并非没有缺点！以下是比较它们的几种方法：

- **代码体积：** 通常，在使用 `useState` 时，一开始只需要编写少量代码。而 `useReducer` 必须提前编写 reducer 函数和需要调度的 actions。但是，当多个事件处理程序以相似的方式修改 state 时，`useReducer` 可以减少代码量。
- **可读性：** 当状态更新逻辑足够简单时，`useState` 的可读性还行。但是，一旦逻辑变得复杂起来，它们会使组件变得臃肿且难以阅读。在这种情况下，`useReducer` 允许你将状态更新逻辑与事件处理程序分离开来。
- **可调试性：** 当使用 `useState` 出现问题时, 你很难发现具体原因以及为什么。 而使用 `useReducer` 时， 你可以在 reducer 函数中通过打印日志的方式来观察每个状态的更新，以及为什么要更新（来自哪个 `action`）。 如果所有 `action` 都没问题，你就知道问题出在了 reducer 本身的逻辑中。 然而，与使用 `useState` 相比，你必须单步执行更多的代码。
- **可测试性：** reducer 是一个不依赖于组件的纯函数。这就意味着你可以单独对它进行测试。一般来说，我们最好是在真实环境中测试组件，但对于复杂的状态更新逻辑，针对特定的初始状态和 `action`，断言 reducer 返回的特定状态会很有帮助。
- **个人偏好：** 并不是所有人都喜欢用 reducer，没关系，这是个人偏好问题。你可以随时在 `useState` 和 `useReducer` 之间切换，它们能做的事情是一样的！

如果你在修改某些组件状态时经常出现问题或者想给组件添加更多逻辑时，我们建议你还是使用 reducer。当然，你也不必整个项目都用 reducer，这是可以自由搭配的。你甚至可以在一个组件中同时使用 `useState` 和 `useReducer`。

## 编写一个好的 reducer [](https://zh-hans.react.dev/learn/extracting-state-logic-into-a-reducer#writing-reducers-well "Link for 编写一个好的 reducer")

编写 `reducer` 时最好牢记以下两点：

- **reducer 必须是纯粹的。** 这一点和 [状态更新函数](https://zh-hans.react.dev/learn/queueing-a-series-of-state-updates) 是相似的，`reducer` 是在渲染时运行的！（actions 会排队直到下一次渲染)。 这就意味着 `reducer` [必须纯净](https://zh-hans.react.dev/learn/keeping-components-pure)，即当输入相同时，输出也是相同的。它们不应该包含异步请求、定时器或者任何副作用（对组件外部有影响的操作）。它们应该以不可变值的方式去更新 [对象](https://zh-hans.react.dev/learn/updating-objects-in-state) 和 [数组](https://zh-hans.react.dev/learn/updating-arrays-in-state)。
- **每个 action 都描述了一个单一的用户交互，即使它会引发数据的多个变化。** 举个例子，如果用户在一个由 `reducer` 管理的表单（包含五个表单项）中点击了 `重置按钮`，那么 dispatch 一个 `reset_form` 的 action 比 dispatch 五个单独的 `set_field` 的 action 更加合理。如果你在一个 `reducer` 中打印了所有的 `action` 日志，那么这个日志应该是很清晰的，它能让你以某种步骤复现已发生的交互或响应。这对代码调试很有帮助！

我靠了，这个东西，有点小难

### 实现一个useReducer

```js
import { useState } from 'react';

export function useReducer(reducer, initialState) {
  const [state, setState] = useState(initialState);
  // ???
  function dispatch(action){
    setState(reducer(state,action))
  }
  return [state, dispatch];
}
```

我好像理解了一点，但不多

我理解了，`reducer`的作用是返回一个由原先的state并且经过我要的动作的处理的之后的值，这个值用来传入`setter()`，`initialState`是用来初始化所有的状态的，`state`是使用`useState(initialState)`得到的值。理解了就感觉好爽！

通过这种方式就将所有的State集中管理，将页面更新的逻辑抽离出来。