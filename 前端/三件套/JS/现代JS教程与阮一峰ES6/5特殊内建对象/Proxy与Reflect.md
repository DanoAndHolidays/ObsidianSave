proxy代理器，用于拦截某些操作，修改原生的操作：
```javascript
let proxy = new Proxy(target, handler)
```
- `target` —— 是要包装的对象，可以是任何东西，包括函数。
- `handler` —— 代理配置：带有“捕捉器”（“traps”，即拦截操作的方法）的对象。比如 `get` 捕捉器用于读取 `target` 的属性，`set` 捕捉器用于写入 `target` 的属性，等等。

对 `proxy` 进行操作，如果在 `handler` 中存在相应的捕捉器，则handler将运行，否则将直接对 target 进行处理:
```javascript
let target = {};
let proxy = new Proxy(target, {}); // 空的 handler 对象

proxy.test = 5; // 写入 proxy 对象 (1)
alert(target.test); // 5，test 属性出现在了 target 中！

alert(proxy.test); // 5，我们也可以从 proxy 对象读取它 (2)

for(let key in proxy) alert(key); // test，迭代也正常工作 (3)
```
![[Pasted image 20250628171616.png]]
带有get的代理器：
```javascript
let dictionary = {
  'Hello': 'Hola',
  'Bye': 'Adiós'
};

dictionary = new Proxy(dictionary, {
  get(target, phrase) { // 拦截读取属性操作
    if (phrase in target) { //如果词典中有该短语
      return target[phrase]; // 返回其翻译
    } else {
      // 否则返回未翻译的短语
      return phrase;
    }
  }
});

// 在词典中查找任意短语！
// 最坏的情况也只是它们没有被翻译。
alert( dictionary['Hello'] ); // Hola
alert( dictionary['Welcome to Proxy']); // Welcome to Proxy（没有被翻译）
```

set：
 ```javascript
 let numbers = [];

numbers = new Proxy(numbers, { // (*)
  set(target, prop, val) { // 拦截写入属性操作
    if (typeof val == 'number') {
      target[prop] = val;
      return true;
    } else {
      return false;
    }
  }
});

numbers.push(1); // 添加成功
numbers.push(2); // 添加成功
alert("Length is: " + numbers.length); // 2

numbers.push("test"); // TypeError（proxy 的 'set' 返回 false）

alert("This line is never reached (error in the line above)");
```


没看完

--- 
#### Reflect
`Reflect` 是一个内建对象，可简化 `Proxy` 的创建。
前面所讲过的内部方法，例如 `[[Get]]` 和 `[[Set]]` 等，都只是规范性的，不能直接调用。
`Reflect` 对象使调用这些内部方法成为了可能。它的方法是内部方法的最小包装。


















