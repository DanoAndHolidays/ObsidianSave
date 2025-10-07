在ES6模块中，导入和导出的使用如果不规范，很容易产生错误。以下是一些常见错误及其解决方法：
### 1. 导入导出类型不匹配错误
**错误表现**：如前面提到的，使用默认导出的模块却用具名导入方式，或者使用具名导出的模块却用默认导入方式，导致找不到对应导出项，报错 `No matching export in "xxx" for import "xxx"` 。
**错误示例**：
 - **导出文件（`module.js`）**：
```javascript
const data = { message: 'Hello' };
export default data;
```
 - **导入文件（`main.js`）**：
```javascript
import { data } from './module.js'; // 错误，这里使用了具名导入，但module.js是默认导出
```
**解决方法**：
 - 如果是默认导出，导入时直接使用默认导入形式：
```javascript
import data from './module.js'; // 正确，使用默认导入
```
 - 如果想使用具名导入，将导出文件修改为具名导出：
```javascript
export const data = { message: 'Hello' };
```
然后在导入文件中使用具名导入：
```javascript
import { data } from './module.js'; // 正确，使用具名导入
```

### 2. 路径错误
**错误表现**：导入模块时指定了错误的文件路径，导致无法找到模块，报错类似于 `Cannot find module 'xxx'` 。
**错误示例**：
```javascript
import { someFunction } from '../wrongPath/module.js'; // 假设模块实际在../correctPath/module.js
```
**解决方法**：仔细检查并确保导入路径与模块实际存放路径一致，修改为正确路径：
```javascript
import { someFunction } from '../correctPath/module.js';
```

### 3. 重复导入
**错误表现**：多次导入同一个模块，虽然在ES6中重复导入不会报错，但可能会导致代码可读性变差，且存在不必要的资源消耗。
**错误示例**：
```javascript
import { someFunction } from './module.js';
import { anotherFunction } from './module.js';
// 又一次导入整个模块
import * as module from './module.js'; 
```
**解决方法**：尽量将多次导入合并为一次导入，按需获取需要的导出项：
```javascript
import { someFunction, anotherFunction } from './module.js';
```
或者使用通配符导入后按需访问：
```javascript
import * as module from './module.js';
const result1 = module.someFunction();
const result2 = module.anotherFunction();
```

### 4. 导出变量未定义
**错误表现**：在导出时，导出了一个未定义的变量，导致运行时报错。
**错误示例**：
```javascript
export { nonExistentVariable }; // nonExistentVariable未定义
```
**解决方法**：确保导出的变量已经被正确声明和赋值：
```javascript
const definedVariable = 'This is defined';
export { definedVariable };
```

### 5. 循环依赖
**错误表现**：模块A导入模块B，而模块B又导入模块A，形成循环引用，可能导致某些变量未初始化就被使用，从而报错。
**错误示例**：
 - **`moduleA.js`**：
```javascript
import { bFunction } from './moduleB.js';
export const aFunction = () => {
    console.log('Inside aFunction');
    bFunction();
};
```
 - **`moduleB.js`**：
```javascript
import { aFunction } from './moduleA.js';
export const bFunction = () => {
    console.log('Inside bFunction');
    aFunction();
};
```
**解决方法**：
 - 重构代码，避免循环依赖，比如将两个模块中互相依赖的部分提取到一个独立的新模块中。
 - 如果无法避免循环依赖，可以尽量确保在循环引用中，被使用的变量在引用前已经被正确初始化。例如，在Node.js环境中，ES6模块的加载机制会先扫描所有导入导出语句，然后按照一定顺序执行模块代码，合理安排代码执行顺序有时能避免问题。

### 6. 导入导出的语法错误
**错误表现**：在使用导入导出语法时，写错关键字或者语法格式，比如忘记写 `export` 或者 `import` 等，导致语法错误。
**错误示例**：
```javascript
const myFunction = () => {
    console.log('Function');
};
function { // 这里少了export关键字，不是一个正确的导出语句
    myFunction();
}
```
**解决方法**：仔细检查导入导出的语法，确保关键字拼写正确，语句格式符合ES6规范。比如上面的代码修改为：
```javascript
const myFunction = () => {
    console.log('Function');
};
export function myExportedFunction() {
    myFunction();
}
``` 

通过`export`命令显式指定输出的代码，再通过`import`命令输入。

```javascript
// ES6模块
import { stat, exists, readFile } from 'fs';
```

---
ES6 的模块自动采用严格模式，不管你有没有在模块头部加上`"use strict";`。
一个模块就是一个独立的文件。该文件内部的所有变量，外部无法获取。如果你希望外部能够读取模块内部的某个变量，就必须使用`export`关键字输出该变量。下面是一个 JS 文件，里面使用`export`命令输出变量。

```javascript
// profile.js
export var firstName = 'Michael';
export var lastName = 'Jackson';
export var year = 1958;

或者export {firstName,lastName,year};
```
通常情况下，`export`输出的变量就是本来的名字，但是可以使用`as`关键字重命名。

```javascript
function v1() { ... }
function v2() { ... }

export {
  v1 as streamV1,
  v2 as streamV2,
  v2 as streamLatestVersion
};
```

上面代码使用`as`关键字，重命名了函数`v1`和`v2`的对外接口。重命名后，`v2`可以用不同的名字输出两次。

需要特别注意的是，`export`命令规定的是对外的接口，必须与模块内部的变量建立一一对应关系。

```javascript
// 报错
export 1;

// 报错
var m = 1;
export m;
```

上面两种写法都会报错，因为没有提供对外的接口。第一种写法直接输出 1，第二种写法通过变量`m`，还是直接输出 1。`1`只是一个值，不是接口。正确的写法是下面这样。

```javascript
// 写法一
export var m = 1;

// 写法二
var m = 1;
export {m};

// 写法三
var n = 1;
export {n as m};
```

上面三种写法都是正确的，规定了对外的接口`m`。其他脚本可以通过这个接口，取到值`1`。它们的实质是，在接口名与模块内部变量之间，建立了一一对应的关系。

同样的，`function`和`class`的输出，也必须遵守这样的写法。

```javascript
// 报错
function f() {}
export f;

// 正确
export function f() {};

// 正确
function f() {}
export {f};
```

目前，export 命令能够对外输出的就是三种接口：函数（Functions）， 类（Classes），var、let、const 声明的变量（Variables）。

另外，`export`语句输出的接口，与其对应的值是动态绑定关系，即通过该接口，可以取到模块内部实时的值。
`export`命令可以出现在模块的任何位置，只要处于模块顶层就可以。如果处于块级作用域内，就会报错，下一节的`import`命令也是如此。这是因为处于条件代码块之中，就没法做静态优化了，违背了 ES6 模块的设计初衷。

如果想为输入的变量重新取一个名字，`import`命令要使用`as`关键字，将输入的变量重命名。

```javascript
import { lastName as surname } from './profile.js';
```

`import`命令输入的变量都是只读的，因为它的本质是输入接口。也就是说，不允许在加载模块的脚本里面，改写接口。

```javascript
import {a} from './xxx.js'

a = {}; // Syntax Error : 'a' is read-only;
```
`import`后面的`from`指定模块文件的位置，可以是相对路径，也可以是绝对路径。如果不带有路径，只是一个模块名，那么必须有配置文件，告诉 JavaScript 引擎该模块的位置。

```javascript
import { myMethod } from 'util';
```

上面代码中，`util`是模块文件名，由于不带有路径，必须通过配置，告诉引擎怎么取到这个模块。

注意，`import`命令具有提升效果，会提升到整个模块的头部，首先执行。

为了给用户提供方便，让他们不用阅读文档就能加载模块，就要用到`export default`命令，为模块指定默认输出。

```javascript
// export-default.js
export default function () {
  console.log('foo');
}
```

上面代码是一个模块文件`export-default.js`，它的默认输出是一个函数。

其他模块加载该模块时，`import`命令可以为该匿名函数指定任意名字。

```javascript
// import-default.js
import customName from './export-default';
customName(); // 'foo'
```

上面代码的`import`命令，可以用任意名称指向`export-default.js`输出的方法，这时就不需要知道原模块输出的函数名。需要注意的是，这时`import`命令后面，不使用大括号。

如果在一个模块之中，先输入后输出同一个模块，`import`语句可以与`export`语句写在一起。

```javascript
export { foo, bar } from 'my_module';

// 可以简单理解为
import { foo, bar } from 'my_module';
export { foo, bar };
```