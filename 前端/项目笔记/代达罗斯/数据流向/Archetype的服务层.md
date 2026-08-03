# Archetype的服务层

[[引入Archetype]]
[[用neverthrow进行错误处理]]

---
## 简单分析
这是一个 Archetype（原型/模板）服务文件，主要功能包括：
1. 定义了错误类型和服务错误结构
2. 定义了各种类型（ConditionInput, ArchetypeInput等）
3. 创建了一个服务工厂函数 createArchetypesService
4. 提供了 CRUD 操作：list, getById, create, update, delete
5. 包含条件验证、循环依赖检测等业务逻辑

| 维度 | 说明 |
|------|------|
| **所属模块** | `@repo/services` 包 |
| **核心职责** | 封装 Archetype 的业务逻辑和数据访问 |
| **设计模式** | 工厂模式（`createArchetypesService`） |
| **错误处理** | 使用 `neverthrow` 的 `Result` 模式 |

---
## 核心功能
### 1. 数据模型定义
```typescript
// 条件输入（来自API）
type ConditionInput = {
  id: string;
  type: "text" | "archetype_ref";  // 文本条件或原型引用
  value: string;
  sortOrder: number;
  dependencies: string[];          // 依赖的其他原型ID
};

// 原型输入
type ArchetypeInput = {
  id: string;
  name: string;
  concept: string;
  scope: "project" | "repository" | "crate" | "page" | "service";
  description: string;
  conditions: ConditionInput[];     // 关联的条件列表
};
```

### 2. 服务接口（CRUD）

| 方法 | 功能 | 返回值 |
|------|------|--------|
| `list` | 分页查询原型列表 | `Result<{data, total}, ServiceError>` |
| `getById` | 根据ID查询单个原型 | `Result<ArchetypeWithConditions | null, ServiceError>` |
| `create` | 创建新原型 | `Result<ArchetypeWithConditions, ServiceError>` |
| `update` | 更新原型 | `Result<ArchetypeWithConditions, ServiceError>` |
| `delete` | 删除原型（含引用检查） | `Result<ArchetypeWithConditions, ServiceError>` |

### 3. 核心业务逻辑
#### 条件验证（`validateConditions`）
- 至少包含一个条件
- 文本条件值不能为空
- 原型引用条件必须有依赖
- 不能自引用
- 依赖的原型必须存在

#### 循环依赖检测（`detectCycle`）
使用 **DFS 算法**检测原型引用是否形成闭环，防止无限循环：
```typescript
const detectCycle = async function (nodeId: string, conditions: ConditionInput[]) {
  const dfs = async function (currentId: string, path: Set<string>): Promise<boolean> {
    if (path.has(currentId)) return true;  // 发现循环
    path.add(currentId);
    // 递归检查依赖...
  };
};
```

#### 删除保护
删除前检查是否有其他原型引用当前原型：
```typescript
const refs = await conditionsDao.findReferencingArchetypes(id);
if (refs.length > 0) {
  return err({
    type: ServiceErrorType.invalidInput,
    message: `Cannot delete: referenced by ${refs.length} archetype(s)`
  });
}
```

---
## 架构设计特点
### 1. 分层架构
```
API层 → Service层（本文件） → DAO层 → 数据库
```

### 2. 依赖注入
通过工厂函数注入数据库连接：
```typescript
export const createArchetypesService = function (db: Database) {
  const archetypesDao = createArchetypesDao(db);
  // ...
};
```

### 3. 错误处理模式
使用 `neverthrow` 库的 `Result` 类型，避免 try-catch：
```typescript
async create(input): Promise<Result<ArchetypeWithConditions, ServiceError>> {
  if (!input.name?.trim()) {
    return err({ type: "invalid_input", message: "Name is required" });
  }
  return ok(archetype);
}
```

### 4. 数据组装
通过 `enrichConditions` 将条件与依赖关系关联：
```typescript
const enrichConditions = async function (conditions) {
  const dependencyMap = await conditionsDao.listDependencies(...);
  return conditions.map(c => ({
    ...c,
    dependencies: dependencyMap.get(c.id) ?? []
  }));
};
```

---
## 具体实现
schema[ˈskiːmə] 斯ki马
```ts
import { err, ok, type Result } from "neverthrow";
import {
  createArchetypesDao,
  createArchetypeConditionsDao,
} from "@repo/db/dao";
import {
  type ArchetypeInsert,
  type ArchetypeRecord,
  type ArchetypeConditionRecord,
} from "@repo/db-schema";
import { createLogger } from "@repo/logger";
import type { Database } from "@repo/db";

const log = createLogger("archetypes-service");

const ServiceErrorType = {
  notFound: "not_found",
  invalidInput: "invalid_input",
} as const;

export type ServiceError = {
  type: (typeof ServiceErrorType)[keyof typeof ServiceErrorType];
  message: string;
};

// Condition input from API (archetypeId assigned by service)
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

type ConditionWithDependencies = ArchetypeConditionRecord & {
  dependencies: string[];
};

type ArchetypeWithConditions = ArchetypeRecord & {
  conditions: ConditionWithDependencies[];
};
```

上下是一个文件，便于阅读就断开了：
```ts
export const createArchetypesService = function (db: Database) {
```

这里的代码是注入数据库连接，两张表[[Archetype的DAO层]]：
```ts
  const archetypesDao = createArchetypesDao(db);
  const conditionsDao = createArchetypeConditionsDao(db);
```

```ts
  // 条件与依赖关系关联
  const enrichConditions = async function (
    conditions: ArchetypeConditionRecord[],
  ): Promise<ConditionWithDependencies[]> {
    if (conditions.length === 0) {
      return [];
    }

    const dependencyMap = await conditionsDao.listDependencies(
      conditions.map((c) => c.id),
    );

    return conditions.map((c) => ({
      ...c,
      dependencies: dependencyMap.get(c.id) ?? [],
    }));
  };

  // 加载对应的conditions
  const loadConditions = async function (
    items: ArchetypeRecord[],
  ): Promise<ArchetypeWithConditions[]> {
    const result: ArchetypeWithConditions[] = [];
    for (const item of items) {
      const conditions = await conditionsDao.listByArchetype(item.id);
      result.push({ ...item, conditions: await enrichConditions(conditions) });
    }

    return result;
  };

  // 单个加载
  const loadSingle = async function (
    item: ArchetypeRecord,
  ): Promise<ArchetypeWithConditions> {
    const conditions = await conditionsDao.listByArchetype(item.id);

    return { ...item, conditions: await enrichConditions(conditions) };
  };

  // 收集依赖
  const collectDependenciesFromDb = async function (
    archetypeId: string,
  ): Promise<string[]> {
    const conditions = await conditionsDao.listByArchetype(archetypeId);
    if (conditions.length === 0) {
      return [];
    }

    const dependencyMap = await conditionsDao.listDependencies(
      conditions.map((c) => c.id),
    );

    return [...new Set([...dependencyMap.values()].flat())];
  };

  // condition合法性检验
  const validateConditions = async function (
    conditions: ConditionInput[],
    currentArchetypeId: string,
  ): Promise<ServiceError | null> {
    // 1. At least one condition
    if (conditions.length === 0) {
      return {
        type: ServiceErrorType.invalidInput,
        message: "At least one condition is required",
      };
    }

    // 2. Validate each condition
    for (const c of conditions) {
      if (c.type === "text" && !c.value.trim()) {
        return {
          type: ServiceErrorType.invalidInput,
          message: "Text condition value must not be empty",
        };
      }

      if (c.type === "archetype_ref") {
        const deps = c.dependencies ?? [];
        if (deps.length === 0) {
          return {
            type: ServiceErrorType.invalidInput,
            message: "Archetype-ref condition must have at least one dependency",
          };
        }

        // Self-reference check
        if (deps.includes(currentArchetypeId)) {
          return {
            type: ServiceErrorType.invalidInput,
            message: "An archetype cannot reference itself",
          };
        }

        // Validate every dependency points to an existing archetype
        for (const depId of deps) {
          const target = await archetypesDao.getById(depId);
          if (!target) {
            return {
              type: ServiceErrorType.invalidInput,
              message: `Referenced archetype not found: ${depId}`,
            };
          }
        }
      }
    }

    // 3. Cycle detection (DAG check for condition dependencies)
    const cycleError = await detectCycle(currentArchetypeId, conditions);
    if (cycleError) {
      return cycleError;
    }

    return null;
  };
```

这里是使用深度优先遍历去找循环引用的：
```ts
  // DFS cycle detection — walk the graph of condition dependencies
  // to ensure no path exists from any referenced archetype back to currentArchetypeId
  const detectCycle = async function (
    nodeId: string,
    conditions: ConditionInput[],
  ): Promise<ServiceError | null> {
    const dfs = async function (
      currentId: string,
      path: Set<string>,
    ): Promise<boolean> {
      if (path.has(currentId)) {
        return true;
      }
      path.add(currentId);

      const deps =
        currentId === nodeId
          ? [...new Set(conditions.flatMap((c) => c.dependencies ?? []))]
          : await collectDependenciesFromDb(currentId);

      for (const depId of deps) {
        if (await dfs(depId, path)) {
          return true;
        }
      }

      path.delete(currentId);

      return false;
    };

    const topLevelDeps = [
      ...new Set(conditions.flatMap((c) => c.dependencies ?? [])),
    ];

    for (const depId of topLevelDeps) {
      if (await dfs(depId, new Set())) {
        return {
          type: ServiceErrorType.invalidInput,
          message: "Circular archetype reference detected",
        };
      }
    }

    return null;
  };

```

保存condition依赖：
```ts
  const saveConditionDependencies = async function (
    conditions: ArchetypeConditionRecord[],
    inputs: ConditionInput[],
  ): Promise<void> {
    const inputMap = new Map(inputs.map((c) => [c.id, c]));

    for (const condition of conditions) {
      const input = inputMap.get(condition.id);
      const deps = input?.dependencies ?? [];
      await conditionsDao.replaceDependencies(condition.id, deps);
    }
  };
```

这个函数的返回值，用来crud的函数们：
```ts
  return {
    async list({
      search,
      page,
      pageSize,
    }: {
      search?: string;
      page?: number;
      pageSize?: number;
    } = {}): Promise<
      Result<{ data: ArchetypeWithConditions[]; total: number }, ServiceError>
    > {
      const result = await archetypesDao.list({ search, page, pageSize });
      const items = await loadConditions(result.data);

      return ok({ data: items, total: result.total });
    },

    async getById(
      id: string,
    ): Promise<Result<ArchetypeWithConditions | null, ServiceError>> {
      const item = await archetypesDao.getById(id);
      if (!item) {
        return ok(null);
      }

      const enriched = await loadSingle(item);

      return ok(enriched);
    },

    async create(
      input: ArchetypeInput,
    ): Promise<Result<ArchetypeWithConditions, ServiceError>> {
      if (!input.name?.trim()) {
        return err({
          type: ServiceErrorType.invalidInput,
          message: "Name is required",
        });
      }

      // Name uniqueness
      const existing = await archetypesDao.getByName(input.name);
      if (existing) {
        return err({
          type: ServiceErrorType.invalidInput,
          message: `An archetype with name "${input.name}" already exists`,
        });
      }

      const condError = await validateConditions(
        input.conditions,
        input.id,
      );
      if (condError) {
        return err(condError);
      }

      const archetype = await archetypesDao.create(input as ArchetypeInsert);
      const conditions = await conditionsDao.bulkReplace(
        archetype.id,
        input.conditions.map((c) => ({
          id: c.id,
          type: c.type,
          value: c.value,
          sortOrder: c.sortOrder,
          archetypeId: archetype.id,
        })),
      );

      await saveConditionDependencies(conditions, input.conditions);

      log.info("Archetype created", { id: archetype.id });

      return ok({ ...archetype, conditions: await enrichConditions(conditions) });
    },

    async update(
      id: string,
      patch: Partial<ArchetypeInput>,
    ): Promise<Result<ArchetypeWithConditions, ServiceError>> {
      const existing = await archetypesDao.getById(id);
      if (!existing) {
        return err({
          type: ServiceErrorType.notFound,
          message: `Archetype ${id} not found`,
        });
      }

      // Name uniqueness (if name changed)
      if (patch.name && patch.name !== existing.name) {
        const dup = await archetypesDao.getByName(patch.name);
        if (dup) {
          return err({
            type: ServiceErrorType.invalidInput,
            message: `An archetype with name "${patch.name}" already exists`,
          });
        }
      }

      // Validate conditions if provided
      if (patch.conditions) {
        const condError = await validateConditions(patch.conditions, id);
        if (condError) {
          return err(condError);
        }
      }

      const updated = await archetypesDao.update(id, patch as Partial<ArchetypeInsert>);
      const result = updated ?? existing;

      const conditions = patch.conditions
        ? await conditionsDao.bulkReplace(
            id,
            patch.conditions.map((c) => ({
              id: c.id,
              type: c.type,
              value: c.value,
              sortOrder: c.sortOrder,
              archetypeId: id,
            })),
          )
        : await conditionsDao.listByArchetype(id);

      if (patch.conditions) {
        await saveConditionDependencies(conditions, patch.conditions);
      }

      log.info("Archetype updated", { id });

      return ok({ ...result, conditions: await enrichConditions(conditions) });
    },

```

仔细看来这个delete所使用的能力全部是由其下的DAO层提供的：
```ts
    async delete(
      id: string,
    ): Promise<Result<ArchetypeWithConditions, ServiceError>> {
      const existing = await archetypesDao.getById(id);
      if (!existing) {
        return err({
          type: ServiceErrorType.notFound,
          message: `Archetype ${id} not found`,
        });
      }

      // Delete protection: check if any other archetype references this one
      const refs = await conditionsDao.findReferencingArchetypes(id);
      if (refs.length > 0) {
        const names = refs.map((r) => r.name).join(", ");

        return err({
          type: ServiceErrorType.invalidInput,
          message: `Cannot delete: referenced by ${refs.length} archetype(s): ${names}`,
        });
      }

      const conditions = await conditionsDao.listByArchetype(id);
      await archetypesDao.delete(id);

      log.info("Archetype deleted", { id });

      return ok({ ...existing, conditions: await enrichConditions(conditions) });
    },
  };
};

export type ArchetypesService = ReturnType<typeof createArchetypesService>;
```

这里是推断出来的类型，可以看到里面的各种服务接口（各种CRUD）：
```ts
type ArchetypesService = {
 list({ search, page, pageSize, }?: {
	 search?: string | undefined;
	 page?: number | undefined;
	 pageSize?: number | undefined;
 }): Promise<Result<{ data: ArchetypeWithConditions[]; total: number }, ServiceError>>;
 
 getById(id: string): Promise<Result<ArchetypeWithConditions | null, ServiceError>>;
 
 create(input: ArchetypeInput): Promise<Result<ArchetypeWithConditions, ServiceError>>;
 
 update(id: string, patch: Partial<ArchetypeInput>):
 Promise<Result<ArchetypeWithConditions, ServiceError>>;
 
 delete(id: string): Promise<Result<ArchetypeWithConditions, ServiceError>>;
}
```

![[Pasted image 20260624230829.png]]

err与ok是会反应在接口的返回结果中的：
![[Pasted image 20260624230916.png]]

日志可以在控制容台看见：
![[Pasted image 20260624231710.png]]

