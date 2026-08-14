# DataBase
> Last Format Time：7/14/2026 20:22:22

这种报错一般是云端的Neon数据库没有推送新加的字段，导致请求失败：
```json
{
    "error": {
        "json": {
            "message": "Failed query: select \"id\", \"name\", \"type\", \"responsibility\", \"repository_id\", \"metadata\", \"created_at\", \"updated_at\" from \"crates\" order by \"crates\".\"created_at\" limit $1\nparams: 20",
            "code": -32603,
            "data": {
                "code": "INTERNAL_SERVER_ERROR",
                "httpStatus": 500,
                "stack": "Error: Failed query: select \"id\", \"name\", \"type\", \"responsibility\", \"repository_id\", \"metadata\", \"created_at\", \"updated_at\" from \"crates\" order by \"crates\".\"created_at\" limit $1\nparams: 20\n    at PostgresJsPreparedQuery.queryWithCache (file:///G:/Save/Grogramming/CodeForge/daedalus/node_modules/.bun/drizzle-orm@0.45.2+33391f1c048f5c2a/node_modules/drizzle-orm/pg-core/session.js:41:15)\n    at processTicksAndRejections (node:internal/process/task_queues:105:5)\n    at file:///G:/Save/Grogramming/CodeForge/daedalus/node_modules/.bun/drizzle-orm@0.45.2+33391f1c048f5c2a/node_modules/drizzle-orm/postgres-js/session.js:37:20\n    at async Promise.all (index 0)\n    at Object.list (G:/Save/Grogramming/CodeForge/daedalus/packages/db/src/dao/crates-dao.ts:43:41)\n    at Object.list (G:/Save/Grogramming/CodeForge/daedalus/packages/services/src/crates-service.ts:114:22)\n    at G:/Save/Grogramming/CodeForge/daedalus/apps/app/src/integrations/trpc/routers/crates.ts:18:22\n    at resolveMiddleware (file:///G:/Save/Grogramming/CodeForge/daedalus/node_modules/.bun/@trpc+server@11.17.0+ca84541ac88a3075/node_modules/@trpc/server/dist/initTRPC-BRf4imah.mjs:221:17)\n    at callRecursive (file:///G:/Save/Grogramming/CodeForge/daedalus/node_modules/.bun/@trpc+server@11.17.0+ca84541ac88a3075/node_modules/@trpc/server/dist/initTRPC-BRf4imah.mjs:256:18)\n    at callRecursive (file:///G:/Save/Grogramming/CodeForge/daedalus/node_modules/.bun/@trpc+server@11.17.0+ca84541ac88a3075/node_modules/@trpc/server/dist/initTRPC-BRf4imah.mjs:256:18)",
                "path": "crates.list"
            }
        }
    }
}
```