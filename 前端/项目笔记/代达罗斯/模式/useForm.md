# useForm
https://react-hook-form.com/docs/useform

基于 `CrateDialog` 从 `useState` 重构为 `react-hook-form` 的实战记录。

---
## 基本用法
### 1. 依赖
```ts
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod/v4";
```

### 2. 定义表单 Schema
优先从已有 schema `.pick()` 派生，避免重复定义字段：
```ts
import { crateCreateSchema } from "@repo/schemas";

const crateFormSchema = crateCreateSchema.pick({
  name: true,
  type: true,
  responsibility: true,
  metadata: true,
});

type CrateForm = z.infer<typeof crateFormSchema>;
```

> 如果不想引入 `z`，可以用 `type CrateForm = Pick<Crate, "name" | "type" | ...>`，但字段写了两遍（schema 里一份、Pick 里一份），不如 `z.infer` 干净。

### 3. 调用 `useForm`
入参：
`useForm<CrateForm>` 泛型参数，告诉 TypeScript 这个表单有哪些字段、每个字段是什么类型
`resolver: zodResolver(crateFormSchema)`把 Zod schema 接进来，字段值变化时自动跑校验
`defaultValues: { ... }`表单初始值

解构：
把原生 DOM 元素注册到 react-hook-form 的函数
包装你的提交函数，先跑校验，通过才调用
当前校验错误，按字段名索引
布尔值，提交中为 true
```ts
const {
  register,
  handleSubmit,
  formState: { errors, isSubmitting },
} = useForm<CrateForm>({
  resolver: zodResolver(crateFormSchema),
  defaultValues: {
    name: "",
    type: "package",
    responsibility: "",
    metadata: "",
  },
});
```

### 4. 绑定输入框 — `register()`
用展开运算符把 `register("fieldName")` 传给原生表单组件：
```tsx
<Input {...register("name")} />
<Select {...register("type")}>
  {CrateTypeValues.map((t) => <option key={t} value={t}>{t}</option>)}
</Select>
<Textarea {...register("responsibility")} />
```

不再需要手写 `value` / `onChange`。

> 注意：shadcn/ui 的 `Select`（Radix 封装，非原生 `<select>`）需要用 `<Controller>` 而不是 `register`。


`register("name")` 返回一个对象，大概长这样：
```js
{
  name: "name",
  onChange: (e) => { /* 更新内部状态 */ },
  onBlur: (e) => { /* 标记字段被触碰过 */ },
  ref: (el) => { /* 拿到真实 DOM 引用 */ },
}
```

展开到 `<Input>` 上，就等价于：
```tsx
<Input
  name="name"
  onChange={(e) => form.setValue("name", e.target.value)}
  onBlur={(e) => form.markTouched("name")}
  ref={form.register("name").ref}
/>
```

**关键点**：你不需要手动写 `value={xxx}` 和 `onChange={yyy}`，`register` 替你接管了一切。

### 5. 显示校验错误
```tsx
<Input {...register("name")} />
{errors.name && (
  <p className="text-sm text-red-600 mt-1">{errors.name.message}</p>
)}
```

### 6. 提交流程
```tsx
<form onSubmit={handleSubmit(onSubmit)}>
```

`handleSubmit` 是一个**高阶函数**：
```
用户点击提交按钮
  → handleSubmit 拦截 submit 事件
  → 用 zodResolver 跑一遍 Zod 校验
  → 校验不通过 → 阻止提交，把错误写入 formState.errors，页面自动显示错误
  → 校验通过   → 调用你传的 onSubmit(values)，values 是当前表单所有字段的值
```

所以你的 `onSubmit` 回调**拿到的 `values` 一定是校验通过的**，不需要在里面再写 `if (!name) return`：
```tsx
const onSubmit = useCallback((values: CrateForm) => {
  const payload = {
    name: values.name.trim(),
    type: values.type,
    responsibility: values.responsibility.trim(),
    metadata: values.metadata?.trim() || undefined,
  };

  if (isEdit) {
    onUpdate(payload);
  } else {
    onCreate({ id: crypto.randomUUID(), ...payload });
  }
}, [isEdit, onCreate, onUpdate]);
```

```tsx
<form onSubmit={handleSubmit(onSubmit)}>
  {/* 输入框 */}
  <Button type="submit" disabled={isSubmitting}>Save</Button>
</form>
```

---
## 常见坑
### 坑 1：`formState` 解构错误
```ts
// ❌ 错误 — 把 errors 重命名为 isSubmitting，两个变量变成同一个
formState: { errors: isSubmitting }

// ✅ 正确 — 分别解构
formState: { errors, isSubmitting }
```

### 坑 2：提交按钮在 `<form>` 外面
HTML 规范要求 `<button type="submit">` 必须位于它要提交的 `<form>` 内部。
当表单内容和按钮拆分在不同 JSX 变量中时容易犯这个错：
```tsx
// ❌ 错误 — button 在 form 外面
const formContent = <form>...</form>;
const footer = <Button type="submit">Save</Button>;
return <>{formContent}{footer}</>;

// ✅ 正确 — form 包住两者
const formContent = <div>...</div>;
const footer = <Button type="submit">Save</Button>;
return (
  <form onSubmit={handleSubmit(onSubmit)}>
    {formContent}
    {footer}
  </form>
);
```

### 坑 3：Schema 字段重复定义
项目中 `@repo/schemas` 已有完整的 Zod schema，不要在组件里重新手写字段和枚举值。用 `.pick()` 摘取需要的字段：
```ts
// ❌ — 枚举值和校验规则重复定义
const crateFormSchema = z.object({
  name: z.string().min(1, "Name is required"),
  type: z.enum(["package", "module", "feature", ...]),
  ...
});

// ✅ — 从已有 schema 派生
const crateFormSchema = crateCreateSchema.pick({
  name: true,
  type: true,
  ...
});
```

同时把 schema 中的常量（如 `CrateTypeValues`）export 出来，在 UI 层直接引用，不需要 `const typeOptions = CrateTypeValues` 这种别名。

### 坑 4：`defaultValues` 中的 `null` vs `undefined`
`z.string().optional()` 推导出的类型是 `string | undefined`，但 Drizzle 数据库可能返回 `null`。给 `defaultValues` 赋值时用 `?? ""` 兜底：
```ts
defaultValues: editing
  ? {
      name: editing.name,
      responsibility: editing.responsibility ?? "",
      metadata: editing.metadata ?? "",       // ← DB 可能返回 null
    }
  : { name: "", type: "package", responsibility: "", metadata: "" },
```

### 坑 5：Vite 热更新缓存
重构后浏览器报 `Failed to fetch dynamically imported module`，但代码本身没问题，可能是 Vite HMR 缓存卡住了。重启 dev server 通常能解决：
```bash
# 杀掉端口进程，重新启动
netstat -ano | grep 9431
cmd //c "taskkill /PID <PID> /F"
cd apps/app && bun run dev
```

---
## 对比总结

| 方面 | 手动 `useState` | `react-hook-form` |
|------|----------------|-------------------|
| 字段绑定 | 每个输入写 `value` + `onChange` | `{...register("name")}` 一行 |
| 校验 | 手写 `if` / `setError` | Zod schema + `zodResolver`，字段级错误自动注入 |
| 重渲染 | 每次按键触发整组件渲染 | 基于 ref，不触发重渲染 |
| 提交按钮禁用 | 需要额外 `isSubmitting` state | `formState.isSubmitting` 内置 |
| 代码量 | ~80 行状态 + 校验逻辑 | ~20 行 |
