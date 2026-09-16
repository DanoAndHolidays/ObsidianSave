# Zod 使用实践指南
> Last Format Time：7/14/2026 20:56:57

> 本文档基于 Daedalus 项目（Turborepo 单体仓库）中 Zod v4 的实际使用模式编写，涵盖 schema 定义、类型推导、表单校验、环境变量验证、tRPC 输入校验、Agent 工具参数定义等场景。

---
## 目录
1. [基础概念](#1-基础概念)
2. [Schema 定义模式](#2-schema-定义模式)
3. [类型推导：z.infer 与 z.input](#3-类型推导zinfer-与-zinput)
4. [内置校验器与修饰符](#4-内置校验器与修饰符)
5. [Schema 组合与变换](#5-schema-组合与变换)
6. [表单校验（react-hook-form + zodResolver）](#6-表单校验react-hook-form--zodresolver)
7. [环境变量校验](#7-环境变量校验)
8. [tRPC 输入校验](#8-trpc-输入校验)
9. [Agent 工具参数定义（Mastra）](#9-agent-工具参数定义mastra)
10. [Service 层数据校验](#10-service-层数据校验)
11. [运行时安全解析：safeParse](#11-运行时安全解析safeparse)
12. [高级模式](#12-高级模式)
13. [最佳实践总结](#13-最佳实践总结)
14. [反模式与常见错误](#14-反模式与常见错误)

---
## 基础概念
本项目使用 **Zod v4**（`zod/v4`），这是一套 TypeScript 优先的运行时校验库。

### 核心理念
```text
Zod Schema（定义形状 + 校验规则）
       │
       ├─→ z.infer<typeof schema>  →  编译时 TypeScript 类型（单一数据源）
       │
       └─→ schema.parse(data) / schema.safeParse(data)  →  运行时校验
```

**项目铁律：所有类型必须从 Zod schema 派生，禁止手写重复类型。** 这意味着项目中不存在独立的 `types.ts` 文件——类型与校验逻辑永远共存于 schema 文件中。

### 导入方式
```typescript
import { z } from "zod/v4";
```

---
## Schema 定义模式
### 2.1 基本对象 Schema
最基础的模式：用 `z.object({...})` 定义对象结构，每个字段链式调用校验方法。

```typescript
// packages/schemas/src/rule-checklist-schema.ts
import { z } from "zod/v4";

export const ruleChecklistInputSchema = z.object({
  id: z.string(),
  level: z.enum(["code", "module", "architecture"]),
  text: z.string().min(1, "Checklist text is required"),
  sortOrder: z.number().default(0),
  enabled: z.boolean().default(true),
});

export type RuleChecklistInput = z.infer<typeof ruleChecklistInputSchema>;
```

### 要点
- 每个字段独立声明类型和校验
- `.min(1, "自定义错误消息")` 提供友好的错误提示
- `.default(值)` 在输入为 `undefined` 时自动填充默认值

### 2.2 嵌套对象 Schema
```typescript
// packages/schemas/src/archetype-schema.ts
export const conditionSchema = z.object({
  id: z.string(),
  type: z.enum(["text", "archetype_ref"]),
  value: z.string(),
  sortOrder: z.number(),
  dependencies: z.array(z.string()).default([]),
});

export const archetypeCreateSchema = z.object({
  id: z.string(),
  name: z.string().min(1),
  scope: z.enum(["project", "repository", "crate", "page", "service"]),
  conditions: z.array(conditionSchema).min(1, "At least one condition is required"),
  createdAt: z.union([z.date(), z.string()]),
  updatedAt: z.union([z.date(), z.string()]),
});
```

### 要点
- Schema 可以嵌套：`z.array(conditionSchema)`
- 子 schema 先定义，父 schema 引用
- `z.array()` 上也支持 `.min()` / `.max()` 校验

### 2.3 引用其他文件中的 Schema
```typescript
// packages/schemas/src/crate-schema.ts
import { z } from "zod/v4";
import { cratePathInputSchema } from "./crate-path-schema";

export const crateCreateSchema = z.object({
  // ...
  paths: z.array(cratePathInputSchema).default([]),
});
```

**要点：** Schema 是普通 JavaScript 对象，可以跨文件 import/export，与复用普通函数无异。

### 2.4 枚举值模式
```typescript
// 先定义 const 数组（运行时值 + 编译时字面量类型）
export const CrateTypeValues = [
  "package",
  "module",
  "feature",
  "library",
  "service",
  "utility",
  "other",
] as const;

// 在 schema 中使用 z.enum()
export const crateCreateSchema = z.object({
  type: z.enum(CrateTypeValues),
});
```

### 要点
- `as const` 确保 TypeScript 推导出字面量联合类型而非 `string[]`
- 枚举值数组从 schema 包导出，UI 层可以直接遍历生成下拉选项
- 比 TypeScript `enum` 更灵活——可以在运行时遍历

---
## 类型推导：`z.infer` 与 `z.input`
### 3.1 `z.infer` — 推导输出类型
```typescript
const mySchema = z.object({
  name: z.string(),
  age: z.number().default(18),
});

// MyType = { name: string; age: number }
// 注意：age 是 number（非 optional），因为 .default() 保证输出总有值
type MyType = z.infer<typeof mySchema>;
```

```typescript
// 项目中的典型用法
export type Crate = z.infer<typeof crateCreateSchema>;
export type Archetype = z.infer<typeof archetypeCreateSchema>;
export type Rule = z.infer<typeof ruleCreateSchema>;
```

### 3.2 `z.input` — 推导输入类型
**关键区别：** 当 schema 中有 `.default()` 或 `.optional()` 时，`z.input` 与 `z.infer` 不同。

```typescript
// apps/app/src/pages/CratesPage/CrateDialog.tsx
const crateFormSchema = crateCreateSchema.pick({
  name: true,
  type: true,
  responsibility: true,
  metadata: true,
  repositoryId: true,
  archetypeIds: true,
});

// z.input 考虑了 .default()：archetypeIds 在输入时是 optional 的
type CrateForm = z.input<typeof crateFormSchema>;
```

### 对比
| 场景 | `z.infer`（输出） | `z.input`（输入） |
|------|-------------------|-------------------|
| `z.string().default("hello")` | `string` | `string \| undefined` |
| `z.string().optional()` | `string \| undefined` | `string \| undefined` |
| `z.array(z.string()).default([])` | `string[]` | `string[] \| undefined` |

**规则：用 `z.infer` 标注数据/返回值类型，用 `z.input` 标注表单输入/用户输入类型。**

---
## 内置校验器与修饰符
### 4.1 字符串校验
```typescript
z.string()                          // 任意字符串
z.string().min(1)                   // 非空字符串
z.string().min(1, "Name is required") // 带自定义错误消息
z.string().min(8, "Password must be at least 8 characters")
z.string().email("Invalid email address")
z.string().url()                    // 必须是有效 URL
z.string().url().default("https://api.deepseek.com/v1")
```

### 4.2 数字校验
```typescript
import { z } from "zod/v4";
```

### 4.3 布尔值
```typescript
import { z } from "zod/v4";
```

### 4.4 日期与联合类型
```typescript
import { z } from "zod/v4";
```

### 4.5 数组
```typescript
import { z } from "zod/v4";
```

### 4.6 可选与可空
```typescript
import { z } from "zod/v4";
```

### 4.7 枚举
```typescript
import { z } from "zod/v4";
```

### 4.8 describe — 为字段添加描述
```typescript
import { z } from "zod/v4";
```

### 4.9 元组
```typescript
import { z } from "zod/v4";
```

---
## Schema 组合与变换
### 5.1 `.pick()` — 选取部分字段
```typescript
import { z } from "zod/v4";
```

### 5.2 `.omit()` — 排除字段
```typescript
import { z } from "zod/v4";
```

### 5.3 `.partial()` — 所有字段变为可选
```typescript
// packages/schemas/src/rule-checklist-schema.ts
import { z } from "zod/v4";

export const ruleChecklistInputSchema = z.object({
  id: z.string(),
  level: z.enum(["code", "module", "architecture"]),
  text: z.string().min(1, "Checklist text is required"),
  sortOrder: z.number().default(0),
  enabled: z.boolean().default(true),
});

export type RuleChecklistInput = z.infer<typeof ruleChecklistInputSchema>;
```

### 5.4 链式组合
```typescript
// packages/schemas/src/rule-checklist-schema.ts
import { z } from "zod/v4";

export const ruleChecklistInputSchema = z.object({
  id: z.string(),
  level: z.enum(["code", "module", "architecture"]),
  text: z.string().min(1, "Checklist text is required"),
  sortOrder: z.number().default(0),
  enabled: z.boolean().default(true),
});

export type RuleChecklistInput = z.infer<typeof ruleChecklistInputSchema>;
```

**核心模式：Base Schema → Create Schema → Update Schema**

```typescript
// packages/schemas/src/rule-checklist-schema.ts
import { z } from "zod/v4";

export const ruleChecklistInputSchema = z.object({
  id: z.string(),
  level: z.enum(["code", "module", "architecture"]),
  text: z.string().min(1, "Checklist text is required"),
  sortOrder: z.number().default(0),
  enabled: z.boolean().default(true),
});

export type RuleChecklistInput = z.infer<typeof ruleChecklistInputSchema>;
```

### 5.5 `.default()` — 在 tRPC router 中使用运行时默认值
```typescript
// packages/schemas/src/rule-checklist-schema.ts
import { z } from "zod/v4";

export const ruleChecklistInputSchema = z.object({
  id: z.string(),
  level: z.enum(["code", "module", "architecture"]),
  text: z.string().min(1, "Checklist text is required"),
  sortOrder: z.number().default(0),
  enabled: z.boolean().default(true),
});

export type RuleChecklistInput = z.infer<typeof ruleChecklistInputSchema>;
```

**`() => crypto.randomUUID()` 的妙用：** `.default()` 可以接受一个函数，在每次解析时调用以生成动态默认值（如 UUID）。

---
## 表单校验（react-hook-form + zodResolver）
### 6.1 基础模式
```typescript
// packages/schemas/src/rule-checklist-schema.ts
import { z } from "zod/v4";

export const ruleChecklistInputSchema = z.object({
  id: z.string(),
  level: z.enum(["code", "module", "architecture"]),
  text: z.string().min(1, "Checklist text is required"),
  sortOrder: z.number().default(0),
  enabled: z.boolean().default(true),
});

export type RuleChecklistInput = z.infer<typeof ruleChecklistInputSchema>;
```

### 6.2 从业务 Schema 派生表单 Schema
```typescript
// packages/schemas/src/rule-checklist-schema.ts
import { z } from "zod/v4";

export const ruleChecklistInputSchema = z.object({
  id: z.string(),
  level: z.enum(["code", "module", "architecture"]),
  text: z.string().min(1, "Checklist text is required"),
  sortOrder: z.number().default(0),
  enabled: z.boolean().default(true),
});

export type RuleChecklistInput = z.infer<typeof ruleChecklistInputSchema>;
```

### 6.3 手动控制的字段（不通过 register）
```typescript
// packages/schemas/src/rule-checklist-schema.ts
import { z } from "zod/v4";

export const ruleChecklistInputSchema = z.object({
  id: z.string(),
  level: z.enum(["code", "module", "architecture"]),
  text: z.string().min(1, "Checklist text is required"),
  sortOrder: z.number().default(0),
  enabled: z.boolean().default(true),
});

export type RuleChecklistInput = z.infer<typeof ruleChecklistInputSchema>;
```

---
## 环境变量校验
### 7.1 简单环境 Schema
```typescript
// packages/schemas/src/rule-checklist-schema.ts
import { z } from "zod/v4";

export const ruleChecklistInputSchema = z.object({
  id: z.string(),
  level: z.enum(["code", "module", "architecture"]),
  text: z.string().min(1, "Checklist text is required"),
  sortOrder: z.number().default(0),
  enabled: z.boolean().default(true),
});

export type RuleChecklistInput = z.infer<typeof ruleChecklistInputSchema>;
```

### 7.2 复杂环境 Schema（含自定义 refine）
```typescript
// packages/schemas/src/rule-checklist-schema.ts
import { z } from "zod/v4";

export const ruleChecklistInputSchema = z.object({
  id: z.string(),
  level: z.enum(["code", "module", "architecture"]),
  text: z.string().min(1, "Checklist text is required"),
  sortOrder: z.number().default(0),
  enabled: z.boolean().default(true),
});

export type RuleChecklistInput = z.infer<typeof ruleChecklistInputSchema>;
```

### 7.3 使用 safeParse 校验 process.env
```typescript
// packages/schemas/src/rule-checklist-schema.ts
import { z } from "zod/v4";

export const ruleChecklistInputSchema = z.object({
  id: z.string(),
  level: z.enum(["code", "module", "architecture"]),
  text: z.string().min(1, "Checklist text is required"),
  sortOrder: z.number().default(0),
  enabled: z.boolean().default(true),
});

export type RuleChecklistInput = z.infer<typeof ruleChecklistInputSchema>;
```

### 要点
- 应用启动时调用一次，校验失败直接抛错（fail-fast 原则）
- 使用 `safeParse` 而非 `parse`，以便自定义错误消息格式
- `error.issues` 包含所有校验失败的详细信息

---
## tRPC 输入校验
### 8.1 内联 Schema（简单查询）
```typescript
// packages/schemas/src/archetype-schema.ts
export const conditionSchema = z.object({
  id: z.string(),
  type: z.enum(["text", "archetype_ref"]),
  value: z.string(),
  sortOrder: z.number(),
  dependencies: z.array(z.string()).default([]),
});

export const archetypeCreateSchema = z.object({
  id: z.string(),
  name: z.string().min(1),
  scope: z.enum(["project", "repository", "crate", "page", "service"]),
  conditions: z.array(conditionSchema).min(1, "At least one condition is required"),
  createdAt: z.union([z.date(), z.string()]),
  updatedAt: z.union([z.date(), z.string()]),
});
```

### 8.2 复用业务 Schema（创建/更新）
```typescript
// packages/schemas/src/archetype-schema.ts
export const conditionSchema = z.object({
  id: z.string(),
  type: z.enum(["text", "archetype_ref"]),
  value: z.string(),
  sortOrder: z.number(),
  dependencies: z.array(z.string()).default([]),
});

export const archetypeCreateSchema = z.object({
  id: z.string(),
  name: z.string().min(1),
  scope: z.enum(["project", "repository", "crate", "page", "service"]),
  conditions: z.array(conditionSchema).min(1, "At least one condition is required"),
  createdAt: z.union([z.date(), z.string()]),
  updatedAt: z.union([z.date(), z.string()]),
});
```

### 8.3 内联复杂 Schema
```typescript
// packages/schemas/src/archetype-schema.ts
export const conditionSchema = z.object({
  id: z.string(),
  type: z.enum(["text", "archetype_ref"]),
  value: z.string(),
  sortOrder: z.number(),
  dependencies: z.array(z.string()).default([]),
});

export const archetypeCreateSchema = z.object({
  id: z.string(),
  name: z.string().min(1),
  scope: z.enum(["project", "repository", "crate", "page", "service"]),
  conditions: z.array(conditionSchema).min(1, "At least one condition is required"),
  createdAt: z.union([z.date(), z.string()]),
  updatedAt: z.union([z.date(), z.string()]),
});
```

### 8.4 动态枚举（从数据库 schema 取值）
```typescript
// packages/schemas/src/archetype-schema.ts
export const conditionSchema = z.object({
  id: z.string(),
  type: z.enum(["text", "archetype_ref"]),
  value: z.string(),
  sortOrder: z.number(),
  dependencies: z.array(z.string()).default([]),
});

export const archetypeCreateSchema = z.object({
  id: z.string(),
  name: z.string().min(1),
  scope: z.enum(["project", "repository", "crate", "page", "service"]),
  conditions: z.array(conditionSchema).min(1, "At least one condition is required"),
  createdAt: z.union([z.date(), z.string()]),
  updatedAt: z.union([z.date(), z.string()]),
});
```

### tRPC + Zod 的分层策略
| 层级 | Schema 来源 | 示例 |
|------|-----------|------|
| 简单查询 | 内联 `z.object({...})` | `{ id: z.string() }` |
| 创建操作 | 复用 `@repo/schemas` 的 CreateSchema | `crateCreateSchema` |
| 更新操作 | `CreateSchema.omit({id}).partial()` | `crateUpdateSchema` |
| 复杂查询 | 内联 + 引用枚举 | `{ status: findingStatusSchema }` |

---
## Agent 工具参数定义（Mastra）
### 9.1 createTool 的 inputSchema
```typescript
// packages/schemas/src/archetype-schema.ts
export const conditionSchema = z.object({
  id: z.string(),
  type: z.enum(["text", "archetype_ref"]),
  value: z.string(),
  sortOrder: z.number(),
  dependencies: z.array(z.string()).default([]),
});

export const archetypeCreateSchema = z.object({
  id: z.string(),
  name: z.string().min(1),
  scope: z.enum(["project", "repository", "crate", "page", "service"]),
  conditions: z.array(conditionSchema).min(1, "At least one condition is required"),
  createdAt: z.union([z.date(), z.string()]),
  updatedAt: z.union([z.date(), z.string()]),
});
```

**`.describe()` 的重要性：** LLM 读取 tool description 来决定如何调用工具，`.describe()` 的内容直接影响 Agent 的行为质量。

### 9.2 嵌套 Schema 作为工具输出结构
```typescript
// packages/schemas/src/archetype-schema.ts
export const conditionSchema = z.object({
  id: z.string(),
  type: z.enum(["text", "archetype_ref"]),
  value: z.string(),
  sortOrder: z.number(),
  dependencies: z.array(z.string()).default([]),
});

export const archetypeCreateSchema = z.object({
  id: z.string(),
  name: z.string().min(1),
  scope: z.enum(["project", "repository", "crate", "page", "service"]),
  conditions: z.array(conditionSchema).min(1, "At least one condition is required"),
  createdAt: z.union([z.date(), z.string()]),
  updatedAt: z.union([z.date(), z.string()]),
});
```

### 9.3 z.custom — 校验函数引用
```typescript
// packages/schemas/src/archetype-schema.ts
export const conditionSchema = z.object({
  id: z.string(),
  type: z.enum(["text", "archetype_ref"]),
  value: z.string(),
  sortOrder: z.number(),
  dependencies: z.array(z.string()).default([]),
});

export const archetypeCreateSchema = z.object({
  id: z.string(),
  name: z.string().min(1),
  scope: z.enum(["project", "repository", "crate", "page", "service"]),
  conditions: z.array(conditionSchema).min(1, "At least one condition is required"),
  createdAt: z.union([z.date(), z.string()]),
  updatedAt: z.union([z.date(), z.string()]),
});
```

**`z.custom()` 用于校验非原始类型**（如函数引用），接受一个类型参数和一个断言函数。

---
## Service 层数据校验
Service 层在接收外部输入时使用 schema 进行二次校验（防御性编程）：

```typescript
// packages/schemas/src/archetype-schema.ts
export const conditionSchema = z.object({
  id: z.string(),
  type: z.enum(["text", "archetype_ref"]),
  value: z.string(),
  sortOrder: z.number(),
  dependencies: z.array(z.string()).default([]),
});

export const archetypeCreateSchema = z.object({
  id: z.string(),
  name: z.string().min(1),
  scope: z.enum(["project", "repository", "crate", "page", "service"]),
  conditions: z.array(conditionSchema).min(1, "At least one condition is required"),
  createdAt: z.union([z.date(), z.string()]),
  updatedAt: z.union([z.date(), z.string()]),
});
```

**要点：** 即使 tRPC 层已经校验过，Service 层仍然可以再次校验——Service 可能被非 tRPC 的调用方使用。

---
## 运行时安全解析：safeParse
### 11.1 基础用法
```typescript
// packages/schemas/src/archetype-schema.ts
export const conditionSchema = z.object({
  id: z.string(),
  type: z.enum(["text", "archetype_ref"]),
  value: z.string(),
  sortOrder: z.number(),
  dependencies: z.array(z.string()).default([]),
});

export const archetypeCreateSchema = z.object({
  id: z.string(),
  name: z.string().min(1),
  scope: z.enum(["project", "repository", "crate", "page", "service"]),
  conditions: z.array(conditionSchema).min(1, "At least one condition is required"),
  createdAt: z.union([z.date(), z.string()]),
  updatedAt: z.union([z.date(), z.string()]),
});
```

### 11.2 在 API Route 中使用
```typescript
// packages/schemas/src/archetype-schema.ts
export const conditionSchema = z.object({
  id: z.string(),
  type: z.enum(["text", "archetype_ref"]),
  value: z.string(),
  sortOrder: z.number(),
  dependencies: z.array(z.string()).default([]),
});

export const archetypeCreateSchema = z.object({
  id: z.string(),
  name: z.string().min(1),
  scope: z.enum(["project", "repository", "crate", "page", "service"]),
  conditions: z.array(conditionSchema).min(1, "At least one condition is required"),
  createdAt: z.union([z.date(), z.string()]),
  updatedAt: z.union([z.date(), z.string()]),
});
```

### 11.3 在 Env 加载中使用
```typescript
// packages/schemas/src/crate-schema.ts
import { z } from "zod/v4";
import { cratePathInputSchema } from "./crate-path-schema";

export const crateCreateSchema = z.object({
  // ...
  paths: z.array(cratePathInputSchema).default([]),
});
```

### 11.4 safeParse vs parse
| 方法 | 行为 | 使用场景 |
|------|------|---------|
| `schema.parse(data)` | 失败时抛出 `ZodError` | tRPC input（框架自动捕获） |
| `schema.safeParse(data)` | 返回 `{ success, data, error }` | 手动处理校验结果 |

**项目约定：** tRPC 层用 `.input(schema)`（内部调用 parse），其他地方统一用 `safeParse`。

---
## 高级模式
### 12.1 `z.refine` — 自定义校验逻辑
```typescript
// packages/schemas/src/crate-schema.ts
import { z } from "zod/v4";
import { cratePathInputSchema } from "./crate-path-schema";

export const crateCreateSchema = z.object({
  // ...
  paths: z.array(cratePathInputSchema).default([]),
});
```

**模式：** `.optional() + .refine()` — 先标记为可选，再对非空值做额外校验。refine 返回 `true` 表示通过，`false` 表示失败。

### 12.2 `z.lazy` — 递归 Schema
```typescript
// packages/schemas/src/crate-schema.ts
import { z } from "zod/v4";
import { cratePathInputSchema } from "./crate-path-schema";

export const crateCreateSchema = z.object({
  // ...
  paths: z.array(cratePathInputSchema).default([]),
});
```

### 要点
- `z.lazy()` 接受一个返回 ZodType 的工厂函数
- 用于自引用（树、链表等递归数据结构）
- 需要显式标注 `z.ZodType<{...}>` 类型注解避免 TypeScript 循环引用报错

### 12.3 `z.custom` — 自定义类型校验
```typescript
// packages/schemas/src/crate-schema.ts
import { z } from "zod/v4";
import { cratePathInputSchema } from "./crate-path-schema";

export const crateCreateSchema = z.object({
  // ...
  paths: z.array(cratePathInputSchema).default([]),
});
```

### 要点
- `z.custom<T>()` 接受一个类型参数 `T`
- 第二个参数是断言函数 `(value: unknown) => boolean`
- 适用于函数、类实例等非 JSON-serializable 类型

### 12.4 条件字段
```typescript
// packages/schemas/src/crate-schema.ts
import { z } from "zod/v4";
import { cratePathInputSchema } from "./crate-path-schema";

export const crateCreateSchema = z.object({
  // ...
  paths: z.array(cratePathInputSchema).default([]),
});
```

---
## 最佳实践总结
### 13.1 架构层面
| 实践 | 说明 |
|------|------|
| **单一数据源** | 类型从 Zod schema 派生，不手写重复类型 |
| **Schema 放 `@repo/schemas`** | 跨包共享的 schema 放在 `packages/schemas/src/` |
| **tRPC 专用 Schema 放 `routers/schemas.ts`** | 与业务 Schema 分离，通过 `.omit()` / `.partial()` 派生 |
| **桶导出** | `packages/schemas/src/index.ts` 统一 re-export 所有 schema 和类型 |

### 13.2 Schema 设计层面
| 实践 | 示例 |
|------|------|
| **枚举值用 `as const` 数组 + `z.enum()`** | `const Types = ["a", "b"] as const; z.enum(Types)` |
| **为校验失败提供友好的 error message** | `.min(1, "Name is required")` |
| **善用 `.default()` 减少必填字段** | `.default([])`, `.default("main")` |
| **善用 `.describe()` 为 LLM 工具提供字段说明** | `.describe("The file path relative to...")` |
| **环境变量 schema 采用 fail-fast 模式** | 启动时校验，不符合立即抛错 |

### 13.3 类型推导层面
| 场景 | 使用 |
|------|------|
| 数据/返回值类型 | `z.infer<typeof schema>` |
| 表单输入类型 | `z.input<typeof schema>` |
| 输出给前端的类型 | 从 `@repo/schemas` 导入 inferred type |

### 13.4 校验层面
| 场景 | 方法 |
|------|------|
| tRPC 输入校验 | `.input(schema)` — 框架自动 parse |
| API Route 手动校验 | `schema.safeParse(body)` |
| 环境变量校验 | `schema.safeParse(process.env)` |
| Service 层防御性校验 | `schema.safeParse(input)` |

---
## 反模式与常见错误
### ❌ 手写重复类型
```typescript
// packages/schemas/src/crate-schema.ts
import { z } from "zod/v4";
import { cratePathInputSchema } from "./crate-path-schema";

export const crateCreateSchema = z.object({
  // ...
  paths: z.array(cratePathInputSchema).default([]),
});
```

```typescript
// packages/schemas/src/crate-schema.ts
import { z } from "zod/v4";
import { cratePathInputSchema } from "./crate-path-schema";

export const crateCreateSchema = z.object({
  // ...
  paths: z.array(cratePathInputSchema).default([]),
});
```

### ❌ 创建独立的 types.ts 文件
```typescript
// packages/schemas/src/crate-schema.ts
import { z } from "zod/v4";
import { cratePathInputSchema } from "./crate-path-schema";

export const crateCreateSchema = z.object({
  // ...
  paths: z.array(cratePathInputSchema).default([]),
});
```

```typescript
// packages/schemas/src/crate-schema.ts
import { z } from "zod/v4";
import { cratePathInputSchema } from "./crate-path-schema";

export const crateCreateSchema = z.object({
  // ...
  paths: z.array(cratePathInputSchema).default([]),
});
```

### ❌ 在表单中使用 z.infer 而非 z.input
```typescript
// packages/schemas/src/crate-schema.ts
import { z } from "zod/v4";
import { cratePathInputSchema } from "./crate-path-schema";

export const crateCreateSchema = z.object({
  // ...
  paths: z.array(cratePathInputSchema).default([]),
});
```

```typescript
// 先定义 const 数组（运行时值 + 编译时字面量类型）
export const CrateTypeValues = [
  "package",
  "module",
  "feature",
  "library",
  "service",
  "utility",
  "other",
] as const;

// 在 schema 中使用 z.enum()
export const crateCreateSchema = z.object({
  type: z.enum(CrateTypeValues),
});
```

### ❌ 使用 parse 而非 safeParse（非 tRPC 场景）
```typescript
// 先定义 const 数组（运行时值 + 编译时字面量类型）
export const CrateTypeValues = [
  "package",
  "module",
  "feature",
  "library",
  "service",
  "utility",
  "other",
] as const;

// 在 schema 中使用 z.enum()
export const crateCreateSchema = z.object({
  type: z.enum(CrateTypeValues),
});
```

```typescript
// 先定义 const 数组（运行时值 + 编译时字面量类型）
export const CrateTypeValues = [
  "package",
  "module",
  "feature",
  "library",
  "service",
  "utility",
  "other",
] as const;

// 在 schema 中使用 z.enum()
export const crateCreateSchema = z.object({
  type: z.enum(CrateTypeValues),
});
```

---
## 附录 A：Schema 文件目录结构
```typescript
// 先定义 const 数组（运行时值 + 编译时字面量类型）
export const CrateTypeValues = [
  "package",
  "module",
  "feature",
  "library",
  "service",
  "utility",
  "other",
] as const;

// 在 schema 中使用 z.enum()
export const crateCreateSchema = z.object({
  type: z.enum(CrateTypeValues),
});
```

---
## 附录 B：项目中使用的 Zod 方法速查
| 方法 | 用途 | 使用文件数 |
|------|------|-----------|
| `z.object({})` | 定义对象结构 | 全部 |
| `z.string()` | 字符串类型 | 全部 |
| `z.number()` | 数字类型 | 多个 |
| `z.boolean()` | 布尔类型 | 多个 |
| `z.array()` | 数组类型 | 多个 |
| `z.enum()` | 枚举/字面量联合 | 多个 |
| `z.union([A, B])` | 联合类型 | 多个（日期/字符串） |
| `z.tuple([A, B])` | 定长元组 | 1 |
| `z.lazy(() => schema)` | 递归/自引用 Schema | 1 |
| `z.custom<T>(fn)` | 自定义类型校验 | 多个（Agent context） |
| `.min(n, msg)` | 最小长度/数量 | 全部 |
| `.optional()` | 可选字段 | 全部 |
| `.nullable()` | 可空字段 | 1 |
| `.default(val)` | 默认值 | 全部 |
| `.describe(msg)` | 字段描述 | Agent 工具 |
| `.refine(fn, opts)` | 自定义校验 | 1（JSON） |
| `.pick({...})` | 选取字段 | 1 |
| `.omit({...})` | 排除字段 | 多个 |
| `.partial()` | 全部可选 | 多个 |
| `z.infer<typeof S>` | 推导输出类型 | 全部 |
| `z.input<typeof S>` | 推导输入类型 | 1 |
| `schema.safeParse()` | 安全解析 | 多个 |
| `schema.parse()` | 断言解析（抛错） | tRPC 内部 |
| `z.ZodType<{...}>` | 显式类型注解 | 递归 Schema |
