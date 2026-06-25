# Archetype的DAO层
1. 这是一个 DAO（Data Access Object）层文件
2. 使用了 Drizzle ORM
3. 提供了对 `archetypesTable` 的数据库操作
4. 包含 CRUD 操作：list、getById、getByName、create、update、delete

这是一个 **DAO（Data Access Object）层文件**，专门负责与数据库的交互。

---
## 文件定位与职责

| 维度 | 说明 |
|------|------|
| **所属模块** | `@repo/db` 包 |
| **核心职责** | 封装对 `archetypes` 表的所有数据库操作 |
| **依赖** | Drizzle ORM（`drizzle-orm`） |
| **设计模式** | 工厂模式（`createArchetypesDao`） |

---
## 核心功能（CRUD）
### 1. 列表查询（`list`）
支持**分页**和**搜索**：
```typescript
async list({ search, page = 1, pageSize = 20 }) {
  // 搜索条件：name 或 concept 模糊匹配
  if (search) {
    conditions.push(
      or(
        like(archetypesTable.name, `%${search}%`),
        like(archetypesTable.concept, `%${search}%`),
      )
    );
  }
  
  // 分页：LIMIT + OFFSET
  dataQuery.limit(pageSize).offset((page - 1) * pageSize);
}
```

### 2. 单条查询
- `getById(id)`：根据 ID 查询
- `getByName(name)`：根据名称查询（用于唯一性校验）

### 3. 新增/更新/删除
- `create(input)`：插入新记录，返回完整记录
- `update(id, input)`：更新记录，自动更新 `updatedAt`
- `delete(id)`：删除记录

---
## 技术特点
### 1. Drizzle ORM 使用
```typescript
import { eq, like, or, sql } from "drizzle-orm";
```

- `eq`：等于条件
- `like`：模糊匹配
- `or`：或条件
- `sql`：原始 SQL 片段

### 2. 类型安全
```typescript
import { archetypesTable, type ArchetypeInsert, type ArchetypeRecord } from "@repo/db-schema";
```

通过 schema 文件引入表定义和类型，确保类型安全。

### 3. 工厂模式注入
```typescript
export const createArchetypesDao = function (db: Database) {
  return { /* ... */ };
};
```

通过注入数据库连接，实现解耦和可测试性。

## 与 Service 层的关系
```
API层 → Service层（archetypes-service.ts） → DAO层（archetypes-dao.ts） → 数据库
                                                    ↑
                                         本文件：专门操作 archetypes 表
```

**Service 层**调用**DAO 层**来完成数据访问，例如：
```typescript
// Service 层代码（archetypes-service.ts）
const archetypesDao = createArchetypesDao(db);

const existing = await archetypesDao.getByName(input.name);
if (existing) {
  return err({ type: "invalid_input", message: "Name already exists" });
}
```

---
## 总结
这个文件是 **Archetype 数据访问层**，负责：
1. 封装所有对 `archetypes` 表的 SQL 操作
2. 提供类型安全的数据库接口
3. 实现分页、搜索等常用查询功能
4. 作为 Service **层和数据库之间的桥梁**