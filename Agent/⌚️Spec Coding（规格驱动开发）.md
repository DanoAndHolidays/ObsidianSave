# ⌚️Spec Coding（规格驱动开发）
> Last Format Time：9/16/2026 19:24:50

Spec Coding = 先定义规格，再实现代码。不要直接告诉 Agent“帮我实现这个功能”，而是先明确这个功能应该满足什么要求，再让 Agent 按规格实现。

基本流程：
```text
Requirement
    ↓
Spec
    ↓
Plan
    ↓
Tasks
    ↓
Implementation
    ↓
Test
    ↓
Verification
```

它和普通 Vibe Coding 最大的区别在于：
```text
Vibe Coding：
需求 → 直接写代码 → 边写边改 → 最后不知道什么算完成

Spec Coding：
需求 → 明确完成标准 → 实现 → 对照标准验收
```

---
## Spec 的作用
Spec 本质上可以理解为：
```text
这个功能要做什么？
应该有什么行为？
边界情况是什么？
不能做什么？
什么状态下算完成？
```

例如实现搜索功能：
```md
## Goal

用户可以通过用户名搜索用户。

## Behavior

1. 输入为空时不请求。
2. 停止输入 300ms 后搜索。
3. 请求中显示 loading。
4. 无结果显示 Empty State。
5. 请求失败显示 Error State。
6. 新请求结果不能被旧请求覆盖。
```

重点：
```text
Spec 尽量描述 What，而不是 How。
```

例如：
```text
❌ 使用 useEffect 实现 debounce

✅ 用户停止输入 300ms 后发送搜索请求
```

前者规定了实现方式，后者规定了系统行为。

---
## 一个 Spec 应该包含什么
推荐结构：
```md
# Feature Name

## Goal

这个功能解决什么问题？

## User Story

As a ...
I want ...
So that ...

## Requirements

- 功能要求
- 功能要求

## Behavior

### Normal Flow

正常流程。

### Edge Cases

边界情况。

## Constraints

- 技术栈
- 性能要求
- 兼容性要求
- 不允许修改的内容

## Acceptance Criteria

Given ...
When ...
Then ...

## Non-goals

本次明确不做：

- ...
- ...

## Open Questions

尚未确认的问题。
```

---
## Acceptance Criteria（验收标准）
常见写法：
```text
Given ...
When ...
Then ...
```

例如：
```text
Given 输入框为空
When 页面加载
Then 不应该发送搜索请求
```

或者：
```text
Given 用户输入 "dan"
When 300ms 内没有继续输入
Then 应该发送一次搜索请求
```

Acceptance Criteria 后面可以直接转成测试。

---
## Spec 和 Test 的关系
```text
Spec = 系统应该是什么样
Test = 验证系统是不是这样
```

关系可以理解为：
```text
Requirement
    ↓
Spec
    ↓
Acceptance Criteria
    ↓
Tests
    ↓
Implementation
```

例如 Spec：
```text
输入为空时不发送请求
```

测试：
```ts
it('does not request when query is empty', () => {
  // ...
})
```

---
## Plan 和 Spec 的区别
```text
Spec
```

回答：

> 做什么？

例如：

```text
搜索输入停止 300ms 后发送请求。
```

而：

```text
Plan
```

---
## 最后进行 Spec Verification
实现完成后，不应该只问：
```text
写完了吗？
```

而应该让 Agent：
```text
对照最初的 Spec 检查实现。

对每条 Acceptance Criteria 标记：

PASS
FAIL
PARTIAL

并给出对应证据：
- 文件
- 函数 / 组件
- 测试
```

例如：
```text
1. 空输入不发送请求
PASS

2. 300ms debounce
PASS

3. Loading State
PASS

4. Error State
PASS

5. 旧请求不能覆盖新请求
PARTIAL
```

这样才能真正判断需求是否完成。