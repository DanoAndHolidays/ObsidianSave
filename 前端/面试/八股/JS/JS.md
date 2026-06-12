# JS

### 【Q003】什么是防抖和节流，他们的应用场景有哪些
- **防抖（Debounce）**：在事件触发 n 秒后才执行，如果在 n 秒内再次触发，重新计时。
  - 场景：搜索框输入（等用户停止输入再请求）、窗口 resize 完成后再计算、表单验证
- **节流（Throttle）**：每隔 n 秒只执行一次，稀释执行频率。
  - 场景：滚动事件（scroll）、鼠标移动（mousemove）、页面 resize、按钮连续点击

```javascript
// 防抖
function debounce(fn, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}
// 节流
function throttle(fn, interval) {
  let last = 0;
  return function (...args) {
    const now = Date.now();
    if (now - last >= interval) {
      last = now;
      fn.apply(this, args);
    }
  };
}
```

### 【Q022】如何实现一个简单的 Promise
```javascript
class MyPromise {
  constructor(executor) {
    this.state = 'pending';
    this.value = undefined;
    this.callbacks = [];

    const resolve = (value) => {
      if (this.state !== 'pending') return;
      this.state = 'fulfilled';
      this.value = value;
      this.callbacks.forEach(cb => cb.onFulfilled(value));
    };
    const reject = (reason) => {
      if (this.state !== 'pending') return;
      this.state = 'rejected';
      this.value = reason;
      this.callbacks.forEach(cb => cb.onRejected(reason));
    };
    try { executor(resolve, reject); } catch (e) { reject(e); }
  }

  then(onFulfilled, onRejected) {
    return new MyPromise((resolve, reject) => {
      const handle = () => {
        const cb = this.state === 'fulfilled' ? onFulfilled : onRejected;
        if (!cb) {
          (this.state === 'fulfilled' ? resolve : reject)(this.value);
          return;
        }
        try {
          const result = cb(this.value);
          result instanceof MyPromise ? result.then(resolve, reject) : resolve(result);
        } catch (e) { reject(e); }
      };
      if (this.state === 'pending') {
        this.callbacks.push({ onFulfilled: handle, onRejected: handle });
      } else {
        setTimeout(handle); // 微任务模拟（用 setTimeout 近似）
      }
    });
  }
}
```

### 【Q027】在前端开发中，如何获取浏览器的唯一标识
**没有可靠的方式**。浏览器没有提供获取唯一标识的 API。常见近似方案（各有缺陷）：
1. **fingerprint.js**：综合 Canvas 指纹、WebGL、字体列表、屏幕分辨率、时区等生成设备指纹，可被伪造也不一定唯一
2. **localStorage/cookie 生成 UUID**：不同浏览器、清除缓存后丢失
3. **navigator.userAgent + 屏幕信息**：信息太粗
4. **第三方登录**：最可靠的身份标识
结论：浏览器环境本身没有稳定唯一的设备 ID。

### 【Q031】js 中如何实现 bind
```javascript
Function.prototype.myBind = function (context, ...args1) {
  const fn = this;
  return function (...args2) {
    return fn.apply(context, [...args1, ...args2]);
  };
};
```

### 【Q032】js 中什么是 softbind，如何实现
**SoftBind**：与 bind 类似，但如果调用时 this 是全局对象（window/global）或 undefined，则使用绑定的 context；如果 this 不是全局对象，则保留该 this。
```javascript
Function.prototype.softBind = function (context, ...args1) {
  const fn = this;
  return function (...args2) {
    const ctx = (!this || this === globalThis) ? context : this;
    return fn.apply(ctx, [...args1, ...args2]);
  };
};
```

### 【Q088】如何实现 promise.map，限制 promise 并发数
```javascript
function pMap(arr, mapper, concurrency = Infinity) {
  return new Promise((resolve, reject) => {
    const results = new Array(arr.length);
    let running = 0;
    let index = 0;

    function next() {
      if (index === arr.length && running === 0) {
        return resolve(results);
      }
      while (running < concurrency && index < arr.length) {
        const i = index++;
        running++;
        Promise.resolve(mapper(arr[i], i))
          .then(val => { results[i] = val; })
          .catch(reject)
          .finally(() => { running--; next(); });
      }
    }
    next();
  });
}
// 使用：pMap(urls, url => fetch(url), 3).then(console.log)
```

### 【Q102】有没有用 npm 发布过 package，如何发布
```bash
# 1. 初始化
npm init
# 2. 登录 npm
npm login
# 3. 发布
npm publish
# 4. 更新版本号（遵循 semver）
npm version patch/minor/major
# 5. 再次发布
npm publish
```

关键配置：package.json 中的 name、version、main（入口文件）、files（需要发布的文件）、license。可使用 `.npmignore` 排除文件。推荐使用 np 工具辅助发布（自动检查、运行测试）。

### 【Q137】js 代码压缩 minify 的原理是什么
1. **删除空白和注释**：去除空格、换行、制表符、注释（不改变语义）
2. **缩短变量名**：将长变量名、函数名替换为 a、b、c 等短名（UglifyJS/Terser 的安全重命名）
3. **语法树优化**：`if (a) { return true; } return false;` → `return !!a;`
4. **死代码删除**：删除永远不会执行的代码
5. **常量折叠**：`60 * 60 * 24` → `86400`
6. **简化表达式**：`true ? a : b` → `a`
7. **去除 console/debugger**（可选）
主要工具：Terser、UglifyJS、esbuild、SWC。

### 【Q148】关于 JSON，以下代码输出什么
（需要看具体题目代码）JSON 考点：
- `JSON.stringify` 会忽略 undefined、Symbol、函数（对象属性中直接丢弃，数组中转为 null）
- `JSON.parse` 配合 reviver 函数可以自定义解析
- BigInt 无法被 JSON.stringify（会报错）
- 循环引用会报错
- Date 对象会被转为 ISO 字符串

### 【Q168】在 js 中如何把类数组转化为数组
```javascript
// 方法1：Array.from（推荐）
const arr = Array.from(arrayLike);

// 方法2：展开运算符
const arr = [...arrayLike];

// 方法3：Array.prototype.slice.call
const arr = [].slice.call(arrayLike);
const arr = Array.prototype.slice.call(arrayLike);

// 方法4：for 循环 + push（最简单直接）
const arr = [];
for (let i = 0; i < arrayLike.length; i++) arr.push(arrayLike[i]);
```

### 【Q169】Array(100).map(x => 1) 结果是多少
结果是 **一个长度为 100 的空数组**（所有元素为 empty，map 不执行）。
`Array(100)` 创建长度为 100 的稀疏数组，元素未被初始化（empty slots），map 只遍历实际存在的元素，跳过 empty slots。
```javascript
// 要填充，先用 fill
Array(100).fill(0).map(x => 1); // [1, 1, 1, ...]
// 或用 Array.from
Array.from({ length: 100 }, () => 1);
```

### 【Q177】如何在 url 中传递数组
```javascript
// 方案1：key=val1&key=val2（最常见，服务端框架大多支持）
?tags=js&tags=html&tags=css
// URLSearchParams 读取时会合并为数组

// 方案2：逗号分隔
?tags=js,html,css

// 方案3：JSON 编码
?data=encodeURIComponent(JSON.stringify([1,2,3]))

// 方案4：带下标的参数
?arr[0]=1&arr[1]=2&arr[2]=3

// URLSearchParams 获取
const params = new URLSearchParams(location.search);
params.getAll('tags'); // ['js', 'html', 'css']
```

### 【Q181】如何实现 compose 函数，进行函数合成
```javascript
// 从右到左执行（pipe 是左到右）
function compose(...fns) {
  return function (value) {
    return fns.reduceRight((acc, fn) => fn(acc), value);
  };
}

// 用法
const double = x => x * 2;
const add1 = x => x + 1;
const compute = compose(double, add1);
compute(5); // double(add1(5)) = 12

// pipe（从左到右）
const pipe = (...fns) => value => fns.reduce((acc, fn) => fn(acc), value);
```

### 【Q196】前端中遇到过处理二进制的场景吗
- 文件上传下载（Blob、ArrayBuffer）
- 图片处理/压缩/裁剪（Canvas + ArrayBuffer）
- WebSocket 二进制消息
- 音视频流处理（Web Audio API、WebRTC）
- 生成 Excel/PDF 文件（SheetJS 等）
- 协议缓冲区（Protocol Buffers）数据解析
- Web Worker 中处理大数据
- 加密/哈希计算（Web Crypto API、SubtleCrypto）

### 【Q197】什么是 TypedArray
TypedArray 是一组操作 ArrayBuffer 的视图类型：
- `Int8Array`、`Uint8Array`、`Uint8ClampedArray`
- `Int16Array`、`Uint16Array`
- `Int32Array`、`Uint32Array`
- `BigInt64Array`、`BigUint64Array`
- `Float32Array`、`Float64Array`

它们操作的是原始的二进制缓冲区（ArrayBuffer），不是普通 JS 数组。优势：固定类型、内存紧凑、处理二进制数据高效、与 WebGL/Canvas/Web Audio API 等原生 API 直接交互。

### 【Q198】如何实现类似 lodash.get 函数
```javascript
function get(obj, path, defaultValue) {
  const keys = Array.isArray(path) ? path : path.replace(/\[(\d+)\]/g, '.$1').split('.');
  let result = obj;
  for (const key of keys) {
    if (result == null) return defaultValue;
    result = result[key];
  }
  return result === undefined ? defaultValue : result;
}
// get({a: {b: [0, {c: 1}]}}, 'a.b[1].c') → 1
```

### 【Q201】js 中什么是可选链操作符，如何访问数组
**可选链操作符（`?.`）**：安全地访问深层嵌套属性，遇到 null/undefined 时短路返回 undefined 而不报错。
```javascript
const name = user?.profile?.name; // user 或 profile 为 null/undefined 时不报错
// 访问数组
const first = arr?.[0];
// 调用函数
const result = obj.method?.();
// 动态属性
const val = obj?.['key' + suffix];
```

### 【Q202】如何实现一个深拷贝 (cloneDeep)
```javascript
function cloneDeep(obj, map = new WeakMap()) {
  if (obj === null || typeof obj !== 'object') return obj;

  // 处理循环引用
  if (map.has(obj)) return map.get(obj);

  // 处理 Date、RegExp 等特殊对象
  if (obj instanceof Date) return new Date(obj);
  if (obj instanceof RegExp) return new RegExp(obj.source, obj.flags);
  if (obj instanceof Map) {
    const copy = new Map();
    map.set(obj, copy);
    obj.forEach((v, k) => copy.set(k, cloneDeep(v, map)));
    return copy;
  }
  if (obj instanceof Set) {
    const copy = new Set();
    map.set(obj, copy);
    obj.forEach(v => copy.add(cloneDeep(v, map)));
    return copy;
  }

  const result = Array.isArray(obj) ? [] : Object.create(Object.getPrototypeOf(obj));
  map.set(obj, result);
  Reflect.ownKeys(obj).forEach(key => {
    result[key] = cloneDeep(obj[key], map);
  });
  return result;
}
```

### 【Q220】请简述一下 event loop
JS 是单线程的，Event Loop 是其异步机制的核心。

执行顺序：
1. 执行同步代码（调用栈）
2. 调用栈清空后，检查**微任务队列**（Promise.then、MutationObserver、queueMicrotask）
3. 执行完所有微任务后，从**宏任务队列**取出一个任务（setTimeout、setInterval、I/O、UI rendering、MessageChannel）
4. 执行该宏任务，然后再次清空微任务队列
5. 重复循环

**关键**：微任务在每次宏任务执行完后全部清空，宏任务一次只取一个。

### 【Q228】如何实现一个 flatMap 函数 (头条)
```javascript
// flatMap = map + flat(1)
function flatMap(arr, fn) {
  return arr.reduce((acc, item, index) => {
    const value = fn(item, index, arr);
    return acc.concat(Array.isArray(value) ? flatMap(value, x => x) : [value]);
  }, []);
}

// 简单版
function flatMap(arr, fn) {
  return arr.reduce((acc, item, index) => acc.concat(fn(item, index, arr)), []);
}
// 或
Array.prototype.flatMap = function (fn) {
  return this.map(fn).flat(1);
};
```

### 【Q230】如何裁剪图片 (情景：选择头像)
```javascript
// 前端裁剪核心步骤
async function cropImage(file, cropArea) {
  // 1. 读取文件
  const img = new Image();
  img.src = URL.createObjectURL(file);
  await new Promise(r => img.onload = r);

  // 2. 在 Canvas 上绘制裁剪区域
  const canvas = document.createElement('canvas');
  canvas.width = cropArea.width;
  canvas.height = cropArea.height;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(img, cropArea.x, cropArea.y, cropArea.width, cropArea.height, 0, 0, cropArea.width, cropArea.height);

  // 3. 导出为 Blob
  return new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg', 0.9));
}
// 库：react-cropper、cropperjs
```

### 【Q240】如何实现一个 async/await
这是 Generator + Promise 的语法糖：
```javascript
// 自动执行 Generator 的函数（co 库的核心）
function asyncToGenerator(generatorFunc) {
  return function (...args) {
    const gen = generatorFunc.apply(this, args);
    return new Promise((resolve, reject) => {
      function step(key, arg) {
        let result;
        try {
          result = gen[key](arg);
        } catch (error) {
          return reject(error);
        }
        const { value, done } = result;
        if (done) return resolve(value);
        Promise.resolve(value).then(
          val => step('next', val),
          err => step('throw', err)
        );
      }
      step('next');
    });
  };
}
```

### 【Q241】如何使用 async/await 实现 Promise.all 的效果
```javascript
async function asyncAll(promises) {
  const results = [];
  for (let i = 0; i < promises.length; i++) {
    results[i] = await promises[i];
  }
  return results;
}
// 但这样是串行的！要并行：
async function asyncAll(promises) {
  const results = [];
  // 同时启动所有 promise，然后 await 结果
  const pending = promises.map((p, i) =>
    Promise.resolve(p).then(v => { results[i] = v; })
  );
  await Promise.all(pending);
  return results;
}
```

### 【Q243】有没有遇到 js 捕捉不到异常堆栈信息的情况
常见情况：
1. **跨域脚本**：从 CDN 加载的 JS 报错只能捕获 `"Script error."`，没有堆栈。解决方案：`crossorigin="anonymous"` + 服务端 CORS 头
2. **Promise 内部异常**：没有 .catch 的 rejected promise，需监听 `unhandledrejection` 事件
3. **setTimeout/事件回调**：异常会在事件循环的其他回合抛出，需要内部的 try-catch
4. **异步函数**：需要 async/await 自己的 try-catch
5. **eval / new Function**：错误堆栈可能不完整
6. **Source Map 缺失**：线上压缩代码难以映射到源码

### 【Q245】有没有用过 Promise.allSettled() ，它是干什么的
`Promise.allSettled()` 等待所有 Promise 完成（无论成功或失败），返回每个 Promise 的结果数组。
```javascript
const results = await Promise.allSettled([p1, p2, p3]);
// results = [
//   { status: 'fulfilled', value: 1 },
//   { status: 'rejected', reason: Error('failed') },
//   { status: 'fulfilled', value: 3 },
// ]
```
与 `Promise.all` 的区别：all 有任何一个失败就立即 reject，而 allSettled 等所有完成。场景：批量请求后展示成功/失败状态、数据统计导出。

### 【Q249】使用 js 实现一个 lru cache
```javascript
class LRUCache {
  constructor(capacity) {
    this.capacity = capacity;
    this.cache = new Map();
  }

  get(key) {
    if (!this.cache.has(key)) return -1;
    const value = this.cache.get(key);
    this.cache.delete(key);
    this.cache.set(key, value); // 移到末尾（最近使用）
    return value;
  }

  put(key, value) {
    if (this.cache.has(key)) this.cache.delete(key);
    this.cache.set(key, value);
    if (this.cache.size > this.capacity) {
      // Map 的 keys() 返回插入顺序，第一个是最不常用的
      this.cache.delete(this.cache.keys().next().value);
    }
  }
}
```

### 【Q253】cookie 有哪些字段
同 Q546。Name/Value、Domain、Path、Expires/Max-Age、Secure、HttpOnly、SameSite。

### 【Q263】你们项目的测试覆盖率是怎么做的
- 使用 Istanbul (nyc / c8) 进行覆盖率统计
- 覆盖率指标：语句（Statement）、分支（Branch）、函数（Function）、行（Line）
- 工具：Jest/Cypress/Playwright 中集成 Istanbul 插件
- CI 环境设置最低覆盖率阈值，覆盖率下降报 warning
- 输出报告：json、lcov、html text 等格式
- 按文件/目录查看未覆盖代码行

### 【Q266】bind 与 call/apply 的区别是什么
- **call/apply**：**立即执行**函数。`fn.call(thisArg, arg1, arg2)`，apply 参数用数组 `fn.apply(thisArg, [arg1, arg2])`
- **bind**：**返回一个新函数**，不立即执行。新函数执行时 this 绑定为 bind 的第一个参数，可预设部分参数（柯里化）

### 【Q272】如何查看你们 JS 项目中应采用的 node 版本
1. **package.json** 中 `engines` 字段：`{ "engines": { "node": ">=16.0.0" } }`
2. **.nvmrc** 文件：让 nvm 自动切换
3. **.node-version** 文件（fnm/nodenv 使用）
4. **volta** 在 package.json 中 `"volta": { "node": "16.14.0" }`
5. **查看 .github/workflows/*.yml** 等 CI 配置中使用的 Node 版本
6. `nvm use` 或 `fnm use` 读取 .nvmrc

### 【Q285】有没有做过裁剪头像图片的需求，如何实现
同 Q230。前端裁剪流程：
1. 选择文件 → FileReader 读取为 Data URL
2. 将图片渲染到裁剪区域（显示给用户选择区域）
3. 用户拖拽/缩放选择裁剪区域（可用 cropperjs 等库）
4. Canvas 绘制裁剪区域 → `ctx.drawImage(img, sx, sy, sw, sh, dx, dy, dw, dh)`
5. `canvas.toBlob()` 导出裁剪后的图片
6. 上传 Blob/File 到服务器

### 【Q291】简述 node/v8 中的垃圾回收机制
V8 垃圾回收分为两代：
1. **新生代（Young Generation）**：存活时间短的对象，使用 Scavenge 算法（Cheney 复制算法），快但空间折半
2. **老生代（Old Generation）**：存活时间长的对象，使用 Mark-Sweep（标记-清除）和 Mark-Compact（标记-整理）
   - 标记阶段：从根（全局对象、栈变量）出发标记所有可达对象
   - 清除阶段：回收未标记的内存
   - 整理阶段：移动存活对象减少碎片

**触发时机**：内存达到阈值、增量标记（incremental marking）避免长暂停。Node 中可通过 `--max-old-space-size` 调整堆大小。

### 【Q305】如何删除项目中没有使用到的 package
```bash
# 1. depcheck 检查未使用的依赖
npx depcheck

# 2. npm-check 交互式清理（推荐）
npx npm-check -u
# 或
npx npm-check --skip-unused

# 3. 手动检查
# 根据 depcheck 输出，手动 npm uninstall <package>

# 4. webpack-bundle-analyzer 分析打包后代码
# 决定哪些是可以移除的
```

### 【Q312】如何实现 Promise.race
```javascript
Promise.myRace = function (promises) {
  return new Promise((resolve, reject) => {
    for (const p of promises) {
      Promise.resolve(p).then(resolve, reject);
    }
  });
};

// 加超时控制的 race（常见场景）
function raceWithTimeout(promises, timeout) {
  return Promise.race([
    ...promises,
    new Promise((_, reject) => setTimeout(() => reject('timeout'), timeout))
  ]);
}
```

### 【Q338】js 中在 new 的时候发生了什么
1. 创建一个空对象
2. 将空对象的 `[[Prototype]]` 指向构造函数的 `prototype`（`__proto__` 关联原型链）
3. 将构造函数的 `this` 绑定为新对象，执行构造函数
4. 如果构造函数返回了对象，返回该对象；否则返回新创建的对象

```javascript
function myNew(constructor, ...args) {
  const obj = Object.create(constructor.prototype);
  const result = constructor.apply(obj, args);
  return result instanceof Object ? result : obj;
}
```

### 【Q355】什么是 Iterable 对象，与 Array 有什么区别
**Iterable**：实现了 `[Symbol.iterator]` 方法的对象，可以通过 `for...of` 遍历。包括 Array、String、Map、Set、TypedArray、arguments、NodeList 等。

**与 Array 的区别**：
- Array 是 Iterable，但 Iterable 不一定是 Array
- Iterable 没有数组方法（map、filter、reduce 等）
- 可以将 Iterable 转为数组：`[...iterable]` 或 `Array.from(iterable)`

### 【Q357】js 如何全部替代一个子串为另一个子串
```javascript
// ES2021+：replaceAll
'hello hello'.replaceAll('hello', 'hi'); // 'hi hi'

// 正则 + g 标志（通用）
'hello hello'.replace(/hello/g, 'hi');

// split + join（不用正则时推荐，兼容性好）
'hello hello'.split('hello').join('hi');

// 特殊字符需 escape：replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
```

### 【Q377】在 js 中如何实现继承
```javascript
// 1. 原型链继承（ES5）
function Parent() { this.name = 'parent'; }
Parent.prototype.say = function () { console.log(this.name); };
function Child() { Parent.call(this); }  // 继承实例属性
Child.prototype = Object.create(Parent.prototype);  // 继承原型方法
Child.prototype.constructor = Child;

// 2. ES6 Class
class Parent {
  constructor() { this.name = 'parent'; }
  say() { console.log(this.name); }
}
class Child extends Parent {
  constructor() {
    super(); // 调用 parent constructor
  }
}
// extends + super 本质上是基于原型链的语法糖
```

### 【Q384】python 中的 self 与 javascript 中的 this 有何不同
- **Python self**：是方法的第一个参数，显式声明的。对象调用方法时 self 自动传入实例本身。self 是**确定的**（词法作用域可知）。
- **JavaScript this**：由**调用方式**决定（运行时确定）。函数作为对象方法调用时 this 指向该对象，直接调用时 this 指向全局对象（严格模式下为 undefined）。可以 bind/call/apply 改变。箭头函数的 this 使用外层词法的 this。

### 【Q389】以下输出顺序多少 (setTimeout 与 promise 顺序)
标准题目：`setTimeout(() => console.log(1), 0) + Promise.resolve().then(() => console.log(2)) + console.log(3)`
输出：**3 → 2 → 1**

原因：同步代码优先 -> 微任务（Promise.then）-> 宏任务（setTimeout）

### 【Q399】实现一个 once 函数，记忆返回结果只执行一次
```javascript
function once(fn) {
  let called = false, result;
  return function (...args) {
    if (!called) {
      called = true;
      result = fn.apply(this, args);
    }
    return result;
  };
}
// 使用场景：单例初始化、事件处理只执行一次
```

### 【Q402】如何实现一个函数 isPlainObject 判断是否为纯对象
```javascript
function isPlainObject(obj) {
  if (typeof obj !== 'object' || obj === null) return false;
  // 原型为 null 或 constructor 的 prototype 就是 obj 自身
  const proto = Object.getPrototypeOf(obj);
  if (proto === null) return true;
  const Ctor = Object.prototype.hasOwnProperty.call(proto, 'constructor') && proto.constructor;
  return typeof Ctor === 'function' && Ctor instanceof Ctor &&
    Function.prototype.toString.call(Ctor) === Function.prototype.toString.call(Object);
}
// Lodash 的 isPlainObject 核心逻辑
```

### 【Q421】如何实现一个无限累加的 sum 函数
```javascript
// sum(1)(2)(3)() = 6 或 sum(1, 2, 3) = 6 或 sum(1)(2)(3) = 6

// 方案1：柯里化 + 空括号终止
function sum(...args1) {
  let total = args1.reduce((a, b) => a + b, 0);
  return function next(...args2) {
    if (args2.length === 0) return total;
    total += args2.reduce((a, b) => a + b, 0);
    return next;
  };
}
// sum(1)(2)(3)() → 6

// 方案2：利用 valueOf / toString
function sum(a) {
  function f(b) { return sum(a + b); }
  f.valueOf = () => a;
  f.toString = () => String(a);
  return f;
}
// +sum(1)(2)(3) → 6
```

### 【Q422】JS 如何实现一个同步的 sleep 函数
**JS 是单线程的，无法实现真正的同步 sleep 而不阻塞整个线程**。唯一近似方式：
```javascript
// 这个会冻结整个浏览器/进程！仅在极度特殊场景用
function sleep(ms) {
  const start = Date.now();
  while (Date.now() - start < ms) {} // 自旋等待，不推荐
}

// 正确做法：使用异步
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
// await sleep(1000);
// 或 Atomics.wait（SharedArrayBuffer 场景）
```

### 【Q429】实现一个函数用来解析 URL 的 querystring
```javascript
function parseQuery(url) {
  const params = {};
  const search = url.includes('?') ? url.split('?')[1] : url;
  if (!search) return params;
  for (const [key, val] of new URLSearchParams(search)) {
    if (params.hasOwnProperty(key)) {
      params[key] = [].concat(params[key], val);
    } else {
      params[key] = val;
    }
  }
  return params;
}
// parseQuery('?a=1&b=2&a=3') → {a: ['1', '3'], b: '2'}

// URL API 一行写法
const qs = Object.fromEntries(new URL(url).searchParams);
```

### 【Q435】JS 如何实现一个 sleep/delay 函数
```javascript
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

async function demo() {
  console.log('开始');
  await sleep(2000);
  console.log('2秒后');
}
```

### 【Q436】如何实现一个 sample 函数，从数组中随机取一个元素
```javascript
function sample(arr) {
  const index = Math.floor(Math.random() * arr.length);
  return arr[index];
}

// 取多个不重复元素
function sampleSize(arr, n) {
  const shuffled = arr.slice().sort(() => Math.random() - 0.5);
  return shuffled.slice(0, n);
}
```

### 【Q440】实现一个函数用来对 URL 的 querystring 进行编码
```javascript
function encodeQuery(params) {
  const searchParams = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (Array.isArray(value)) {
      value.forEach(v => searchParams.append(key, v));
    } else {
      searchParams.set(key, value);
    }
  }
  return searchParams.toString();
}
// encodeQuery({a: 1, b: [2, 3]}) → 'a=1&b=2&b=3'

// 手动方式
function encodeQuery(params) {
  return Object.entries(params)
    .map(([k, v]) => [].concat(v).map(val => `${encodeURIComponent(k)}=${encodeURIComponent(val)}`).join('&'))
    .join('&');
}
```

### 【Q441】v8 是如何执行一段 JS 代码的
1. **Parser（解析器）**：将源码解析为 AST（抽象语法树）
2. **Ignition（解释器）**：将 AST 编译为字节码并立即执行
3. **TurboFan（优化编译器）**：对热点代码（频繁执行的函数）进行优化编译（JIT），生成优化的机器码
4. **Deoptimization**：如果优化的假设失败（如类型变化），退回字节码
5. **垃圾回收**：Orinoco GC 做增量/并发标记-清除

JIT（Just-In-Time）编译的核心思想：解释执行 + 热点优化。

### 【Q443】实现一个数组扁平化的函数 flatten
```javascript
// 递归版
function flatten(arr, depth = Infinity) {
  return depth > 0
    ? arr.reduce((acc, item) => acc.concat(Array.isArray(item) ? flatten(item, depth - 1) : item), [])
    : arr.slice();
}

// 迭代版（栈）
function flatten(arr) {
  const result = [];
  const stack = [...arr];
  while (stack.length) {
    const next = stack.pop();
    if (Array.isArray(next)) {
      stack.push(...next);
    } else {
      result.unshift(next);
    }
  }
  return result;
}

// 原生：arr.flat(depth) 或 arr.flat(Infinity)
```

### 【Q445】实现一个数组去重函数 unique
```javascript
// Set（最简单，不能去重对象）
const unique = arr => [...new Set(arr)];

// reduce + includes
const unique = arr => arr.reduce((acc, cur) => acc.includes(cur) ? acc : [...acc, cur], []);

// filter + indexOf
const unique = arr => arr.filter((item, index) => arr.indexOf(item) === index);

// 对象数组去重（按某个字段）
const uniqueBy = (arr, key) => [...new Map(arr.map(item => [item[key], item])).values()];
```

### 【Q447】如何实现一个数组洗牌函数 shuffle
```javascript
// Fisher-Yates（Knuth）洗牌算法
function shuffle(arr) {
  const result = arr.slice();
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}
// 时间复杂度 O(n)，公平随机
```

### 【Q449】vue3 中，如何监听数组的变化
Vue3 使用 Proxy（而非 defineProperty）可以直接拦截：
- 数组的索引赋值：`arr[0] = newVal`
- length 修改：`arr.length = 0`
- 方法调用：push、pop、shift、unshift、splice、sort、reverse
Vue2 需要重写数组的这些方法（数组变异方法）。Vue3 的 Proxy 天然支持数组操作。

### 【Q452】现代框架如 React、Vue 相比原生开发有什么优势
1. **声明式编程**：写"想要什么"而非"怎么实现"，DOM 更新自动化
2. **组件化**：复用、封装、组合
3. **虚拟 DOM / 响应式系统**：优化的视图更新
4. **状态管理**：统一的数据流管理
5. **路由**：SPA 前端路由
6. **生态**：大量的工具、UI 库、插件
7. **开发效率**：CLI 脚手架、热更新、DevTools 调试
8. **性能**：自动批量更新、diff 优化

### 【Q453】typeof 与 instanceof 的区别
- **typeof**：返回基础类型字符串。`typeof 1` → `'number'`，`typeof []` → `'object'`（无法区分数组/对象/null）。`typeof null` → `'object'`（历史 bug）。
- **instanceof**：检测构造函数的 prototype 是否出现在对象的原型链上。`[] instanceof Array` → `true`。不能跨 iframe/realm（不同全局上下文有独立的构造函数）。

### 【Q462】JS 如何翻转一个字符串
```javascript
const reverse = str => str.split('').reverse().join('');

// 或用扩展运算符
const reverse = str => [...str].reverse().join('');

// for 循环
function reverse(str) {
  let result = '';
  for (let i = str.length - 1; i >= 0; i--) result += str[i];
  return result;
}
```

### 【Q473】关于模块化，什么是 amd 和 umd
- **AMD**（Asynchronous Module Definition）：异步加载模块（浏览器环境）。代表：RequireJS. `define(['dep'], function(dep) { return module; });`。特点是依赖前置，模块不阻塞加载。
- **UMD**（Universal Module Definition）：通用模块定义，兼容 AMD + CommonJS + 全局变量。典型结构是判断环境（typeof define vs module.exports vs window），选择对应的模块定义方式。让一个包在 Node、浏览器、AMD 环境下都能使用。

### 【Q474】简单介绍以下浏览器中的 module
浏览器原生 ES Module：
```html
<script type="module">
  import { foo } from './module.js';
  // 模块作用域，默认 strict 模式
  // 默认 defer（等 DOM 解析完后执行）
</script>
```
特点：
- 模块作用域，不会污染全局
- 静态导入，支持 Tree Shaking
- 自然支持 `import()` 动态导入
- CORS 限制（不能 import 本地文件）
- `nomodule` 属性可降级兼容不支持 ESM 的浏览器

### 【Q475】什么是 commonjs2
CommonJS 规范，是 Node.js 的模块系统。使用 `require()` 和 `module.exports`。
- **CommonJS1**：社区自发的规范，module.exports
- **CommonJS2**：一般是webpack对 CommonJS 的称呼，指 `module.exports = ...`（而非 `exports.xxx = ...`）
- 本质区别：CJS2 支持 `module.exports = x` 直接替换导出（CJS1 用 `exports.x = ...`）
- 实际中两者混合使用，webpack 导出配置时 `output.libraryTarget: 'commonjs2'`

### 【Q479】前端上传文件时如何读取文件内容
```javascript
const input = document.querySelector('input[type=file]');
input.addEventListener('change', (e) => {
  const file = e.target.files[0];

  // 1. FileReader 读文本
  const reader = new FileReader();
  reader.onload = () => console.log(reader.result);
  reader.readAsText(file); // 文本

  // 2. 读为 ArrayBuffer
  reader.readAsArrayBuffer(file);

  // 3. 读为 Data URL（Base64 预览）
  reader.readAsDataURL(file);

  // 4. 不读取，直接使用 Blob/File 对象
  const url = URL.createObjectURL(file); // 预览图片等
});
```

### 【Q480】你最喜欢的三个 js 库是什么
开放题。常见推荐：
- **lodash**：函数式工具库，性能好
- **dayjs / date-fns**：日期处理
- **immer**：不可变数据结构
- **rxjs**：响应式编程
- **axios / ky**：HTTP 请求
- 根据自己的项目真实回答即可

### 【Q482】现代化前端框架中如何进行调试
1. **浏览器 DevTools**：断点调试、Network 分析、Performance 录制
2. **React DevTools / Vue DevTools**：组件树、state/props 查看
3. **Redux DevTools**：状态变更时间旅行
4. **console.log / console.table / console.trace**
5. **debugger 语句**：代码中断点
6. **Source Map**：线上代码映射到源码调试
7. **VSCode Debugger**：attach 到浏览器
8. **whistle / Charles**：抓包/代理调试

### 【Q489】如何实现一个函数 lodash.merge
```javascript
function merge(target, ...sources) {
  for (const source of sources) {
    for (const key of Object.keys(source)) {
      if (isPlainObject(source[key]) && isPlainObject(target[key])) {
        merge(target[key], source[key]);
      } else if (Array.isArray(source[key]) && Array.isArray(target[key])) {
        // 数组浅合并（Lodash 默认行为），也可改为递归
        target[key] = source[key];
      } else if (source[key] !== undefined) {
        target[key] = source[key];
      }
    }
  }
  return target;
}
```

### 【Q490】如何实现一个 promise.any
```javascript
Promise.myAny = function (promises) {
  let count = 0;
  const errors = new Array(promises.length);
  return new Promise((resolve, reject) => {
    promises.forEach((p, i) => {
      Promise.resolve(p).then(resolve, err => {
        errors[i] = err;
        count++;
        if (count === promises.length) {
          reject(new AggregateError(errors, 'All promises were rejected'));
        }
      });
    });
  });
};
```
与 race 的区别：any 忽略 reject 直到第一个 resolve 或所有 reject。

### 【Q491】如何实现一个 Promise.all
```javascript
Promise.myAll = function (promises) {
  return new Promise((resolve, reject) => {
    const results = new Array(promises.length);
    let count = 0;
    promises.forEach((p, i) => {
      Promise.resolve(p).then(value => {
        results[i] = value;
        count++;
        if (count === promises.length) resolve(results);
      }, reject);
    });
  });
};
```

### 【Q494】如何过滤数组中的 falsy value
```javascript
// falsy: false, 0, '', null, undefined, NaN
const arr = [0, 1, false, '', 'hello', null, undefined, NaN];
const truthy = arr.filter(Boolean);
// [1, 'hello']
```

### 【Q495】如何把一个数组随机打乱
同 Q447，Fisher-Yates 算法。

### 【Q505】JS 中基础数据类型有哪些
- **原始类型**（7 种）：`number`、`string`、`boolean`、`null`、`undefined`、`symbol`、`bigint`
- **引用类型**：Object（包括 Array、Function、Date、RegExp、Map、Set 等）
- 原始类型存在栈中，不可变（immutable），按值传递
- 引用类型存在堆中，按引用地址传递

### 【Q507】如何创建一个数组大小为100，每个值都为0的数组
```javascript
// 方法1：Array.from（推荐）
Array.from({ length: 100 }, () => 0);

// 方法2：fill
new Array(100).fill(0);

// 方法3：扩展 + map
[...Array(100)].map(() => 0);

// 方法4：循环
const arr = [];
for (let i = 0; i < 100; i++) arr.push(0);
```

### 【Q513】有没有使用过 async/await，他们的原理是什么
Async/Await 是 Generator + Promise 的语法糖：
1. `async` 函数总是返回 Promise
2. `await` 暂停函数执行，等待 Promise 解析
3. Babel/TypeScript 编译后是 Generator 自动化执行器（co 库的核心逻辑）
4. JS 引擎原生实现更高效：不再需要 Generator 包装
5. 核心：把异步代码写成同步的代码结构，底层仍是 Promise + 微任务

### 【Q514】什么是闭包，闭包的应用有哪些地方
**闭包**：函数 + 能访问的外部作用域变量。函数内部定义的函数访问了外部函数的变量，即使外部函数执行完毕，这些变量仍被内部函数引用而不会被 GC 回收。

**应用**：
- 封装私有变量（模块化、数据隐藏）
- 函数工厂（柯里化、偏函数）
- 防抖/节流
- 单例模式
- React Hooks（useState、useEffect 利用闭包保存状态）
- 事件回调持有作用域

### 【Q515】关于事件循环，一道异步代码执行输出顺序问题
同 Q389。解题关键：同步 → 微任务（Promise.then、queueMicrotask）→ 宏任务（setTimeout、setInterval）。注意：async 函数中 `await` 之后的部分相当于 Promise.then 的内容（微任务）。还要注意 Promise 构造函数本身是同步执行的。

### 【Q527】解构赋值一个数组，a 取第一项默认值为 3，c取剩下的值组成数组
```javascript
const arr = [];
const [a = 3, ...c] = arr;
// a = 3, c = []

const arr2 = [1, 2, 3, 4];
const [a2 = 3, ...c2] = arr2;
// a2 = 1, c2 = [2, 3, 4]
```

### 【Q528】解构赋值以下对象，他们的值是多少
（需看具体题目）常见解构考点：
- 可嵌套：`const { a: { b } } = obj;`
- 可设默认值：`const { a = 3 } = {};`
- 可重命名：`const { a: b } = { a: 1 }; // b = 1`
- 可与 rest 结合

### 【Q529】Map 与 WeakMap 有何区别
| 维度 | Map | WeakMap |
|------|-----|---------|
| Key 类型 | 任意类型 | 只能是 Object |
| 垃圾回收 | 强引用，key 不被 GC | 弱引用，key 可被 GC 回收 |
| 枚举 | 可遍历（keys/values/entries） | 不可遍历 |
| 大小 | 有 size 属性 | 无 size 属性 |
| 方法 | set/get/has/delete/clear/forEach | set/get/has/delete |

### 【Q539】Javascript 数组中有那些方法可以改变自身，那些不可以
**改变自身（Mutator）**：push、pop、shift、unshift、splice、sort、reverse、copyWithin、fill

**不改变自身（返回新数组）**：map、filter、slice、concat、reduce、every、some、find、findIndex、flat、flatMap、includes、indexOf、join

**需要记的关键**：sort、reverse、splice 会改变原数组，而 slice 不改变。

### 【Q540】如何判断一个数组是否包含某个值
```javascript
// 基本类型
arr.includes(value);          // ES2016，返回 boolean
arr.indexOf(value) !== -1;    // ES5

// 对象数组（按条件）
arr.some(item => item.id === targetId);
arr.find(item => item.id === targetId) !== undefined;
```

### 【Q541】如何判断字符串包含某个子串
```javascript
str.includes(substr);              // ES2015，返回 boolean
str.indexOf(substr) !== -1;        // ES1，返回位置
/pattern/.test(str);               // 正则匹配
str.match(/pattern/);              // 返回匹配结果
str.startsWith(substr);            // 是否以某串开头
str.endsWith(substr);              // 是否以某串结尾
```

### 【Q549】如何判断某一个值是数组
```javascript
Array.isArray(value);  // 最佳选择，能跨 iframe
// 其他方法（有局限性）
value instanceof Array;  // 跨 iframe 失效
Object.prototype.toString.call(value) === '[object Array]';  // 也可靠
Array.isArray = (arg) => Object.prototype.toString.call(arg) === '[object Array]';
```

### 【Q550】简述 Object.defineProperty
定义/修改对象属性的特性：
```javascript
Object.defineProperty(obj, 'name', {
  value: 'John',
  writable: false,       // 是否可写
  enumerable: true,      // 是否可枚举（for...in、Object.keys）
  configurable: false,   // 是否可配置/删除
  get() { return this._name; },  // getter
  set(val) { this._name = val; }  // setter
});
```
Vue2 用它实现响应式（劫持对象属性的 getter/setter），但无法监听新增/删除属性和数组索引直接修改。

### 【Q551】Object.keys 与 Object.getOwnPropertyNames() 有何区别
- **Object.keys()**：返回**自身可枚举**的属性名数组
- **Object.getOwnPropertyNames()**：返回**自身所有**（可枚举 + 不可枚举）的属性名数组（不含 Symbol 属性名）
- **Object.getOwnPropertySymbols()**：返回自身 Symbol 属性名
- **Reflect.ownKeys()**：返回自身所有属性名（可枚举+不可枚举+Symbol），等同于 getOwnPropertyNames + getOwnPropertySymbols

### 【Q561】实现一个 inherits 函数进行继承
```javascript
// Node.js 的 util.inherits 也类似于这个
function inherits(Child, Parent) {
  Child.prototype = Object.create(Parent.prototype);
  Child.prototype.constructor = Child;
  //Node legacy hack: 如果 Parent 是 Error 等特殊类型
  // 通常在 ES5 时代用于简化的 "寄生组合继承"
}
```

### 【Q562】WeakMap 与垃圾回收有何关系
WeakMap 的 key 是**弱引用**。当 key 对象没有其他强引用时，即使 WeakMap 中仍有该 key，GC 也可以回收该 key 对应的内存。WeakSet 类似。

**应用场景**：
- 为 DOM 元素存储私有数据而不用担心内存泄漏
- 缓存计算结果（key 被回收则缓存自动失效）
- Vue 3 的响应式系统用 WeakMap 存储依赖关系

### 【Q566】关于块级作用域，以下代码输出多少，在何时间输出
（需看具体代码）考点：`let/const` 块级作用域（`var` 无块级）、循环中的 `var` 变量提升 + 闭包问题（`for (var i = 0; ...)` → 所有闭包引用同一个 i）、`let` 每次迭代创建新绑定。

### 【Q567】如何逆序一个字符串
同 Q462。

### 【Q568】为何 0.1+0.2 不等于 0.3，应如何做相等比较
**原因**：浮点数用二进制存储，0.1 和 0.2 在二进制中是**无限循环小数**，存储时被截断，相加产生精度误差。0.1 + 0.2 = 0.30000000000000004。

```javascript
// 解决方案
Math.abs(a - b) < Number.EPSILON;  // 同 Number.EPSILON 比较
(a * 10 + b * 10) / 10;             // 转为整数运算（需适用的情况）
a.toFixed(10) === b.toFixed(10);    // 限定位数比较
```

### 【Q569】关于 this 与包装对象，以下输出多少
（需看具体代码）考点：原始类型（string/number/boolean）在调用方法时会被临时包装为对象（String/Number/Boolean），方法执行完后包装对象销毁。严格模式下 this 保持原始值，非严格模式下 this 被转换为包装对象。

### 【Q571】关于类型转化，判断以下代码输出
（需看具体代码）考点：
- `[] + []` → `""`（空数组转空字符串）
- `[] + {}` → `"[object Object]"`
- `{} + []` → `0`（{} 被解析为空代码块，+[] 转为 0）（在某些上下文中也可能为 "[object Object]"）
- `true + true` → `2`
- `1 + '1'` → `'11'`
- `'2' - 1` → `1`

### 【Q572】关于暂时性死域，判断以下代码输出
**暂时性死区（TDZ）**：用 `let/const` 声明的变量，在声明之前不可访问（会抛 ==ReferenceError==），这段区域就是 TDZ。`var` 没有 TDZ（变量提升 + 初始化为 ==undefined==）。

### 【Q573】关于词法作用域，判断以下代码输出
**词法作用域**：函数的作用域在**定义时**确定（不是调用时），由函数书写位置决定。JS 没有动态作用域（除了 this）。考点：嵌套函数访问上一层函数的变量。

### 【Q574】关于 this，判断以下代码输出
（需看具体代码）考点：
1. 函数直接调用 this = undefined（严格模式）或 window（非严格）
2. 方法调用 this = 调用者对象
3. 箭头函数 this = 外层词法的 this（一旦定义，永远不变）
4. call/apply/bind 显式绑定
5. new 构造函数中的 this = 新实例
6. DOM 事件回调中 this = 绑定事件的 DOM 元素

### 【Q575】关于 new，判断以下代码输出
考点：new 操作符的 4 步过程、constructor 返回对象时 new 表达式的值、原型链的建立。

### 【Q577】关于简单的事件循环，判断以下代码输出
同 Q389 / Q515。同步 > 微任务 > 宏任务。

### 【Q581】箭头函数和普通函数的区别
1. **this**：箭头函数没有自己的 this，继承外层词法的 this；普通函数 this 由调用方式决定
2. **arguments**：箭头函数没有 arguments 对象（用 rest 参数代替）
3. **new**：箭头函数不能作为构造函数（不能被 new）
4. **prototype**：箭头函数没有 prototype 属性
5. **generator**：箭头函数不能用作 Generator 函数（不能使用 yield）
6. **语法更短**：适合简单回调

### 【Q591】什么是纯函数
**纯函数**满足两个条件：
1. 相同的输入永远得到相同的输出（确定性）
2. 没有副作用（不修改外部状态、不操作 DOM、不发起网络请求等）

```javascript
// 纯函数
const add = (a, b) => a + b;

// 非纯函数（有副作用）
let count = 0;
const increment = () => ++count;
```
**好处**：可缓存、可测试、可并行、容易推理。React 中强调 pure component，Redux 中 reducer 必须是纯函数。

### 【Q594】给数字添加千位符
```javascript
// 正则
function formatNumber(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// Intl.NumberFormat（原生）
new Intl.NumberFormat('en-US').format(1234567);  // '1,234,567'

// toLocaleString
(1234567).toLocaleString('en-US');  // '1,234,567'
```

### 【Q598】如何实现一个深比较的函数 deepEqual
```javascript
function deepEqual(a, b) {
  if (a === b) return true;
  if (a == null || b == null || typeof a !== 'object' || typeof b !== 'object') {
    return a !== a && b !== b; // NaN 比较
  }
  if (a.constructor !== b.constructor) return false;

  if (a instanceof Date) return a.getTime() === b.getTime();
  if (a instanceof RegExp) return a.toString() === b.toString();

  const keysA = Object.keys(a);
  const keysB = Object.keys(b);
  if (keysA.length !== keysB.length) return false;

  return keysA.every(key => deepEqual(a[key], b[key]));
}
```

### 【Q599】Object.is 与全等运算符( === )有何区别
- `===`：`+0 === -0` 为 `true`，`NaN !== NaN`
- `Object.is`：`Object.is(+0, -0)` 为 `false`，`Object.is(NaN, NaN)` 为 `true`
- 其他情况行为一致

```javascript
// Object.is polyfill
Object.defineProperty(Object, 'is', {
  value(x, y) {
    return x === y ? (x !== 0 || 1 / x === 1 / y) : x !== x && y !== y;
  }
});
```

### 【Q602】如何把对象转化为 key/value 的二维数组
```javascript
Object.entries(obj);  // {a: 1, b: 2} → [['a', 1], ['b', 2]]

// 手动实现不适用原生
function toEntries(obj) {
  return Object.keys(obj).map(key => [key, obj[key]]);
}

// 反向：Object.fromEntries(entries) → 对象
```

### 【Q603】在 JS 中如何监听 Object 某个属性值的变化
```javascript
// 1. Object.defineProperty（Vue2）
let _val = obj.prop;
Object.defineProperty(obj, 'prop', {
  get() { return _val; },
  set(val) { console.log('changed'); _val = val; }
});

// 2. Proxy（Vue3）
const proxy = new Proxy(obj, {
  set(target, key, value) {
    console.log(`${key} changed to ${value}`);
    target[key] = value;
    return true;
  }
});

// 3. getter/setter（class 内定义）
```

### 【Q605】js 中什么是 AsyncIterable
实现了 `[Symbol.asyncIterator]` 的对象，可通过 `for await...of` 异步遍历。每步迭代返回一个 Promise。
```javascript
const asyncIterable = {
  async *[Symbol.asyncIterator]() {
    for (let i = 0; i < 3; i++) {
      await sleep(1000);
      yield i;
    }
  }
};
for await (const value of asyncIterable) {
  console.log(value); // 每秒输出一次
}
// 场景：分页 API、流式数据、Node.js Readable Stream
```

### 【Q606】关于事件循环，仅有 Promise，判断以下代码输出
考点：Promise 构造函数中的代码是**同步**执行的，只有 `.then()/.catch()/.finally()` 中的回调是微任务。注意 then 的链式调用：每个 .then 返回一个新的 Promise，其回调也是微任务。

### 【Q610】了解什么是 JSBridge 吗
JSBridge 是 Native App（iOS/Android）与 WebView 中 JS 之间的通信桥梁。
- **原理**：Native 注入全局对象给 JS，或拦截 URL Scheme
- **Android**：通过 `addJavascriptInterface` 注入对象 或 拦截 `shouldOverrideUrlLoading`
- **iOS**：通过 `WKScriptMessageHandler` 或 URL Scheme
- **请求方向**：JS → Native（调用 Native 方法）、Native → JS（调用 JS 函数）
- **应用**：Hybrid App（H5 调用原生相机、扫码、支付等）、微信小程序

### 【Q618】列举 Number、String、Array、Object、Promise 有哪些 API
- **Number**：isNaN、isFinite、isInteger、isSafeInteger、parseInt、parseFloat、MAX_VALUE、EPSILON
- **String**：length、charAt、includes、indexOf、slice、substring、split、replace、match、trim、startsWith、endsWith、toLowerCase、toUpperCase
- **Array**：push/pop/shift/unshift/splice/slice/concat/join/map/filter/reduce/find/forEach/some/every/includes/indexOf/flat/reverse/sort/fill
- **Object**：keys、values、entries、assign、create、defineProperty、freeze、seal、is、fromEntries
- **Promise**：all、allSettled、race、any、resolve、reject；实例方法 then/catch/finally

### 【Q619】使用 JS 如何生成一个随机字符串
```javascript
// 方法1：Math.random + toString（常用、简短）
Math.random().toString(36).substring(2, 10); // 8 位

// 方法2：crypto.getRandomValues（更安全）
Array.from(crypto.getRandomValues(new Uint8Array(16)), byte =>
  byte.toString(16).padStart(2, '0')
).join(''); // 32 位十六进制字符串

// 方法3：指定字符集
function randomStr(len) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  return Array.from({ length: len }, () => chars[Math.floor(Math.random() * chars.length)]).join('');
}

// 方法4：crypto.randomUUID()
crypto.randomUUID(); // '36b8f84d-...' 唯一的 UUID v4
```

### 【Q622】Number.isNaN 与 globalThis.isNaN 有何区别
- **globalThis.isNaN**：先把参数转为 Number，再判断是否为 NaN。`isNaN('abc')` → true（因为 Number('abc') = NaN）
- **Number.isNaN**：不自带类型转换，只有值严格等于 NaN 才返回 true。`Number.isNaN('abc')` → false
- 建议使用 `Number.isNaN` 避免隐式转换陷阱

### 【Q623】如何判断一个数值为整数
```javascript
Number.isInteger(value); // 最推荐，ES6

// 旧方法
typeof value === 'number' && value % 1 === 0;
Math.floor(value) === value;
parseInt(value) === value;
```

### 【Q630】什么是安全整数，如何判断一个整数是安全整数
JS 整数安全范围：`-(2^53 - 1)` 到 `2^53 - 1`（即 Number.MIN_SAFE_INTEGER 到 Number.MAX_SAFE_INTEGER ≈ ±9007199254740991）。超出这个范围，整数会丢失精度（不能精确表示）。

```javascript
Number.isSafeInteger(value);
Number.MAX_SAFE_INTEGER; // 9007199254740991
// 涉及大整数的场景用 BigInt
const big = 9007199254740992n;
```

### 【Q638】如何把字符串全部转化为小写格式
```javascript
str.toLowerCase();  // 'Hello'.toLowerCase() → 'hello'
str.toLocaleLowerCase('tr'); // 土耳其语等特定字符映射问题
```

### 【Q647】Array 中那些 API 可改变自身
同 Q539。push、pop、shift、unshift、splice、sort、reverse、copyWithin、fill。

### 【Q648】如何把一个数组 Array 转化为迭代器 Iterable
```javascript
// 数组已经实现了 Iterable 接口，直接可迭代
for (const v of arr) {}

// 获取迭代器对象
const iterator = arr[Symbol.iterator]();
iterator.next(); // { value: 1, done: false }

// 如果一定要"转化"为纯迭代器（舍弃数组其他特性）
function* arrayToGenerator(arr) { yield* arr; }
```

### 【Q656】JS 中如何实现 call/apply
```javascript
// call 实现
Function.prototype.myCall = function (context, ...args) {
  context = context == null ? globalThis : Object(context);
  const key = Symbol('fn');
  context[key] = this;
  const result = context[key](...args);
  delete context[key];
  return result;
};

// apply 实现
Function.prototype.myApply = function (context, args) {
  context = context == null ? globalThis : Object(context);
  const key = Symbol('fn');
  context[key] = this;
  const result = context[key](...args);
  delete context[key];
  return result;
};
```

### 【Q661】Number 中最大数、最大安全整数、EPSILON 都是多少，原理是什么
- **Number.MAX_VALUE**：≈ 1.7976931348623157e+308，双精度能表示的最大正数
- **Number.MAX_SAFE_INTEGER**：9007199254740991（2^53 - 1），能精确表示的最大整数
- **Number.EPSILON**：2^-52 ≈ 2.22e-16，1 与大于 1 的最小可表示数之间的差值

原理：双精度浮点数使用 64 位（1 符号位 + 11 指数位 + 52 尾数位），52 位尾数决定了有效精度，所以安全整数范围为 ±(2^53 - 1)。

### 【Q665】JS 如何检测到对象中有循环引用
```javascript
function hasCycle(obj, seen = new WeakSet()) {
  if (obj === null || typeof obj !== 'object') return false;
  if (seen.has(obj)) return true;
  seen.add(obj);
  for (const key of Object.keys(obj)) {
    if (hasCycle(obj[key], seen)) return true;
  }
  return false;
}
// WeakSet 用弱引用，不影响 GC
```

### 【Q666】实现二进制与十进制的互相转化的两个函数
```javascript
// 十进制 → 二进制（字符串）
function dec2bin(dec) { return dec.toString(2); }
// 或手动
function dec2bin(dec) {
  if (dec === 0) return '0';
  let result = '';
  while (dec > 0) {
    result = (dec % 2) + result;
    dec = Math.floor(dec / 2);
  }
  return result;
}

// 二进制 → 十进制
function bin2dec(bin) { return parseInt(bin, 2); }
// 或手动
function bin2dec(bin) {
  let result = 0;
  for (let i = 0; i < bin.length; i++) {
    result = result * 2 + (+bin[i]);
  }
  return result;
}
```

### 【Q668】JS 中异步任务为何分为微任务与宏任务
**设计原因**：快速响应高优先级异步操作。

- **宏任务（Task）**：由宿主环境（浏览器/Node）提供的异步任务：setTimeout、setInterval、I/O、UI rendering、事件回调
- **微任务（Microtask）**：JS 引擎级别的异步任务：Promise.then、MutationObserver、queueMicrotask
- **调度策略**：每个宏任务执行完后，立即清空当前所有微任务（微任务优先级高于下一个宏任务）。这保证能优先处理 Promise 链等关键异步操作。

### 【Q672】什么是原码、补码与反码
- **原码**：最高位符号位（0 正 1 负），其余位为绝对值。如 +5 = 00000101，-5 = 10000101
- **反码**：正数反码 = 原码。负数反码 = 符号位不变，其余取反。如 -5 = 11111010
- **补码**：正数补码 = 原码。负数补码 = 反码 + 1。如 -5 = 11111011
- **为什么用补码**：统一处理加减法（减法用加法实现）、零只有一种表示（补码中 0 唯一）、简化电路设计
- JS 中位运算使用 32 位有符号整数（补码表示）

### 【Q685】如何遍历一个对象
```javascript
// 1. for...in：遍历自身 + 原型链上可枚举的属性
for (const key in obj) {
  if (obj.hasOwnProperty(key)) { /* 只遍历自身属性 */ }
}

// 2. Object.keys：自身可枚举的属性名
Object.keys(obj).forEach(key => console.log(key, obj[key]));

// 3. Object.entries：自身可枚举的键值对
for (const [key, value] of Object.entries(obj)) { }

// 4. Object.values：自身可枚举的属性值
Object.values(obj).forEach(value => console.log(value));

// 5. Object.getOwnPropertyNames：自身所有属性（含不可枚举，不包含 Symbol）
// 6. Reflect.ownKeys：自身所有属性（含 Symbol 和不可枚举）
```

### 【Q688】setTimeout为什么最小只能设置4ms，如何实现一个0ms的setTimeout?
浏览器规范中 5 层嵌套以上的 setTimeout 最小间隔为 4ms（HTML5 规范），不嵌套时允许 0ms（实际浏览器实现通常也限制最低为 1-4ms）。Node.js 中最小为 1ms。

**绕过方式**：
```javascript
// 使用 postMessage 或 MessageChannel 实现接近 0ms 的延迟
function setImmediate(fn) {
  const channel = new MessageChannel();
  channel.port1.onmessage = fn;
  channel.port2.postMessage('');
}

// 或直接在 web worker 中使用 setImmediate polyfill
setTimeout(fn); // 不指定时间等同于 setTimeout(fn, 0)
```

### 【Q689】JS 中如何原生实现 instanceOf
```javascript
function myInstanceOf(obj, Constructor) {
  let proto = Object.getPrototypeOf(obj);
  const prototype = Constructor.prototype;
  while (proto) {
    if (proto === prototype) return true;
    proto = Object.getPrototypeOf(proto);
  }
  return false;
}
```

### 【Q702】return promise 与 return await promise 有何区别
```javascript
async function foo() {
  // return promise：promise 被 resolve 包装，如果 Promise 抛出异常，异常被吞没处理时机稍晚
  return promise;

  // return await promise：await 会在 await 点时捕获异常、并在 async 函数内部
  return await promise; // 微任务稍多了一些，但能正确捕获异常栈
}
```
在 try-catch 中，`return promise` 不会捕获 promise 的 reject，而 `return await promise` 会。

### 【Q703】在 ES6 Class 中，super 的过程中做了什么
1. `super(...)` 调用**父类构造函数**
2. 创建 this（由父类构造函数执行），将 this 绑定到子类实例
3. ES6 Class 要求：在子类构造函数中使用 `this` 前必须先调用 `super()`
4. `super.method()` 调用父类原型上的方法
5. 内部通过 `[[ConstructorKind]]` 区分基类和派生类，派生类使用 `super` 来分配 this

### 【Q704】关于 Promise，判断以下代码的输出
（需看具体代码）考点：Promise 构造函数同步执行、then 是微任务、then 中返回普通值=包裹 resolve、返回 Promise=等待其状态、链式调用的执行顺序。

### 【Q737】如何取得一个数字的小数部分与整数部分
```javascript
// 整数部分
Math.trunc(3.14);       // 3（ES6）
Math.floor(3.14);       // 3
Math.floor(-3.14);      // -4（注意 floor 是向下取整）
~~3.14;                 // 3（位运算取整，32位）

// 小数部分
num % 1;                // 0.14
num - Math.trunc(num);  // 0.14
String(num).split('.')[1]; // '14'（字符串方式）
```

### 【Q743】实现 batchFn 函数，可以批量执行函数
```javascript
function batchFn(fn) {
  let argsList = [];
  let scheduled = false;

  return function (arg) {
    argsList.push(arg);
    if (!scheduled) {
      scheduled = true;
      Promise.resolve().then(() => {
        fn(argsList);
        argsList = [];
        scheduled = false;
      });
    }
  };
}
// 在同一个微任务中多次调用的参数会批量传给 fn
```

### 【Q756】Promise.race 与 Promise.any
- **race**：只要第一个完成的 Promise（无论成功/失败）。比速度。
- **any**：只要第一个成功的 Promise（忽略 reject）。只有全部失败才 reject（AggregateError）。比成功。
- 使用：race 用于超时控制，any 用于多个资源获取最快成功的那个。

### 【Q757】如何解决深拷贝问题中的循环引用
核心：用 **WeakMap** 记录已拷贝的对象。
```javascript
function cloneDeep(obj, map = new WeakMap()) {
  if (obj === null || typeof obj !== 'object') return obj;
  if (map.has(obj)) return map.get(obj); // 遇到循环引用，直接返回已拷贝的引用

  const copy = Array.isArray(obj) ? [] : {};
  map.set(obj, copy);

  for (const key of Object.keys(obj)) {
    copy[key] = cloneDeep(obj[key], map);
  }
  return copy;
}
```
WeakMap 用弱引用，不会阻止 GC 回收源对象。
