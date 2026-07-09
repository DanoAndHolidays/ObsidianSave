# LoadingState&useList的组合
  fix: 为 Crate/Archetype 列表页添加加载状态，修复 CrateDetailPage 的 hooks 顺序错误

  问题:
  1. CratesPage 和 ArchetypesPage 在数据尚未拉取时直接展示空表，用户看不到任何加载反馈
  2. CrateDetailPageContent 存在 React Rules of Hooks 违规：早期 return
     出现在 useMemo 之前，导致两次渲染之间 hook 数量不一致而报错

  修改:
  - CratesPageContent: 从 useList 中解构 query，在 query.isLoading 时
    渲染 LoadingState 组件（复用自 @/components/ui/loading-state）
  - ArchetypesPageContent: 同上
  - CrateDetailPageContent: 将 boundArchetypes 的 useMemo 及所依赖的普通
    变量移至早期 return 之前，确保每次渲染 hook 调用顺序一致

  影响页面: /architecture/crates、/architecture/archetypes、/architecture/crates/$id