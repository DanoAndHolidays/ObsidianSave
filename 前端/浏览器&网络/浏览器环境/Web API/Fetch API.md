# Fetch API
> Last Format Time：8/13/2026 15:34:12

[MDN 文档：使用 Fetch](https://developer.mozilla.org/zh-CN/docs/Web/API/Fetch_API/Using_Fetch)〔CR-001〕

---
## 基本请求与错误处理
〔CR-002〕

```javascript
export const createFetch = async () => {
    const res = await fetch(
        'https://playlet.zonelian.com/api/playlet/random?page=1&limit=15&zlsj=zlsj',
        {
            method: 'GET',
            headers: {
                'content-type': 'application/json',
                a: 1,
            },
        },
    )
    console.log(res)
    if (!res.ok) {
        throw new Error(`HTTP error: ${res.status}`)
    }
    const data = await res.json()
    console.log(data)
}

```

`fetch()` 通常只在请求本身失败（例如网络错误或 URL 不合法）时拒绝 Promise；HTTP 404、500 等错误状态不会自动触发拒绝，因此需要检查 `Response.ok` 或 `Response.status`。〔CR-003〕

---
## 取消请求
使用 `AbortController` 创建取消信号，将 `controller.signal` 传给 `fetch()`；调用 `controller.abort()` 后，请求会以名为 `AbortError` 的 `DOMException` 拒绝。〔CR-004〕

```javascript
const url = 'https://example.com/data'
const controller = new AbortController()

fetch(url, { signal: controller.signal })
controller.abort()
```

---
## 请求凭据
`credentials` 控制请求是否携带凭据，以及浏览器是否接收响应中的凭据信息。这里的凭据不只包括 Cookie，还包括 TLS 客户端证书和 HTTP 身份验证信息。

- `omit`：请求不携带凭据，并忽略响应中的凭据信息。
- `same-origin`：仅对同源请求发送并接收凭据，是默认值。
- `include`：同源和跨源请求都尝试发送并接收凭据。

跨源请求使用 `include` 时，Cookie 仍受 `SameSite` 属性限制，服务端也必须返回允许凭据的 CORS 响应头；因此，`include` 不等于跨站 Cookie 一定会被发送或响应一定能被前端读取。〔CR-005〕

---
## 内容审核变更记录
### CR-001｜删减去重
- 日期：8/13/2026
- 位置：文首参考资料
- 原内容：连续出现两个内容和目标完全相同的“MDN文档”链接。
- 调整后：保留一个链接，并将链接文字明确为“MDN 文档：使用 Fetch”。
- 原因：删除重复内容，并让链接名称能够说明目标页面。
- 依据：无需外部依据（重复内容清理）。

### CR-002｜流畅性
- 日期：8/13/2026
- 位置：原“二级标题”章节标题
- 原内容：二级标题
- 调整后：基本请求与错误处理
- 原因：原标题是模板占位词，无法概括章节中的 Fetch 请求示例。
- 依据：无需外部依据（标题表意调整）。

### CR-003｜代码修正
- 日期：8/13/2026
- 位置：“基本请求与错误处理”代码示例及其后说明
- 原内容：取得 `Response` 后直接调用 `res.json()`，没有判断 HTTP 状态。
- 调整后：解析响应体前检查 `res.ok`，失败时抛出包含状态码的错误，并补充 Fetch Promise 与 HTTP 错误状态的关系。
- 原因：`fetch()` 不会仅因收到 404、500 等 HTTP 错误状态而拒绝 Promise，直接解析可能把错误响应误当作成功结果。
- 依据：[MDN：Window.fetch()](https://developer.mozilla.org/en-US/docs/Web/API/Window/fetch)、[MDN：Response.ok](https://developer.mozilla.org/en-US/docs/Web/API/Response/ok)

### CR-004｜代码修正
- 日期：8/13/2026
- 位置：“取消请求”章节
- 原内容：取消请求使用 `AbortControllor()`。
- 调整后：改正为 `AbortController`，并补充创建控制器、传入 `signal` 和调用 `abort()` 的完整用法。
- 原因：原构造器名称拼写错误，且没有说明控制器如何与 Fetch 请求关联。
- 依据：[MDN：AbortController](https://developer.mozilla.org/en-US/docs/Web/API/AbortController)

### CR-005｜事实纠错
- 日期：8/13/2026
- 位置：“请求凭据”章节
- 原内容：`credentials` 指在使用 `fetch` 发送请求时是否应当发送 `cookie`；`include` 表示同源与跨域时都发送 `cookie`。
- 调整后：说明 `credentials` 控制请求和响应中的凭据处理，凭据不只包含 Cookie；同时补充 `SameSite` 与 CORS 对跨源凭据请求的限制。
- 原因：原描述把凭据等同于 Cookie，并容易让人误以为设置 `include` 后跨站 Cookie 必然发送且响应必然可读。
- 依据：[MDN：Using the Fetch API - Including credentials](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#including_credentials)、[WHATWG Fetch Standard：credentials mode](https://fetch.spec.whatwg.org/#concept-request-credentials-mode)
