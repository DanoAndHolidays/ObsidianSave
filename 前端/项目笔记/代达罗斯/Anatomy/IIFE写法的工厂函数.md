# IIFE写法的工厂函数

当然可以直接写 `function`。这里写成这种形式，主要是为了利用 **立即执行函数（IIFE）+ 闭包**，把 `counter` 私有化。

原代码：
```ts
const uid = (() => {
  const state = { counter: 0 };

  return (): string => {
    state.counter += 1;

    return crypto.randomUUID?.() ?? `node-${state.counter}-${Date.now()}`;
  };
})();
```

可以先拆开理解。

## 1. 外层函数立即执行

```ts
(() => {
  // ...
})();
```

这叫立即执行函数，相当于：

```ts
const createUid = () => {
  // ...
};

const uid = createUid();
```

注意，`uid` 保存的不是外层函数，而是外层函数返回的那个函数。

因此最终的 `uid` 可以这样调用：

```ts
uid();
uid();
uid();
```

## 2. `state` 会被闭包保存

外层函数中创建了：

```ts
const state = { counter: 0 };
```

然后返回的内部函数使用了它：

```ts
return () => {
  state.counter += 1;
};
```

虽然外层函数已经执行结束，但内部函数还引用着 `state`，所以 `state` 不会被销毁。

每次调用：

```ts
uid();
```

都会操作同一个 `state.counter`。

大致过程是：

```ts
uid(); // counter 变成 1
uid(); // counter 变成 2
uid(); // counter 变成 3
```

这就是闭包。

## 3. 为什么不直接写普通函数

当然可以这样写：

```ts
let counter = 0;

function uid(): string {
  counter += 1;

  return crypto.randomUUID?.() ?? `node-${counter}-${Date.now()}`;
}
```

功能上基本一样。

但区别是，这里的 `counter` 暴露在外层作用域中：

```ts
counter = 999;
```

同一个模块中的其他代码可能会意外修改它。

而闭包版本：

```ts
const uid = (() => {
  const state = { counter: 0 };

  return () => {
    state.counter += 1;
    return `node-${state.counter}`;
  };
})();
```

外部只能调用 `uid`：

```ts
uid();
```

却无法直接访问或修改：

```ts
state.counter = 999; // 访问不到 state
```

所以这种写法的主要目的就是：

> 让计数器成为 `uid` 函数的私有状态。

## 4. 为什么使用对象 `state`，而不是直接使用 `counter`

其实也可以写得更简单：

```ts
const uid = (() => {
  let counter = 0;

  return (): string => {
    counter += 1;

    return crypto.randomUUID?.() ?? `node-${counter}-${Date.now()}`;
  };
})();
```

在这个场景里，使用：

```ts
const state = { counter: 0 };
```

并不是必需的。

可能的原因有两个。

第一，作者习惯把相关状态放在一个对象里：

```ts
const state = {
  counter: 0,
  prefix: "node",
};
```

以后扩展比较方便。

第二，`state` 本身是 `const`，但对象内部属性可以修改：

```ts
state.counter += 1;
```

不过使用：

```ts
let counter = 0;
```

其实更加直接。

## 5. 它本质上相当于什么

可以把原代码理解为一个“函数工厂”：

```ts
function createUidGenerator() {
  let counter = 0;

  return function uid(): string {
    counter += 1;

    return crypto.randomUUID?.() ?? `node-${counter}-${Date.now()}`;
  };
}

const uid = createUidGenerator();
```

这里只是把“创建生成器”和“立即创建生成器”写在了一起：

```ts
const uid = createUidGenerator();
```

进一步压缩后，就成了原来的 IIFE：

```ts
const uid = (() => {
  let counter = 0;

  return () => {
    counter += 1;
    return `node-${counter}`;
  };
})();
```

## 6. `crypto.randomUUID?.()` 的作用

```ts
crypto.randomUUID?.()
```

这里的 `?.()` 表示：

* 如果 `crypto.randomUUID` 存在，就调用它；
* 如果不存在，就返回 `undefined`。

然后通过空值合并运算符：

```ts
?? `node-${state.counter}-${Date.now()}`
```

使用备用方案。

也就是说：

```ts
return crypto.randomUUID?.() ?? fallbackId;
```

相当于：

```ts
if (crypto.randomUUID) {
  return crypto.randomUUID();
}

return `node-${state.counter}-${Date.now()}`;
```

不过有一点值得注意：如果浏览器支持 `randomUUID()`，那么 fallback 根本不会执行，`counter` 的值实际上没有参与最终 ID。它只是为了旧环境中的备用 ID 服务。

因此还可以稍微优化为：

```ts
const uid = (() => {
  let counter = 0;

  return (): string => {
    if (crypto.randomUUID) {
      return crypto.randomUUID();
    }

    counter += 1;
    return `node-${counter}-${Date.now()}`;
  };
})();
```

这样只有真正使用 fallback 时才增加计数器。

总结一下：**不是不能直接写 `function`，而是这种写法能够把 `counter` 封装成私有状态，避免污染外部作用域，也避免被其他代码随意修改。**
