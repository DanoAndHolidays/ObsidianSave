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
    const data = await res.json()
    console.log(data)
}

```
取消请求使用AbortControllor（）

`credentials` 指在使用 `fetch` 发送请求时是否应当发送 `cookie`
- `omit`: 从不发送 `cookie`.
- `same-origin`: 同源时发送 `cookie` (浏览器默认值)
- `include`: 同源与跨域时都发送 `cookie`