# COD-225 Anatomy 管理与版本绑定实现计划

> **执行指引：** 推荐使用 `subagent-driven-development` 技能逐任务执行此计划；每个 Task 完成规格审查和代码质量审查后再进入下一个 Task。
> 步骤使用 checkbox (`- [ ]`) 追踪进度。

**目标：** 建立可编辑、可发布、可版本化的 Anatomy，并让 Crate 显式选择和回访一个不可变的 Published Anatomy Version。

**架构：** Anatomy 的身份、Draft、Version 和 Crate 引用使用关系表；文件/目录树及策略使用经 Zod 校验的嵌套 `JSONB`。Draft 整体保存并通过 revision 乐观锁防止覆盖，Publish 在事务中校验、创建不可变 Version 并移除活动 Draft；前端通过 Refine data provider 访问 tRPC，不从组件直接调用 tRPC。

**技术栈：** PostgreSQL/Neon、Drizzle ORM、Zod v4、neverthrow、tRPC、Refine、React 19、react-hook-form、TanStack Router、Vitest、oxlint。

> 对应 PRD：`docs/COD-225/prd.md`
> Linear Issue：[COD-225](https://linear.app/code-forge-official/issue/COD-225/anatomyfeature%E4%BD%9C%E4%B8%BA-crate-%E7%BB%B4%E6%8A%A4%E8%80%85%E6%88%91%E5%B8%8C%E6%9C%9B%E5%AE%9A%E4%B9%89-crate-%E5%86%85%E6%96%87%E4%BB%B6%E4%B8%8E%E7%9B%AE%E5%BD%95%E5%BF%85%E9%A1%BB%E5%A6%82%E4%BD%95%E7%BB%84%E7%BB%87-define-how-files)
> 创建时间：2026-07-20
> 状态：⏳ 计划中
> Linear 状态：In Progress | 优先级：High | 估算：16 Points | 负责人：Dano

> Worktree 提示：计划自审时发现 `packages/db-schema/src/tables/anatomies_table.ts` 与 `anatomy_versions_table.ts` 是未跟踪、未完成的并行草稿；实施 Task 2 前必须先确认其所有者并逐行合并，禁止直接覆盖。当前 `docs/` 受 `.gitignore` 规则忽略，如需提交本计划，应显式执行 `git add -f -- docs/COD-225/prd.md docs/COD-225/plan.md`。

---

## 1. 范围与已锁定决策

### 1.1 本轮交付

- Anatomy 列表、状态过滤、创建 Draft、保存 Draft、归档。
- File/Directory 树、固定/占位名称、四种 Quantity、One-of 组合。
- Anatomy 默认策略、Directory/Entry 策略覆盖及有效策略来源预览。
- Publish 校验、不可变 Version、从 Version 创建新 Draft、Version 历史。
- Crate 选择 Published Version、预览、显式切换和未配置状态。
- 数据库迁移生成、自动化验证及 Neon schema 推送。

### 1.2 数据建模决策

采用混合模型：

```text
anatomies 1 ── 0..1 anatomy_drafts
    │
    └── 1..N anatomy_versions 1 ── 0..N crates

anatomy_drafts.structure  = JSONB 可编辑树
anatomy_versions.structure = JSONB 不可变快照
crates.anatomy_version_id  = nullable FK
```

不采用扁平 `anatomy_entries` 邻接表。当前所有读写均以完整树为聚合边界，扁平表会引入递归 CTE、排序列、孤儿/循环检测、One-of 关联表和发布时批量复制，而没有 Entry 级查询需求。

### 1.3 状态语义

Draft 与 Published 不是互斥状态：已有 Version 的 Anatomy 可以同时拥有一个新 Draft。

- Draft 过滤：`draft != null && archivedAt == null`
- Published 过滤：`latestVersion != null && archivedAt == null`
- Archived 过滤：`archivedAt != null`
- 列表允许同时展示 `Draft` 与 `vN Published` 徽标。
- Archived Anatomy 只读；历史 Version 和 Crate 引用继续可访问。

### 1.4 明确不做

- 不实现 Bonus B1 示例目录演练。
- 不扫描 Repository 或真实文件系统，不生成 Finding。
- 不接入 Archetype、Rule、AST、DOM、JSX 或 Code Sample。
- 不保存 Repository、Project、Branch、绝对路径或计算出的真实路径。
- 不实现 Entry 级共享、权限、审计或跨 Anatomy 搜索。
- 不允许删除 Published Version；本轮也不提供 Anatomy 物理删除。

## 2. 推荐分支与提交边界

```text
feature/anatomy-management
```

基线分支：`develop`

执行前：

```bash
git checkout develop
git pull origin develop
git checkout -b feature/anatomy-management
```

推荐原子提交：

```text
feat(COD-225): add anatomy domain schemas
feat(COD-225): persist anatomy drafts and versions
feat(COD-225): add anatomy validation and publishing
feat(COD-225): expose anatomy trpc resources
feat(COD-225): add anatomy management pages
feat(COD-225): bind published anatomy versions to crates
test(COD-225): cover anatomy workflows
```

## 3. 核心数据契约

### 3.1 Zod 单一类型源

新增 `packages/schemas/src/anatomy-schema.ts`，所有 TypeScript 类型均由 Zod 推导，不新建 `type.ts`。

```typescript
import { z } from "zod/v4";

export const AnatomyPolicyValues = ["block", "warn", "allow"] as const;
export const AnatomyQuantityValues = [
  "exactly_one",
  "optional",
  "one_or_more",
  "zero_or_more",
] as const;

export const anatomyPolicySchema = z.enum(AnatomyPolicyValues);
export const anatomyQuantitySchema = z.enum(AnatomyQuantityValues);

export const anatomyPoliciesSchema = z.object({
  missingRequired: anatomyPolicySchema,
  unexpectedEntry: anatomyPolicySchema,
  nameMismatch: anatomyPolicySchema,
  nestingMismatch: anatomyPolicySchema,
});

export const anatomyPolicyOverridesSchema = anatomyPoliciesSchema.partial();

export const anatomyNameExpressionSchema = z.discriminatedUnion("type", [
  z.object({ type: z.literal("literal"), value: z.string().trim().min(1) }),
  z.object({ type: z.literal("placeholder"), value: z.string().trim().min(3) }),
]);

const anatomyEntryBaseSchema = z.object({
  id: z.string().uuid(),
  name: anatomyNameExpressionSchema,
  quantity: anatomyQuantitySchema,
  policyOverrides: anatomyPolicyOverridesSchema.default({}),
});

export const anatomyFileEntrySchema = anatomyEntryBaseSchema.extend({
  kind: z.literal("file"),
});

export const anatomyDirectoryEntrySchema = anatomyEntryBaseSchema.extend({
  kind: z.literal("directory"),
  get children() {
    return z.array(anatomyNodeSchema);
  },
});

export const anatomyEntrySchema = z.discriminatedUnion("kind", [
  anatomyFileEntrySchema,
  anatomyDirectoryEntrySchema,
]);

export const anatomyOneOfGroupSchema = z.object({
  id: z.string().uuid(),
  kind: z.literal("one_of"),
  minimumMatches: z.number().int().min(1),
  maximumMatches: z.number().int().min(1),
  get alternatives() {
    return z.array(anatomyEntrySchema).min(2);
  },
});

export const anatomyNodeSchema = z.discriminatedUnion("kind", [
  anatomyFileEntrySchema,
  anatomyDirectoryEntrySchema,
  anatomyOneOfGroupSchema,
]);

export const anatomyStructureSchema = z.object({
  schemaVersion: z.literal(1),
  defaultPolicies: anatomyPoliciesSchema,
  root: z.object({ children: z.array(anatomyNodeSchema) }),
});

export const anatomyDraftInputSchema = z.object({
  name: z.string().trim().min(1).max(120),
  purpose: z.string().trim().max(2000),
  structure: anatomyStructureSchema,
});

export const anatomyDraftSaveSchema = anatomyDraftInputSchema.extend({
  expectedRevision: z.number().int().positive(),
});

export type AnatomyPolicies = z.infer<typeof anatomyPoliciesSchema>;
export type AnatomyPolicyOverrides = z.infer<typeof anatomyPolicyOverridesSchema>;
export type AnatomyEntry = z.infer<typeof anatomyEntrySchema>;
export type AnatomyNode = z.infer<typeof anatomyNodeSchema>;
export type AnatomyStructure = z.infer<typeof anatomyStructureSchema>;
export type AnatomyDraftInput = z.infer<typeof anatomyDraftInputSchema>;
```

若 Zod 对递归 getter 的推导在 TypeScript 5.9 下产生循环推断错误，只允许在同一文件为递归 schema 添加 `z.ZodType<z.infer<...>>` 边界；不得复制一套独立业务类型。

### 3.2 默认 Draft

```typescript
export const createEmptyAnatomyDraft = function (
  name: string,
  purpose: string,
): AnatomyDraftInput {
  return {
    name,
    purpose,
    structure: {
      schemaVersion: 1,
      defaultPolicies: {
        missingRequired: "block",
        unexpectedEntry: "warn",
        nameMismatch: "warn",
        nestingMismatch: "block",
      },
      root: { children: [] },
    },
  };
};
```

### 3.3 持久化模型

```typescript
export const anatomiesTable = pgTable("anatomies", {
  id: text("id").primaryKey(),
  archivedAt: timestamp("archived_at"),
  createdAt: timestamp("created_at").notNull().defaultNow(),
  updatedAt: timestamp("updated_at").notNull().defaultNow(),
});

export const anatomyVersionsTable = pgTable(
  "anatomy_versions",
  {
    id: text("id").primaryKey(),
    anatomyId: text("anatomy_id")
      .notNull()
      .references(() => anatomiesTable.id, { onDelete: "cascade" }),
    version: integer("version").notNull(),
    name: text("name").notNull(),
    purpose: text("purpose").notNull().default(""),
    structure: jsonb("structure").$type<unknown>().notNull(),
    publishedAt: timestamp("published_at").notNull().defaultNow(),
  },
  (table) => [
    uniqueIndex("uq_anatomy_versions_anatomy_version").on(
      table.anatomyId,
      table.version,
    ),
    index("idx_anatomy_versions_anatomy_id").on(table.anatomyId),
  ],
);

export const anatomyDraftsTable = pgTable(
  "anatomy_drafts",
  {
    id: text("id").primaryKey(),
    anatomyId: text("anatomy_id")
      .notNull()
      .unique()
      .references(() => anatomiesTable.id, { onDelete: "cascade" }),
    basedOnVersionId: text("based_on_version_id").references(
      () => anatomyVersionsTable.id,
      { onDelete: "set null" },
    ),
    name: text("name").notNull(),
    purpose: text("purpose").notNull().default(""),
    structure: jsonb("structure").$type<unknown>().notNull(),
    revision: integer("revision").notNull().default(1),
    createdAt: timestamp("created_at").notNull().defaultNow(),
    updatedAt: timestamp("updated_at").notNull().defaultNow(),
  },
  (table) => [index("idx_anatomy_drafts_anatomy_id").on(table.anatomyId)],
);
```

`cratesTable` 新增：

```typescript
anatomyVersionId: text("anatomy_version_id").references(
  () => anatomyVersionsTable.id,
  { onDelete: "restrict" },
),
```

### 3.4 有效策略结果

新增 `packages/schemas/src/anatomy-policy.ts`，供 Service 校验和浏览器预览复用：

```typescript
import type { AnatomyPolicies, AnatomyPolicyOverrides } from "./anatomy-schema";

export type AnatomyPolicySource = "entry" | "parent" | "anatomy";

export type ResolvedAnatomyPolicy = {
  value: AnatomyPolicies[keyof AnatomyPolicies];
  source: AnatomyPolicySource;
  sourceEntryId?: string;
};

export const resolveAnatomyPolicies = function (
  defaults: AnatomyPolicies,
  ancestors: Array<{ id: string; overrides: AnatomyPolicyOverrides }>,
  entry?: { id: string; overrides: AnatomyPolicyOverrides },
): Record<keyof AnatomyPolicies, ResolvedAnatomyPolicy> {
  const keys = Object.keys(defaults) as Array<keyof AnatomyPolicies>;

  return Object.fromEntries(keys.map((key) => {
    const entryValue = entry?.overrides[key];
    if (entryValue) {
      return [key, { value: entryValue, source: "entry", sourceEntryId: entry.id }];
    }

    const parent = [...ancestors].reverse().find((candidate) => candidate.overrides[key]);
    if (parent) {
      return [key, {
        value: parent.overrides[key]!,
        source: "parent",
        sourceEntryId: parent.id,
      }];
    }

    return [key, { value: defaults[key], source: "anatomy" }];
  })) as Record<keyof AnatomyPolicies, ResolvedAnatomyPolicy>;
};
```

不得把解析后的有效策略或完整路径写回 JSONB；它们必须保持派生状态。

## 4. 文件结构规划

### 4.1 数据、Schema 与服务端

| 文件                                                         | 操作      | 单一职责                                         |
| ---------------------------------------------------------- | ------- | -------------------------------------------- |
| `packages/schemas/src/anatomy-schema.ts`                   | 新增      | Anatomy Zod 形状、常量和推导类型                       |
| `packages/schemas/src/anatomy-policy.ts`                   | 新增      | 策略继承解析与来源说明                                  |
| `packages/schemas/src/index.ts`                            | 修改      | 只做上述模块的 re-export                            |
| `packages/db-schema/src/tables/anatomies_table.ts`         | 修改未跟踪草稿 | Anatomy 身份与归档时间；修正当前草稿的表名、归档字段和重复列名          |
| `packages/db-schema/src/tables/anatomy_drafts_table.ts`    | 新增      | 单一活动 Draft 与 revision                        |
| `packages/db-schema/src/tables/anatomy_versions_table.ts`  | 修改未跟踪草稿 | 不可变发布快照；补全当前仅有残缺声明的文件                        |
| `packages/db-schema/src/tables/crates_table.ts`            | 修改      | nullable `anatomyVersionId` 外键               |
| `packages/db-schema/src/tables/index.ts`                   | 修改      | 只做表 re-export                                |
| `packages/db-schema/src/relations.ts`                      | 修改      | Anatomy/Draft/Version/Crate 关系               |
| `apps/app/drizzle/0014_anatomy-management.sql`             | 生成      | PostgreSQL 迁移                                |
| `apps/app/drizzle/meta/0014_snapshot.json`                 | 生成      | Drizzle schema snapshot                      |
| `apps/app/drizzle/meta/_journal.json`                      | 生成修改    | 迁移日志                                         |
| `packages/db/src/dao/anatomies-dao.ts`                     | 新增      | Anatomy 身份列表、归档和基础查询                         |
| `packages/db/src/dao/anatomy-drafts-dao.ts`                | 新增      | Draft CRUD 与 revision 乐观锁                    |
| `packages/db/src/dao/anatomy-versions-dao.ts`              | 新增      | 只读 Version 查询及事务内 insert                     |
| `packages/db/src/dao/index.ts`                             | 修改      | DAO re-export                                |
| `packages/services/src/repository/anatomies-repository.ts` | 新增      | create/save/publish 跨表事务                     |
| `packages/services/src/repository/index.ts`                | 修改      | Repository re-export                         |
| `packages/services/src/anatomy-validator.ts`               | 新增      | 发布级结构校验和错误定位                                 |
| `packages/services/src/anatomy-validator.test.ts`          | 新增      | 所有冲突和继承规则测试                                  |
| `packages/services/src/anatomies-service.ts`               | 新增      | Draft、Publish、Version 和归档业务                  |
| `packages/services/src/anatomies-service.test.ts`          | 新增      | Publish 不可变、乐观锁、Crate 使用保护                   |
| `packages/services/src/crates-service.ts`                  | 修改      | 校验并返回 Anatomy Version                        |
| `packages/services/src/repository/crates-repository.ts`    | 修改      | 事务内写入 `anatomyVersionId`                     |
| `packages/services/src/index.ts`                           | 修改      | Service re-export                            |
| `apps/app/src/integrations/trpc/routers/anatomies.ts`      | 新增      | Anatomy tRPC procedures                      |
| `apps/app/src/integrations/trpc/routers/crates.ts`         | 修改      | Crate 输入沿用共享 Schema                          |
| `apps/app/src/integrations/trpc/router.ts`                 | 修改      | 注册 `anatomiesRouter`                         |
| `apps/app/src/integrations/refine/dataProvider.ts`         | 修改      | Anatomies/Versions CRUD 和 custom mutation 映射 |
| `apps/app/src/integrations/refine/dataProvider.test.ts`    | 修改      | Refine → tRPC 映射测试                           |

### 4.2 前端

| 文件 | 操作 | 单一职责 |
|---|---|---|
| `apps/app/src/routes/_layout/architecture/anatomies/index.tsx` | 新增 | Anatomy 列表路由与 search schema |
| `apps/app/src/routes/_layout/architecture/anatomies/$id.tsx` | 新增 | Anatomy 详情/编辑路由 |
| `apps/app/src/pages/AnatomiesPage/AnatomiesPage.tsx` | 新增 | 页面 Wrapper |
| `apps/app/src/pages/AnatomiesPage/AnatomiesPageContent.tsx` | 新增 | 列表、过滤、分页和创建入口 |
| `apps/app/src/pages/AnatomiesPage/AnatomyCreateDialog.tsx` | 新增 | react-hook-form 新建 Draft 表单 |
| `apps/app/src/pages/AnatomiesPage/index.ts` | 新增 | 页面桶导出 |
| `apps/app/src/pages/AnatomyDetailPage/AnatomyDetailPage.tsx` | 新增 | 页面 Wrapper |
| `apps/app/src/pages/AnatomyDetailPage/AnatomyDetailPageContent.tsx` | 新增 | 查询状态、保存、发布、归档和版本切换协调 |
| `apps/app/src/pages/AnatomyDetailPage/AnatomyEditorForm.tsx` | 新增 | FormProvider、名称、用途和根结构编辑 |
| `apps/app/src/pages/AnatomyDetailPage/AnatomyTreeEditor.tsx` | 新增 | 根节点及同级选择/One-of 操作 |
| `apps/app/src/pages/AnatomyDetailPage/AnatomyEntryRow.tsx` | 新增 | 单个 File/Directory 编辑行 |
| `apps/app/src/pages/AnatomyDetailPage/OneOfGroupEditor.tsx` | 新增 | One-of 匹配数和替代项编辑 |
| `apps/app/src/pages/AnatomyDetailPage/FallbackPolicyEditor.tsx` | 新增 | 默认与 Entry 覆盖策略控件 |
| `apps/app/src/pages/AnatomyDetailPage/AnatomyVersionPanel.tsx` | 新增 | 历史 Version 列表和 Create draft |
| `apps/app/src/pages/AnatomyDetailPage/PublishAnatomyDialog.tsx` | 新增 | Publish 确认及结构错误定位 |
| `apps/app/src/pages/AnatomyDetailPage/index.ts` | 新增 | 页面桶导出 |
| `apps/app/src/components/AnatomyTreePreview/AnatomyTreePreview.tsx` | 新增 | 编辑页与 Crate 详情复用的只读树/策略预览 |
| `apps/app/src/components/AnatomyTreePreview/AnatomyTreePreview.test.tsx` | 新增 | 树、数量、策略来源静态渲染测试 |
| `apps/app/src/components/AnatomyTreePreview/index.ts` | 新增 | 组件桶导出 |
| `apps/app/src/lib/anatomy-tree.ts` | 新增 | 不可变 add/update/remove/group 纯函数 |
| `apps/app/src/lib/anatomy-tree.test.ts` | 新增 | 树操作和同级 One-of 约束测试 |
| `apps/app/src/pages/CratesPage/CrateAnatomyField.tsx` | 新增 | Published Version 选择和保存前预览 |
| `apps/app/src/pages/CratesPage/CrateDialog.tsx` | 修改 | 接入 `anatomyVersionId` 字段 |
| `apps/app/src/pages/CrateDetailPage/CrateAnatomyCard.tsx` | 新增 | 已绑定版本/未配置状态/显式切换入口 |
| `apps/app/src/pages/CrateDetailPage/CrateDetailPageContent.tsx` | 修改 | 组合 Anatomy Card |
| `apps/app/src/components/app-sidebar.tsx` | 修改 | Anatomy 导航及数量 |
| `apps/app/src/components/sidebar-icons.tsx` | 修改 | `AnatomiesIcon` |
| `apps/app/src/components/header-bar.tsx` | 修改 | breadcrumb 与 New Anatomy 按钮 |
| `apps/app/src/integrations/i18n/locales/en.json` | 修改 | 英文 Anatomy 文案 |
| `apps/app/src/integrations/i18n/locales/zh.json` | 修改 | 中文 Anatomy 文案 |
| `apps/app/src/routeTree.gen.ts` | 自动生成 | TanStack Router 生成结果，不手工编辑 |

## 5. Service 与 API 合约

### 5.1 发布校验

`packages/services/src/anatomy-validator.ts` 导出：

```typescript
export const AnatomyValidationCode = {
  duplicateId: "duplicate_id",
  duplicateLiteralName: "duplicate_literal_name",
  invalidPlaceholder: "invalid_placeholder",
  absolutePath: "absolute_path",
  invalidOneOfRange: "invalid_one_of_range",
  impossibleOneOf: "impossible_one_of",
} as const;

export type AnatomyValidationIssue = {
  code: (typeof AnatomyValidationCode)[keyof typeof AnatomyValidationCode];
  nodeId: string;
  parentId: string | null;
  field: "id" | "name" | "minimumMatches" | "maximumMatches";
  message: string;
};

export const validateAnatomyForPublish = function (
  input: AnatomyDraftInput,
): Result<AnatomyDraftInput, AnatomyValidationIssue[]>;
```

校验必须深度优先遍历并一次返回全部问题。固定名称冲突只在同一 Directory 或同一 One-of alternatives 范围内比较；占位名称必须匹配 `^<[^<>/\\]+>[^/\\]*$`；Windows 盘符、UNC、`/` 开头和包含 `..` 路径段均判定为真实路径表达。

One-of 必须满足：

```text
1 <= minimumMatches <= maximumMatches <= alternatives.length
```

### 5.2 Anatomy Service

```typescript
export type AnatomyServiceError = {
  type: "not_found" | "invalid_input" | "conflict" | "archived" | "in_use";
  message: string;
  issues?: AnatomyValidationIssue[];
};

export const createAnatomiesService = function (db: Database) {
  return {
    list(input: AnatomyListInput): Promise<Result<AnatomyListResult, AnatomyServiceError>>,
    getById(id: string): Promise<Result<AnatomyDetail | null, AnatomyServiceError>>,
    createDraft(input: AnatomyDraftInput): Promise<Result<AnatomyDetail, AnatomyServiceError>>,
    saveDraft(
      anatomyId: string,
      input: AnatomyDraftSaveInput,
    ): Promise<Result<AnatomyDetail, AnatomyServiceError>>,
    publish(
      anatomyId: string,
      expectedRevision: number,
    ): Promise<Result<AnatomyVersion, AnatomyServiceError>>,
    createDraftFromVersion(
      anatomyId: string,
      versionId: string,
    ): Promise<Result<AnatomyDetail, AnatomyServiceError>>,
    archive(anatomyId: string): Promise<Result<AnatomyDetail, AnatomyServiceError>>,
    listPublishedVersions(
      input: PublishedAnatomyVersionListInput,
    ): Promise<Result<PublishedAnatomyVersionListResult, AnatomyServiceError>>,
    getVersionById(id: string): Promise<Result<AnatomyVersion | null, AnatomyServiceError>>,
  };
};
```

数据库 Promise 使用 `ResultAsync.fromPromise` 映射到 `AnatomyServiceError`；不得使用裸 `try-catch`。Version DAO 只能提供查询和 `createWithTx`，不得暴露 update/delete。

### 5.3 tRPC Router

```typescript
export const anatomiesRouter = router({
  list: publicProcedure.input(anatomyListInputSchema).query(...),
  getById: publicProcedure.input(z.object({ id: z.string() })).query(...),
  createDraft: authedProcedure.input(anatomyDraftInputSchema).mutation(...),
  saveDraft: authedProcedure.input(z.object({
    id: z.string(),
    draft: anatomyDraftSaveSchema,
  })).mutation(...),
  publish: authedProcedure.input(z.object({
    id: z.string(),
    expectedRevision: z.number().int().positive(),
  })).mutation(...),
  createDraftFromVersion: authedProcedure.input(z.object({
    id: z.string(),
    versionId: z.string(),
  })).mutation(...),
  archive: authedProcedure.input(z.object({ id: z.string() })).mutation(...),
  listPublishedVersions: publicProcedure
    .input(publishedAnatomyVersionListInputSchema)
    .query(...),
  getVersionById: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(...),
});
```

Router 只解包 `Result.match()` 并转换错误，不包含发布校验、Version 计算或数据库查询。

### 5.4 Refine 资源

```typescript
export const ResourceName = {
  // existing resources
  anatomies: "anatomies",
  anatomyVersions: "anatomyVersions",
} as const;

export const AnatomyCustomAction = {
  publish: "anatomies/publish",
  createDraftFromVersion: "anatomies/create-draft-from-version",
  archive: "anatomies/archive",
} as const;
```

- `getList(anatomies)` → `trpcClient.anatomies.list.query`
- `getOne(anatomies)` → `trpcClient.anatomies.getById.query`
- `create(anatomies)` → `trpcClient.anatomies.createDraft.mutate`
- `update(anatomies)` → `trpcClient.anatomies.saveDraft.mutate`
- `getList(anatomyVersions)` → `listPublishedVersions`
- `getOne(anatomyVersions)` → `getVersionById`
- `custom` 按 `url` 映射 Publish、Create draft、Archive。

## 6. 最小任务拆解

### Task 1：建立 Anatomy Zod 契约和纯函数

**文件：**

- 新建：`packages/schemas/src/anatomy-schema.ts`
- 新建：`packages/schemas/src/anatomy-policy.ts`
- 修改：`packages/schemas/src/index.ts`
- 测试：`packages/services/src/anatomy-validator.test.ts` 的 shape/继承用例先行

- [ ] **Step 1（Red）：写递归 shape、默认 Draft 和策略继承测试**

```typescript
it("resolves entry before parent before anatomy defaults", () => {
  const result = resolveAnatomyPolicies(
    {
      missingRequired: "block",
      unexpectedEntry: "warn",
      nameMismatch: "warn",
      nestingMismatch: "block",
    },
    [{ id: "parent", overrides: { nameMismatch: "allow" } }],
    { id: "entry", overrides: { missingRequired: "warn" } },
  );

  expect(result.missingRequired).toMatchObject({ value: "warn", source: "entry" });
  expect(result.nameMismatch).toMatchObject({ value: "allow", source: "parent" });
  expect(result.unexpectedEntry).toMatchObject({ value: "warn", source: "anatomy" });
});
```

- [ ] **Step 2：运行测试确认模块不存在或导出不存在**

运行：`cd packages/services && bun run test -- src/anatomy-validator.test.ts`

预期：FAIL，提示无法解析 `@repo/schemas` 中的 Anatomy 导出。

- [ ] **Step 3（Green）：实现第 3 节完整 Zod 契约、默认值和策略解析**
- [ ] **Step 4：更新 `packages/schemas/src/index.ts`，仅 re-export，不声明变量或类型**
- [ ] **Step 5：运行 `bun run --cwd packages/schemas quality` 与目标测试，预期全部通过**
- [ ] **Step 6（Refactor）：确认没有手写重复联合类型，Quantity/Policy 只引用导出的 Values**
- [ ] **Step 7：提交 `feat(COD-225): add anatomy domain schemas`**

完成标准：嵌套 Directory、File、One-of 可通过 Zod 往返解析；File schema 无 `children`；有效策略含值和来源。

### Task 2：新增关系表、JSONB 和 Crate 外键

**文件：**

- 修改未跟踪草稿：`packages/db-schema/src/tables/anatomies_table.ts`
- 新建：`packages/db-schema/src/tables/anatomy_drafts_table.ts`
- 修改未跟踪草稿：`packages/db-schema/src/tables/anatomy_versions_table.ts`
- 修改：`packages/db-schema/src/tables/crates_table.ts`
- 修改：`packages/db-schema/src/tables/index.ts`
- 修改：`packages/db-schema/src/relations.ts`
- 生成：`apps/app/drizzle/0014_anatomy-management.sql`
- 生成：`apps/app/drizzle/meta/0014_snapshot.json`
- 修改：`apps/app/drizzle/meta/_journal.json`

- [ ] **Step 1：先确认两个未跟踪表草稿的所有者并保存其 diff；记录需要保留的设计意图**
- [ ] **Step 2（Red）：先在 `cratesTable` 类型使用 `anatomyVersionId`，运行 db-schema typecheck**

运行：`bun run --cwd packages/db-schema check-types`

预期：FAIL，当前未跟踪的 `anatomy_versions_table.ts` 声明不完整，且表尚未进入桶导出和 relations。

- [ ] **Step 3（Green）：按第 3.3 节完成三张表并加入 Crate FK；把草稿中的 `anatomise` 改为 `anatomies`、`archiveAt` 改为 `archivedAt`，确保没有重复 `created_at`，并修正 `pgTabel` 导入拼写**
- [ ] **Step 4：在 relations 中加入 Anatomy→Draft、Anatomy→Versions、Version→Crates 和 Crate→Version**
- [ ] **Step 5：桶文件只新增 re-export 行，不引入业务逻辑**
- [ ] **Step 6：运行 `bun run --cwd packages/db-schema quality`，预期类型与 lint 通过**
- [ ] **Step 7：生成命名迁移**

运行：`cd apps/app && bun run db:generate -- --name anatomy-management`

预期：生成 `0014_anatomy-management.sql`、`0014_snapshot.json` 并更新 `_journal.json`。

- [ ] **Step 8：人工审阅 SQL，确认三个新表、唯一约束、索引、nullable Crate FK 和 `ON DELETE RESTRICT`**
- [ ] **Step 9：提交 `feat(COD-225): persist anatomy drafts and versions`**

完成标准：数据库可同时表达历史 Versions 与一个活动 Draft；Crate 只能通过外键引用已存在的 Version 行。

### Task 3：实现 DAO 与事务 Repository

**文件：**

- 新建：`packages/db/src/dao/anatomies-dao.ts`
- 新建：`packages/db/src/dao/anatomy-drafts-dao.ts`
- 新建：`packages/db/src/dao/anatomy-versions-dao.ts`
- 修改：`packages/db/src/dao/index.ts`
- 新建：`packages/services/src/repository/anatomies-repository.ts`
- 修改：`packages/services/src/repository/index.ts`

- [ ] **Step 1（Red）：在 Service 测试声明以下 Repository 行为并确认导出不存在**

```typescript
type AnatomiesRepositoryContract = {
  createDraft(input: AnatomyDraftInput): Promise<{ anatomyId: string }>;
  saveDraft(
    anatomyId: string,
    expectedRevision: number,
    input: AnatomyDraftInput,
  ): Promise<"updated" | "conflict" | "not_found">;
  publish(
    anatomyId: string,
    expectedRevision: number,
    input: AnatomyDraftInput,
  ): Promise<{ versionId: string; version: number } | "conflict" | "not_found">;
  createDraftFromVersion(
    anatomyId: string,
    versionId: string,
  ): Promise<"created" | "draft_exists" | "not_found">;
};
```

- [ ] **Step 2（Green）：实现每表一个 DAO；Version DAO 不提供 update/delete**
- [ ] **Step 3：Draft update 使用 `WHERE anatomy_id = ? AND revision = ?`，成功后 `revision = revision + 1`**
- [ ] **Step 4：Repository.createDraft 在一个事务中插入 Anatomy 身份和活动 Draft**
- [ ] **Step 5：Repository.publish 在一个事务中重新检查 revision、计算 `max(version)+1`、插入 Version、删除 Draft**
- [ ] **Step 6：Repository.createDraftFromVersion 复制 Version 的 name/purpose/structure，设置 `basedOnVersionId` 和 revision=1**
- [ ] **Step 7：list 查询返回 `hasDraft`、`latestVersion`、`usageCount`，usageCount 只统计引用任一 Version 的 Crate**
- [ ] **Step 8：运行 `bun run --cwd packages/db quality` 与 `bun run --cwd packages/services check-types`**
- [ ] **Step 9（Refactor）：去除重复事务代码，DAO 只负责 Drizzle 查询，Repository 只负责跨表原子性**

完成标准：两个客户端以同一 revision 保存时只有一个成功；Publish 不留下 Draft；历史 Version 行没有更新路径。

### Task 4：实现发布校验和 Anatomy Service

**文件：**

- 新建：`packages/services/src/anatomy-validator.ts`
- 新建：`packages/services/src/anatomy-validator.test.ts`
- 新建：`packages/services/src/anatomies-service.ts`
- 新建：`packages/services/src/anatomies-service.test.ts`
- 修改：`packages/services/src/index.ts`

- [ ] **Step 1（Red）：为发布冲突写完整参数化测试**

```typescript
it.each([
  ["duplicate literal", duplicateLiteralDraft, "duplicate_literal_name"],
  ["absolute unix path", absoluteUnixDraft, "absolute_path"],
  ["windows drive path", windowsPathDraft, "absolute_path"],
  ["duplicate id", duplicateIdDraft, "duplicate_id"],
  ["invalid one-of range", invalidOneOfDraft, "invalid_one_of_range"],
])("rejects %s", (_name, draft, code) => {
  const result = validateAnatomyForPublish(draft);

  expect(result.isErr()).toBe(true);
  expect(result._unsafeUnwrapErr()).toEqual(
    expect.arrayContaining([expect.objectContaining({ code })]),
  );
});
```

- [ ] **Step 2：运行目标测试，预期 FAIL，validator 尚未实现**
- [ ] **Step 3（Green）：实现深度优先遍历、全量 issue 收集和 nodeId 定位**
- [ ] **Step 4（Red）：Service 测试覆盖保存冲突、Archived 拒绝编辑、Publish 成功、校验失败保留 Draft、从 Version 创建 Draft**
- [ ] **Step 5（Green）：按第 5.2 节实现 Service，所有失败通过 neverthrow Result 表达**
- [ ] **Step 6：Publish 先解析 JSONB 为 `anatomyStructureSchema`，再执行业务校验，最后调用事务 Repository**
- [ ] **Step 7：list/get 将数据库中的 unknown JSONB 再次经过 Zod parse；非法历史数据返回 `invalid_input`，不得把 unknown 强转为 Anatomy 类型**
- [ ] **Step 8：运行 `bun run --cwd packages/services quality`，预期全部通过**
- [ ] **Step 9：提交 `feat(COD-225): add anatomy validation and publishing`**

完成标准：AC-02、AC-03、AC-05、AC-07、AC-10、AC-11 的后端规则全部有自动化覆盖。

### Task 5：暴露 tRPC 与 Refine 资源

**文件：**

- 新建：`apps/app/src/integrations/trpc/routers/anatomies.ts`
- 修改：`apps/app/src/integrations/trpc/router.ts`
- 修改：`apps/app/src/integrations/refine/dataProvider.ts`
- 修改：`apps/app/src/integrations/refine/dataProvider.test.ts`

- [ ] **Step 1（Red）：扩展 hoisted tRPC mock，写 `getList/getOne/create/update/custom` 映射测试**

```typescript
it("maps publish custom action to anatomies.publish", async () => {
  publishAnatomy.mockResolvedValue({ id: "version-1", version: 1 });

  const result = await dataProvider.custom!({
    url: AnatomyCustomAction.publish,
    method: "post",
    payload: { id: "anatomy-1", expectedRevision: 3 },
  });

  expect(publishAnatomy).toHaveBeenCalledWith({
    id: "anatomy-1",
    expectedRevision: 3,
  });
  expect(result.data).toMatchObject({ id: "version-1", version: 1 });
});
```

- [ ] **Step 2：运行 `cd apps/app && bun run test -- src/integrations/refine/dataProvider.test.ts`，预期 FAIL**
- [ ] **Step 3（Green）：实现 Router，所有输入复用 `@repo/schemas`，只在路由组合 id/payload 对象**
- [ ] **Step 4：在 appRouter 注册 `anatomies`**
- [ ] **Step 5：实现 Refine 资源和 custom actions；UI 代码不得导入 `trpcClient`**
- [ ] **Step 6：运行目标测试、`bun run --cwd apps/app check-types` 和 lint**
- [ ] **Step 7：提交 `feat(COD-225): expose anatomy trpc resources`**

完成标准：前端所有 Anatomy 查询和命令均可通过 Refine hook 执行；Draft 不出现在 Published Versions 列表。

### Task 6：实现 Anatomy 列表与创建 Draft

**文件：**

- 新建：`apps/app/src/routes/_layout/architecture/anatomies/index.tsx`
- 新建：`apps/app/src/pages/AnatomiesPage/AnatomiesPage.tsx`
- 新建：`apps/app/src/pages/AnatomiesPage/AnatomiesPageContent.tsx`
- 新建：`apps/app/src/pages/AnatomiesPage/AnatomyCreateDialog.tsx`
- 新建：`apps/app/src/pages/AnatomiesPage/index.ts`

- [ ] **Step 1（Red）：为 create search 参数、状态过滤和空状态写页面静态/纯函数测试**
- [ ] **Step 2：实现路由 search schema**

```typescript
const anatomyStatusSchema = z.enum(["draft", "published", "archived"]);

const searchSchema = z.object({
  create: z.boolean().optional(),
  search: z.string().optional(),
  status: anatomyStatusSchema.optional(),
  page: z.number().int().positive().optional(),
});
```

- [ ] **Step 3：`AnatomiesPage` 只渲染 `AnatomiesPageContent`，不承载查询或业务逻辑**
- [ ] **Step 4：Content 使用 `useList` 的 `query.isLoading` 驱动 `LoadingState`，URL 是搜索、状态、页码的单一来源**
- [ ] **Step 5：列表展示 name、Draft 徽标、latest vN、publishedAt、usageCount、Archived 徽标**
- [ ] **Step 6：Create Dialog 使用 react-hook-form + zodResolver + 项目 Button/Input/Textarea/Select；提交 `createEmptyAnatomyDraft`**
- [ ] **Step 7：创建成功导航到 `/architecture/anatomies/$id`，关闭时移除 `create` search 参数**
- [ ] **Step 8：运行 app 目标测试、typecheck 和 lint**

完成标准：AC-01；列表可独立浏览 Draft、Published、Archived，Published+Draft 可同时显示。

### Task 7：实现目录树编辑、One-of、策略与实时预览

**文件：**

- 新建：`apps/app/src/routes/_layout/architecture/anatomies/$id.tsx`
- 新建：`apps/app/src/pages/AnatomyDetailPage/AnatomyDetailPage.tsx`
- 新建：`apps/app/src/pages/AnatomyDetailPage/AnatomyDetailPageContent.tsx`
- 新建：`apps/app/src/pages/AnatomyDetailPage/AnatomyEditorForm.tsx`
- 新建：`apps/app/src/pages/AnatomyDetailPage/AnatomyTreeEditor.tsx`
- 新建：`apps/app/src/pages/AnatomyDetailPage/AnatomyEntryRow.tsx`
- 新建：`apps/app/src/pages/AnatomyDetailPage/OneOfGroupEditor.tsx`
- 新建：`apps/app/src/pages/AnatomyDetailPage/FallbackPolicyEditor.tsx`
- 新建：`apps/app/src/lib/anatomy-tree.ts`
- 新建：`apps/app/src/lib/anatomy-tree.test.ts`

- [ ] **Step 1（Red）：为树纯函数写 add/update/remove/group 测试**

```typescript
it("groups selected siblings as exactly one", () => {
  const result = groupSiblingEntries(root, null, [indexTs.id, indexTsx.id]);

  expect(result.children).toHaveLength(1);
  expect(result.children[0]).toMatchObject({
    kind: "one_of",
    minimumMatches: 1,
    maximumMatches: 1,
    alternatives: [indexTs, indexTsx],
  });
});

it("refuses to insert a child below a file", () => {
  const result = insertAnatomyNode(root, file.id, childFile);

  expect(result).toEqual(root);
});
```

- [ ] **Step 2（Green）：纯函数使用不可变递归，不修改 Refine query cache 返回对象**
- [ ] **Step 3：Editor 使用 `FormProvider<AnatomyDraftSaveInput>`；子组件通过 `useFormContext` 读取字段，避免传递整棵树 props**
- [ ] **Step 4：Directory 行显示 Add File/Add Directory；File 行不显示 Add，并用说明文字表达 only directories contain children**
- [ ] **Step 5：名称控件先选 Literal/Placeholder，再输入 value；Quantity 只使用共享 Values 渲染项目 Select**
- [ ] **Step 6：同一父节点选择至少两个 Entry 后启用 Group as One of；Group 编辑 minimum/maximum 且 maximum 不超过 alternatives 数量**
- [ ] **Step 7：Fallback 编辑器分别呈现四个策略；Entry override 增加 `inherit` UI 值，但提交时把 inherit 转为字段缺失**
- [ ] **Step 8：保存调用 `useUpdate` 并携带当前 revision；409/conflict 显示“Draft 已被其他会话更新，请重新载入”，不静默覆盖**
- [ ] **Step 9：保存成功以服务端返回 revision reset 表单 dirty 状态**
- [ ] **Step 10：运行 lib 测试、app tests、typecheck、lint**

完成标准：AC-04、AC-05、AC-06、AC-07、AC-08、AC-09；重新加载后树、名称和数量保持一致。

### Task 8：实现预览、发布和 Version 历史

**文件：**

- 新建：`apps/app/src/components/AnatomyTreePreview/AnatomyTreePreview.tsx`
- 新建：`apps/app/src/components/AnatomyTreePreview/AnatomyTreePreview.test.tsx`
- 新建：`apps/app/src/components/AnatomyTreePreview/index.ts`
- 新建：`apps/app/src/pages/AnatomyDetailPage/AnatomyVersionPanel.tsx`
- 新建：`apps/app/src/pages/AnatomyDetailPage/PublishAnatomyDialog.tsx`
- 修改：`apps/app/src/pages/AnatomyDetailPage/AnatomyDetailPageContent.tsx`
- 新建：`apps/app/src/pages/AnatomyDetailPage/index.ts`

- [ ] **Step 1（Red）：静态渲染测试验证文件夹层级、Quantity、One-of 和 `entry/parent/anatomy` 来源标签**
- [ ] **Step 2（Green）：Preview 只接收 `AnatomyStructure`，使用共享策略解析函数，不发起查询**
- [ ] **Step 3：Preview 对每个策略显示 `Block/Warn/Allow · Entry override/Inherited from <directory>/Anatomy default`**
- [ ] **Step 4：Publish Dialog 提交当前 revision；若表单 dirty，先保存成功再 publish，避免发布旧快照**
- [ ] **Step 5：Publish 返回 issues 时按 `nodeId` 高亮并滚动到第一条冲突；Draft 和表单内容保持不变**
- [ ] **Step 6：Publish 成功切换为只读 Version 视图，展示 version、publishedAt、usageCount 和完整 Preview**
- [ ] **Step 7：Version Panel 可回访每个历史 Version；Create draft 只在没有活动 Draft 且未 Archived 时启用**
- [ ] **Step 8：Archive 需要确认；归档后隐藏编辑/发布/Create draft，保留历史 Version**
- [ ] **Step 9：运行目标组件测试和 app quality**
- [ ] **Step 10：提交 `feat(COD-225): add anatomy management pages`**

完成标准：AC-02、AC-03、AC-10、AC-11；已发布内容没有任何保存或删除控件。

### Task 9：让 Crate 选择并回访 Published Version

**文件：**

- 修改：`packages/schemas/src/crate-schema.ts`
- 修改：`packages/db-schema/src/tables/crates_table.ts`（Task 2 已完成字段）
- 修改：`packages/services/src/repository/crates-repository.ts`
- 修改：`packages/services/src/crates-service.ts`
- 修改：`apps/app/src/integrations/trpc/routers/schemas.ts`
- 新建：`apps/app/src/pages/CratesPage/CrateAnatomyField.tsx`
- 修改：`apps/app/src/pages/CratesPage/CrateDialog.tsx`
- 新建：`apps/app/src/pages/CrateDetailPage/CrateAnatomyCard.tsx`
- 修改：`apps/app/src/pages/CrateDetailPage/CrateDetailPageContent.tsx`

- [ ] **Step 1（Red）：扩展 crate schema 测试，覆盖 UUID/null/省略值；Service 测试覆盖不存在 Version 拒绝保存**
- [ ] **Step 2（Green）：在 `crateWriteSchema` 增加 `anatomyVersionId: z.string().nullable().optional()`，类型继续由 Zod 推导**
- [ ] **Step 3：Crates Repository 将 anatomyVersionId 作为 crates 表普通字段写入事务，不建立中间绑定表**
- [ ] **Step 4：Crates Service create/update 对非 null id 调用 Version DAO；查不到即返回 invalid_input**
- [ ] **Step 5：Crate list/detail 返回下列只读摘要**

```typescript
type CrateAnatomyVersionSummary = {
  id: string;
  anatomyId: string;
  name: string;
  version: number;
  purpose: string;
  structure: AnatomyStructure;
  publishedAt: Date | string;
};
```

- [ ] **Step 6：CrateAnatomyField 使用 `useList(ResourceName.anatomyVersions)`，选项显示 name、vN、publishedAt、usageCount；Draft 不经过该资源返回**
- [ ] **Step 7：选择后立即显示 `AnatomyTreePreview`，允许选择空值；编辑时保持当前 Version id，不根据 latestVersion 自动替换**
- [ ] **Step 8：CrateAnatomyCard 在 null 时显示明确未配置状态，在有值时展示名称、vN、发布时间和完整树**
- [ ] **Step 9：Change Anatomy 打开现有 CrateDialog；从 v1 切到 v2 必须点击 Save，不能因列表刷新自动提交**
- [ ] **Step 10：运行 crate/service 测试和 app quality**
- [ ] **Step 11：提交 `feat(COD-225): bind published anatomy versions to crates`**

完成标准：AC-12、AC-13、AC-14、AC-15；新 Version 发布后已有 Crate 的 FK 保持不变。

### Task 10：接入导航、i18n 和路由生成

**文件：**

- 修改：`apps/app/src/components/app-sidebar.tsx`
- 修改：`apps/app/src/components/sidebar-icons.tsx`
- 修改：`apps/app/src/components/header-bar.tsx`
- 修改：`apps/app/src/integrations/i18n/locales/en.json`
- 修改：`apps/app/src/integrations/i18n/locales/zh.json`
- 自动生成：`apps/app/src/routeTree.gen.ts`

- [ ] **Step 1（Red）：Header/AppSidebar 静态测试期望 Anatomies 链接和标题**
- [ ] **Step 2（Green）：新增 `AnatomiesIcon`，Architecture 导航顺序为 Archetypes、Crates、Anatomies**
- [ ] **Step 3：Sidebar 使用 `useList(ResourceName.anatomies, pageSize: 1)` 获取总数**
- [ ] **Step 4：Header 增加列表 breadcrumb、详情 breadcrumb 和 New Anatomy 按钮，按钮写入 `create=true`**
- [ ] **Step 5：中英文 JSON 使用完全相同的 key 集，所有新增可见文案通过 `t()` 获取**
- [ ] **Step 6：运行 `cd apps/app && bun run dev` 触发 route tree 生成后停止开发服务器**
- [ ] **Step 7：运行 app quality，预期 route 类型无错误**

完成标准：可以从 Architecture 导航进入列表、创建 Draft、打开详情；英文和中文界面无裸 key。

### Task 11：全量验收、迁移 Neon 和记录结果

**文件：**

- 修改：`docs/COD-225/plan.md`

- [ ] **Step 1：运行包级质量检查**

```bash
bun run --cwd packages/schemas quality
bun run --cwd packages/db-schema quality
bun run --cwd packages/db quality
bun run --cwd packages/services quality
bun run --cwd apps/app quality
```

预期：TypeScript、oxlint、Vitest 全部退出 0。

- [ ] **Step 2：运行仓库全量检查**

```bash
bun run quality
bun run build
bun run knip
```

预期：无新增错误；若 knip 报告仓库既有问题，在实施记录中区分既有与本次新增。

- [ ] **Step 3：使用本地数据库先执行 `bun run db:push`，按 AC-01 至 AC-16 完成 UI 手工验收**
- [ ] **Step 4：确认 `.env` 当前 `DATABASE_URL` 指向 Neon 后执行 `bun run db:push`**
- [ ] **Step 5：只读查询确认 `anatomies`、`anatomy_drafts`、`anatomy_versions` 和 `crates.anatomy_version_id` 已存在**
- [ ] **Step 6：验证 v1 Crate 在 v2 发布后仍引用 v1；验证 Version 无编辑/删除入口；验证 Anatomy JSON 不含仓库和真实路径字段**
- [ ] **Step 7：在本计划第 9 节逐项更新状态并填写实施记录**
- [ ] **Step 8：提交 `test(COD-225): cover anatomy workflows`**

完成标准：全量质量检查通过，Neon schema 已迁移，16 条 AC 均有自动化证据或明确的手工验收记录。

## 7. 验收映射

| AC | 验收标准 | 实现 Task | 自动化/手工证据 | 状态 |
|---|---|---|---|---|
| AC-01 | 创建并继续编辑 Draft | 4、5、6 | Service + 页面流程 | ⬜ |
| AC-02 | 发布不可变 Version | 3、4、8 | Publish Service 测试 + UI | ⬜ |
| AC-03 | 从 Version 创建新 Draft | 3、4、8 | Repository/Service 测试 | ⬜ |
| AC-04 | 根下新增 File/Directory | 7 | tree pure function + UI | ⬜ |
| AC-05 | File 不能包含子项 | 1、4、7 | schema/tree/validator 测试 | ⬜ |
| AC-06 | 名称与 Quantity 持久化 | 1、3、7 | save/reload 手工 + Service | ⬜ |
| AC-07 | One-of 恰好一个 | 1、4、7 | validator + tree 测试 | ⬜ |
| AC-08 | Missing required = Block | 7、8 | preview 测试 | ⬜ |
| AC-09 | Unexpected entry = Warn | 7、8 | preview 测试 | ⬜ |
| AC-10 | 解释策略继承来源 | 1、8 | policy + preview 测试 | ⬜ |
| AC-11 | 冲突阻止发布并定位 | 4、8 | validator + Publish UI | ⬜ |
| AC-12 | Crate 保存和回访 Version | 2、9 | Service + Crate UI | ⬜ |
| AC-13 | Draft 不可选择 | 5、9 | dataProvider/Service 测试 | ⬜ |
| AC-14 | 新版本不自动升级 | 2、9、11 | FK 断言 + 手工流程 | ⬜ |
| AC-15 | Crate 可不配置 Anatomy | 1、9 | schema + UI empty state | ⬜ |
| AC-16 | 不产生错误领域关联 | 1、2、4、11 | schema 审查 + JSON 检查 | ⬜ |

## 8. 风险、边界与缓解

| 风险 | 影响 | 缓解 |
|---|---|---|
| JSONB 无法用 FK/CHECK 表达递归树规则 | 非法结构可能落库 | 保存执行 Zod shape 校验；Publish 执行完整业务校验；读取再次 parse |
| 两个页面同时编辑同一 Draft | 后保存者覆盖前者 | revision 乐观锁，冲突要求显式重新载入 |
| 并发 Publish 得到相同版本号 | 唯一约束冲突 | 事务内计算 next version，并由 `(anatomyId, version)` 唯一索引兜底 |
| Anatomy 同时 Published 和 Draft，单状态字段失真 | 列表过滤/徽标错误 | 使用 `hasDraft`、`latestVersion`、`archivedAt` 三个正交字段 |
| 有效策略被持久化后过期 | 父策略变化但子摘要未更新 | 仅保存 defaults/overrides，预览实时派生 |
| 大型 JSON 更新产生行重写 | Draft 保存开销上升 | 当前结构规模预期较小；超过千节点、出现协同编辑需求时另立扁平 Draft 设计 |
| Crate 选择器误返回 Draft | 违反版本稳定性 | 独立 `anatomyVersions` 资源只查询 versions 表 |
| Archived Version 被 Crate 引用 | 详情无法回访 | Archive 只影响 Anatomy 编辑入口，不隐藏已引用 Version 查询 |
| Neon migration 作用于线上数据库 | schema 变更风险 | 先审阅生成 SQL并在本地验证；质量检查通过后再切换 DATABASE_URL 推送 Neon |
| `CrateDialog.tsx` 与其他工作并行修改 | 合并冲突 | 实施 Task 9 前重新读取 worktree diff，只做局部接入并保留用户改动 |

## 9. 实施记录

| 日期 | Task | 变更 | 验证 | 提交 |
|---|---|---|---|---|
| 2026-07-20 | 计划 | 从 Linear 拉取 COD-225、附件、关联需求和评论；完成 JSONB/关系模型决策与仓库影响分析 | `prd.md`、`plan.md` 自审 | — |

## 10. 计划自审结果

- [x] 已覆盖 PRD 的 4 个 Task 和 16 条 Acceptance Criteria。
- [x] 已明确 JSONB 聚合边界、关系表、不可变 Version 和 nullable Crate FK。
- [x] 已列出具体创建/修改文件、接口签名、测试样例、命令和完成标准。
- [x] 已按 Schema → DB → DAO/Repository → Service → Router/Refine → Frontend → Migration 排序。
- [x] 已纳入 Red → Green → Refactor、频繁提交、neverthrow、Zod 推导类型和 Refine 数据访问约束。
- [x] 已排除 Bonus、Repository/Path、Archetype、Rule、扫描与 Finding。
- [x] 计划正文不存在未决占位符；Drizzle 迁移通过固定 `--name anatomy-management` 获得可追踪文件名。
