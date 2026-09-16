# COD-306 Task 10：Settings 工具目录与调用记录详细实现计划
> Last Format Time：8/13/2026 15:14:03

> **执行指引：** 推荐使用 `subagent-driven-development` 技能逐任务执行此计划；如果你自己实现，请严格按 checkbox 顺序，一次只完成一个小节。
> 步骤使用 checkbox (`- [ ]`) 追踪进度。所有命令默认从仓库根目录 `G:\Save\Grogramming\CodeForge\daedalus` 执行。

**目标：** 在 `Settings → AI Reviews → MCP → 连接详情` 中增加“可用工具”和“调用记录”两个 Tab，让用户能看清每个 Tool 的权限、确认要求及每次调用的结果。

**架构：** tRPC Router 先验证当前用户拥有目标 MCP Connection，再读取 Tool Catalog 或 Invocation DAO。前端只能经 Refine `useList` 访问 DataProvider，页面组件不直接调用 tRPC。容器组件负责查询状态，展示组件只负责分组、表格与 Badge。

**技术栈：** TypeScript、Zod v4、tRPC、Refine v5、React 19、Radix Tabs、项目现有 Table/Badge/LoadingState/ErrorState/EmptyState、Vitest、Storybook。

---
## 开始前先看懂数据怎么流动
```mermaid
flowchart LR
  Dialog["McpConnectionDetailsDialog"] --> ToolsTab["McpAvailableToolsTab"]
  Dialog --> HistoryTab["McpInvocationHistoryTab"]
  ToolsTab --> UseListA["Refine useList"]
  HistoryTab --> UseListB["Refine useList"]
  UseListA --> Provider["dataProvider.getList"]
  UseListB --> Provider
  Provider --> Router["mcpConnectionsRouter"]
  Router --> Owner["getForOwner：隐藏他人连接"]
  Owner --> Catalog["McpToolCatalog"]
  Owner --> Dao["mcpToolInvocationsDao.listByConnection"]
```

必须保持下面三条安全边界：

1. 浏览器传 `connectionId`，但不能传 `workspaceId`；Workspace 由 Connection 决定。
2. Router 必须先调用 `getForOwner(connectionId, sessionUserId)`，验证通过后才允许查询 Invocation DAO。
3. 查询别人的 Connection 一律返回 `NOT_FOUND`，不能返回 `FORBIDDEN`，避免泄露该连接存在。

---
## 文件结构规划
### 共享契约
- 修改 `packages/schemas/src/mcp-tool-schema.ts`：增加 Invocation 列表输入、Invocation 展示模型及推导类型。
- 修改 `packages/services/src/mcp-tool/mcp-tool-contracts.test.ts`：验证分页边界和展示模型，复用现有 Vitest 配置。

### 服务端适配
- 修改 `apps/app/src/integrations/trpc/routers/mcp-connections.ts`：新增 `listTools`、`listInvocations`。
- 新建 `apps/app/src/integrations/trpc/routers/mcp-connections.test.ts`：验证 owner、分页和信息隐藏。

### Refine 数据层
- 修改 `apps/app/src/integrations/refine/dataProvider.ts`：增加两个只读 Resource。
- 修改 `apps/app/src/integrations/refine/dataProvider.test.ts`：验证 filter 和分页映射。

### 页面专用组件
- 新建 `apps/app/src/pages/AiReviewsSettingsPage/McpAvailableToolsTab/`：查询容器。
- 新建 `apps/app/src/pages/AiReviewsSettingsPage/McpAvailableToolsList/`：纯展示组件和 Storybook。
- 新建 `apps/app/src/pages/AiReviewsSettingsPage/McpInvocationHistoryTab/`：查询、分页和状态容器。
- 新建 `apps/app/src/pages/AiReviewsSettingsPage/McpInvocationHistoryTable/`：纯表格组件和 Storybook。
- 修改 `apps/app/src/pages/AiReviewsSettingsPage/McpConnectionDetailsDialog/`：只组合三个 Tab。

这些组件只服务于 `AiReviewsSettingsPage`，不要放进全局 `apps/app/src/components/`。

### 文案
- 修改 `apps/app/src/integrations/i18n/locales/zh.json`。
- 修改 `apps/app/src/integrations/i18n/locales/en.json`。
- 新建 `apps/app/src/integrations/i18n/mcp-translations.test.ts`。
- 修改 Consent、Setup Page 和 `/mcp/setup` 中引用的旧 key。

---
## Task 10.0：确认 Task 1–9 基线
- [x] **Step 1：确认工作分支和状态**

```powershell
git branch --show-current
git status --short
```

预期：分支是 COD-306 功能分支。若工作区不干净，先确认现有改动属于 Task 1–9，不要用 `git reset --hard` 或 `git checkout --` 清理。

- [x] **Step 2：确认 Task 10 的依赖已存在**

```powershell
Test-Path 'packages/schemas/src/mcp-tool-schema.ts'
Test-Path 'packages/models/src/daos/mcpToolInvocationsDao/mcpToolInvocationsDao.ts'
Test-Path 'apps/app/src/integrations/mcp/mcp-tool-registry.ts'
Select-String -Path 'apps/app/src/integrations/mcp/mcp-tool-registry.ts' -Pattern 'auditedExecute'
```

预期：前三条输出 `True`，最后一条能找到调用审计包装。任何一项失败都先停止 Task 10。

- [x] **Step 3：跑基线测试**

```powershell
Set-Location apps/app
bun run test src/integrations/mcp/mcp-protocol-handler.test.ts
bun run check-types
Set-Location ../..
```

预期：协议测试和类型检查通过。记录现有、与本任务无关的警告，不要顺手修改其他页面。

---
## Task 10.1：补齐前后端共享的 Invocation 契约
### 文件
- 修改 `packages/schemas/src/mcp-tool-schema.ts`
- 修改 `packages/services/src/mcp-tool/mcp-tool-contracts.test.ts`

- [ ] **Step 1：先写分页与记录 Schema 测试（Red）**

在现有 `packages/services/src/mcp-tool/mcp-tool-contracts.test.ts` 的 `@repo/schemas` import 中加入：

```typescript
mcpToolInvocationListInputSchema,
mcpToolInvocationSchema,
```

然后把下面三个测试追加到现有 `describe`：

```typescript
  it("applies safe pagination defaults", () => {
    expect(mcpToolInvocationListInputSchema.parse({
      connectionId: "connection-a",
    })).toEqual({
      connectionId: "connection-a",
      limit: 20,
      offset: 0,
    });
  });

  it("rejects an oversized page", () => {
    const result = mcpToolInvocationListInputSchema.safeParse({
      connectionId: "connection-a",
      limit: 51,
      offset: 0,
    });

    expect(result.success).toBe(false);
  });

  it("accepts the bounded invocation shape shown by Settings", () => {
    expect(mcpToolInvocationSchema.safeParse({
      id: "invocation-a",
      connectionId: "connection-a",
      workspaceId: "workspace-a",
      durationMs: 25,
      toolName: "project_get",
      module: "project",
      accessLevel: "read",
      outcome: "success",
      resultSummary: "{\"id\":\"project-a\"}",
      errorCode: null,
      errorMessage: null,
      createdAt: new Date("2026-08-07T00:00:00.000Z"),
    }).success).toBe(true);
  });
```

- [ ] **Step 2：运行测试确认失败**

```powershell
Set-Location packages/services
bun run test src/mcp-tool/mcp-tool-contracts.test.ts
```

预期：FAIL，提示 `mcpToolInvocationListInputSchema` 或 `mcpToolInvocationSchema` 尚未导出。

- [ ] **Step 3：实现 Schema（Green）**

在 `packages/schemas/src/mcp-tool-schema.ts` 末尾、`mcpToolErrorSchema` 之前加入：

```typescript
export const mcpToolInvocationListInputSchema = z.object({
  connectionId: z.string().min(1),
  limit: z.number().int().min(1).max(50).default(20),
  offset: z.number().int().min(0).default(0),
});

export const mcpToolInvocationSchema = z.object({
  id: z.string().min(1),
  connectionId: z.string().min(1),
  workspaceId: z.string().min(1),
  durationMs: z.number().int().min(0),
  toolName: z.string().min(1),
  module: mcpToolModuleSchema,
  accessLevel: mcpToolAccessLevelSchema,
  outcome: mcpToolOutcomeSchema,
  resultSummary: z.string().max(500).nullable(),
  errorCode: z.string().nullable(),
  errorMessage: z.string().nullable(),
  createdAt: z.date(),
});

export type McpToolInvocationListInput = z.infer<
  typeof mcpToolInvocationListInputSchema
>;
export type McpToolInvocation = z.infer<typeof mcpToolInvocationSchema>;
```

`packages/schemas/src/index.ts` 已经 `export * from "./mcp-tool-schema"`，不要再加重复导出。

- [ ] **Step 4：验证 Schema**

```powershell
bun run test src/mcp-tool/mcp-tool-contracts.test.ts
bun run check-types
bun run lint
Set-Location ../..
```

预期：测试、类型检查、lint 全部通过。

- [ ] **Step 5：提交本小节**

```powershell
git add packages/schemas/src/mcp-tool-schema.ts packages/services/src/mcp-tool/mcp-tool-contracts.test.ts
git commit -m "feat(COD-306): define mcp invocation query contract"
```

---
## Task 10.2：增加受 owner 保护的 tRPC 查询
### 文件
- 修改 `apps/app/src/integrations/trpc/routers/mcp-connections.ts`
- 新建 `apps/app/src/integrations/trpc/routers/mcp-connections.test.ts`

- [ ] **Step 1：创建 Router 失败测试（Red）**

创建测试文件，先覆盖三条最关键规则：

```typescript
import { beforeEach, describe, expect, it, vi } from "vitest";
import { err, ok } from "neverthrow";

vi.hoisted(() => {
  process.env.DATABASE_URL =
    "postgresql://postgres:test@localhost:5432/daedalus";
});

const getForOwner = vi.fn();
const listByConnection = vi.fn();

vi.mock("@repo/db", () => ({ db: {} }));
vi.mock("@repo/models", () => ({
  createMcpToolInvocationsDao: vi.fn(() => ({ listByConnection })),
}));
vi.mock("@repo/services", () => ({
  createMcpConnectionsService: vi.fn(() => ({ getForOwner })),
  createMcpSetupService: vi.fn(() => ({
    createDescriptor: vi.fn(),
  })),
}));
vi.mock("@/integrations/server-env", () => ({
  getServerEnv: vi.fn(() => ({ VITE_APP_URL: "http://localhost:9431" })),
}));

import { McpToolCatalog } from "@repo/schemas";
import { mcpConnectionsRouter } from "./mcp-connections";

const caller = function(userId = "user-a") {
  return mcpConnectionsRouter.createCaller({
    session: { user: { id: userId } },
    workspaceId: null,
  });
};

describe("mcpConnectionsRouter tool visibility", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns NOT_FOUND before reading another owner's invocations", async () => {
    getForOwner.mockResolvedValue(err({
      type: "not_found",
      message: "MCP connection not found",
    }));

    await expect(caller("user-b").listInvocations({
      connectionId: "connection-a",
      limit: 20,
      offset: 0,
    })).rejects.toMatchObject({ code: "NOT_FOUND" });
    expect(listByConnection).not.toHaveBeenCalled();
  });

  it("returns the catalog only after owner validation", async () => {
    getForOwner.mockResolvedValue(ok({ id: "connection-a" }));

    const result = await caller().listTools({ id: "connection-a" });

    expect(result).toEqual(McpToolCatalog);
    expect(getForOwner).toHaveBeenCalledWith("connection-a", "user-a");
  });

  it("returns the owner's paginated invocation history", async () => {
    getForOwner.mockResolvedValue(ok({ id: "connection-a" }));
    listByConnection.mockResolvedValue({ rows: [], total: 0 });

    const result = await caller().listInvocations({
      connectionId: "connection-a",
      limit: 20,
      offset: 40,
    });

    expect(result).toEqual({ rows: [], total: 0 });
    expect(listByConnection).toHaveBeenCalledWith("connection-a", {
      limit: 20,
      offset: 40,
    });
  });
});
```

- [ ] **Step 2：运行测试确认失败**

```powershell
Set-Location apps/app
bun run test src/integrations/trpc/routers/mcp-connections.test.ts
```

预期：FAIL，提示 Router 中没有 `listTools` / `listInvocations`。

- [ ] **Step 3：实现 owner 检查和查询（Green）**

在 `mcp-connections.ts` 增加导入：

```typescript
import { createMcpToolInvocationsDao } from "@repo/models";
import {
  McpToolCatalog,
  createMcpConnectionInputSchema,
  mcpConnectionIdInputSchema,
  mcpToolInvocationListInputSchema,
  type McpConnection,
} from "@repo/schemas";
```

在 `withSetup` 后面增加统一 owner 检查：

```typescript
const requireOwnedConnection = async function(
  connectionId: string,
  ownerUserId: string,
): Promise<void> {
  const result = await service().getForOwner(connectionId, ownerUserId);
  if (result.isErr()) {
    throw new TRPCError({
      code: "NOT_FOUND",
      message: "MCP connection not found",
    });
  }
};
```

在 `mcpConnectionsRouter` 的 `getById` 后加入：

```typescript
listTools: authedProcedure
  .input(mcpConnectionIdInputSchema)
  .query(async ({ ctx, input }) => {
    await requireOwnedConnection(input.id, getUserId(ctx.session));

    return [...McpToolCatalog];
  }),

listInvocations: authedProcedure
  .input(mcpToolInvocationListInputSchema)
  .query(async ({ ctx, input }) => {
    await requireOwnedConnection(
      input.connectionId,
      getUserId(ctx.session),
    );

    return createMcpToolInvocationsDao(db).listByConnection(
      input.connectionId,
      { limit: input.limit, offset: input.offset },
    );
  }),
```

不要把 `workspaceId` 加到输入，也不要先查 Invocation 再验证 owner。

- [ ] **Step 4：验证 Router**

```powershell
bun run test src/integrations/trpc/routers/mcp-connections.test.ts
bun run check-types
Set-Location ../..
```

预期：三个测试全部通过。

- [ ] **Step 5：提交本小节**

```powershell
git add apps/app/src/integrations/trpc/routers/mcp-connections.ts apps/app/src/integrations/trpc/routers/mcp-connections.test.ts
git commit -m "feat(COD-306): expose owned mcp tool history queries"
```

---
## Task 10.3：把两个查询接入 Refine DataProvider
### 文件
- 修改 `apps/app/src/integrations/refine/dataProvider.ts`
- 修改 `apps/app/src/integrations/refine/dataProvider.test.ts`

- [ ] **Step 1：先扩展测试 mock（Red）**

在 `dataProvider.test.ts` 的 `vi.hoisted` 中加入：

```typescript
listMcpTools: vi.fn(),
listMcpToolInvocations: vi.fn(),
```

在 `trpcClient.mcpConnections` mock 中加入：

```typescript
listTools: { query: listMcpTools },
listInvocations: { query: listMcpToolInvocations },
```

增加测试：

```typescript
it("maps MCP Tool catalog and invocation history filters", async () => {
  listMcpTools.mockResolvedValue([{ name: "project_get" }]);
  listMcpToolInvocations.mockResolvedValue({
    rows: [{ id: "invocation-a" }],
    total: 41,
  });

  const tools = await dataProvider.getList({
    resource: ResourceName.mcpAvailableTools,
    filters: [{
      field: "connectionId",
      operator: "eq",
      value: "connection-a",
    }],
  });
  const invocations = await dataProvider.getList({
    resource: ResourceName.mcpToolInvocations,
    filters: [{
      field: "connectionId",
      operator: "eq",
      value: "connection-a",
    }],
    pagination: { currentPage: 3, pageSize: 20 },
  });

  expect(listMcpTools).toHaveBeenCalledWith({ id: "connection-a" });
  expect(listMcpToolInvocations).toHaveBeenCalledWith({
    connectionId: "connection-a",
    limit: 20,
    offset: 40,
  });
  expect(tools.total).toBe(1);
  expect(invocations).toEqual({
    data: [{ id: "invocation-a" }],
    total: 41,
  });
});
```

- [x] **Step 2：运行测试确认失败**

```powershell
Set-Location apps/app
bun run test src/integrations/refine/dataProvider.test.ts
```

预期：FAIL，提示新 Resource 不存在或 `getList` 未实现。

- [x] **Step 3：增加 Resource 和映射（Green）**

在 `ResourceName` 中加入：

```typescript
mcpAvailableTools: "mcpAvailableTools",
mcpToolInvocations: "mcpToolInvocations",
```

在 `getList` 的 `mcpConnections` case 后加入：

```typescript
case ResourceName.mcpAvailableTools: {
  const connectionId = getFilterValue(params, "connectionId");
  if (!connectionId) return { data: [], total: 0 };

  const data = await trpcClient.mcpConnections.listTools.query({
    id: connectionId,
  });

  return { data: data as unknown as TData[], total: data.length };
}
case ResourceName.mcpToolInvocations: {
  const connectionId = getFilterValue(params, "connectionId");
  if (!connectionId) return { data: [], total: 0 };

  const { currentPage = 1, pageSize = 20 } = params.pagination ?? {};
  const result = await trpcClient.mcpConnections.listInvocations.query({
    connectionId,
    limit: pageSize,
    offset: (currentPage - 1) * pageSize,
  });

  return {
    data: result.rows as unknown as TData[],
    total: result.total,
  };
}
```

- [x] **Step 4：验证 DataProvider**

```powershell
bun run test src/integrations/refine/dataProvider.test.ts
bun run check-types
Set-Location ../..
```

预期：测试通过；分页第 3 页准确映射为 `offset: 40`。

- [x] **Step 5：提交本小节**

```powershell
git add apps/app/src/integrations/refine/dataProvider.ts apps/app/src/integrations/refine/dataProvider.test.ts
git commit -m "feat(COD-306): map mcp visibility resources in refine"
```

---
## Task 10.4：实现 Available Tools 展示组件
### 文件
- 新建 `apps/app/src/pages/AiReviewsSettingsPage/McpAvailableToolsList/McpAvailableToolsList.tsx`
- 新建对应 `.test.tsx`、`.stories.tsx`、`index.ts`
- 新建 `apps/app/src/pages/AiReviewsSettingsPage/McpAvailableToolsTab/McpAvailableToolsTab.tsx`
- 新建对应 `.test.tsx`、`index.ts`

- [ ] **Step 1：先写纯展示组件测试（Red）**

测试必须证明：按 module 分组、Metadata Tool 全为 Read、确认标识可见。

```typescript
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it, vi } from "vitest";
import { McpToolCatalog } from "@repo/schemas";
import { McpAvailableToolsList } from "./McpAvailableToolsList";

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}));

describe("McpAvailableToolsList", () => {
  it("groups tools and shows access/confirmation metadata", () => {
    vi.stubGlobal("React", React);
    const markup = renderToStaticMarkup(
      <McpAvailableToolsList tools={[...McpToolCatalog]} />,
    );

    expect(markup).toContain("project_get");
    expect(markup).toContain("finding_update_status");
    expect(markup).toContain("mcp.availableTools.access.read");
    expect(markup).toContain("mcp.availableTools.confirmation.required");
  });
});
```

- [ ] **Step 2：实现纯展示组件（Green）**

实现时使用以下固定规则：

```typescript
const moduleOrder = [
  "workspace",
  "project",
  "repository",
  "crate",
  "archetype",
  "anatomy",
  "dictionary",
  "rule",
  "scan_profile",
  "scan",
  "run",
  "finding",
  "trace",
] as const;

const accessVariants = {
  read: "blue",
  execute: "orange",
  write: "red",
} as const;
```

组件签名固定为：

```typescript
import type { McpToolDefinition } from "@repo/schemas";

export type McpAvailableToolsListProps = {
  tools: McpToolDefinition[];
};
```

每个 module 一个 `<section>`；每个 Tool 展示 `title`、等宽字体的 `name`、`description`、access Badge、是否需要确认。不要在组件里复制 `McpToolCatalog`，数据必须来自 props。

- [ ] **Step 3：实现查询容器**

`McpAvailableToolsTab.tsx` 的完整状态分支：

```typescript
import { useList } from "@refinedev/core";
import { useTranslation } from "react-i18next";
import type { McpToolDefinition } from "@repo/schemas";
import { ErrorState } from "@/components/ui/error-state";
import { LoadingState } from "@/components/ui/loading-state";
import { ResourceName } from "@/integrations/refine/dataProvider";
import { McpAvailableToolsList } from "../McpAvailableToolsList";

export type McpAvailableToolsTabProps = { connectionId: string };

export const McpAvailableToolsTab = function({
  connectionId,
}: McpAvailableToolsTabProps) {
  const { t } = useTranslation();
  const { query, result } = useList<McpToolDefinition>({
    resource: ResourceName.mcpAvailableTools,
    filters: [{
      field: "connectionId",
      operator: "eq",
      value: connectionId,
    }],
    pagination: { currentPage: 1, pageSize: 50 },
  });

  if (query.isLoading) {
    return <LoadingState message={t("mcp.availableTools.loading")} />;
  }
  if (query.isError) {
    return <ErrorState message={t("mcp.availableTools.loadError")} />;
  }

  return <McpAvailableToolsList tools={result?.data ?? []} />;
};
```

- [ ] **Step 4：写容器状态测试**

在 `McpAvailableToolsTab.test.tsx` 中 mock `useList`，至少分别返回 loading、error、success 三种结果，并断言对应 i18n key 或 Tool name 出现在静态 HTML 中。

- [ ] **Step 5：写 Storybook**

`McpAvailableToolsList.stories.tsx` 至少导出：

```typescript
export const FullCatalog: Story = {
  args: { tools: [...McpToolCatalog] },
};
export const WorkspaceProjectRepository: Story = {
  args: {
    tools: McpToolCatalog.filter((tool) =>
      ["workspace", "project", "repository"].includes(tool.module),
    ),
  },
};
export const MetadataReadOnly: Story = {
  args: {
    tools: McpToolCatalog.filter((tool) =>
      ["crate", "archetype", "anatomy", "dictionary", "rule", "scan_profile"]
        .includes(tool.module),
    ),
  },
};
```

- [ ] **Step 6：桶导出只做 re-export**

两个 `index.ts` 分别只写：

```typescript
export * from "./McpAvailableToolsList";
```

```typescript
export * from "./McpAvailableToolsTab";
```

- [ ] **Step 7：运行组件测试**

```powershell
Set-Location apps/app
bun run test src/pages/AiReviewsSettingsPage/McpAvailableToolsList/McpAvailableToolsList.test.tsx src/pages/AiReviewsSettingsPage/McpAvailableToolsTab/McpAvailableToolsTab.test.tsx
bun run check-types
Set-Location ../..
```

- [ ] **Step 8：提交本小节**

```powershell
git add apps/app/src/pages/AiReviewsSettingsPage/McpAvailableToolsList apps/app/src/pages/AiReviewsSettingsPage/McpAvailableToolsTab
git commit -m "feat(COD-306): show available mcp tools"
```

---
## Task 10.5：实现 Invocation History 表格与分页
### 文件
- 新建 `McpInvocationHistoryTable/` 组件单元
- 新建 `McpInvocationHistoryTab/` 组件单元

- [ ] **Step 1：写表格展示测试（Red）**

测试数据必须同时包含 success 和 denied/error。断言 Tool name、outcome、duration、errorCode 都能展示，但不存在输入正文、Token 或代码内容列。

- [ ] **Step 2：实现纯表格**

组件 props：

```typescript
import type { McpToolInvocation } from "@repo/schemas";

export type McpInvocationHistoryTableProps = {
  invocations: McpToolInvocation[];
  locale: string;
};
```

表头固定为：时间、Tool、Module、Access、Outcome、Duration、Summary/Error。Badge 映射固定为：

```typescript
const outcomeVariants = {
  success: "green",
  denied: "orange",
  error: "red",
} as const;
```

最后一列显示规则：成功显示 `resultSummary ?? "—"`；失败显示 `errorCode` 和已经脱敏的 `errorMessage`。不要增加展开完整输入/输出的按钮。

- [ ] **Step 3：实现查询和分页容器**

固定页大小：

```typescript
const PAGE_SIZE = 20;
```

容器必须使用：

```typescript
const { query, result } = useList<McpToolInvocation>({
  resource: ResourceName.mcpToolInvocations,
  filters: [{
    field: "connectionId",
    operator: "eq",
    value: connectionId,
  }],
  pagination: { currentPage, pageSize: PAGE_SIZE },
});
```

状态顺序固定：

```typescript
const rows = result?.data ?? [];
const total = result?.total ?? 0;

if (query.isLoading) return <LoadingState />;
if (query.isError) return <ErrorState />;
if (rows.length === 0) return <EmptyState />;
```

分页使用项目 `Button`，不要写原生 `<button>`：

```typescript
const canPrevious = currentPage > 1;
const canNext = currentPage * PAGE_SIZE < total;
```

“上一页”执行 `setCurrentPage((page) => Math.max(1, page - 1))`；“下一页”执行 `setCurrentPage((page) => page + 1)`。

- [ ] **Step 4：写容器测试**

mock `useList`，分别覆盖：Loading、Error、Empty、Success。Success 必须断言记录出现，并确认 `useList` 收到了 `connectionId` filter 与 `{ currentPage: 1, pageSize: 20 }`。

- [ ] **Step 5：写 Storybook**

纯表格 Story 至少导出：`SuccessList`、`DeniedAndError`。容器的 Loading/Error/Empty 由单元测试证明，不在 Storybook 中伪造 Refine Provider。

- [ ] **Step 6：验证并提交**

```powershell
Set-Location apps/app
bun run test src/pages/AiReviewsSettingsPage/McpInvocationHistoryTable/McpInvocationHistoryTable.test.tsx src/pages/AiReviewsSettingsPage/McpInvocationHistoryTab/McpInvocationHistoryTab.test.tsx
bun run check-types
Set-Location ../..
git add apps/app/src/pages/AiReviewsSettingsPage/McpInvocationHistoryTable apps/app/src/pages/AiReviewsSettingsPage/McpInvocationHistoryTab
git commit -m "feat(COD-306): show mcp invocation history"
```

---
## Task 10.6：把三个 Tab 组合进连接详情 Dialog
### 文件
- 修改 `McpConnectionDetailsDialog.tsx`
- 修改对应测试和 Story

- [ ] **Step 1：先更新 Dialog 测试（Red）**

在测试里 mock 两个查询容器，避免静态渲染依赖 Refine Provider：

```typescript
vi.mock("../McpAvailableToolsTab", () => ({
  McpAvailableToolsTab: ({ connectionId }: { connectionId: string }) =>
    <div>available-tools:{connectionId}</div>,
}));
vi.mock("../McpInvocationHistoryTab", () => ({
  McpInvocationHistoryTab: ({ connectionId }: { connectionId: string }) =>
    <div>invocation-history:{connectionId}</div>,
}));
```

断言 HTML 包含三个 Tab key：

```typescript
expect(markup).toContain("mcp.detailsDialog.tabs.overview");
expect(markup).toContain("mcp.detailsDialog.tabs.availableTools");
expect(markup).toContain("mcp.detailsDialog.tabs.invocationHistory");
```

- [ ] **Step 2：用现有 Tabs 组合**

增加导入：

```typescript
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/Tabs";
import { McpAvailableToolsTab } from "../McpAvailableToolsTab";
import { McpInvocationHistoryTab } from "../McpInvocationHistoryTab";
```

Dialog 内容结构以本文附录 C 的完整文件为准：Overview 保留原有详情、失败原因、Setup Guide 和 recheck Button；另外两个 TabsContent 只各放一个查询容器。

不要把分组、分页或数据表逻辑写进 Dialog。

- [ ] **Step 3：更新 Story**

给 `McpConnectionDetailsDialog.stories.tsx` 添加 Refine decorator，或者只在 Dialog Story 中 mock DataProvider。DataProvider 对 `mcpAvailableTools` 返回 `McpToolCatalog`，对 `mcpToolInvocations` 返回静态记录。Story 必须能切换三个 Tab 且不请求真实后端。

- [ ] **Step 4：验证并提交**

```powershell
Set-Location apps/app
bun run test src/pages/AiReviewsSettingsPage/McpConnectionDetailsDialog/McpConnectionDetailsDialog.test.tsx
bun run check-types
Set-Location ../..
git add apps/app/src/pages/AiReviewsSettingsPage/McpConnectionDetailsDialog
git commit -m "feat(COD-306): compose mcp connection detail tabs"
```

---
## Task 10.7：修正 Consent 与 Setup 的过期安全文案
### 文件
- 修改中英文 locale
- 新建 `apps/app/src/integrations/i18n/mcp-translations.test.ts`
- 修改三个使用方

- [ ] **Step 1：先写 key 对齐测试（Red）**

```typescript
import { describe, expect, it } from "vitest";
import en from "./locales/en.json";
import zh from "./locales/zh.json";

describe("MCP translations", () => {
  it("keeps the new review tool security keys aligned", () => {
    expect(en.mcp.consentPage.accessReviewTools).toBeTruthy();
    expect(zh.mcp.consentPage.accessReviewTools).toBeTruthy();
    expect(en.mcp.setupPage.securityReviewTools).toBeTruthy();
    expect(zh.mcp.setupPage.securityReviewTools).toBeTruthy();
    expect(en.mcp.setupOverview.securityReviewTools).toBeTruthy();
    expect(zh.mcp.setupOverview.securityReviewTools).toBeTruthy();
  });
});
```

- [ ] **Step 2：替换旧 key 和文案**

中文：

```json
"accessReviewTools": "此连接可在绑定的工作空间内使用审查读取工具；执行扫描或修改 Finding 前必须再次获得你的明确确认。",
"securityReviewTools": "连接仅开放已列出的 Read、Execute 和 Write 审查工具。Team Admin、Metadata Write、Harness、GitHub Delivery、Pull Request 和代码写入仍不开放。"
```

英文：

```json
"accessReviewTools": "This connection can use review read tools inside its bound Workspace. Starting scans or changing Findings requires your explicit confirmation.",
"securityReviewTools": "Only the listed Read, Execute, and Write review tools are exposed. Team Admin, Metadata Write, Harness, GitHub Delivery, Pull Requests, and code writes remain unavailable."
```

替换引用：

```tsx
t("mcp.consentPage.accessReviewTools")
t("mcp.setupPage.securityReviewTools")
t("mcp.setupOverview.securityReviewTools")
```

删除旧 `accessNoTools` / `securityNoTools` key，避免以后误用。

- [ ] **Step 3：补充新页面所需 key**

中英文必须同时增加：Tab 标题、module 名称、access 名称、确认状态、History 表头、Loading/Error/Empty、上一页/下一页。新增后用测试或脚本比较 `mcp` 节点键结构。

- [ ] **Step 4：验证并提交**

```powershell
Set-Location apps/app
bun run test src/integrations/i18n/mcp-translations.test.ts
bun run check-types
bun run lint
Set-Location ../..
git add apps/app/src/integrations/i18n apps/app/src/pages/McpConsentPage apps/app/src/pages/McpSetupPage apps/app/src/routes/mcp/setup.tsx
git commit -m "fix(COD-306): describe exposed mcp review tools"
```

---
## Task 10.8：最终前端验收
- [ ] **Step 1：运行 Task 10 定向测试**

```powershell
Set-Location apps/app
bun run test src/integrations/trpc/routers/mcp-connections.test.ts src/integrations/refine/dataProvider.test.ts src/integrations/i18n/mcp-translations.test.ts src/pages/AiReviewsSettingsPage/McpAvailableToolsList/McpAvailableToolsList.test.tsx src/pages/AiReviewsSettingsPage/McpAvailableToolsTab/McpAvailableToolsTab.test.tsx src/pages/AiReviewsSettingsPage/McpInvocationHistoryTable/McpInvocationHistoryTable.test.tsx src/pages/AiReviewsSettingsPage/McpInvocationHistoryTab/McpInvocationHistoryTab.test.tsx src/pages/AiReviewsSettingsPage/McpConnectionDetailsDialog/McpConnectionDetailsDialog.test.tsx
```

预期：全部 PASS。

- [ ] **Step 2：运行 App 质量检查和 Storybook 构建**

```powershell
bun run check-types
bun run lint
bun run test
bun run build-storybook
Set-Location ../..
```

预期：退出码全部为 0。若全量测试出现既有的 5 秒 Storybook 动态导入超时，先单独重跑失败文件；不要未经确认修改无关组件。

- [ ] **Step 3：人工检查 UI**

```powershell
Set-Location apps/app
bun run dev
```

浏览器检查：

1. 打开 Settings → AI Reviews → MCP。
2. 打开一个 Connection 详情。
3. Overview 原内容完整。
4. Available Tools 正确分组，Metadata 全是 Read。
5. Execute/Write 有醒目 Badge 和确认提示。
6. Invocation History 能显示成功、拒绝、错误和分页。
7. 窄窗口下表格可横向滚动，Dialog 不超出屏幕。

- [ ] **Step 4：检查变更边界**

```powershell
git status --short
git diff --check
git diff --name-only
```

预期：没有 Task 11 E2E 文件、没有 GitHub Delivery/PR/code write 实现、没有 `docs/COD-306` 被暂存。

---
## Task 10 完成标准
- [ ] 其他用户的 Connection ID 返回 `NOT_FOUND`，Invocation DAO 不执行。
- [ ] 两个 UI 查询都经过 Refine DataProvider。
- [ ] Tool Catalog 按 module 展示，权限和确认要求清晰。
- [ ] Invocation History 只显示 Task 9 已脱敏字段。
- [ ] Dialog 只组合子组件，没有数据表或分组算法。
- [ ] AC-04、AC-08 有测试和 Storybook 证据。
- [ ] Consent/Setup 不再声称“没有业务工具”。
- [ ] Task 10 的提交中没有本地计划文档。

---
## 新手排错表
| 现象 | 最可能原因 | 处理方式 |
|---|---|---|
| `useList` 返回空数组 | filter 字段写成 `id` 而不是 `connectionId` | 对照 DataProvider 的 `getFilterValue(params, "connectionId")` |
| 第 2 页重复第 1 页 | offset 直接使用了 `currentPage` | 改成 `(currentPage - 1) * pageSize` |
| 能看到别人的调用记录 | Router 先调用了 DAO | 把 `requireOwnedConnection` 移到 DAO 之前 |
| Dialog 单测报 Refine Provider 缺失 | 测试没有 mock 两个 Tab 容器 | 按 Task 10.6 Step 1 mock |
| Storybook 请求真实接口 | Story 使用了容器组件 | Story 优先展示纯 List/Table；Dialog Story 使用静态 DataProvider |
| Metadata 出现 Write Badge | UI 自己改写了 accessLevel | 只展示服务端 `McpToolCatalog` 返回值，不在前端推断 |
| i18n 显示 key 本身 | 中英文少了同名 key | 运行 `mcp-translations.test.ts` 并核对路径 |

---
## 附录 A：`McpAvailableToolsList.tsx` 完整参考实现
```typescript
import { useTranslation } from "react-i18next";
import type { McpToolDefinition } from "@repo/schemas";
import { Badge, type BadgeVariant } from "@/components/ui/badge";

const moduleOrder: readonly McpToolDefinition["module"][] = [
  "workspace",
  "project",
  "repository",
  "crate",
  "archetype",
  "anatomy",
  "dictionary",
  "rule",
  "scan_profile",
  "scan",
  "run",
  "finding",
  "trace",
];

const accessVariants: Record<
  McpToolDefinition["accessLevel"],
  BadgeVariant
> = {
  read: "blue",
  execute: "orange",
  write: "red",
};

export type McpAvailableToolsListProps = {
  tools: McpToolDefinition[];
};

export const McpAvailableToolsList = function({
  tools,
}: McpAvailableToolsListProps) {
  const { t } = useTranslation();
  const groups = moduleOrder
    .map((module) => ({
      module,
      tools: tools.filter((tool) => tool.module === module),
    }))
    .filter((group) => group.tools.length > 0);

  return (
    <div className="space-y-4">
      {groups.map((group) => (
        <section
          key={group.module}
          aria-labelledby={`mcp-tool-module-${group.module}`}
          className="rounded-xl border border-border"
        >
          <h3
            className="border-b border-border px-4 py-3 text-sm font-semibold"
            id={`mcp-tool-module-${group.module}`}
          >
            {t(`mcp.availableTools.modules.${group.module}`)}
          </h3>
          <ul className="divide-y divide-border">
            {group.tools.map((tool) => (
              <li className="space-y-2 px-4 py-3" key={tool.name}>
                <div className="flex flex-wrap items-center gap-2">
                  <span className="font-medium">{tool.title}</span>
                  <Badge variant={accessVariants[tool.accessLevel]}>
                    {t(`mcp.availableTools.access.${tool.accessLevel}`)}
                  </Badge>
                  <Badge variant={tool.requiresConfirmation ? "orange" : "default"}>
                    {t(
                      tool.requiresConfirmation
                        ? "mcp.availableTools.confirmation.required"
                        : "mcp.availableTools.confirmation.notRequired",
                    )}
                  </Badge>
                </div>
                <code className="text-xs text-muted-foreground">
                  {tool.name}
                </code>
                <p className="text-sm text-muted-foreground">
                  {tool.description}
                </p>
              </li>
            ))}
          </ul>
        </section>
      ))}
    </div>
  );
};
```

---
## 附录 B：Invocation History 两个组件完整参考实现
### `McpInvocationHistoryTable.tsx`
```typescript
import { useTranslation } from "react-i18next";
import type { McpToolInvocation } from "@repo/schemas";
import { Badge, type BadgeVariant } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

const outcomeVariants: Record<McpToolInvocation["outcome"], BadgeVariant> = {
  success: "green",
  denied: "orange",
  error: "red",
};

export type McpInvocationHistoryTableProps = {
  invocations: McpToolInvocation[];
  locale: string;
};

export const McpInvocationHistoryTable = function({
  invocations,
  locale,
}: McpInvocationHistoryTableProps) {
  const { t } = useTranslation();

  return (
    <div className="overflow-x-auto rounded-xl border border-border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>{t("mcp.invocationHistory.columns.createdAt")}</TableHead>
            <TableHead>{t("mcp.invocationHistory.columns.tool")}</TableHead>
            <TableHead>{t("mcp.invocationHistory.columns.module")}</TableHead>
            <TableHead>{t("mcp.invocationHistory.columns.access")}</TableHead>
            <TableHead>{t("mcp.invocationHistory.columns.outcome")}</TableHead>
            <TableHead>{t("mcp.invocationHistory.columns.duration")}</TableHead>
            <TableHead>{t("mcp.invocationHistory.columns.summary")}</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {invocations.map((invocation) => (
            <TableRow key={invocation.id}>
              <TableCell className="whitespace-nowrap">
                {new Intl.DateTimeFormat(locale, {
                  dateStyle: "medium",
                  timeStyle: "medium",
                }).format(invocation.createdAt)}
              </TableCell>
              <TableCell>
                <code className="text-xs">{invocation.toolName}</code>
              </TableCell>
              <TableCell>
                {t(`mcp.availableTools.modules.${invocation.module}`)}
              </TableCell>
              <TableCell>
                {t(`mcp.availableTools.access.${invocation.accessLevel}`)}
              </TableCell>
              <TableCell>
                <Badge variant={outcomeVariants[invocation.outcome]}>
                  {t(`mcp.invocationHistory.outcomes.${invocation.outcome}`)}
                </Badge>
              </TableCell>
              <TableCell className="whitespace-nowrap">
                {t("mcp.invocationHistory.durationMs", {
                  value: invocation.durationMs,
                })}
              </TableCell>
              <TableCell className="max-w-sm break-words">
                {invocation.outcome === "success"
                  ? invocation.resultSummary ?? "—"
                  : [invocation.errorCode, invocation.errorMessage]
                      .filter(Boolean)
                      .join(": ") || "—"}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};
```

### `McpInvocationHistoryTab.tsx`
```typescript
import { useCallback, useState } from "react";
import { useList } from "@refinedev/core";
import { useTranslation } from "react-i18next";
import type { McpToolInvocation } from "@repo/schemas";
import { Button } from "@/components/ui/button";
import { EmptyState } from "@/components/ui/empty-state";
import { ErrorState } from "@/components/ui/error-state";
import { LoadingState } from "@/components/ui/loading-state";
import { ResourceName } from "@/integrations/refine/dataProvider";
import { McpInvocationHistoryTable } from "../McpInvocationHistoryTable";

const PAGE_SIZE = 20;

export type McpInvocationHistoryTabProps = { connectionId: string };

export const McpInvocationHistoryTab = function({
  connectionId,
}: McpInvocationHistoryTabProps) {
  const { t, i18n } = useTranslation();
  const [currentPage, setCurrentPage] = useState(1);
  const { query, result } = useList<McpToolInvocation>({
    resource: ResourceName.mcpToolInvocations,
    filters: [{
      field: "connectionId",
      operator: "eq",
      value: connectionId,
    }],
    pagination: { currentPage, pageSize: PAGE_SIZE },
  });
  const rows = result?.data ?? [];
  const total = result?.total ?? 0;
  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));
  const handlePrevious = useCallback(
    () => setCurrentPage((page) => Math.max(1, page - 1)),
    [],
  );
  const handleNext = useCallback(
    () => setCurrentPage((page) => page + 1),
    [],
  );

  if (query.isLoading) {
    return <LoadingState message={t("mcp.invocationHistory.loading")} />;
  }
  if (query.isError) {
    return <ErrorState message={t("mcp.invocationHistory.loadError")} />;
  }
  if (rows.length === 0) {
    return (
      <EmptyState
        description={t("mcp.invocationHistory.emptyDescription")}
        title={t("mcp.invocationHistory.emptyTitle")}
      />
    );
  }

  return (
    <div className="space-y-3">
      <McpInvocationHistoryTable
        invocations={rows}
        locale={i18n.resolvedLanguage || i18n.language || "en"}
      />
      <div className="flex items-center justify-between">
        <span className="text-xs text-muted-foreground">
          {t("mcp.invocationHistory.page", {
            current: currentPage,
            total: totalPages,
          })}
        </span>
        <div className="flex gap-2">
          <Button
            disabled={currentPage <= 1}
            size="sm"
            type="button"
            variant="outline"
            onClick={handlePrevious}
          >
            {t("mcp.invocationHistory.previous")}
          </Button>
          <Button
            disabled={currentPage >= totalPages}
            size="sm"
            type="button"
            variant="outline"
            onClick={handleNext}
          >
            {t("mcp.invocationHistory.next")}
          </Button>
        </div>
      </div>
    </div>
  );
};
```

---
## 附录 C：`McpConnectionDetailsDialog.tsx` 完整参考实现
```typescript
import { useTranslation } from "react-i18next";
import type { McpConnectionDetail } from "@repo/schemas";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Dialog } from "@/components/ui/dialog";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/Tabs";
import { McpSetupGuide } from "@/pages/McpSetupPage/McpSetupGuide";
import { McpAvailableToolsTab } from "../McpAvailableToolsTab";
import { McpInvocationHistoryTab } from "../McpInvocationHistoryTab";

export type McpConnectionDetailsDialogProps = {
  connection: McpConnectionDetail | null;
  open: boolean;
  isChecking: boolean;
  onClose: () => void;
  onRecheck: () => void;
};

const handleNoop = function(): void {};

const formatDate = function(
  value: Date | null,
  locale: string,
  emptyLabel: string,
): string {
  return value
    ? new Intl.DateTimeFormat(locale, {
        dateStyle: "medium",
        timeStyle: "short",
      }).format(value)
    : emptyLabel;
};

export const McpConnectionDetailsDialog = function({
  connection = null,
  open = false,
  isChecking = false,
  onClose = handleNoop,
  onRecheck = handleNoop,
}: McpConnectionDetailsDialogProps) {
  const { t, i18n } = useTranslation();
  if (!connection) return null;

  const locale = i18n.resolvedLanguage || i18n.language || "en";
  const noActivity = t("mcp.detailsDialog.noActivity");
  const failureReason = connection.failureCode
    ? t(`mcp.failureReasons.${connection.failureCode}`)
    : connection.failureReason;

  return (
    <Dialog
      className="max-w-4xl"
      open={open}
      title={connection.name}
      onClose={onClose}
    >
      <div className="max-h-[75vh] overflow-y-auto pr-1">
        <Tabs defaultValue="overview">
          <TabsList>
            <TabsTrigger value="overview">
              {t("mcp.detailsDialog.tabs.overview")}
            </TabsTrigger>
            <TabsTrigger value="available-tools">
              {t("mcp.detailsDialog.tabs.availableTools")}
            </TabsTrigger>
            <TabsTrigger value="invocation-history">
              {t("mcp.detailsDialog.tabs.invocationHistory")}
            </TabsTrigger>
          </TabsList>

          <TabsContent className="mt-4 space-y-5" value="overview">
            <dl className="grid grid-cols-2 gap-3 rounded-xl border border-border p-4 text-sm">
              <div>
                <dt className="text-muted-foreground">{t("mcp.common.client")}</dt>
                <dd className="font-medium">
                  {t(`mcp.clientTypes.${connection.clientType}`)}
                </dd>
              </div>
              <div>
                <dt className="text-muted-foreground">{t("mcp.common.workspace")}</dt>
                <dd className="font-medium">{connection.workspace.name}</dd>
              </div>
              <div>
                <dt className="text-muted-foreground">{t("mcp.common.status")}</dt>
                <dd>
                  <Badge variant={
                    connection.status === "active"
                      ? "green"
                      : connection.status === "failed"
                        ? "failed"
                        : "default"
                  }>
                    {t(`mcp.statuses.${connection.status}`)}
                  </Badge>
                </dd>
              </div>
              <div>
                <dt className="text-muted-foreground">{t("mcp.detailsDialog.created")}</dt>
                <dd className="font-medium">
                  {formatDate(connection.createdAt, locale, noActivity)}
                </dd>
              </div>
              <div>
                <dt className="text-muted-foreground">{t("mcp.detailsDialog.lastChecked")}</dt>
                <dd className="font-medium">
                  {formatDate(connection.lastCheckedAt, locale, noActivity)}
                </dd>
              </div>
              <div>
                <dt className="text-muted-foreground">{t("mcp.detailsDialog.lastActivity")}</dt>
                <dd className="font-medium">
                  {formatDate(connection.lastActivityAt, locale, noActivity)}
                </dd>
              </div>
            </dl>

            {failureReason && (
              <div className="rounded-xl border border-destructive/30 bg-destructive/5 p-3 text-sm text-destructive">
                {failureReason}
              </div>
            )}

            {connection.status !== "revoked" && (
              <McpSetupGuide setup={connection.setup} />
            )}

            <div className="flex justify-end">
              <Button
                disabled={isChecking || connection.status === "revoked"}
                type="button"
                variant="outline"
                onClick={onRecheck}
              >
                {isChecking
                  ? t("mcp.detailsDialog.checking")
                  : t("mcp.detailsDialog.recheck")}
              </Button>
            </div>
          </TabsContent>

          <TabsContent className="mt-4" value="available-tools">
            <McpAvailableToolsTab connectionId={connection.id} />
          </TabsContent>
          <TabsContent className="mt-4" value="invocation-history">
            <McpInvocationHistoryTab connectionId={connection.id} />
          </TabsContent>
        </Tabs>
      </div>
    </Dialog>
  );
};
```

---
## 附录 D：Task 10 新增 i18n 节点完整清单
把下面中文节点合并到 `zh.json` 的 `mcp` 对象中；不要覆盖已经存在的其他 `mcp` key：

```json
{
  "detailsDialog": {
    "tabs": {
      "overview": "概览",
      "availableTools": "可用工具",
      "invocationHistory": "调用记录"
    }
  },
  "availableTools": {
    "loading": "正在加载可用工具...",
    "loadError": "无法加载可用工具。",
    "access": {
      "read": "读取",
      "execute": "执行",
      "write": "写入"
    },
    "confirmation": {
      "required": "需要确认",
      "notRequired": "无需确认"
    },
    "modules": {
      "workspace": "工作空间",
      "project": "项目",
      "repository": "代码仓库",
      "crate": "Crate",
      "archetype": "Archetype",
      "anatomy": "Anatomy",
      "dictionary": "术语字典",
      "rule": "规则",
      "scan_profile": "扫描配置",
      "scan": "扫描",
      "run": "运行记录",
      "finding": "发现",
      "trace": "执行轨迹"
    }
  },
  "invocationHistory": {
    "loading": "正在加载调用记录...",
    "loadError": "无法加载调用记录。",
    "emptyTitle": "暂无调用记录",
    "emptyDescription": "该连接还没有调用任何 Daedalus MCP 工具。",
    "durationMs": "{{value}} 毫秒",
    "page": "第 {{current}} / {{total}} 页",
    "previous": "上一页",
    "next": "下一页",
    "columns": {
      "createdAt": "时间",
      "tool": "工具",
      "module": "模块",
      "access": "权限",
      "outcome": "结果",
      "duration": "耗时",
      "summary": "摘要 / 错误"
    },
    "outcomes": {
      "success": "成功",
      "denied": "已拒绝",
      "error": "错误"
    }
  }
}
```

英文对应节点：

```json
{
  "detailsDialog": {
    "tabs": {
      "overview": "Overview",
      "availableTools": "Available Tools",
      "invocationHistory": "Invocation History"
    }
  },
  "availableTools": {
    "loading": "Loading available tools...",
    "loadError": "Available tools could not be loaded.",
    "access": {
      "read": "Read",
      "execute": "Execute",
      "write": "Write"
    },
    "confirmation": {
      "required": "Confirmation required",
      "notRequired": "No confirmation required"
    },
    "modules": {
      "workspace": "Workspace",
      "project": "Project",
      "repository": "Repository",
      "crate": "Crate",
      "archetype": "Archetype",
      "anatomy": "Anatomy",
      "dictionary": "Dictionary",
      "rule": "Rule",
      "scan_profile": "Scan Profile",
      "scan": "Scan",
      "run": "Run",
      "finding": "Finding",
      "trace": "Trace"
    }
  },
  "invocationHistory": {
    "loading": "Loading invocation history...",
    "loadError": "Invocation history could not be loaded.",
    "emptyTitle": "No invocation history",
    "emptyDescription": "This connection has not called a Daedalus MCP tool yet.",
    "durationMs": "{{value}} ms",
    "page": "Page {{current}} of {{total}}",
    "previous": "Previous",
    "next": "Next",
    "columns": {
      "createdAt": "Time",
      "tool": "Tool",
      "module": "Module",
      "access": "Access",
      "outcome": "Outcome",
      "duration": "Duration",
      "summary": "Summary / Error"
    },
    "outcomes": {
      "success": "Success",
      "denied": "Denied",
      "error": "Error"
    }
  }
}
```

注意：`detailsDialog`、`consentPage`、`setupPage`、`setupOverview` 已经存在，实际编辑时只把子键合并进去，不能在同一 JSON 对象中创建第二个同名 key。
