# Barrel Export

---
## 场景分析
### 桶导出定义
桶导出（Barrel Export）是一种模块组织模式：每个目录下的 `index.ts` 文件**仅**负责将该目录中所有公共模块通过 `export *` 统一 re-export，对外暴露单一入口。

```ts
目录结构：
  components/
    Button.tsx          ← 组件实现
    Modal.tsx           ← 组件实现
    Tooltip.tsx         ← 组件实现
    index.ts            ← 桶（barrel）：export * from './Button' ...

使用时：
  import { Button, Modal, Tooltip } from '@/components'
  // 而非：
  import { Button } from '@/components/Button'
  import { Modal } from '@/components/Modal'
```

### 设计原则
飞书文档 + 现有 Skill（`barrel-export-best-practice`）存在8 条检查规则：

| # | 原则 | 核心要求 | 可判定性 |
|---|------|---------|---------|
| 1 | 每个目录有 index 文件 | 存在导出文件的目录必须有 `index.ts` | **脚本化**（glob 检查） |
| 2 | 仅包含 re-export 语句 | `index.ts` 只允许 `export * from './...'`，不含业务逻辑 | **脚本化**（AST 分析） |
| 3 | 禁止默认导出 | 桶导出文件中禁止 `export default` | **脚本化**（AST 分析） |
| 4 | 使用相对路径 | 导出路径必须以 `./` 或 `../` 开头 | **脚本化**（字符串匹配） |
| 5 | 无循环依赖 | 桶导出文件不得与被导出模块形成循环引用 | **脚本化**（依赖图分析） |
| 6 | 导出项与实际文件一致 | 导出的模块名必须对应真实存在的文件 | **脚本化**（文件系统校验） |
| 7 | 解决命名冲突 | 同名导出冲突时在原文件重命名 | **LLM 评估**（需语义判断） |
| 8 | 无重复导出 | 同一标识符不得被多次导出 | **脚本化**（去重检查） |

### 与其他 Archetype 的交叉、区别
桶导出作为基础设施模式，会与多个 Archetype 存在约束关系。

桶导出与 Form 等组件领域分析有本质不同：

| 维度        | 组件领域       | 桶导出                                                                             |
| --------- | ---------- | ------------------------------------------------------------------------------- |
| **作用域**   | 特定组件领域     | 全项目跨领域                                                                          |
| **约束对象**  | 具体组件实现     | `index.ts` 文件（每个目录）                                                             |
| **工具化程度** | 部分可脚本化     | **高度可脚本化**（barrelsby 自动生成、oxlint 规则检查）                                          |
| **违规影响**  | 局部         | 全局（导入路径混乱、循环依赖风险）                                                               |

---
## Crate 设计
### Crate 分层
```
barrel-standard (utility)  ←── 规范定义层
    │
    │ 规范驱动
    ▼
barrel-checker (utility)   ←── 检查执行层
    │
    │ 发现问题 → 触发修复
    ▼
barrel-generator (utility) ←── 生成修复层
```

| 层级 | 说明 |
|------|------|
| **规范层** | 定义桶导出的规则和标准（文档/配置） |
| **检查层** | 自动化检查桶导出合规性（CLI/oxlint 规则） |
| **生成层** | 自动生成/修复桶导出文件（barrelsby / check-barrel-export skill） |

### Crate 详细定义
#### Crate A: `barrel-standard`

| 字段 | 值 |
|------|-----|
| **name** | `barrel-standard` |
| **type** | `utility` |
| **responsibility** | 桶导出规范的权威定义：8 条检查规则的详细描述、合规示例与反模式文档、与其他 Archetype（no-re-export、one-component-per-file）的边界约定、`export *` vs `export { }` 的唯一例外场景（命名冲突时的具名重导出） |
| **metadata** | `{"rules": 8, "scriptable": 7, "tools": ["barrelsby", "check-barrel-export"], "related_archetypes": ["no-re-export-best-practice", "one-component-per-file-best-practice", "component-unit-best-practice"]}` |

**包含内容**：
- 桶导出规范文档（标准化 `.md`）
- 合规示例代码（`best-practice-examples/` 目录）
- 反模式目录（`anti-patterns/` 目录）
- 与其他 Archetype 的交叉引用映射

#### Crate B: `barrel-checker`

| 字段 | 值 |
|------|-----|
| **name** | `barrel-checker` |
| **type** | `utility` |
| **responsibility** | 桶导出合规性自动化检查引擎：基于 oxlint 自定义规则实现的静态检查（规则 1-6、8）、`check-barrel-export` skill 的自动化执行逻辑、检查报告生成（违规文件路径 + 违规类型 + 修复建议） |
| **metadata** | `{"implementation": ["oxlint-custom-rules", "skill-check-barrel-export"], "coverage": "7/8 rules (87.5%)", "uncovered": "rule-7 (naming conflict resolution)"}` |

**包含内容**：
- oxlint 自定义规则插件
- `check-barrel-export` skill 执行脚本
- 检查结果的数据结构

#### Crate C: `barrel-generator`

| 字段 | 值 |
|------|-----|
| **name** | `barrel-generator` |
| **type** | `utility` |
| **responsibility** | 桶导出文件自动生成与修复：barrelsby CLI 的集成封装、`--delete` 模式自动清理过期导出、"检查 + 修复" 一键流水线（先运行 barrel-checker 发现问题，再运行 barrel-generator 自动修复） |
| **metadata** | `{"package": "barrelsby", "modes": ["generate", "delete", "check-and-fix"], "integration": "npm scripts / bun run"}` |

**包含内容**：
- `barrelsby` 配置模板
-  npm script 封装


---
## Archetype 契约定义
### 总览

| Archetype                         | Scope   | 约束对象（目标 Crate）                                        | Condition 数 | 说明        |
| --------------------------------- | ------- | ----------------------------------------------------- | ----------- | --------- |
| **`barrel-export-best-practice`** | `crate` | `barrel-standard`、`barrel-checker`、`barrel-generator` | 8           | 桶导出文件组织契约 |

### 完整定义
**Name**: `barrel-export-best-practice`
**Scope**: `crate`
**Concept**: 确保每个有导出文件的目录通过 `index.ts` 桶文件提供统一入口，桶文件仅做 `export *` re-export，不含业务逻辑、默认导出、别名路径，且不引入循环依赖

##### C-1: 每个目录有 index 文件
- **ID**: `c-barrel-directory-has-index`
- **类型**: `text`
- **排序**: 1
- **条件内容**:
  ```
  存在导出文件（含 .ts/.tsx 模块文件）的目录必须包含 index.ts 桶导出文件。
  仅含非导出资源（如 __tests__/、stories/、assets/）的目录可豁免。
  空目录或仅含 README.md 的目录可豁免。

  ❌ 违规:
    components/
      Button.tsx
      Modal.tsx
      // 无 index.ts

  ✅ 正确:
    components/
      Button.tsx
      Modal.tsx
      index.ts  ← export * from './Button'; export * from './Modal'
  ```

##### C-2: 仅包含 re-export 语句
- **ID**: `c-barrel-re-export-only`
- **类型**: `text`
- **排序**: 2
- **条件内容**:
  ```
  index.ts 文件只允许包含 `export * from './...'` 语句。禁止出现：
  - 变量声明（const/let）
  - 函数/类定义（function/class）
  - import 语句后跟使用（如 import + console.log）
  - 任何形式的业务逻辑

  唯一的例外：当 `export *` 导致命名冲突时，可在原模块文件中使用具名重导出
  （export { Foo as FooA }），而非在 index.ts 中解决。

  ❌ 违规:
    export const API_BASE = '/api/v1'
    export * from './Button'

  ❌ 违规:
    export { Button } from './Button'  // 显式命名导出

  ✅ 正确:
    export * from './Button'
    export * from './Modal'
  ```

##### C-3: 禁止默认导出
- **ID**: `c-barrel-no-default-export`
- **类型**: `text`
- **排序**: 3
- **条件内容**:
  ```
  桶导出文件中禁止使用 export default。所有模块必须通过命名导出的方式被 re-export。
  如果原模块使用了 export default，必须先在原模块改为命名导出，
  然后在 index.ts 中使用 `export * from './...'`。

  ❌ 违规:
    export * from './Button'
    export default Button

  ✅ 正确:
    // Button.tsx 中：export { Button }
    // index.ts 中：export * from './Button'
  ```

##### C-4: 使用相对路径
- **ID**: `c-barrel-relative-path`
- **类型**: `text`
- **排序**: 4
- **条件内容**:
  ```
  桶导出中的所有路径必须以 `./` 或 `../` 开头。禁止使用：
  - 别名路径（如 `@/components/Button`）
  - 绝对路径（如 `src/components/Button`）
  - 包名路径（如 `@repo/ui/Button`）

  原因：别名路径在 monorepo 中可能指向不同包的实际路径，
  导致桶导出文件不可移植。

  ❌ 违规:
    export * from '@/components/Button'

  ✅ 正确:
    export * from './Button'
  ```

##### C-5: 无循环依赖
- **ID**: `c-barrel-no-circular-dependency`
- **类型**: `text`
- **排序**: 5
- **条件内容**:
  ```
  桶导出文件不得与被导出模块形成循环引用。即：
  index.ts export → A.ts，而 A.ts import → 同级或上级的 index.ts。

  循环依赖的典型路径：
    index.ts → export * from './Button'
    Button.tsx → import { Modal } from './index'  ← 循环！

  检测方法：从 index.ts 出发构建依赖图，检查是否存在回到自身的路径。

  ❌ 违规:
    // index.ts
    export * from './Button'
    // Button.tsx
    import { Modal } from './index'  // 引用了桶文件

  ✅ 正确:
    // Button.tsx
    import { Modal } from './Modal'  // 直接引用目标文件
  ```

##### C-6: 导出项与实际文件一致
- **ID**: `c-barrel-export-target-exists`
- **类型**: `text`
- **排序**: 6
- **条件内容**:
  ```
  桶导出中引用的每个模块名必须对应真实存在的文件。文件扩展名可省略
  （TypeScript 自动解析 .ts/.tsx/.js）。

  ❌ 违规:
    export * from './Foo'  // Foo.ts 不存在

  ✅ 正确:
    export * from './Button'  // Button.tsx 存在
  ```

##### C-7: 解决命名冲突
- **ID**: `c-barrel-resolve-naming-conflict`
- **类型**: `text`
- **排序**: 7
- **条件内容**:
  ```
  当多个模块通过 `export *` 导出同名标识符时，必须在原模块文件中解决冲突，
  而非在 index.ts 中使用具名导出规避。

  解决方案优先级：
  1. 在原模块中重命名导出（如 `export { Foo as FooA }`）
  2. 若无法修改原模块（第三方代码），在 index.ts 中使用显式重导出：
     `export { Foo as FooA } from './ModuleA'`
     （这是唯一允许 `export { } from` 的场景）

  ❌ 违规:
    // 两个模块都导出了 type Foo，导致 import 方类型歧义
    export * from './ModuleA'  // 导出 Foo
    export * from './ModuleB'  // 也导出 Foo

  ✅ 正确:
    // ModuleA/Foo.ts 中：
    export type { Foo as FooA }
    // 或 index.ts 中（仅当无法修改原模块）：
    export { type Foo as FooA } from './ModuleA'
    export * from './ModuleB'
  ```

##### C-8: 无重复导出
- **ID**: `c-barrel-no-duplicate-export`
- **类型**: `text`
- **排序**: 8
- **条件内容**:
  ```
  同一标识符不得在同一 index.ts 中被多次导出。包括：
  - 同一条 `export * from` 语句重复出现
  - 不同模块导出同名标识符（此时应触发 C-7 命名冲突解决）

  ❌ 违规:
    export * from './Button'
    export * from './Button'  // 重复

  ✅ 正确: 每个模块只导出一次
  ```

---
## Crate与Archetype关系
目前定义的crate只与当前定义的Archetype有关

---
## 缺口分析
### Skill ↔ Crate/Archetype 一致性
目前是通过skill的最佳实践来创建Crate/Archetype。在未来的迭代中引入通过项目目前已有规范自动创建，可以大幅减少一个新项目接入代达罗斯的成本

### 脚本化维度缺口
当前都依赖 LLM 执行检查。没有落地为 oxlint 每次检查都消耗 LLM token，且结果非确定性

### 工具链缺口
飞书文档推荐了 barrelsby，`check-barrel-export` skill 也引用了它，但项目中没有 `barrelsby` 依赖、没有配置、没有 npm script。`barrel-generator` Crate 的"自动生成"能力完全依赖 LLM 手动写 `export *` 语句

桶导出检查未集成到 CI pipeline。如果 oxlint 规则落地，可加入 `bun quality` 或 GitHub Actions 在 PR 阶段自动拦截

---
## 参考
[飞书文档](https://ocn10zycuxwg.feishu.cn/wiki/KrDhw4N2zi1tDpku0JGcPcWOnEg)
[skill仓库]()