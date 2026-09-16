# CratesFilterToolbar测试笔记
> Last Format Time：9/16/2026 19:24:53

[https://cn.vitest.dev/guide/mocking/modules](https://cn.vitest.dev/guide/mocking/modules)

---
## 测试目的
这个测试主要验证：

> **不同路由筛选条件下，`CratesFilterToolbar` 是否渲染出正确的 UI。**

它测试的是：

```text
路由状态 → 组件 → 渲染结果
```

不是测试点击后是否真的修改 URL、请求数据等完整交互。

---
## 两个测试分别做什么
**1. 默认状态**

```ts
expect(markup).toContain(">All</button>");
expect(markup).toContain('aria-label="Filter"');
```

验证基础筛选栏是否正确渲染：

* 有 `All`
* 有 `Filter` 按钮

**2. 有筛选条件时**

```ts
routeSearch.current = {
  search: "billing",
  type: "service",
};
```

验证 UI 是否显示：

```text
billing
service 类型条件
Clear Filters
```

也就是验证：

```text
?search=billing&type=service
        ↓
CratesFilterToolbar
        ↓
正确展示当前筛选条件
```

---
## `vi.mock` 的作用
这些 mock 都是在**隔离外部依赖**，让测试只关注 `CratesFilterToolbar`。

```ts
Route.useSearch()
```

模拟 URL 查询参数。

```ts
useCratesPageStore()
useStore()
```

模拟 Zustand Store 和事件处理函数。

```ts
useTranslation()
```

模拟 i18n，直接返回翻译 key，避免加载真实翻译配置。

---
## `beforeEach`
```ts
beforeEach(() => {
  routeSearch.current = {
    search: undefined,
    type: undefined,
  };
});
```

每个测试前重置状态，避免测试之间互相污染。

---
## 核心理解
整个测试可以概括成：

```text
Arrange：准备路由状态
   ↓
Act：渲染组件
   ↓
Assert：检查生成的 HTML
```

例如：

```ts
// Arrange
routeSearch.current = {
  search: "billing",
  type: "service",
};

// Act
const markup = renderToStaticMarkup(<CratesFilterToolbar />);

// Assert
expect(markup).toContain("billing");
```

---
## 一句话总结
> 这是一个组件渲染测试，用来保证 `CratesFilterToolbar` 能根据当前路由筛选状态正确显示对应的筛选 UI；`vi.mock` 只是为了隔离路由、Store、i18n 等外部依赖。
