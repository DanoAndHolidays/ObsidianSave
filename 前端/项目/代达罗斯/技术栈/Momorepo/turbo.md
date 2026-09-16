# turbo
> Last Format Time：8/14/2026 10:55:41

你说的 `turbo`，在前端项目里通常指 **Turborepo**。它本质上是一个面向 JavaScript / TypeScript 项目的**构建系统和任务调度工具**，尤其适合 **Monorepo（单仓多包）**。官方也把它定义为高性能的 JS/TS build system。([Turborepo][1])

你可以先把它理解成：

> **Turbo = 帮你管理一个仓库里很多 package/app 的 `build`、`test`、`lint`、`dev` 等任务，并尽可能让它们跑得更快。**

比如你的项目可能长这样：

```text
my-project/
├── apps/
│   ├── web/
│   └── admin/
├── packages/
│   ├── ui/
│   ├── schemas/
│   └── db/
├── package.json
└── turbo.json
```

这其实就很像你之前看到的这种导入：

```ts
import { Database } from "@repo/db";
import { mcpToolInvocationInsert } from "@repo/db-schema";
```

`@repo/db`、`@repo/db-schema` 很可能就是同一个 Monorepo 里的不同 package。Turbo 经常用来管理这种项目。

---
## Turbo 主要解决 3 件事
**第一，知道任务应该按什么顺序运行。**

假设：

```text
web
 ↓
ui
 ↓
schemas
```

`web` 依赖 `ui`，`ui` 又依赖 `schemas`。

你运行：

```bash
turbo build
```

Turbo 会根据 package 之间的依赖关系决定执行顺序，而不是乱跑。

比如：

```text
schemas build
      ↓
ui build
      ↓
web build
```

官方文档里也明确提到，`turbo build` 会根据仓库的 dependency graph 执行构建任务。([Turborepo][2])


**第二，缓存任务结果。**

这其实是 Turbo 最重要的能力之一。

比如第一次：

```bash
turbo build
```

需要：

```text
schemas   2s
ui        3s
web       8s

总共 13s
```

Turbo 会记录这些任务的输入和输出。

第二次如果代码没变化：

```bash
turbo build
```

它发现：

```text
schemas 没变
ui 没变
web 没变
```

就可以直接：

```text
cache hit
```

不重新 build。

所以你经常会看到类似：

```text
Tasks:    5 successful, 5 total
Cached:   4 cached, 5 total
Time:     1.2s
```

这里的：

```text
Cached: 4 cached
```

就是 Turbo 帮你省掉了重复执行。

Turbo 官方把这一点叫做缓存 / Remote Caching，核心目的就是**避免重复做相同工作**。([Turborepo][1])


**第三，并行运行彼此无关的任务。**

比如：

```text
web
admin
docs
```

它们之间没有依赖关系。

那么 Turbo 可以尽量：

```text
        ┌─ web build
turbo ──┼─ admin build
        └─ docs build
```

而不是：

```text
web
 ↓
admin
 ↓
docs
```

这样整个构建速度会快很多。

---
## 那它和 pnpm workspace 是什么关系？
这是最容易混淆的地方。

你可以这样记：

```text
pnpm workspace
负责：
“这些 package 属于同一个仓库，并且它们之间怎么安装依赖”

Turbo
负责：
“这些 package 的 build/test/lint/dev 应该怎么执行，并且怎么执行得更快”
```

比如：

```yaml
# pnpm-workspace.yaml

packages:
  - "apps/*"
  - "packages/*"
```

这是 pnpm 在管理 workspace。

然后：

```json
// turbo.json

{
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "test": {},
    "lint": {}
  }
}
```

这是 Turbo 在管理任务。

所以现实项目经常是：

```text
pnpm + Turborepo
```

而不是二选一。

---
## `turbo.json` 中最重要的东西
比如：

```json
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"]
    }
  }
}
```

这里：

```text
dependsOn
```

表示任务依赖。

而：

```text
^build
```

非常关键，它的意思不是：

```text
先运行我自己的 build
```

而是：

> **先运行我所依赖的 package 的 build。**

例如：

```text
web
 └── @repo/ui
      └── @repo/schemas
```

执行：

```bash
turbo build
```

Turbo 大致会变成：

```text
@repo/schemas#build
        ↓
@repo/ui#build
        ↓
web#build
```

这就是 Turbo 很核心的**任务依赖图**。


所以，如果让我用一句前端开发里比较容易记的话：

> **pnpm workspace 管“包”，Turbo 管“包里的任务”。**

或者再形象一点：

```text
Monorepo

pnpm
 ↓
这些项目是谁？
它们依赖谁？

Turbo
 ↓
它们应该先执行谁？
哪些可以并行？
哪些结果可以直接用缓存？
```

你现在项目里已经出现很多 `@repo/xxx` 这样的 package，我觉得你接下来最值得搞懂的其实就是 **`turbo.json` 里的 `dependsOn: ["^build"]` 到底是怎么根据 package.json 的 dependencies 构建任务图的**。把这个搞懂，Turbo 基本就入门一半了。([Turborepo][3])

[1]: https://turborepo.dev/?utm_source=chatgpt.com "Turborepo"
[2]: https://turborepo.dev/docs/getting-started/installation?utm_source=chatgpt.com "Installation"
[3]: https://turborepo.dev/docs?utm_source=chatgpt.com "Introduction"
