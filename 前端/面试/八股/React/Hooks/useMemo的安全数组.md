你可以先把这段代码拆成两个问题来看：

```ts
const anatomies = useMemo(
  () => result?.data ?? [],
  [result?.data],
);
```

它同时做了两件事：

1. 保证 `anatomies` 永远是数组。
2. 尽量让这个数组的引用保持稳定。

---

## 1. `result?.data ?? []` 为什么叫“安全数组”

`useList` 在请求完成之前，`result` 可能还不存在：

```ts
result === undefined
```

这时：

```ts
result?.data
```

得到的是：

```ts
undefined
```

如果直接写：

```ts
const anatomies = result?.data;
```

那么 `anatomies` 的类型和实际值可能是：

```ts
AnatomySummary[] | undefined
```

下游使用时就要反复判断：

```tsx
anatomies?.map(...)
anatomies?.length
```

或者：

```tsx
if (!anatomies) return null;
```

加上 `?? []` 后：

```ts
const anatomies = result?.data ?? [];
```

意思是：

> 有数据就使用数据，没有数据就使用空数组。

因此 `anatomies` 始终是：

```ts
AnatomySummary[]
```

下游可以安全地写：

```tsx
anatomies.map(...)
anatomies.length
```

这就是“始终提供安全数组”。

---

## 2. 为什么直接写 `?? []` 可能产生不稳定引用

这里是理解 `useMemo` 的关键。

数组属于引用类型。每次写：

```ts
[]
```

都会创建一个新的数组。

例如：

```ts
[] === []
```

结果是：

```ts
false
```

虽然两个数组内容都是空的，但它们不是同一个数组对象。

假设组件重新渲染了很多次，而数据还没有回来：

```ts
const anatomies = result?.data ?? [];
```

每次渲染都会执行一次 `[]`：

```ts
// 第一次渲染
anatomies = 空数组A

// 第二次渲染
anatomies = 空数组B

// 第三次渲染
anatomies = 空数组C
```

因此：

```ts
空数组A !== 空数组B
空数组B !== 空数组C
```

这就叫做**引用不稳定**。

---

## 3. `useMemo` 在这里做了什么

```ts
const anatomies = useMemo(
  () => result?.data ?? [],
  [result?.data],
);
```

它的意思是：

> 只有当 `result?.data` 发生变化时，才重新计算数组；否则继续返回上一次的数组。

当 `result?.data` 一直是 `undefined` 时：

```ts
// 第一次渲染
useMemo 创建空数组A

// 第二次渲染，result?.data 没变化
继续使用空数组A

// 第三次渲染，result?.data 没变化
继续使用空数组A
```

因此引用保持稳定：

```ts
第一次的 anatomies === 第二次的 anatomies
```

这不是为了避免什么昂贵计算，因为：

```ts
result?.data ?? []
```

本身几乎没有计算成本。

它主要是为了保持数组引用稳定。

---

## 4. 为什么引用稳定有时很重要

假设把 `anatomies` 传给一个经过 `memo` 优化的子组件：

```tsx
const AnatomyList = memo(function AnatomyList({
  anatomies,
}: {
  anatomies: AnatomySummary[];
}) {
  return anatomies.map((item) => <div key={item.id}>{item.name}</div>);
});
```

父组件中：

```tsx
<AnatomyList anatomies={anatomies} />
```

如果父组件这样写：

```ts
const anatomies = result?.data ?? [];
```

请求还没完成时，每次父组件渲染都会产生新数组：

```ts
旧 anatomies !== 新 anatomies
```

React 会认为传给子组件的 props 变了，于是 `AnatomyList` 也会重新渲染。

即使两个数组都是空数组，引用不同也会被认为发生了变化。

使用 `useMemo` 后：

```ts
const anatomies = useMemo(
  () => result?.data ?? [],
  [result?.data],
);
```

只要 `result?.data` 没变，传给子组件的数组引用就不变，`memo` 才有机会跳过无意义渲染。

---

## 5. 但为什么又说“不需要为了 useMemo 而 useMemo”

因为不是所有引用变化都会造成实际问题。

假设你只是在当前组件中直接渲染：

```tsx
return (
  <div>
    {anatomies.map((item) => (
      <div key={item.id}>{item.name}</div>
    ))}
  </div>
);
```

这里没有：

* 把 `anatomies` 传给 `memo` 子组件；
* 把 `anatomies` 放进其他 Hook 的依赖数组；
* 基于 `anatomies` 做昂贵计算；
* 依赖数组引用判断数据是否变化。

那么直接写：

```ts
const anatomies = result?.data ?? [];
```

通常就完全足够。

虽然每次无数据时都会创建新空数组，但创建一个空数组成本非常低，不一定值得增加 `useMemo` 的复杂度。

所以评价里的意思是：

> 不要看到数组就机械地使用 `useMemo`，先看这个数组的引用稳定性是否真的会影响下游。

---

## 6. 什么叫“下游依赖引用稳定性”

常见的情况有三种。

### 情况一：传给 `memo` 子组件

```tsx
<MemoizedList data={anatomies} />
```

此时稳定引用可能有价值。

### 情况二：放进其他 Hook 的依赖数组

```ts
useEffect(() => {
  doSomething(anatomies);
}, [anatomies]);
```

如果无数据时每次都创建新空数组，Effect 可能每次渲染都执行：

```ts
const anatomies = result?.data ?? [];
```

因为每次的 `anatomies` 都是不同引用。

使用稳定空数组后可以避免这种情况。

不过很多时候，更合理的是直接依赖原始数据：

```ts
useEffect(() => {
  doSomething(result?.data ?? []);
}, [result?.data]);
```

### 情况三：作为另一个 `useMemo` 的依赖

```ts
const grouped = useMemo(
  () => groupAnatomies(anatomies),
  [anatomies],
);
```

如果 `anatomies` 每次都是新空数组，那么 `grouped` 也会每次重新计算。

---

## 7. 为什么依赖 `[result?.data]` 比 `[result]` 更准确

原代码是：

```ts
const anatomies = useMemo(
  () => result?.data,
  [result],
);
```

标准答案是：

```ts
const anatomies = useMemo(
  () => result?.data ?? [],
  [result?.data],
);
```

原因是你真正关心的是：

```ts
result.data
```

而不是整个：

```ts
result
```

假设 Refine 每次渲染都返回一个新的 `result` 对象：

```ts
resultA = {
  data: dataA,
  total: 10,
};

resultB = {
  data: dataA,
  total: 10,
};
```

虽然：

```ts
resultA !== resultB
```

但它们内部的 `data` 可能还是同一个引用：

```ts
resultA.data === resultB.data
```

依赖整个 `result`：

```ts
[result]
```

会导致 `useMemo` 重新计算。

依赖具体使用的值：

```ts
[result?.data]
```

只有数据数组真正变化时才重新计算。

可以理解为：

```ts
// 依赖范围太大
[result]

// 精确依赖
[result?.data]
```

不过，这里的重新计算本身非常简单，所以主要是代码语义更加精确，而不是性能差距很大。

---

## 8. 模块级 `EMPTY_ARRAY` 是什么方案

还可以在组件外创建一个固定的空数组：

```ts
const EMPTY_ANATOMIES: AnatomySummary[] = [];
```

组件中：

```ts
const anatomies = result?.data ?? EMPTY_ANATOMIES;
```

因为 `EMPTY_ANATOMIES` 只在模块加载时创建一次，所以每次没有数据时，使用的都是同一个数组引用：

```ts
EMPTY_ANATOMIES === EMPTY_ANATOMIES
```

这样不需要 `useMemo`，也能保持稳定引用。

完整写法：

```ts
const EMPTY_ANATOMIES: AnatomySummary[] = [];

function AnatomyPage() {
  const { result } = useList<AnatomySummary>({
    resource: ResourceName.anatomies,
  });

  const anatomies = result?.data ?? EMPTY_ANATOMIES;
  const total = result?.total ?? 0;

  // ...
}
```

这种写法在“只需要稳定的默认空数组”时很清楚。

注意，不要修改这个共享空数组：

```ts
// 不要这样
anatomies.push(newItem);
```

通常查询数据本身也不应该直接被修改。

还可以冻结它：

```ts
const EMPTY_ANATOMIES: readonly AnatomySummary[] = [];
```

但这会让类型变成只读数组，需要看下游是否接受。

---

## 9. 为什么 `total` 不需要 `useMemo`

```ts
const total = result?.total ?? 0;
```

`total` 是数字，数字是原始值。

对于数字：

```ts
0 === 0 // true
10 === 10 // true
```

不存在“每次创建一个新的数字对象”这种问题。

数组不同：

```ts
[] === [] // false
```

数字相同：

```ts
0 === 0 // true
```

所以没必要写：

```ts
const total = useMemo(
  () => result?.total ?? 0,
  [result?.total],
);
```

这不仅没有实际收益，反而增加了代码复杂度。

---

## 10. 这三种写法怎么选

### 普通场景，推荐最简单的

```ts
const anatomies = result?.data ?? [];
```

适合：

* 只在当前组件里使用；
* 没有放入依赖数组；
* 没有传给 `memo` 子组件；
* 不在意空数组引用变化。

### 明确需要稳定引用

```ts
const anatomies = useMemo(
  () => result?.data ?? [],
  [result?.data],
);
```

适合：

* 传给 `memo` 子组件；
* 作为其他 Hook 的依赖；
* 引用变化会触发额外工作。

### 只想稳定默认空数组

```ts
const EMPTY_ANATOMIES: AnatomySummary[] = [];

const anatomies = result?.data ?? EMPTY_ANATOMIES;
```

适合：

* 不想使用 `useMemo`；
* 只是为了避免反复创建默认空数组。

---

## 最核心的理解

`useMemo` 不只是“缓存昂贵计算”，它还可以缓存一个数组或对象的**引用**。

但是否需要缓存，要看这个引用是否会影响下游：

```ts
// 简单、安全，通常足够
const anatomies = result?.data ?? [];
```

```ts
// 当引用稳定确实有意义时再用
const anatomies = useMemo(
  () => result?.data ?? [],
  [result?.data],
);
```

所以这道题标准答案的重点并不是：

> 数组必须使用 `useMemo`。

而是：

> 对外提供安全数组；需要引用稳定时，再用 `useMemo` 或模块级空数组。
