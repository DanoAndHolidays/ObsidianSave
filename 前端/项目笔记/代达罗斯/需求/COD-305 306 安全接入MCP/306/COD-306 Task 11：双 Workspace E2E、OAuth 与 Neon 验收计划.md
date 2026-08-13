# COD-306 Task 11：双 Workspace E2E、OAuth 与 Neon 验收计划
> Last Format Time：8/13/2026 15:14:03

> **执行指引：** 推荐使用 `subagent-driven-development` 技能逐任务执行；数据库步骤必须由你本人确认目标环境。
> 步骤使用 checkbox (`- [ ]`) 追踪进度。所有命令默认从 `G:\Save\Grogramming\CodeForge\daedalus` 执行。

**目标：** 用真实 PostgreSQL、真实 MCP JSON-RPC Request/Response 和真实 Connection 授权规则，证明 Connection A 永远不能读取或修改 Workspace B 的审查数据，并完成 Neon Schema 验收。

**架构：** 自动化测试使用本地 PostgreSQL，创建带唯一前缀的 User、两个 Workspace、Connection、Project、Run、Finding 和 Trace；调用 `createDaedalusMcpProtocolHandler` 发送真实 MCP HTTP Request。OAuth 的密码学交换通过最后的浏览器/客户端 smoke test 验证，连接失效逻辑由真实 `createMcpConnectionsService(db).authorizeRequest` 验证。

**技术栈：** Vitest、PostgreSQL 16、Drizzle ORM、MCP JSON-RPC、Better Auth OAuth 2.1、Bun、Neon。

---
## 为什么 Task 11 要分成三层
```mermaid
flowchart TD
  A["自动化：真实 PostgreSQL"] --> B["真实 MCP HTTP Request"]
  B --> C["Workspace 隔离、确认、审计"]
  D["自动化：authorizeRequest"] --> E["Revoked / membership lost"]
  F["人工 Smoke：真实 Codex + 浏览器 OAuth"] --> G["令牌签发与 consent 页面"]
  H["人工确认"] --> I["Neon db:push"]
```

不能只写一个“看起来像 E2E”的 mock 测试：

- Workspace 隔离必须让 SQL 真正在 PostgreSQL 中执行。
- GitHub 文件读取可以 mock 外部 `fetch`，避免依赖网络；但 Repository Service、MCP 协议和数据库必须是真实实现。
- 自动化测试不能使用 Neon，防止测试删除生产/预览数据。
- Neon 只做 Schema push 和只读结构验证，不运行会增删数据的 E2E。

---
## 文件结构
- 新建 `apps/app/src/integrations/mcp/mcp-review-tools.e2e-fixtures.ts`：本地数据库种子和清理。
- 新建 `apps/app/src/integrations/mcp/mcp-review-tools.e2e-client.ts`：MCP JSON-RPC Request/SSE 解析。
- 新建 `apps/app/src/integrations/mcp/mcp-review-tools.e2e.test.ts`：业务验收。
- 修改 `apps/app/package.json`：增加显式 E2E script，避免普通测试误跑。
- 本地更新 COD-306 计划的 AC checkbox，但不加入 Git。

---
## Task 11.0：数据库安全前置检查
- [ ] **Step 1：确认 PostgreSQL 服务**

```powershell
sc.exe query postgresql-x64-16
```

预期：`STATE` 包含 `RUNNING`。

- [ ] **Step 2：显式设置本地 E2E 数据库**

只在当前 PowerShell 窗口设置：

```powershell
$env:DATABASE_URL='postgresql://postgres:123456@localhost:5432/daedalus'
$env:RUN_MCP_E2E='1'
```

禁止把这两行写进受 Git 管理的源码。自动化测试必须拒绝 `neon.tech`、非 localhost host 和非 `daedalus` 数据库。

- [ ] **Step 3：验证连接和目标库**

```powershell
$env:PGPASSWORD='123456'
& 'G:\Installation\Postgre\bin\psql.exe' -h localhost -p 5432 -U postgres -d daedalus -c 'select current_database(), current_user;'
```

预期：数据库为 `daedalus`，用户为 `postgres`。

- [ ] **Step 4：检查 Task 2 表是否已推到本地库**

```powershell
& 'G:\Installation\Postgre\bin\psql.exe' -h localhost -p 5432 -U postgres -d daedalus -c "select to_regclass('public.mcp_tool_invocations');"
```

预期：返回 `mcp_tool_invocations`。若为空，先在本地环境执行：

```powershell
bun run db:push
```

只允许对本地库执行这一步。

---
## Task 11.1：实现安全的 E2E Fixture
### 文件
- 新建 `apps/app/src/integrations/mcp/mcp-review-tools.e2e-fixtures.ts`

- [ ] **Step 1：定义固定返回类型和本地库保护**

文件开头写：

```typescript
import { and, eq, inArray } from "drizzle-orm";
import { db } from "@repo/db";
import {
  auditRecordsTable,
  findingFeedbackTable,
  findingsTable,
  githubProjectsTable,
  mcpConnectionsTable,
  mcpToolInvocationsTable,
  reviewRunsTable,
  rulesTable,
  scanProfilesTable,
  traceEventsTable,
  usersTable,
  workspaceMembershipsTable,
  workspacesTable,
} from "@repo/db-schema";

export type McpReviewE2eFixture = {
  prefix: string;
  userId: string;
  workspaceAId: string;
  workspaceBId: string;
  connectionAId: string;
  projectAId: string;
  projectBId: string;
  ruleAId: string;
  ruleBId: string;
  profileAId: string;
  runAId: string;
  runBId: string;
  failedRunAId: string;
  findingAId: string;
  findingBId: string;
  traceAId: string;
  traceBId: string;
};

export const assertLocalMcpE2eDatabase = function(): void {
  const databaseUrl = process.env.DATABASE_URL;
  if (!databaseUrl) throw new Error("DATABASE_URL is required for MCP E2E");

  const parsed = new URL(databaseUrl);
  const localHost = ["localhost", "127.0.0.1"].includes(parsed.hostname);
  const localDatabase = parsed.pathname === "/daedalus";
  if (!localHost || !localDatabase || parsed.hostname.includes("neon.tech")) {
    throw new Error(
      "MCP E2E is destructive and may only run against localhost/daedalus",
    );
  }
};
```

- [ ] **Step 2：实现种子函数**

使用随机前缀避免碰撞：

```typescript
export const seedMcpReviewE2eFixture = async function(): Promise<
  McpReviewE2eFixture
> {
  assertLocalMcpE2eDatabase();
  const prefix = `cod306-e2e-${crypto.randomUUID()}`;
  const fixture: McpReviewE2eFixture = {
    prefix,
    userId: `${prefix}-user`,
    workspaceAId: `${prefix}-workspace-a`,
    workspaceBId: `${prefix}-workspace-b`,
    connectionAId: `${prefix}-connection-a`,
    projectAId: `${prefix}-project-a`,
    projectBId: `${prefix}-project-b`,
    ruleAId: `${prefix}-rule-a`,
    ruleBId: `${prefix}-rule-b`,
    profileAId: `${prefix}-profile-a`,
    runAId: `${prefix}-run-a`,
    runBId: `${prefix}-run-b`,
    failedRunAId: `${prefix}-run-failed-a`,
    findingAId: `${prefix}-finding-a`,
    findingBId: `${prefix}-finding-b`,
    traceAId: `${prefix}-trace-a`,
    traceBId: `${prefix}-trace-b`,
  };

  await db.insert(usersTable).values({
    id: fixture.userId,
    name: "COD-306 E2E User",
    email: `${prefix}@example.test`,
    emailVerified: true,
  });
  await db.insert(workspacesTable).values([
    {
      id: fixture.workspaceAId,
      name: `${prefix} Workspace A`,
      type: "team",
      monogram: "A",
    },
    {
      id: fixture.workspaceBId,
      name: `${prefix} Workspace B`,
      type: "team",
      monogram: "B",
    },
  ]);
  await db.insert(workspaceMembershipsTable).values([
    {
      id: `${prefix}-membership-a`,
      workspaceId: fixture.workspaceAId,
      userId: fixture.userId,
      role: "owner",
    },
    {
      id: `${prefix}-membership-b`,
      workspaceId: fixture.workspaceBId,
      userId: fixture.userId,
      role: "owner",
    },
  ]);
  await db.insert(mcpConnectionsTable).values({
    id: fixture.connectionAId,
    name: "COD-306 Connection A",
    clientType: "codex",
    ownerUserId: fixture.userId,
    workspaceId: fixture.workspaceAId,
    status: "active",
  });
  await db.insert(githubProjectsTable).values([
    {
      id: fixture.projectAId,
      workspaceId: fixture.workspaceAId,
      owner: "fixture-owner",
      repo: "fixture-repo-a",
      branch: "main",
      url: "https://github.com/fixture-owner/fixture-repo-a",
    },
    {
      id: fixture.projectBId,
      workspaceId: fixture.workspaceBId,
      owner: "fixture-owner",
      repo: "fixture-repo-b",
      branch: "main",
      url: "https://github.com/fixture-owner/fixture-repo-b",
    },
  ]);
  await db.insert(scanProfilesTable).values({
    id: fixture.profileAId,
    name: `${prefix} Profile A`,
    workspaceId: fixture.workspaceAId,
  });
  await db.insert(rulesTable).values([
    {
      id: fixture.ruleAId,
      name: `${prefix} Rule A`,
      category: "bug",
      prompt: "Check Workspace A fixture code.",
      workspaceId: fixture.workspaceAId,
    },
    {
      id: fixture.ruleBId,
      name: `${prefix} Rule B`,
      category: "bug",
      prompt: "Check Workspace B fixture code.",
      workspaceId: fixture.workspaceBId,
    },
  ]);
  await db.insert(reviewRunsTable).values([
    {
      id: fixture.runAId,
      status: "completed",
      scope: "file",
      projectId: fixture.projectAId,
      targetPath: "src/a.ts",
      branch: "main",
      profileId: fixture.profileAId,
      triggeredBy: fixture.userId,
    },
    {
      id: fixture.runBId,
      status: "completed",
      scope: "file",
      projectId: fixture.projectBId,
      targetPath: "src/b.ts",
      branch: "main",
      triggeredBy: fixture.userId,
    },
    {
      id: fixture.failedRunAId,
      status: "failed",
      scope: "directory",
      projectId: fixture.projectAId,
      targetPath: "src",
      branch: "main",
      profileId: fixture.profileAId,
      triggeredBy: fixture.userId,
      contextSnapshot: { source: "cod306-e2e" },
      effectiveSettings: { mode: "strict" },
      reportLanguagePlan: { primary: "zh" },
    },
  ]);
  await db.insert(findingsTable).values([
    {
      id: fixture.findingAId,
      runId: fixture.runAId,
      ruleId: fixture.ruleAId,
      category: "bug",
      severity: "high",
      title: "Workspace A Finding",
      description: "A-only evidence",
      suggestion: "Fix A",
      filePath: "src/a.ts",
      lineStart: 10,
      lineEnd: 12,
      status: "pending",
    },
    {
      id: fixture.findingBId,
      runId: fixture.runBId,
      ruleId: fixture.ruleBId,
      category: "bug",
      severity: "medium",
      title: "Workspace B Finding",
      description: "B-only evidence",
      suggestion: "Fix B",
      filePath: "src/b.ts",
      lineStart: 20,
      lineEnd: 22,
      status: "pending",
    },
  ]);
  await db.insert(traceEventsTable).values([
    {
      id: fixture.traceAId,
      runId: fixture.runAId,
      type: "status",
      name: "workspace-a-progress",
      content: { message: "safe-a" },
      rawContentRef: `${prefix}-raw-a-do-not-return`,
      retentionRuleId: "cod306-e2e",
      policyVersion: "1",
    },
    {
      id: fixture.traceBId,
      runId: fixture.runBId,
      type: "status",
      name: "workspace-b-progress",
      content: { message: "safe-b" },
      rawContentRef: `${prefix}-raw-b-do-not-return`,
      retentionRuleId: "cod306-e2e",
      policyVersion: "1",
    },
  ]);

  return fixture;
};
```

- [ ] **Step 3：实现严格按外键顺序清理**

```typescript
export const cleanupMcpReviewE2eFixture = async function(
  fixture: McpReviewE2eFixture,
): Promise<void> {
  assertLocalMcpE2eDatabase();
  const runIds = [
    fixture.runAId,
    fixture.runBId,
    fixture.failedRunAId,
  ];

  const createdRuns = await db
    .select({ id: reviewRunsTable.id })
    .from(reviewRunsTable)
    .where(eq(reviewRunsTable.triggeredBy, fixture.userId));
  const allRunIds = [...new Set([
    ...runIds,
    ...createdRuns.map((row) => row.id),
  ])];

  await db.delete(mcpToolInvocationsTable).where(
    eq(mcpToolInvocationsTable.connectionId, fixture.connectionAId),
  );
  await db.delete(auditRecordsTable).where(
    inArray(auditRecordsTable.runId, allRunIds),
  );
  await db.delete(findingFeedbackTable).where(
    inArray(findingFeedbackTable.runId, allRunIds),
  );
  await db.delete(traceEventsTable).where(
    inArray(traceEventsTable.runId, allRunIds),
  );
  await db.delete(findingsTable).where(
    inArray(findingsTable.runId, allRunIds),
  );
  await db.delete(reviewRunsTable).where(
    inArray(reviewRunsTable.id, allRunIds),
  );
  await db.delete(scanProfilesTable).where(
    eq(scanProfilesTable.id, fixture.profileAId),
  );
  await db.delete(rulesTable).where(
    inArray(rulesTable.id, [fixture.ruleAId, fixture.ruleBId]),
  );
  await db.delete(githubProjectsTable).where(
    inArray(githubProjectsTable.id, [fixture.projectAId, fixture.projectBId]),
  );
  await db.delete(mcpConnectionsTable).where(
    eq(mcpConnectionsTable.id, fixture.connectionAId),
  );
  await db.delete(workspaceMembershipsTable).where(
    and(
      eq(workspaceMembershipsTable.userId, fixture.userId),
      inArray(workspaceMembershipsTable.workspaceId, [
        fixture.workspaceAId,
        fixture.workspaceBId,
      ]),
    ),
  );
  await db.delete(workspacesTable).where(
    inArray(workspacesTable.id, [fixture.workspaceAId, fixture.workspaceBId]),
  );
  await db.delete(usersTable).where(eq(usersTable.id, fixture.userId));
};
```

不要写“删除所有测试数据”这种宽泛 SQL；所有 delete 必须绑定本次 fixture ID。

---
## Task 11.2：实现 MCP HTTP 测试客户端
### 文件
- 新建 `apps/app/src/integrations/mcp/mcp-review-tools.e2e-client.ts`

- [ ] **Step 1：写 JSON-RPC/SSE helper**

```typescript
import type { McpAuthorizationContext } from "@repo/services";
import { createDaedalusMcpProtocolHandler } from "./mcp-protocol-handler";

type RpcPayload = {
  result?: {
    tools?: Array<{ name: string }>;
    structuredContent?: McpToolEnvelope;
  };
  error?: { code: number; message: string };
};

export type McpToolEnvelope = {
  success: boolean;
  workspace: { id: string; name: string | null };
  tool: string;
  result: unknown;
  nextActions: string[];
  error: null | {
    code: string;
    message: string;
    recovery: string | null;
  };
};

const parseMcpResponse = async function(response: Response): Promise<RpcPayload> {
  const body = await response.text();
  const dataLine = body
    .split("\n")
    .find((line) => line.startsWith("data: "));

  return JSON.parse(dataLine?.slice(6) ?? body) as RpcPayload;
};

export const createMcpE2eClient = function(
  authorization: McpAuthorizationContext,
) {
  const handler = createDaedalusMcpProtocolHandler(authorization);
  let requestId = 0;

  const send = async function(method: string, params: object = {}) {
    requestId += 1;
    const response = await handler(new Request(
      `http://localhost/api/mcp?connectionId=${authorization.connectionId}`,
      {
        method: "POST",
        headers: {
          Accept: "application/json, text/event-stream",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          jsonrpc: "2.0",
          id: requestId,
          method,
          params,
        }),
      },
    ));

    if (response.status !== 200) {
      throw new Error(`MCP HTTP request failed with ${response.status}`);
    }

    return parseMcpResponse(response);
  };

  return {
    listTools: async () => {
      const payload = await send("tools/list");

      return payload.result?.tools ?? [];
    },
    callTool: async (name: string, arguments_: Record<string, unknown>) => {
      const payload = await send("tools/call", {
        name,
        arguments: arguments_,
      });
      const envelope = payload.result?.structuredContent;
      if (!envelope) throw new Error(`Missing structuredContent for ${name}`);

      return envelope;
    },
  };
};
```

- [ ] **Step 2：类型检查**

```powershell
Set-Location apps/app
bun run check-types
Set-Location ../..
```

预期：PASS。不要用 `as any` 绕过 MCP envelope。

---
## Task 11.3：写双 Workspace 自动化验收
### 文件
- 新建 `apps/app/src/integrations/mcp/mcp-review-tools.e2e.test.ts`
- 修改 `apps/app/package.json`

- [ ] **Step 1：增加显式 script**

在 `apps/app/package.json` scripts 中增加：

```json
"test:mcp-e2e": "vitest run src/integrations/mcp/mcp-review-tools.e2e.test.ts"
```

- [ ] **Step 2：建立测试生命周期**

```typescript
import { afterAll, beforeAll, describe, expect, it, vi } from "vitest";
import { eq } from "drizzle-orm";
import { db } from "@repo/db";
import {
  findingFeedbackTable,
  findingsTable,
  mcpConnectionsTable,
  mcpToolInvocationsTable,
  reviewRunsTable,
  workspaceMembershipsTable,
} from "@repo/db-schema";
import { createMcpConnectionsService } from "@repo/services";
import { McpToolCatalog } from "@repo/schemas";
import {
  cleanupMcpReviewE2eFixture,
  seedMcpReviewE2eFixture,
  type McpReviewE2eFixture,
} from "./mcp-review-tools.e2e-fixtures";
import { createMcpE2eClient } from "./mcp-review-tools.e2e-client";

vi.mock("@/integrations/trpc/routers/github-token", async () => {
  const { okAsync } = await import("neverthrow");

  return {
    resolveGitHubTokenResult: vi.fn(() => okAsync("e2e-github-token")),
  };
});

const runE2e = process.env.RUN_MCP_E2E === "1";
const describeE2e = runE2e ? describe : describe.skip;

describeE2e("COD-306 MCP review tools E2E", () => {
  let fixture: McpReviewE2eFixture;
  let client: ReturnType<typeof createMcpE2eClient>;

  beforeAll(async () => {
    fixture = await seedMcpReviewE2eFixture();
    client = createMcpE2eClient({
      connectionId: fixture.connectionAId,
      ownerUserId: fixture.userId,
      workspaceId: fixture.workspaceAId,
      clientType: "codex",
    });
  });

  afterAll(async () => {
    if (fixture) await cleanupMcpReviewE2eFixture(fixture);
    vi.unstubAllGlobals();
  });
```

测试文件最后要补齐 `});`。

- [ ] **Step 3：验证 Tool 目录和未开放能力**

```typescript
it("lists exactly the approved catalog without delivery or code write tools", async () => {
  const tools = await client.listTools();
  const names = tools.map((tool) => tool.name).sort();

  expect(names).toEqual(McpToolCatalog.map((tool) => tool.name).sort());
  expect(names).not.toEqual(expect.arrayContaining([
    "finding_deliver_to_github",
    "pull_request_create",
    "repository_write_file",
    "rule_update",
    "crate_create",
    "trace_get_raw_content",
    "team_admin_update",
    "harness_run",
  ]));
});
```

- [ ] **Step 4：验证 Project/Run/Finding 越权**

```typescript
it("keeps Project, Run, and Finding reads inside Workspace A", async () => {
  const list = await client.callTool("project_list", { limit: 20, offset: 0 });
  expect(list.success).toBe(true);
  expect(JSON.stringify(list.result)).toContain(fixture.projectAId);
  expect(JSON.stringify(list.result)).not.toContain(fixture.projectBId);

  for (const [tool, arguments_] of [
    ["project_get", { id: fixture.projectBId }],
    ["run_get", { runId: fixture.runBId }],
    ["finding_get", { findingId: fixture.findingBId }],
  ] as const) {
    const response = await client.callTool(tool, arguments_);
    expect(response.success).toBe(false);
    expect(response.error?.code).toBe("not_found");
    expect(response.workspace.id).toBe(fixture.workspaceAId);
    expect(JSON.stringify(response)).not.toContain("Workspace B Finding");
  }
});
```

再追加一条 Workspace A 正常 Finding 证据断言：

```typescript
it("returns Workspace A Finding rule and source location", async () => {
  const response = await client.callTool("finding_get", {
    findingId: fixture.findingAId,
  });

  expect(response.success).toBe(true);
  expect(response.result).toMatchObject({
    id: fixture.findingAId,
    ruleId: fixture.ruleAId,
    filePath: "src/a.ts",
    lineStart: 10,
    lineEnd: 12,
  });
  expect(JSON.stringify(response.result)).not.toContain(
    "export const a = true",
  );
});
```

- [ ] **Step 5：验证 Repository 文件读取但 mock 外部 GitHub**

```typescript
it("returns bounded repository content for Project A", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(
    JSON.stringify({
      type: "file",
      name: "a.ts",
      path: "src/a.ts",
      sha: "fixture-sha",
      size: 24,
      encoding: "base64",
      content: Buffer.from("export const a = true;\n").toString("base64"),
    }),
    { status: 200, headers: { "Content-Type": "application/json" } },
  )));

  const response = await client.callTool("repository_read_file", {
    projectId: fixture.projectAId,
    branch: "main",
    path: "src/a.ts",
  });

  expect(response.success).toBe(true);
  expect(response.result).toMatchObject({
    projectId: fixture.projectAId,
    repository: "fixture-owner/fixture-repo-a",
    branch: "main",
    path: "src/a.ts",
    content: "export const a = true;\n",
    truncated: false,
  });
});
```

- [ ] **Step 6：验证确认规则和副作用**

```typescript
it("requires confirmation before scans and Finding writes", async () => {
  const runsBefore = await db
    .select({ id: reviewRunsTable.id })
    .from(reviewRunsTable)
    .where(eq(reviewRunsTable.triggeredBy, fixture.userId));

  const deniedScan = await client.callTool("scan_start", {
    projectId: fixture.projectAId,
    scope: "file",
    targetPath: "src/a.ts",
    branch: "main",
    profileId: fixture.profileAId,
    confirmed: false,
  });
  expect(deniedScan.error?.code).toBe("confirmation_required");

  const runsAfterDenied = await db
    .select({ id: reviewRunsTable.id })
    .from(reviewRunsTable)
    .where(eq(reviewRunsTable.triggeredBy, fixture.userId));
  expect(runsAfterDenied).toHaveLength(runsBefore.length);

  const acceptedScan = await client.callTool("scan_start", {
    projectId: fixture.projectAId,
    scope: "file",
    targetPath: "src/a.ts",
    branch: "main",
    profileId: fixture.profileAId,
    confirmed: true,
    confirmationSummary: "E2E user confirmed Project A file scan.",
  });
  expect(acceptedScan.success).toBe(true);
  expect(acceptedScan.result).toMatchObject({ status: "pending" });

  const deniedFinding = await client.callTool("finding_update_status", {
    findingId: fixture.findingAId,
    status: "confirmed",
    confirmed: false,
  });
  expect(deniedFinding.error?.code).toBe("confirmation_required");
  const unchanged = await db
    .select({ status: findingsTable.status })
    .from(findingsTable)
    .where(eq(findingsTable.id, fixture.findingAId));
  expect(unchanged[0]?.status).toBe("pending");

  const updated = await client.callTool("finding_update_status", {
    findingId: fixture.findingAId,
    status: "confirmed",
    confirmed: true,
    confirmationSummary: "E2E user confirmed the Finding status change.",
  });
  expect(updated.result).toMatchObject({
    findingId: fixture.findingAId,
    before: { status: "pending" },
    after: { status: "confirmed" },
  });
});
```

- [ ] **Step 7：验证 Trace、Retry 和 Feedback**

```typescript
it("returns filtered Trace, creates retry, and attributes feedback", async () => {
  const trace = await client.callTool("trace_list_latest", {
    runId: fixture.runAId,
  });
  const serializedTrace = JSON.stringify(trace.result);
  expect(serializedTrace).toContain("safe-a");
  expect(serializedTrace).not.toContain("rawContentRef");
  expect(serializedTrace).not.toContain("raw-a-do-not-return");

  const retry = await client.callTool("run_retry", {
    runId: fixture.failedRunAId,
    confirmed: true,
    confirmationSummary: "E2E user confirmed retry.",
  });
  expect(retry.result).toMatchObject({
    status: "pending",
    retryOf: fixture.failedRunAId,
  });

  const feedback = await client.callTool("finding_add_feedback", {
    findingId: fixture.findingAId,
    outcome: "accepted",
    note: "Confirmed by E2E",
    confirmed: true,
    confirmationSummary: "E2E user confirmed feedback submission.",
  });
  expect(feedback.success).toBe(true);

  const rows = await db
    .select()
    .from(findingFeedbackTable)
    .where(eq(findingFeedbackTable.findingId, fixture.findingAId));
  expect(rows[0]?.createdBy).toBe(fixture.userId);
});
```

- [ ] **Step 8：验证每次调用有脱敏审计**

```typescript
it("stores bounded invocation records without repository content", async () => {
  const rows = await db
    .select()
    .from(mcpToolInvocationsTable)
    .where(eq(mcpToolInvocationsTable.connectionId, fixture.connectionAId));

  expect(rows.length).toBeGreaterThan(0);
  expect(rows.some((row) => row.outcome === "success")).toBe(true);
  expect(rows.some((row) => row.outcome === "denied")).toBe(true);
  for (const row of rows) {
    expect(row.resultSummary?.length ?? 0).toBeLessThanOrEqual(500);
    const serialized = JSON.stringify(row);
    expect(serialized).not.toContain("e2e-github-token");
    expect(serialized).not.toContain("export const a = true");
  }
});
```

---
## Task 11.4：验证 Connection 失效发生在业务逻辑之前
- [ ] **Step 1：使用真实 Connection Service 测试 revoked**

把这条测试放在 E2E 文件最后，避免影响前面的 Tool 调用：

```typescript
it("rejects revoked and membership-lost connections before tool execution", async () => {
  const connectionsService = createMcpConnectionsService(db);

  await db
    .update(mcpConnectionsTable)
    .set({ status: "revoked", revokedAt: new Date() })
    .where(eq(mcpConnectionsTable.id, fixture.connectionAId));
  const revoked = await connectionsService.authorizeRequest({
    connectionId: fixture.connectionAId,
    subjectUserId: fixture.userId,
    oauthClientId: `${fixture.prefix}-oauth-client`,
  });
  expect(revoked.isErr()).toBe(true);
  expect(revoked._unsafeUnwrapErr().type).toBe("revoked");

  await db
    .update(mcpConnectionsTable)
    .set({ status: "active", revokedAt: null })
    .where(eq(mcpConnectionsTable.id, fixture.connectionAId));
  await db
    .delete(workspaceMembershipsTable)
    .where(eq(
      workspaceMembershipsTable.id,
      `${fixture.prefix}-membership-a`,
    ));

  const membershipLost = await connectionsService.authorizeRequest({
    connectionId: fixture.connectionAId,
    subjectUserId: fixture.userId,
    oauthClientId: `${fixture.prefix}-oauth-client`,
  });
  expect(membershipLost.isErr()).toBe(true);
  expect(membershipLost._unsafeUnwrapErr().type).toBe("forbidden");
});
```

这里不调用 `createDaedalusMcpProtocolHandler`，因为授权上下文本来就应该在创建 Protocol Handler 之前生成。该测试证明失败发生在 Tool Registry 和业务 DAO 之前。

---
## Task 11.5：运行自动化 E2E
- [ ] **Step 1：先确认环境变量仍指向本地库**

```powershell
$database = [System.Uri]$env:DATABASE_URL
$database.Host
$database.AbsolutePath
```

预期：`localhost` 和 `/daedalus`。不是这两个值就停止。

- [ ] **Step 2：运行 E2E**

```powershell
Set-Location apps/app
bun run test:mcp-e2e
Set-Location ../..
```

预期：所有测试 PASS。若测试失败，`afterAll` 应清理本次 fixture；仍需运行下面的残留检查。

- [ ] **Step 3：检查没有残留**

```powershell
$env:PGPASSWORD='123456'
& 'G:\Installation\Postgre\bin\psql.exe' -h localhost -p 5432 -U postgres -d daedalus -c "select count(*) from users where email like 'cod306-e2e-%@example.test';"
```

预期：`0`。如果不是 0，不要写无条件 delete；先查询具体 prefix，再按该 prefix 精确删除。

- [ ] **Step 4：提交 E2E 代码**

```powershell
git add apps/app/package.json apps/app/src/integrations/mcp/mcp-review-tools.e2e-client.ts apps/app/src/integrations/mcp/mcp-review-tools.e2e-fixtures.ts apps/app/src/integrations/mcp/mcp-review-tools.e2e.test.ts
git commit -m "test(COD-306): cover workspace scoped mcp workflows"
```

---
## Task 11.6：运行全仓质量检查
- [ ] **Step 1：普通测试必须保持 E2E skip**

新开一个 PowerShell，或执行：

```powershell
Remove-Item Env:RUN_MCP_E2E -ErrorAction SilentlyContinue
```

然后运行：

```powershell
bun run quality
bun run build
bun run knip
```

预期：全部退出码为 0，E2E 文件显示 skipped 而不是连接数据库。

- [ ] **Step 2：处理既有偶发超时**

如果只有 Anatomy Story 动态导入测试在全量并发下超过 5 秒，先单独运行失败文件确认；不要把 Task 11 扩展成无关页面重构。若连续三次全量测试都失败，再单独建问题处理。

---
## Task 11.7：真实 OAuth 客户端 Smoke Test
这一步验证自动化测试没有覆盖的浏览器 OAuth/Consent 交换。

- [ ] **Step 1：启动 App**

```powershell
Set-Location apps/app
bun run dev
```

预期：Vite 在 `http://localhost:9431` 启动。

- [ ] **Step 2：在 UI 创建 Connection A**

1. 登录 Daedalus。
2. 打开 Settings → AI Reviews → MCP。
3. 选择 Workspace A，创建 Codex Connection。
4. 复制 UI 生成的 Codex 命令，不要手工复制 access token、cookie 或 client secret。

- [ ] **Step 3：在 Codex 配置 MCP**

使用 UI 给出的命令。若需要手工验证 URL，先读取 Connection ID：

```powershell
$connectionId = Read-Host '请输入 UI 中显示的 Connection A ID'
codex mcp add daedalus --url "http://localhost:9431/api/mcp?connectionId=$connectionId"
```

仍以 UI 实际生成的命令为准。

- [ ] **Step 4：完成浏览器授权并检查 Consent**

Consent 页面必须明确显示：

- 连接绑定的 Workspace。
- Read Tool 可以读取审查上下文。
- Execute/Write 需要明确确认。
- Team Admin、Metadata Write、Harness、GitHub Delivery、PR、code write 不开放。

- [ ] **Step 5：用自然语言完成最小 Smoke**

向 Coding Agent 依次要求：

1. “列出当前 Daedalus Workspace 和项目。”
2. “读取 Project A 的 `src/a.ts`。”
3. “准备扫描 Project A，但先不要执行。”
4. 确认范围后再执行 `scan_start`。
5. 查询返回的 Run 和最新 Trace。

检查 Daedalus Connection Details 的 Invocation History 出现对应调用。

- [ ] **Step 6：撤销连接后重试**

在 Settings 撤销 Connection A，再让 Agent 调用 `project_list`。预期：OAuth/连接层拒绝，不能进入业务 Tool。

不要为了“测试拒绝”去修改 Workspace B 数据。

---
## Task 11.8：推送并验证 Neon Schema

> 这是外部数据库写操作。执行前必须人工确认环境、查看 Drizzle 变更摘要；若出现 DROP/TRUNCATE/重建现有表，立即取消。

- [ ] **Step 1：清除本地 E2E 环境变量并切换 `.env` 到 Neon**

```powershell
Remove-Item Env:RUN_MCP_E2E -ErrorAction SilentlyContinue
Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue
```

编辑 `apps/app/.env`，只启用 Neon `DATABASE_URL`。不要在终端输出完整连接字符串，不要把 `.env` 加入 Git。

- [ ] **Step 2：再次确认不是本地库**

人工查看 `.env` 中启用行的 host 应包含 `neon.tech`。只确认 host，不复制密码到聊天、Issue 或日志。

- [ ] **Step 3：执行 Schema push**

```powershell
Set-Location apps/app
bun run db:push
Set-Location ../..
```

预期：Drizzle 只新增或确认 `mcp_tool_invocations` 表、外键和索引。遇到破坏性变更提示时选择取消，先检查 schema 差异。

- [ ] **Step 4：在 Neon SQL Editor 只读验证**

```sql
select table_name
from information_schema.tables
where table_schema = 'public'
  and table_name = 'mcp_tool_invocations';

select indexname
from pg_indexes
where schemaname = 'public'
  and tablename = 'mcp_tool_invocations'
order by indexname;
```

预期至少看到：

- `mcp_tool_invocations_connection_created_idx`
- `mcp_tool_invocations_workspace_created_idx`
- 主键索引

- [ ] **Step 5：确认仓库没有环境文件改动**

```powershell
git status --short
```

预期：没有 `.env`、Obsidian 文档或 `docs/COD-306` 被暂存。

---
## Task 11.9：16 条 AC 最终证据表
| AC | 自动化/人工证据 | 通过条件 |
|---|---|---|
| AC-01 | E2E `project_list` | 只有 Project A |
| AC-02 | E2E `repository_read_file` | 返回 repo/path/content，外部 fetch 可控 |
| AC-03 | E2E `project_get(Project B)` | 泛化 `not_found` |
| AC-04 | Task 10 Storybook | Tool 按 module 展示 |
| AC-05 | Task 6 单测 + tools/list | 治理读取 Tool 存在 |
| AC-06 | Task 6 单测 | 关系数据可追踪 |
| AC-07 | E2E tools/list | 无 Metadata Write |
| AC-08 | Task 10 Storybook | Metadata Badge 全 Read |
| AC-09 | E2E confirmed scan | 返回 pending Run ID |
| AC-10 | E2E run/trace | 可轮询状态和 Trace |
| AC-11 | E2E run_retry | 新 Run 带 retryOf |
| AC-12 | E2E unconfirmed scan | 不新增 Run |
| AC-13 | E2E finding_get | Rule ID/文件/行号可见，不含整文件 |
| AC-14 | E2E finding_update_status | 返回 before/after |
| AC-15 | E2E finding_add_feedback | createdBy 为 Connection owner |
| AC-16 | E2E tools/list + OAuth smoke | 无 Delivery/PR/code write |

所有行都有证据后，才把 COD-306 标记完成。

---
## Task 11 完成标准
- [ ] E2E 只能在 localhost/daedalus 运行。
- [ ] Fixture 成功和失败时都能按 ID 清理。
- [ ] MCP Request 真正经过 Protocol Handler、Tool Registry、Service、DAO、PostgreSQL。
- [ ] 跨 Workspace 的 Project/Run/Finding 均为泛化拒绝。
- [ ] 未确认操作无副作用，已确认操作有 before/after 和 invocation audit。
- [ ] Trace 不返回 `rawContentRef`。
- [ ] revoked/membership lost 在业务 Tool 前失败。
- [ ] 真实 Codex OAuth smoke 通过。
- [ ] Neon 只有预期 Schema 变化。
- [ ] `quality`、`build`、`knip` 通过。
- [ ] 代码已提交，本地计划和 Obsidian 文档未提交。

---
## 新手最容易犯的危险错误
1. 把 Neon URL 放进 `DATABASE_URL` 后运行 E2E。测试必须主动拒绝。
2. 清理时按 `email like '%e2e%'` 批量删除。只能按本次 fixture ID 删除。
3. 为了测试 Repository 直接请求真实 GitHub。自动化中 mock 外部 fetch，避免限流和私有仓库泄露。
4. 把 `confirmed: true` 当成充分确认。还必须传非空 `confirmationSummary`。
5. 只检查 Tool 返回错误，不检查数据库副作用。拒绝场景必须查询 Run/Finding 数量或状态。
6. 用 Protocol Handler 直接测试 revoked。Revoked 应在创建 Authorization Context 之前由 Connection Service 拦截。
7. 在 Neon 运行测试数据 seed。Neon 只做 Schema push 和只读结构检查。
8. 把 OAuth token、Neon 密码或 `.env` 内容粘贴到测试日志或文档。
