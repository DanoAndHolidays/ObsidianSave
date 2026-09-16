# Storybook测试
> Last Format Time：9/16/2026 19:24:53

简单说，Storybook 是“组件的独立展厅 + 可交互文档 + 浏览器测试环境”。

它让你不必打开完整业务页面，也不需要手动准备整套应用状态，就可以单独查看和调试一个 React 组件。

以这个文件为例：[CratesFilterToolbar.stories.tsx](G:/Save/Grogramming/CodeForge/daedalus/apps/app/src/pages/CratesPage/_components/CratesFilterToolbar/CratesFilterToolbar.stories.tsx)

---
## 这个文件做了什么
`meta` 部分告诉 Storybook：

- 展示的组件是 `CratesFilterToolbar`
- 在侧边栏中放到 `Pages/CratesPage/Components/CratesFilterToolbar`
- 页面四周添加 padding
- 模拟当前路由为 `/architecture/crates`
- 为依赖 TanStack Router 的组件提供路由环境

下面导出的每个对象都是一个独立展示场景：

```text
export const Base: Story = {
  args: {},
};
```

打开 Storybook 后，侧边栏里会出现 `Base`，并渲染：

```text
<CratesFilterToolbar />
```

`BaseUsage` 则额外展示了组件放在带背景和间距的容器中是什么样子。

你可以通过下面的命令启动：

```text
cd apps/app
bun run storybook
```

然后访问 `http://localhost:6006`。

---
## 为什么它也能在测试时运行
项目专门配置了 Storybook 浏览器测试：

```text
bun run test:storybook
```

而 `bun run quality` 也包含这项检查。

Story 中的：

```text
play: shouldRender
```

会在真实浏览器环境渲染组件后执行。当前项目的 `shouldRender` 主要检查：

- Story 的 DOM 已经连接到页面
- 页面没有显示 Storybook 的渲染错误

所以它目前属于“冒烟测试”：能发现组件导入失败、缺少 Provider、路由环境错误、渲染崩溃等问题，但不会深入验证筛选按钮的业务行为。

---
## Storybook 和单元测试有什么区别
|Storybook Story|Vitest 单元测试|
|---|---|
|给开发者和设计人员直接看|给测试程序执行|
|展示不同 UI 状态|验证明确的业务结果|
|可以手动点击和调试|通过 `expect` 自动判断|
|在真实浏览器中渲染|常见情况下使用模拟环境或服务端渲染|
|也能通过 `play` 编写交互测试|更适合细粒度逻辑和行为测试|

当前组件的单元测试验证了：

- 是否出现 `All` 按钮
- 是否出现 Filter
- URL 查询条件能否正确展示
- 清除筛选入口是否出现

Storybook 则更适合让你直观看到：工具栏到底长什么样、样式是否正常、交互时 UI 有没有问题。

---
## 这个 Story 目前写得好吗
它有用，但目前四个场景基本都在展示相同状态：

- `Base`
- `Default`
- `ShouldRenderToolbar`

三者几乎重复；`BaseUsage` 也只是多了一层容器。它还没有充分发挥 Storybook 的价值。

更有意义的 Story 应该分别展示：

- 无筛选条件
- 有搜索关键词
- 已选择 crate type
- 同时存在多个筛选条件
- 窄屏布局
- 点击清空、输入搜索、选择类型的交互

所以，这个文件现在主要提供了“组件能够在真实浏览器和模拟路由中独立渲染”的保障，但它的场景覆盖还有明显提升空间。