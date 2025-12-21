## 1 使用{ }的 JSX

在{}中可以写表达式

### Pitfall
Now you know almost everything about JSX:

-   JSX attributes inside quotes are passed as strings.
-   Curly braces let you bring JavaScript logic and variables into your markup.
-   They work inside the JSX tag content or immediately after `=` in attributes. (注意：TypeScript 类型注解需在 tsx 代码块中使用)
-   `` `{{` `` and `` `}}` `` is not special syntax: it’s a JavaScript object tucked inside JSX curly braces.

# XML (可扩展标记语言)

## 1 标记语言

标记语言，是一种将文本（Text）以及文本相关的其他信息结合起来，展现出关于文档 结构和数据处理细节的电脑文字编码。当今广泛使用的标记语言是超文本标记语言.（HyperText Markup Language，HTML）和可扩展标记语言(Extensible Markup Language XML)。标记语言广泛应用于网页和网络应用程序。

**1、超文本标记语言** **HTML**
(1)写法格式： `<a href="link.html">link</a>`
(2)关注数据的展示与用户体验
(3)标记是预定义、不可扩展的（如 `<a></a>`表示超链接）

**2、可扩展的标记语言** **XML**
(1)写法格式：同 html 样式
(2)仅关注数据本身
(3)标记可扩展，可自定义

```tsx
export default function Square() {
    return (
        <>
            <button className="square">X</button>
            <button className="square">X</button>
        </>
    )
}
```