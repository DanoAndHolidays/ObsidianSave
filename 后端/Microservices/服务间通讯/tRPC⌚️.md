# tRPC
**T**ypeScript **R**emote **P**rocedure **C**all 是一种类型安全的 RPC 框架，主要用于 TypeScript 的前后端项目

它的核心思路是：后端定义 procedure 和 router，前端通过服务端 router 的类型推导出请求参数、返回值和错误类型

这解决了前端一个非常熟悉的问题

假设后端返回：
```
{
  "id": 1001,
  "name": "Dano"
}
```

前端一般要手动写接口类型：
```
interface User {
  id: number;
  name: string;
}
```

但是后端突然把 `name` 改成 `username` 了，如果前端类型没有获取 IDL 同步，TypeScript 仍然可能认为 `name` 存在，直到运行时才发现不对劲

tRPC 就是为了减少这种前后端类型不一致的问题，它通常会和 Zod 结合，对输入参数做运行时校验。例如后端定义：
```
const getAnatomy = procedure
  .input(anatomyIdSchema)
  .query(({ input }) => {
    // 查询业务数据
  });
```

前端可以得到类型提示：
```
trpc.anatomy.get.useQuery({
  id: anatomyId,
});
```

如果参数名称、类型或者返回值发生变化，前端在编译阶段就能发现问题

---
## tRPC 具体使用
先在 TypeScript 服务端定义一个 Procedure：
```
// server/router.ts
import { initTRPC } from "@trpc/server"
import { z } from "zod"

const t = initTRPC.create()

export const appRouter = t.router({
  getUser: t.procedure
    .input(z.object({ id: z.number() }))
    .query(({ input }) => {
      return {
        id: input.id,
        name: "Dano",
        age: 22,
      }
    }),
})

export type AppRouter = typeof appRouter
```

接下来客户端通过 tRPC Client 发起调用（假设服务端已经挂载好 HTTP Adapter）：
```
// client.ts
import { createTRPCClient, httpLink } from "@trpc/client"
import type { AppRouter } from "./server/router"

const trpc = createTRPCClient<AppRouter>({
  links: [
    httpLink({
      url: "http://localhost:3000/trpc",
    }),
  ],
})

const user = await trpc.getUser.query({ id: 1001 })

console.log(user.name)
console.log(user.age)
```

有意思的地方来了。

前端没有写 `User` 接口，却能自动推导：
```
type User = {
  id: number
  name: string
  age: number
}
```

假如你写：
```
trpc.getUser.query({ id: "1001" })
```

TypeScript 会在编译检查时提示类型错误，因为服务端定义的 `id` 是 number。

而 `.input(z.object(...))` 使用 Zod 在服务端执行运行时校验，即使恶意客户端绕过 TypeScript，错误数据也不会直接通过验证。

这就是 tRPC 的关键设计：

- TypeScript：编译时类型推导
- Zod 等校验器：运行时参数验证
- HTTP Link：实际执行网络通信

tRPC 把 Procedure 分为 Query、Mutation 和 Subscription，分别用于读取、修改和订阅数据；它也支持通过 `httpBatchLink` 将多个调用批量发送。

---
## tRPC 与 HTTP
tRPC 并没有消除网络请求

它让你写：
```
await trpc.getUser.query({ id: 1001 })
```

但背后依然可能是一个普通 HTTP 请求

---
## tRPC 有什么缺点
它最大的优势，也形成了一定的适用范围

- 依赖 TypeScript 类型生态：如果后端是 Java、Go、Python，就不能直接使用同样的 TypeScript 类型推导模式。
- 跨语言共享契约不如 gRPC 自然：tRPC 主要面向全栈 TS。
- 前后端存在版本协调问题：共享类型可以发现编译期不兼容，但不能自动保证已经部署的客户端和服务端兼容。
- 类型安全不等于运行时安全：认证、授权、输入校验仍然必须在服务端实现

所以，如果你的项目是 `React + Node.js + TypeScript`，tRPC 是一个很值得考虑的方案

但如果是 `React + Spring Boot`，不建议仅仅为了用 tRPC 就重新设计 Java 后端。可以优先考虑 REST + OpenAPI 生成 TypeScript 客户端
