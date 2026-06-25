# tRPC 
是一个 TypeScript 优先的 RPC 框架，核心卖点是 端到端类型安全

---
## 简述
你在服务端定义的函数签名，客户端直接就能获得完整的类型推断，不需要手动写 API 类型、不需要 schema生成、不需要 swagger。

用你们项目里的例子来说：
  1. 服务端 (apps/app/src/integrations/trpc/init.ts) 定义了 procedure 类型：
    - publicProcedure — 无需登录
    - protectedProcedure — 需要 ctx.user

  2. Router 里写一个查询大概长这样：
```ts
  // 服务端
  const rulesRouter = router({
    list: protectedProcedure.query(({ ctx }) => rulesService.list(ctx.db)),
  });
```
  
  3. 客户端调用时直接有类型提示：
```ts
  // 前端 — trpc.rules.list.useQuery() 是带类型的
  const { data } = trpc.rules.list.useQuery({ page: 1 });
```

  对比传统做法：传统 REST 需要你定义 OpenAPI schema → 生成类型 →
  两边各写各的，一旦接口改了什么，类型不同步就是线上 bug。tRPC 把这三个环节压缩成了一个。改服务端代码，客户端马上报编译错，不需要中间层。

  你们项目选择 tRPC 配合 TanStack Start（SSR）来做，一个比较关键的好处是 SSR 阶段可以直接在服务端调tRPC，不会有那种"首屏先 loading 一下"的问题。
  
---
## 具体实现
```js
import { createFileRoute } from "@tanstack/react-router";
import { fetchRequestHandler } from "@trpc/server/adapters/fetch";
import { appRouter } from "@/integrations/trpc/router";
import { auth } from "@/integrations/better-auth/auth";

const handleRequest = async (request: Request) => {
  const session = await auth.api.getSession({ headers: request.headers });

  return fetchRequestHandler({
    endpoint: "/api/trpc",
    req: request,
    router: appRouter,
    createContext: () => ({
      session: session ?? null,
    }),
  });
};

export const Route = createFileRoute("/api/trpc/$")({
  server: {
    handlers: {
      GET: ({ request }) => handleRequest(request),
      POST: ({ request }) => handleRequest(request),
    },
  },
});

// 这个文件 = TanStack Start 的路由文件，负责接收所有 /api/trpc/* 请求 → 提取用户身份 → 转交 tRPC 处理。项目里所有的增删改查接口都走这一个门进来。
```

### 第 1-4 行：导入依赖
```typescript
import { createFileRoute } from "@tanstack/react-router";  // TanStack Start 的文件路由
import { fetchRequestHandler } from "@trpc/server/adapters/fetch"; // tRPC 的请求处理器
import { appRouter } from "@/integrations/trpc/router";  // 所有 API 接口的定义
import { auth } from "@/integrations/better-auth/auth";  // 登录认证模块
```

- **`createFileRoute`**：TanStack Start 的约定——文件放在 `routes/api/trpc.$.ts`，自动映射到 `/api/trpc/*` 路由。那个 `$` 是**通配符**，匹配 `/api/trpc/` 后面所有路径。
- **`fetchRequestHandler`**：tRPC 提供的工具函数，把原始的 HTTP 请求翻译成 tRPC 能理解的格式。
- **`appRouter`**：所有业务接口的集合（rules、runs、findings 等），就像一个"接口菜单"。
- **`auth`**：Better Auth 实例，用来检查请求是谁发的。

### 第 6-17 行：核心处理函数
```typescript
const handleRequest = async (request: Request) => {
  // 1️⃣ 从请求头里提取 session，判断用户是否登录
  const session = await auth.api.getSession({ headers: request.headers });

  // 2️⃣ 把请求交给 tRPC 处理
  return fetchRequestHandler({
    endpoint: "/api/trpc",           // API 前缀
    req: request,                     // 原始请求
    router: appRouter,                // 接口菜单
    createContext: () => ({
      session: session ?? null,       // 用户信息（未登录就是 null）
    }),
  });
};
```

流程：
1. **鉴权**：从 HTTP 请求头里提取 session → 知道是谁在调用
2. **转发**：把请求、session、路由表一起交给 tRPC，让它找到对应的接口并执行

### 第 19-26 行：注册路由
```typescript
export const Route = createFileRoute("/api/trpc/$")({
  server: {
    handlers: {
      GET: ({ request }) => handleRequest(request),   // GET 请求走这里
      POST: ({ request }) => handleRequest(request),  // POST 请求走这里
    },
  },
});
```

告诉 TanStack Start："凡是发到 `/api/trpc/*` 的 GET 或 POST 请求，都交给 `handleRequest` 处理"。

---
## 为什么用 `$` 而不是具体路径？
tRPC 的所有接口共用这一个端点（不像传统 REST 那样 `/api/users`、`/api/posts` 各一个路由）。tRPC 通过请求体里的内容区分调用哪个接口，所以 URL 只需要一个通配入口。