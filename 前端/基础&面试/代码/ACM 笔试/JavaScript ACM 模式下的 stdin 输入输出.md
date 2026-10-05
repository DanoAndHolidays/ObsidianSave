# JavaScript ACM 模式下的 stdin 输入输出
> Last Format Time：9/16/2026 19:24:50

*牛客的笔试会有，而且有的笔试提供商，居然不给代码模版，666*

---
## ACM 模式是什么
LeetCode 通常只需要写函数：

```js
function solve(nums) {
  // ...
}
```

ACM 模式需要自己完成：

```text
读取 stdin
→ 解析输入
→ 执行算法
→ 输出答案
```

Node.js 中最推荐的读取方式：

```js
const fs = require('fs')

const input = fs.readFileSync(0, 'utf8').trim()
```

其中：

- `0` 表示标准输入 stdin
    
- 读取到的数据都是字符串
    

---
## 最常用：Token 模式
如果输入主要是数字、单词等由空格或换行分隔的数据：

```js
const fs = require('fs')

const input = fs.readFileSync(0, 'utf8').trim()
const tokens = input.split(/\s+/)

let index = 0
```

例如输入：

```text
5
1 2 3 4 5
10
```

经过：

```js
input.split(/\s+/)
```

得到：

```js
['5', '1', '2', '3', '4', '5', '10']
```

然后用指针依次读取：

```js
const n = Number(tokens[index++])

const arr = []

for (let i = 0; i < n; i++) {
  arr.push(Number(tokens[index++]))
}

const target = Number(tokens[index++])
```

核心 mental model：

```text
stdin
→ 一个字符串
→ 拆成 tokens
→ index 从左往右消费数据
```

`tokens[index++]` 等价于：

```js
const value = tokens[index]
index++
```

---
## 一堆数字时可以直接拍平
```js
const nums = input.split(/\s+/).map(Number)
```

例如：

```text
1 2
3 4
```

得到：

```js
[1, 2, 3, 4]
```

`\s+` 可以匹配：

- 空格
    
- 多个空格
    
- 换行
    
- Tab
    

因此数字题通常不需要关心输入到底分成几行。

---
## 按行读取
如果“每一整行”本身具有意义，例如字符串中包含空格：

```text
3
hello world
hello javascript
good morning
```

应该：

```js
const lines = input.split(/\r?\n/)
```

例如：

```js
const n = Number(lines[0])

for (let i = 1; i <= n; i++) {
  const str = lines[i]
}
```

不要使用：

```js
input.split(/\s+/)
```

否则：

```text
hello world
```

会被拆成：

```js
['hello', 'world']
```

判断原则：

```text
数字 / 单词由空白分隔
→ Token 模式

整行文本本身有意义
→ Line 模式
```

---
## 多组测试数据
输入：

```text
3
1 2
3 4
5 6
```

第一项表示测试次数 `T`：

```js
const tokens = input.split(/\s+/)
let index = 0

const T = Number(tokens[index++])

for (let i = 0; i < T; i++) {
  const a = Number(tokens[index++])
  const b = Number(tokens[index++])

  console.log(a + b)
}
```

---
## 读取直到 EOF
如果题目没有给 `T`，而是：

> 输入若干组数据，直到文件结束。

可以：

```js
let index = 0

while (index < tokens.length) {
  const a = Number(tokens[index++])
  const b = Number(tokens[index++])

  console.log(a + b)
}
```

本质：

```text
还有 token
→ 继续读取

没有 token
→ 输入结束
```

---
## 输出
少量输出：

```js
console.log(answer)
```

大量结果推荐先收集：

```js
const result = []

result.push(answer1)
result.push(answer2)

console.log(result.join('\n'))
```

避免大量调用 `console.log`。

---
## readline
Node.js 也可以：

```js
const readline = require('readline')

const rl = readline.createInterface({
  input: process.stdin
})

rl.on('line', (line) => {
  // 每读取一行执行一次
})
```

它是事件驱动的：

```text
stdin 来一行
→ line callback

再来一行
→ 再执行 callback
```

但算法笔试中通常：

```js
fs.readFileSync(0, 'utf8')
```

更简单，因为可以一次得到完整输入，再统一解析。

因此 ACM 笔试默认优先使用 `fs`。

---
## 推荐默认模板
### Token 模式
```js
const fs = require('fs')

const input = fs.readFileSync(0, 'utf8').trim()
const tokens = input.split(/\s+/)

let index = 0

// const n = Number(tokens[index++])

// 算法...

// console.log(answer)
```

### 全部都是数字
```js
const fs = require('fs')

const input = fs.readFileSync(0, 'utf8').trim()
const nums = input.split(/\s+/).map(Number)
```

### 按行读取
```js
const fs = require('fs')

const input = fs.readFileSync(0, 'utf8').trim()
const lines = input.split(/\r?\n/)
```

---
## 核心结论
ACM 模式本质上不是新的算法模式，只是多了：

```text
读取输入 + 解析输入 + 输出结果
```

JS 最常用套路：

```js
const input = fs.readFileSync(0, 'utf8').trim()

const tokens = input.split(/\s+/)

let index = 0
```

然后：

```js
const value = Number(tokens[index++])
```

不断从左到右消费输入即可。

优先记住：

```text
普通数字题 → token + index
整行字符串 → lines
大量输出 → result.join('\n')
ACM 默认 → fs.readFileSync(0, 'utf8')
```