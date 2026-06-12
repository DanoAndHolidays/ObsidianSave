`call`、`apply`、`bind` 都是 JavaScript 中用来**显式改变函数运行时 this 指向**的方法，它们都定义在 `Function.prototype` 上。三者的核心区别在于**调用方式**和**传参形式**。

---

### 1. call
- **立即执行**函数。
- 第一个参数是 this 要指向的对象，后面的参数**逐个传递**。
```javascript
func.call(thisArg, arg1, arg2, ...)
```
示例：
```javascript
const obj = { name: 'Alice' };
function say(greeting, punctuation) {
  console.log(greeting + ', ' + this.name + punctuation);
}
say.call(obj, 'Hello', '!'); // Hello, Alice!
```

---

### 2. apply
- **立即执行**函数。
- 第一个参数是 this 要指向的对象，第二个参数是一个**数组（或类数组）**，里面包含所有参数。
```javascript
func.apply(thisArg, [arg1, arg2, ...])
```
示例：
```javascript
say.apply(obj, ['Hi', '?']); // Hi, Alice?
```
- 经典使用场景：借用 `Math.max` 处理数组。
```javascript
Math.max.apply(null, [1, 5, 3]); // 5
```

---

### 3. bind
- **不会立即执行**，而是返回一个**绑定了 this 的新函数**。
- 可以预设部分参数（柯里化），在真正调用时再传入剩余参数。
```javascript
const boundFunc = func.bind(thisArg, arg1, arg2, ...)
boundFunc(restArgs...)
```
示例：
```javascript
const sayToAlice = say.bind(obj, 'Hey');
sayToAlice('!!'); // Hey, Alice!!
```
- 典型使用场景：事件回调中固定 this，或延迟执行。
```javascript
const user = {
  name: 'Bob',
  greet() { console.log('Hi, ' + this.name); }
};
setTimeout(user.greet.bind(user), 1000);
```

---

### 核心区别对比

| 特性 | call | apply | bind |
|------|------|-------|------|
| **是否立即执行** | ✅ 是 | ✅ 是 | ❌ 否，返回新函数 |
| **参数传递方式** | 逐个传入 (comma-separated) | 以数组形式传入 | 可分批传入（预设+剩余） |
| **返回值** | 函数执行结果 | 函数执行结果 | 绑定了 this 的新函数 |
| **典型场景** | 明确参数个数时借用方法 | 参数已经是数组（如 Math.max） | 回调、事件监听、偏函数 |

简单记忆：  
- `call` —— **C**omma（逗号）传参，立即执行。  
- `apply` —— **A**rray（数组）传参，立即执行。  
- `bind` —— **B**ind 之后不立即执行，返回新函数，传参类似 call。