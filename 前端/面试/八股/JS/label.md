# label
> Last Format Time：7/14/2026 20:25:30

如果你说的是 **JavaScript 中的“标签（label）”**，它是一种比较少用的语法，用来给代码块或循环起一个名字，然后配合 `break` 或 `continue` 使用。

语法如下：

```js
labelName: statement
```

例如：

```js
outer: {
  console.log("开始");

  break outer;

  console.log("这里不会执行");
}

console.log("结束");
```

输出：

```text
开始
结束
```

这里的 `outer:` 就是一个标签。

---
## 配合 break 使用
最常见的用途是**跳出指定的代码块或循环**。

### 没有标签
```js
for (let i = 0; i < 3; i++) {
  for (let j = 0; j < 3; j++) {
    if (j === 1) {
      break;
    }

    console.log(i, j);
  }
}
```

输出：

```text
0 0
1 0
2 0
```

`break` 只能退出**内层循环**。


### 使用标签
```js
outer:
for (let i = 0; i < 3; i++) {
  for (let j = 0; j < 3; j++) {
    if (j === 1) {
      break outer;
    }

    console.log(i, j);
  }
}
```

输出：

```text
0 0
```

执行到 `break outer` 时，直接退出整个 `outer` 循环。

相当于：

```text
outer
 └── for i
      └── for j
            ↓
      break outer
            ↓
退出整个 outer
```

---
## 配合 continue 使用
`continue` 可以直接进入**指定标签对应循环**的下一次迭代。

例如：

```js
outer:
for (let i = 0; i < 3; i++) {
  for (let j = 0; j < 3; j++) {
    if (j === 1) {
      continue outer;
    }

    console.log(i, j);
  }
}
```

输出：

```text
0 0
1 0
2 0
```

流程：

```js
outer: {
  console.log("开始");

  break outer;

  console.log("这里不会执行");
}

console.log("结束");
```

整个内层循环都被跳过了。

---
## 标签也可以标记普通代码块
例如：

```js
outer: {
  console.log("开始");

  break outer;

  console.log("这里不会执行");
}

console.log("结束");
```

输出：

```js
outer: {
  console.log("开始");

  break outer;

  console.log("这里不会执行");
}

console.log("结束");
```

这里 `break block` 就相当于提前结束这个代码块。

---
## 一个实际例子
假设要在二维数组中找到某个数字，找到后立即结束所有循环。

### 不使用标签
通常需要一个额外变量：

```js
outer: {
  console.log("开始");

  break outer;

  console.log("这里不会执行");
}

console.log("结束");
```


### 使用标签
```js
outer: {
  console.log("开始");

  break outer;

  console.log("这里不会执行");
}

console.log("结束");
```

这样代码更直接。

---
## 注意事项
标签名就是一个普通标识符：

```js
outer: {
  console.log("开始");

  break outer;

  console.log("这里不会执行");
}

console.log("结束");
```

它不是字符串，所以不要写成：

```js
outer: {
  console.log("开始");

  break outer;

  console.log("这里不会执行");
}

console.log("结束");
```

---
## 为什么平时几乎见不到？
因为现代 JavaScript 开发中：

- 可以把代码拆成函数，用 `return` 提前退出。
    
- 可以使用数组方法（`find`、`some`、`every` 等）替代多层循环。
    
- 多层循环也可以用状态变量控制。
    

因此，标签（label）除了在**需要从多层循环中快速跳出**的场景外，很少使用。

### 总结
标签最核心的作用只有两个：

- `break label`：跳出指定标签对应的代码块或循环。
    
- `continue label`：直接开始指定标签对应循环的下一次迭代（只能用于循环标签）。
    

对于日常开发来说，**90% 以上的标签使用场景都是处理多层嵌套循环时的 `break outer`**。这也是你最可能在实际项目中遇到的用法。