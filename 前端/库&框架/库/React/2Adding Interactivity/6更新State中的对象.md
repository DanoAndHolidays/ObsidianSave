state 中可以保存任意类型的 JavaScript 值，包括对象。但是，你不应该直接修改存放在 React state 中的对象。相反，当你想要更新一个对象时，你需要创建一个新的对象（或者将其拷贝一份），然后将 state 更新为此对象。

现在考虑 state 中存放对象的情况：

```
const [position, setPosition] = useState({ x: 0, y: 0 });
```

从技术上来讲，可以改变对象自身的内容。**当你这样做时，就制造了一个 mutation**：

```
position.x = 5;
```

然而，虽然严格来说 React state 中存放的对象是可变的，但你应该像处理数字、布尔值、字符串一样将它们视为不可变的。因此你应该替换它们的值，而不是对它们进行修改。

应该创建一个新的对象，将它传递给setter函数，像这样的代码就 **没有任何问题**，因为你改变的是你刚刚创建的一个新的对象：

```
const nextPosition = {};
nextPosition.x = e.clientX;
nextPosition.y = e.clientY;
setPosition(nextPosition);
```

事实上，它完全等同于下面这种写法：

```
setPosition({  x: e.clientX,  y: e.clientY});
```

只有当你改变已经处于 state 中的 **现有** 对象时，mutation 才会成为问题。而修改一个你刚刚创建的对象就不会出现任何问题，因为 **还没有其他的代码引用它**。改变它并不会意外地影响到依赖它的东西。这叫做“局部 mutation”。你甚至可以 [在渲染的过程中](https://zh-hans.react.dev/learn/keeping-components-pure#local-mutation-your-components-little-secret) 进行“局部 mutation”的操作。这种操作既便捷又没有任何问题！

### 使用展开语法

```
setPerson({  
	firstName: e.target.value, // 从 input 中获取新的 first name  
	lastName: person.lastName,  
	email: person.email
});
```

你可以使用 `...` [对象展开](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/Spread_syntax#spread_in_object_literals) 语法，这样你就不需要单独复制每个属性。但是 `...` 展开语法本质是是“浅拷贝”——它只会复制一层。这使得它的执行速度很快，但是也意味着当你想要更新一个嵌套属性时，你必须得多次使用展开语法。可以在对象的定义中使用 `[` 和 `]` 括号来实现属性的动态命名。

```
setPerson({  
	...person, // 复制上一个 person 中的所有字段  
	firstName: e.target.value // 但是覆盖 firstName 字段 
});
```