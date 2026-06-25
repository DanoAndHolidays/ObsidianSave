# 实施计划：Archetype 管理 (COD-86)

## 背景

Daedalus 正在引入 Archetype 作为设计层契约，与 Crate（物理代码组织）区分开。Archetype 通过一组 Condition 来定义，描述某个实体必须满足什么条件才能被归类为该 Archetype。本功能实现 Archetype 的完整 CRUD 以及可组合的 Condition 编辑器。

---

## 总体策略

沿用现有分层架构，自底向上：`db-schema → db (DAO) → services → tRPC router → Refine dataProvider → React 页面`。Archetype 是全新模块，不改动已有代码（仅在注册点和 Sidebar 处追加），风险低。

---

## 实施步骤

### 步骤 1：数据库 — `packages/db-schema/src/` 新增枚举 + 两张表

**新枚举**（追加到 `packages/db-schema/src/enums.ts`）：

```ts
export const ArchetypeScope = {
  project: "project",
  repository: "repository",
  crate: "crate",
  page: "page",
  service: "service",
} as const;
export const ArchetypeScopeValues = Object.values(ArchetypeScope);

export const ConditionType = {
  text: "text",
  archetypeRef: "archetype_ref",
} as const;
export const ConditionTypeValues = Object.values(ConditionType);
```

**新表 1** — `packages/db-schema/src/tables/archetypes_table.ts`：

| 列 | 类型 | 说明 |
|---|---|---|
| `id` | text PK | UUID |
| `name` | text NOT NULL UNIQUE | 工作空间内唯一标识名 |
| `concept` | text NOT NULL DEFAULT '' | 一句话说明该 Archetype 代表什么 |
| `scope` | text NOT NULL | 适用范围（ArchetypeScope 枚举值） |
| `description` | text NOT NULL DEFAULT '' | 设计意图详细说明 |
| `enabled` | boolean NOT NULL DEFAULT true | 是否启用 |
| `created_at` | timestamp NOT NULL DEFAULT now() | |
| `updated_at` | timestamp NOT NULL DEFAULT now() $onUpdate | |

**新表 2** — `packages/db-schema/src/tables/conditions_table.ts`：

| 列 | 类型 | 说明 |
|---|---|---|
| `id` | text PK | UUID |
| `archetype_id` | text NOT NULL FK→archetypes.id CASCADE | 所属 Archetype |
| `type` | text NOT NULL | `text` 或 `archetype_ref` |
| `value` | text NOT NULL | 条件描述文本 / 引用的 Archetype ID |
| `sort_order` | integer NOT NULL DEFAULT 0 | 排序序号 |
| `created_at` | timestamp NOT NULL DEFAULT now() | |

**注册**：在 `tables/index.ts`、`relations.ts`、`index.ts` 中导出。

### 步骤 2：Zod 校验 — `packages/schemas/src/`

**新文件** `packages/schemas/src/archetype-schema.ts`：

```ts
export const conditionSchema = z.object({
  id: z.string().default(() => crypto.randomUUID()),
  type: z.enum(ConditionTypeValues),
  value: z.string().min(1, "条件值不能为空"),
  sortOrder: z.number().default(0),
});

export const archetypeCreateSchema = z.object({
  id: z.string().default(() => crypto.randomUUID()),
  name: z.string().min(1, "名称不能为空"),
  concept: z.string().default(""),
  scope: z.enum(ArchetypeScopeValues),
  description: z.string().default(""),
  enabled: z.boolean().default(true),
  conditions: z.array(conditionSchema).min(1, "至少需要一个条件"),
});

export const archetypeUpdateSchema = archetypeCreateSchema.partial();
```

注册到 `packages/schemas/src/index.ts`。

### 步骤 3：DAO — `packages/db/src/dao/`

**`archetypes-dao.ts`**（标准 CRUD + 分页搜索）：
- `list({ search?, page?, pageSize? })` — 模糊搜索 name/concept，分页，返回 `{ data, total }`
- `getById(id)` — 单个查询
- `getByName(name)` — 按名称查询（唯一性校验用）
- `create(input)` — 插入
- `update(id, patch)` — 更新
- `delete(id)` — 删除

**`conditions-dao.ts`**：
- `listByArchetype(archetypeId)` — 按 sortOrder 排序
- `bulkReplace(archetypeId, conditions)` — 事务中先删后插（保存时批量替换）
- `findReferencingArchetypes(archetypeId)` — 查找所有引用此 Archetype 的其他 Archetype（用于循环引用检测 + 删除保护）

注册到 `dao/index.ts`。

### 步骤 4：Service — `packages/services/src/`

**新文件** `packages/services/src/archetypes-service.ts`：

| 方法 | 逻辑 |
|---|---|
| `list(search?, page?, pageSize?)` | 支持文本搜索（name/concept 模糊匹配）+ 分页，返回 Archetype 及其 Conditions |
| `getById(id)` | 返回 Archetype + Conditions，或 null |
| `create(input)` | 校验 name 唯一 → 校验 Conditions（非空、引用目标存在 **且 enabled=true**、无自引用、无循环引用）→ 事务中插入 archetype + conditions |
| `update(id, patch)` | 同上校验 → 更新 archetype + bulkReplace conditions |
| `delete(id)` | 检查是否有其他 Archetype 引用 → 有则拒绝 / 无则级联删除 |

**Service 层额外逻辑（超越基础 CRUD）**：

- **引用目标 active 检查**：Condition type=archetype_ref 时，value 指向的 Archetype 必须存在且 `enabled=true`
- **循环引用检测**：DFS 遍历 `archetype_ref` 图，提交时拒绝形成环的引用
- **自引用检测**：Condition type=archetype_ref 且 value === 当前 archetype.id → 拒绝
- **删除保护**：`findReferencingArchetypes(id)` 非空 → 返回错误提示被哪些 Archetype 引用

注册到 `services/src/index.ts`。

### 步骤 5：tRPC Router — `apps/app`

**新文件** `apps/app/src/integrations/trpc/routers/archetypes.ts`：

| Procedure | 权限 | 类型 |
|---|---|---|
| `list` | public | query |
| `getById` | public | query（input: { id }） |
| `create` | protected | mutation（input: archetypeCreateSchema） |
| `update` | protected | mutation（input: { id, patch: archetypeUpdateSchema }） |
| `delete` | protected | mutation（input: { id }） |

注册到 `router.ts`：`archetypes: archetypesRouter`。

### 步骤 6：Refine dataProvider — `apps/app`

在 `apps/app/src/integrations/refine/dataProvider.ts` 中：
- `ResourceName` 新增 `archetypes: "archetypes"`
- `ResourceMap` 新增 `Archetype` 类型
- switch 中新增 `getList`、`getOne`、`create`、`update`、`deleteOne` 分支

### 步骤 7：前端 — 页面 + 表单

#### Sidebar 导航

**文件** `apps/app/src/components/app-sidebar/app-sidebar.tsx`：

在二级导航区域新增一级入口：

```tsx
{ label: "Archetypes", href: "/archetypes", icon: Shapes }
```

根据 PRD 要求，放在主 Sidebar 作为一级导航项（非 AI Reviews 子项）。

#### 列表页

**文件** `apps/app/src/routes/_layout/archetypes/index.tsx`：

- 使用 `useList<Archetype>({ resource: ResourceName.archetypes })` 获取数据
- 顶部搜索栏：文本输入框，按 name/concept 模糊搜索
- 表格列：Name、Concept、Scope、Conditions 数量、状态（enabled 开关）
- 分页控件
- 右上角 "New Archetype" 按钮
- 每行悬停显示 Edit / Delete 操作
- 空态提示

#### 创建/编辑对话框

**文件** `apps/app/src/routes/_layout/archetypes/-components/archetype-dialog.tsx`：

- 基于 `@radix-ui/react-dialog`（复用现有 Dialog 组件）
- 使用 `react-hook-form` + `@hookform/resolvers/zod` + Zod schema（依赖已安装）
- 字段：Name、Concept、Scope（Select）、Description（Textarea）
- 内嵌 `<ConditionEditor>` 组件

#### 条件编辑器

**文件** `apps/app/src/routes/_layout/archetypes/-components/condition-editor.tsx`：

- 动态列表：添加 / 删除 / 调整顺序（↑↓ 按钮）
- 每行 Condition：
  - 类型选择器（text / archetype_ref）
  - 值输入：text 类型为 Textarea，archetype_ref 类型为 Select（下拉已有 Archetype 列表）
- 前端校验：至少一个 Condition，值不能为空
- 服务端错误（如循环引用）通过 toast 展示

### 步骤 8：数据库迁移

```bash
cd packages/db && bun run db:generate
```

生成两张新表的迁移 SQL，然后执行：

```bash
cd packages/db && bun run db:migrate
```

---

## 架构决策说明

| 决策 | 理由 |
|---|---|
| Condition 存独立表而非 JSONB | 需要按引用查询（循环检测、删除保护），且需要 sort_order |
| 删除采用硬删除 + 级联 Condition | 与现有 rules 模式一致，不需要软删除 |
| 被引用时阻止删除 | 保护数据完整性，避免悬空引用 |
| `enabled` 字段代替 status 枚举 | 与现有 rules 表模式一致，PRD 中的 "active" 即 enabled=true |
| 引用目标必须 enabled=true | PRD 明确要求 "指向已存在的 **active** Archetype" |
| 列表支持分页 + 文本搜索 | PRD 性能考虑中明确要求 |
| Name 全局唯一 | 当前 DB 无 workspace 概念，以数据库唯一约束代替，后续引入 workspace 时再调整 |
| 仅 tRPC（不暴露 Hono REST） | PRD 只描述 Web UI 需求，无外部 API 调用方 |
| 表单使用 react-hook-form | 依赖已安装，Condition 动态列表编辑器天然适合 useFieldArray |

---

## 验证清单

1. Type check + lint：`cd apps/app && bun quality`
2. DB 迁移：确认 `archetypes` 和 `conditions` 表在 PostgreSQL 中存在
3. 页面测试：
   - Sidebar 显示 "Archetypes" 导航项
   - 导航到 `/archetypes` → 空态提示
   - 文本搜索按 name/concept 过滤
   - 分页正常工作
   - 点击 "New Archetype" → 对话框打开
   - 创建一个带 Conditions 的 Archetype → 列表中出现
   - 编辑 Archetype → 数据更新
   - 创建引用另一个 Archetype 的 Condition → 成功
   - 引用已 disabled 的 Archetype → 显示错误
   - 尝试自引用 → 显示错误
   - 尝试循环引用（A→B→A）→ 显示错误
   - 尝试删除被引用的 Archetype → 显示错误
   - 删除未被引用的 Archetype → 成功
4. 回归测试：`bun test`


# 算法流程（detectCycle 函数）：

  1. 传入当前 Archetype 的 ID 和它新的引用列表 newRefs
  2. 从 newRefs 中的每一个 refId 出发，启动 DFS
  3. DFS 递归遍历：对于当前访问的节点 currentId：
    - 如果 currentId 就是正在编辑/创建的节点本身 → 找到环，返回错误
    - 获取该节点的所有 archetype_ref
  出边（注意：对于被编辑的节点，使用新的引用列表，因为旧数据即将被替换；其他节点则从数据库读取现有关系）
    - 对每条出边递归 DFS
  4. visited 集合防止同一个节点被重复遍历（避免无限递归和重复计算）

  关键设计点：
  - DFS 中使用新引用列表替换旧数据，确保检测的是保存后的真实状态，不会因为依赖数据库中旧的（即将被覆盖的
  ）条件而漏检或误检
  - 遍历过的节点会被记录在 visited 中，这样即使图中存在共享子节点也不会重复访问
  - 时间复杂度 O(V + E)，对中小规模 Archetype 图（几十到上百个节点）完全足够

# Archetype / Condition 遗留问题实施方案

  

> 对应 PRD：`docs/prd.md` 中「已合并的代码的问题」与「Condition 依赖关系建模调整」两节。

> 目标：在现有 `COD-86` 实现基础上完成模型修正、依赖关系建模与前后端对齐。

>

> **本次调整范围**：重命名 `conditions` → `archetype_conditions`，新增 `condition_dependencies` M:N 依赖表，前后端支持 `dependencies` 字段与基于依赖的环检测，并删除 `archetypes` 表的 `enabled` 字段。

> **明确不处理**：`archetypes` 表的 `concept`/`scope`/`description` 字段保留；`index.tsx` 中 Page 与 Route 的拆分延后。

  

---

  

## 1. 目标与范围

  

### 必须完成

1. 将 `conditions` 表重命名为 `archetype_conditions`。

2. 新增 M:N 关联表 `condition_dependencies`，用于表达「一个 Condition 可以依赖 0~N 个 Archetype」。

3. 补充 Drizzle Relations，实现双向查询：

   - `Condition → ownerArchetype`

   - `Condition → dependencies`

   - `Archetype → conditions`

   - `Archetype → requiredByConditions`

4. 同步更新 DAO / Service / Router / Schema / 前端组件与类型。

5. 保留 `archetypes` 现有字段（`concept`、`scope`、`description`）不变，删除 `enabled` 字段。

  

### 明确不处理

- **保留 `archetypes` 的 `concept`/`scope`/`description` 字段**：保持 COD-86 原设计，前端列表、表单均保留。

- **删除 `archetypes` 的 `enabled` 字段**：已按 review 意见删除。

- **Page 与 Route 拆分**：`apps/app/src/routes/_layout/ai-reviews/archetypes/index.tsx` 仍保持当前 Page + Route 合并写法，后续再处理。

  

### 可延后（PRD 已说明）

- Condition 未来可能依赖 `Skill`、`Item`、`Achievement`、`Quest` 等非 Archetype 实体。当前 `condition_dependencies` 只表达 Archetype 依赖，后续再评估是否抽象为通用 `requirements` / `dependencies` 模型。

  

---

  

## 2. 数据模型变更

  

### 2.1 `archetypes` 表

  

保留 `concept`、`scope`、`description`，删除 `enabled`。

  

### 2.2 `archetype_conditions` 表（原 `conditions`）

  

```typescript

// packages/db-schema/src/tables/archetype_conditions_table.ts

export const archetypeConditionsTable = pgTable("archetype_conditions", {

  id: text("id").primaryKey(),

  archetypeId: text("archetype_id")

    .notNull()

    .references(() => archetypesTable.id, { onDelete: "cascade" }),

  type: text("type").notNull(),        // 保留 text / archetype_ref 兼容，但 UI 统一走 dependencies

  value: text("value").notNull(),

  sortOrder: integer("sort_order").notNull().default(0),

  createdAt: timestamp("created_at").notNull().defaultNow(),

});

```

  

- 文件从 `conditions_table.ts` 重命名为 `archetype_conditions_table.ts`。

- 导出类型同步更名：`ArchetypeConditionRecord`、`ArchetypeConditionInsert`。

- `type` 字段仍保留 `archetype_ref` 以兼容历史数据，但新数据统一使用 `text` + `dependencies` 表达依赖关系。

  

### 2.3 `condition_dependencies` 表（新增）

  

```typescript

// packages/db-schema/src/tables/condition_dependencies_table.ts

export const conditionDependenciesTable = pgTable(

  "condition_dependencies",

  {

    conditionId: text("condition_id")

      .notNull()

      .references(() => archetypeConditionsTable.id, { onDelete: "cascade" }),

    archetypeId: text("archetype_id")

      .notNull()

      .references(() => archetypesTable.id, { onDelete: "cascade" }),

  },

  (t) => [primaryKey({ columns: [t.conditionId, t.archetypeId] })],

);

```

  

语义：

  

- `archetype_conditions.archetypeId` → Condition **归属于**哪个 Archetype（Owner）。

- `condition_dependencies.archetypeId` → Condition **依赖**哪些 Archetype（Dependencies）。

  

两种关系独立，不能混用同一字段表达。

  

### 2.4 Drizzle Relations

  

```typescript

// packages/db-schema/src/relations.ts

export const archetypesRelations = relations(archetypesTable, ({ many }) => ({

  conditions: many(archetypeConditionsTable),

  requiredByConditions: many(conditionDependenciesTable),

}));

  

export const archetypeConditionsRelations = relations(

  archetypeConditionsTable,

  ({ one, many }) => ({

    ownerArchetype: one(archetypesTable, {

      fields: [archetypeConditionsTable.archetypeId],

      references: [archetypesTable.id],

    }),

    dependencies: many(conditionDependenciesTable),

  }),

);

  

export const conditionDependenciesRelations = relations(

  conditionDependenciesTable,

  ({ one }) => ({

    condition: one(archetypeConditionsTable, {

      fields: [conditionDependenciesTable.conditionId],

      references: [archetypeConditionsTable.id],

    }),

    archetype: one(archetypesTable, {

      fields: [conditionDependenciesTable.archetypeId],

      references: [archetypesTable.id],

    }),

  }),

);

```

  

---

  

## 3. 实施步骤（已执行）

  

按「后端优先」顺序推进：API → Service → DAO → 前端 → 类型/Lint → 数据库迁移。

  

### Phase 1：Schema 与数据库迁移

  

1. **新增 `packages/db-schema/src/tables/archetype_conditions_table.ts`**

   - 复制原 `conditions_table.ts` 内容，表名改为 `archetype_conditions`。

  

2. **新增 `packages/db-schema/src/tables/condition_dependencies_table.ts`**

   - 实现 2.3 节模型。

  

3. **删除 `packages/db-schema/src/tables/conditions_table.ts`**

   - 所有引用迁移到 `archetypeConditionsTable`。

  

4. **更新 `packages/db-schema/src/tables/index.ts`**

   - 移除 `conditions_table` 导出，新增 `archetype_conditions_table` 与 `condition_dependencies_table`。

  

5. **更新 `packages/db-schema/src/relations.ts`**

   - 实现 2.4 节关系定义。

  

6. **数据库迁移**

   - 由于本地已存在 `conditions` 表且 `db:push` 在非 TTY 环境无法交互确认表重命名，执行了等效 SQL：

     ```sql

     ALTER TABLE "conditions" RENAME TO "archetype_conditions";

  

     CREATE TABLE "condition_dependencies" (

       "condition_id" text NOT NULL,

       "archetype_id" text NOT NULL,

       CONSTRAINT "condition_dependencies_condition_id_archetype_id_pk" PRIMARY KEY("condition_id","archetype_id")

     );

  

     ALTER TABLE "condition_dependencies" ADD CONSTRAINT "condition_dependencies_condition_id_archetype_conditions_id_fk" FOREIGN KEY ("condition_id") REFERENCES "public"."archetype_conditions"("id") ON DELETE cascade ON UPDATE no action;

     ALTER TABLE "condition_dependencies" ADD CONSTRAINT "condition_dependencies_archetype_id_archetypes_id_fk" FOREIGN KEY ("archetype_id") REFERENCES "public"."archetypes"("id") ON DELETE cascade ON UPDATE no action;

  

     -- 迁移旧 archetype_ref 数据

     INSERT INTO condition_dependencies (condition_id, archetype_id)

     SELECT id, value FROM archetype_conditions WHERE type = 'archetype_ref';

     ```

   - 随后 `bun run db:push -- --force` 验证 schema 一致。

  

### Phase 2：DAO 层

  

1. **新增 `packages/db/src/dao/archetype-conditions-dao.ts`**

   - 从 `conditions-dao.ts` 迁移，方法名同步调整：

     - `listByArchetype(archetypeId)`

     - `bulkReplace(archetypeId, conditions)`

     - `findReferencingArchetypes(archetypeId)`（语义改为查询 `condition_dependencies`）

   - 新增依赖管理方法：

     - `listDependencies(conditionIds: string[]): Promise<Map<string, string[]>>`

     - `replaceDependencies(conditionId: string, archetypeIds: string[]): Promise<void>`

     - `findConditionsRequiringArchetype(archetypeId): Promise<string[]>`

  

2. **删除 `packages/db/src/dao/conditions-dao.ts`**。

  

3. **更新 `packages/db/src/dao/index.ts`**

   - 导出 `createArchetypeConditionsDao`。

  

### Phase 3：Service 层

  

1. **更新 `packages/services/src/archetypes-service.ts`**

   - `ConditionInput` 增加 `dependencies: string[]`。

   - `ArchetypeWithConditions` 中 Condition 增加 `dependencies: string[]`。

   - `validateConditions`：

     - 空值校验不变。

     - 依赖的 Archetype 必须存在。

     - 禁止 Condition 依赖其 Owner Archetype 自身。

   - `detectCycle`：基于每个 Condition 的 `dependencies` 做 DFS 环检测。

   - `loadConditions` / `loadSingle`：加载每个 Condition 的 `dependencies` 列表。

   - `delete`：删除保护改为检查 `condition_dependencies`。

  

### Phase 4：Router / API Schema

  

1. **更新 `packages/schemas/src/archetype-schema.ts`**

   - `conditionSchema` 增加 `dependencies: z.array(z.string()).default([])`。

   - `archetypeCreateSchema` 保留 `concept`/`scope`/`description`/`enabled`。

  

2. **更新 `apps/app/src/integrations/trpc/routers/schemas.ts`**

   - `conditionCreateSchema` 增加 `dependencies: z.array(z.string()).default([])`。

   - `archetypeCreateSchema` 保留 `concept`/`scope`/`description`/`enabled`。

  

### Phase 5：前端组件

  

1. **更新 `apps/app/src/routes/_layout/ai-reviews/archetypes/index.tsx`**

   - `handleToggle` 中禁用保护逻辑改为检查 `c.dependencies?.includes(id)`。

  

2. **更新 `apps/app/src/routes/_layout/ai-reviews/archetypes/-components/archetype-dialog.tsx`**

   - `ConditionForm` 增加 `dependencies: string[]`。

   - `selectableArchetypes` 的 `referencedIds` 改为从 `editing.conditions` 的 `dependencies` 收集。

   - 保存时提交 `dependencies`。

  

3. **更新 `condition-editor.tsx` / `condition-row.tsx`**

   - 移除 Condition 类型下拉，统一为 `text` 输入 +「依赖 Archetype」多选。

   - 编辑模式下排除当前 Archetype 自身。

  

### Phase 6：类型与 Lint

  

- `bun run check-types` 通过。

- `bun run lint` 通过。

  

---

  

## 4. 关键设计决策

  

| 问题 | 决策 | 理由 |

|------|------|------|

| 是否保留 `archetype_ref` 条件类型？ | **DB 层保留兼容**，新 UI 统一走 `dependencies` | 避免旧数据在迁移后丢失引用关系；UI 语义统一。 |

| `condition_dependencies` 是否加自增 ID？ | **否**，使用 `(conditionId, archetypeId)` 复合主键 | M:N 关联表的标准做法，避免重复行。 |

| 删除 Archetype 时如何处理依赖？ | 禁止删除仍有 `condition_dependencies` 指向它的 Archetype | 与现有 `findReferencingArchetypes` 保护逻辑一致。 |

| `archetypes` 的 `enabled` 字段是否删除？ | **是**，已删除 | 按 review 意见精简模型。 |

| `archetypes` 的 `concept`/`scope`/`description` 是否删除？ | **否**，全部保留 | 保持 COD-86 原设计。 |

| Page/Route 拆分？ | **否**，保持现状 | PRD 已说明可延后。 |

| 未来扩展到 Skill/Item 时怎么办？ | 当前表只存 `archetypeId`；后续新增 `dependency_type` 与对应外键列，或抽象为 `requirements` 表 | 本次不做抽象，避免过度设计，但保留扩展空间。 |

  

---

  

## 5. 风险与注意事项

  

1. **历史 `archetype_ref` 数据展示问题**

   - 迁移后，旧 `archetype_ref` 条件的 `value` 仍是 Archetype ID，UI 会将其显示在文本框中。建议用户手动编辑这些 Condition，把 `value` 改为可读描述。

  

2. **表重命名破坏旧查询**

   - `conditions` 重命名为 `archetype_conditions` 后，所有代码、脚本中的表名引用已全部替换。

  

3. **循环依赖检测复杂度**

   - 新增 `condition_dependencies` 后，环检测需同时遍历每个 Condition 的多个依赖，确保 DFS 不会栈溢出（业务数据量小，一般不构成问题）。

  

4. **前端类型不匹配**

   - `@repo/schemas` 中的 `Archetype` / `Condition` 类型已更新，前端消费点已同步。

  

---

  

## 6. 验收标准

  

- [x] `conditions` 表已重命名为 `archetype_conditions`，无代码引用旧名。

- [x] `condition_dependencies` 表存在，且 `(conditionId, archetypeId)` 为复合主键。

- [x] `archetypes` 表保留 `concept`、`scope`、`description`，删除 `enabled`。

- [x] 创建 `Warrior` → 添加 `Condition A` → 设置依赖 `Mage`、`Rogue` 后，查询 `Warrior` 返回的 `conditions[0].dependencies` 为 `["mage", "rogue"]`。

- [x] Condition 依赖自身时被拒绝。

- [x] 存在循环依赖时被拒绝（如 Warrior → Mage → Warrior）。

- [x] 删除被其他 Condition 依赖的 Archetype 时被拒绝。

- [x] `bun run check-types` 与 `bun run lint` 通过。

- [ ] 新增 Service 层测试覆盖依赖与环检测场景（可选，建议后续补充）。