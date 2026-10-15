一个规范的 PR（Pull Request）不仅要告诉别人改了什么代码，还要让 Reviewer（代码审查者）快速理解：

为什么改？改了什么？怎么验证？有没有风险？

GitHub 官方并没有规定唯一的 PR 格式，但在实际团队协作中，通常会形成统一的 PR Template。

## 一、标准 PR 应该包含什么？

|模块|内容|重要程度|
|---|---|---|
|Title|用一句话概括本次改动|必须|
|Summary / Description|改动背景、目的及实现方案|必须|
|Changes|具体修改了哪些功能、模块|必须|
|Testing|如何测试，测试结果如何|必须|
|Related Issues|关联需求、Bug、Issue|推荐|
|Screenshots|前端 UI 改动前后对比|按需|
|Breaking Changes / Risks|兼容性问题、潜在风险|按需|
|Checklist|提交前的自检清单|推荐|

## 二、PR Title 怎么写？

推荐采用类似 Conventional Commits 的命名方式：

`<type>(<scope>): <description>`

例如：

```
feat(admin): separate user and admin dashboards
fix(auth): resolve token expiration issue
refactor(api): simplify request error handling
perf(list): optimize virtual list rendering
docs(readme): update deployment instructions
```

常见的 Type：

|Type|含义|
|---|---|
|`feat`|新增功能|
|`fix`|修复 Bug|
|`refactor`|重构，不改变外部功能|
|`perf`|性能优化|
|`docs`|文档修改|
|`test`|测试代码|
|`chore`|构建、配置、依赖等维护工作|
|`ci`|CI/CD 相关|

需要注意：PR Title 使用 Conventional Commits 是团队约定，不是 GitHub 的强制标准。

## 三、推荐直接使用的 PR Template

这是一个兼顾规范性和实用性的版本，前端、后端、全栈项目都可以使用。

## Summary

简要说明本次 PR 的背景、目标以及解决的问题。

## Changes

-   
    
-   
    
-   
    

## Related Issues

Closes #xxx

## Testing

- 本地功能验证通过
    
- 相关单元测试通过
    
- Lint / Type Check 通过
    
- 构建成功
    

**Test Steps:**

1.   
    
2.   
    
3.   
    

## Screenshots (if applicable)

如涉及 UI 改动，附上修改前后的截图或录屏。

## Risks & Breaking Changes

- **Breaking Changes:** None
    
- **Potential Risks:** None
    
- **Rollback Plan:** Revert this PR
    

## Checklist

- 代码符合项目规范
    
- 已完成自测
    
- 已移除调试代码和无用日志
    
- 已添加或更新必要的测试
    
- 已更新相关文档（如有必要）
    
- 不包含无关代码修改或敏感信息
    

其中 `Closes #xxx` 会在满足 GitHub 关联关闭条件、PR 合并到默认分支后自动关闭对应 Issue；如果只是关联需求，没有完全解决，可以使用 `Refs #xxx`，避免误关闭。

![](https://www.google.com/s2/favicons?domain=https://docs.github.com&sz=32)

GitHub Docs

## 四、一个真实业务场景的 PR 示例

假设你在 SideBy 中完成了管理员与普通用户控制台的拆分。

Title：

`feat(admin): separate admin and user dashboards`

feat(admin): separate admin and user dashboards

Open

enhancement

feature/separate-admin-dashboards → main

Summary

Separate administrator and regular user dashboards to improve role-based navigation and maintainability.

Changes

- Add a dedicated dashboard for administrators.
    
- Update route configuration with role-based access control.
    
- Extract shared dashboard components to reduce duplication.
    
- Redirect users to the appropriate dashboard after login.
    
    Testing
    
- Verified role-based routing.
    
- Verified administrator dashboard rendering.
    
- Verified unauthorized access is blocked.
    
    以上为示例测试结果，并非对你实际代码的测试。
    
    Risks
    
- Existing dashboard URLs may need compatibility handling.
    
- Rollback: revert the PR.
    

注意这里 Summary 和 Changes 的区别：

- Summary：为什么要改、想达到什么目标。
    
- Changes：为了实现目标，具体做了哪些修改。
    

这也是很多初级开发者容易混淆的地方。

## 五、怎么在 GitHub 项目中统一 PR 格式？

可以在仓库根目录创建：

```
SideBy/
├── .github/
│   └── pull_request_template.md
├── apps/
├── packages/
└── README.md
```

将上面的模板放进 `.github/pull_request_template.md`，合并到默认分支后，GitHub 创建 PR 时就能自动填充描述模板。

![](https://www.google.com/s2/favicons?domain=https://docs.github.com&sz=32)

GitHub Docs

+1

## 六、真正专业的 PR，还需要注意什么？

PR 规范并不只是把描述写好，工程实践上还有几个重要原则：

1. 一个 PR 尽量只解决一个独立问题。 不要把新增功能、代码重构、格式化整个项目混在一起。
    
2. 控制 PR 大小。 改动越集中，越容易 Review，也越容易定位和回滚问题。
    
3. 测试必须真实。 没有运行的测试不要勾选通过；无法验证的场景应说明原因。
    
4. 改动尚未完成就使用 Draft PR。 完成后再标记为 Ready for review。
    
    ![](https://www.google.com/s2/favicons?domain=https://docs.github.com&sz=32)
    
    GitHub Docs
    
    +1
    
5. 确保 CI 检查通过。 包括类型检查、Lint、单元测试以及构建等，具体以项目配置为准。
    
    ![](https://www.google.com/s2/favicons?domain=https://docs.github.com&sz=32)
    
    GitHub Docs
    

我的建议： 对于个人项目或者日常前端业务开发，固定使用 `Summary + Changes + Testing + Screenshots + Risks + Checklist` 就已经足够规范。

最关键的是让 Reviewer 在不反复追问你的情况下，知道为什么改、改了什么、如何验证以及合并是否安全。这比堆砌大量格式化文字更重要。