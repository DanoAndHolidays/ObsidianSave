# Form

---
## 场景分析
### 项目中的Form
在 Daedalus 项目中，[form](https://ocn10zycuxwg.feishu.cn/wiki/KSMswZ2q2ihY1rk27R4cxe5Vnjc)是一套**完整的前端表单架构规范**：
```
┌─────────────────────────────────────────────────────┐
│                  Form Architecture                  │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐  │
│  │ react-hook-  │  │ shadcn/ui    │  │ Zod (v4)  │  │
│  │ form         │  │ Form 组件层   │ │ Schema     │  │
│  │ 状态管理      │  │ UI 结构      │  │ 校验层     │  │
│  └──────┬───────┘  └──────┬───────┘  └─────┬─────┘  │
│         │                 │                │        │
│         └────────┬────────┴────────┬───────┘        │
│                  │                 │                │
│                  ▼                 ▼                │
│           useForm()          zodResolver            │
│                  │                 │                │
│                  └────────┬────────┘                │
│                           │                         │
│                           ▼                         │
│                    Form Component                   │
│                           │                         │
│                    仅提交时输出                      │
│                    数据副本给外部                    │
│                           │                         │
│                           ▼                         │
│              ┌──────────────────────┐               │
│              │Global State (Zustand)│               │
│              │ 或 API 调用           │               │
│              └──────────────────────┘               │
└─────────────────────────────────────────────────────┘
```

### 能力模型

| 层级 | 职责 | 包含要素 |
|------|------|---------|
| **状态管理** | 表单字段值的生命周期 | useForm、formControl、FormProvider、独立状态树、沙盒隔离 |
| **UI 结构** | 标准化的组件层级 | Form → FormField → FormItem → FormLabel → FormControl → Input → FormMessage |
| **校验集成** | 类型安全的表单校验 | Zod schema、zodResolver、zod/v4 导入、schema 派生（.pick/.omit） |
| **数据流** | 初始化 → 编辑 → 提交的数据通道 | defaultValues 深拷贝、null→undefined 处理、提交时副本传递 |
| **复杂表单拆分** | 多子组件的表单上下文共享 | FormProvider + useFormContext、禁止 props 透传 control |

### "两棵树"状态隔离模型
这是 Form 场景最核心的架构概念：
```
┌─────────────────────────────────────┐
│  Global State Tree (Zustand)        │
│  - 跨组件共享的业务状态               │
│  - 用户信息、路由状态、UI 开关        │
│  - 不包含任何表单字段值               │
└─────────────────────────────────────┘
         ↑ 仅在提交时传入数据副本
         │ （单向，不可反向流入）
┌─────────────────────────────────────┐
│  Form State Tree (react-hook-form)  │
│  - 字段值、脏值、错误、提交状态        │
│  - 完全独立，自包含生命周期           │
│  - defaultValues 初始化 → 用户编辑   │
│    → handleSubmit 输出副本           │
└─────────────────────────────────────┘
```

**单向数据流**：
1. **初始化**：`defaultValues` 接收原始数据的**深拷贝副本**（`structuredClone` 或 `{...data}`）
2. **编辑过程**：所有用户输入仅在 react-hook-form 内部流转，原始数据不可变
3. **提交时刻**：`handleSubmit((values) => onSubmit({...values}))` 传递数据副本
4. **禁止反向污染**：Zustand 状态不应直接驱动表单字段值（除非是初始值）

### 两种合法范式
飞书文档 + 现有 Skill 定义了两种表单范式，**必须先选定范式**再按对应 Condition 约束：

| 范式 | 适用场景 | formControl 位置 | Props |
|------|---------|------------------|-------|
| **范式 A：独立表单组件** | 跨页面复用、纯输入收集器 | 组件内部 `useForm()` | `initialData` + `onSubmit` |
| **范式 B：页面绑定表单** | Dialog 内表单、单页面紧耦合 | Zustand slice 中 `createFormControl<T>()` | 无（从 slice 读取） |

代码示例：
```tsx
// 范式 A 示例：
// 组件接收 initialData + onSubmit，内部 useForm()
export const CreateCrateForm = ({
  initialData,
  onSubmit,
}: CreateCrateFormProps) => {
  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: initialData ? { ...initialData } : defaultValues,
  });
  // ...
};

// 范式 B 示例：
// formControl 在 slice 中，组件不接 props
// slice.ts:
const formControl = createFormControl<AgentFormValues>({
  defaultValues: { name: "", description: "" },
  resolver: zodResolver(agentFormSchema),
});
// component.tsx:
const formControl = useStore(store, (s) => s.agentFormControl);
const handleFormSubmit = useStore(store, (s) => s.handleFormSubmit);
const form = useForm<AgentFormValues>({ formControl: formControl.formControl });
```

---
## Crate 设计
对齐 Button 和 Barrel Export 场景的层级拆分策略：

| 层级 | 说明 |
|------|------|
| **功能模块级** | 一个 Crate = 一组内聚的功能，不是单个组件 |
| **与路由/页面解耦** | Crate 不绑定到特定页面，可跨路由复用 |
| **类型语义明确** | 使用 `CrateTypeValues` 中的枚举值 |
| **按"层"拆分** | 引擎层 / UI 层 / 校验层 / 桥接层 |

#### Crate A: `form-engine`

| 字段 | 值 |
|------|-----|
| **name** | `form-engine` |
| **type** | `library` |
| **responsibility** | 封装 react-hook-form 核心集成：useForm 工厂函数、FormProvider 上下文设置、formControl 生命周期管理、与 zodResolver 的基础绑定、沙盒隔离机制 |
| **metadata** | `{"package": "react-hook-form", "version": "^7.x", "paradigm": ["A", "B"]}` |

**包含内容**：
- `useForm` 的类型安全封装（泛型 FormValues、zodResolver 集成）
- FormProvider + useFormContext 的标准用法
- `createFormControl<T>()` 工厂（供 Zustand slice 使用）
- 表单提交流程的标准化（handleSubmit → deep copy → callback）
- 范式 A/B 的路由逻辑（initialData + onSubmit vs formControl + handleFormSubmit）

#### Crate B: `form-components`

| 字段 | 值 |
|------|-----|
| **name** | `form-components` |
| **type** | `module` |
| **responsibility** | 提供 shadcn/ui Form 系列组件的标准化封装：Form、FormField、FormItem、FormLabel、FormControl、FormMessage，确保字段层级结构一致 |
| **metadata** | `{"package": "shadcn/ui", "components": ["Form", "FormField", "FormItem", "FormLabel", "FormControl", "FormMessage"]}` |

**包含内容**：
- `Form` — `useForm()` 返回值展开，包裹表单
- `FormField` — `control` + `name` → `render={({ field }) => ...}`
- `FormItem` — 字段容器 + 错误状态上下文
- `FormLabel` — 可选标签
- `FormControl` — 包裹实际输入组件，传递 field 属性
- `FormMessage` — Zod 校验错误自动展示

#### Crate C: `form-validation`

| 字段 | 值 |
|------|-----|
| **name** | `form-validation` |
| **type** | `utility` |
| **responsibility** | Zod 表单 Schema 工具集：从 @repo/schemas 派生表单 schema 的辅助函数、常用校验模式（required、minLength、email 等）、zodResolver 配置模板、null→undefined 兜底工具 |
| **metadata** | `{"package": "zod", "version": "v4", "resolver": "@hookform/resolvers/zod"}` |

**包含内容**：
- Zod 从 `"zod/v4"` 的统一导入
- `zodResolver` 的标准配置
- 从已有 schema `.pick()` / `.omit()` 的派生模式
- 常用校验组合（如 `requiredString`、`optionalString`）
- `defaultValues` 的 `null → undefined` 兜底工具

#### Crate D: `form-store-bridge`

| 字段 | 值 |
|------|-----|
| **name** | `form-store-bridge` |
| **type** | `utility` |
| **responsibility** | 范式 B 的 react-hook-form ↔ Zustand 桥接层：createFormControl 在 slice 中的标准用法、handleFormSubmit 模式、formControl 与 slice 其他状态的生命周期协调 |
| **metadata** | `{"package": "zustand", "version": "^5.x", "paradigm": "B"}` |

**包含内容**：
- `createFormControl<T>()` 在 Zustand slice 中的标准位置
- `handleFormSubmit` 的完整流程模板（mutate → toast → reset → close）
- formControl 的 reset / 清理生命周期
- 防止 formControl 引用泄漏的规范


### 目前项目中的实现分布

| 目标 Crate            | 实际对应物                                         | 位置                                             | 类型                                         |
| ------------------- | --------------------------------------------- | ---------------------------------------------- | ------------------------------------------ |
| `form-engine`       | **`form-best-practice` Skill**                | `.claude/skills/form-best-practice/`           | Claude Code Skill                          |
|                     | — `references/checklist.md`                   | 同上                                             | 检查清单（范式 A/B 判定 + 7 节规则）                    |
|                     | — `references/form-best-practice-guide.md`    | 同上                                             | "两棵树"模型 + 状态隔离原则 + 两种范式                    |
|                     | — `references/anatomy.json`                   | 同上                                             | 表单组件树结构 JSON                               |
|                     | — `best-practice-examples/CreateUserForm.tsx` | 同上                                             | 范式 A 示例代码                                  |
|                     | **`form-best-practice` Archetype**            | `docs/archetypes/form-best-practice.md`        | Daedalus Archetype 文档                      |
|                     | — 19 条 Condition（含 `archetype_ref` 传递依赖）      | 同上                                             | 结构化条件定义                                    |
| `form-components`   | **shadcn/ui Form 组件**                         | `@/components/ui/form`（标准 shadcn 位置）           | UI 组件                                      |
| `form-validation`   | **@repo/schemas**（Zod schema 源）               | `packages/schemas/src/`                        | 共享 Schema 包                                |
|                     | **`zod-infer-type-best-practice` Skill**      | `.claude/skills/zod-infer-type-best-practice/` | Claude Code Skill                          |
| `form-store-bridge` | **`CrateDialog` 迁移实战**                        | `apps/app/src/`                                | 实际组件（范式 B 的参考实现）                           |
|                     | — `useForm({ formControl })` 模式               | 同上                                             | 范式 B 的 formControl 托管                      |
|                     | **`store-best-practice` Skill**               | `.claude/skills/store-best-practice/`          | Claude Code Skill（定义 createFormControl 规范） |

---
## Archetype 契约定义
**Archetype ID**: `form-best-practice`
**Scope**: `page`
**Concept**: 确保所有前端表单遵循 react-hook-form + Zod + shadcn/ui 标准架构，实现表单状态与全局状态的严格隔离

> 我们这里假设出现的archetype_ref均已实现

##### C-1: 禁止 useState 管理表单字段
- **ID**: `c-form-no-usestate`
- **类型**: `text`
- **排序**: 1
- **依赖**: 无
- **条件内容**:
  ```
  所有表单字段值必须由 react-hook-form 管理。禁止使用 useState、useReducer 或任何其他本地状态
  管理表单字段的 value/onChange。

  ❌ 违规: const [name, setName] = useState("")
  ✅ 正确: 通过 useForm({ defaultValues }) + <Input {...field} /> 管理
  ```

##### C-2: 禁止表单字段直接绑定 Zustand
- **ID**: `c-form-no-zustand-binding`
- **类型**: `text`
- **排序**: 2
- **依赖**: 无
- **条件内容**:
  ```
  表单字段值禁止直接双向绑定到 Zustand 全局状态。禁止从 Zustand store 读取字段值并实时写回。

  ❌ 违规: <Input value={store.name} onChange={(e) => store.setName(e.target.value)} />
  ✅ 正确: 通过 react-hook-form field 管理，仅在 onSubmit 时将数据副本传给 store action

  注意：范式 B 下 formControl 实例托管在 slice 中不算违反此条（formControl 是控制器，不是字段值）。
  ```

##### C-3: 表单沙盒隔离
- **ID**: `c-form-sandbox`
- **类型**: `text`
- **排序**: 3
- **依赖**: 无
- **条件内容**:
  ```
  表单是独立沙盒。所有用户输入仅在 react-hook-form 内部流转，不影响原始数据。
  仅在调用 onSubmit/handleSubmit 时，将表单值的深拷贝副本传递给外部（API、Zustand action 等）。

  ❌ 违规: 在 onChange 回调中实时 dispatch(setFormData(values))
  ✅ 正确: 在 handleSubmit((values) => onSubmit({ ...values })) 中传递副本

  关键原则：原始数据在整个表单生命周期内不可变（immutable），避免"边编辑边污染源数据"。
  ```

##### C-4: 范式 B — formControl 托管在 slice
- **ID**: `c-form-paradigm-b-formcontrol`
- **类型**: `archetype_ref`
- **排序**: 4
- **依赖**: `["store-best-practice"]`
- **条件内容**:
  ```
  范式 B 场景下，formControl 实例必须由 Zustand slice 通过 createFormControl<T>() 创建并持有。
  组件使用 useForm({ formControl: slice.formControl }) 接管，不在组件内本地创建 useForm()。

  ❌ 违规（范式 B 场景）: 在组件内 const form = useForm({ resolver, defaultValues })
  ✅ 正确: slice 中 export const formControl = createFormControl<T>({...})，
          组件中 const form = useForm({ formControl: store.formControl })
  ```

##### C-5: 范式 B — handleFormSubmit 在 slice
- **ID**: `c-form-paradigm-b-submit`
- **类型**: `archetype_ref`
- **排序**: 5
- **依赖**: `["store-best-practice"]`
- **条件内容**:
  ```
  范式 B 场景下，完整的提交流程（mutate / navigate / toast / close）必须在 slice 的
  handleFormSubmit 方法中完成。组件仅通过 <form onSubmit={form.handleSubmit(handleFormSubmit)}>
  绑定，禁止在组件内 JS 主动调用 submit 逻辑。

  ❌ 违规（范式 B 场景）: 组件内 const onSubmit = async (values) => { await mutate(...); close() }
  ✅ 正确: slice 中定义 handleFormSubmit，组件中只做绑定
  ```

##### C-6: shadcn/ui Form 外层包裹
- **ID**: `c-form-shadcn-wrapper`
- **类型**: `text`
- **排序**: 6
- **依赖**: 无
- **条件内容**:
  ```
  表单外层必须使用 shadcn/ui 的 <Form {...form}> 组件包裹（展开 useForm 返回值）。
  禁止仅使用原生 <form> 元素而不使用 shadcn Form 组件。

  ❌ 违规: <form onSubmit={handleSubmit(...)}>  // 无 <Form>
  ✅ 正确: <Form {...form}><form onSubmit={form.handleSubmit(onSubmit)}>...</form></Form>
  ```

##### C-7: 完整字段层级结构
- **ID**: `c-form-field-hierarchy`
- **类型**: `text`
- **排序**: 7
- **依赖**: 无
- **条件内容**:
  ```
  每个表单字段必须使用完整组件层级：
  FormField → FormItem → FormControl → 实际输入组件 → FormMessage

  ❌ 违规: 跳过 FormItem 直接 <FormControl><Input /></FormControl>
  ❌ 违规: 不使用 FormMessage 导致校验错误无显示
  ✅ 正确:
    <FormField control={form.control} name="xxx" render={({ field }) => (
      <FormItem>
        <FormLabel>XXX</FormLabel>
        <FormControl><Input {...field} /></FormControl>
        <FormMessage />
      </FormItem>
    )} />
  ```

##### C-8: {...field} 展开模式
- **ID**: `c-form-field-spread`
- **类型**: `text`
- **排序**: 8
- **依赖**: 无
- **条件内容**:
  ```
  输入组件必须通过 render={({ field }) => <Input {...field} />} 方式接入 react-hook-form。
  严禁手动处理 value 和 onChange。

  ❌ 违规: <Input value={form.watch("name")} onChange={(e) => form.setValue("name", e.target.value)} />
  ✅ 正确: render={({ field }) => <Input {...field} />}

  注意：对于非原生输入组件（如 shadcn/ui 的 Select、DatePicker），应使用 <Controller>
  或该组件库提供的专用适配方式。
  ```

##### C-9: 提交按钮在 form 内部
- **ID**: `c-form-submit-button-inside`
- **类型**: `text`
- **排序**: 9
- **依赖**: 无
- **条件内容**:
  ```
  <button type="submit">（或 shadcn/ui <Button type="submit">）必须位于它要提交的 <form> 元素内部。
  当表单内容和按钮拆分在不同 JSX 变量中时，确保 <form> 标签包裹两者。

  ❌ 违规:
    const formContent = <form>...</form>;
    const footer = <Button type="submit">Save</Button>;
    return <>{formContent}{footer}</>;  // button 在 form 外面

  ✅ 正确:
    const formContent = <div>...</div>;
    const footer = <Button type="submit">Save</Button>;
    return <form onSubmit={...}>{formContent}{footer}</form>;
  ```

##### C-10: Zod Schema 派生（禁止重复定义）
- **ID**: `c-form-zod-derivation`
- **类型**: `archetype_ref`
- **排序**: 10
- **依赖**: `["zod-infer-type-best-practice"]`
- **条件内容**:
  ```
  表单的 Zod schema 应优先从已有 schema（@repo/schemas）通过 .pick() / .omit() 派生，
  禁止在组件中重新手写字段定义和枚举值。

  ❌ 违规:
    const formSchema = z.object({
      name: z.string().min(1),
      type: z.enum(["package", "module", ...]),  // 与 @repo/schemas 重复
    });

  ✅ 正确:
    const formSchema = crateCreateSchema.pick({ name: true, type: true });
  ```

##### C-11: zodResolver 集成
- **ID**: `c-form-zod-resolver`
- **类型**: `text`
- **排序**: 11
- **依赖**: 无
- **条件内容**:
  ```
  useForm 必须通过 zodResolver 集成 Zod Schema 校验。禁止使用自定义 validate 函数
  或手动 if/else 校验逻辑。

  ❌ 违规: useForm({ validate: (values) => { if (!values.name) return "Required" } })
  ✅ 正确: useForm({ resolver: zodResolver(formSchema) })

  导入规范:
  - z 必须从 "zod/v4" 导入（非 "zod"）
  - zodResolver 必须从 "@hookform/resolvers/zod" 导入
  ```

##### C-12: Zod 从 zod/v4 导入
- **ID**: `c-form-zod-v4-import`
- **类型**: `text`
- **排序**: 12
- **依赖**: 无
- **条件内容**:
  ```
  Zod 必须从 "zod/v4" 导入，禁止从 "zod" 导入。

  ❌ 违规: import { z } from "zod"
  ✅ 正确: import { z } from "zod/v4"
  ```

##### C-13: defaultValues 深拷贝
- **ID**: `c-form-defaultvalues-deepcopy`
- **类型**: `text`
- **排序**: 13
- **依赖**: 无
- **条件内容**:
  ```
  useForm 的 defaultValues 必须使用原始数据的深拷贝副本，禁止直接传递引用对象。

  ❌ 违规: defaultValues: originalData  // 直接传引用
  ✅ 正确: defaultValues: { ...originalData }  // 浅拷贝副本
  ✅ 正确: defaultValues: structuredClone(originalData)  // 深拷贝副本（嵌套对象场景）

  原因：直接传引用会导致表单编辑时意外修改原始数据，破坏 immutable 原则。
  ```

##### C-14: null → undefined 处理
- **ID**: `c-form-null-undefined`
- **类型**: `text`
- **排序**: 14
- **依赖**: 无
- **条件内容**:
  ```
  Drizzle 数据库可能返回 null 值，但 z.string().optional() 推导类型为 string | undefined。
  给 defaultValues 赋值时，对可能为 null 的字段使用 ?? "" 或 ?? undefined 兜底。

  ❌ 违规:
    defaultValues: {
      description: editing.description,  // DB 可能返回 null，类型不匹配
    }

  ✅ 正确:
    defaultValues: {
      description: editing.description ?? "",  // null → ""
    }
  ```

##### C-15: 提交时传递数据副本
- **ID**: `c-form-submit-deepcopy`
- **类型**: `text`
- **排序**: 15
- **依赖**: 无
- **条件内容**:
  ```
  表单提交（onSubmit / handleSubmit 回调）时，必须将表单值副本传递给外部，
  禁止直接传递 react-hook-form 内部引用或原始对象引用。

  ❌ 违规: onSubmit(form.getValues())  // 传 react-hook-form 内部引用
  ✅ 正确: handleSubmit((values) => onSubmit({ ...values }))  // 传递副本
  ```

##### C-16: FormProvider 共享上下文
- **ID**: `c-form-provider-context`
- **类型**: `text`
- **排序**: 16
- **依赖**: 无
- **条件内容**:
  ```
  当表单拆分为多个子组件时，必须使用 FormProvider 包裹以共享 react-hook-form 上下文。
  子组件通过 useFormContext() 访问 form 方法（control, setValue, getValues, watch 等）。

  ❌ 违规: 通过 props 将 control 或 register 逐层传递给子组件
  ✅ 正确:
    // 父组件
    const form = useForm();
    return <FormProvider {...form}><ChildComponent /></FormProvider>;

    // 子组件
    const { control } = useFormContext<FormValues>();
  ```

##### C-17: 禁止 control/register props 透传
- **ID**: `c-form-no-control-props`
- **类型**: `archetype_ref`
- **排序**: 17
- **依赖**: `["c-form-provider-context"]`
- **条件内容**:
  ```
  禁止通过组件 props 逐层传递 control 或 register。子组件需要访问 form 上下文时，
  必须使用 useFormContext()（配合父组件的 FormProvider）。

  ❌ 违规: function NameField({ control }: { control: Control<FormValues> })
  ✅ 正确: function NameField() { const { control } = useFormContext<FormValues>() }

  例外：原子级 UI 组件（如封装了 FormField 逻辑的通用字段组件）可以从 props 接收 control。
  ```

##### C-18: 命名导出函数组件
- **ID**: `c-form-named-export`
- **类型**: `text`
- **排序**: 18
- **依赖**: 无
- **条件内容**:
  ```
  表单组件必须使用命名导出（named export），禁止使用默认导出（default export）。

  ❌ 违规: export default function MyForm()
  ✅ 正确: export const MyForm = function () { ... }
  ```

##### C-19: 范式 A — 标准 Props 接口
- **ID**: `c-form-paradigm-a-props`
- **类型**: `text`
- **排序**: 19
- **依赖**: 无
- **条件内容**:
  ```
  范式 A（独立表单组件）必须接收以下标准 props：
  - initialData?: FormValues（可选，预填数据）
  - onSubmit: (data: FormValues) => void | Promise<void>（必填，提交回调）

  ❌ 违规: 使用其他命名如 data、defaultData、submitFn
  ✅ 正确: props 统一为 initialData 和 onSubmit

  Props 类型必须显式声明，禁止使用 any。
  ```

---
## 参考
[飞书文档](https://ocn10zycuxwg.feishu.cn/wiki/KSMswZ2q2ihY1rk27R4cxe5Vnjc)