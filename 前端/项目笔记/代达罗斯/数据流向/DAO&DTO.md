# DAO&DTO
用户问的是 DAO 与 DTO 的区别。这是一个概念性的问题，不需要查看代码，我可以直接解释这两个概念的区别。

DAO (Data Access Object) 和 DTO (Data Transfer Object) 是两种不同的设计模式，有着不同的职责：

1. DAO (数据访问对象)：
   - 职责：封装数据库访问逻辑
   - 作用：提供对数据库的 CRUD 操作
   - 例子：我们刚才看到的 `archetypes-dao.ts`

2. DTO (数据传输对象)：
   - 职责：在不同层之间传输数据
   - 作用：封装需要传输的数据结构
   - 例子：`ArchetypeInput`, `ConditionInput` 等类型

我需要清晰地解释这两个概念的区别，最好用表格对比，再结合代码示例来说明。
DAO 和 DTO 是两种完全不同的设计模式，职责和用途有着本质区别。

---
## 核心区别对比

| 维度 | **DAO（Data Access Object）** | **DTO（Data Transfer Object）** |
|------|-------------------------------|---------------------------------|
| **本质** | 行为对象（行为/操作） | 数据对象（数据结构） |
| **职责** | 封装数据库访问逻辑 | 在不同层之间传输数据 |
| **关注点** | *如何*访问数据 | *传输什么*数据 |
| **形态** | 包含方法的对象（类/函数） | 纯数据结构（接口/类型） |
| **生命周期** | 服务级别（长期存在） | 请求级别（一次性传输） |

---
## 结合项目代码理解
### DAO 示例（行为层）
```typescript
// archetypes-dao.ts - 提供数据库操作方法
export const createArchetypesDao = function (db: Database) {
  return {
    // 行为：如何从数据库获取数据
    async getById(id: string): Promise<ArchetypeRecord | undefined> {
      const rows = await db
        .select()
        .from(archetypesTable)
        .where(eq(archetypesTable.id, id))
        .limit(1);
      return rows[0];
    },
    
    // 行为：如何插入数据
    async create(input: ArchetypeInsert): Promise<ArchetypeRecord> {
      const rows = await db.insert(archetypesTable).values(input).returning();
      return rows[0]!;
    }
  };
};
```

### DTO 示例（数据结构）
```typescript
// 用于 API 输入的数据结构
export type ConditionInput = {
  id: string;
  type: "text" | "archetype_ref";
  value: string;
  sortOrder: number;
  dependencies: string[];
};

export type ArchetypeInput = {
  id: string;
  name: string;
  concept: string;
  scope: "project" | "repository" | "crate" | "page" | "service";
  description: string;
  conditions: ConditionInput[];
};
```

## 在分层架构中的位置
```
┌─────────────────────────────────────────────────────────────┐
│                     API Layer（控制器）                      │
│  接收请求 → 使用 DTO 定义输入格式 → 调用 Service              │
├─────────────────────────────────────────────────────────────┤
│                   Service Layer（业务逻辑）                   │
│  业务规则验证 → 调用 DAO 操作数据库 → 返回 DTO                │
├─────────────────────────────────────────────────────────────┤
│                     DAO Layer（数据访问）                     │
│  封装 SQL → 执行数据库操作 → 返回 Entity/Record               │
├─────────────────────────────────────────────────────────────┤
│                      Database（数据库）                       │
└─────────────────────────────────────────────────────────────┘
```

---
## 典型使用场景

| 场景 | 使用 DAO | 使用 DTO |
|------|----------|----------|
| 查询数据库 | ✅ | ❌ |
| 插入/更新记录 | ✅ | ❌ |
| API 请求参数 | ❌ | ✅ |
| API 响应数据 | ❌ | ✅ |
| 层间数据传递 | ❌ | ✅ |

---
## 总结
- **DAO 是动词**：它做事情（查询、插入、更新、删除）
- **DTO 是名词**：它是数据的载体，本身不做任何事情

在这个项目中：
- `archetypes-dao.ts` 是 **DAO**：提供对数据库的操作方法
- `ArchetypeInput`、`ConditionInput` 是 **DTO**：定义 API 输入的数据结构