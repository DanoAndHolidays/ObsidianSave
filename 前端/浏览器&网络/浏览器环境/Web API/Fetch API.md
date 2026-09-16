# Fetch API
> Last Format Time：9/16/2026 19:30:37

[MDN 文档：使用 Fetch](https://developer.mozilla.org/zh-CN/docs/Web/API/Fetch_API/Using_Fetch)

---
## 基本请求与错误处理
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

`fetch()` 通常只在请求本身失败（例如网络错误或 URL 不合法）时拒绝 Promise；HTTP 404、500 等错误状态不会自动触发拒绝，因此需要检查 `Response.ok` 或 `Response.status`。

---
## 取消请求
使用 `AbortController` 创建取消信号，将 `controller.signal` 传给 `fetch()`；调用 `controller.abort()` 后，请求会以名为 `AbortError` 的 `DOMException` 拒绝。

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

跨源请求使用 `include` 时，Cookie 仍受 `SameSite` 属性限制，服务端也必须返回允许凭据的 CORS 响应头；因此，`include` 不等于跨站 Cookie 一定会被发送或响应一定能被前端读取。
