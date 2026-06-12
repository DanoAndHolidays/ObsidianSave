# DOM&浏览器 API

### 【Q001】网站开发中，如何实现图片的懒加载
1. **loading="lazy"（原生方案）**：`<img src="img.jpg" loading="lazy">`，浏览器自动懒加载，兼容性已广泛支持。
2. **Intersection Observer API**：
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      observer.unobserve(img);
    }
  });
});
document.querySelectorAll('img[data-src]').forEach(img => observer.observe(img));
```
3. **scroll 事件 + getBoundingClientRect()**（旧方案，需节流）

### 【Q160】如何设置一个 cookie
```javascript
// 基础设置
document.cookie = "username=John; path=/";

// 带过期时间（Max-Age 优先于 Expires）
document.cookie = "username=John; max-age=86400; path=/";  // 24小时
document.cookie = "username=John; expires=Thu, 18 Dec 2025 12:00:00 UTC; path=/";

// 带更多属性
document.cookie = "token=abc123; path=/; domain=.example.com; secure; samesite=strict";

// 封装函数
function setCookie(name, value, days) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
}
```

### 【Q161】如何删除一个 cookie
设置 cookie 的过期时间为**过去的时间**，或 `max-age=0`：
```javascript
document.cookie = "username=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/";
document.cookie = "username=; max-age=0; path=/";
// 注意：domain 和 path 必须与创建时一致才能删除
```

### 【Q210】如何判断当前环境是移动端还是PC端
```javascript
// 方案1：User Agent 检测（最常用）
const isMobile = /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

// 方案2：屏幕宽度 + Touch 事件
const isMobile = window.innerWidth <= 768 && 'ontouchstart' in window;

// 方案3：使用 matchMedia
const isMobile = window.matchMedia('(max-width: 768px)').matches;

// 更可靠的组合判断
function isMobileDevice() {
  return /Mobi|Android/i.test(navigator.userAgent)
    || ('ontouchstart' in window && window.innerWidth <= 1024);
}
```

### 【Q214】input 中监听值的变化是在监听什么事件
- **input 事件**：用户每次输入都触发（包括复制粘贴、拖拽），实时响应。最常用。
- **change 事件**：失去焦点且值发生变化时触发。适合选择框（select）、checkbox 等。
- **keydown/keyup**：只对键盘输入有效，不能捕获粘贴、拖拽等操作。
- **compositionstart/compositionend**：中文输入法等 IME 组合输入的处理，配合 input 事件使用。
- React 中 onChange 实际绑定的是原生 **input** 事件。

### 【Q215】什么是跨域，如何解决跨域问题
**跨域**：浏览器的同源策略限制从一个源加载的脚本与另一个源的资源交互。协议、域名、端口任一不同即为跨域。

**解决方案**：
1. **CORS**（最推荐）：服务端设置 `Access-Control-Allow-Origin` 等头部
2. **反向代理**：Nginx/Webpack DevServer 代理转发，使请求同源
3. **JSONP**：利用 `<script>` 标签不受同源限制，只能 GET，需要服务器配合
4. **postMessage**：iframe/window 之间通信
5. **WebSocket**：不遵守同源策略
6. **document.domain + iframe**（子域名场景，已废弃）

### 【Q284】prefetch 与 preload 的区别是什么
- **preload（预加载）**：`<link rel="preload" href="font.woff2" as="font">`，告诉浏览器**此资源当前页面立即需要**，优先加载。用于关键资源（字体、首屏图片、关键 JS/CSS）。如果不及时使用，浏览器会警告。
- **prefetch（预获取）**：`<link rel="prefetch" href="page2.js">`，告诉浏览器**未来页面可能需要**，浏览器空闲时才加载。用于下一页/未来导航的资源。
- 关键区别：preload 强制浏览器（当前页面），prefetch 是可选的（未来页面），preload 有 as 属性、优先级更高。

### 【Q295】fetch 中 credentials 指什么意思，可以取什么值
控制是否发送 Cookie 和 HTTP 认证信息：
- **omit**：永远不发送/接收 Cookie
- **same-origin**（默认，旧版）：同源请求才发送 Cookie
- **include**：总是发送 Cookie，跨域也发送（服务端需设置 `Access-Control-Allow-Credentials: true` 且 Origin 不能为 *）

### 【Q311】当 cookie 没有设置 maxage 时，cookie 会存在多久
cookie 没有设置 Expires 和 Max-Age 时，被当作**会话 Cookie（Session Cookie）**，浏览器关闭时自动删除。只在浏览器会话期间存在，关闭浏览器标签/窗口即清除。

### 【Q313】在浏览器中如何获取剪切板中内容
```javascript
// 现代浏览器 - Clipboard API（需用户授权）
const text = await navigator.clipboard.readText();

// 图片/富文本
const items = await navigator.clipboard.read();
for (const item of items) {
  if (item.types.includes('image/png')) {
    const blob = await item.getType('image/png');
  }
}

// 旧方案：监听 paste 事件
document.addEventListener('paste', (e) => {
  const text = e.clipboardData.getData('text/plain');
});
```

### 【Q362】js 动画和 css 动画那个性能比较好
（同 Q319）一般 CSS 动画性能更好（GPU 加速、不受主线程阻塞），但关键取决于动画的属性类型（transform/opacity 最佳）。现代 requestAnimationFrame + transform 的 JS 动画性能也很好，且更灵活。

### 【Q374】简单介绍 requestIdleCallback 及使用场景
**requestIdleCallback**：在浏览器空闲时执行低优先级任务，避免阻塞渲染。
```javascript
requestIdleCallback((deadline) => {
  while (deadline.timeRemaining() > 0 && tasks.length > 0) {
    const task = tasks.shift();
    performTask(task);
  }
}, { timeout: 2000 }); // 最多等2秒
```
**场景**：预加载资源、数据上报/埋点、日志发送、缓存清理、次要 UI 更新。React 内部用类似机制做时间切片（Scheduler 包）。

### 【Q411】如何找到当前页面出现次数最多的HTML标签
```javascript
function mostFrequentTag() {
  const all = [...document.querySelectorAll('*')];
  const count = {};
  all.forEach(el => {
    const tag = el.tagName.toLowerCase();
    count[tag] = (count[tag] || 0) + 1;
  });
  const sorted = Object.entries(count).sort((a, b) => b[1] - a[1]);
  return sorted[0];
}
```

### 【Q425】什么是层叠上下文 (stacking context)
同 Q335。层叠上下文决定了元素在 Z 轴上的覆盖顺序。由 position + z-index、opacity、transform、filter 等属性创建。子元素的 z-index 值只在当前层叠上下文中比较。

### 【Q430】如何把 DOM 转化为图片
```javascript
// 方案1：html2canvas 库（最常用）
const canvas = await html2canvas(document.querySelector('#capture'));
const img = canvas.toDataURL('image/png');

// 方案2：SVG foreignObject + Canvas（不用库）
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
  <foreignObject width="100%" height="100%">
    ${new XMLSerializer().serializeToString(element)}
  </foreignObject>
</svg>`;
const img = new Image();
img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svg)));
// 绘制到 Canvas 上再导出
```

### 【Q437】浏览器的剪切板中如何监听复制事件
```javascript
document.addEventListener('copy', (e) => {
  e.preventDefault(); // 阻止默认行为
  const selection = document.getSelection().toString();
  // 可修改复制内容
  e.clipboardData.setData('text/plain', selection + ' - 来源：xxx');
});

document.addEventListener('cut', (e) => {
  // 剪切事件处理
});

document.addEventListener('paste', (e) => {
  const text = e.clipboardData.getData('text/plain');
});
```

### 【Q439】JSONP 的原理是什么，如何实现
**原理**：利用 `<script>` 标签不受同源策略限制。前端动态创建 script 标签，URL 带上回调函数名；服务端返回 `callback(data)` 形式的 JS 代码，浏览器执行后触发回调。

```javascript
// 前端实现
function jsonp(url, callbackName = 'callback') {
  return new Promise((resolve) => {
    const script = document.createElement('script');
    const fnName = `_jsonp_${Date.now()}`;
    window[fnName] = (data) => {
      resolve(data);
      delete window[fnName];
      document.body.removeChild(script);
    };
    script.src = `${url}?${callbackName}=${fnName}`;
    document.body.appendChild(script);
  });
}

// 服务端返回格式
// callback({ name: "John", age: 30 });
```

### 【Q446】如何实现页面文本不可复制
```css
/* CSS 方式（最常用） */
user-select: none;           /* 标准 */
-webkit-user-select: none;   /* Safari/Chrome */
-ms-user-select: none;       /* IE */

/* 配合事件阻止 */
document.addEventListener('copy', (e) => e.preventDefault());
document.addEventListener('contextmenu', (e) => e.preventDefault());  /* 右键菜单 */
// 注意：这只是增加难度，不能完全禁止（F12 开发者工具仍可看到）
```

### 【Q448】异步加载 JS 脚本时，async 与 defer 有何区别 ⌚️
- **普通 `<script>`**：解析暂停 → 下载 + 执行 JS → 继续解析（阻塞）
- **`<script defer>`**：异步下载，**DOM 解析完成后、DOMContentLoaded 前**按顺序执行。保证执行顺序。
- **`<script async>`**：异步下载，**下载完立即执行**（可能阻塞解析），**不保证**执行顺序。
- 适用：defer 适合有依赖关系的脚本；async 适合独立的第三方脚本（如统计、广告）。

要理解 `defer` 和 `async` 是如何处理脚本执行顺序的，关键在于区分它们的**下载方式**与**执行时机**。我们可以把浏览器解析 HTML 的过程想象成“读一本小说”：

 1. `async`（异步加载）：谁先下完谁先跑

- **机制**：当浏览器遇到 `<script async>` 时，它会继续“读小说”（不阻塞 HTML 解析），同时让助手去后台并行下载脚本。一旦某个脚本下载完成，浏览器会**立刻暂停阅读**来执行这个脚本，执行完再继续读。
- **顺序保证**：**完全不保证顺序**。多个 `async` 脚本的执行顺序完全取决于它们的下载速度。哪怕在代码里 `A.js` 写在 `B.js` 前面，只要 `B.js` 体积小、下载快，它就会先执行。
- **适用场景**：仅适用于完全独立、互不依赖的脚本（如统计代码、广告 SDK）。如果它们之间有依赖关系，很容易因为执行顺序错乱而报错。

 2. `defer`（延迟加载）：按出场顺序排队执行

- **机制**：遇到 `<script defer>` 时，浏览器同样在后台并行下载脚本（不阻塞 HTML 解析）。但即使脚本提前下载完了，它也**绝对不会立即执行**，而是乖乖在一旁等待，直到整本“小说”读完（HTML 文档完全解析完毕，DOM 树构建完成后），再统一拿出来执行。
- **顺序保证**：**严格保证顺序**。无论哪个脚本先下载完，浏览器都会严格按照它们在 HTML 中出现的先后顺序依次执行。例如，如果 `vendor.js` 写在 `app.js` 前面，那么一定会先执行 `vendor.js`，再执行 `app.js`。
- **适用场景**：非常适合有依赖关系的业务主逻辑（如 jQuery 及其插件、Vue/React 入口文件），因为它们需要等 DOM 准备好，且必须按顺序执行。

|特性|`async` (异步)|`defer` (延迟)|
|:--|:--|:--|
|**下载阶段**|与 HTML 解析并行，不阻塞|与 HTML 解析并行，不阻塞|
|**执行时机**|下载完成后**立即插队执行**|HTML 解析完毕后**排队执行**|
|**执行顺序**|**无序**（按下载速度快慢决定）|**有序**（严格按 HTML 声明顺序）|
|**是否阻塞解析**|执行时会阻塞 HTML 解析|下载和执行均不阻塞 HTML 解析|

简单来说：如果你希望脚本尽快运行且不需要管它排在第几个，用 `async`；如果你希望脚本们不打架、乖乖按照你写的顺序排队干活，就用 `defer`。在实际开发中，如果拿不准该用哪个，选择 `defer` 通常是更安全稳妥的做法。

### 【Q454】load 事件与 DomContentLoaded 事件的先后顺序
- **DOMContentLoaded**：HTML 解析完成，DOM 树构建完毕（不等待 CSS/图片/iframe）-> **先触发**
- **load**：页面所有资源（图片、CSS、iframe 等）全部加载完成 -> **后触发**
- 顺序：`DOMContentLoaded` → `load`（DOMContentLoaded 一定先于 load 触发）

### 【Q455】React/Vue 中的 router 实现原理如何
前端路由两种模式：
1. **Hash 模式**：监听 `hashchange` 事件（URL 中 # 后面的部分变化），兼容性好，不会发请求到服务端
2. **History 模式**：使用 HTML5 History API（`pushState`/`replaceState` + `popstate` 事件），URL 更美观。需服务端配置 fallback（所有路径返回 index.html），否则刷新 404

### 【Q463】前端如何实现文件上传功能
```javascript
// HTML
<input type="file" id="upload" multiple>

// JS - FormData 方式
const input = document.getElementById('upload');
input.addEventListener('change', async (e) => {
  const file = e.target.files[0];
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch('/upload', { method: 'POST', body: formData });
});

// 大文件分片上传
const chunkSize = 1024 * 1024; // 1MB
for (let i = 0; i < file.size; i += chunkSize) {
  const chunk = file.slice(i, i + chunkSize);
  const fd = new FormData();
  fd.append('chunk', chunk);
  fd.append('index', i / chunkSize);
  await fetch('/upload/chunk', { method: 'POST', body: fd });
}
// 最后请求合并分片
await fetch('/upload/merge', { method: 'POST', body: JSON.stringify({ filename: file.name }) });
```

### 【Q472】什么是 HTML 的实体编码 (HTML Entity Encode)
将 HTML 中的特殊字符转换为对应的实体编码，防止被解析为 HTML 标签。

| 字符 | 实体编码 |
|------|----------|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `&` | `&amp;` |
| `"` | `&quot;` |
| `'` | `&#x27;` / `&apos;` |
| 空格 | `&nbsp;` |

用途：防止 XSS、展示 HTML 代码片段、显示特殊符号。

### 【Q493】如何取消请求的发送
```javascript
// 1. fetch + AbortController（推荐）
const controller = new AbortController();
fetch('/api', { signal: controller.signal });
// 取消
controller.abort();

// 2. XMLHttpRequest
const xhr = new XMLHttpRequest();
xhr.open('GET', '/api');
xhr.send();
// 取消
xhr.abort();

// 3. Axios（基于 CancelToken）
const source = axios.CancelToken.source();
axios.get('/api', { cancelToken: source.token });
source.cancel('取消请求');
```

### 【Q542】DOM 中如何阻止事件默认行为，如何判断事件否可阻止？
```javascript
// 阻止默认行为
element.addEventListener('click', (e) => {
  e.preventDefault(); // 阻止默认行为（链接跳转、表单提交等）
});

// 判断是否可阻止
element.addEventListener('click', (e) => {
  if (e.cancelable) { // 判断事件是否可取消
    e.preventDefault();
  }
});
```
- `e.cancelable`：true 表示可阻止默认行为（如 click、submit、keydown）
- passive 事件监听器中的 touch/wheel 事件不可阻止

### 【Q543】什么是事件冒泡和事件捕获
DOM 事件传播三个阶段：
1. **捕获阶段**：从 window → document → ... → 目标元素的父元素（从外向内）
2. **目标阶段**：到达目标元素本身
3. **冒泡阶段**：从目标元素 → ... → window（从内向外）

默认使用冒泡阶段处理事件。`addEventListener('click', fn, true)` 使第三个参数为 true 则使用捕获阶段。

### 【Q544】什么是事件委托，e.currentTarget 与 e.target 有何区别
**事件委托**：利用事件冒泡，在父元素上绑定事件，通过 e.target 判断实际点击的子元素。减少绑定次数，支持动态添加元素。

```javascript
// 事件委托示例
ul.addEventListener('click', (e) => {
  if (e.target.tagName === 'LI') {
    console.log('点击了：', e.target.textContent);
  }
});
```

- **e.target**：触发事件的元素（最深的被点击元素）
- **e.currentTarget**：绑定事件监听器的元素（即 this）

### 【Q545】关于事件捕获和冒泡，以下代码输出多少
需要看具体题目代码。通用解题思路：
1. 先看 addEventListener 第三个参数：false/不传=冒泡，true=捕获
2. 捕获阶段从外到内执行，冒泡阶段从内到外
3. `e.stopPropagation()` 可阻止继续传播
4. 目标元素上按绑定顺序执行（不区分捕获/冒泡）

### 【Q546】浏览器中 cookie 有哪些字段
- **Name/Value**：键值对（必填）
- **Domain**：生效域名，默认当前域名，设为 `.example.com` 则子域名也共享
- **Path**：生效路径，默认当前路径
- **Expires/Max-Age**：过期时间
- **Secure**：仅 HTTPS 发送
- **HttpOnly**：禁止 JS 访问（document.cookie 不可见），防 XSS
- **SameSite**：Strict/Lax/None，防 CSRF
- **Size**：每个 Cookie 最大约 4KB

### 【Q548】DOM 中 Element 与 Node 有何区别
- **Node**：DOM 树中所有节点的基类。包括元素节点（1）、文本节点（3）、注释节点（8）、文档节点（9）等。
- **Element**：继承自 Node（`Element extends Node`），特指 HTML/SVG 元素节点（nodeType === 1）。
- Element 有 Node 没有的功能：`querySelector`、`getAttribute`、`classList`、`children` 等
- 所有 Element 都是 Node，但不是所有 Node 都是 Element（如文本节点、注释节点）

### 【Q555】sessionStorage与localStorage有何区别
| 维度 | localStorage | sessionStorage |
|------|-------------|----------------|
| 生命周期 | 永久（除非手动删除） | 页面会话期间（关闭标签即删除） |
| 作用域 | 同源所有标签共享 | 同源但仅限于当前标签 |
| 大小 | 约 5-10MB | 约 5-10MB |
| 新标签打开 | 共享数据 | 不共享（新标签创建新会话） |
| API | 相同 | 相同 |

### 【Q556】如何封装一个支持过期时间的 localStorage
```javascript
const storage = {
  set(key, value, ttl) { // ttl 单位秒
    const item = {
      value,
      expire: Date.now() + ttl * 1000
    };
    localStorage.setItem(key, JSON.stringify(item));
  },
  get(key) {
    const raw = localStorage.getItem(key);
    if (!raw) return null;
    const item = JSON.parse(raw);
    if (Date.now() > item.expire) {
      localStorage.removeItem(key);
      return null;
    }
    return item.value;
  }
};

// 使用
storage.set('token', 'abc123', 3600); // 1小时过期
storage.get('token'); // 过期返回 null
```

### 【Q558】如何统计当前页面出现的所有标签
```javascript
function countAllTags() {
  const all = document.querySelectorAll('*');
  const map = new Map();
  all.forEach(el => {
    const tag = el.tagName.toLowerCase();
    map.set(tag, (map.get(tag) || 0) + 1);
  });
  return [...map.entries()].sort((a, b) => b[1] - a[1]);
}
```

### 【Q559】如何监听 localStorage 的变动
```javascript
// storage 事件：在其他标签页/iframe 修改 localStorage 时触发（同源下）
window.addEventListener('storage', (e) => {
  console.log(e.key);      // 变动的 key
  console.log(e.oldValue);
  console.log(e.newValue);
  console.log(e.url);      // 哪个页面触发的
});
// 注意：当前页面自身的修改不会触发此事件！
// 要监听当前页面的修改，需 monkey-patch setItem
const origSetItem = localStorage.setItem;
localStorage.setItem = function(key, value) {
  const event = new CustomEvent('localStorageChange', { detail: { key, value } });
  window.dispatchEvent(event);
  origSetItem.call(localStorage, key, value);
};
```

### 【Q565】浏览器中事件有哪些属性与方法
- **属性**：`type`、`target`、`currentTarget`、`eventPhase`、`bubbles`、`cancelable`、`defaultPrevented`、`timeStamp`、`isTrusted`
- **鼠标事件**：`clientX/Y`、`pageX/Y`、`screenX/Y`、`button`、`altKey/ctrlKey/shiftKey/metaKey`
- **键盘事件**：`key`、`code`、`keyCode`（已废弃）、`altKey/ctrlKey/shiftKey/metaKey`
- **方法**：`preventDefault()`（阻止默认行为）、`stopPropagation()`（阻止冒泡）、`stopImmediatePropagation()`（阻止当前元素上的其他监听器）

### 【Q570】浏览器中如何读取二进制信息
```javascript
// 1. FileReader
const reader = new FileReader();
reader.readAsArrayBuffer(file); // 读取为 ArrayBuffer
reader.onload = () => console.log(reader.result);

// 2. Blob API
const blob = new Blob([data], { type: 'application/octet-stream' });
const arrayBuffer = await blob.arrayBuffer();
const text = await blob.text();

// 3. Response (fetch)
const res = await fetch('/file.bin');
const buf = await res.arrayBuffer();
const view = new Uint8Array(buf);

// 4. FileReader 多种读取方式
reader.readAsArrayBuffer(file); // ArrayBuffer
reader.readAsBinaryString(file); // 二进制字符串（已废弃）
reader.readAsDataURL(file);    // Base64 DataURL
reader.readAsText(file);       // 文本
```

### 【Q595】React 中监听 input 的 onChange 事件的原生事件是什么
React 的 onChange 监听的是原生 **input** 事件（不是原生的 change 事件）。React 合成事件系统中，onChange 对应原生的 input 事件（实时触发），而原生 change 事件需要在失焦时才触发。这样设计是为了提供更一致的跨浏览器行为。

### 【Q596】在浏览器中点击 a 标签保存为文件如何做
```javascript
// 方案1：Blob + a 标签 download 属性
function download(content, filename, type = 'text/plain') {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url); // 释放内存
}

// 方案2：Canvas to 图片下载
canvas.toBlob(blob => {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'image.png'; a.click();
});
```

### 【Q646】如何禁止打开浏览器控制台
**几乎不可能完全禁止**。常见手段（均可轻易绕过）：
1. 监听 F12、Ctrl+Shift+I、Ctrl+Shift+J 等快捷键
2. 利用 `debugger` 无限循环（检测到 DevTools 打开时不断 `debugger`）
3. 利用 `console.log` + 检测 `console` 对象的 getter 行为
4. 检测窗口尺寸变化（DevTools 打开会改变视口）
5. `Object.defineProperty(window, 'console', { get: ... })`
**结论**：前端只能提高门槛，无法真正阻止。

### 【Q667】简述下 WebWorker，它如何进行通信
**Web Worker** 在独立的后台线程中运行 JS，不阻塞主线程（UI 线程）。
- 不能操作 DOM、不能访问 window 的部分 API
- 通过 **postMessage** 通信（消息是拷贝的，非共享）
- 可做：复杂计算、数据处理、加密、图像处理等

```javascript
// 主线程
const worker = new Worker('worker.js');
worker.postMessage({ type: 'calc', data: [1, 2, 3] });
worker.onmessage = (e) => console.log('结果:', e.data);
worker.terminate(); // 关闭

// worker.js
self.onmessage = (e) => {
  const result = heavyCalc(e.data);
  self.postMessage(result);
};
```

### 【Q671】浏览器中监听事件函数 addEventListener 第三个参数有那些值
第三个参数可以是：
- **boolean**：`true` = 捕获阶段，`false` = 冒泡阶段（默认，可选）
- **options 对象**：
  - `capture`：是否捕获阶段
  - `once`：只触发一次
  - `passive`：true 表示不会调用 `preventDefault()`，提升滚动性能
  - `signal`：AbortSignal，用于移除事件监听器

```javascript
el.addEventListener('click', fn, { once: true, passive: true });
// signal 方式移除
const controller = new AbortController();
el.addEventListener('click', fn, { signal: controller.signal });
controller.abort(); // 移除监听
```

### 【Q675】浏览器中 Frame 与 Event Loop 的关系是什么
每个浏览器标签页都有一个独立的事件循环（Event Loop），但同源标签可能共享渲染进程（Site Isolation 之前）。每个 frame（iframe）在主线程中与主页面共享同一个 Event Loop。Web Worker 有自己独立的 Event Loop。

简化理解：
- 1 个标签页 = 1 个浏览器进程中的渲染进程
- 1 个渲染进程 = 1 个主线程（Event Loop）+ 多个 Worker 线程（各自有 Event Loop）
- iframe 与主页面共享主线程的 Event Loop

### 【Q726】浏览器中如何使用原生的 ESM
```html
<!-- type="module" 开启 ESM -->
<script type="module">
  import { add } from './math.js';
  // ESM 默认 defer（等 DOM 解析完后执行）
</script>

<!-- 也可以引用外部模块 -->
<script type="module" src="./app.js"></script>

<!-- importmap（映射裸模块标识符） -->
<script type="importmap">
{
  "imports": {
    "lodash": "https://cdn.skypack.dev/lodash-es"
  }
}
</script>
```

### 【Q755】简述 WebWorker API
除了专用 Worker（Dedicated Worker），还有：
- **SharedWorker**：多个页面/iframe 共享同一个 Worker 实例，通过 port 通信
- **Service Worker**：充当网络代理，拦截请求，实现缓存、离线、推送通知（PWA 核心）
- **Worklet**：轻量级 Worker，如 PaintWorklet（CSS Houdini）、AudioWorklet
- Worker 限制：无 DOM 访问、无 window、无 localStorage（但可用 IndexedDB）、通过 postMessage 通信
