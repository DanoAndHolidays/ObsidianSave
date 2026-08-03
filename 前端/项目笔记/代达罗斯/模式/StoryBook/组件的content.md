

这里的 `=` 表示：**给泛型参数设置默认类型**。

```ts
<TData extends BaseRecord = BaseRecord>
```

可以拆成两部分看：

```ts
TData extends BaseRecord
```

表示 `TData` 必须符合 `BaseRecord` 的结构约束。

```ts
TData = BaseRecord
```

表示调用时如果没有显式指定 `TData`，就默认使用 `BaseRecord`。

所以完整含义是：

> `TData` 必须是 `BaseRecord` 或它的子类型；如果调用者没有传类型，就把 `TData` 当作 `BaseRecord`。

例如：

```ts
type BaseRecord = {
  id: string;
};

type User = {
  id: string;
  name: string;
};
```

显式传入类型：

```ts
getList<User>();
```

此时：

```ts
TData = User
```

返回值就是：

```ts
Promise<GetListResponse<User>>
```

不传类型：

```ts
getList();
```

此时使用默认值：

```ts
TData = BaseRecord
```

返回值相当于：

```ts
Promise<GetListResponse<BaseRecord>>
```

如果没有这个默认值：

```ts
async <TData extends BaseRecord>(): Promise<GetListResponse<TData>>
```

调用 `getList()` 时，TypeScript 需要尝试推断 `TData`。但这个函数没有参数可以帮助推断，最终类型可能比较宽泛或者不符合库作者期望。

加上默认值后：

```ts
<TData extends BaseRecord = BaseRecord>
```

就明确告诉 TypeScript：推断不出来时，直接使用 `BaseRecord`。

你的完整代码可以理解为：

```ts
getList: async <
  TData extends BaseRecord = BaseRecord
>(): Promise<GetListResponse<TData>> => ({
  data: snippets as unknown as TData[],
  total: snippets.length,
}),
```

其中：

```ts
Promise<GetListResponse<TData>>
```

表示返回的数据结构中的 `data` 最终应该是：

```ts
TData[]
```

因此可以简单记住：

```ts
<T extends A = B>
```

含义是：

```text
extends A：T 必须满足 A 的约束
= B：没有指定 T 时，默认使用 B
```

这里刚好默认值和约束类型一样：

```ts
<TData extends BaseRecord = BaseRecord>
```

但它们也可以不同：

```ts
type Animal = {
  name: string;
};

type Dog = Animal & {
  bark(): void;
};

function createAnimal<T extends Animal = Dog>(): T {
  // ...
}
```

这里 `T` 必须属于 `Animal` 范围，但默认使用 `Dog`。
