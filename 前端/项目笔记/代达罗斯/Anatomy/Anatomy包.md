# Anatomy包

https://linear.app/code-forge-official/issue/COD-292/anatomyfeaturecli%E4%BD%9C%E4%B8%BA%E9%A1%B9%E7%9B%AE%E7%BB%B4%E6%8A%A4%E8%80%85%E6%88%91%E5%B8%8C%E6%9C%9B%E9%80%9A%E8%BF%87-cli-%E6%A0%A1%E9%AA%8C%E4%BB%A3%E7%A0%81%E7%BB%93%E6%9E%84-validate-project-structure

---
## 需求表述
当前 Anatomy 的 schema、树处理、服务、Repository、DAO、tRPC 与 UI 分散在 apps/app、packages/schemas、packages/services、packages/db 和 packages/db-schema 中。

核心结构约束尚未形成可独立消费的领域能力，也无法脱离 Web 业务流程直接去检查一个本地项目。

为了让 Anatomy 成为可复用的功能模块，需要把现有 Anatomy Service、Repository、树操作与校验能力聚合到 packages/anatomies。Schema 继续由 @repo/schemas 提供，DAO 和表定义继续由 @repo/db 与 @repo/db-schema 提供。packages/anatomies 通过依赖这些公共包完成 Web 业务编排，同时用独立的 core 子入口向 CLI 提供不加载数据库的结构检查能力。

---
## 类似库

| 工具 | 主要检测能力 | 与 Anatomy 的区别 |
|---|---|---|
| [ls-lint](https://ls-lint.org/2.3/configuration/the-basics.html) | 文件、目录命名；按目录配置规则；正则；文件或目录数量 `N`、`N-M` | 最接近当前 CLI，但不擅长表达完整结构模板、`one_of` 和策略继承 |
| [Steiger](https://github.com/feature-sliced/steiger) | 通用文件结构和项目架构 lint；支持配置规则、watch；内置 FSD 规则 | 概念最接近，但目前仍是 beta，现成规则主要面向 Feature-Sliced Design |
| [ArchUnitTS](https://github.com/LukasNiessen/ArchUnitTS) | TypeScript 文件、目录、依赖关系和架构测试；支持 Vitest | 规则通过测试代码编写，不是可存储、发布的 JSON Anatomy 定义 |
| [dependency-cruiser](https://github.com/sverweij/dependency-cruiser) | import 依赖边界、循环依赖、分层依赖、required/allowed/forbidden 和严重级别 | 关注“谁依赖谁”，不检查目录里是否必须存在某个文件 |
| [eslint-plugin-boundaries](https://github.com/javierbrea/eslint-plugin-boundaries) | 模块分类和 import 边界；新版本也提供 Oxlint 集成指引 | 更适合限制 Service、DAO、UI 之间的依赖，不负责完整文件树 |
| [Nx Module Boundaries](https://nx.dev/docs/features/enforce-module-boundaries) | 通过项目标签限制 monorepo 包之间的依赖 | 依赖 Nx 项目模型，而当前项目是 Turborepo，不太适合直接引入 |

其中 `ls-lint` 已经支持这种数量规则：
```yaml
ls:
  components/*:
    .tsx: regex:[A-Z][a-zA-Z]+ | exists:1
    .test.tsx: regex:[A-Z][a-zA-Z]+ | exists:0-1
```

不过 Anatomy 目前仍有几个比较明确的差异化能力：
- JSON 结构可以在 UI 中创建、修改和发布版本。
- 支持嵌套的目录树模板。
- 支持 `optional`、`exactly_one`、`one_or_more`、`zero_or_more`。
- 支持 `one_of`。
- 每项约束可以配置 `block`、`warn`、`allow`。
- Policy 可以从 Anatomy、父目录和当前节点继承。
- 同一份定义既可以在平台使用，也能由 CLI 在本地或 CI 中执行。

我的判断是：Anatomy 并不是完全重复造轮子。它更像是“可视化、可版本化的 `ls-lint` + 架构规范管理平台”。

比较合理的长期定位是：
```text
Anatomy
├── 文件与目录结构：自身实现
├── 命名、数量、one_of：自身实现
├── import 依赖规则：未来接 dependency-cruiser 或 boundaries
└── UI、版本、发布、团队共享：Anatomy 的核心差异
```

因此不建议现在用现有库替换 Anatomy。可以重点参考 `ls-lint` 的正则、目录变量和数量表达方式；后续如果要检查“UI 不能直接依赖 DAO”这类规则，再集成 `dependency-cruiser` 会比自己解析 TypeScript import 更划算。