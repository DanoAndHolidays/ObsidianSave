# Zod Schema 模式
> Last Format Time：7/14/2026 20:56:57

---
## 表单 Schema 复用：`.pick()` + `.extend()`
表单的 Zod schema 不应重新定义已有字段，而应从 API/数据库 schema 派生。

### 核心方法
| 方法 | 作用 |
|------|------|
| `.pick({ a: true, b: true })` | 从已有 schema 中选取指定字段，生成子集 |
| `.extend({ c: z.string() })` | 在已有 schema 基础上追加新字段 |

### 为什么需要这两种方法
表单层的类型和数据库 schema 的类型通常不完全一致：

- **表单用字符串表示数组**：用户在文本框输入逗号/换行分隔的值，提交后才转换为 `string[]`
- **表单不需要 `id`、`createdAt`、`updatedAt`**：这些由后端生成
- **`.default()` 导致字段变 optional**：原始 schema 中带 `.default()` 的字段，其 input 类型变为 `string | undefined`，不能直接被 form schema 复用

### 示例
```ts
// packages/schemas/src/dictionary-entry-schema.ts —— 数据库 schema
export const dictionaryEntryCreateSchema = z.object({
  id: z.string(),
  name: z.string().min(1),
  partOfSpeech: z.enum(["noun", "verb"]),
  aliases: z.array(z.string()).default([]),       // string[] → 表单用逗号分隔的 string
  definition: z.string().min(1),
  writingStandard: z.string().default(""),         // 带 .default()，input 类型为 optional
  usageBoundary: z.string().default(""),           // 同上
  examples: z.array(z.string()).default([]),       // string[] → 表单用换行分隔的 string
  relatedEntryIds: z.array(z.string()).default([]),// string[] → 表单用逗号分隔的 string
  createdAt: z.union([z.date(), z.string()]),
  updatedAt: z.union([z.date(), z.string()]),
});

// apps/app/src/pages/DictionaryPage/DictionaryDialog.tsx —— 表单 schema
const dictionaryFormSchema = dictionaryEntryCreateSchema.pick({
  // ✅ 类型直接匹配，复用校验规则（.min(1)、.enum(...)）
  name: true,
  partOfSpeech: true,
  definition: true,
}).extend({
  // ✅ 表单层用 string，覆盖原始 schema 中的 string[] / string|undefined
  writingStandard: z.string(),
  usageBoundary: z.string(),
  aliases: z.string(),          // 原始是 z.array(z.string())
  examples: z.string(),         // 原始是 z.array(z.string())
  relatedEntryIds: z.string(),  // 原始是 z.array(z.string())
});

type DictionaryForm = z.infer<typeof dictionaryFormSchema>;
```

### 选型对照
| 字段 | 原始类型 | 表单类型 | 处理方式 |
|------|---------|---------|---------|
| `name` | `z.string().min(1)` | `string` | `.pick()` 直接复用 |
| `partOfSpeech` | `z.enum([...])` | `"noun" \| "verb"` | `.pick()` 直接复用 |
| `definition` | `z.string().min(1)` | `string` | `.pick()` 直接复用 |
| `writingStandard` | `z.string().default("")` | `string \| undefined` | `.extend()` 覆盖（去 default） |
| `usageBoundary` | `z.string().default("")` | `string \| undefined` | `.extend()` 覆盖（去 default） |
| `aliases` | `z.array(z.string())` | `string[]` | `.extend()` 覆盖（string 替代 array） |
| `examples` | `z.array(z.string())` | `string[]` | `.extend()` 覆盖（string 替代 array） |
| `relatedEntryIds` | `z.array(z.string())` | `string[]` | `.extend()` 覆盖（string 替代 array） |
| `id` | `z.string()` | 不需要 | 不 pick |
| `createdAt` | `z.union([...])` | 不需要 | 不 pick |
| `updatedAt` | `z.union([...])` | 不需要 | 不 pick |

---
## 完整表单模式（react-hook-form + zodResolver）
结合项目中的 `CrateDialog.tsx` 和 `DictionaryDialog.tsx`，标准表单模式如下：

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod/v4";
import { someCreateSchema } from "@repo/schemas";

// 1. 从已有 schema 派生 form schema
const formSchema = someCreateSchema.pick({
  fieldA: true,
  fieldB: true,
}).extend({
  formOnlyField: z.string(),
});

type FormValues = z.infer<typeof formSchema>;

export const MyDialog = ({ editing, onCreate, onUpdate, onClose }) => {
  // 2. useForm + zodResolver
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: editing ? { /* 从 editing 映射 */ } : { /* 空值 */ },
  });

  // 3. handleSubmit 包装提交逻辑
  const onSubmit = (values: FormValues) => {
    const payload = { /* 转换表单值 → API 值 */ };
    if (editing) onUpdate(payload);
    else onCreate({ id: crypto.randomUUID(), ...payload });
  };

  return (
    // 4. <form> + handleSubmit，按钮 type="submit"
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("fieldA")} />
      {errors.fieldA && <p>{errors.fieldA.message}</p>}

      <button type="submit" disabled={isSubmitting}>保存</button>
    </form>
  );
};
```

### 关键要点
- **字段绑定**：`{...register("fieldName")}` 替代手动的 `value`/`onChange`
- **校验**：Zod schema 自动校验，错误通过 `errors.fieldName?.message` 逐字段显示
- **提交状态**：`isSubmitting` 禁用按钮，防止重复提交
- **表单元素**：用 `<form onSubmit={handleSubmit(onSubmit)}>` + `type="submit"`，不用 `type="button"` + `onClick`
