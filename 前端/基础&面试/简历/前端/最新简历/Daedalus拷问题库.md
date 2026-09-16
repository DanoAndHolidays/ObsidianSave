# Daedalus拷问题库
> Last Format Time：9/16/2026 19:24:53

> 用途：秋招面试前，围绕简历中的 Daedalus 项目进行“能讲清楚、能落到源码、能经得起追问”的准备。
>
> 适用岗位：前端开发 / React + TypeScript / AI 工程化 / 平台型产品。
>
> 整理日期：2026-08-30

推荐回答模板
1. **先说结论**：我解决了什么问题。
2. **再说方案**：为什么选这个技术，核心数据结构是什么。
3. **再说边界**：哪些由前端负责，哪些由后端/服务层负责。
4. **最后说验证**：用什么测试、源码检查或手工路径验证；没有数据就明确说没有做量化基准。

---
## 项目介绍
### Q：请你介绍一下 Daedalus 项目。
### 建议回答
Daedalus 是一个面向代码审查和==代码治理==的平台。它不是单纯的 CRUD 后台，而是把==代码组织、设计契约、目录结构、术语、审查规则和扫描结果==等治理对象结构化，再通过 ==Web 界面、CLI 和 MCP== 暴露给开发者或 Coding Agent 使用。我主要参与前端开发，负责 Crate、Archetype、Anatomy、Dictionary 等核心模块的列表、详情、创建、编辑和发布体验，同时处理==大型仓库文件树的虚拟化==、==页面级状态管理==、共享业务组件和 MCP 连接相关界面。技术上主要使用 React、TypeScript、TanStack、Refine、Zustand、Zod，后端请求通过 Refine dataProvider 接到 tRPC 和 Service 分层。

**可能追问：为什么说它是“治理平台”，而不是管理后台？**

### 追问回答要点
- 管理后台强调对数据做==增删改查==；治理平台还要表达“代码应该==遵守什么规则==”。
- Crate、Archetype、Anatomy、Dictionary 这些对象之间存在语义关联。
- Anatomy 可以被 CLI 用来检查真实项目目录结构，Finding 可以记录扫描发现的问题。
- MCP 让外部 Agent 在权限和审计边界内读取上下文或执行操作。
- 因此链路是“定义治理标准 → 校验/扫描 → 发现问题 → 处理问题”，而不是孤立的页面。

### Q：你在项目中具体负责什么？
### 建议回答
我的职责重点是前端模块和交互落地：
- 一是治理元数据模块的页面和表单，包括列表、详情、创建、编辑、发布；
- 二是 500+ 节点仓库文件树的可见节点扁平化和虚拟渲染；
- 三是基于 Radix UI / shadcn/ui 封装业务组件并用 Storybook 验证；
- 四是把页面局部状态和回调重构为 Context + Zustand 的页面级 Store，减少 Props Drilling；
- 五是参与 Anatomy 独立包、CLI、Monorepo 规范和 MCP 连接相关页面的联调与状态反馈。

**可能追问：哪些是你独立完成，哪些是团队已有能力？**

### 建议回答
我会把“我直接实现的前端页面/组件和重构”与“团队已有的后端服务或协议实现”区分开。比如文件树虚拟化、表单组件、页面级 Store 和 UI 状态是我可以直接讲实现细节的部分；MCP 的 OAuth、Token 存储和撤销涉及服务层与数据库，我可以根据源码说明整体链路及前端如何联调，但不会把全部后端能力都说成是我一个人从零完成。

### Q：请用 90 秒讲一下你在 Daedalus 中最有挑战的一项工作。
### 建议回答
我会讲仓库文件树虚拟化。原始问题是树节点数量达到 500+ 后，如果递归把整个展开树都渲染成 DOM，展开、滚动和状态变化都会带来不必要的渲染压力。我的方案不是直接把树组件换成虚拟列表，而是先维护目录展==开路径集合==，再用显式栈把当前可见节点==扁平化成带 depth== 的数组。TanStack Virtual 只根据这个数组创建视口附近的行，容器高度用 totalSize 占位，每一行使用 absolute positioning 和 virtualRow.start 定位。节点 key 使用路径，overscan 设置为 12，估算行高为 26。仓库或分支切换时，我还用 ==tree identity 隔离旧的展开状态==，避免用户切换项目后复用错误的展开路径。这个方案的核心收益是减少同时挂载的 DOM 数量，同时保留树的层级、展开和键盘/无障碍语义；但我不会在没有基准数据的情况下宣称具体 FPS 或倍数提升。

---
## 产品和领域模型：面试官先判断你是否真的理解业务
### Q：Crate、Archetype、Anatomy、Dictionary 分别解决什么问题？
### 建议回答
可以把它们理解为不同维度的治理元数据：
- **Crate**：描述代码组织或代码包相关的归属、路径、仓库等信息。
- **Archetype**：描述设计或实现上的契约/模式。
- **Anatomy**：描述项目目录和文件结构应该长什么样。
- **Dictionary**：沉淀项目中的术语和命名语义，帮助统一理解。

它们不是互相替代的对象。Anatomy 更接近“结构校验”，Archetype 更接近“设计契约”，Dictionary 解决“术语一致性”，Crate 则承载代码组织维度。它们最终会服务于 CLI 校验、扫描和 Finding。

### Q：Anatomy 和普通的文件树有什么区别？
### 建议回答
普通文件树描述的是“当前有哪些文件”；Anatomy 描述的是“==允许或期望==有哪些文件，以及==层级、数量、命名==和==可选性==规则”。例如一个节点可能是 literal 固定名称，也可能是 placeholder 动态名称；子节点可以有 `one_of`、`exactly_one`、`one_or_more`、`zero_or_more` 等数量或选择策略。CLI 扫描真实目录后，会把实际树与 definition 对比，产出 missing_required、unexpected_entry、name_mismatch、nesting_mismatch、quantity_exceeded 等问题。

---
## 简历逐条深挖
### Q：你为什么要做 500+ 节点文件树虚拟化？
### 建议回答
问题不只是节点数量 500+，而是树组件会随着展开状态变化，递归渲染所有可见后代；如果用户展开多个目录，DOM 节点数、布局计算和 React reconciliation 成本会同时增加。虚拟列表的思路是把“逻辑上可见的树节点”与“实际挂载的 DOM 行”分离：前者仍然完整计算，后者只挂载视口附近的一小段。这样不会破坏树的展开语义，又能控制 DOM 规模。

**可能追问：500 个节点真的需要虚拟化吗？**

### 追问回答要点
- 500 个节点本身未必一定需要，实际压力取决于展开比例、每行复杂度和交互频率。
- 这里的价值在于为更大仓库和深层展开留出增长空间，同时降低全量 DOM 的上限。
- 正确做法应配合基准测试比较节点数、渲染耗时、滚动响应和内存，而不是只看节点数量。
- 当前源码能证明采用了虚拟化结构，但没有足够数据支持具体性能数字。

### Q：你在简历中说“扁平化可见节点”，具体怎么做？
### 建议回答
输入是嵌套的 `ProjectFileTreeNode[]` 和 `expandedPaths: Set<string>`，输出是 `{ depth, node }[]`。我会从根节点开始遍历，使用==显式栈而不是递归==：根节点逆序入栈，出栈时按稳定顺序追加到结果；如果当前节点是目录并且它的 path 在 expandedPaths 中，再把 children 逆序压栈，并把 depth 加一。这样结果顺序保持和树的展示顺序一致，而且只展开需要展示的分支。

**可能追问：为什么根节点要逆序入栈？**

### 追问回答要点
栈是后进先出。如果希望最终结果按原数组顺序输出，就要把 children 从后往前入栈，最前面的节点才会最先出栈。这个技巧可以保留迭代遍历的低调用栈风险和明确的顺序控制。

### Q：为什么不用递归扁平化？
### 建议回答
递归写法更直观，但仓库目录深度不完全可控；显式栈可以避免极深目录导致调用栈风险，也更容易在遍历过程中控制展开条件、顺序和深度。这里的重点不是“递归一定错误”，而是文件系统这种外部输入深度不可预期，迭代方。

### Q：TanStack Virtual 具体配置了什么？
### 建议回答
核心配置包括：`count: visibleNodes.length`、`estimateSize: () => 26`、`getScrollElement: () => scrollRef.current`、`overscan: 12`、`getItemKey` 优先使用节点 path，并且设置 `useFlushSync: false`。外层内容高度使用 `virtualizer.getTotalSize()`，每行用 `virtualRow.start` 进行绝对定位。这样虚拟器只负责可视窗口和位置计算，树的展开逻辑仍由业务代码维护。

### Q：overscan 是什么？为什么设置为 12？
### 建议回答
overScan 是在视口上下==额外预渲染的行数==。它可以避免用户==快速滚动==时视口边缘频繁卸载/挂载造成==白屏或闪烁==，但数值越大，实际 DOM 数量也越多。当前代码使用 12，这是一个==工程折中值==；如果要严谨调参，应根据行高、滚动速度、设备性能和长列表基准测试调整，不能把 12 说成通用最优值。

### Q：固定行高和动态行高有什么取舍？
### 建议回答
当前文件树行高使用估算值 26，适合每行结构统一、没有多行文本的场景，优点是测量简单、滚动位置稳定、虚拟化开销低。如果未来节点名称可能==换行==、==行内出现错误提示==或操作面板，就需要动态测量，代价是测量和重新计算更复杂，也要处理滚动锚点变化。这里固定高度是符合当前 UI 约束的选择。

### Q：为什么 key 使用 path？path 一定稳定吗？
### 建议回答
在==同一个仓库==分支的文件树中，path 能作为节点的自然身份，适合作为 key 和展开状态索引。为了避免跨仓库或跨分支复用相同 path，我还把 ==owner、repo、branch== 组成 `treeIdentity`，在树身份变化时隔离并重置展开状态。若未来存在重命名或 path 不唯一的场景，就需要后端稳定 ID，不能继续假设 path 永远唯一。

### Q：切换仓库或分支时，为什么要处理展开状态？
### 建议回答
展开状态是针对一棵具体树的 UI 状态。若从仓库 A 切到仓库 B，仍然复用 A 的 expandedPaths，可能出现 B 中不存在的路径被保留，或者碰巧同名路径错误展开。实现中通过 `JSON.stringify([owner, repo, branch])` 形成 tree identity，并在身份变化时重置滚动位置、reconcile 展开路径，只保留新树中仍然有效的目录路径。

### Q：reconcileTreeExpansion 解决什么问题？
### 建议回答
它把旧的展开路径集合和新加载的树做一次对齐，清理已经不存在的路径，避免状态集合持续积累。它也能保证展开状态只作用于目录节点，而不是文件或旧仓库中的残留路径。这个过程本质上是“外部数据变化后，对本地 UI 状态做一致性修复”。

### Q：虚拟化后如何保证树的缩进和可访问性？
### 建议回答
扁平化结果保留 depth，渲染行时根据 depth 计算缩进；容器使用 `role="tree"`，加载时使用 `aria-busy`，行组件需要继续保持树节点语义和展开状态表达。虚拟化只改变 DOM 挂载策略，不应改变用户看到的层级关系。真正完整的键盘导航、`aria-level`、`aria-expanded` 等细节要结合当前组件源码确认，面试时只承诺源码中确实存在的部分。

### Q：虚拟列表会不会影响搜索、定位和浏览器查找？
### 建议回答
会有影响，因为未进入视口的节点不在 DOM 中。搜索应基于==完整的树数据==或==服务端搜索==，而不是只查 DOM；定位到节点时，需要先计算或==更新展开路径==，再调用 virtualizer 的 scrollToIndex/scrollToOffset，让目标节点进入视口。浏览器原生查找只能找到已挂载内容，这是虚拟化的常见取舍。

### Q：如果文件树出现滚动跳动，你怎么排查？
### 追问回答要点
1. 检查==估算行高==是否与==真实行高==一致，尤其是字体、边框、折行变化。
2. 检查 ==key 是否稳定==，不能因为 index 改变导致行身份错乱。
3. 检查==展开/收起==时是否同步更新 visibleNodes 和 totalSize。
4. 检查数据刷新是否替换了节点对象，导致测量缓存失效。
5. 检查滚动容器是否真正传给 `getScrollElement`。
6. 用 React Profiler、浏览器 Performance 和不同展开规模做对比，而不是凭感觉判断。

---
## Crate 动态表单深挖
### Q：为什么用 React Hook Form，而不是多个 useState？
### 建议回答
Crate 表单包含普通字段、受控 UI 字段和动态 paths 数组。多个 useState 会让字段值、错误、提交状态、动态数组增删和重置==逻辑分散==；React Hook Form 能集中管理表单控制器，配合 FormProvider 让深层字段通过 useFormContext 读取同一个 control，再通过 Zod resolver 使用==共享 Schema 校验==。它减少了表单状态散落，也更适合新增/编辑共用字段结构。

### Q：useFieldArray 解决了什么问题？
### 建议回答
`paths` 是动态数组，用户可能新增、删除、调整多条路径。`useFieldArray` 提供稳定的 field id 和数组操作方法，避免手动用 useState 拼接数组时出现 key 不稳定、注册字段错位、删除后错误信息对应错误等问题。渲染时使用 `field.id` 作为 React key，而不是数组 index。

### Q：为什么不能用 index 作为动态列表 key？
### 建议回答
删除中间项或插入新项后，index 会变化，React 可能复用错误的 DOM 和输入状态，导致用户看到的值、错误信息或焦点归属错位。
这里的具体问题是因为fiber的identity是 type + key
`useFieldArray` 提供的 `field.id` 是该数组项在表单生命周期内的稳定身份，更适合 key。

### Q：FormProvider 和 useFormContext 是怎么减少 Props Drilling 的？
### 建议回答
创建表单的容器拿到 `control`、`register`、`formState`、`handleSubmit` 等对象后，通过 `FormProvider` 放到 React Context。下层字段组件用 `useFormContext<CrateFormValues>()` 获取同一套 API，不需要从 Dialog 一层层传递。这样字段组件可以独立测试和复用，但仍然共享一个表单控制器。它解决的是“表单依赖传递”，不是把所有业务状态都塞进 Context。

### Q：register 和 Controller 有什么区别？
### 建议回答
`register` 更适合原生 input/select 等可以通过 ref 和标准事件接入的非受控字段；`Controller` 适合 Radix/shadcn 这类受控组件，负责把 value、onChange、onBlur 和 ref 等表单能力桥接给组件。使用 Controller 时要确认组件的 change 签名、空值约定和 ref 转发是否匹配，否则会出现界面变了但表单值没更新的问题。

### Q：useWatch 在 Crate 表单中有什么作用？
### 建议回答
代码中通过 `useWatch({ control, name: "repositoryId" })` 订阅 repositoryId。当仓库选择变化时，相关字段可以根据当前值展示、联动或触发校验，而不需要让整个表单组件因任意字段变化都重新执行。它比直接读取某个闭包里的初始值更可靠，也能把订阅粒度限制在需要的字段。

### Q：Zod 校验放前端有什么意义？后端还需要校验吗？
### 建议回答
前端校验解决即时反馈和减少无效提交，后端校验解决安全边界和数据一致性。当前通过 `zodResolver(CrateFormValuesSchema)` 让表单使用共享 Schema，提交前可以得到结构化错误；但任何来自浏览器的输入都不可信，tRPC input 和 Service 层仍要再次校验业务规则、权限和关联对象是否存在。前端 Schema 不能替代后端授权。

### Q：新增和编辑为什么共用字段组件，但分开 form control？
### 建议回答
字段布局和字段级交互相同，所以抽出共享 Fields 可以避免新增/编辑两份 JSX 漂移；但创建和编辑的默认值、提交 mutation、关闭重置和生命周期不同，应该各自持有自己的 form control。编辑时通过 `reset(createCrateFormValues(editingCrate))` 回填，创建时使用空白默认值。这样复用 UI，不混淆状态和提交语义。

### Q：为什么需要 createCrateFormValues？直接把服务端对象传给 reset 不行吗？
### 建议回答
转换函数把服务端模型映射成表单模型，并明确复制 `archetypeIds`、`paths` 及其中对象，避免表单编辑过程中直接修改服务端查询结果的引用。它也是领域模型和 UI 表单模型之间的边界，未来后端字段变化时只需要集中调整映射，不让字段组件感知数据库结构。

### Q：表单提交时如何避免重复提交和旧数据覆盖？
### 追问回答要点
- 使用 `formState.isSubmitting` 或 mutation loading 状态禁用提交按钮。
- 成功后再关闭 Dialog、刷新列表和详情，避免用户看到未落库的数据。
- 编辑时以当前记录 ID 为目标，不能从过期闭包里读取旧的 editingCrate。
- 关闭/切换记录时调用 reset，清理错误和脏状态。
- 如果允许快速切换编辑对象，要确保 reset 与对象身份同步，必要时取消或忽略过期请求结果。

### Q：如果点击提交没有任何反应，你怎么排查？
### 追问回答要点
1. 看 `handleSubmit` 是否真正包裹了 submit handler。
2. 看 Zod resolver 是否在提交前拦截，并检查 `formState.errors`。
3. 检查 Controller 的 `name`、value 和 onChange 是否正确绑定。
4. 检查动态 field 的路径名是否和 Schema 对齐。
5. 检查 mutation 是否触发、网络响应和 tRPC 错误。
6. 检查权限错误是否被统一错误适配器转成了用户可见提示。

---
## Context + Zustand 页面级 Store
### Q：Context 和 Zustand 各自解决什么问题？
### 建议回答
Context 负责把“当前页面这一实例的 Store”提供给页面子树，避免手动逐层传递 Store；Zustand 负责==存储状态==、==action== 和订阅机制。Context 是实例注入边界，Zustand 是状态管理和更新机制。两者结合后，页面可以拥有独立 Store，测试时也能创建独立实例，不会把页面状态污染到全局。

### Q：为什么是页面级 Store，而不是全局 Store？
### 建议回答
RepositoriesPage、McpSetupPage 等状态主要服务于单个页面的交互流程，例如导入状态、校验、授权跳转和表单步骤。做成==全局 Store== 会扩大状态生命周期和依赖范围，==页面离开后还可能残留状态==。页面级 Store 更符合状态归属，卸载页面时自然释放；真正跨页面共享的认证、主题等状态才更适合放全局。

### Q：selector 为什么能减少重渲染？
### 建议回答
组件使用 `useStore(pageStore, state => state.someField)` ==只订阅自己需要的字段或 action==。Store 中其他字段变化时，selector 结果不变，组件就==不需要重新渲染==。若一次性返回整个 state 对象，就会让==订阅范围变大==；复杂 selector 还要注意返回对象的引用稳定性，必要时使用 shallow 比较或拆成更细的 selector。

### Q：Slice 为什么有价值？
### 建议回答
Slice 把页面状态和 action 按职责组织，而不是把所有逻辑塞进一个巨大 create 函数。它有三个价值：一是提高==可读性==，二是让不同交互域可以==独立测试==，三是未来扩展页面流程时减少互相耦合。Slice 不是为了机械拆文件，边界应该围绕页面业务能力划分。

### Q：dependencies 显式注入带来了什么？
### 建议回答
Repositories Store 的 dependencies 中包含 createRepository、validateRepository、linkGitHubAccount、navigateToRepository、redirectToAuthorization、translate、invalidateRepositories 等能力。Store action 不直接 import 具体实现，而是依赖接口/函数参数。测试时可以注入 fake implementation，验证“校验失败不创建、创建成功后跳转、授权失败给出正确状态”等行为，不需要启动完整路由、网络和翻译环境。

### Q：Zustand、Refine/React Query、React Hook Form 的状态边界怎么划分？
### 建议回答
- **Refine/React Query**：服务端状态，例如列表、详情、缓存、请求中、错误和失效刷新。
- **React Hook Form**：表单草稿、字段错误、脏状态、动态字段。
- **Zustand**：页面流程状态和跨多个组件共享的 UI action，例如导入步骤、校验中、创建中、连接中。
- **组件局部 state**：只影响一个组件的短生命周期状态，如局部展开或 hover。

把服务端数据复制到 Zustand 通常会产生双份真相；把每个表单字段都放 Store 又会让表单和页面流程耦合。

### Q：ImportFlowStatus 为什么设计成idle/validating/creating/connecting？
### 建议回答
这是把异步导入流程显式建模成有限状态，而不是用多个 boolean 组合。多个 boolean 容易出现 `isValidating` 和 `isCreating` 同时为 true 这类非法组合；字符串状态能表达当前阶段，UI 可以据此显示 loading、禁用按钮和错误恢复。后续如果要支持失败、重试或取消，可以继续扩展状态模型，或把错误信息作为独立字段。

### Q：Store 的异步 action 如何防止竞态？
### 追问回答要点
- 给每次流程一个 request/operation identity，旧请求完成时先判断是否仍然是当前操作。
- 开始新流程前清理旧错误和旧结果。
- 在 action 内读取最新 state，避免只依赖创建时捕获的闭包值。
- 提交期间禁用重复触发；如果底层支持，取消过期请求。
- 导航或卸载后不要再写入已经失效页面的状态。

### Q：如何测试页面级 Store？
### 建议回答
单元测试直接创建 Store，注入 fake dependencies，然后调用 action 并断言状态变化和依赖调用。例如：校验失败时状态回到 idle 且不调用 createRepository；创建成功时状态经历 validating/creating 并调用 invalidateRepositories 和 navigateToRepository；授权异常时进入可恢复的错误状态。测试重点是业务转移和副作用边界，不是测试 Zustand 本身。

---
## Refine → tRPC → Service → DAO/Repository 分层
### Q：为什么 UI 不直接调用 tRPC，而要经过 Refine dataProvider？
### 建议回答
Refine dataProvider 是前端==数据访问==的==统一适配层==。列表、详情、创建、更新、删除等页面都可以通过 Refine hooks 表达，缓存失效、loading、error 和资源命名也能统一管理；tRPC 只作为传输和类型安全的后端入口。这样页面不需要知道具体 procedure 名称和调用细节，未来替换接口实现或统一处理错误时，影响面更小。

### Q：dataProvider 做了什么？
### 建议回答
它把 Refine 的通用方法==映射==到项目的 tRPC client，例如 getList、getOne、create、update、deleteOne 等，再把参数转换成对应 procedure 的 input。它还参与 query key、分页/过滤参数和失效策略的统一。页面只使用 `useList`、`useOne` 等 Refine hooks，并用 query 状态驱动 LoadingState，而不是在 UI 里直接写 tRPC 调用。

### Q：tRPC procedure、Service、DAO、Repository 的职责如何区分？
### 建议回答
- **tRPC procedure**：接收请求，做认证和输入校验，调用 Service，统一解包 Result 并转换错误。
- **Service**：承载业务规则、权限组合和视图编排；通过依赖注入获取 DAO/Repository，返回 `neverthrow Result`。
- **DAO**：面向单表的数据库读写，按实体和 operation 共置。
- **Repository**：只有跨表写入需要事务一致性时使用，例如撤销一个 MCP connection 时同时处理 OAuth client、access token、refresh token、consent 和 connection 状态。
- **Drizzle/DB**：负责 ORM 和数据库连接，不应该被 UI 或 Service 随意直接构造查询。

### Q：为什么 Service 返回 neverthrow Result，而不是到处 throw？
### 建议回答
Result 把成功和失败变成显式类型，调用方必须处理错误分支，适合跨 Service、tRPC 和异步数据库操作传递业务错误。它也能把“预期失败”与真正的程序异常区分开，例如权限不足、记录不存在、Token 过期属于可预期业务失败；tRPC 层再通过统一错误适配器转换成客户端可理解的错误。这样比到处 try/catch 和隐式 throw 更容易追踪控制流。

### Q：为什么项目约束 Service/DAO 不使用原生 try-catch？
### 建议回答
这是为了统一错误处理模型。原生 try-catch 容易在不同层被重复捕获、吞掉或转换成不一致的错误；neverthrow 的 Result/ResultAsync 可以组合异步步骤，并保留错误类型。并不是说异常永远不需要捕获，而是应该在边界层有明确的适配策略，而不是每个方法随意捕获和重新 throw。

### Q：DAO 和 Repository 什么时候会混用？
### 建议回答
读取和单表操作优先 DAO；需要多个表在同一事务内更新时使用 Repository。以 MCP revoke 为例，如果先单独禁用 OAuth client，再删除 token，中间失败可能留下半完成状态，所以应在一个 Repository operation 中使用同一事务。不要为了“复用”把所有读取也塞进 Repository，否则会模糊职责。

### Q：前端如何处理请求 loading 和失效刷新？
### 建议回答
页面通过 Refine query/mutation 的状态驱动 LoadingState、按钮禁用和错误提示；mutation 成功后让 dataProvider/Refine 对相关 list/detail query 做 invalidate，而不是在组件中手动维护第二份服务端数据。对于创建/编辑 Dialog，关闭和刷新要放在成功分支，避免请求失败时误关闭并丢失用户输入。

### Q：如果服务端返回“创建成功但页面没更新”，怎么排查？
### 追问回答要点
1. 查看 mutation 是否真的成功，是否只是前端乐观更新被回滚。
2. 检查 invalidate 的资源名、query key、scope 是否和列表/详情一致。
3. 检查列表查询是否有过滤条件或分页导致新数据不在当前页。
4. 检查服务端事务是否提交、读写连接是否一致。
5. 检查表单是否仍然显示旧的本地对象引用。
6. 用网络面板和 React Query Devtools 确认请求、缓存和重新请求过程。

### Q：类型安全具体体现在哪里？
### 建议回答
tRPC 可以让 procedure 的输入和输出在客户端获得类型；Zod Schema 是运行时数据契约，TypeScript 类型从 Schema 推导，避免手写接口漂移；Refine dataProvider 再把资源操作统一到这些类型上。类型安全不是“编译通过就一定安全”，来自网络、数据库和用户输入的数据仍需要运行时校验。

### Q：如果面试官质疑分层导致代码冗余，你如何回应？
### 建议回答
分层确实会增加文件和适配代码，但这里平台包含多种入口：Web UI、CLI、MCP/Agent，且有权限、事务、审计等复杂业务。将 tRPC 传输、Service 业务、DAO 数据访问和 Repository 事务拆开后，新增入口可以复用 Service，数据库细节也不会泄漏到 UI。对于简单只读场景可以保持轻量，但一旦存在跨入口复用和事务边界，分层的维护收益会超过初始冗余。

---
## MCP：连接、鉴权、调用和撤销
> MCP 这一章是最容易被追问的地方。回答时要把“协议请求如何进来”“用户是谁”“连接能否使用”“操作是否有审计”四件事分开。
### Q：你们为什么要接入 MCP？
### 建议回答
目的是让 Codex、Claude Code、OpenCode 等 Coding Agent 能在受控边界内读取 Daedalus 的治理上下文、发起扫描、查看 Run/Trace/Finding，必要时创建或更新治理数据。与其让 Agent 通过浏览器模拟点击，不如提供结构化协议入口，再结合 workspace 隔离、权限校验、Token 撤销、写操作确认和调用记录，降低自动化接入成本并保留可控性。

### Q：一次 MCP 请求的大致流程是什么？
### 建议回答
请求先进入 MCP API route，由 request handler 读取 connectionId 和 Authorization。Authorization 可能走 OAuth JWT，也可能走 `Bearer` API Token。完成身份和 connection 权限校验后，进入统一的 MCP protocol handler。协议响应如果是 HTTP 400 以上，会记录 protocol failure；前端可以通过连接状态和调用记录看到失败或恢复情况。

```text
HTTP request
  → 读取 connectionId / Authorization
  → OAuth JWT 或 API Token 鉴权
  → 校验 connection、workspace、owner、状态和过期时间
  → MCP protocol handler
  → 记录 outcome / duration / error
  → 返回协议响应
```

### Q：OAuth JWT 和 API Token 两种鉴权有什么区别？
### 建议回答
OAuth JWT 通常由==授权服务器签发==，服务端根据 JWT 中的 `sub`、`azp` 或 `client_id` 等信息识别主体，并结合 OAuth client/consent 检查授权关系。API Token 是 Daedalus 为连接签发的长期凭证，客户端通过 `Authorization: Bearer xxx` 传递；服务端不保存明文，而是对 Token 做 SHA-256 hash 后查表，再验证连接归属、状态、过期和撤销时间。OAuth 更适合标准授权流程，API Token 更适合无浏览器的远程 Agent，但泄露风险需要靠只显示一次、TTL 和撤销控制。

### Q：为什么 API Token 不直接明文存数据库？
### 建议回答
数据库只保存 hash、末四位、创建时间、过期时间、撤销时间和最后使用时间。请求到来时对输入 Token 做同样的 SHA-256 hash，再查 hash。这样即使数据库只读泄露，攻击者也不能直接拿存储值当 Bearer 凭证使用。明文 Token 只在签发成功时返回一次，详情页不再显示。

### Q：Token 是怎么生成的？
### 建议回答
源码中使用 `randomBytes(32)` 生成随机字节，拼接 `dld_` 前缀作为用户可识别的 Token 形态，再对完整 Token 做 SHA-256 hash 保存。前缀便于识别凭证类型，随机字节提供不可预测性；TTL 当前约为 90 天。面试时不要把前缀、TTL 说成协议标准，它们是项目实现选择。

### Q：只保存 hash 以后，怎么验证 Token？
### 建议回答
服务端从 Authorization header 取出 Bearer Token，按与签发时完全一致的规范计算 hash，用 hash 查找 token 记录。找到后继续验证 token 是否属于请求 connection、是否被撤销、是否过期，以及 connection 状态和 owner 当前 workspace 权限。只查到 hash 不代表请求一定有权限。

### Q：为什么还要检查 owner 的 workspace 权限？Token 不已经代表连接了吗？
### 建议回答
Token 代表的是一条==连接凭证==，不应绕过当前的资源授权。如果用户已经离开 workspace、workspace 被归档，或者 connection 被标记 unavailable，原来签发的 Token 也应该失效。源码中会检查 connectionId 与 token 的匹配，并再次检查 owner 对 workspace 的当前访问权限，这样可以降低离职、移除成员或资源状态变化后的残留访问风险。

### Q：connection revoked 和 unavailable 有什么区别？
### 建议回答
`revoked` 通常表示用户主动撤销或明确关闭连接，是终态倾向更强的状态；`unavailable` 更像当前依赖条件不可用，例如 workspace archived 或 owner membership 丢失，未来条件恢复后是否允许 recheck 要看业务定义。两者都不应继续正常处理请求，但 UI 上应区分“主动撤销”和“需要重新检查/恢复”的反馈。

### Q：revoke 一个 MCP connection 为什么需要事务？
### 建议回答
撤销不是只改一列状态。它还要 disable OAuth client、删除 access tokens、撤销 refresh tokens、删除 consents，并更新 connection status。如果这些操作分开提交，中途失败会出现“页面显示 revoked，但旧 refresh token 仍可用”或“客户端禁用了但连接记录没更新”的不一致。Repository 将相关跨表写入放在一个事务里，要么整体成功，要么整体回滚。

### Q：OAuth metadata 有哪些作用？
### 建议回答
服务暴露 authorization server metadata 和 protected resource metadata，让支持 OAuth discovery 的客户端知道授权服务器、受保护资源、支持的 scope 和 bearer 传输方式。当前 scope 是 `mcp:connect`，bearer method 是 header，资源文档指向 `/mcp/setup`。metadata 还设置了短时间 Cache-Control，避免客户端长期缓存过期配置。

### Q：GET、POST、DELETE 的 MCP route 为什么要区别处理？
### 建议回答
源码中 GET 无 Authorization 时返回 401，并通过 `WWW-Authenticate` 指向 metadata，让客户端知道需要授权；GET 有 Authorization 时返回 405，提示使用 POST/DELETE。POST 和 DELETE 才进入 MCP handler。这个设计把 discovery/认证挑战、方法限制和实际协议操作分开，避免任意 HTTP 方法都执行协议逻辑。

### Q：为什么当前不支持 server-initiated SSE？
### 建议回答
SSE 会引入长连接生命周期、断线重连、连接状态同步和资源释放等复杂度。如果当前产品主要需求是 Agent 发起请求并得到响应，那么先支持 request/response 能降低实现复杂度。面试中可以补充：如果未来需要 server push，应明确连接模型、心跳、重连、背压、权限续期和部署环境对长连接的支持，而不是简单加一个 EventSource。

### Q：怎么防止 OAuth client 绑定多个 connection？
### 建议回答
服务层在创建或授权时检查 client 与 connection 的关系，不能让同一个 OAuth client 无边界地映射到多个 connection，否则主体、权限和撤销关系会变得不清晰。这个约束有助于把一次授权的生命周期绑定到明确的 Daedalus connection 上。

### Q：调用记录为什么不直接保存完整结果？
### 建议回答
调用记录目前保存 connectionId、workspaceId、durationMs、toolName、module、accessLevel、outcome、resultSummary、errorCode、errorMessage、createdAt 等字段，并有 connection + createdAt、workspace + createdAt 索引。完整 MCP 结果可能包含代码、Token 相关上下文或用户数据，默认保存安全摘要能满足审计和诊断，又减少敏感信息泄露和存储成本。若将来要存原始结果，应做脱敏、权限分级、保留期限和加密设计。

### Q：审计记录里的 durationMs 有什么用途？
### 建议回答
它既能帮助排查慢请求，也能按工具、模块、workspace 观察耗时分布。分析时不能只看平均值，还应看 P95/P99、失败请求和调用量；如果要做性能告警，还需要明确采样、时钟来源和异步记录是否影响主请求。当前源码证明有耗时字段和索引，但不应直接声称已经建立完整监控体系。

### Q：MCP 前端页面需要展示哪些状态？
### 建议回答
连接管理页面至少要区分加载中、授权中、已连接、失败、撤销、重定向和不可用等状态；操作按钮应根据状态和权限决定是否可用。前端不应只用一个 boolean `isConnected`，否则无法解释“正在授权”和“已经撤销”的差异。失败状态要展示可恢复动作，例如重试、重新授权或重新检查，但不泄漏 Token 明文。

### Q：如果用户重复点击“授权”或“撤销”，你怎么处理？
### 追问回答要点
- action 开始后禁用同一操作按钮，并显示进行中状态。
- 请求带有当前 connection identity，避免旧请求完成后覆盖新连接状态。
- 撤销应具备幂等语义；重复撤销最终应保持 revoked，而不是产生不可预测错误。
- 前端成功后刷新 connection detail/list 和 invocation records。
- 对重定向授权流程要防止重复打开窗口或重复消费 callback。

### Q：如何发现 Token 泄露？
### 建议回答
可以利用最后使用时间、异常 workspace/connection 访问、失败次数、IP/设备等运行信息做风险检测，但当前源码中能确认的主要是最后使用时间、调用记录和撤销能力。若要扩展，应增加异常检测、主动轮换、单 Token 限流、短 TTL 或绑定 scope，并明确误报处理。不能把“保存 hash”说成已经解决所有泄露风险，因为 Token 在客户端配置、日志、终端历史里仍可能暴露。

### Q：MCP 写操作如何保证安全？
### 建议回答
至少要有认证、workspace/owner 授权、connection 状态检查、输入 Schema 校验、写操作确认或高风险操作限制、审计记录和撤销能力。前端负责把状态和确认流程表达清楚，真正的权限判定必须在服务端执行，不能依赖按钮是否显示。对创建/更新治理数据还应考虑幂等、并发覆盖和最小权限。

---
## 九、Anatomy 独立包和 CLI
### Q：为什么要把 Anatomy 抽成独立包？
### 建议回答
Anatomy 的核心价值是对“definition 与实际文件树是否一致”做校验，这个能力不应该只存在于某个 React 页面。抽成独立包后，Web 页面、CLI、未来的 CI 或其他工具都能复用同一套 tree、policy 和 validation 逻辑，避免前端一套、CLI 一套导致规则漂移。独立包还迫使核心逻辑不依赖浏览器和 UI，更容易做纯函数测试。

### Q：Anatomy CLI 的完整执行流程是什么？
### 建议回答
1. 解析命令行参数。
2. 读取 JSON definition。
3. 用 `anatomyDraftInputSchema` 做运行时校验。
4. 递归读取目标目录并构造文件树。
5. 对目录项排序，保证输出稳定。
6. 忽略 `.git`、`.next`、`.output`、`.turbo`、build、coverage、dist、node_modules 等目录，并跳过符号链接。
7. 调用独立包的 `checkAnatomy`。
8. 输出 human-readable 或 JSON 结果。
9. 使用退出码区分通过、规则阻断和工具错误。

### Q：CLI 为什么要区分退出码 0、1、2？
### 建议回答
- `0`：检查通过，可以继续后续流程。
- `1`：工具正常执行，但项目结构违反规则并产生 BLOCK，适合让 CI 明确判定校验失败。
- `2`：definition 无效、文件读取失败或工具运行异常，属于“检查本身没能可靠完成”。

如果只用 0/1，就无法区分“代码不符合规则”和“校验器坏了/输入坏了”，CI 的错误定位会很差。

### Q：为什么扫描目录时要排序？
### 建议回答
文件系统返回目录项的顺序不一定稳定。排序后，相同输入可以得到稳定的 tree 和错误输出，便于测试快照、日志对比和 CI 复现。确定性是 CLI 工具很重要的工程属性。

### Q：为什么跳过符号链接？
### 建议回答
符号链接可能指向目标目录外部，也可能形成循环。如果直接递归，会有越界扫描、重复扫描或无限循环风险。当前选择跳过符号链接是安全和可预测性优先的方案。若未来必须支持，需要做 realpath、根目录边界、visited inode/path 集合和循环检测。

### Q：为什么要有默认 ignore 列表？用户能否配置？
### 建议回答
`.git`、node_modules、dist、coverage 等目录通常是工具元数据、依赖或构建产物，不属于需要治理的业务源码，扫描它们会增加时间和噪声。默认 ignore 提供合理开箱体验；如果产品需要扩展，应允许用户在安全边界内追加或覆盖，但要处理路径规范化、通配符和跨平台分隔符。

### Q：Anatomy 可以检查哪些类型的问题？
### 建议回答
当前校验会涉及 definition 发布前合法性、重复 literal 名称、ID 合法性、one_of 范围，以及实际树中的 `missing_required`、`unexpected_entry`、`name_mismatch`、`nesting_mismatch`、`quantity_exceeded`、`one_of_mismatch` 等。节点数量策略包括 optional、exactly_one、one_or_more、zero_or_more，名称既可以是 literal，也可以是 placeholder。

### Q：literal name 和 placeholder name 有什么区别？
### 建议回答
literal name 要求实际节点使用固定名称，例如必须存在 `src`；placeholder 表示一类满足规则的动态名称，例如任意 feature 目录。literal 更严格，placeholder 更灵活。校验器需要先明确匹配优先级，避免一个节点同时被多个 placeholder 或 literal 重复消费。

### Q：one_of 和数量策略如何理解？
### 建议回答
数量策略描述某个定义节点允许出现多少次，例如 exactly_one 必须恰好一次、one_or_more 至少一次、zero_or_more 任意次数、optional 可以不存在。one_of 描述多个候选中允许或要求匹配某一个/某一组。实现时关键是避免贪心匹配导致后面的定义无法命中，并能给出可解释的错误，而不只是返回 false。

### Q：policy inheritance 和 override 为什么容易出错？
### 建议回答
父节点 policy 可能向下继承，子节点又允许局部 override。如果直接修改同一个 policy 对象，会让兄弟节点互相污染；更安全的做法是每个节点基于父 policy 生成新的有效 policy，再合并当前 override。测试要覆盖多层继承、局部覆盖、兄弟隔离和默认值。

### Q：发布前为什么还要 validate-anatomy-for-publish？
### 建议回答
编辑态可以允许临时不完整，方便用户逐步构建 definition；发布态必须保证 ID、引用、策略和结构完整，否则 CLI 消费后会得到无法解释的结果。发布前校验是把“可保存草稿”和“可作为治理契约使用”分开，类似 CMS 的 draft/publish 生命周期。

### Q：Anatomy 如何接入 CI？
### 建议回答
理论链路是 CI 拉取或读取 versioned definition，执行 anatomy-cli 扫描仓库，使用 JSON 输出生成机器可读结果，并根据退出码决定阻断或继续。需要固定 CLI 版本、definition 版本和 ignore 配置，避免本地与 CI 结果不一致。当前我可以确认核心包和 CLI 已具备这些能力，但是否所有仓库都已完成 hook/CI 接入要以实际配置为准。

### Q：CLI 如何保证跨平台？
### 追问回答要点
- 使用 path API 处理 Windows/POSIX 分隔符，不手写字符串拼接。
- 对输出中的路径格式做统一规范化。
- 避免依赖 shell 特有语法。
- 符号链接和权限错误要有平台差异测试。
- JSON 输出应独立于终端颜色和本地语言。
- Bun runtime 和打包/分发方式也需要在目标平台实际验证。

---
## 十、Monorepo、Bun 与工程架构
### Q：项目为什么使用 Monorepo？
### 建议回答
Daedalus 同时有 ==Web app==、==Hono server==、==anatomy-cli==，以及 schemas、services、models、ui、anatomy 等共享包。Monorepo 能让共享 Schema、UI 组件、类型和核心校验逻辑在同一仓库演进，配合 workspace 依赖和统一质量命令，减少跨仓库版本不同步。代价是==构建图、边界约束==和 ==CI 缓存更复杂==，所以需要清晰的包职责和依赖方向。

### Q：有哪些主要应用和包？
### 建议回答
应用包括 React/TanStack Start 主应用、Hono REST server、Bun anatomy-cli。核心包包括 `anatomy`、`db`、`db-schema`、`models`、`services`、`schemas`、`ui`、`shared`、`agent` 以及共享 TypeScript/oxlint/formatter 配置。回答时不需要背全部数量，重点是说明应用层和可复用包层分开。

### Q：为什么 Bun 和 Turborepo 一起用？
### 建议回答
Bun 负责 workspace 包管理、脚本运行和部分应用 runtime，Turborepo 负责跨包任务编排、依赖图和缓存。两者不是重复关系：Bun 更接近包管理器/运行时，Turbo 更接近 Monorepo task orchestrator。使用时要确保 lockfile、CI runtime 和本地版本一致，并正确声明 build/test/typecheck 的输入输出。

### Q：Monorepo 最容易出现什么问题？
### 追问回答要点
- 包之间形成==循环==依赖。
- 深路径导入内部文件，破坏公共 API。
- barrel export 导致==意外导出==、循环依赖或 ==tree-shaking== 变差。
- 共享包==过度膨胀==，任何改动都使全仓重建。
- TypeScript project references 或 package exports 配置不一致。
- 测试环境和生产构建解析路径不同。
- workspace 版本漂移或隐式依赖未声明。

### Q：为什么 schemas 要按领域和单 Schema 文件组织？
### 建议回答
Zod v4 是运行时契约的单一来源，每个主 Schema 独立文件，并从 Schema 推导 TypeScript 类型。领域目录 index 只做 re-export，根 index 再公开统一 API，消费方从 `@repo/schemas` 导入。这样可以避免一个巨大 schema 文件互相耦合，也防止 UI 跨领域深路径引用内部实现。

### Q：barrel export 有什么风险？
### 建议回答
barrel 适合提供稳定公共 API，但不应在普通实现文件中层层 re-export，也要避免互相引用形成循环依赖。项目约束是领域目录 `index.ts` 和根 `index.ts` 只做导出聚合；实现文件应直接导入真正依赖。新增导出时要确认是否属于公共 API，而不是为了缩短路径把所有内部文件都暴露出去。

### Q：你怎么防止 UI、Service、Model 反向依赖？
### 建议回答
通过 package 边界、公开 exports、代码检查和 code review 保持依赖方向：UI 可以依赖 schemas 和 dataProvider，但不能依赖 db/models；Service 可以依赖 DAO/Repository 接口，不直接 import db；models/db-schema 不应反向依赖 app。必要时可以用 dependency-cruiser、eslint/oxlint 规则或自定义结构检查把约束自动化。

---
## 十一、Radix UI / shadcn/ui / Storybook
### Q：为什么不直接写原生 button、select、dialog？
### 建议回答
项目把跨应用复用的基础 UI 放在 `packages/ui/src`，基于 Radix UI / shadcn/ui 统一交互、样式、可访问性和主题。业务页面优先组合已有组件，避免在 `apps/app/src/components/ui` 再复制一套。这样可以集中修复焦点管理、键盘交互和样式一致性问题。

### Q：Radix UI 和 shadcn/ui 分别提供什么？
### 建议回答
Radix 更偏无样式、可访问性的交互 primitive，例如 Dialog、Select、Popover 的焦点和键盘语义；shadcn/ui 更像基于 primitive 的可复制组件实现和样式范式。项目实际使用时仍要封装自己的设计 token、variant、错误态和业务组合，不能把第三方组件当成完整设计系统。

### Q：业务组件和基础 UI 组件怎么划分？
### 建议回答
跨应用、与领域无关的 Button/Input/Dialog 放 `packages/ui`；App 内跨页面复用的领域组件放 `apps/app/src/components`；只服务某个页面或 Tab 的组件放对应 `pages/<PageName>` 目录。这样组件的复用范围与目录层级一致，避免把业务组件误放到基础 UI 包，导致 UI 包依赖领域模型。

### Q：Storybook 在项目中解决什么问题？
### 建议回答
Storybook 为组件提供==脱离完整应用==的==数据和路由环境==，可以展示==默认==、==loading==、==error==、==disabled==、==empty==、长文本等状态，也便于==视觉检查和交互验证==。它不能替代单元测试和 E2E；更准确地说，Storybook 是组件状态目录和人工/自动视觉验证入口。

### Q：如何设计一个可复用业务组件？
### 追问回答要点
- 先明确组件职责和复用范围，不把整个页面抽成万能组件。
- Props 表达业务意图，避免传大量底层样式开关。
- Store 中已经存在的数据和 action 优先由组件 selector 获取，减少重复 Props Drilling。
- loading/error/empty/disabled 状态必须可表达。
- 事件回调需要稳定语义，异步操作要有重复提交保护。
- 提供 test 和 stories，避免只验证 happy path。

### Q：为什么页面专用组件还要“一组件一目录”？
### 建议回答
项目约定一个页面组件单元包含 `ComponentName.tsx`、测试、Storybook 和只做 re-export 的 index。这样实现、验证和公开入口共置，组件变复杂时不用再重构目录；也能限制对内部 helper 的直接导入。代价是文件数量较多，所以只对真正独立的组件单元使用，不应把每个小函数都目录化。

---
## 十二、测试、质量与验证
### Q：项目有哪些测试和质量工具？
### 建议回答
主要有 TypeScript `tsc --noEmit`、oxlint、Vitest、Storybook、Playwright，以及根目录的 Turbo 任务。`bun run quality` 会组合类型检查、lint 和测试；`bun run knip` 用于发现未使用文件和依赖。不同层次测试的职责不同：纯函数/Store 用 Vitest，组件交互用 Testing Library/Storybook，关键用户链路用 Playwright。

### Q：文件树虚拟化应该怎么测试？
### 建议回答
至少分三层：

1. **纯函数测试**：不同 expandedPaths 下，扁平化顺序、depth、目录收起、空树和深层树是否正确。
2. **组件测试**：展开/收起、loading、空状态、仓库/分支切换、tree role 和滚动容器。
3. **性能/浏览器验证**：生成不同规模树，记录 DOM 数量、commit time、长任务和滚动响应。

当前测试更多能证明结构和关键配置存在，不应把它说成完整性能回归体系。

### Q：动态表单应该覆盖哪些测试？
### 追问回答要点
- 默认值和编辑回填。
- paths 新增、删除和中间项删除后的 key/错误归属。
- repositoryId 联动。
- Zod 必填、格式和数组规则。
- Controller 组件 value/onChange 桥接。
- 成功提交、服务端错误、重复提交禁用。
- Dialog 关闭后 reset，再打开其他记录不残留旧值。

### Q：Store 单测和组件测试如何取舍？
### 建议回答
业务状态转移和依赖调用优先做 Store 单测，速度快且错误定位明确；组件测试验证 selector 订阅、用户操作和 UI 反馈是否正确；E2E 只覆盖最关键流程。不要在组件测试中完整 mock 所有内部实现，也不要只测 Store 而完全忽略真实用户操作。

### Q：如果测试依赖源码字符串检查，有什么局限？
### 建议回答
源码结构测试可以防止关键配置被删除，例如 overscan 或使用路径 key，但它不能证明浏览器中的行为和性能。重命名、重构也可能在功能不变时让测试失败。更稳妥的是纯函数行为测试、DOM 交互测试和浏览器性能验证结合，源码结构检查只作为补充。

### Q：你如何评价测试覆盖率？
### 建议回答
覆盖率只能说明代码是否被执行，不能证明断言质量。平台型项目更应该关注风险覆盖：权限、事务、状态机、编辑回填、数据隔离、撤销和错误恢复。面试中不要只报一个覆盖率数字，而是能说明关键风险如何被验证。

---
## 性能、错误处理、无障碍与安全
### Q：除了虚拟列表，你还会从哪些方面优化大树？
### 追问回答要点
- 后端==按目录懒加载==，避免首次传输整个仓库树。
- 对 flatten 结果做合理 memoization，但先确认计算是否真是瓶颈。
- 搜索使用索引或==服务端接口==，不遍历 DOM。
- 限制行内复杂组件和昂贵图标。
- 目录展开时按需加载并缓存 children。
- 使用 ==startTransition== 处理非紧急的大规模展开更新，但要验证交互效果。
- 通过 React Profiler 和 Performance 先测量再优化。

### Q：useMemo 能解决所有性能问题吗？
### 建议回答
不能。useMemo 只缓存计算结果，依赖变化时仍会重算，也有比较和内存成本。如果瓶颈是大量 DOM、布局和 paint，useMemo 无法替代虚拟化；如果输入对象每次都换引用，memo 也可能无效。应该先确认瓶颈属于计算、渲染、网络还是布局，再选择方案。

### Q：React 19 下如何看待并发更新？
### 建议回答
并发能力可以让非紧急更新可中断，但不会自动让错误的数据结构变快。文件树展开如果一次生成大量可见节点，可以考虑 transition 区分紧急点击反馈和列表更新；表单输入通常保持紧急同步。使用前要验证 loading/过渡状态，避免并发请求结果覆盖和 UI 状态撕裂。

### Q：前端错误处理应该分哪些层？
### 建议回答
- 字段级错误：RHF + Zod，就近显示。
- 请求业务错误：Refine/tRPC 统一适配，页面显示可恢复信息。
- 页面级加载失败：ErrorState + retry。
- 未捕获渲染异常：Error Boundary。
- 服务端业务失败：Result 类型，映射为稳定错误码。
- 审计/协议失败：记录安全摘要，不向用户暴露内部堆栈。

### Q：为什么不能只用 Toast 显示所有错误？
### 建议回答
Toast 是瞬时的，用户可能错过，也不能指向具体字段或页面区域。字段错误应贴近输入框，页面加载失败应占据内容区域并提供 retry，撤销等关键操作应明确显示最终状态。Toast 更适合补充性的全局反馈，不是唯一错误承载方式。

### Q：虚拟树的无障碍难点是什么？
### 建议回答
虚拟化意味着部分逻辑节点不在 DOM，屏幕阅读器无法一次感知整棵树。要正确提供 tree/treeitem、level、expanded、selected、setsize/posinset 等语义，并实现方向键、Home/End、Enter/Space 等键盘行为。焦点节点被虚拟卸载时要处理焦点恢复。当前源码确认了 `role="tree"` 和 `aria-busy`，其他完整能力应以行组件实际实现为准。

### Q：前端隐藏按钮能否作为权限控制？
### 建议回答
不能。隐藏按钮只能改善体验，攻击者仍可直接发请求。权限必须在 tRPC/Service/MCP 鉴权路径中基于当前用户、workspace、资源归属和 connection 状态验证。前端只负责根据同一权限模型展示状态，不能成为最终安全边界。

### Q：OAuth/API Token 最需要防什么？
### 追问回答要点
- Token 泄露到日志、URL、截图和终端历史。
- Token 过期/撤销后仍可使用。
- connectionId 与 token 不匹配。
- 用户失去 workspace 权限后凭证继续有效。
- OAuth client 重复绑定或 consent 清理不完整。
- 错误响应泄露内部资源是否存在。
- 重放、暴力尝试和缺少速率限制。

---
## Payload CMS 与公开 Web

> 这一部分简历里属于“参与建设”。如果不是你亲自负责完整 CMS 后端，回答要说清楚你参与的是页面、数据映射、联调还是发布链路，不要包装成独立 owner。

### Q：为什么引入 Payload CMS？
### 建议回答
公开站点的文案、导航、SEO 和页面区块不适合每次都通过代码发布。Payload CMS 提供管理后台、草稿/版本和发布能力，公开 Web 再通过稳定的 public content endpoint 消费已发布内容。项目中 Pages 使用 Hero、Content、FeatureGrid 等 block，SiteNavigation 和 SiteSettings 作为 globals，内容模型比把整页 HTML 存数据库更结构化、可校验。

### Q：Pages collection 的核心设计是什么？
### 建议回答
Pages 具备 title、slug、summary、sections、navigation、SEO 和 publishedAt 等字段。sections 是 block 类型数组，当前包含 Hero、Content、FeatureGrid，并要求至少有一个 section。访问控制区分 authenticated、publisherOnly、publisherOrDraftEditor 等角色；页面支持 drafts 和 autosave，同时限制版本数量。这样编辑器可以保存草稿，只有通过发布校验且有 publisher 权限的用户才能成为公开内容。

### Q：草稿预览和公开页面如何隔离？
### 建议回答
Payload admin 的 live preview 会生成带 preview token 的 `/preview/pages/:slug` 地址，预览页明确标记为 draft preview 并设置 `noindex,nofollow`。公开 endpoint 只读取 published 内容或已保存的 published snapshot，不应该让未登录用户直接看到 draft。Preview secret 通过环境变量管理，不能硬编码到页面。

### Q：为什么要保存 published snapshot？
### 建议回答
公开内容读取可以优先使用已发布页面；如果 CMS 临时不可用或映射失败，服务会尝试读取经过 Schema 校验的 published snapshot，返回 `fallback` 状态。这样公开站点不会因为后台短暂故障直接变成空白，同时还能区分 published、fallback、unpublished、not_found、unavailable。快照不是任意缓存，它必须只在发布成功后同步，并保持内容结构可验证。

### Q：发布时为什么要校验内部链接？
### 建议回答
如果一个页面的 CTA 指向另一个内部页面，而目标页面还是 draft 或不存在，发布后用户会看到死链。`validatePublishIntent` 在 `_status` 变成 published 时检查 publisher 权限、至少一个 section、导航 label，以及启用的 internal link 是否指向 published page。发布校验放在 CMS 生命周期 hook，能防止绕过前端直接调用 API 造成无效公开内容。

### Q：公开内容服务返回 fallback 还是 unavailable 的条件是什么？
### 建议回答
先读取 published page 并映射为公开模型；如果读取/映射失败，会尝试读取 snapshot，并用 `PublicPageSchema.safeParse` 校验。快照合法就返回 fallback；快照读取失败或校验不通过就返回 unavailable。如果没有 published page，再查询是否存在任意 page，以区分 unpublished 和 not_found。这种状态建模让前端能给出不同反馈，而不是把所有问题都当 404。

### Q：为什么公开内容还要经过 mapper 和 Schema？
### 建议回答
CMS 的内部类型包含管理字段、关系对象和 Payload 特有结构，公开 Web 只需要稳定、最小化的 PublicPage 模型。mapper 负责把内部内容转换成公开契约，Schema 再做运行时校验，避免公开接口直接暴露 CMS 内部结构或把脏数据传给页面。未来更换 CMS，只需要适配 source 和 mapper，公开 Web 契约可以保持稳定。

### Q：如何避免发布成功但快照没保存？
### 建议回答
`afterChange` 在页面发布后重新读取 published page，映射为 PublicPage，再 upsert published-page-snapshots；任何步骤失败时抛出 APIError，提示最后有效快照未保存。更严格地说，Payload hook 与数据库事务的具体边界要结合运行时确认；设计目标是不要把“已对外可用”的状态与“快照已同步”分离得不可控。

### Q：MCP 为什么不能直接暴露 CMS 所有管理工具？
### 建议回答
MCP 插件配置按 collection/global 粒度显式开放工具。Pages 可以创建和编辑 draft，publish 使用独立的 `publishPageTool`，它额外检查 publisher access、参数范围和发布校验；published snapshots、cms-users 等内部集合的工具被关闭。最小暴露面比“把后台 API 全部开放给 Agent”更安全，也便于审计和回收权限。

### Q：MCP 发布工具的 idempotentHint 有什么意义？
### 建议回答
发布同一页面的重复调用最终仍是 published 状态，因此可以向客户端声明幂等倾向；但这不代表所有副作用都天然无风险，仍要考虑版本、审计、locale 和并发更新。工具输入限制 depth 0~10，并支持 locale、publishAllLocales，实际操作还要经过 publisher 权限和 collection 的 publish validation。

### Q：如果 CMS 不可用，公开站点怎么降级？
### 建议回答
公开内容服务将状态显式分为 fallback 和 unavailable，页面使用 `pageResult ?? unavailablePageDelivery` 作为兜底。fallback 表示当前数据来自最后有效快照，unavailable 表示没有可安全展示的内容。降级时不要渲染未经 Schema 校验的任意响应，也不要把内部数据库错误堆栈暴露给访客。

---
## AI 编程、Agent 与团队协作
### Q：你如何使用 AI 编程，而不是让 AI 代写代码？
### 建议回答
我会先把需求拆成领域模型、边界条件、现有约束和验收标准，再让 AI 做定向搜索、生成初稿或补测试；关键代码由我对照源码、类型、测试和实际交互逐段验证。对于 Daedalus，AI 适合帮助梳理跨包调用和重复模式，但权限、Token、事务、发布校验等高风险逻辑必须由人确认。最终提交以质量检查和 review 结果为准，而不是以 AI 输出为准。

### Q：你如何确认 AI 没有引入幻觉？
### 追问回答要点
- 要求它引用真实文件路径和函数名。
- 用 `rg`、TypeScript、测试和构建验证每个结论。
- 对外部协议查官方文档，不凭模型记忆实现 OAuth/MCP。
- 不接受源码中不存在的性能数字、上线结果和测试结论。
- 对数据库迁移、权限和安全代码做人工逐行 review。

### Q：如果 AI 建议把所有状态放到全局 Zustand，你会怎么判断？
### 建议回答
先按状态归属分类：服务端状态归 Refine/React Query，表单状态归 RHF，页面流程状态归页面级 Store，纯局部交互留在组件。只有需要跨页面、长生命周期共享的状态才考虑全局。架构选择应从生命周期、数据源唯一性、订阅范围和测试边界出发，而不是因为 Zustand 方便就全局化。

### Q：如何把一个模糊需求拆成可实现任务？
### 建议回答
先明确用户流程和完成定义，再拆为 schema/数据、服务接口、页面状态、组件、错误态、测试和发布/回滚。以 MCP connection 为例，要分别列 connection list/detail、授权状态、Token 一次性展示、revoke、owner 校验、调用记录和失败恢复，而不是只写一个“接入 MCP 页面”。

### Q：你做 code review 会重点看什么？
### 追问回答要点
- 数据是否有==唯一来源==，是否复制出双份状态。
- 异步状态是否能表达成功、失败、取消和重复触发。
- 权限是否在服务端闭环，是否存在只靠 UI 隐藏按钮的假安全。
- 动态列表 key、effect 依赖和 stale closure。
- Schema、类型、API 输入输出是否一致。
- loading/empty/error/disabled 和无障碍状态是否完整。
- 测试是否覆盖风险而不只是覆盖 happy path。

### Q：遇到与既有架构冲突的需求怎么办？
### 建议回答
先确认需求目标和约束，再找同领域已有实现，区分“必须新增能力”和“可以复用的模式”。如果确实需要偏离架构，就记录原因、影响面、迁移计划和回滚方式，并让相关人 review。不要为了短期交付在页面里直接访问数据库或复制一套 UI，最后把技术债隐藏起来。