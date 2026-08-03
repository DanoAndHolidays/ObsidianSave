# CrateCodeSnippetDialog

---
## code
```ts
import { useCallback, useEffect } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  crateCodeSnippetFormSchema,
  type CrateCodeSnippet,
  type CrateCodeSnippetFormValues,
} from "@repo/schemas";
import { useTranslation } from "react-i18next";
import { Button } from "@/components/ui/button";
import { Dialog } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

export type CrateCodeSnippetDialogProps = {
  initialData?: CrateCodeSnippet | null;
  isSubmitting?: boolean;
  open?: boolean;
  serverError?: string | null;
  onClose: () => void;
  onSubmit: (values: CrateCodeSnippetFormValues) => void;
};


// 这上面的不用看了
const getDefaultValues = function (
  initialData?: CrateCodeSnippet | null,
): CrateCodeSnippetFormValues {
  return {
    name: initialData?.name ?? "",
    language: initialData?.language ?? "",
    code: initialData?.code ?? "",
    description: initialData?.description ?? "",
  };
};

export const CrateCodeSnippetDialog = function ({
  initialData = null,
  isSubmitting = false,
  open = false,
  serverError = null,
  onClose,
  onSubmit,
}: CrateCodeSnippetDialogProps) {
  const { t } = useTranslation();

  // 使用useForm来获取form实例
  const form = useForm<CrateCodeSnippetFormValues>({

    // 应该就是去校验数据的 
    resolver: zodResolver(crateCodeSnippetFormSchema),

    // 用来提供数据来编辑
    defaultValues: getDefaultValues(initialData),
  });

  useEffect(() => {
    if (open) form.reset(getDefaultValues(initialData));
  }, [form, initialData, open]);

  const handleClose = useCallback(() => onClose(), [onClose]);

  // 使用form的高阶函数来校验value的值是否合法
  const handleSubmit = form.handleSubmit((values) => {
    onSubmit({ ...values });
  });

  return (
    <Dialog
      className="max-w-2xl"
      open={open}
      title={
        initialData
          ? t("crateDetail.editSnippet")
          : t("crateDetail.addSnippet")
      }
      onClose={handleClose}
    >
      <FormProvider {...form}>
        <form className="space-y-4" onSubmit={handleSubmit}>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">

              {/* htmlFor是用来 */}
              <Label htmlFor="crate-code-snippet-name">
                {t("crateDetail.snippetName")}
              </Label>
              <Input
                id="crate-code-snippet-name"
                placeholder={t("crateDetail.snippetNamePlaceholder")}
                {...form.register("name")}
              />
              {form.formState.errors.name && (
                <p className="text-sm text-destructive" role="alert">
                  {form.formState.errors.name.message}
                </p>
              )}
            </div>

            <div className="space-y-1.5">
              <Label htmlFor="crate-code-snippet-language">
                {t("crateDetail.snippetLanguage")}
              </Label>
              <Input
                id="crate-code-snippet-language"
                placeholder={t("crateDetail.snippetLanguagePlaceholder")}
                {...form.register("language")}
              />
              {form.formState.errors.language && (
                <p className="text-sm text-destructive" role="alert">
                  {form.formState.errors.language.message}
                </p>
              )}
            </div>
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="crate-code-snippet-description">
              {t("crateDetail.snippetDescription")}
            </Label>
            <Textarea
              id="crate-code-snippet-description"
              placeholder={t("crateDetail.snippetDescriptionPlaceholder")}
              rows={3}
              {...form.register("description")}
            />
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="crate-code-snippet-code">
              {t("crateDetail.snippetCode")}
            </Label>
            <Textarea
              className="min-h-56 font-mono"
              id="crate-code-snippet-code"
              placeholder={t("crateDetail.snippetCodePlaceholder")}
              spellCheck={false}
              {...form.register("code")}
            />
            {form.formState.errors.code && (
              <p className="text-sm text-destructive" role="alert">
                {form.formState.errors.code.message}
              </p>
            )}
          </div>

          {serverError && (
            <p className="text-sm text-destructive" role="alert">
              {serverError}
            </p>
          )}

          <div className="flex justify-end gap-2 border-t pt-4">
            <Button type="button" variant="outline" onClick={handleClose}>
              {t("common.cancel")}
            </Button>
            <Button disabled={isSubmitting} type="submit">
              {isSubmitting ? t("common.saving") : t("common.save")}
            </Button>
          </div>
        </form>
      </FormProvider>
    </Dialog>
  );
};

```

这个组件本质上是一个**“新增 / 编辑代码片段”弹窗表单**。

它将以下几个工具组合在一起：

* `Dialog`：负责弹窗
* `react-hook-form`：负责表单数据、校验状态和提交
* `Zod`：定义校验规则
* `zodResolver`：把 Zod 接入 react-hook-form
* `react-i18next`：负责多语言文本

---

## 一、组件整体做了什么

当用户打开弹窗时：

1. 如果没有 `initialData`，展示空表单，用于新增代码片段。
2. 如果有 `initialData`，把已有数据填入表单，用于编辑。
3. 用户点击保存时，先经过 Zod 校验。
4. 校验通过，调用外部传入的 `onSubmit`。
5. 校验失败，在对应输入框下面显示错误信息。
6. 如果后端提交失败，通过 `serverError` 展示服务端错误。

可以把整个流程理解为：

```text
打开弹窗
   ↓
填充默认值
   ↓
用户编辑表单
   ↓
点击保存
   ↓
Zod 校验
   ↓
成功 → 调用 onSubmit
失败 → 展示字段错误
```

---

# 二、默认值处理

```ts
const getDefaultValues = function (
  initialData?: CrateCodeSnippet | null,
): CrateCodeSnippetFormValues {
  return {
    name: initialData?.name ?? "",
    language: initialData?.language ?? "",
    code: initialData?.code ?? "",
    description: initialData?.description ?? "",
  };
};
```

这个函数负责把 `initialData` 转换成表单需要的数据结构。

当编辑已有数据时：

```ts
initialData = {
  name: "React 示例",
  language: "tsx",
  code: "const App = () => {}",
  description: "一个示例"
}
```

最终返回：

```ts
{
  name: "React 示例",
  language: "tsx",
  code: "const App = () => {}",
  description: "一个示例"
}
```

当新增时，`initialData` 是 `null`，返回：

```ts
{
  name: "",
  language: "",
  code: "",
  description: ""
}
```

这里使用了：

```ts
initialData?.name ?? ""
```

含义是：

* `initialData` 存在，就访问它的 `name`
* 如果 `name` 是 `null` 或 `undefined`，使用空字符串
* 如果 `initialData` 不存在，也使用空字符串

为什么表单字段最好使用空字符串，而不是 `undefined`？

因为输入框一般应该始终有明确的字符串值，能够避免 React 中“非受控组件切换为受控组件”之类的问题。

---

# 三、组件接收到的参数

```ts
export type CrateCodeSnippetDialogProps = {
  initialData?: CrateCodeSnippet | null;
  isSubmitting?: boolean;
  open?: boolean;
  serverError?: string | null;
  onClose: () => void;
  onSubmit: (values: CrateCodeSnippetFormValues) => void;
};
```

每个参数的作用如下。

### `initialData`

```ts
initialData?: CrateCodeSnippet | null;
```

用于区分新增和编辑。

新增：

```tsx
<CrateCodeSnippetDialog initialData={null} />
```

编辑：

```tsx
<CrateCodeSnippetDialog initialData={snippet} />
```

---

### `isSubmitting`

```ts
isSubmitting?: boolean;
```

表示数据是否正在提交。

提交过程中：

```tsx
<Button disabled={isSubmitting}>
```

按钮会被禁用，避免重复提交。

按钮文本也会变化：

```tsx
isSubmitting ? t("common.saving") : t("common.save")
```

例如：

```text
保存
```

变为：

```text
保存中
```

---

### `open`

```ts
open?: boolean;
```

控制弹窗是否显示。

```tsx
<Dialog open={open} />
```

---

### `serverError`

```ts
serverError?: string | null;
```

用于展示后端错误。

例如：

```text
代码片段名称已经存在
```

这和 Zod 字段校验错误不同：

* Zod 错误：前端校验发现的问题
* `serverError`：请求发送后，后端返回的问题

---

### `onClose`

```ts
onClose: () => void;
```

关闭弹窗时调用。

父组件通常会这样写：

```tsx
const [open, setOpen] = useState(false);

<CrateCodeSnippetDialog
  open={open}
  onClose={() => setOpen(false)}
/>
```

---

### `onSubmit`

```ts
onSubmit: (values: CrateCodeSnippetFormValues) => void;
```

表单校验成功后调用。

父组件可以在这里请求接口：

```tsx
onSubmit={(values) => {
  createSnippet(values);
}}
```

---

# 四、参数默认值

```ts
export const CrateCodeSnippetDialog = function ({
  initialData = null,
  isSubmitting = false,
  open = false,
  serverError = null,
  onClose,
  onSubmit,
}: CrateCodeSnippetDialogProps) {
```

这里通过参数解构设置默认值。

例如父组件没有传 `isSubmitting`：

```tsx
<CrateCodeSnippetDialog
  onClose={handleClose}
  onSubmit={handleSubmit}
/>
```

组件内部会自动认为：

```ts
isSubmitting === false
```

---

# 五、国际化

```ts
const { t } = useTranslation();
```

`t` 是一个翻译函数。

例如：

```tsx
t("common.save")
```

在中文环境下可能返回：

```text
保存
```

在英文环境下可能返回：

```text
Save
```

所以组件里没有直接写：

```tsx
<Button>保存</Button>
```

而是写：

```tsx
<Button>{t("common.save")}</Button>
```

---

# 六、创建表单实例

```ts
const form = useForm<CrateCodeSnippetFormValues>({
  resolver: zodResolver(crateCodeSnippetFormSchema),
  defaultValues: getDefaultValues(initialData),
});
```

这是整个组件最核心的部分。

`useForm` 返回一个表单对象：

```ts
form
```

里面包含很多能力，例如：

```ts
form.register
form.handleSubmit
form.reset
form.formState
form.getValues
form.setValue
form.watch
```

---

## 1. 泛型的作用

```ts
useForm<CrateCodeSnippetFormValues>()
```

它告诉 TypeScript：

> 这个表单的数据结构是 `CrateCodeSnippetFormValues`。

假设类型是：

```ts
type CrateCodeSnippetFormValues = {
  name: string;
  language: string;
  code: string;
  description: string;
};
```

那么下面这些字段是合法的：

```ts
form.register("name");
form.register("language");
form.register("code");
```

但是下面这个不存在的字段会报错：

```ts
form.register("age");
```

TypeScript 会提示：

```text
"age" 不是 CrateCodeSnippetFormValues 的字段
```

---

## 2. `resolver`

```ts
resolver: zodResolver(crateCodeSnippetFormSchema)
```

`crateCodeSnippetFormSchema` 是一个 Zod Schema。

例如它可能类似：

```ts
const crateCodeSnippetFormSchema = z.object({
  name: z.string().min(1, "名称不能为空"),
  language: z.string().min(1, "语言不能为空"),
  code: z.string().min(1, "代码不能为空"),
  description: z.string(),
});
```

但是 react-hook-form 本身并不知道怎么执行 Zod Schema。

因此需要：

```ts
zodResolver(crateCodeSnippetFormSchema)
```

作为适配器。

整体关系是：

```text
react-hook-form
       ↓
  zodResolver
       ↓
   Zod Schema
```

提交时，react-hook-form 会把表单数据交给 Zod：

```ts
{
  name: "",
  language: "tsx",
  code: ""
}
```

Zod 校验后可能返回：

```text
name 不能为空
code 不能为空
```

这些错误最后会进入：

```ts
form.formState.errors
```

---

## 3. `defaultValues`

```ts
defaultValues: getDefaultValues(initialData)
```

这是表单第一次创建时的默认数据。

新增时：

```ts
{
  name: "",
  language: "",
  code: "",
  description: ""
}
```

编辑时：

```ts
{
  name: initialData.name,
  language: initialData.language,
  code: initialData.code,
  description: initialData.description
}
```

有一个很重要的特点：

> `defaultValues` 通常只在 `useForm` 第一次执行时生效。

也就是说，如果后面 `initialData` 发生变化，react-hook-form 不会自动更新输入框。

因此下面还需要使用 `reset`。

---

# 七、为什么需要 `useEffect` 和 `reset`

```ts
useEffect(() => {
  if (open) form.reset(getDefaultValues(initialData));
}, [form, initialData, open]);
```

这段代码的作用是：

> 每次打开弹窗，或者编辑的数据发生变化时，重新设置表单内容。

举个例子。

第一次编辑代码片段 A：

```ts
initialData = {
  name: "代码片段 A"
}
```

表单显示：

```text
代码片段 A
```

关闭弹窗，然后编辑代码片段 B：

```ts
initialData = {
  name: "代码片段 B"
}
```

如果没有 `reset`，表单可能仍然显示：

```text
代码片段 A
```

因为 `defaultValues` 不会自动跟着 `initialData` 更新。

加入：

```ts
form.reset(getDefaultValues(initialData));
```

之后，打开 B 时就会重新填充：

```text
代码片段 B
```

---

## 为什么要判断 `open`

```ts
if (open)
```

只有弹窗打开时才重置表单。

这样可以避免在弹窗关闭状态下，无意义地修改表单状态。

而且“每次打开弹窗重置”还有一个效果：

假设用户打开弹窗后修改了内容，但没有保存，直接关闭：

```text
原名称：示例代码
修改为：乱写了一些内容
```

再次打开时，由于会执行：

```ts
form.reset(getDefaultValues(initialData))
```

未保存的修改会被清除，重新显示原始数据。

---

## 更常见的写法

目前依赖项中写了整个 `form`：

```ts
[form, initialData, open]
```

也可以只解构出 `reset`：

```ts
const { reset } = form;

useEffect(() => {
  if (open) {
    reset(getDefaultValues(initialData));
  }
}, [initialData, open, reset]);
```

语义会更加明确：

```ts
const form = useForm<CrateCodeSnippetFormValues>({
  resolver: zodResolver(crateCodeSnippetFormSchema),
  defaultValues: getDefaultValues(initialData),
});

const { reset } = form;

useEffect(() => {
  if (open) {
    reset(getDefaultValues(initialData));
  }
}, [initialData, open, reset]);
```

---

# 八、关闭弹窗

```ts
const handleClose = useCallback(() => onClose(), [onClose]);
```

这里创建了一个 `handleClose` 函数，它内部调用父组件传入的 `onClose`。

等价于：

```ts
const handleClose = () => {
  onClose();
};
```

使用 `useCallback` 后，只要 `onClose` 没有变化，`handleClose` 就会保持同一个函数引用。

不过这个组件里，`useCallback` 并不是必需的。直接使用 `onClose` 也可以：

```tsx
<Dialog onClose={onClose}>
```

取消按钮也可以：

```tsx
<Button type="button" onClick={onClose}>
```

当前写法没有问题，只是稍微多包了一层。

---

# 九、表单提交处理

```ts
const handleSubmit = form.handleSubmit((values) => {
  onSubmit({ ...values });
});
```

这里最容易让人困惑。

## `form.handleSubmit` 是什么

它是 react-hook-form 提供的一个高阶函数。

它接收一个“校验成功后的回调”：

```ts
form.handleSubmit((values) => {
  // 校验成功后执行
});
```

然后返回一个真正可以交给 `<form>` 的事件处理函数：

```ts
const handleSubmit = form.handleSubmit(...);
```

最后：

```tsx
<form onSubmit={handleSubmit}>
```

所以提交过程是：

```text
浏览器触发 submit
       ↓
handleSubmit 接收到事件
       ↓
react-hook-form 阻止浏览器默认刷新
       ↓
读取所有字段
       ↓
执行 Zod 校验
       ↓
校验成功：执行回调
校验失败：更新 errors
```

---

## `values` 是什么

```ts
(values) => {
  onSubmit({ ...values });
}
```

`values` 就是最终的表单数据：

```ts
{
  name: "React 状态示例",
  language: "tsx",
  code: "const [count, setCount] = useState(0)",
  description: "useState 示例"
}
```

然后把它传给父组件：

```ts
onSubmit(values)
```

当前写的是：

```ts
onSubmit({ ...values });
```

`{ ...values }` 创建了一个浅拷贝对象。

在这里通常没有必要，可以直接写：

```ts
const handleSubmit = form.handleSubmit(onSubmit);
```

或者：

```ts
const handleSubmit = form.handleSubmit((values) => {
  onSubmit(values);
});
```

---

# 十、Dialog 部分

```tsx
<Dialog
  className="max-w-2xl"
  open={open}
  title={
    initialData
      ? t("crateDetail.editSnippet")
      : t("crateDetail.addSnippet")
  }
  onClose={handleClose}
>
```

这里控制弹窗。

---

## `className`

```tsx
className="max-w-2xl"
```

限制弹窗最大宽度。

Tailwind 中：

```text
max-w-2xl
```

大约表示最大宽度为 `42rem`。

---

## `open`

```tsx
open={open}
```

控制弹窗显示状态。

---

## 动态标题

```tsx
title={
  initialData
    ? t("crateDetail.editSnippet")
    : t("crateDetail.addSnippet")
}
```

这是一个三元表达式：

```ts
条件 ? 条件成立的值 : 条件不成立的值
```

有初始数据时：

```text
编辑代码片段
```

没有初始数据时：

```text
添加代码片段
```

所以一个组件同时支持新增和编辑。

---

# 十一、`FormProvider` 的作用

```tsx
<FormProvider {...form}>
```

`FormProvider` 会通过 React Context，把整个 `form` 对象提供给内部所有后代组件。

内部组件可以通过：

```ts
useFormContext()
```

拿到表单实例，而不需要层层传参。

例如：

```tsx
function NameField() {
  const form = useFormContext<CrateCodeSnippetFormValues>();

  return <Input {...form.register("name")} />;
}
```

这样父组件不需要写：

```tsx
<NameField form={form} />
```

---

## 当前组件真的需要 `FormProvider` 吗

从目前展示的代码看，所有地方都直接使用：

```ts
form.register(...)
form.formState.errors
```

并没有看到子组件使用：

```ts
useFormContext()
```

因此如果 `Input`、`Textarea` 等内部也没有使用 `useFormContext`，这里的 `FormProvider` 可以去掉：

```tsx
<form onSubmit={handleSubmit}>
```

不过保留也没有问题。

它可能是为了之后把每个字段拆成独立组件。

---

# 十二、`form.register` 是什么

以名称输入框为例：

```tsx
<Input
  id="crate-code-snippet-name"
  placeholder={t("crateDetail.snippetNamePlaceholder")}
  {...form.register("name")}
/>
```

`register("name")` 的作用是：

> 把这个输入框注册到 react-hook-form，并告诉表单这个字段叫 `name`。

`form.register("name")` 大致会返回：

```ts
{
  name: "name",
  ref: 某个函数,
  onChange: 某个函数,
  onBlur: 某个函数
}
```

通过展开运算符：

```tsx
{...form.register("name")}
```

相当于：

```tsx
<Input
  name="name"
  ref={...}
  onChange={...}
  onBlur={...}
/>
```

于是 react-hook-form 就可以：

* 获取输入框当前值
* 监听值变化
* 监听失焦事件
* 执行校验
* 保存字段状态

---

## 为什么没有写 `value`

你可能会注意到这里没有：

```tsx
value={name}
onChange={(event) => setName(event.target.value)}
```

因为 react-hook-form 默认采用偏向**非受控组件**的方式管理表单。

普通 React 写法：

```tsx
const [name, setName] = useState("");

<Input
  value={name}
  onChange={(event) => setName(event.target.value)}
/>
```

react-hook-form 写法：

```tsx
<Input {...form.register("name")} />
```

这样写通常更加简洁，而且大表单中可以减少不必要的重新渲染。

---

# 十三、`Label` 和 `htmlFor`

```tsx
<Label htmlFor="crate-code-snippet-name">
  {t("crateDetail.snippetName")}
</Label>
```

对应的输入框：

```tsx
<Input id="crate-code-snippet-name" />
```

`htmlFor` 要和输入框的 `id` 对应：

```tsx
htmlFor="crate-code-snippet-name"
id="crate-code-snippet-name"
```

它的作用主要有两个。

## 1. 点击标签时聚焦输入框

用户点击：

```text
代码片段名称
```

浏览器会自动聚焦对应的输入框。

## 2. 提升无障碍访问能力

屏幕阅读器可以知道：

> 这个 Label 是在描述哪个输入框。

注意在原生 HTML 中属性叫：

```html
<label for="name">
```

但是在 React JSX 中要写：

```tsx
<label htmlFor="name">
```

因为 `for` 在 JavaScript 中是关键字，而且 React DOM 属性采用 `htmlFor`。

---

# 十四、错误信息展示

```tsx
{form.formState.errors.name && (
  <p className="text-sm text-destructive" role="alert">
    {form.formState.errors.name.message}
  </p>
)}
```

`form.formState.errors` 保存所有字段错误。

例如：

```ts
form.formState.errors = {
  name: {
    type: "too_small",
    message: "名称不能为空"
  },
  code: {
    type: "too_small",
    message: "代码不能为空"
  }
}
```

因此：

```ts
form.formState.errors.name
```

表示名称字段有没有错误。

如果有错误，渲染：

```tsx
<p>
  {form.formState.errors.name.message}
</p>
```

结果可能是：

```text
名称不能为空
```

---

## `role="alert"`

```tsx
role="alert"
```

这是一个无障碍属性。

当错误信息出现时，屏幕阅读器会更主动地向用户播报这段内容。

它不仅影响样式，而是告诉辅助设备：

> 这是一条需要用户注意的动态错误信息。

---

# 十五、表单布局

```tsx
<div className="grid grid-cols-2 gap-4">
```

这里把名称和语言放在两列中。

```text
┌──────────────────┬──────────────────┐
│ 名称             │ 语言             │
│ [输入框]         │ [输入框]         │
└──────────────────┴──────────────────┘
```

* `grid`：使用 CSS Grid
* `grid-cols-2`：两列
* `gap-4`：行列之间留出间距

---

## 字段内部布局

```tsx
<div className="space-y-1.5">
```

表示内部直接子元素在垂直方向上保留间距。

例如：

```text
Label
  ↓ 间距
Input
  ↓ 间距
错误信息
```

---

# 十六、描述字段

```tsx
<Textarea
  id="crate-code-snippet-description"
  placeholder={t("crateDetail.snippetDescriptionPlaceholder")}
  rows={3}
  {...form.register("description")}
/>
```

`rows={3}` 表示文本框默认大约显示三行高度。

这里没有渲染：

```tsx
form.formState.errors.description
```

可能有两种情况：

1. `description` 是可选字段，不会校验失败。
2. Schema 有校验，但是开发者忘记展示错误信息。

需要结合 `crateCodeSnippetFormSchema` 才能确定。

---

# 十七、代码字段

```tsx
<Textarea
  className="min-h-56 font-mono"
  id="crate-code-snippet-code"
  placeholder={t("crateDetail.snippetCodePlaceholder")}
  spellCheck={false}
  {...form.register("code")}
/>
```

这里针对代码内容做了一些特殊处理。

## `min-h-56`

设置最小高度，给代码输入提供更大的空间。

## `font-mono`

使用等宽字体。

代码适合等宽字体，因为字符宽度一致，例如：

```text
const name = "Dano";
```

缩进和结构会更加清晰。

## `spellCheck={false}`

关闭浏览器拼写检查。

如果不关闭，浏览器可能会把变量名标成拼写错误：

```ts
crateCodeSnippet
```

下面出现很多红色波浪线，会影响代码编辑体验。

---

# 十八、服务端错误

```tsx
{serverError && (
  <p className="text-sm text-destructive" role="alert">
    {serverError}
  </p>
)}
```

这是表单整体级别的错误。

比如用户输入的内容前端校验完全正确：

```ts
{
  name: "React Demo",
  language: "tsx",
  code: "..."
}
```

但是后端返回：

```text
该名称已经存在
```

父组件就可以传入：

```tsx
serverError="该名称已经存在"
```

然后弹窗中展示这个错误。

字段错误和服务端错误的来源不同：

```text
form.formState.errors
    来自 react-hook-form + Zod

serverError
    来自父组件，一般是接口请求结果
```

---

# 十九、底部按钮

```tsx
<div className="flex justify-end gap-2 border-t pt-4">
```

它表示：

* `flex`：按钮横向排列
* `justify-end`：按钮靠右
* `gap-2`：两个按钮之间留间距
* `border-t`：顶部边框
* `pt-4`：顶部内边距

视觉效果类似：

```text
────────────────────────────────
                  [取消] [保存]
```

---

# 二十、为什么取消按钮必须写 `type="button"`

```tsx
<Button type="button" variant="outline" onClick={handleClose}>
```

HTML 中，`form` 内部的 `<button>` 默认类型通常是：

```html
type="submit"
```

如果不写：

```tsx
type="button"
```

点击取消按钮也可能触发表单提交。

因此取消按钮明确写：

```tsx
type="button"
```

保存按钮写：

```tsx
type="submit"
```

这样职责很清楚。

---

# 二十一、保存按钮

```tsx
<Button disabled={isSubmitting} type="submit">
  {isSubmitting ? t("common.saving") : t("common.save")}
</Button>
```

点击后会触发：

```tsx
<form onSubmit={handleSubmit}>
```

提交过程中按钮被禁用：

```tsx
disabled={isSubmitting}
```

这样可以避免：

```text
用户连续点击 5 次
→ 发出 5 个请求
→ 创建 5 条重复数据
```

不过最终是否完全避免重复请求，还需要父组件正确维护 `isSubmitting`。

例如：

```ts
const handleSubmit = async (values) => {
  setIsSubmitting(true);

  try {
    await api.createSnippet(values);
  } finally {
    setIsSubmitting(false);
  }
};
```

---

# 二十二、完整运行过程

假设父组件这样使用：

```tsx
<CrateCodeSnippetDialog
  open={dialogOpen}
  initialData={selectedSnippet}
  isSubmitting={isSubmitting}
  serverError={serverError}
  onClose={() => setDialogOpen(false)}
  onSubmit={handleSave}
/>
```

### 第一步：打开弹窗

```ts
dialogOpen = true
```

组件执行：

```ts
form.reset(getDefaultValues(initialData))
```

---

### 第二步：填写输入框

用户输入：

```text
名称：React Context 示例
语言：tsx
描述：演示 useContext
代码：const value = useContext(...)
```

`register` 会让 react-hook-form 记录这些数据。

---

### 第三步：点击保存

保存按钮：

```tsx
type="submit"
```

触发表单：

```tsx
onSubmit={handleSubmit}
```

---

### 第四步：Zod 校验

```ts
resolver: zodResolver(crateCodeSnippetFormSchema)
```

如果名称为空，产生：

```ts
form.formState.errors.name.message
```

页面展示错误，不调用外部 `onSubmit`。

---

### 第五步：校验通过

执行：

```ts
onSubmit(values)
```

父组件开始请求后端，并设置：

```ts
isSubmitting = true
```

按钮变成：

```text
保存中
```

同时不能再次点击。

---

### 第六步：请求结果

成功时：

```ts
setDialogOpen(false)
```

失败时：

```ts
setServerError("保存失败，请稍后重试")
```

组件展示：

```text
保存失败，请稍后重试
```

---

# 二十三、这个组件的职责分层

这个组件主要负责：

```text
表单展示
表单字段状态
前端校验
错误展示
提交事件通知
```

它不直接负责：

```text
调用后端接口
保存数据库
决定保存成功后做什么
维护弹窗的最终开关状态
```

这些事情交给父组件。

这是一种比较合理的组件设计：

```text
CrateCodeSnippetDialog
    负责 UI 和表单

父组件
    负责业务逻辑和接口请求
```

---

# 二十四、几个可以简化或改进的地方

## 1. `handleSubmit` 可以简化

现在：

```ts
const handleSubmit = form.handleSubmit((values) => {
  onSubmit({ ...values });
});
```

可以改成：

```ts
const handleSubmit = form.handleSubmit(onSubmit);
```

因为不需要额外复制一遍 `values`。

---

## 2. `handleClose` 可以简化

现在：

```ts
const handleClose = useCallback(() => onClose(), [onClose]);
```

可以直接使用：

```tsx
<Dialog onClose={onClose}>
```

以及：

```tsx
<Button type="button" onClick={onClose}>
```

除非你以后需要在关闭时增加额外操作，例如：

```ts
const handleClose = useCallback(() => {
  form.clearErrors();
  onClose();
}, [form, onClose]);
```

---

## 3. `useEffect` 可以只依赖 `reset`

```ts
const { reset } = form;

useEffect(() => {
  if (open) {
    reset(getDefaultValues(initialData));
  }
}, [initialData, open, reset]);
```

比依赖整个 `form` 更明确。

---

## 4. `FormProvider` 可能暂时不需要

如果内部组件没有调用 `useFormContext`，可以移除。

不过将来准备把字段拆出去时，保留是合理的。

---

## 5. 可以为输入框补充无障碍关联

现在虽然有：

```tsx
role="alert"
```

但输入框没有直接通过 `aria-describedby` 关联错误消息。

可以写成：

```tsx
<Input
  id="crate-code-snippet-name"
  aria-invalid={Boolean(form.formState.errors.name)}
  aria-describedby={
    form.formState.errors.name
      ? "crate-code-snippet-name-error"
      : undefined
  }
  {...form.register("name")}
/>

{form.formState.errors.name && (
  <p
    id="crate-code-snippet-name-error"
    className="text-sm text-destructive"
    role="alert"
  >
    {form.formState.errors.name.message}
  </p>
)}
```

这样辅助设备能够更明确地知道：

> 这个错误属于哪个输入框。

---

## 6. 两列布局可以考虑响应式

现在固定：

```tsx
grid-cols-2
```

在较窄的屏幕上可能太挤。

可以改为：

```tsx
<div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
```

表示：

* 小屏幕：一列
* `sm` 及以上：两列

---

最核心的三处代码可以这样记：

```ts
const form = useForm({
  resolver,
  defaultValues,
});
```

负责创建表单。

```tsx
<Input {...form.register("name")} />
```

负责注册字段。

```ts
const handleSubmit = form.handleSubmit(onSubmit);
```

负责校验并提交。

而这段：

```ts
useEffect(() => {
  if (open) {
    form.reset(getDefaultValues(initialData));
  }
}, [form, initialData, open]);
```

则负责让同一个弹窗能够正确地在“新增”和“编辑不同数据”之间切换。
