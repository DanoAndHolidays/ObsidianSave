# HTML

### 【Q019】浏览器中如何实现剪切板复制内容的功能
```javascript
// 现代方案：Clipboard API
await navigator.clipboard.writeText('要复制的文本');

// 传统方案：execCommand（已废弃但兼容性好）
function copyText(text) {
  const textarea = document.createElement('textarea');
  textarea.value = text;
  textarea.style.position = 'fixed'; // 防止页面滚动
  textarea.style.opacity = '0';
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand('copy');
  document.body.removeChild(textarea);
}
```

### 【Q126】localhost:3000 与 localhost:5000 的 cookie 信息是否共享
**不共享**。Cookie 的同源判断中，**端口不同即为不同源**。localhost:3000 和 localhost:5000 端口不同，cookie 无法共享。即使 Domain 相同（localhost），端口不同也构成跨源。==只有 protocol、hostname、port 三者完全一致才是同源。==

### 【Q159】什么是 CSRF 攻击
**跨站请求伪造（Cross-Site Request Forgery）**：攻击者诱导用户在已登录的网站上执行非本意的操作（转账、修改密码等）。利用浏览器**自动携带认证 Cookie**的特性。

**攻击示例**：
1. 用户登录 A 银行网站，浏览器保存了认证 Cookie
2. 用户访问恶意网站 B（或点击钓鱼链接）
3. 网站 B 中有一个隐藏的表单或 img/script 标签发送请求到 A 银行的转账接口
4. 浏览器自动带上 A 银行的 Cookie，转账成功

**防御**：SameSite Cookie、CSRF Token、验证 Referer/Origin、敏感操作二次验证。

### 【Q349】如何把 json 数据转化为 demo.json 并下载文件
```javascript
function downloadJSON(data, filename = 'demo.json') {
  const json = JSON.stringify(data, null, 2);
  const blob = new Blob([json], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
downloadJSON({ name: 'John', age: 30 }, 'data.json');
```

### 【Q461】如何计算白屏时间和首屏时间
```javascript
// 白屏时间：从导航开始到第一次渲染内容的时间
// 一般在 head 中记录
const whiteScreenTime = performance.timing.domLoading - performance.timing.navigationStart;

// 首屏时间（First Contentful Paint）- 使用 PerformanceObserver
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.name === 'first-contentful-paint') {
      console.log('FCP:', entry.startTime);
    }
  }
}).observe({ type: 'paint', buffered: true });

// LCP (Largest Contentful Paint)
new PerformanceObserver((list) => {
  const entries = list.getEntries();
  const lastEntry = entries[entries.length - 1];
  console.log('LCP:', lastEntry.startTime);
}).observe({ type: 'largest-contentful-paint', buffered: true });

// 自定义首屏时间：首屏内容加载完成后的时间
// MutationObserver 监听 DOM 变化 + requestAnimationFrame
```

### 【Q464】什么是重排重绘，如何减少重排重绘
- **重排（Reflow）**：元素几何属性变化（宽高、位置、显示/隐藏），浏览器重新计算布局。代价高。
- **重绘（Repaint）**：外观变化但不影响布局（颜色、背景色、visibility），代价较低。
- **合成（Composite）**：仅 transform/opacity 变化，跳过重排和重绘，性能最好。

**减少策略**：
1. 使用 transform/opacity 做动画（跳过重排/重绘）
2. 批量 DOM 操作：`documentFragment` 或先 `display:none` → 修改 → 恢复
3. 不在一循环中频繁读样式（读 layout 会强制同步重排）
4. `will-change` 提前通知浏览器创建合成层
5. 减少 CSS 嵌套层级，避免复杂的选择器
6. 使用 `requestAnimationFrame` 做视觉更新
7. 虚拟列表处理长列表

### 【Q469】HTML 中的 input 标签有哪些 type
- 文本类：text、password、email、url、tel、search、number、date、time、datetime-local、month、week、color
- 选择类：checkbox、radio、file、range
- 按钮类：submit、reset、button、image
- 其他：hidden（隐藏域）
- HTML5 新增：email、url、tel、number、date 系列、color、search、range

### 【Q470】什么是 Data URL
Data URL 是一种将数据直接嵌入到文档中的 URI 方案。格式：`data:[<mediatype>][;base64],<data>`。
- 优点：减少 HTTP 请求量
- 缺点：增大 HTML/CSS 体积、不会单独缓存、Base64 体积大 33%
- 应用：小图标、内联 Web Font、邮件图片

### 【Q476】textarea 如何禁止拉伸
```css
textarea { resize: none; }
/* 其他值：vertical（只可纵向拉伸）、horizontal（只可横向拉伸）、both（默认） */
```

### 【Q477】在 Canvas 中如何处理跨域的图片
```javascript
// 图片设置 crossOrigin 属性
const img = new Image();
img.crossOrigin = 'anonymous';  // 发送跨域请求但不带 Cookie
img.src = 'https://other-domain.com/image.jpg';
img.onload = () => {
  ctx.drawImage(img, 0, 0);
  // 现在可以将 Canvas 导出为图片（否则 toDataURL/toBlob 会报安全错误）
};

// 服务端需设置 CORS 头
// Access-Control-Allow-Origin: *
```

### 【Q530】HTML 中有哪些语义化标签
- 结构：`<header>`、`<nav>`、`<main>`、`<article>`、`<section>`、`<aside>`、`<footer>`
- 文本：`<h1>-<h6>`、`<p>`、`<blockquote>`、`<pre>`、`<code>`、`<mark>`、`<time>`、`<address>`
- 媒体：`<figure>` + `<figcaption>`、`<picture>` + `<source>`
- 交互：`<details>` + `<summary>`、`<dialog>`
- 列表：`<ul>`/`<ol>`/`<dl>`
- 表格：`<table>` + `<thead>`/`<tbody>`/`<tfoot>` + `<th>`/`<td>`
- 好处：SEO 友好、屏幕阅读器友好、代码可读性高

### 【Q582】什么是 URL 编码 (URL Encode)
将 URL 中的特殊字符转换为 % 开头、后跟两位十六进制数的格式。
- 空格 → `%20`
- 中文等非 ASCII 字符 → UTF-8 编码后每个字节转换为 `%XX`
- `encodeURIComponent()`：对 URL 参数值编码（会编码 = & / ? 等），用于 value
- `encodeURI()`：对整个 URL 编码但保留 URL 结构字符（不编码 : / ? = &），用于完整 URL
