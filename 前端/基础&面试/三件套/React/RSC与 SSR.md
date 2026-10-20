# RSC与 SSR
> Last Format Time：9/16/2026 19:24:51

[[16 斑马智行-全部]]

---
## 核心区别
React Server Components（RSC）和 SSR 都发生在服务器，但它们解决的是不同层面的问题。

可以先记住一句话：

> **SSR 讨论的是「React UI 在哪里生成 HTML」；RSC 讨论的是「组件本身在哪里执行」。**

---
## SSR：Server-Side Rendering
SSR 的目标是：

> 在服务器上先执行 React，提前生成 HTML，再把 HTML 发送给浏览器。

例如：

```jsx
function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      {count}
    </button>
  );
}
```

SSR 时：

```text
Counter
   ↓
服务器执行 React
   ↓
<button>0</button>
   ↓
HTML 发给浏览器
```

浏览器可以立刻看到：

```html
<button>0</button>
```

但此时页面还没有 React 交互能力。

之后浏览器还需要下载：

```text
React
Counter.js
事件处理逻辑
```

然后进行 hydration（水合）：

```text
服务器生成的 HTML
        +
客户端 React Component
        ↓
    hydration
        ↓
获得真正的交互能力
```

因此 SSR 的关键特点是：

```text
组件可以在服务器执行
        ↓
生成 HTML

但是组件 JS 通常仍然需要发送到客户端
        ↓
客户端还会继续运行这个组件
```

所以：

> **SSR 只是把首次渲染提前到了服务器，并没有让组件永久留在服务器。**


# 3. React Server Components

RSC 的目标不同。

Server Component：

> **组件只在服务器执行，它的 JavaScript 代码不会发送到浏览器。**

例如：

```jsx
async function UserList() {
  const users = await db.user.findMany();

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

如果 `UserList` 是 Server Component：

```text
UserList.js
数据库查询
服务器业务逻辑
```

全部留在服务器。

客户端不需要下载：

```text
UserList.js
数据库 SDK
相关服务器逻辑
```

因此：

```text
Server Component

服务器执行：✅
客户端执行：❌
组件代码发送客户端：❌
```

这才是 RSC 和 SSR 最本质的区别。


# 4. SSR 和 RSC 不是竞争关系

不要理解成：

```text
SSR vs RSC
```

它们实际上可以同时存在。

更准确的是两个不同维度。

### 维度一：HTML 在哪里生成？
```text
CSR
→ 浏览器生成

SSR
→ 服务器生成
```

### 维度二：组件在哪里执行？
```text
Server Component
→ 只在服务器执行

Client Component
→ 可以在客户端执行
```

所以 Next.js App Router 中经常实际上是：

```text
RSC
+
SSR
+
Client Component hydration
```


# 5. Client Component 不等于 CSR

例如：

```jsx
'use client';

function Counter() {
  const [count, setCount] = useState(0);

  return <button>{count}</button>;
}
```

`"use client"` 并不是说：

> 这个组件只能在浏览器渲染。

它真正表示的是：

> **这个组件属于 Client Component graph，它的代码需要能够发送到客户端运行。**

Client Component 依然可以参与 SSR：

```text
服务器
   ↓
Counter SSR
   ↓
<button>0</button>
   ↓
发送浏览器
   ↓
下载 Counter.js
   ↓
hydrate
```

因此：

```text
Client Component ≠ CSR
```


# 6. RSC Payload 是什么？

Server Component 执行之后，并不是直接生成 HTML。

它首先产生：

```text
RSC Payload
React Server Component Payload
```

可以把它理解成：

> **React Component Tree 在网络上传输时的一种序列化表示。**

一个非常好用的 mental model 是：

```text
RSC Payload
≈ serialized React tree

HTML
≈ serialized DOM tree
```

二者虽然都是：

```text
服务器生成
   ↓
网络发送
   ↓
客户端消费
```

但描述的是完全不同的抽象层级。


# 7. HTML 与 RSC Payload 的区别

例如：

```jsx
async function Page() {
  const user = await getUser();

  return (
    <main>
      <h1>{user.name}</h1>
      <LikeButton userId={user.id} />
    </main>
  );
}
```

假设：

```text
Page       → Server Component
LikeButton → Client Component
```

HTML 最终可能只是：

```html
<main>
  <h1>Dano</h1>
  <button>Like</button>
</main>
```

HTML 描述的是：

```text
DOM Tree

main
├─ h1
│  └─ "Dano"
└─ button
   └─ "Like"
```

它只能告诉浏览器：

> 页面最后有哪些 DOM。

但是它已经不知道：

```jsx
<LikeButton userId={123} />
```

曾经存在过。

组件这一层的信息已经被压扁成：

```html
<button>Like</button>
```


RSC Payload 则可以保留 React 层面的信息。

概念上可以想象成：

```text
main
├─ h1
│  └─ "Dano"
│
└─ ClientComponentReference
      component: LikeButton
      props:
        userId: 123
```

注意这只是帮助理解的伪结构，并不是实际 RSC 协议格式。

客户端通过 RSC Payload 可以知道：

```text
这里有一个 main

这里有一个 h1

这里还有一个 Client Component：
LikeButton

它对应某个客户端 JS Module

它的 props 是：
{ userId: 123 }
```

所以：

> **HTML 描述 DOM；RSC Payload 描述 React UI Tree。**


# 8. 为什么 RSC Payload 不能直接换成 HTML？

核心原因是：

> HTML 会丢失 React Component 层面的信息。

例如：

```jsx
<Counter initialCount={10} />
```

如果只变成：

```html
<button>10</button>
```

那么客户端只看 HTML，并不知道：

```text
这个 button 来自 Counter

Counter 对应哪个 JS 文件

Counter 的 props 是什么

这个位置需要哪个 Client Component
```

而 RSC Payload 可以表达：

```text
Client Component Reference:
Counter

props:
{
  initialCount: 10
}
```

因此 React 可以重新得到类似：

```jsx
<Counter initialCount={10} />
```

这样的 React Tree 信息。


# 9. Server Component 与 Client Component 在 Payload 中的区别

假设：

```jsx
<Page>
  <Article />
  <LikeButton />
</Page>
```

其中：

```text
Page       → Server Component
Article    → Server Component
LikeButton → Client Component
```

服务器执行：

```text
Page
 │
 ├─ Article
 │    ↓
 │  Server Component 执行
 │    ↓
 │  展开成普通 React Elements
 │
 └─ LikeButton
      ↓
    Client Component
      ↓
    保留 Client Reference
```

所以最终可以粗略理解为：

```text
main
├─ article
│  ├─ h1
│  └─ p
│
└─ ClientReference(LikeButton)
     props:
       articleId: 123
```

这里有一个很重要的现象：

```text
Article 这个组件本身消失了
```

因为它已经在服务器执行完了。

客户端只需要它执行之后产生的 UI 结果。

因此：

```text
Article.js
→ 不需要发送客户端
```

但：

```text
LikeButton
```

需要交互，因此 Payload 中保留它的 Client Component reference，客户端之后加载对应 JS。


# 10. RSC → SSR → Browser 的完整关系

可以把整个过程理解成两层转换。

第一层：

```text
Server Component
       ↓
服务器执行
       ↓
RSC Payload
```

这一层属于：

> React Component → React UI 描述

第二层：

```text
React UI Tree
      ↓
SSR
      ↓
HTML
```

这一层属于：

> React UI → DOM 描述

因此完整 mental model：

```text
        Server Components
               │
               │ RSC Render
               ▼
          RSC Payload
               │
               ▼
          React UI Tree
               │
               │ SSR
               ▼
              HTML
               │
               ▼
            Browser
```

与此同时，RSC Payload 里面还可能存在：

```text
Client Component References
            │
            ▼
     Client JS Modules
            │
            ▼
        Hydration
```


# 11. 最终总结

### SSR
关注：

```text
React UI 在哪里生成 HTML？
```

答案：

```text
服务器
```

但组件通常仍然：

```text
服务器执行一次
+
客户端继续执行
```


### RSC
关注：

```text
组件本身在哪里执行？
```

Server Component：

```text
只在服务器执行
不发送组件 JS
客户端不执行
```


### RSC Payload
它不是 HTML。

可以记成：

```text
HTML
≈ DOM Tree 的序列化描述

RSC Payload
≈ React UI Tree 的序列化描述
```

HTML 表达：

```text
页面最终有哪些 DOM？
```

RSC Payload 表达：

```text
这棵 React UI Tree 是什么？

哪些部分已经是 Server Component 的执行结果？

哪些位置仍然是 Client Component？

Client Component 是谁？

需要传给它什么 props？
```

---
## 一句话记忆

> **SSR 是把 React 的首次 HTML 渲染放到服务器；RSC 是把部分组件永久留在服务器；RSC Payload 则是服务器把“React 层的 UI 结果”传给客户端的格式，而 HTML 是 DOM 层的结果。**

可以进一步浓缩成：

```text
Server Component
      ↓
RSC Payload       ← React 层
      ↓
React Renderer
      ↓
HTML              ← DOM 层
      ↓
Browser DOM
```