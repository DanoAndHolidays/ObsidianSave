# 隐式分发与 Feature Flag 💡
> Last Format Time：9/16/2026 19:24:53

分发（dispatch）可以理解为根据某个条件，决定程序最终走哪一条代码路径。

显式分发：
```js
if (useNewVersion) {
  return newVersion()
} else {
  return oldVersion()
}
```

---
## 隐式分发
有时不会直接使用 `if / else`，而是利用表达式本身的行为完成选择。

例如：
```js
const config = userConfig || defaultConfig
```

`||` 具有 short-circuit evaluation（短路求值）：
```text
左侧 truthy
→ 返回左侧

左侧 falsy
→ 返回右侧
```

实际上隐式完成了：
```text
userConfig 有有效值
    ↓
使用 userConfig

userConfig 为 falsy
    ↓
使用 defaultConfig
```

但需要注意“`||` 是隐式分发”并不是 JavaScript 的正式术语。更准确的说法是 `||` 利用短路求值实现条件选择或 fallback（兜底）。

---
## Feature Flag 是什么
Feature Flag（功能开关 / 特性开关）是一种通过运行时开关决定某个功能是否启用的机制。

例如：
```js
if (featureFlags.newSearch) {
  return <NewSearch />
}

return <OldSearch />
```

代码中同时存在：
```text
OldSearch
NewSearch
```

Feature Flag 决定用户最终进入哪一条路径：
```text
newSearch = false
      ↓
OldSearch

newSearch = true
      ↓
NewSearch
```

---
## Feature Flag 的核心价值
最重要的一点 将 Deploy（代码部署）和 Release（功能发布）解耦。

以前：
```text
写代码
→ 部署
→ 用户立刻获得功能
```

使用 Feature Flag不一定每次发布功能都需要重新部署代码：
```text
写代码
→ 部署
→ flag 关闭
→ 用户暂时看不到

需要发布时
→ 打开 flag
→ 用户看到新功能
```

### 功能开关
```js
if (flags.newEditor) {
  return <NewEditor />
}

return <OldEditor />
```

### 灰度发布
例如：
```text
5% 用户
→ 新版

95% 用户
→ 旧版
```

然后逐渐：
```text
5%
↓
20%
↓
50%
↓
100%
```

这种方式通常叫Rollout（逐步放量 / 灰度发布）
