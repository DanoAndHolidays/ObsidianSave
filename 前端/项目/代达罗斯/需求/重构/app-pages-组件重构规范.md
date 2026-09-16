---
title: 代达罗斯 app pages 组件重构规范
date: 2026-08-14
tags:
  - 代达罗斯
  - 前端
  - React
  - 重构
  - 组件规范
---

# app-pages-组件重构规范
> Last Format Time：8/14/2026 10:55:41

> 适用范围：apps/app/src/pages
>
> 文档目标：总结当前页面组件的真实写法，区分“已形成的有效模式”和“需要在重构中收敛的问题”，最终给出一套可执行、可检查、可渐进迁移的统一规范。

---
## 结论先行
当前 pages 已经形成一套清晰的页面归属结构：

1. 页面根目录只暴露 Wrapper。
2. 页面私有组件全部收敛到 _components。
3. 页面 Wrapper 负责路由参数、依赖适配和 Store Provider。
4. PageContent 负责页面内容编排。
5. 页面级 Store 使用 Zustand Context + Provider + useInit。
6. Storybook 已经成为页面和组件的强制契约。

这套骨架应保留。重构的重点不是重新设计目录，而是收紧以下边界：

1. PageContent 和部分业务组件过大，需要按职责拆分。
2. 数据读取同时存在 Refine、TanStack Query 直连和 trpcClient 直连，需要统一到 Refine DataProvider。
3. 22/24 个页面都创建了 Store，需要重新判断哪些页面真的需要 Store。
4. 页面 Store、URL 状态、表单状态、服务端状态的边界还不完全统一。
5. 页面私有组件的 Story 覆盖很好，但单元测试覆盖不足。
6. 页面实现中仍存在较多原生 button、input、textarea 等标准交互元素。
7. 表单已经普遍采用 react-hook-form，但没有统一使用 FormField 组件族。

推荐把 CratesPage 作为当前仓库内的主要正向样板：它的 Content 只做组合，查询被封装到 _hooks，服务端状态保留在 Refine Query，Store 主要承接筛选、分页和弹窗交互。

---
## 本次盘点范围与数据
### 2.1 总体规模
| 指标 | 当前值 |
| --- | ---: |
| 页面目录 | 24 |
| pages 下文件总数 | 671 |
| TSX 文件 | 372 |
| TS 文件 | 299 |
| 排除 test、spec、stories 后的实现 TSX | 183 |
| 使用页面级 Store 的页面 | 22 / 24 |
| 页面私有组件目录 | 119 |
| 具备同名主组件的组件目录 | 118 |
| 具备 index.ts 的组件目录 | 119 / 119 |
| 具备同名 Story 的主组件 | 118 / 118 |
| 具备同名 Test 的主组件 | 44 / 118，约 37% |

### 2.2 复杂度信号
| 指标 | 当前值 |
| --- | ---: |
| 实现 TSX 超过 150 行 | 52 |
| 实现 TSX 超过 200 行 | 32 |
| 实现 TSX 超过 300 行 | 12 |
| 实现 TSX 超过 400 行 | 7 |
| 实现 TSX 超过 500 行 | 3 |
| 实现 TSX 中位数 | 约 70 行 |
| 实现 TSX 平均值 | 约 111 行 |

超过 500 行的三个文件：

- JobDetailPage/_components/JobDetailPageContent/JobDetailPageContent.tsx
- ProjectDetailPage/_components/ScanDialog/ScanDialog.tsx
- ArchetypeDetailPage/_components/ArchetypeDetailPageContent/ArchetypeDetailPageContent.tsx

另外，ProjectDetailPageContent、DictionaryDetailPageContent、AnatomyEntryRow、AnatomyDetailPageContent 等也超过 400 行。

行数不是唯一拆分依据，但这些文件已经同时具备“数据读取、业务动作、状态分支、布局和局部组件”多种职责，应作为优先重构对象。

### 2.3 数据访问现状
| 信号 | 当前值 |
| --- | ---: |
| 使用或导入 trpcClient 的实现 TS/TSX | 29 个文件 |
| 使用 TanStack useQuery 的实现 TS/TSX | 15 个文件 |
| 使用 Refine useList | 12 个文件 |
| 使用 Refine useOne | 5 个文件 |
| 使用 Refine useCreate | 3 个文件 |
| 使用 Refine useUpdate | 7 个文件 |
| 使用 Refine useDelete | 3 个文件 |

问题不是 Refine 不存在，而是同一层中并存三条访问路径。目标必须统一为：

Component → Refine hook → DataProvider → tRPC

组件、PageContent、Wrapper、页面私有 hook 不再直接调用 trpcClient，也不使用 TanStack useQuery 直接包装 tRPC。

### 2.4 UI 与表单现状
| 信号 | 当前值 |
| --- | ---: |
| 包含原生标准交互元素的实现 TSX | 37 / 183 |
| 原生标准交互元素总计 | 93 |
| 其中原生 button | 75 |
| 使用 useForm 的实现文件 | 9 |
| 使用 zodResolver 的实现文件 | 6 |
| 使用 FormProvider 的实现文件 | 6 |
| 使用 FormField 的实现文件 | 0 |

原生布局和文本标签不需要替换；需要收敛的是原生 button、input、textarea、select、dialog、table 等已有共享 UI 对应物的标准交互。

### 2.5 已有自动化契约
以下测试已于 2026-08-14 验证通过，共 2 个测试文件、16 个测试：

- apps/app/src/pages/page-colocation.spec.ts
- apps/app/src/pages/page-stories-coverage.spec.ts

它们已经强制保证：

- 页面根目录只保留公开入口文件。
- 每个页面必须有 Wrapper、_components 和 index.ts。
- 页面 index.ts 只能导出 Wrapper。
- _components 下每个直接子项必须是独立目录并包含 index.ts。
- 每个页面 Wrapper 必须有 Story。
- 每个具备同名主组件的组件单元必须有 Story。
- Story 标题必须由页面归属推导。
- 每个 Story 必须包含 Base、Default、BaseUsage。
- Default 必须使用空 args。
- 每个页面 Story 必须包含 MockData 和 FullApplication。
- 路由页面 Story 必须声明 URL、在渲染前安装 mock。

这些规则是仓库当前的硬契约，重构时不能破坏。

---
## 当前写法的分层总结
### 3.1 Page Wrapper
典型结构：

~~~tsx
import { XxxPageContent } from "./_components/XxxPageContent";
import { XxxPageStoreProvider } from "./_store";

export const XxxPage = () => {
  return (
    <XxxPageStoreProvider>
      <XxxPageContent />
    </XxxPageStoreProvider>
  );
};
~~~

当前 Wrapper 通常承担：

- 读取路由 params 或 search。
- 获取路由器、QueryClient、全局 Store 实例。
- 把外部能力转换为页面 Store dependencies。
- 挂载页面 Store Provider。
- 渲染 PageContent。

这是合理方向，但已经出现三类偏差：

- AiReviewsRulesPage、AiReviewsSettingsPage、TeamSettingsPage 的 Wrapper 超过 50 行。
- 部分 Wrapper 直接调用 trpcClient。
- 部分 Wrapper 内联创建了大量依赖实现和业务流程。

结论：Wrapper 可以做依赖注入，但不能成为新的业务 Service。

### 3.2 PageContent
当前仓库没有把 PageContent 直接放在页面根目录，而是统一放在：

~~~text
PageName/_components/PageNameContent/
~~~

这是仓库自身测试所保护的真实结构，应优先于通用模板，并继续保留。

理想的 PageContent 只负责页面级组合，例如 CratesPageContent：

~~~tsx
export const CratesPageContent = () => {
  return (
    <>
      <CratesHeaderActions />
      <div className="px-7 py-2.5">
        <CratesFilterToolbar />
        <CratesTable />
        <CratesPagination />
      </div>
      <CreateCrateDialog />
      <EditCrateDialog />
    </>
  );
};
~~~

当前偏差是部分 PageContent 同时承担：

- 数据查询和 mutation。
- 查询参数拼装。
- Loading、Error、Empty、Success 全部分支。
- 复杂列表、表格或树渲染。
- Dialog、Tabs 和局部表单。
- 业务事件适配。

这会形成 God Component，也是当前 300～500 行文件的主要来源。

### 3.3 页面私有组件
当前页面私有组件统一归属于：

~~~text
PageName/_components/ComponentName/
~~~

绝大多数目录已经包含：

- ComponentName.tsx
- ComponentName.stories.tsx
- index.ts

这是非常好的共置模式。需要补齐的是：

- ComponentName.test.tsx。
- 一组件一目录。
- 一文件一组件。
- Props 类型导出。

目前有 8 个组件目录内放了多个实现 TSX，例如：

- FindingPills
- AnatomiesFilterToolbar
- ArchetypeDialogAdapter
- CrateDetailPageContent
- CratesTable
- DictionaryDialogAdapter
- ProjectDetailPageContent
- ScanDialog

这些目录中的附属组件如果具备独立职责、独立引用或超过约 10 行，应拆成自己的组件目录；纯函数、类型、常量、hook 可以继续与主组件共置。

### 3.4 页面 Store
22 个页面存在 _store。所有 22 个 Provider 都使用 useInit 创建 Store 实例，19 个页面显式定义 dependencies。这是目前最稳定的实现模式之一。

常见结构：

~~~text
_store/
├── index.ts
├── provider.tsx
├── xxxPageDependencies.ts
├── xxxPageSlice.ts
├── xxxPageStore.ts
└── xxxPageStore.test.ts
~~~

复杂页面允许把 Slice 进一步拆到：

~~~text
_store/_slices/
~~~

当前 Store 的主要职责：

- 跨兄弟组件共享的 UI 状态。
- Dialog、Tab、Selection、Filter 等交互状态。
- UI 事件 handler。
- 页面业务流程的依赖调用。
- 部分页面表单的 formControl。

需要收紧的边界：

- 查询结果、query loading、query error 不进入 Store。
- URL 可表达的筛选、分页、Tab 优先放 Route Search。
- 表单字段值由 react-hook-form 管理，不和 Zustand 双向同步。
- 页面业务流程可以由 Slice 编排，但外部副作用优先通过 dependencies 注入。
- Store 不直接依赖 React 组件、JSX 或 React hook。

### 3.5 Storybook
当前 Storybook 规范非常成熟，应直接继承：

页面 Story 标题：

~~~text
Pages/PageName/Page
~~~

页面私有组件 Story 标题：

~~~text
Pages/PageName/Components/ComponentName
~~~

每个 Story 至少包含：

- Base
- Default
- BaseUsage

页面 Story 还必须包含：

- MockData
- FullApplication

有业务交互的组件增加 ShouldXxx，并通过 play 执行真实用户行为。

---
## 重构后的目标目录规范
### 4.1 标准页面
~~~text
PageName/
├── index.ts
├── PageName.tsx
├── PageName.stories.tsx
├── PageName.test.tsx                  # Wrapper 有路由或依赖行为时要求
├── _components/
│   ├── PageNameContent/
│   │   ├── index.ts
│   │   ├── PageNameContent.tsx
│   │   ├── PageNameContent.test.tsx
│   │   └── PageNameContent.stories.tsx
│   └── FeaturePanel/
│       ├── index.ts
│       ├── FeaturePanel.tsx
│       ├── FeaturePanel.test.tsx
│       └── FeaturePanel.stories.tsx
├── _hooks/                            # 可选：页面私有查询或组合 hook
│   ├── index.ts
│   └── usePageNameQuery.ts
├── _store/                            # 可选：确有跨组件 UI 状态时创建
│   ├── index.ts
│   ├── provider.tsx
│   ├── pageNameDependencies.ts
│   ├── pageNameSlice.ts
│   ├── pageNameStore.ts
│   └── pageNameStore.test.ts
└── _lib/                              # 可选：纯函数、常量、view model
    └── buildPageNameViewModel.ts
~~~

### 4.2 页面根目录
页面根目录只允许：

- PageName.tsx
- PageName.stories.tsx
- PageName.test.tsx
- PageName.stories.test.tsx
- index.ts
- _components、_hooks、_store、_lib 等私有目录

禁止把具体业务组件、schema、工具函数散落在页面根目录。

### 4.3 index.ts
页面根 index.ts 只能：

~~~ts
export * from "./PageName";
~~~

组件单元 index.ts 只能：

~~~ts
export * from "./ComponentName";
~~~

要求：

- 只做 re-export。
- 使用相对路径。
- 不写变量、函数、类型定义或业务逻辑。
- 不使用 default export。
- 外部消费者通过目录入口导入。
- 同目录实现文件不要反向 import 自己的 index.ts，避免循环依赖。

---
## 各层职责规范
### 5.1 Wrapper：只做入口适配和依赖注入
允许：

- 读取 route params、route search。
- 获取必须由 React hook 提供的外部能力。
- 调用 useXxxPageDependencies 形成稳定 dependencies。
- 挂载页面 Provider。
- 传入真正的入口参数，例如路由 ID。

禁止：

- 可见 UI、页面布局和 Tailwind className。
- Loading、Error、Empty 等渲染分支。
- 直接调用 trpcClient。
- 内联实现大段 CRUD 或业务流程。
- 持有页面业务数据。
- 用 useState 管理页面状态。

建议：

- Wrapper 目标控制在 30 行以内。
- 超过 50 行必须把依赖构造移入 useXxxPageDependencies 或 createXxxPageDependencies。
- 依赖对象使用 useMemo，避免 Provider 或 Store 因每次渲染获得新引用。

### 5.2 PageContent：只做页面级编排
允许：

- 组合 Header、Toolbar、Table、Panel、Dialog 等页面私有组件。
- 定义页面主布局。
- 在非常简单的页面中读取少量本地状态。

禁止：

- 直接调用 trpcClient。
- 直接使用 TanStack useQuery 访问业务数据。
- 同时承担查询、复杂业务动作和大块 JSX。
- 在文件内定义多个可独立复用的子组件。
- 把 Store 中已有数据先读取后再层层传给页面绑定子组件。

建议：

- PageContent 以“看一眼就能理解页面由哪些区域组成”为目标。
- JSX 嵌套超过 4 层、条件分支超过 3 组、出现可命名区域时就拆分。
- 150 行进入拆分评审，300 行原则上必须拆分；例外需在代码评审中说明职责仍然单一的原因。

### 5.3 页面私有业务组件
每个组件：

- 一个组件一个文件。
- 一个有独立职责的组件一个目录。
- 文件名、目录名、组件名保持 PascalCase 一致。
- 使用命名导出。
- 有 Props 时导出 ComponentNameProps。
- 与测试和 Story 同目录。
- 通过 className 或组合提供合理扩展点。
- 交互元素满足键盘、焦点和 aria 语义。

拆分依据按优先级排序：

1. 是否承担两个以上业务职责。
2. 是否可独立测试和独立命名。
3. 是否存在复杂条件渲染。
4. 是否被多个位置使用。
5. JSX 是否过深。
6. 文件是否超过建议行数。

不要仅为了减少行数拆出没有语义的 1～2 行组件。

### 5.4 Props 与 Store
页面绑定组件和纯展示组件采用不同规则：

页面绑定组件：

- Store 中已有的页面状态直接通过颗粒化 selector 读取。
- 不允许 Parent 从 Store 读取，再只为传给 Child 而透传。
- 不允许一次订阅整个 Store state。
- 每个 selector 读取一个字段或一组紧密相关字段。

纯展示或可复用组件：

- 通过明确、最小的 Props 接收数据。
- 不耦合页面 Store。
- 可以接收 label、route ID、纯展示数据、事件回调。
- 不接收整个 Store、Query 对象或过大的配置对象。

判断原则：

- 如果组件只属于当前页面且业务状态已经在该页面 Store 中，直接读 Store。
- 如果组件应脱离页面独立展示、测试或复用，使用明确 Props。

---
## 状态归属决策表
| 状态类型 | 应放位置 | 示例 |
| --- | --- | --- |
| 服务端数据 | Refine Query | 列表、详情、统计、成员 |
| 查询 loading/error | Refine 返回的 query | LoadingState、ErrorState |
| URL 可表达状态 | TanStack Router search/params | page、search、type、tab、create |
| 表单字段、dirty、校验错误 | react-hook-form | name、email、paths |
| 单组件临时 UI 状态 | useState | 局部 hover、一次性折叠 |
| 跨兄弟组件 UI 状态 | 页面 Zustand Store | Dialog open、selection、编辑目标 |
| 全应用状态 | 全局 Store | 当前 workspace、toast |

### 6.1 何时创建页面 Store
满足任一条件时可以创建：

- 状态需要被两个以上页面私有组件共享。
- 出现超过一层的 Props Drilling。
- 存在多步骤交互或多组件协作流程。
- 需要颗粒化 selector 控制重渲染。
- 页面 UI 状态需要在局部组件卸载后保留。

以下情况不要创建页面 Store：

- 纯展示页。
- 只有一个 useList 或 useOne 的数据页。
- 只有一个简单表单。
- 状态只属于单个组件。
- 只是为了统一代码外观而创建空 Provider。

重构时应重点复核当前 22 个 Store；Store 的存在必须能回答“哪些兄弟组件共享了什么 UI 状态”。

---
## 数据获取统一规范
### 7.1 查询
查询必须使用 Refine：

~~~tsx
import { useList } from "@refinedev/core";
import { ResourceName } from "@/integrations/refine/dataProvider";

export const useItemsListQuery = () => {
  const { query, result } = useList<Item>({
    resource: ResourceName.items,
  });

  return {
    items: result.data,
    error: query.error,
    isLoading: query.isLoading,
    total: result.total ?? 0,
  };
};
~~~

注意：

- 必须使用 useList 返回的 query 控制 LoadingState 和 ErrorState。
- 不把 result.data、query.isLoading、query.error复制进 Zustand。
- 页面中多处使用同一查询时，封装为语义化的 useXxxQuery。

### 7.2 修改
标准 CRUD 使用：

- useCreate
- useUpdate
- useDelete
- useCustomMutation
- useInvalidate

如果 Store 需要编排修改流程，由 Provider 或专用 dependency hook 获取 Refine mutation，再以函数依赖注入 Store。

禁止：

- 在组件、PageContent、Wrapper 中直接调用 trpcClient。
- 用 TanStack useQuery 或 useMutation 直接包装 tRPC。
- 手写 query key 作为主要失效机制，优先用 Refine useInvalidate。
- 因为 Refine 内置方法暂时不够用就绕过 DataProvider；应扩展 DataProvider 或使用 custom。

### 7.3 渲染状态
每个服务端数据组件按顺序处理：

1. Error。
2. Loading。
3. Empty。
4. Success。

优先使用：

- ErrorState
- LoadingState
- EmptyState

不要在 PageContent 中重复实现页面各区域的状态细节；状态属于实际消费该查询的业务组件。

---
## Store 规范
### 8.1 标准结构
~~~ts
export interface XxxPageSlice {
  dialogOpen: boolean;
  handleCreateButtonClick: () => void;
  handleDialogOpenChange: (open: boolean) => void;
}
~~~

~~~tsx
export const XxxPageStoreProvider = ({ children }: Props) => {
  const dependencies = useXxxPageDependencies();
  const store = useInit(() => createXxxPageStore(dependencies));

  return (
    <XxxPageStoreContext.Provider value={store}>
      {children}
    </XxxPageStoreContext.Provider>
  );
};
~~~

### 8.2 Store 硬规则
- 使用 createStore，不创建隐式全局单例页面 Store。
- 通过 React Context 提供 Store。
- Provider 使用 useInit，保证每个页面实例只创建一次 Store。
- 组件只从 _store 桶入口导入。
- Slice 按职责拆分，不按字段机械拆分。
- 方法采用 UI 行为命名，例如 handleSubmitButtonClick、handleSearchInputChange。
- 输入 handler 的签名尽量直接匹配事件 prop，避免 JSX 内联适配层。
- Store 测试覆盖默认状态、关键动作、异步成功和失败路径。
- Store 不包含 React 组件、JSX、useState、useEffect、useNavigate、useForm 等 hook。

### 8.3 异步流程的统一决策
项目现有规则之间存在一个表面冲突：一处规则要求 Slice 不包含异步请求，另一处规则允许 Slice 编排异步业务流程。

本项目统一为：

- Slice 可以编排由 UI 事件触发的异步流程。
- 真正的数据访问能力通过 dependencies 注入。
- 查询数据和查询状态始终留在 Refine Query。
- Slice 不直接调用 trpcClient。
- Slice 不直接使用 React hook。

这样既保留 Store 对复杂交互流程的集中管理，也不会破坏 Component → Refine → DataProvider → tRPC 的数据链路。

---
## 表单规范
### 9.1 技术栈
- react-hook-form 管理表单状态。
- Zod v4 作为数据契约。
- zodResolver 集成校验。
- @repo/ui 的 Form、FormField、FormItem、FormControl、FormMessage 和输入组件负责 UI。
- Zustand 不与表单字段双向绑定。

### 9.2 两种合法范式
范式 A：独立可复用表单。

- 接收 initialData 和 onSubmit。
- 内部创建 useForm。
- 不依赖页面 Store。
- 适合跨页面或纯输入收集组件。

范式 B：页面绑定表单。

- formControl 由页面 Slice 使用 createFormControl 创建。
- 组件使用 useForm 接管 formControl。
- 提交流程由 Slice 的 handleFormSubmit 编排。
- 不通过 Props 传递 initialData、onSubmit 或 control。

### 9.3 字段结构
~~~tsx
<Form {...form}>
  <form onSubmit={form.handleSubmit(handleFormSubmit)}>
    <FormField
      control={form.control}
      name="name"
      render={({ field }) => (
        <FormItem>
          <FormLabel>Name</FormLabel>
          <FormControl>
            <Input {...field} />
          </FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
    <Button type="submit">Save</Button>
  </form>
</Form>
~~~

说明：

- Form 提供表单上下文，内部原生 form 保留正确的提交语义，这是允许的组合。
- 字段不手写 value + onChange。
- 跨子组件共享时使用 FormProvider + useFormContext。
- defaultValues 使用副本，不直接持有原始对象引用。
- 领域 Schema 和类型优先从 @repo/schemas 导入，类型通过 z.infer 推导。

---
## UI 与可访问性规范
标准交互优先使用 @repo/ui：

| 原生写法 | 项目组件 |
| --- | --- |
| button | Button |
| input | Input、Checkbox、RadioGroup |
| select | Select 组件族 |
| textarea | Textarea |
| label | Label 或 FormLabel |
| table | Table 组件族 |
| dialog | Dialog 组件族 |
| 分页 | Pagination |
| 状态反馈 | LoadingState、ErrorState、EmptyState |

允许保留原生元素：

- div、span、section、header、main 等布局元素。
- h1～h6、p、ul、ol 等文本结构。
- @repo/ui 未覆盖、且已经封装为独立可访问组件的特殊交互。
- Form 内用于提交语义的原生 form。

每个交互组件必须：

- 支持键盘操作。
- 有清晰焦点状态。
- 图标按钮提供 aria-label。
- 行点击同时支持 Enter 或 Space。
- Dialog 正确处理焦点和关闭行为。

---
## Story 与 Test 规范
### 11.1 Story
每个页面 Wrapper 和每个具备主组件的 Component Unit 都必须有 Story。

基础 Story：

- Base
- Default
- BaseUsage

页面 Story：

- MockData
- FullApplication
- route path
- beforeEach mock
- withPageStoryShell

状态型组件增加：

- Loading
- Error
- Empty
- Disabled
- Filtered
- Paginated

交互型组件增加 ShouldXxx，并通过 play 覆盖用户行为。

### 11.2 Test
重构目标是把当前约 37% 的同名测试覆盖提升到 100% Component Unit 覆盖。

每个 ComponentName.test.tsx 至少覆盖：

- 默认渲染。
- 必传 Props 或依赖。
- 关键用户交互。
- Loading、Error、Empty 等关键分支。
- 可访问性语义。

Store 测试覆盖：

- 默认状态。
- 每个关键 handler。
- 异步成功。
- 异步失败。
- formControl reset 或状态恢复。

测试优先验证可观察行为，不依赖实现细节；只有架构契约测试可以直接读取源码。

---
## 重构优先级
### P0：先统一数据边界
目标：

- 清理 29 个直接使用 trpcClient 的实现文件。
- 清理 15 个直接使用 TanStack useQuery 的实现文件。
- 将查询迁移到 Refine useList、useOne、useCustom。
- 将扩展查询迁移进 DataProvider。
- 服务端状态退出 Zustand。

原因：先统一数据流，后续拆组件时才不会把错误依赖复制到更多文件。

### P1：拆分超大组件和超大 Wrapper
优先对象：

- JobDetailPageContent
- ScanDialog
- ArchetypeDetailPageContent
- ProjectDetailPageContent
- DictionaryDetailPageContent
- AnatomyEntryRow
- AnatomyDetailPageContent
- AiReviewsRulesPage Wrapper
- AiReviewsSettingsPage Wrapper
- TeamSettingsPage Wrapper

拆分方向：

- Query hook。
- Header、Toolbar、Tabs、Panel、Table、Dialog。
- 纯 view model builder。
- 页面 dependency hook。

### P1：统一表单与 UI
目标：

- 9 个 useForm 文件统一到两种合法表单范式。
- 全部接入 zodResolver。
- 使用 FormField 组件族。
- 替换 37 个文件中的标准原生交互元素，优先处理 75 个原生 button。

### P2：补齐 Component Unit
目标：

- 为缺少测试的 74 个具备主组件的目录补齐同名 Test。
- 将 8 个包含多个实现组件的目录按独立职责拆分。
- 所有 Props 类型明确并导出。

### P2：复核 Store 必要性
目标：

- 对 22 个页面 Store 逐个应用“是否需要 Store”决策表。
- 删除只包装查询、简单表单或单组件状态的 Store。
- 保留跨组件 UI 状态和复杂流程。

### P3：把新规范自动化
建议扩展现有两个结构测试，新增：

- 禁止 pages 实现文件直接 import trpcClient。
- 禁止 pages 实现文件直接使用 TanStack useQuery/useMutation 访问业务数据。
- 检查 Component Unit 同名 Test。
- 检查一个组件目录内的独立组件是否拥有自己的目录。
- 检查页面和组件 Story 的固定 case。
- 检查页面根 index.ts 只导出 Wrapper。
- 检查原生标准交互元素。
- 检查 PageContent 和 Wrapper 的复杂度告警。

---
## 重构验收清单
### 页面结构
- [ ] 页面根目录只保留公开入口文件和私有目录。
- [ ] index.ts 只导出 Wrapper。
- [ ] Wrapper 只负责参数适配、依赖注入和 Provider。
- [ ] PageContent 位于 _components/PageNameContent。
- [ ] 页面专用组件未提升到全局 components。

### 组件
- [ ] 一个文件只有一个主组件。
- [ ] 一个独立组件拥有独立目录。
- [ ] 组件、目录、文件名一致。
- [ ] 使用命名导出。
- [ ] Props 最小化且类型明确。
- [ ] 不存在 God Component。
- [ ] 不存在无意义 Props Drilling。

### 状态
- [ ] 服务端数据和 query 状态不进入 Zustand。
- [ ] URL 状态保存在 Router search/params。
- [ ] 表单字段状态只由 react-hook-form 管理。
- [ ] Store 只承接确实跨组件的 UI 状态和流程。
- [ ] Store 使用颗粒化 selector。

### 数据
- [ ] 组件和页面不直接调用 trpcClient。
- [ ] 业务查询不直接使用 TanStack useQuery 包装 tRPC。
- [ ] 查询使用 Refine hook。
- [ ] LoadingState 使用 Refine 返回的 query 状态。
- [ ] 自定义能力通过 DataProvider custom 扩展。

### 表单与 UI
- [ ] useForm 配置 zodResolver。
- [ ] 字段使用 FormField 完整结构。
- [ ] 复杂表单使用 FormProvider + useFormContext。
- [ ] 标准交互使用 @repo/ui。
- [ ] 图标按钮和行交互满足可访问性要求。

### 质量
- [ ] 每个页面和主组件都有 Story。
- [ ] 每个 Component Unit 都有同名 Test。
- [ ] Story 包含固定基础 case。
- [ ] 交互 Story 使用 play。
- [ ] 页面结构测试通过。
- [ ] 页面 Story 覆盖测试通过。
- [ ] apps/app 的 test、check-types、lint 或 quality 通过。

---
## 推荐的新页面最小模板
### PageName.tsx
~~~tsx
import { PageNameContent } from "./_components/PageNameContent";
import { PageNameStoreProvider } from "./_store";

export const PageName = () => {
  return (
    <PageNameStoreProvider>
      <PageNameContent />
    </PageNameStoreProvider>
  );
};
~~~

无 Store 时直接渲染 PageNameContent，不创建空 Provider。

### PageNameContent.tsx
~~~tsx
import { PageHeader } from "../PageHeader";
import { PageToolbar } from "../PageToolbar";
import { PageResults } from "../PageResults";

export const PageNameContent = () => {
  return (
    <>
      <PageHeader />
      <PageToolbar />
      <PageResults />
    </>
  );
};
~~~

### index.ts
~~~ts
export * from "./PageName";
~~~

---
## 参考实现与反向样本
推荐优先参考：

- apps/app/src/pages/CratesPage/CratesPage.tsx
- apps/app/src/pages/CratesPage/_components/CratesPageContent/CratesPageContent.tsx
- apps/app/src/pages/CratesPage/_hooks/useCratesListQuery.ts
- apps/app/src/pages/CratesPage/_store/provider.tsx
- apps/app/src/pages/CratesPage/_store/cratesPageStore.ts
- apps/app/src/pages/CratesPage/_components/CratesTable/CratesTable.tsx
- apps/app/src/pages/page-colocation.spec.ts
- apps/app/src/pages/page-stories-coverage.spec.ts

优先重构样本：

- apps/app/src/pages/AiReviewsRulesPage/AiReviewsRulesPage.tsx
- apps/app/src/pages/AiReviewsSettingsPage/AiReviewsSettingsPage.tsx
- apps/app/src/pages/TeamSettingsPage/TeamSettingsPage.tsx
- apps/app/src/pages/JobDetailPage/_components/JobDetailPageContent/JobDetailPageContent.tsx
- apps/app/src/pages/ProjectDetailPage/_components/ScanDialog/ScanDialog.tsx
- apps/app/src/pages/ArchetypeDetailPage/_components/ArchetypeDetailPageContent/ArchetypeDetailPageContent.tsx

---
## 最终统一原则
一句话概括目标结构：

> Wrapper 负责接线，Content 负责组合，组件负责一个明确区域，Refine 负责服务端状态，Router 负责 URL 状态，react-hook-form 负责表单状态，Zustand 只负责跨组件 UI 状态和交互流程。

重构时优先修边界，再拆文件，最后补测试和自动检查。这样可以避免只把大文件拆成多个仍然彼此耦合的小文件。
