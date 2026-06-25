# 数据库迁移 Drizzle 迁移文件说明

---
## 三个核心文件
每次运行 `bun run db:generate` 后，Drizzle Kit 会在 `apps/app/drizzle/` 下生成三个文件：

| 文件 | 位置 | 作用 |
|------|------|------|
| `_journal.json` | `drizzle/meta/` | 迁移目录，记录所有迁移的序号、时间戳和标签 |
| `XXXX_snapshot.json` | `drizzle/meta/` | Schema 快照，记录本次迁移后数据库的完整结构 |
| `XXXX_tag.sql` | `drizzle/` | 实际可执行的 SQL 迁移脚本 |

---
## 1. `_journal.json` — 迁移日志
```json
{
  "version": "7",
  "dialect": "postgresql",
  "entries": [
    {
      "idx": 6,
      "version": "7",
      "when": 1782377985932,
      "tag": "0006_friendly_pyro",
      "breakpoints": true
    }
  ]
}
```

**各字段含义：**
- **`idx`** — 迁移序号，从 0 开始递增
- **`version`** — journal 格式版本号
- **`when`** — Unix 时间戳（毫秒），标记迁移创建时间
- **`tag`** — 迁移标签名，对应同名的 `.sql` 和 `_snapshot.json` 文件。格式为 `序号_随机形容词_随机名词`，由 Drizzle Kit 自动生成，无业务语义
- **`breakpoints`** — 标记为断点。Drizzle Kit 生成新迁移时，以最近的 breakpoint 为基准进行 diff

## 2. `XXXX_snapshot.json` — Schema 快照
记录迁移执行后数据库的**完整结构**，包含所有表、列、索引、外键、唯一约束、检查约束等元数据。
```json
{
  "id": "8925096c-...",
  "prevId": "928723d8-...",
  "version": "7",
  "dialect": "postgresql",
  "tables": { /* 所有表的完整定义 */ },
  "enums": {},
  "schemas": {},
  "sequences": {},
  "roles": {},
  "policies": {},
  "views": {}
}
```

**关键字段 `id` 和 `prevId`：** 两者组成一条链，`id` 是当前快照的 UUID，`prevId` 指向上一个快照的 UUID。Drizzle Kit 通过此链验证迁移历史的连续性。

## 3. `XXXX_tag.sql` — SQL 迁移脚本
本次迁移要执行的 SQL DDL 语句。例如：
```sql
CREATE TABLE "crates" (
    "id"             text PRIMARY KEY,
    "name"           text UNIQUE NOT NULL,
    ...
);
```

---
## 增量迁移流程
```
你修改了 Drizzle schema 代码（packages/db-schema/src/tables/）
        ↓
bun run db:generate
        ↓
Drizzle Kit 读取最近的 snapshot（如 0006_snapshot.json）
        ↓
与你当前的 schema 代码做 diff
        ↓
生成增量 SQL（如 0007_xxx.sql）—— 只包含变更部分
        ↓
写入新的 snapshot（0007_snapshot.json）供下次 diff 使用
        ↓
在 _journal.json 中追加一条新 entry
```

---
## 类比
可以把这三个文件理解为一个版本控制系统的不同部分：

| Drizzle 文件 | Git 类比 |
|-------------|---------|
| `_journal.json` | `git log --oneline` |
| `XXXX_snapshot.json` | 某次 commit 后的完整文件树快照 |
| `XXXX_tag.sql` | 某次 commit 的 diff / patch |
