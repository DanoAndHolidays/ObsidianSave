# useForm
详见[[前端/项目笔记/代达罗斯/模式/useForm|useForm]]
https://react-hook-form.com/docs/useform

```ts
import { useState, useRef, useCallback } from "react";

// ─── 类型 ───────────────────────────────────────────

type FieldValues = Record<string, unknown>;

interface RegisterReturn {
  name: string;
  onChange: (e: { target: { value: unknown } }) => void;
  onBlur: () => void;
  ref: (el: unknown) => void;
}

type ValidateFn<T> = (values: T) => Record<string, { message?: string }> | undefined;

/**
 * 简易版 useForm
 *
 * 内部三个核心数据：
 *   valuesRef  → useRef({ name: "", email: "" })    当前所有字段值
 *   errors     → useState({})                       当前校验错误（变化时触发渲染）
 *   touchedRef → useRef(Set)                        哪些字段被用户碰过
 *
 * 为什么 values 用 useRef 而 errors 用 useState？
 *   - values 每个字符都变，用 useState 会导致每个字符重渲染 → 用 ref 避免
 *   - errors 只在校验失败/成功时变化，用 useState 刚好在需要时触发渲染
 *   真实 react-hook-form 也是这个策略。
 */
export function useForm<T extends FieldValues>(options: {
  defaultValues: T;
  validate?: ValidateFn<T>;
}) {
  const { defaultValues, validate } = options;

  // ── 状态 ──────────────────────────────────────
  // 字段值：高频变化，用 ref 避免不必要的渲染
  const valuesRef = useRef<T>({ ...defaultValues });

  // 错误：低频变化（只在校验触发时变），用 state 驱动渲染
  const [errors, setErrors] = useState<Record<string, { message?: string } | undefined>>({});

  // 提交中状态
  const [isSubmitting, setIsSubmitting] = useState(false);

  // 已触碰字段集合：只记不渲染
  const touchedRef = useRef<Set<string>>(new Set());

  // 用 ref 存 validate 的当前引用，避免 register 的 useCallback 依赖 validate 导致频繁重建
  const validateRef = useRef(validate);
  validateRef.current = validate;

  // ── register ──────────────────────────────────
  /**
   * register("name") 返回一个对象，展开到 <input> 上：
   *
   *   <input {...register("name")} />
   *   ↓ 等价于
   *   <input
   *     name="name"
   *     value={valuesRef.current.name}
   *     onChange={(e) => setField("name", e.target.value)}
   *     onBlur={() => markTouched("name")}
   *   />
   *
   * 为什么叫 register？把真实 DOM 元素"注册"到表单中央管理系统，
   * 从此这个 input 的值、焦点、校验全部由 useForm 接管。
   */
  const register = useCallback(
    (name: keyof T & string): RegisterReturn => ({
      name,
      onChange: (e: { target: { value: unknown } }) => {
        // 更新 ref 中的值（不触发渲染）
        valuesRef.current = { ...valuesRef.current, [name]: e.target.value };

        // 如果字段已被触碰过，实时校验当前字段
        if (touchedRef.current.has(name) && validateRef.current) {
          const fieldErrors = validateRef.current(valuesRef.current);
          // 只更新当前字段的错误
          setErrors((prev) => {
            const prevErr = prev[name];
            const nextErr = fieldErrors?.[name];
            // 避免相同错误导致无意义渲染
            if (prevErr?.message === nextErr?.message) return prev;
            return { ...prev, [name]: nextErr };
          });
        }
      },
      onBlur: () => {
        touchedRef.current.add(name);
        // 失焦时跑单字段校验
        if (validateRef.current) {
          const fieldErrors = validateRef.current(valuesRef.current);
          setErrors((prev) => {
            const prevErr = prev[name];
            const nextErr = fieldErrors?.[name];
            if (prevErr?.message === nextErr?.message) return prev;
            return { ...prev, [name]: nextErr };
          });
        }
      },
      ref: () => {
        // 真实实现里这里拿到 DOM 引用，用于 focus() 等操作
      },
    }),
    [], // 空依赖 —— 所有可变数据都通过 ref 读取
  );

  // ── handleSubmit ──────────────────────────────
  /**
   * handleSubmit(onSubmit) 返回一个函数，挂到 <form onSubmit={...}> 上。
   *
   *   用户点提交
   *     → preventDefault
   *     → 全量校验
   *     → 有错误？setErrors，结束，onSubmit 不执行
   *     → 无错误？onSubmit(values副本)
   */
  const handleSubmit = useCallback(
    (onSubmit: (values: T) => void | Promise<void>) =>
      async (e?: { preventDefault: () => void }) => {
        e?.preventDefault();
        setIsSubmitting(true);

        // 1. 全量校验
        if (validateRef.current) {
          const allErrors = validateRef.current(valuesRef.current);
          if (allErrors && Object.keys(allErrors).length > 0) {
            setErrors(allErrors);
            setIsSubmitting(false);
            return; // ← 校验不通过，onSubmit 不会被调用
          }
        }

        // 2. 校验通过
        setErrors({});
        try {
          await onSubmit({ ...valuesRef.current }); // 副本输出
        } finally {
          setIsSubmitting(false);
        }
      },
    [],
  );

  // ── 返回值 ────────────────────────────────────
  return {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  };
}
```