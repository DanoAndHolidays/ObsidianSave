# CrateDialog

```ts
import { useCallback, useMemo } from "react";
import { Controller, FormProvider, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useList } from "@refinedev/core";
import {
  crateFormSchema,
  CrateTypeValues,
  type Archetype,
  type Crate,
  type CrateFormValues,
  type CratePathInput,
} from "@repo/schemas";
import { X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Dialog } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { MultiSelect } from "@/components/ui/multi-select";
import { Textarea } from "@/components/ui/textarea";
import { useTranslation } from "react-i18next";
import { ResourceName } from "@/integrations/refine/dataProvider";
import { CratePathsField } from "./CratePathsField";

interface CrateDialogProps {
  editing: Crate | null;
  onCreate: (values: Record<string, unknown>) => void;
  onUpdate: (values: Record<string, unknown>) => void;
  onClose: () => void;
}

export const toRepositoryId = function (
  value: string | null | undefined,
  isEdit: boolean,
): string | null | undefined {
  // ============================================================
  // 📝 第1题：规范化仓库 ID 的写入语义
  // ============================================================
  // 实现创建与编辑场景下 repositoryId 的边界转换：有值时原样返回；
  // 空值在编辑时应表示“显式解除关联”，创建时应表示“不提交该字段”。
  // （提示：使用 value、isEdit，并区分 null 与 undefined）

  // ✏️ 你的代码：

  return undefined;
};

export const CrateDialog = function ({
  editing,
  onCreate,
  onUpdate,
  onClose,
}: CrateDialogProps) {
  // ============================================================
  // 📝 第2题：解析编辑态并构造安全的初始快照
  // ============================================================
  // 获取翻译函数、判断当前模式，并从 editing 中读取 archetypeIds、
  // repositoryId 与 paths。缺失字段要提供正确默认值，数组数据不能直接复用原引用。
  // （提示：useTranslation、isEdit；保留 editingArchetypeIds、editingRepositoryId、
  // editingPaths 三个变量名；paths 的元素也要浅拷贝）

  // ✏️ 你的代码：


  // ============================================================
  // 📝 第3题：用共享 Zod Schema 初始化表单
  // ============================================================
  // 创建类型安全的 React Hook Form 实例，接入共享 schema，并同时覆盖创建态与编辑态默认值。
  // （提示：useForm<CrateFormValues>、zodResolver(crateFormSchema)、defaultValues；
  // type 的创建态默认值为 package，数组默认值应避免共享引用）

  // ✏️ 你的代码：


  // ============================================================
  // 📝 第4题：提取表单控制能力与状态
  // ============================================================
  // 从表单实例中取得原生字段注册、受控字段控制、提交包装器、校验错误和提交中状态。
  // （提示：变量名为 control、handleSubmit、register、errors、isSubmitting；
  // errors 与 isSubmitting 位于 formState）

  // ✏️ 你的代码：


  // ============================================================
  // 📝 第5题：加载 Archetype 并生成多选项
  // ============================================================
  // 通过 Refine 获取全部 Archetype，将可能为空的查询结果稳定为数组，
  // 再映射成 MultiSelect 所需的 { id, label } 结构。
  // （提示：useList<Archetype>、ResourceName.archetypes、pageSize: 0；
  // 用 useMemo 创建 archetypes 与 archetypeOptions，并写全依赖数组）

  // ✏️ 你的代码：


  // ============================================================
  // 📝 第6题：加载 GitHub 仓库候选项
  // ============================================================
  // 查询全部 GitHub 项目，并把 result.data 规范化为供仓库 Select 使用的 projects 数组。
  // （提示：useList<Record<string, unknown>>、ResourceName.githubProjects；
  // 将 result 重命名为 projectsResult，useMemo 依赖 projectsResult?.data）

  // ✏️ 你的代码：


  // ============================================================
  // 📝 第7题：实现关闭与提交边界
  // ============================================================
  // 实现稳定的关闭回调与表单提交回调。提交时清理文本字段、规范化可选 metadata、
  // 调用第1题的仓库 ID 转换、保留路径和 Archetype 关联；编辑调用 onUpdate，
  // 创建则补充 crypto.randomUUID() 生成的 id 后调用 onCreate。
  // （提示：useCallback；onSubmit 参数类型为 CrateFormValues；注意完整依赖数组）

  // ✏️ 你的代码：


  // ============================================================
  // 📝 第8题：完成表单内容与双模式界面渲染
  // ============================================================
  // 完成 Crate 表单、底部操作区以及创建/编辑两种容器：创建态使用 Dialog，
  // 编辑态使用右侧抽屉。所有原生表单控件均复用已导入的 UI 组件。
  // （提示：FormProvider 包裹 form；form.onSubmit 使用 handleSubmit(onSubmit)；
  // 普通字段使用 register，archetypeIds 使用 Controller + MultiSelect；
  // type 选项来自 CrateTypeValues；路径编辑复用 CratePathsField；
  // 展示 errors.name/errors.metadata，提交按钮绑定 isSubmitting；
  // Select 的仓库选项展示 owner/repo，关闭按钮使用 handleClose）

  // ✏️ 你的代码：

  return null;
};

```