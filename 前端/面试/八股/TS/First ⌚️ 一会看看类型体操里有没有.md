# First
实现一个函数first()，其返回值类型是其输入的数组或元组的第一个类型

简单实现
```ts
// 使用泛型 T 约束输入必须是至少包含一个元素的元组或数组
function first<T extends readonly unknown[]>(arr: T): T[0] {
  if (arr.length === 0) {
    throw new Error("Cannot get the first element of an empty array");
  }
  return arr[0];
}
```

在 TypeScript 中，可以直接通过 `T[0]` 来获取数组的第一个元素类型。结合条件类型判断是否为空数组即可：
```typescript
// 直接利用 T[0] 提取，比 infer 更直观
type First<T extends any[]> = T extends [] ? never : T[0];

function first<T extends readonly unknown[]>(arr: [...T]): First<[...T]> | undefined {
    return arr[0] as any; 
}
```

你也可以通过检查数组的 `length` 属性来判断是否为空，这种方式与上面的逻辑类似，但换了一种特判角度：
```typescript
// 通过 length 属性特判空数组
type First<T extends any[]> = T['length'] extends 0 ? never : T[0];
```