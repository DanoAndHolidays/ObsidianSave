# Utility-first & Atomic CSS
Utility-first：通过组合预定义的工具类构建样式，而不是为每个组件创建专属 CSS 类。

Atomic CSS（原子化 CSS）：将样式拆分为细粒度、可复用的 CSS 规则。一个工具类通常对应一个或少量 CSS 属性。

传统 CSS：
```
.card {
  display: flex;
  padding: 24px;
  border-radius: 12px;
}
```

Tailwind：
```
<div className="flex rounded-xl p-6" />
```

Tailwind 主要改变的是 CSS 的编写和组织方式，而不是浏览器的 CSS 运行机制

---
## TailwindCSS
> Last Format Time：9/16/2026 19:24:50

==CSS 原子化==方案之一
引入这两个后就可以快速的开发样式

```html
<!-- 引入 Tailwind CSS --> 
<script src="https://cdn.tailwindcss.com"></script> 

<!-- 引入 Font Awesome 等图标库（可选） --> 
<link href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css" rel="stylesheet">
```

---
## Tailwind 的工作原理
核心流程：扫描源代码 → 识别工具类 → 构建时生成 CSS → 浏览器正常渲染

例如：
```
<div className="flex gap-4 p-6" />
```

Tailwind 构建工具识别对应类名，生成类似：
```
.flex {
  display: flex;
}

.gap-4 {
  gap: 1rem;
}

.p-6 {
  padding: 1.5rem;
}
```

Tailwind v4 会按项目中检测到的有效候选类名生成需要的 CSS，而不是把所有可能的工具类都输出。

Tailwind 不需要浏览器运行时解析类名来生成样式

---
## 常用语法
### 基础工具类
```
<div className="flex items-center justify-between gap-4 p-6">
  <span className="text-lg font-semibold">Hello</span>
</div>
```

每个工具类负责一项或一组较小的样式功能。

### 状态变体（Variants）
```
<button className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50">
  Submit
</button>
```

- `hover:`：悬停状态

- `focus-visible:`：键盘等交互下的可见焦点状态

- `disabled:`：禁用状态

- `group-hover:`：根据父级 group 的悬停状态应用样式


变体最终会转换为符合条件的普通 CSS 规则。

### 响应式与容器查询
```
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3" />
```

使用移动优先的响应式设计。

Tailwind v4 默认断点：

- `md`：≥ 48rem
- `lg`：≥ 64rem


容器查询：
```
<div className="@container">
  <div className="grid grid-cols-1 @md:grid-cols-2" />
</div>
```

`md:` 基于视口宽度，`@md:` 基于查询容器的宽度。

### 主题配置 `@theme`
Tailwind v4 使用 CSS-first（CSS 优先）的主题配置方式。
```
@import "tailwindcss";

@theme {
  --color-brand-500: #2563eb;
  --radius-card: 12px;
}
```

```
<button className="bg-brand-500 rounded-card">
  Submit
</button>
```

`@theme` 定义的设计令牌不仅可以生成对应工具类，也可以作为 CSS 自定义属性使用。

---
## 动态类名问题
Tailwind 主要通过扫描源代码中的完整候选类名来生成 CSS。
错误示例：
```
<div className={`bg-${color}-500`} />
```

构建工具无法可靠地识别动态拼接后可能出现的完整类名。

推荐使用静态映射：
```
const variants = {
  blue: "bg-blue-500",
  red: "bg-red-500",
} as const;

<div className={variants[color]} />
```

这样 Tailwind 可以发现完整类名。

对于任意动态数值，例如用户自定义颜色，也可以结合 CSS Variables 实现。

---
## 类名冲突与样式复用
### className 顺序不决定优先级
```
<div className="bg-red-500 bg-blue-500" />
```

后面的 `bg-blue-500` 不一定生效

因为 HTML 的 class 顺序不等于 CSS 规则顺序，最终仍遵循 Cascade（层叠）

React 项目常见工具：

- `clsx`：条件拼接 className
- `tailwind-merge`：根据 Tailwind 工具类规则合并冲突类名

### Tailwind 仍然可以编写 CSS
可以使用原生 CSS、`@layer` 和 `@apply`：
```
@layer components {
  .custom-card {
    padding: 24px;
    border-radius: 12px;
  }
}

.button {
  @apply rounded-lg bg-blue-600 px-4 py-2;
}
```

但不建议把所有工具类都重新封装成 CSS 类，否则会削弱 Utility-first 的优势。
