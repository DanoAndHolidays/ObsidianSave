# Monorepo 设计分析

本文档剖析本项目的 Monorepo 架构设计，并沉淀可复用的设计方法论。

---
## 项目全景
### 1. 目录结构
```
daedalus/
├── apps/                    # 可部署的应用（2 个）
│   ├── app/                 # TanStack Start SSR 前端 (:9431)
│   └── server/              # Hono REST API (:9434)
│
├── packages/                # 共享库（11 个）
│   ├── db-schema/           # Drizzle ORM 表定义（叶节点）
│   ├── db/                  # DAO 数据访问层
│   ├── ai/                  # LLM 调用封装
│   ├── agent/               # Agent 编排逻辑
│   ├── services/            # 业务逻辑层
│   ├── schemas/             # Zod 校验 schema
│   ├── shared/              # 共享常量
│   ├── logger/              # 日志工具
│   ├── ui/                  # shadcn/ui 组件 + cn() 工具
│   ├── typescript-config/   # 共享 tsconfig
│   ├── oxlint-config/       # 共享 oxlint 规则
│   └── oxc-formatter-config/ # 共享格式化配置
│
├── docs/                    # 项目文档
├── package.json             # 根 package.json (workspaces 定义)
├── turbo.json               # Turborepo 任务编排
├── bun.lock                 # Bun 锁文件
└── CLAUDE.md                # AI 编码助手指令
```

### 2. 顶层工具链选型

| 维度 | 选择 | 角色 |
|------|------|------|
| 包管理器 | **Bun 1.3** (`workspaces`) | 原生 workspace 协议 + 极速安装 |
| 任务编排 | **Turborepo 2.8** | 并行执行、缓存输出、依赖拓扑排序 |
| 类型系统 | **TypeScript 5.9** | 全项目统一版本 |
| Lint | **oxlint** | Rust 编写，毫秒级 |
| 格式化 | **Prettier 3.7** | 统一代码风格 |
| 死代码检测 | **Knip** | 发现未使用导出/依赖 |

工具链全部声明在根 `package.json` 的 `devDependencies`：

```jsonc
// package.json
"devDependencies": {
  "knip": "^6.4.0",
  "oxlint": "^1.59.0",
  "prettier": "^3.7.4",
  "turbo": "^2.8.21",
  "typescript": "5.9.2"
}
```

根目录脚本统一委派给 turbo，由 turbo 并行调度各子包：

```jsonc
"scripts": {
  "build":       "turbo run build",
  "dev":         "turbo run dev",
  "test":        "turbo run test -- --run",
  "lint":        "turbo run lint",
  "check-types": "turbo run check-types",
  "quality":     "turbo run quality",  // 一键质检全项目
  "db:generate": "turbo run db:generate",
  "db:push":     "turbo run db:push"
}
```

---

## 二、核心架构：分层单向依赖

### 依赖拓扑（DAG）

```
db-schema  ← 纯表定义，零内部依赖
   ↓
  db      ← 依赖 db-schema + drizzle-orm
   ↓
services  ← 依赖 db + db-schema + schemas + agent
   ↓
  apps    ← 依赖 services + db + ui + shared（所有 package）
```

完整依赖链（从叶到根）：

```
db-schema → db → services ──→ apps/app (TanStack Start + tRPC)
                    ↑      └─→ apps/server (Hono REST :9434)
                    ai
```

### 核心约束

**规则 1：apps/ 只能依赖 packages/，app 之间不得互相依赖。**

`apps/app` 和 `apps/server` 是两个独立部署单元，各自引用 `@repo/*` 共享包。如果一个模块两个 app 都需要，放 `packages/`。

**规则 2：packages/ 之间的依赖必须形成 DAG，禁止循环。**

一个好的包名就是它的契约：
- `db-schema` → 只定义表结构，不导入任何项目内包
- `db` → 只导入 `db-schema`，提供 DAO
- `services` → 聚合 db + schemas + agent，编排业务

**规则 3：内部包用 `workspace:*` 协议，必须标记 `"private": true`。**

```jsonc
// packages/services/package.json
"dependencies": {
  "@repo/db":        "workspace:*",  // 由包管理器解析为本地路径
  "@repo/db-schema": "workspace:*",
  // ...
}
"private": true  // 防止意外发布到 npm
```

---

## 三、Turborepo 任务编排

### turbo.json 核心配置

```jsonc
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"],                // 先构建所有依赖包
      "inputs": ["$TURBO_DEFAULT$", ".env*"],  // 变更检测范围
      "outputs": ["dist/**", ".next/**"]        // 缓存输出目录
    },
    "test": {
      "dependsOn": ["^test"],
      "outputs": []
    },
    "dev": {
      "cache": false,       // 开发服务器不缓存
      "persistent": true    // 长期运行进程
    }
  }
}
```

### `^build` 语法详解

`^` 是 Turbo 的核心语法——"先构建本包的拓扑依赖"：

```
执行 turbo run build 时：

1. Turbo 读取每个包的 package.json，解析 workspace:* 依赖
2. 构建依赖图：app → services → db → db-schema
3. 按拓扑逆序执行：先 db-schema，再 db，再 services，最后 app
4. 独立包并行执行（如 agent 和 ai 可同时 build）
```

手写 `dependsOn` 时不需要列出每个依赖包名——`^` 自动完成拓扑排序。

### 缓存命中

Turbo 对任务输出做内容寻址缓存：

```
第一次 build → 计算 inputs hash → 写入缓存
第二次 build → 匹配 inputs hash → 直接回放 outputs，跳过执行
```

缓存默认存储在 `node_modules/.cache/turbo`，可通过 `--remote-cache` 分享到团队。

---

## 四、共享配置的 DRY 设计

### TypeScript 配置

将 `tsconfig` 抽取为独立包：

```jsonc
// packages/typescript-config/package.json
{
  "name": "@repo/typescript-config",
  "exports": {
    "./base.json": "./base.json",
    "./react-library.json": "./react-library.json"
  }
}
```

其他包通过 `workspace:*` 引用：

```jsonc
// packages/db/package.json
"devDependencies": {
  "@repo/typescript-config": "workspace:*"
}
```

```jsonc
// packages/db/tsconfig.json
{
  "extends": "@repo/typescript-config/base.json"
}
```

### 同理 oxlint 配置

```
packages/oxlint-config/
├── oxlintrc.json         # React 项目用（apps/app）
└── non-react.oxlintrc.json  # Node 项目用（packages/*）
```

每个包在自己的 `package.json` 中指定：

```jsonc
// packages/db/package.json
"lint": "oxlint --config ../oxlint-config/non-react.oxlintrc.json src/"
```

修改一处配置，13 个子包全部生效。

---

## 五、包导出控制（Barrel Export）

### 规则：每个包通过 `exports` 字段控制 API 面

```jsonc
// packages/db/package.json
"exports": {
  ".": "./src/index.ts",        // 公开 API
  "./dao": "./src/dao/index.ts"  // 子路径导出
}
```

### index.ts 只做 re-export

```typescript
// packages/db/src/index.ts —— 公有契约
export { createDb } from './client'
// 不导出内部实现细节
```

调用方只能通过包名访问公开 API：

```typescript
// ✅ 正确：通过公开 API
import { createDb } from '@repo/db'

// ❌ 禁止：穿透到内部路径
import { something } from '@repo/db/src/internal/secret'
```

---

## 六、代码质量体系

### 每个包的三合一质检链

```jsonc
"quality": "bun run check-types && bun run lint && bun run test"
```

| 步骤 | 命令 | 作用 |
|------|------|------|
| 类型检查 | `tsc --noEmit` | 确保类型安全 |
| Lint | `oxlint` | 代码风格 + 潜在 bug |
| 测试 | `vitest run` | 单元/集成测试 |

### 根目录一键质检

```bash
bun quality    # turbo 并行执行所有子包的 quality
```

Turbo 自动并行调度：db-schema 和 ai 的类型检查可以同时跑，互不阻塞。

### 额外防线

| 工具 | 命令 | 作用 |
|------|------|------|
| Knip | `bun run knip` | 检测未使用的导出和依赖 |
| Prettier | `bun run format` | 统一格式化 |

---

## 七、应用层设计

### apps/app — TanStack Start SSR 前端

```jsonc
// apps/app/package.json
"dependencies": {
  "@repo/db":        "workspace:*",
  "@repo/db-schema": "workspace:*",
  "@repo/services":   "workspace:*",
  "@repo/shared":     "workspace:*",
  "@repo/ui":         "workspace:*",
  // 外部依赖
  "@tanstack/react-start": "...",
  "@trpc/client": "...",
  "zustand": "...",
  "react-hook-form": "...",
}
```

技术栈：TanStack Start (Vite + Nitro SSR + React 19) → tRPC API → Better Auth (GitHub OAuth) → shadcn/ui + Tailwind v4 → Zustand v5。

### apps/server — Hono REST 服务器

独立的 Hono 服务器 (:9434)，为外部 REST API 消费者提供服务。无鉴权。委托给同一 `@repo/services`。

### 两个 app 共享同一套业务逻辑

```
apps/app  ─→ @repo/services ─→ @repo/db ─→ PostgreSQL
apps/server ─→ @repo/services ─→ @repo/db ─→ PostgreSQL
```

services 是唯一的业务逻辑真实来源（single source of truth）。

---

## 八、如何设计一个合理的大仓项目

### 先回答三个根本问题

**① 你的应用有几个可部署单元？**

每一个独立部署、独立启动的进程就是一个 `apps/*`：
- 1 个前端 + 1 个后端 = 2 个 app
- 再加 1 个文档站 + 1 个 CLI = 4 个 app

**② 哪些代码被多个 app 共享？**

关键标准：**一个模块被 ≥2 个 app 用到，它就进 `packages/`**。

常见候选：
- 数据库表定义 → `packages/db-schema`
- API 类型/校验 → `packages/schemas`
- 业务逻辑 → `packages/services`
- UI 组件 → `packages/ui`
- 共享常量 → `packages/shared`

**③ 依赖方向是什么？**

画箭头图，严格保证从叶到根，绝不允许形成循环。

### 十个设计决策

| # | 决策点 | 推荐 | 说明 |
|---|--------|------|------|
| 1 | 包管理器 | **pnpm** 或 **bun** | pnpm 生态最大、依赖隔离最严；bun 速度最快。不推荐新项目用 yarn |
| 2 | 任务编排 | **Turborepo** | 缓存 + 并行 + 配置最简单。Nx 功能强但复杂，Lage 适合大团队 |
| 3 | 版本策略 | 固定版本（小团队） | 统一升级，简单可控。发布 npm 包的场景才需要独立版本 + Changesets |
| 4 | 命名规范 | `@repo/*` | 清晰区分内部包和外部依赖 |
| 5 | 目录结构 | `apps/` + `packages/` | 经典二分法，最易理解。三分法可加 `tools/` |
| 6 | 共享配置 | 抽取为独立包 | 一改全改，消除跨包复制粘贴 |
| 7 | 包导出控制 | `package.json` `"exports"` 字段 | 严格控制公有 API |
| 8 | 循环检测 | Knip + ESLint `import/no-cycle` | CI 中强制阻断 |
| 9 | CI/CD | `turbo prune` | 按变更范围选择性构建，大幅减时 |
| 10 | Docker | 多阶段构建 + `turbo prune` | 每个 app 一个 Dockerfile，只打包需要的依赖 |

### 设计过程

```
第一步：画部署单元
  → 列出所有独立进程 → 每个进程一个 apps/*

第二步：找出共享代码
  → 标记被 ≥2 个 app 使用的模块 → 每个模块一个 packages/*

第三步：画依赖箭头
  → 从 apps 向下追溯到叶节点 → 验证是 DAG，无环

第四步：配置工具链
  → 选包管理器 → 配 workspace → 加 turbo.json → 抽共享配置

第五步：建立质量门禁
  → 每个包配 quality 脚本 → 根 turbo quality → CI 中强制执行
```

### 常见陷阱

**❌ 循环依赖**

```
services → db → services  ← 死锁！
```
解法：抽取共同部分到第三个包，或用依赖反转。

**❌ apps/ 之间互相依赖**

`apps/app` 不能依赖 `apps/server`。共享代码放 `packages/`。

**❌ "厨房水槽" 包**

一个 `@repo/utils` 放 200 个不相关函数。应拆成 `@repo/logger`、`@repo/crypto` 等语义明确的独立包。

**❌ 内部包未标记 `"private": true`**

不打算发布到 npm，忘了加可能导致意外发布。

**❌ TypeScript 版本漂移**

各包用不同 TS 版本。应在根 `package.json` 统一版本，通过共享 tsconfig 约束。

**❌ 过早抽取**

一个模块只被一个地方用时不要急着放 `packages/`。至少等出现第二个消费者再抽取。

### 心法

> **先画依赖图，再建目录树。依赖方向决定可维护性，工具链决定开发体验。**

Monorepo 的价值不在"把代码放在一起"，而在"强制暴露模块边界"。每一个 `package.json` 的 `exports` 字段都是一份契约——它声明了这个包对外的承诺。好的 monorepo 让边界显式化，坏的 monorepo 让边界更加模糊。
