# 脚本：async，defer（校验补充版）
> Last Format Time：9/3/2026 10:13:33

> 基于原笔记《脚本：async，defer》整理。重点校正解析器阻塞、渲染阻塞、`DOMContentLoaded`、模块脚本以及动态插入脚本的行为。

---
## 一、普通脚本为什么会影响页面加载
当 HTML 解析器遇到**解析器插入的经典外部脚本**（`<script src="..."></script>`），且该脚本没有 `async` 或 `defer` 时，浏览器通常会暂停 HTML 解析，获取脚本并执行，之后才继续解析后面的 HTML。内联经典脚本也会在解析到它的位置执行。

这会带来两个常见影响：

- 脚本执行时，位于脚本标签后面的 DOM 还没有被解析，因此脚本不能直接查询这些后续节点；
- 脚本的获取和求值会延迟后续 HTML 解析，并可能阻塞渲染。已经解析出的内容是否能先被用户看到，还会受到浏览器渲染时机、CSS、网络和脚本执行时间等因素影响，不能绝对地说“顶部脚本加载前页面完全不可见”。

```html
<p>...content before script...</p>

<script src="https://example.com/long.js"></script>

<!-- 解析器需要等待脚本完成后，才会继续处理这里 -->
<p>...content after script...</p>
```

### 把脚本放在 `body` 末尾
```html
<body>
  ...all content is above the script...

  <script src="https://example.com/app.js"></script>
</body>
```

这样脚本执行时，前面的 DOM 通常已经存在，且脚本对页面后半部分的阻塞影响会降低。但它并没有消除解析器阻塞，而且浏览器直到解析到脚本标签才知道需要获取该脚本；对很长的 HTML 文档，脚本获取可能开始得较晚。将脚本放在底部也不是所有页面的最佳方案，仍应结合 `defer`、模块脚本和实际性能数据决定。

---
## 二、`defer`
对**解析器插入的经典外部脚本**，`defer` 表示：脚本可以在 HTML 解析期间并行获取，但要等文档解析完成后再执行。

```html
<p>...content before script...</p>

<script defer src="https://example.com/app.js"></script>

<!-- HTML 解析可以继续到这里 -->
<p>...content after script...</p>
```

`defer` 经典脚本的主要特征：

- 获取脚本时不会暂停 HTML 解析；
- 脚本在文档解析完成后执行，因此此时页面 DOM 已经构建到解析结束的位置；
- 多个解析器插入的 `defer` 经典脚本按它们在文档中的顺序执行，即使后面的脚本更早下载完成；
- `DOMContentLoaded` 会等待这些脚本获取并执行完成；
- 脚本的执行仍会占用 JavaScript 执行线程，因此不能把 `defer` 理解为“执行过程完全不会影响渲染”；
- 对没有 `src` 的经典内联脚本，`defer` 不起作用；对模块脚本，`defer` 属性本身没有额外效果，因为模块脚本默认采用延迟执行模型。

上述规则中的“按顺序”和“等待 DOM 解析完成”特指**解析器插入的经典外部脚本**，不能无条件推广到动态创建的 `<script>` 元素。

### `DOMContentLoaded` 与 `defer`
```html
<script defer src="https://example.com/app.js"></script>

<script>
  document.addEventListener('DOMContentLoaded', () => {
    console.log('defer 脚本已经执行，DOM 已解析完成');
  });
</script>
```

`DOMContentLoaded` 发生在 HTML 解析完成，并且需要等待的延迟脚本执行完成之后。它不等待图片、普通异步脚本等资源。若页面包含会阻塞 DOMContentLoaded 的样式表，脚本执行时机还可能受到样式表加载影响，因此实际时序应通过浏览器事件和性能面板验证。

---
## 三、`async`
对外部经典脚本，`async` 表示脚本可以在 HTML 解析期间并行获取，并在脚本可用时尽快执行。执行时 HTML 解析可能被短暂暂停；脚本求值也可能暂时占用主线程，所以“不会阻塞页面”应理解为**不会阻塞脚本获取阶段的 HTML 解析**，而不是保证执行阶段完全不影响页面。

```html
<script async src="https://example.com/analytics.js"></script>
```

`async` 脚本的主要特征：

- 不保证与其他 `async` 脚本的执行顺序；
- 不等待其他普通脚本或 `defer` 脚本，也不会让其他脚本等待自己；
- 可能在 HTML 解析完成前执行，也可能在 `DOMContentLoaded` 之后执行；
- 不会因为自身加载完成而阻塞 `DOMContentLoaded`；
- 适合统计、广告、监控等彼此独立且不依赖页面业务脚本顺序的脚本。

如果一个脚本依赖另一个脚本，不能仅因为两个脚本都“能并行下载”就使用 `async`；应改用 `defer`、模块 `import` 或显式的加载完成通知。

---
## 四、三种常见经典脚本加载方式对比
| 写法 | 获取时机 | 执行时机 | 执行顺序 | 是否影响 `DOMContentLoaded` |
|---|---|---|---|---|
| `<script src="..."></script>` | 解析到标签时获取 | 获取完成后立即执行 | 按解析顺序，阻塞解析 | 会影响，直到脚本完成 |
| `<script defer src="..."></script>` | 与解析并行获取 | HTML 解析完成后 | 按文档顺序 | 会等待脚本完成 |
| `<script async src="..."></script>` | 与解析并行获取 | 获取完成后尽快执行 | 加载完成优先，不保证顺序 | 不因它而等待 |

这里的“解析并行获取”指网络获取可以与 HTML 解析重叠，不表示 JavaScript 会在一个独立线程中执行。脚本求值通常仍需要在页面 JavaScript 执行环境中进行，并可能与其他主线程任务竞争。

---
## 五、模块脚本的特殊规则
```html
<script type="module" src="/assets/app.js"></script>
<script type="module" async src="/assets/independent-module.js"></script>
```

- `type="module"` 脚本默认是延迟执行的：模块及其依赖会获取，文档解析完成后再按模块依赖关系执行；不需要额外写 `defer`；
- 模块脚本具有模块作用域，使用 `import`/`export`，并按模块依赖图加载；
- `async` 对模块脚本仍有意义：模块及其依赖获取完成后即可执行，不必等待文档解析完成；多个异步模块之间也不保证执行顺序；
- `defer` 对模块脚本没有额外效果；
- 模块脚本的加载通常采用 CORS 模式，跨源模块资源需要服务器正确返回 CORS 响应头。

因此，现代应用中通常优先使用模块脚本；需要让多个入口脚本按依赖顺序执行时，应通过 `import` 表达依赖关系，而不是依赖多个 `async` 标签的偶然加载顺序。

---
## 六、动态创建的脚本
可以使用 JavaScript 动态创建并插入 `<script>`：

```javascript
function loadScript(src) {
  const script = document.createElement('script');
  script.src = src;
  document.head.append(script);
  return script;
}

const script = loadScript('/assets/feature.js');
script.addEventListener('load', () => {
  console.log('feature.js 已加载并执行');
});
```

对于通过 `document.createElement('script')` 等方式创建的非解析器插入脚本，默认行为通常是异步加载和执行：先准备好的脚本可能先执行，不能依赖插入顺序。通过 `innerHTML` 或 `outerHTML` 写入的 `<script>` 元素通常不会执行；通过 `document.write()` 插入的脚本则属于另一套解析器相关行为，可能是同步的。

### 按插入顺序执行动态脚本
如果确实需要让多个动态创建的经典脚本按加入顺序执行，可以在插入文档前将 `async` DOM 属性设为 `false`：

```javascript
function loadInOrder(src) {
  const script = document.createElement('script');
  script.async = false; // 注意：这是 DOM 属性赋值，不是 HTML 中的 async="false"
  script.src = src;
  document.head.append(script);
  return script;
}

loadInOrder('/assets/vendor.js');
loadInOrder('/assets/app.js');
```

这会使非解析器插入的经典脚本进入有序脚本队列：它们仍然是动态加载的，不会像没有 `async`/`defer` 的解析器插入脚本那样阻塞 HTML 解析，但会按加入顺序执行。它也不等同于 `defer`：具体执行和页面生命周期时机仍取决于脚本何时插入、资源何时可用以及文档当前状态。

另外，HTML 布尔属性只看“是否存在”：`<script async="false">` 仍然表示 `async` 为真。要在 JavaScript 中关闭动态脚本的异步行为，应使用 `script.async = false`，并在设置 `src`、插入文档之前完成设置。

---
## 七、如何选择
### 使用 `defer` 的场景
- 脚本需要访问页面 DOM；
- 多个经典脚本有明确的先后依赖；
- 希望脚本获取与 HTML 解析并行，但在 DOM 解析完成后执行。

```html
<script defer src="/assets/vendor.js"></script>
<script defer src="/assets/app.js"></script>
```

### 使用 `async` 的场景
- 脚本与页面业务逻辑独立；
- 不依赖其他脚本的执行顺序；
- 允许它在 DOM 解析完成前或之后执行；
- 典型例子是统计、广告、第三方监控等。

### 使用模块脚本的场景
- 应用代码有模块依赖；
- 希望用 `import`/`export` 表达依赖关系；
- 希望避免通过多个全局脚本变量手工协调加载顺序。

无论选择哪种方式，都应检查脚本是否真的需要 DOM、是否依赖其他脚本、是否能承受失败或延迟，并使用浏览器 Performance 面板、Network 面板和事件日志验证实际行为。

---
## 八、常见误区
1. **`async` 不等于完全不阻塞。** 它主要避免获取阶段阻塞解析，但下载完成后的脚本执行仍可能暂停解析并占用主线程。
2. **`defer` 不等于“脚本越早执行越好”。** 它把执行推迟到解析完成后，并且可能延迟 `DOMContentLoaded`。
3. **`defer` 不是动态脚本的通用顺序控制器。** 动态脚本应使用模块依赖、Promise、`load`/`error` 事件或 `script.async = false` 等明确机制。
4. **`async="false"` 不是关闭异步。** HTML 布尔属性只要出现就是开启；关闭动态脚本的异步行为应使用 DOM 属性 `script.async = false`。
5. **脚本获取并行不代表脚本执行并行。** 同一页面中的 JavaScript 执行通常仍受执行环境和主线程调度约束。
6. **`DOMContentLoaded` 不等于所有资源都加载完成。** 图片、部分媒体和异步脚本可能仍在加载；需要等待完整页面资源时应使用 `load` 或针对具体资源监听事件。

---
## 参考资料
- [WHATWG HTML：Scripting](https://html.spec.whatwg.org/multipage/scripting.html)
- [MDN：`<script>` 元素](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Reference/Elements/script)
- [MDN：`HTMLScriptElement`](https://developer.mozilla.org/zh-CN/docs/Web/API/HTMLScriptElement)
- [MDN：`DOMContentLoaded` 事件](https://developer.mozilla.org/zh-CN/docs/Web/API/Document/DOMContentLoaded)
- [MDN：JavaScript 模块](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Guide/Modules)
- [MDN：`async` 属性](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/async)
- [MDN：`defer` 属性](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/defer)
