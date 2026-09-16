# ⌚️如何与 Agent 协作编程
> Last Format Time：9/16/2026 19:24:50

我负责定义问题、架构、边界和验收标准，Agent 负责调查、实现、验证和重复劳动。

可以把 Agent 理解成：执行能力很强，但需要明确技术方向的工程师。

---
## 推荐协作流程
完整流程：
```text
需求
↓
Explore（探索代码库）
↓
Plan（提出方案）
↓
Decide（人工决策）
↓
Implement（Agent 实现）
↓
Verify（验证）
↓
Review（人工 Review）
↓
Iterate（继续修改）
```

其中：
```text
人：What + Why + Tradeoff
Agent：大量 How
```

---
## 不要直接让 Agent 写代码
不推荐：
```text
给用户列表增加搜索功能。
```

推荐 Repository Exploration（代码库探索）：
```text
先不要修改代码。

请分析用户列表相关实现，找到：

1. 数据从哪里获取
2. 分页在哪里实现
3. 筛选条件如何保存
4. 项目中有没有类似实现

然后告诉我：

- 涉及哪些文件
- 当前数据流
- 推荐实现方案
- 潜在风险
```

---
## 先 Plan，再 Implement
推荐：
```text
先分析当前实现，不要修改代码。

告诉我：

1. 当前架构
2. 需要修改的位置
3. 推荐方案
4. 方案的 tradeoff
5. 潜在风险
```

等方案确定后可以先判断Agent 到底有没有理解当前架构：
```text
按照这个方案实现。
```

---
## 任务一定要可验收
不好的任务：
```text
优化一下这个组件。
```

问题：
```text
“优化”没有明确标准。
```

推荐：
```text
优化 UserTable。

目标：

1. page 切换时 Header 不重新 render
2. Row 数据没变化时 Row 不重新 render
3. 不改变现有 API
4. 不引入新的状态管理库
```

再增加 Definition of Done（完成标准）：
```text
- lint 通过
- typecheck 通过
- 原测试通过
- 新功能有测试
- public API 不变
```

---
## 一次只解决一个逻辑闭环
不推荐：
```text
帮我优化整个后台：

- 性能
- 权限
- API
- UI
- SEO
- 测试
```

应该拆成：
```text
Task 1：
找到 UserTable 不必要 render 的原因

Task 2：
修复 render propagation

Task 3：
添加测试

Task 4：
Review 当前实现
```

---
## 控制修改范围
Agent 容易出现：
```text
发现 A
↓
修改 A
↓
顺便修改 B
↓
顺便重构 C
↓
顺便更新 D
```

最后：
```text
27 files changed
```

因此需要明确Scope Control（范围控制）例如：
```text
修改范围限制在：

src/components/tabs/**
src/hooks/useControllableState.ts

不要修改其他模块。

如果确实需要修改其他模块，
先说明原因。
```

---
## 适合 Agent 的任务
### 重复性、机械性任务
```text
补测试
补 TypeScript 类型
rename
批量 refactor
API migration
lint 修复
补 loading/error
更新文档
```

这类任务特点：
```text
规则清楚
+
重复劳动多
+
容易验证
```

### 人设计，Agent 实现
例如：
```text
组件 API
状态管理
缓存策略
权限模型
数据库 Schema
状态边界
```

推荐：
```text
人：
设计 architecture

Agent：
按照 architecture 实现
```

例如：
```text
Tabs
├── Root
├── List
├── Trigger
└── Content
```

架构由人确定，然后 Agent 实现：
```text
Controlled / Uncontrolled
Roving Tabindex
Manual Activation
ARIA
```

### Agent 调查，人做决定
特别适合 Debug：
```text
为什么页面越来越慢？
为什么 hydration mismatch？
为什么接口请求两次？
为什么 build 变慢？
```

可以让 Agent：
```text
先调查，不修改。

告诉我：

1. root cause
2. 调用链
3. 可能方案
4. 每种方案 tradeoff
```

然后由人选择方案。

---
## Agent 写完不等于完成
错误：
```text
Implement
=
Done
```

正确：
```text
Implement
↓
lint
↓
typecheck
↓
test
↓
review diff
↓
Done
```

因此可以固定要求：
```text
实现完成后：

1. 运行 lint
2. 运行 typecheck
3. 运行相关测试
4. 修复发现的问题
5. review 当前 git diff

最后告诉我：

- 修改了什么
- 为什么这么修改
- 验证结果
- 剩余风险
```

---
## 让 Agent Review Agent
实现完成后可以重新切换角色：
```text
现在不要修改代码。

假设你是另一个 Senior Engineer。

Review 当前 git diff。

重点检查：

1. correctness
2. backward compatibility
3. 是否过度修改
4. 重复逻辑
5. 潜在 bug
6. 是否存在更简单方案
```

形成：
```text
Agent A：Implement
Agent B：Review
```

即使实际上是同一个 Agent，也能减少很多问题。

---
## 通用 Agent Prompt 模板
```text
目标：
<我要实现什么>

背景：
<业务 / 架构背景>

要求：
- xxx
- xxx
- xxx

限制：
- 不修改 xxx
- 不引入 xxx
- 保持 xxx API

第一步：

先阅读相关代码，不要修改。

告诉我：

1. 当前实现方式
2. 涉及文件
3. 数据流 / 调用链
4. 推荐方案
5. 风险

方案明确后再实现。

实现完成后：

- lint
- typecheck
- test
- review diff

最后总结：

- 修改内容
- 关键设计
- 验证结果
- 剩余风险
```

---
## 能力不能完全外包给 Agent
以后 Agent 写代码会越来越强，但工程师依然需要掌握：
```text
需求拆解
架构设计
状态所有权
数据流设计
API 设计
Tradeoff 判断
Code Review
Debug Reasoning
```

因为 Agent 可以很快写：
```js
useEffect(...)
useMemo(...)
useCallback(...)
```

但人需要判断：
```text
这个 state 是否本来就不应该存在？
这个 Effect 是否在同步两个 source of truth？
这个 Context 边界设计是否合理？
这个 abstraction 是否过度设计？
```

所以未来工程师的价值会从：
```text
我能不能写出这 100 行代码
```

逐渐变成：
```text
我能不能判断这 100 行代码
是否应该存在。
```

---
## 最终心智模型
以后使用 Codex、Claude Code、Cursor Agent 等工具时，可以固定记住：
```text
① Explore
理解代码库

② Plan
提出方案

③ Decide
人工决定架构和 tradeoff

④ Implement
Agent 实现

⑤ Verify
lint / typecheck / test

⑥ Review
人工 Review diff

⑦ Iterate
继续修改
```

不要训练“怎么让 Agent 一次把代码写对”，而应该训练“怎么把模糊需求==拆==成 Agent 可以可靠==执行==、==验证==和 Review 的工程任务”。