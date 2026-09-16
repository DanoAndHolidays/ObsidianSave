可以把 **CommonJS（CJS）和 ESM 的根本区别**先压缩成一句：

> **CommonJS 是“运行时执行代码来加载模块”，ESM 是“在执行代码之前，先静态分析并建立模块依赖关系”。**

这个区别基本决定了后面的 tree shaking（摇树优化）、循环依赖、导入导出行为。

---
## CommonJS 底层大概是怎么实现的？
你听到的：

> CommonJS 是立即执行函数 IIFE 实现的。

**不算完全错，但不准确。**

更准确地说，Node.js 会把一个 CommonJS 文件**包装进一个函数里执行**。

比如你写：

```js
// a.js
const x = 1

module.exports = {
  x
}
```

Node 内部可以粗略理解成：

```js
(function (exports, require, module, __filename, __dirname) {
  const x = 1

  module.exports = {
    x
  }
})
```

然后 Node 再调用这个函数：

```js
wrapper.call(
  module.exports,
  module.exports,
  require,
  module,
  __filename,
  __dirname
)
```

所以你在 CommonJS 文件里为什么可以凭空使用：

```js
require
module
exports
__filename
__dirname
```

不是因为这些东西是真正的全局变量，而是因为 Node **把它们作为函数参数传进来了**。

### 那它是不是 IIFE？
IIFE 是：

```js
(function () {
  // ...
})()
```

特点是：

> 函数创建以后立即调用。

Node 的 CommonJS wrapper 在效果上有点像 IIFE：

```js
(function (...) {
  // module code
})(...)
```

但从模块机制的角度，最好记成：

> **CommonJS 使用 function wrapper（函数包装器）为每个模块创建独立作用域。**

不要单纯记成“CommonJS = IIFE”。


# CJS与ESM的区别 💡
> Last Format Time：9/16/2026 19:24:53

假设：

```js
const foo = require('./foo')
```

可以粗略理解成：

```text
require('./foo')
        ↓
解析文件路径
        ↓
检查 module cache（模块缓存）
        ↓
没有缓存
        ↓
创建 Module 对象
        ↓
读取 foo.js
        ↓
包装成函数
        ↓
执行函数
        ↓
foo.js 修改 module.exports
        ↓
缓存 module
        ↓
返回 module.exports
```

例如：

```js
// foo.js

console.log('foo execute')

module.exports = {
  value: 123
}
```

```js
const a = require('./foo')
const b = require('./foo')
```

一般只会：

```text
foo execute
```

一次。

因为第一次之后：

```js
require.cache
```

里已经有它了。

所以：

```js
a === b
```

通常是：

```js
true
```

这也是为什么 CommonJS 天然很适合实现单例式模块。


# 3. CommonJS 的 export 本质是什么？

这一点特别重要。

CommonJS：

```js
module.exports = {}
```

本质上：

> **一个模块执行完成以后，返回 `module.exports` 这个对象。**

比如：

```js
// counter.js

let count = 0

module.exports = {
  count
}
```

另一个文件：

```js
const counter = require('./counter')
```

本质类似：

```js
const counter = module.exports
```

所以 CJS 的核心 mental model（心智模型）是：

```text
执行一个函数
    ↓
得到 module.exports
```


# 4. ESM 底层完全不一样

ESM：

```js
import { foo } from './foo.js'

export const bar = 123
```

JavaScript 引擎不会简单把它理解成：

```js
const foo = require('./foo')
```

而是会在代码真正执行之前，对：

```js
import
export
```

进行分析。

ESM 大致有几个阶段：

```text
Parsing
解析
 ↓
Module Linking
模块链接
 ↓
Instantiation
实例化
 ↓
Evaluation
执行
```

简化理解：

```text
读取文件
  ↓
发现 import / export
  ↓
构建 module graph（模块依赖图）
  ↓
建立 import 和 export 的绑定关系
  ↓
最后才真正执行模块代码
```

例如：

```js
// a.js
export const foo = 1
```

```js
// b.js
import { foo } from './a.js'
```

在真正运行：

```js
console.log(foo)
```

之前，引擎已经知道：

```text
b.js
 |
 └── foo → a.js 的 foo export
```


# 5. 这里有一个关键概念：ESM 是 static structure（静态结构）

ESM 要求：

```js
import { foo } from './foo.js'
```

这种 import 基本必须出现在模块顶层。

你不能这样：

```js
if (condition) {
  import { foo } from './foo.js'
}
```

这是语法错误。

动态导入必须使用：

```js
if (condition) {
  const module = await import('./foo.js')
}
```

为什么 ESM 这么设计？

因为引擎希望在**代码真正执行之前**就知道：

```text
这个模块依赖谁？
导入了什么？
导出了什么？
```

于是 bundler（打包器）也可以提前知道。

这正是 tree shaking 的基础。


# 6. CommonJS 为什么很难 tree shaking？

看这个：

```js
const moduleName = Math.random() > 0.5
  ? './a'
  : './b'

const module = require(moduleName)
```

你在静态分析阶段很难知道：

```text
最终 require a 还是 b？
```

甚至：

```js
const name = getModuleName()

require(name)
```

更不知道。

再比如：

```js
const exports = require('./utils')

exports[getKey()]()
```

bundler 很难确认：

```text
utils 里究竟哪些东西会被使用？
```

因为 `require()` 是：

> **普通 JavaScript 函数调用。**

它发生在 runtime（运行时）。


# 7. ESM 为什么适合 Tree Shaking？

例如：

```js
// utils.js

export function add() {}

export function subtract() {}

export function multiply() {}
```

你只使用：

```js
import { add } from './utils.js'

add()
```

bundler 在打包之前就能知道：

```text
utils exports:
- add        ← used
- subtract   ← unused
- multiply   ← unused
```

于是：

```js
subtract
multiply
```

可以被删掉。

最终可能只剩：

```js
function add() {}

add()
```

这就是 tree shaking（摇树优化）的基本思想。


# 8. 所以“只有 ESM 能 Tree Shaking”吗？

严格来说：

> **不是。**

更准确的说法是：

> **ESM 天然支持可靠的静态 tree shaking；CommonJS 很难做可靠的 tree shaking，但现代 bundler 有时能对部分 CommonJS 做有限优化。**

比如：

```js
exports.foo = function () {}
exports.bar = function () {}
```

一些打包器可能通过静态分析猜出来：

```text
foo 被用了
bar 没被用
```

于是优化掉一些代码。

但是只要代码复杂起来：

```js
module.exports[getName()] = foo
```

或者：

```js
Object.assign(module.exports, someObject)
```

或者：

```js
if (condition) {
  module.exports.foo = ...
}
```

分析难度就会暴涨。

所以工程上一般记：

```text
ESM
↓
static import/export
↓
module graph 可以静态分析
↓
天然适合 tree shaking
```

而：

```text
CommonJS
↓
require() / module.exports
↓
运行时行为
↓
tree shaking 困难
```


# 9. 还有一个很重要的底层区别：ESM 是 live binding（实时绑定）

例如：

```js
// counter.js

export let count = 0

export function increment() {
  count++
}
```

```js
import {
  count,
  increment
} from './counter.js'

console.log(count) // 0

increment()

console.log(count) // 1
```

这里：

```js
count
```

不是简单：

```js
const count = counter.count
```

它实际上是一个：

> live binding（实时绑定）

可以理解成：

```text
import 的 count
      ↓
一直指向
      ↓
counter 模块里的那个 count binding
```

所以原模块修改：

```js
count++
```

导入方看到的值也会变化。

---
## CommonJS 更像“拿到对象”
CommonJS：

```js
// counter.js

let count = 0

module.exports = {
  count,
  increment() {
    count++
  }
}
```

```js
const counter = require('./counter')

console.log(counter.count) // 0

counter.increment()

console.log(counter.count) // 还是 0
```

因为：

```js
module.exports = {
  count
}
```

相当于：

```js
module.exports = {
  count: count
}
```

此时把当前数字 `0` 放到了对象里。

除非你：

```js
module.exports = {
  get count() {
    return count
  }
}
```

才会得到类似效果。


# 10. 两套机制可以这样对比

||CommonJS|ESM|
|---|---|---|
|语法|`require` / `module.exports`|`import` / `export`|
|加载时机|runtime（运行时）|执行前建立依赖关系|
|模块结构|dynamic（动态）|static（静态）|
|模块本质|执行函数得到 `module.exports`|Module Record + binding|
|import 行为|拿到 exports 对象|建立 live binding|
|Tree Shaking|困难 / 有限支持|天然适合|
|浏览器原生支持|❌|✅|
|Node 支持|✅|✅|
|模块作用域|function wrapper|原生 Module Scope|


# 11. 你可以建立这个底层 mental model

### CommonJS
```text
foo.js
↓
Node 读取文件
↓
包一层 function
↓
执行 function
↓
module.exports 被填充
↓
require() 返回 module.exports
```

也就是：

```js
const module = {
  exports: {}
}

(function (
  exports,
  require,
  module,
  __filename,
  __dirname
) {
  // 你的 foo.js
})(...)

return module.exports
```


### ESM
```text
foo.js
 ↓
Parser 发现 import/export
 ↓
创建 Module Record
 ↓
构建 Module Graph
 ↓
Link imports ↔ exports
 ↓
建立 live bindings
 ↓
Evaluate module
```

所以真正本质上的区别不是：

```text
require vs import
```

而是：

> **CommonJS 是 execution-based module system（基于执行的模块系统），ESM 是 declarative/static module system（声明式、静态模块系统）。**

而你问的 **tree shaking**，基本就是这个设计差异带来的直接结果。

最后纠正你听到的那句话，可以记成：

> ❌ CommonJS 底层就是 IIFE。  
> ✅ Node 的 CommonJS 会把每个模块包装进一个函数中执行，这种形式和 IIFE 很像，但更准确叫 **Module Wrapper / Function Wrapper（模块函数包装器）**。