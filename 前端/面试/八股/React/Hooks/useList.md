# useList
Refine 在这里本质上是一个 "规范化的数据访问门面"——它不强耦合于任何 UI 组件库，只是提供了一套统一的 hook 接口来约束前端如何获取和变更数据，确保所有数据流都经过同一个通道，便于维护和测试。


  CratesPageContent.tsx

  - 从 useList 额外解构了 query
  - 引入已有的 LoadingState 组件
  - 渲染逻辑改为三层：query?.isLoading → 显示加载动画 → crates.length === 0 →显示空状态 → 显示表格

  ArchetypesPageContent.tsx

  - 同样的改动：解构 query、引入 LoadingState、三层条件渲染

  现在这两个列表页在数据首次加载时会显示居中的旋转加载动画（Loader2 图标），数据加载完成后才显示表格或空状态，与项目中 CrateDetailPage、ArchetypeDetailPage等页面使用相同的 LoadingState 组件。