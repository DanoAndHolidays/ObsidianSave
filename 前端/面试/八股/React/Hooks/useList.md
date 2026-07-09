# useList


  CratesPageContent.tsx

  - 从 useList 额外解构了 query
  - 引入已有的 LoadingState 组件
  - 渲染逻辑改为三层：query?.isLoading → 显示加载动画 → crates.length === 0 →显示空状态 → 显示表格

  ArchetypesPageContent.tsx

  - 同样的改动：解构 query、引入 LoadingState、三层条件渲染

  现在这两个列表页在数据首次加载时会显示居中的旋转加载动画（Loader2 图标），数据加载完成后才显示表格或空状态，与项目中 CrateDetailPage、ArchetypeDetailPage等页面使用相同的 LoadingState 组件。