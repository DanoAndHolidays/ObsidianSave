有区别，但当前业务行为基本一致，主要差别是生命周期。

放在 procedure 内：

```ts
.query(async ({ input }) => {
  const service = createAnatomiesModule(db).service;
  return service.list(input);
});
```

每次请求都会重新创建：

- Anatomy DAO
- Draft DAO
- Version DAO
- Repository
- Service 及其内部函数

放在模块顶层：

```ts
const anatomiesService = createAnatomiesModule(db).service;
```

这些对象只在模块加载时创建一次，之后所有请求复用。在 Serverless 环境中通常是“每个实例冷启动创建一次”，而不是全平台永久唯一。

当前放外面更合适，因为：

- Service、DAO 和 Repository 都只是持有 `db` 的无状态闭包。
- 没有保存当前用户、request、session 等请求级数据。
- 没有跨请求共享的可变状态。
- 避免每个 procedure 重复装配同一组依赖。
- Router 内代码更聚焦于校验输入、调用 Service、处理结果。

只有以下情况才应该在请求内部创建：

- Service 需要当前用户或 session。
- Service 保存请求级缓存或 trace ID。
- 每个请求需要独立事务。
- Service 内部存在可变状态。
- 不同请求需要注入不同实现。

当前 Anatomy Service 不属于这些情况，因此外部创建是合理的。

不过更可测试的最终形态是把 Router 本身也做成工厂：

```ts
export const createAnatomiesRouter = function (
  service: AnatomiesService,
) {
  return router({
    list: publicProcedure.query(({ input }) => service.list(input)),
  });
};

export const anatomiesRouter = createAnatomiesRouter(
  createAnatomiesModule(db).service,
);
```

这样生产环境复用一个无状态 Service，测试时又可以注入 mock Service。就当前 COD-292 的范围来说，现有模块顶层创建已经没问题，不必为了生命周期再迁回 procedure 内。