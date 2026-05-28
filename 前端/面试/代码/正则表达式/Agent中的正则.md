# Agent中的正则
我们需要实现一个 `parseOutput` 函数，用来提取大模型返回的结构化字符串

## 字符串的match()
`match()` 是 JavaScript 字符串（String）原型上的一个非常强大的内置方法。它的核心作用就是**让一个字符串去匹配正则表达式，并把匹配到的结果提取出来**。

### 基础语法与返回值
它的基本调用格式是：`字符串.match(正则表达式)`。 它的返回值只有两种情况：

- **匹配成功**：返回一个**数组**，里面装着匹配到的各种信息。
- **匹配失败**：返回 **`null`**。（这也是为什么我们在写代码时，一定要先判断 `if (matchResult)` 防止报错的原因）。

### 决定返回结果的“开关”：全局标志 `g`
`match()` 方法的行为，完全取决于你传入的正则表达式**有没有带 `g`（全局匹配）标志**。

- **情况一：不带 `g` 标志（你刚才代码中的用法）** 它只会找**第一个**符合条件的匹配项就停下来。返回的数组非常详细，不仅包含匹配到的文本，还带有额外的属性：
    - `array[0]`：完整匹配到的文本。
    - `array[1]`, `array[2]`...：对应正则里第1个、第2个**小括号 `()`（捕获组）**里匹配到的内容。
    - `index`：匹配到的文本在原字符串中的起始位置。
    - `input`：原始字符串本身。

- **情况二：带了 `g` 标志（例如 `/abc/g`）** 它会化身“吸尘器”，把字符串里**所有**符合条件的内容全部找出来。
    - 返回的数组**只包含所有匹配到的完整文本**，**不会**包含小括号里的捕获组信息，也**没有** `index` 和 `input` 属性。

```javascript
const str = "Chapter 1.1 and Chapter 2.3";

// 1. 不带 g 标志：只找第一个，但提供详细信息（包括捕获组）
const regex1 = /Chapter (\d+\.\d+)/; 
const result1 = str.match(regex1);
console.log(result1);
// 输出结果：
// [
//   'Chapter 1.1',   // [0] 完整匹配
//   '1.1',           // [1] 第一个小括号 (\d+\.\d+) 捕获的内容
//   index: 0,        // 起始位置
//   input: 'Chapter 1.1 and Chapter 2.3', // 原字符串
//   groups: undefined
// ]

// 2. 带了 g 标志：找出所有，但只给纯文本，没有捕获组和位置信息
const regex2 = /Chapter (\d+\.\d+)/g;
const result2 = str.match(regex2);
console.log(result2);
// 输出结果：
// ['Chapter 1.1', 'Chapter 2.3'] 
```

## 函数实现
要实现这个 `parseOutput` 函数，核心就是通过字符串匹配把 `Thought:` 和 `Action:` 后面的内容分别提取出来：
```javascript
function parseOutput(responseWithThoughtAndAction) {
    let thought = ''
    let action = ''

    // 1. 提取 Thought 部分
    // 匹配 "Thought:" 开头，直到遇到 "Action:" 之前的所有内容
    const thoughtMatch = responseWithThoughtAndAction.match(/Thought:\s*([\s\S]*?)(?=\s*Action:)/)
    if (thoughtMatch && thoughtMatch[1]) {
        thought = thoughtMatch[1].trim()
    }

    // 2. 提取 Action 部分
    // 匹配 "Action:" 开头，直到字符串结束的所有内容
    const actionMatch = responseWithThoughtAndAction.match(/Action:\s*([\s\S]*)/)
    if (actionMatch && actionMatch[1]) {
        action = actionMatch[1].trim()
    }

    return { thought, action }
}

// --- 测试一下 ---
const testInput = `Thought: 用户想要去北京旅行，需要一个旅行计划。我可以 根据自己对北京的了解来生成一个详细的计划，包括景点、行程安排、美食建议等。不需要调用任何工具，直接给出答案即可。
Action: Finish[北京旅行计划（建议3-5天）]
## 第一天：历史经典游
- **上午**：天安门广场（免费，需预约）→ 故宫博物院（门票60元，建议提前购票，游览3-4小时）
- **下午**：景山公园（2元，俯瞰故宫全景）→ 北海公园（10元，可 划船）
- **晚上**：王府井步行街（小吃街、购物）`

const result = parseOutput(testInput)

console.log('--- 提取出的 Thought ---')
console.log(result.thought)
console.log('\n--- 提取出的 Action ---')
console.log(result.action)
```

1. **`/Thought:\s*([\s\S]*?)(?=\s*Action:)/`**：
    - `Thought:\s*`：匹配 "Thought:" 及其后面的空白字符（包括换行），`\s*`用来尽可能多地去匹配空白字符，直到遇到第一个非空白字符（比如你文本里的“用”字）时，\s* 就会停下来，把控制权交给后面。
    - `([\s\S]*?)`：核心捕获组。`[\s\S]` 表示匹配任意字符（包括换行符），`*?` 表示**非贪婪匹配**，即尽可能少地匹配，直到遇到后面的条件为止。
    - `(?=\s*Action:)`：这是一个**正向先行断言**，意思是“匹配到这里就停，因为后面紧跟着的是 Action:”，但它本身不会被包含在提取结果里。

2. **`/Action:\s*([\s\S]*)/`**：
    - 匹配 "Action:" 之后的所有剩余内容（包括多行的旅行计划详情），直到字符串结束。

3. **`.trim()`**：
    - 最后对提取出的字符串调用 `trim()`，是为了去掉首尾可能多余的空格或换行符，保证数据干净。
