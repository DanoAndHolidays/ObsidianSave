# CrateCodeSnippetsPanel

---
## code
```ts
import { useCallback, useMemo, useState } from "react";
import {
  useCreate,
  useCustomMutation,
  useDelete,
  useList,
  useUpdate,
  type BaseRecord,
  type HttpError,
} from "@refinedev/core";
import type {
  CrateCodeSnippet,
  CrateCodeSnippetCreateInput,
  CrateCodeSnippetFormValues,
  CrateCodeSnippetReorderInput,
  CrateCodeSnippetUpdateInput,
} from "@repo/schemas";
import { ArrowDown, ArrowUp, Code2, Pencil, Plus, Trash2, ChevronDown, ChevronRight } from "lucide-react";
import { useTranslation } from "react-i18next";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { ErrorState } from "@/components/ui/error-state";
import { LoadingState } from "@/components/ui/loading-state";
import {
  DataProviderCustomAction,
  ResourceName,
} from "@/integrations/refine/dataProvider";
import { CrateCodeSnippetDialog } from "@/components/CrateCodeSnippetDialog";
import { DeleteCrateCodeSnippetDialog } from "@/components/DeleteCrateCodeSnippetDialog";
import { moveCrateCodeSnippet } from "./moveCrateCodeSnippet";

// 这上面的不看了
export type CrateCodeSnippetsPanelProps = {
  crateId: string;
};

export const CrateCodeSnippetsPanel = function ({
  crateId,
}: CrateCodeSnippetsPanelProps) {
  const { t } = useTranslation();
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingSnippet, setEditingSnippet] =
    useState<CrateCodeSnippet | null>(null);
  const [deletingSnippet, setDeletingSnippet] =
    useState<CrateCodeSnippet | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);
  const [expandedSnippetIds, setExpandedSnippetIds] = useState<ReadonlySet<string>>(new Set<string>());

  const { result, query } = useList<CrateCodeSnippet>({
    resource: ResourceName.crateCodeSnippets,
    filters: [{ field: "crateId", operator: "eq", value: crateId }],
    pagination: { currentPage: 1, pageSize: 0 },
    queryOptions: { enabled: crateId.length > 0 },
  });
  
  const snippets = useMemo(
    () => (result?.data ?? []) as CrateCodeSnippet[],
    [result?.data],
  );

  // 这里是Refine的使用，和useList、useOne很像的
  const createMutation = useCreate<
    CrateCodeSnippet,
    HttpError,
    CrateCodeSnippetCreateInput
    >();
  
  
  const updateMutation = useUpdate<
    CrateCodeSnippet,
    HttpError,
    CrateCodeSnippetUpdateInput
    >();
  
  
  const deleteMutation = useDelete<CrateCodeSnippet>();


  const reorderMutation = useCustomMutation<
    BaseRecord,
    HttpError,
    CrateCodeSnippetReorderInput
  >();

  const handleAdd = useCallback(() => {
    setActionError(null);
    setEditingSnippet(null);
    setDialogOpen(true);
  }, []);

  const handleEdit = useCallback((snippet: CrateCodeSnippet) => {
    setActionError(null);
    setEditingSnippet(snippet);
    setDialogOpen(true);
  }, []);

  const handleCloseDialog = useCallback(() => {
    setDialogOpen(false);
    setEditingSnippet(null);
    setActionError(null);
  }, []);

  const handleSubmit = useCallback(
    (values: CrateCodeSnippetFormValues) => {
      setActionError(null);

      if (editingSnippet) {
        updateMutation.mutate(
          {
            resource: ResourceName.crateCodeSnippets,
            id: editingSnippet.id,
            values,
          },
          {
            onSuccess: handleCloseDialog,
            onError: (error) => setActionError(error.message),
          },
        );

        return;
      }

      createMutation.mutate(
        {
          resource: ResourceName.crateCodeSnippets,
          values: {
            id: crypto.randomUUID(),
            crateId,
            ...values,
            sortOrder: snippets.length,
          },
        },
        {
          onSuccess: handleCloseDialog,
          onError: (error) => setActionError(error.message),
        },
      );
    },
    [
      crateId,
      createMutation,
      editingSnippet,
      handleCloseDialog,
      snippets.length,
      updateMutation,
    ],
  );

  const handleDelete = useCallback(() => {
    if (!deletingSnippet) return;
    setActionError(null);
    deleteMutation.mutate(
      {
        resource: ResourceName.crateCodeSnippets,
        id: deletingSnippet.id,
      },
      {
        onSuccess: () => setDeletingSnippet(null),
        onError: (error) => setActionError(error.message),
      },
    );
  }, [deleteMutation, deletingSnippet]);

  const handleMove = useCallback(
    (index: number, direction: -1 | 1) => {
      const reordered = moveCrateCodeSnippet(snippets, index, direction);
      if (reordered === snippets) return;
      setActionError(null);

      reorderMutation.mutate(
        {
          url: DataProviderCustomAction.reorderCrateCodeSnippets,
          method: "post",
          values: {
            crateId,
            snippetIds: reordered.map((snippet) => snippet.id),
          },
        },
        {
          onSuccess: () => {
            void query.refetch();
          },
          onError: (error) => setActionError(error.message),
        },
      );
    },
    [crateId, query, reorderMutation, snippets],
  );

  const handleRetry = useCallback(() => {
    void query.refetch();
  }, [query]);

  const handleOpenDelete = useCallback((snippet: CrateCodeSnippet) => {
    setActionError(null);
    setDeletingSnippet(snippet);
  }, []);

  const handleCancelDelete = useCallback(() => {
    setDeletingSnippet(null);
  }, []);

  const handleToggleExpand = useCallback((snippetId: string) => {
    setExpandedSnippetIds((current) => {
      const next = new Set<string>(current)

      if (next.has(snippetId)) {
        next.delete(snippetId);
      } else {
        next.add(snippetId);
      }

      return next
    })
  }, [])

  const isSaving =
    createMutation.mutation.isPending || updateMutation.mutation.isPending;
  const isReordering = reorderMutation.mutation.isPending;

  return (
    <section aria-labelledby="crate-code-snippets-heading" className="space-y-3">
      <div className="rounded-[10px] border border-[#ececef] dark:border-border bg-card px-[17px] py-4">
        {/* <div className="text-[13px] font-semibold mb-[3px]">{t("crateDetail.linkedPaths", "Linked Paths")}</div> */}
        <div className="flex items-center justify-between gap-3">
          <div>
            <h2 className="text-[13px] font-semibold" id="crate-code-snippets-heading">
              {t("crateDetail.codeSnippets")}
            </h2>
            <p className="mt-1 text-xs text-muted-foreground">
              {t("crateDetail.codeSnippetsDescription")}
            </p>
          </div>
          <Button size="sm" type="button" variant="outline" onClick={handleAdd}>
            <Plus aria-hidden="true" className="size-4" />
            {t("crateDetail.addSnippet")}
          </Button>
        </div>

        {actionError && (
          <p className="text-sm text-destructive" role="alert">
            {actionError}
          </p>
        )}

        {query.isLoading ? (
          <LoadingState className="py-10" />
        ) : query.isError ? (
          <ErrorState
            action={
              <Button type="button" variant="outline" onClick={handleRetry}>
                {t("common.retry")}
              </Button>
            }
            className="py-10"
            message={query.error.message}
            title={t("crateDetail.snippetsLoadError")}
          />
        ) : snippets.length === 0 ? (
          <EmptyState
            action={
              <Button size="sm" type="button" onClick={handleAdd}>
                {t("crateDetail.addSnippet")}
              </Button>
            }
            className="py-10"
            description={t("crateDetail.noSnippetsDescription")}
            icon={<Code2 aria-hidden="true" className="size-7" />}
            title={t("crateDetail.noSnippets")}
          />
        ) : (
          <div className="space-y-3 mt-4">
            {snippets.map((snippet, index) => {
              const isExpanded = expandedSnippetIds.has(snippet.id);
              // const codeRegionId = `crate-code-snippet-${snippet.id}-code`;

              return (
                <Card key={snippet.id}>
                  <CardHeader className="gap-3">
                    <div className="min-w-0">
                      <div className="flex items-center gap-2">
                        <h3 className="truncate text-sm font-semibold">{snippet.name}</h3>
                        <Badge>{snippet.language}</Badge>
                      </div>
                      {snippet.description && (
                        <p className="mt-1 text-xs text-muted-foreground">
                          {snippet.description}
                        </p>
                      )}
                    </div>
                    <div className="flex shrink-0 items-center gap-1">
                      <Button
                        aria-label={t("crateDetail.moveSnippetUp", { name: snippet.name })}
                        className="size-8 p-0"
                        disabled={index === 0 || isReordering}
                        size="sm"
                        type="button"
                        variant="ghost"
                        onClick={() => handleMove(index, -1)}
                      >
                        <ArrowUp aria-hidden="true" className="size-4" />
                      </Button>
                      <Button
                        aria-label={t("crateDetail.moveSnippetDown", { name: snippet.name })}
                        className="size-8 p-0"
                        disabled={index === snippets.length - 1 || isReordering}
                        size="sm"
                        type="button"
                        variant="ghost"
                        onClick={() => handleMove(index, 1)}
                      >
                        <ArrowDown aria-hidden="true" className="size-4" />
                      </Button>
                      <Button
                        aria-label={t("crateDetail.editSnippetNamed", { name: snippet.name })}
                        className="size-8 p-0"
                        size="sm"
                        type="button"
                        variant="ghost"
                        onClick={() => handleEdit(snippet)}
                      >
                        <Pencil aria-hidden="true" className="size-4" />
                      </Button>
                      <Button
                        aria-label={t("crateDetail.deleteSnippetNamed", { name: snippet.name })}
                        className="size-8 p-0"
                        size="sm"
                        type="button"
                        variant="ghost"
                        onClick={() => handleOpenDelete(snippet)}
                      >
                        <Trash2 aria-hidden="true" className="size-4" />
                      </Button>
                      <Button
                        aria-label={t("crateDetail.deleteSnippetNamed", { name: snippet.name })}
                        className="size-8 p-0"
                        size="sm"
                        type="button"
                        variant="ghost"
                        onClick={() => handleToggleExpand(snippet.id)}
                      >
                        {isExpanded ? (<ChevronDown aria-hidden="true" className="size-4" />) : (<ChevronRight aria-hidden="true" className="size-4" />)}
                      </Button>
                    </div>
                  </CardHeader>
                  {isExpanded && (
                    <CardContent>
                      <pre className="max-h-80 overflow-auto rounded-lg bg-muted p-4 text-xs leading-relaxed">
                        <code className="font-mono">{snippet.code}</code>
                      </pre>
                    </CardContent>
                  )}
                </Card>
              )
            }
            )}
          </div>
        )}

        <CrateCodeSnippetDialog
          initialData={editingSnippet}
          isSubmitting={isSaving}
          open={dialogOpen}
          serverError={actionError}
          onClose={handleCloseDialog}
          onSubmit={handleSubmit}
        />
        <DeleteCrateCodeSnippetDialog
          isDeleting={deleteMutation.mutation.isPending}
          snippet={deletingSnippet}
          onCancel={handleCancelDelete}
          onConfirm={handleDelete}
        />
      </div>
    </section>
  );
};

```

---
## 解析

这个 `CrateCodeSnippetsPanel` 是上一段 `CrateCodeSnippetDialog` 的**父组件和业务容器组件**。

上一段 Dialog 主要负责：

```text
展示表单
收集输入
执行 Zod 校验
把合法数据交给父组件
```

而这个父组件主要负责：

```text
从后端获取代码片段
控制新增/编辑弹窗
调用新增、修改、删除、排序接口
展示列表状态
控制代码展开收起
把状态和回调传给 Dialog
```

整体关系可以理解为：

```text
CrateCodeSnippetsPanel
├── 获取代码片段列表
├── 管理新增、编辑、删除、排序
├── 展示代码片段卡片
├── CrateCodeSnippetDialog
│   └── 新增/编辑表单
└── DeleteCrateCodeSnippetDialog
    └── 删除确认弹窗
```

---

# 一、组件接收的参数

```ts
export type CrateCodeSnippetsPanelProps = {
  crateId: string;
};
```

这个组件只接收一个 `crateId`。

```tsx
export const CrateCodeSnippetsPanel = function ({
  crateId,
}: CrateCodeSnippetsPanelProps) {
```

这里的含义是：

> 当前面板展示的是哪个 Crate 下面的代码片段。

后面查询、创建和排序时，都会用到这个 `crateId`。

例如：

```text
Crate A
├── snippet 1
├── snippet 2
└── snippet 3

Crate B
├── snippet 4
└── snippet 5
```

传入不同的 `crateId`，组件就会加载不同的代码片段。

---

# 二、组件管理的状态

```ts
const [dialogOpen, setDialogOpen] = useState(false);

const [editingSnippet, setEditingSnippet] =
  useState<CrateCodeSnippet | null>(null);

const [deletingSnippet, setDeletingSnippet] =
  useState<CrateCodeSnippet | null>(null);

const [actionError, setActionError] =
  useState<string | null>(null);

const [expandedSnippetIds, setExpandedSnippetIds] =
  useState<ReadonlySet<string>>(new Set<string>());
```

父组件一共管理了五类状态。

---

## 1. `dialogOpen`

```ts
const [dialogOpen, setDialogOpen] = useState(false);
```

控制新增/编辑 Dialog 是否打开。

```text
false → 弹窗关闭
true  → 弹窗打开
```

最终传给子组件：

```tsx
<CrateCodeSnippetDialog open={dialogOpen} />
```

---

## 2. `editingSnippet`

```ts
const [editingSnippet, setEditingSnippet] =
  useState<CrateCodeSnippet | null>(null);
```

表示当前正在编辑哪个代码片段。

新增时：

```ts
editingSnippet === null
```

编辑时：

```ts
editingSnippet === 某个代码片段对象
```

因此，这个状态不仅保存编辑数据，也承担了判断新增还是编辑的作用：

```ts
if (editingSnippet) {
  // 修改
} else {
  // 新增
}
```

它最终作为上一段 Dialog 的 `initialData`：

```tsx
<CrateCodeSnippetDialog
  initialData={editingSnippet}
/>
```

所以：

```text
editingSnippet = null
→ Dialog 显示空表单
→ 新增模式

editingSnippet = snippet
→ Dialog 填充已有数据
→ 编辑模式
```

---

## 3. `deletingSnippet`

```ts
const [deletingSnippet, setDeletingSnippet] =
  useState<CrateCodeSnippet | null>(null);
```

表示当前准备删除哪个代码片段。

```text
null
→ 删除确认弹窗关闭

某个 snippet
→ 删除确认弹窗打开
```

它被传给：

```tsx
<DeleteCrateCodeSnippetDialog
  snippet={deletingSnippet}
/>
```

这里和编辑弹窗的设计略有不同：

* 编辑弹窗使用单独的 `dialogOpen`
* 删除弹窗直接根据 `deletingSnippet` 是否为空判断是否打开

---

## 4. `actionError`

```ts
const [actionError, setActionError] =
  useState<string | null>(null);
```

用于保存新增、修改、删除、排序等操作产生的错误。

例如：

```ts
onError: (error) => setActionError(error.message)
```

页面中会统一展示：

```tsx
{actionError && (
  <p className="text-sm text-destructive" role="alert">
    {actionError}
  </p>
)}
```

它也会传给新增/编辑 Dialog：

```tsx
serverError={actionError}
```

所以这个状态目前同时承担：

```text
列表区域操作错误
表单提交错误
删除操作错误
排序操作错误
```

---

## 5. `expandedSnippetIds`

```ts
const [expandedSnippetIds, setExpandedSnippetIds] =
  useState<ReadonlySet<string>>(new Set<string>());
```

这个集合保存所有已展开代码片段的 ID。

例如：

```ts
new Set([
  "snippet-1",
  "snippet-3",
])
```

表示：

```text
snippet-1 已展开
snippet-2 未展开
snippet-3 已展开
```

使用 `Set` 的好处是检查某个 ID 是否存在很方便：

```ts
expandedSnippetIds.has(snippet.id)
```

---

# 三、获取代码片段列表

```ts
const { result, query } = useList<CrateCodeSnippet>({
  resource: ResourceName.crateCodeSnippets,
  filters: [{ field: "crateId", operator: "eq", value: crateId }],
  pagination: { currentPage: 1, pageSize: 0 },
  queryOptions: { enabled: crateId.length > 0 },
});
```

这里使用 Refine 的 `useList` 获取列表数据。

---

## `resource`

```ts
resource: ResourceName.crateCodeSnippets
```

告诉 Refine：

> 我要操作的是 `crateCodeSnippets` 资源。

它最终会通过项目的 `dataProvider` 发起请求。

可以大致理解为：

```text
useList
  ↓
dataProvider.getList
  ↓
GET /crate-code-snippets
```

具体 URL 取决于项目的 `dataProvider` 实现。

---

## `filters`

```ts
filters: [
  {
    field: "crateId",
    operator: "eq",
    value: crateId,
  },
]
```

表示筛选：

```text
crateId 等于当前传入的 crateId
```

可以近似理解成：

```sql
SELECT *
FROM crate_code_snippets
WHERE crate_id = ?
```

所以这个面板只显示当前 Crate 的代码片段。

---

## `pagination`

```ts
pagination: {
  currentPage: 1,
  pageSize: 0,
}
```

从代码意图看，它希望获取当前 Crate 下的全部代码片段。

不过 `pageSize: 0` 的具体行为，要看当前 Refine 版本和项目 `dataProvider` 的约定。有些实现可能把 `0` 当成“不分页”，有些实现可能需要使用其他配置。

---

## `queryOptions.enabled`

```ts
queryOptions: {
  enabled: crateId.length > 0,
}
```

只有 `crateId` 不为空时才发起查询。

```text
crateId = ""
→ 不请求

crateId = "crate-123"
→ 发起请求
```

这样可以避免出现无效请求：

```text
GET /crate-code-snippets?crateId=
```

---

# 四、处理查询结果

```ts
const snippets = useMemo(
  () => (result?.data ?? []) as CrateCodeSnippet[],
  [result?.data],
);
```

`result?.data` 是 Refine 返回的列表数据。

如果查询还没完成，它可能是 `undefined`，所以使用：

```ts
result?.data ?? []
```

确保 `snippets` 始终是数组。

结果可能是：

```ts
const snippets = [
  {
    id: "1",
    name: "React Context",
    language: "tsx",
    code: "...",
  },
  {
    id: "2",
    name: "CSS Grid",
    language: "css",
    code: "...",
  },
];
```

这里的 `useMemo` 不是非常必要，因为只是：

```ts
result?.data ?? []
```

计算成本很低。

它主要能保证：

> 当 `result.data` 没变化时，`snippets` 尽量保持相同引用。

不过是否真的需要，要结合子组件优化和后续依赖来看。

---

# 五、创建四种 Mutation

这个组件需要执行：

```text
新增
修改
删除
排序
```

因此创建了四个 Mutation。

---

## 1. 新增 Mutation

```ts
const createMutation = useCreate<
  CrateCodeSnippet,
  HttpError,
  CrateCodeSnippetCreateInput
>();
```

泛型分别描述：

```text
CrateCodeSnippet
→ 创建成功后返回的数据类型

HttpError
→ 失败时的错误类型

CrateCodeSnippetCreateInput
→ 创建接口接收的数据类型
```

---

## 2. 修改 Mutation

```ts
const updateMutation = useUpdate<
  CrateCodeSnippet,
  HttpError,
  CrateCodeSnippetUpdateInput
>();
```

用于修改已有代码片段。

---

## 3. 删除 Mutation

```ts
const deleteMutation = useDelete<CrateCodeSnippet>();
```

用于根据 ID 删除代码片段。

---

## 4. 排序 Mutation

```ts
const reorderMutation = useCustomMutation<
  BaseRecord,
  HttpError,
  CrateCodeSnippetReorderInput
>();
```

排序不是普通的单条增删改查，而是一个自定义接口，所以使用：

```ts
useCustomMutation
```

这四个 Mutation 分别负责对应的接口操作。

---

# 六、打开新增弹窗

```ts
const handleAdd = useCallback(() => {
  setActionError(null);
  setEditingSnippet(null);
  setDialogOpen(true);
}, []);
```

点击“添加代码片段”时执行。

执行顺序是：

```ts
setActionError(null);
```

清除上一次操作留下的错误。

```ts
setEditingSnippet(null);
```

明确进入新增模式。

```ts
setDialogOpen(true);
```

打开 Dialog。

最终状态：

```text
editingSnippet = null
dialogOpen = true
```

子组件接收到：

```tsx
<CrateCodeSnippetDialog
  initialData={null}
  open={true}
/>
```

于是展示空表单。

---

# 七、打开编辑弹窗

```ts
const handleEdit = useCallback((snippet: CrateCodeSnippet) => {
  setActionError(null);
  setEditingSnippet(snippet);
  setDialogOpen(true);
}, []);
```

点击某个代码片段的编辑按钮时执行。

比如点击：

```ts
{
  id: "snippet-1",
  name: "React Context",
  language: "tsx",
  code: "...",
}
```

执行：

```ts
setEditingSnippet(snippet);
```

最终子组件收到：

```tsx
<CrateCodeSnippetDialog
  initialData={snippet}
  open={true}
/>
```

上一段 Dialog 内部的：

```ts
getDefaultValues(initialData)
```

就会把这个代码片段的数据放到输入框中。

---

# 八、关闭新增/编辑弹窗

```ts
const handleCloseDialog = useCallback(() => {
  setDialogOpen(false);
  setEditingSnippet(null);
  setActionError(null);
}, []);
```

关闭时会同时清理三个状态。

```ts
setDialogOpen(false);
```

关闭弹窗。

```ts
setEditingSnippet(null);
```

清除正在编辑的数据。

```ts
setActionError(null);
```

清除错误信息。

这样下次打开弹窗时，不会残留上一次编辑对象或错误。

---

# 九、最核心的 `handleSubmit`

```ts
const handleSubmit = useCallback(
  (values: CrateCodeSnippetFormValues) => {
    setActionError(null);

    if (editingSnippet) {
      // 修改
      return;
    }

    // 新增
  },
  [...]
);
```

这个函数接收上一段 Dialog 校验完成后的表单数据。

比如：

```ts
values = {
  name: "useContext 示例",
  language: "tsx",
  code: "const value = useContext(Context);",
  description: "演示 React Context",
};
```

然后根据：

```ts
editingSnippet
```

判断是新增还是修改。

---

## 修改流程

```ts
if (editingSnippet) {
  updateMutation.mutate(
    {
      resource: ResourceName.crateCodeSnippets,
      id: editingSnippet.id,
      values,
    },
    {
      onSuccess: handleCloseDialog,
      onError: (error) => setActionError(error.message),
    },
  );

  return;
}
```

关键判断：

```ts
if (editingSnippet)
```

如果当前有正在编辑的数据，就调用修改接口。

发送的数据包括：

```ts
{
  resource: ResourceName.crateCodeSnippets,
  id: editingSnippet.id,
  values,
}
```

例如：

```ts
{
  resource: "crateCodeSnippets",
  id: "snippet-123",
  values: {
    name: "修改后的名称",
    language: "tsx",
    code: "...",
    description: "...",
  },
}
```

成功后：

```ts
onSuccess: handleCloseDialog
```

关闭弹窗并清理状态。

失败后：

```ts
onError: (error) => setActionError(error.message)
```

保存错误，传给 Dialog 展示。

---

## 为什么修改时不需要传 `crateId`

修改接口已经知道：

```ts
id: editingSnippet.id
```

通常可以直接根据代码片段 ID 找到对应记录。

并且表单只允许修改：

```text
name
language
code
description
```

所以这里直接传 `values`。

---

## 新增流程

如果：

```ts
editingSnippet === null
```

就执行：

```ts
createMutation.mutate(
  {
    resource: ResourceName.crateCodeSnippets,
    values: {
      id: crypto.randomUUID(),
      crateId,
      ...values,
      sortOrder: snippets.length,
    },
  },
  {
    onSuccess: handleCloseDialog,
    onError: (error) => setActionError(error.message),
  },
);
```

新增数据由几部分组成：

```ts
{
  id: crypto.randomUUID(),
  crateId,
  ...values,
  sortOrder: snippets.length,
}
```

---

### `crypto.randomUUID()`

```ts
id: crypto.randomUUID()
```

在前端生成一个 UUID，例如：

```text
8c7f8502-5a3e-4aac-9583-d3d4be29e875
```

用作代码片段 ID。

---

### `crateId`

```ts
crateId
```

说明新代码片段属于当前 Crate。

---

### `...values`

```ts
...values
```

把表单数据展开：

```ts
{
  name,
  language,
  code,
  description,
}
```

---

### `sortOrder`

```ts
sortOrder: snippets.length
```

新创建的数据被放到当前列表末尾。

如果已有三个元素：

```text
索引 0
索引 1
索引 2
```

那么新元素：

```ts
sortOrder = 3
```

---

# 十、`handleSubmit` 的依赖数组

```ts
[
  crateId,
  createMutation,
  editingSnippet,
  handleCloseDialog,
  snippets.length,
  updateMutation,
]
```

因为回调函数内部使用了这些外部变量，所以它们出现在 `useCallback` 依赖数组中。

特别注意：

```ts
snippets.length
```

这里函数只需要当前列表长度，不需要整个 `snippets` 数组，所以依赖长度即可。

---

# 十一、删除流程

## 打开删除确认弹窗

```ts
const handleOpenDelete = useCallback((snippet: CrateCodeSnippet) => {
  setActionError(null);
  setDeletingSnippet(snippet);
}, []);
```

点击删除按钮时：

```ts
setDeletingSnippet(snippet)
```

删除 Dialog 收到非空的 `snippet`，于是打开。

---

## 取消删除

```ts
const handleCancelDelete = useCallback(() => {
  setDeletingSnippet(null);
}, []);
```

把删除对象清空，确认弹窗关闭。

---

## 确认删除

```ts
const handleDelete = useCallback(() => {
  if (!deletingSnippet) return;

  setActionError(null);

  deleteMutation.mutate(
    {
      resource: ResourceName.crateCodeSnippets,
      id: deletingSnippet.id,
    },
    {
      onSuccess: () => setDeletingSnippet(null),
      onError: (error) => setActionError(error.message),
    },
  );
}, [deleteMutation, deletingSnippet]);
```

首先进行保护判断：

```ts
if (!deletingSnippet) return;
```

因为没有删除目标时，无法知道要删除哪个 ID。

然后调用：

```ts
deleteMutation.mutate({
  resource: ResourceName.crateCodeSnippets,
  id: deletingSnippet.id,
});
```

成功后：

```ts
setDeletingSnippet(null)
```

关闭删除确认弹窗。

失败后：

```ts
setActionError(error.message)
```

展示错误。

---

# 十二、移动和重新排序

```ts
const handleMove = useCallback(
  (index: number, direction: -1 | 1) => {
    const reordered = moveCrateCodeSnippet(
      snippets,
      index,
      direction,
    );

    if (reordered === snippets) return;

    setActionError(null);

    reorderMutation.mutate(...);
  },
  [crateId, query, reorderMutation, snippets],
);
```

参数：

```ts
index
```

表示当前代码片段的位置。

```ts
direction: -1 | 1
```

只允许两个值：

```text
-1 → 向上移动
 1 → 向下移动
```

---

## 本地计算新顺序

```ts
const reordered = moveCrateCodeSnippet(
  snippets,
  index,
  direction,
);
```

假设列表是：

```text
A
B
C
```

执行：

```ts
handleMove(1, -1)
```

就是将 B 向上移动：

```text
B
A
C
```

---

## 为什么判断引用相等

```ts
if (reordered === snippets) return;
```

`moveCrateCodeSnippet` 很可能在不能移动时，直接返回原数组。

例如：

```text
第一个元素继续向上
最后一个元素继续向下
```

如果返回的还是原数组，就说明顺序没有变化，不需要调用后端。

---

## 向后端发送新的 ID 顺序

```ts
reorderMutation.mutate({
  url: DataProviderCustomAction.reorderCrateCodeSnippets,
  method: "post",
  values: {
    crateId,
    snippetIds: reordered.map((snippet) => snippet.id),
  },
});
```

假设排序后：

```ts
reordered = [
  { id: "B" },
  { id: "A" },
  { id: "C" },
];
```

发送：

```ts
{
  crateId: "...",
  snippetIds: ["B", "A", "C"],
}
```

后端根据这个数组更新顺序。

成功后：

```ts
void query.refetch();
```

重新请求列表，确保页面顺序与服务端一致。

失败后：

```ts
setActionError(error.message)
```

展示错误。

---

# 十三、重试列表查询

```ts
const handleRetry = useCallback(() => {
  void query.refetch();
}, [query]);
```

当列表加载失败时，用户点击重试按钮，再次请求数据。

这里的：

```ts
void query.refetch();
```

表示开发者明确忽略这个 Promise 的返回值。

如果直接写：

```ts
query.refetch();
```

某些 ESLint 规则可能提示：

```text
Promise 没有被 await 或处理
```

写成：

```ts
void query.refetch();
```

表示：

> 我知道它返回 Promise，但这里不需要等待结果。

---

# 十四、展开和收起代码

```ts
const handleToggleExpand = useCallback((snippetId: string) => {
  setExpandedSnippetIds((current) => {
    const next = new Set<string>(current);

    if (next.has(snippetId)) {
      next.delete(snippetId);
    } else {
      next.add(snippetId);
    }

    return next;
  });
}, []);
```

这里使用了 React 状态的函数式更新。

```ts
setExpandedSnippetIds((current) => {
```

`current` 是最新的展开 ID 集合。

然后复制一份：

```ts
const next = new Set<string>(current);
```

为什么不能直接修改 `current`？

不推荐这样写：

```ts
current.add(snippetId);
return current;
```

因为 React 判断状态有没有变化，主要依赖引用。

如果返回原来的 `Set`：

```ts
return current;
```

引用没有变化，React 可能不会重新渲染。

所以这里创建新的 Set：

```ts
const next = new Set(current);
```

再修改并返回：

```ts
return next;
```

---

## 展开逻辑

```ts
if (next.has(snippetId)) {
  next.delete(snippetId);
} else {
  next.add(snippetId);
}
```

即：

```text
已经展开 → 从 Set 删除 → 收起
没有展开 → 加入 Set → 展开
```

---

# 十五、组合请求状态

```ts
const isSaving =
  createMutation.mutation.isPending ||
  updateMutation.mutation.isPending;

const isReordering =
  reorderMutation.mutation.isPending;
```

`isSaving` 同时表示：

```text
正在新增
或
正在修改
```

因为这两种操作使用的是同一个表单 Dialog，所以可以合并成一个状态。

最终传给：

```tsx
<CrateCodeSnippetDialog
  isSubmitting={isSaving}
/>
```

如果正在保存，上一段 Dialog 中的按钮会：

```tsx
<Button disabled={isSubmitting}>
```

从而防止重复提交。

`isReordering` 则用于禁用上下移动按钮。

---

# 十六、最外层 `section`

```tsx
<section
  aria-labelledby="crate-code-snippets-heading"
  className="space-y-3"
>
```

`aria-labelledby` 指向：

```tsx
<h2 id="crate-code-snippets-heading">
```

这表示：

> 这个 section 的标题是这个 h2。

有利于屏幕阅读器理解页面结构。

---

# 十七、顶部标题和添加按钮

```tsx
<div className="flex items-center justify-between gap-3">
  <div>
    <h2>{t("crateDetail.codeSnippets")}</h2>
    <p>{t("crateDetail.codeSnippetsDescription")}</p>
  </div>

  <Button onClick={handleAdd}>
    <Plus aria-hidden="true" />
    {t("crateDetail.addSnippet")}
  </Button>
</div>
```

布局效果大致是：

```text
代码片段                         [ + 添加代码片段 ]
管理当前 Crate 下的代码示例
```

点击按钮执行：

```ts
handleAdd()
```

进入新增模式。

图标使用：

```tsx
aria-hidden="true"
```

因为按钮已经有文字“添加代码片段”，图标只是装饰，屏幕阅读器不需要重复朗读。

---

# 十八、错误展示

```tsx
{actionError && (
  <p className="text-sm text-destructive" role="alert">
    {actionError}
  </p>
)}
```

只要 `actionError` 不为空，就展示错误。

```tsx
role="alert"
```

会告诉辅助技术：

> 这是一条需要立即关注的动态信息。

需要注意，这个错误位于主面板中，而它又同时被传给表单 Dialog，因此某些错误可能会在两个地方同时出现。

---

# 十九、四种列表状态

这里使用了连续的三元表达式：

```tsx
{query.isLoading ? (
  <LoadingState />
) : query.isError ? (
  <ErrorState />
) : snippets.length === 0 ? (
  <EmptyState />
) : (
  <代码片段列表 />
)}
```

这是典型的异步页面状态处理。

执行优先级是：

```text
1. 正在加载
2. 加载失败
3. 数据为空
4. 正常展示列表
```

---

## 加载状态

```tsx
<LoadingState className="py-10" />
```

请求还没完成时展示 Loading。

---

## 错误状态

```tsx
<ErrorState
  action={
    <Button onClick={handleRetry}>
      {t("common.retry")}
    </Button>
  }
  message={query.error.message}
  title={t("crateDetail.snippetsLoadError")}
/>
```

列表请求失败时：

* 展示错误标题
* 展示错误内容
* 提供重试按钮

---

## 空状态

```tsx
<EmptyState
  action={
    <Button onClick={handleAdd}>
      {t("crateDetail.addSnippet")}
    </Button>
  }
  icon={<Code2 />}
  title={t("crateDetail.noSnippets")}
  description={t("crateDetail.noSnippetsDescription")}
/>
```

没有代码片段时，引导用户创建第一条记录。

---

## 正常状态

```tsx
snippets.map((snippet, index) => {
```

遍历代码片段并渲染 Card。

---

# 二十、代码片段卡片

每个代码片段使用：

```tsx
<Card key={snippet.id}>
```

`key={snippet.id}` 用于帮助 React 区分列表元素。

卡片头部展示：

```tsx
<h3>{snippet.name}</h3>
<Badge>{snippet.language}</Badge>
```

例如：

```text
React Context      [tsx]
```

如果有描述：

```tsx
{snippet.description && (
  <p>{snippet.description}</p>
)}
```

只有描述不为空时才渲染。

---

# 二十一、向上和向下移动按钮

向上按钮：

```tsx
<Button
  disabled={index === 0 || isReordering}
  onClick={() => handleMove(index, -1)}
>
```

两种情况下禁用：

```text
当前是第一个元素
正在执行排序请求
```

向下按钮：

```tsx
<Button
  disabled={
    index === snippets.length - 1 ||
    isReordering
  }
  onClick={() => handleMove(index, 1)}
>
```

两种情况下禁用：

```text
当前是最后一个元素
正在执行排序请求
```

这样 UI 就不会允许无效移动，也防止排序请求期间连续点击。

---

# 二十二、编辑按钮

```tsx
<Button
  aria-label={t("crateDetail.editSnippetNamed", {
    name: snippet.name,
  })}
  onClick={() => handleEdit(snippet)}
>
  <Pencil aria-hidden="true" />
</Button>
```

按钮只有图标，没有可见文字，所以需要：

```tsx
aria-label="编辑 React Context"
```

让屏幕阅读器知道按钮的用途。

点击后把当前 `snippet` 传给：

```ts
handleEdit(snippet)
```

然后打开编辑 Dialog。

---

# 二十三、删除按钮

```tsx
<Button
  aria-label={t("crateDetail.deleteSnippetNamed", {
    name: snippet.name,
  })}
  onClick={() => handleOpenDelete(snippet)}
>
  <Trash2 aria-hidden="true" />
</Button>
```

点击后不会立即删除，而是：

```ts
setDeletingSnippet(snippet)
```

打开确认弹窗。

这是一个重要的交互保护：

```text
点击删除
→ 打开确认弹窗
→ 用户确认
→ 才调用删除接口
```

---

# 二十四、展开按钮

```tsx
<Button
  onClick={() => handleToggleExpand(snippet.id)}
>
  {isExpanded ? (
    <ChevronDown />
  ) : (
    <ChevronRight />
  )}
</Button>
```

这里根据 `isExpanded` 切换图标：

```text
未展开：ChevronRight  →
已展开：ChevronDown   ↓
```

然后根据状态决定是否显示代码：

```tsx
{isExpanded && (
  <CardContent>
    <pre>
      <code>{snippet.code}</code>
    </pre>
  </CardContent>
)}
```

代码使用：

```tsx
<pre>
  <code>{snippet.code}</code>
</pre>
```

这样能保留原始换行和空格。

同时：

```tsx
max-h-80 overflow-auto
```

表示代码过长时限制最大高度，并出现滚动条。

---

# 二十五、父组件如何使用新增/编辑 Dialog

```tsx
<CrateCodeSnippetDialog
  initialData={editingSnippet}
  isSubmitting={isSaving}
  open={dialogOpen}
  serverError={actionError}
  onClose={handleCloseDialog}
  onSubmit={handleSubmit}
/>
```

这正是父子组件连接的核心。

每个参数对应关系如下：

```text
父组件状态或函数              子组件 Props
────────────────────────────────────────────
editingSnippet        →      initialData
isSaving              →      isSubmitting
dialogOpen            →      open
actionError           →      serverError
handleCloseDialog     →      onClose
handleSubmit          →      onSubmit
```

---

## 数据向下传递

```text
父组件
  editingSnippet
       ↓
子组件
  initialData
       ↓
表单默认值
```

这是 React 的单向数据流。

---

## 事件向上传递

```text
用户在子组件点击保存
       ↓
子组件完成 Zod 校验
       ↓
调用 props.onSubmit(values)
       ↓
执行父组件 handleSubmit
       ↓
父组件调用新增或修改接口
```

因此子组件并不知道接口地址，也不负责调用 Refine。

这是一种很清晰的职责分离：

```text
Dialog
→ 管 UI 和表单

Panel
→ 管数据和业务
```

---

# 二十六、父组件如何使用删除 Dialog

```tsx
<DeleteCrateCodeSnippetDialog
  isDeleting={deleteMutation.mutation.isPending}
  snippet={deletingSnippet}
  onCancel={handleCancelDelete}
  onConfirm={handleDelete}
/>
```

对应关系：

```text
删除请求状态        → isDeleting
当前待删除对象      → snippet
取消函数            → onCancel
确认删除函数        → onConfirm
```

删除子组件只需要负责：

```text
展示待删除代码片段信息
询问用户是否确认
触发 onCancel 或 onConfirm
```

实际删除接口仍然由父组件执行。

---

# 二十七、完整的新增流程

```text
用户点击“添加代码片段”
        ↓
handleAdd
        ↓
editingSnippet = null
dialogOpen = true
        ↓
Dialog 打开空表单
        ↓
用户填写并提交
        ↓
Dialog 使用 Zod 校验
        ↓
调用父组件 handleSubmit(values)
        ↓
editingSnippet 是 null
        ↓
createMutation.mutate
        ↓
创建成功
        ↓
handleCloseDialog
```

---

# 二十八、完整的编辑流程

```text
用户点击某个卡片的编辑按钮
        ↓
handleEdit(snippet)
        ↓
editingSnippet = snippet
dialogOpen = true
        ↓
Dialog 根据 initialData 填充表单
        ↓
用户修改并提交
        ↓
调用父组件 handleSubmit(values)
        ↓
editingSnippet 不为 null
        ↓
updateMutation.mutate
        ↓
更新成功
        ↓
handleCloseDialog
```

---

# 二十九、完整的删除流程

```text
点击删除按钮
        ↓
handleOpenDelete(snippet)
        ↓
deletingSnippet = snippet
        ↓
删除确认 Dialog 打开
        ↓
用户确认
        ↓
handleDelete
        ↓
deleteMutation.mutate
        ↓
删除成功
        ↓
deletingSnippet = null
```

---

# 三十、完整的排序流程

```text
点击向上或向下按钮
        ↓
handleMove(index, direction)
        ↓
moveCrateCodeSnippet 计算新数组
        ↓
发送排序后的 snippetIds
        ↓
后端更新 sortOrder
        ↓
query.refetch()
        ↓
重新获取最新顺序
```

---

# 三十一、这个组件的职责划分

这个父组件负责：

```text
数据查询
创建请求
更新请求
删除请求
排序请求
请求状态
业务错误
弹窗开关
当前编辑对象
当前删除对象
列表渲染
展开收起
```

子组件 `CrateCodeSnippetDialog` 负责：

```text
展示输入框
管理表单值
执行 Zod 校验
显示字段错误
触发 onSubmit
```

删除子组件负责：

```text
展示删除确认
触发取消
触发确认
```

这种结构可以概括成：

```text
父组件：聪明组件 / 容器组件
子组件：展示组件 / 表单组件
```

---

# 三十二、代码中值得注意的几个问题

## 1. 展开按钮的 `aria-label` 写错了

展开按钮目前使用的是：

```tsx
aria-label={t("crateDetail.deleteSnippetNamed", {
  name: snippet.name,
})}
```

也就是“删除某个代码片段”。

但这个按钮实际功能是展开和收起。

这会导致屏幕阅读器错误地朗读：

```text
删除 React Context
```

实际上点击后却只是展开代码。

应该根据状态写成类似：

```tsx
aria-label={
  isExpanded
    ? t("crateDetail.collapseSnippetNamed", {
        name: snippet.name,
      })
    : t("crateDetail.expandSnippetNamed", {
        name: snippet.name,
      })
}
```

这是当前代码中一个比较明确的无障碍 Bug。

---

## 2. `actionError` 承担了太多职责

目前：

```ts
const [actionError, setActionError] = useState<string | null>(null);
```

同时保存：

```text
新增错误
编辑错误
删除错误
排序错误
```

并且既展示在主页面，也传给编辑 Dialog：

```tsx
serverError={actionError}
```

可能出现这种情况：

```text
排序失败
→ actionError 被赋值
→ 用户打开新增弹窗
→ 虽然 handleAdd 会清空，但其他时序下可能混用
```

更清晰的设计可以拆成：

```ts
const [formError, setFormError] = useState<string | null>(null);
const [deleteError, setDeleteError] = useState<string | null>(null);
const [reorderError, setReorderError] = useState<string | null>(null);
```

不过当前代码通过每次操作前：

```ts
setActionError(null)
```

已经降低了错误串场的可能性。

---

## 3. 删除成功后的列表更新依赖 Refine 行为

删除成功时只做了：

```ts
setDeletingSnippet(null)
```

没有显式：

```ts
query.refetch()
```

这可能是因为 Refine 的 `useDelete` 会自动失效相关查询缓存并刷新列表。

如果项目的 invalidation 配置正常，这没有问题。

如果发现删除成功后页面没有更新，就需要：

```ts
onSuccess: () => {
  setDeletingSnippet(null);
  void query.refetch();
}
```

---

## 4. 新增时的 `sortOrder`

```ts
sortOrder: snippets.length
```

假设现有排序值一定连续：

```text
0, 1, 2
```

那么新值 `3` 没问题。

但如果数据库中出现：

```text
0, 5, 10
```

当前列表长度是 `3`，新记录就会得到：

```ts
sortOrder = 3
```

它可能插入中间，而不是末尾。

更稳妥的方式可能是：

```ts
const lastSortOrder = snippets.at(-1)?.sortOrder ?? -1;

sortOrder: lastSortOrder + 1
```

前提是 `CrateCodeSnippet` 中确实存在 `sortOrder` 字段并且列表已经按它排序。

---

## 5. 排序没有进行乐观更新

当前点击移动后：

```text
点击按钮
→ 请求后端
→ 请求成功
→ refetch
→ 页面顺序变化
```

网络慢时，用户可能感觉按钮没有立即生效。

可以考虑：

```text
先在页面更新顺序
再请求后端
失败时回滚
```

也就是乐观更新。

不过当前实现更简单，也能保证最终页面以服务端结果为准。

---

## 6. `useMemo` 可能不需要

```ts
const snippets = useMemo(
  () => (result?.data ?? []) as CrateCodeSnippet[],
  [result?.data],
);
```

这里的计算本身非常简单，可以直接写：

```ts
const snippets =
  (result?.data ?? []) as CrateCodeSnippet[];
```

除非确实依赖稳定的数组引用，否则使用 `useMemo` 的收益有限。

---

# 三十三、最核心的理解

这个组件最关键的是三个状态：

```ts
dialogOpen
editingSnippet
deletingSnippet
```

其中新增和编辑复用了同一个 Dialog：

```text
dialogOpen 决定是否打开
editingSnippet 决定新增还是编辑
```

最关键的判断是：

```ts
if (editingSnippet) {
  updateMutation.mutate(...);
  return;
}

createMutation.mutate(...);
```

最关键的父子通信是：

```tsx
<CrateCodeSnippetDialog
  initialData={editingSnippet}
  open={dialogOpen}
  onClose={handleCloseDialog}
  onSubmit={handleSubmit}
/>
```

可以把它记成：

```text
父组件把“数据和状态”传给 Dialog
Dialog 把“用户操作结果”传回父组件
父组件再调用后端接口
```

这正是 React 中非常典型的：

```text
状态提升 + 单向数据流
```
