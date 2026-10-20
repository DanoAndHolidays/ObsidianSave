# Type Guard
> Last Format Time：10/8/2026 23:35:46

类型守卫通过运行时条件判断，让 TypeScript 在某个代码分支中缩小变量的可能类型范围。

它属于==类型收窄（Type Narrowing）==机制。

例如：
```ts
function format(value: string | number) {
  if (typeof value === "string") {
    // TS 知道这里 value 是 string
    return value.toUpperCase();
  }

  // 这里 value 是 number
  return value.toFixed(2);
}
```

常见的守卫包括 `typeof`、`instanceof`、`in`、判别属性判断，以及自定义类型谓词。

自定义守卫：
```ts
type User = {
  id: number;
  name: string;
};

function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    typeof value.id === "number" &&
    "name" in value &&
    typeof value.name === "string"
  );
}
```

这里的 `value is User` 是类型谓词，告诉 TS：函数返回 `true` 时，可以把 `value` 收窄为 `User`。

注意，类型守卫并不是 TypeScript 在运行时生成的类型检查。真正执行的是 JavaScript 判断逻辑，类型收窄由编译器分析完成。

---
## `number | undefined` 的变量与 1 比较
```text
function check(a: number | undefined) {
  return a > 1;
}
```

要区分两个层面。

JavaScript 运行时：
```text
undefined > 1; // false
```

因为 `undefined` 在这里参与数值比较会被转换为 `NaN`，比较结果是 `false`。

TypeScript 编译时：
启用 `strictNullChecks` 后，直接写 `a > 1` 会提示 `a` 可能是 `undefined`。

更合适的写法：
```text
function check(a: number | undefined) {
  return a !== undefined && a > 1;
}
```

如果业务允许给缺失值提供默认值：
```text
return (a ?? 0) > 1;
```

但两种做法语义不同：前者显式检查缺失值，后者将缺失值当作 0。

这道题真正考的是：你能否区分 TS 的静态类型检查和 JS 的运行时行为。
