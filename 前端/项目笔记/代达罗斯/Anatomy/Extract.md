`Extract` 是 TypeScript 内置的**工具类型**，作用是：

> 从一个联合类型中，筛选出能够赋值给指定类型的成员。

它的定义可以近似理解为：

```ts
type Extract<T, U> = T extends U ? T : never;
```

你的代码：

```ts
type TreeNodeParent =
  | (AnatomyEntry & { kind: "directory" })
  | Extract<AnatomyNode, { kind: "one_of" }>
  | null;
```

这里：

```ts
Extract<AnatomyNode, { kind: "one_of" }>
```

表示：

> 从 `AnatomyNode` 的所有成员中，取出 `kind` 为 `"one_of"` 的那一种类型。

---

## 举个例子

假设 `AnatomyNode` 是一个联合类型：

```ts
type AnatomyNode =
  | {
      kind: "file";
      name: string;
    }
  | {
      kind: "directory";
      name: string;
      children: AnatomyNode[];
    }
  | {
      kind: "one_of";
      options: AnatomyNode[];
    };
```

那么：

```ts
type OneOfNode = Extract<AnatomyNode, { kind: "one_of" }>;
```

得到的类型就是：

```ts
type OneOfNode = {
  kind: "one_of";
  options: AnatomyNode[];
};
```

也就是说，`Extract` 帮你从这个联合类型中把目标成员筛选出来了。

---

## 它是怎么筛选的

TypeScript 会逐个检查联合类型成员。

对于：

```ts
Extract<AnatomyNode, { kind: "one_of" }>
```

相当于逐个判断：

```ts
{ kind: "file"; name: string }
  extends { kind: "one_of" }
    ? 保留
    : never;
```

结果是不符合，所以变成 `never`。

```ts
{ kind: "directory"; children: AnatomyNode[] }
  extends { kind: "one_of" }
    ? 保留
    : never;
```

也不符合。

```ts
{ kind: "one_of"; options: AnatomyNode[] }
  extends { kind: "one_of" }
    ? 保留
    : never;
```

符合，所以保留。

最后 `never` 会从联合类型中消失，剩下：

```ts
{
  kind: "one_of";
  options: AnatomyNode[];
}
```

---

## 为什么不直接写 `{ kind: "one_of" }`

因为只写：

```ts
{ kind: "one_of" }
```

只能说明它有一个 `kind` 属性：

```ts
{
  kind: "one_of";
}
```

但会丢失这个节点原本的其他属性。

假设真正的 `one_of` 节点是：

```ts
{
  kind: "one_of";
  id: string;
  name: string;
  options: AnatomyNode[];
}
```

使用：

```ts
Extract<AnatomyNode, { kind: "one_of" }>
```

得到的是完整类型：

```ts
{
  kind: "one_of";
  id: string;
  name: string;
  options: AnatomyNode[];
}
```

所以 `Extract` 的意义是：

> 根据某个特征筛选类型，同时保留这个成员完整的属性结构。

---

## 完整理解 `TreeNodeParent`

```ts
type TreeNodeParent =
  | (AnatomyEntry & { kind: "directory" })
  | Extract<AnatomyNode, { kind: "one_of" }>
  | null;
```

它表示 `TreeNodeParent` 可以是以下三种情况：

```ts
// 1. directory 类型的 AnatomyEntry
AnatomyEntry & { kind: "directory" }

// 2. AnatomyNode 中 kind 为 one_of 的节点
Extract<AnatomyNode, { kind: "one_of" }>

// 3. 没有父节点
null
```

也就是说，一个树节点的父节点可能是：

* 一个目录节点；
* 一个 `one_of` 节点；
* 或者没有父节点，通常表示它是根节点。

---

## `Extract` 常见用法

不仅能筛选对象联合类型，也可以筛选普通联合类型。

```ts
type Value = string | number | boolean;

type StringValue = Extract<Value, string>;
```

结果：

```ts
type StringValue = string;
```

也可以筛选多个类型：

```ts
type Result = Extract<
  string | number | boolean,
  string | number
>;
```

结果是：

```ts
type Result = string | number;
```

---

可以简单记成：

```ts
Extract<联合类型, 筛选条件>
```

也就是：

> 从前面的联合类型中，提取符合后面条件的成员。

与它相反的是 `Exclude`：

```ts
Exclude<AnatomyNode, { kind: "one_of" }>
```

表示排除掉 `kind: "one_of"` 的成员，保留其他成员。
