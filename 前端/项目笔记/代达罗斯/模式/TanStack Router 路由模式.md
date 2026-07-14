# TanStack Router 路由模式
> Last Format Time：7/14/2026 20:56:57

本项目使用 TanStack Start 基于文件的路由系统。

---
## 路由文件结构
```text
routes/
├── __root.tsx              → /                         根路由（认证守卫）
├── _layout.tsx             → /_layout                  布局壳（侧边栏 + 顶栏）
│   ├── index.tsx           → /                         首页
│   ├── dictionary/
│   │   ├── index.tsx       → /dictionary               列表页
│   │   └── $id.tsx         → /dictionary/:id           详情页
│   └── architecture/
│       ├── crates/
│       │   ├── index.tsx   → /architecture/crates
│       │   └── $id.tsx     → /architecture/crates/:id
│       └── archetypes/
│           ├── index.tsx   → /architecture/archetypes
│           └── $id.tsx     → /architecture/archetypes/:id
```

- **`$id`**：动态路径参数，`/dictionary/$id` 匹配 `/dictionary/任何值`
- **`_layout`**：下划线开头表示布局路由，不参与 URL，子路由通过 `<Outlet />` 渲染
- **`__root`**：双下划线开头表示根路由
- **`index.tsx`**：目录的默认路由，对应目录路径本身

---
## 路由树自动生成
`routeTree.gen.ts` 由 TanStack Router 根据文件系统自动生成，**不应手动编辑**。每次新增/删除路由文件后，运行 `bun run dev` 会自动重新生成。

---
## 路由定义模式
### 基本页面路由
```tsx
// routes/_layout/dictionary/$id.tsx
import { createFileRoute } from "@tanstack/react-router";
import { DictionaryDetailPage } from "@/pages/DictionaryDetailPage";

export const Route = createFileRoute("/_layout/dictionary/$id")({
  component: DictionaryDetailPage,
});
```

### 带 search params 校验的路由
```tsx
// routes/_layout/dictionary/index.tsx
import { createFileRoute } from "@tanstack/react-router";
import { z } from "zod/v4";

const searchSchema = z.object({
  create: z.boolean().optional(),
});

export const Route = createFileRoute("/_layout/dictionary/")({
  component: DictionaryPage,
  validateSearch: searchSchema,  // URL query string 由 Zod 解析和校验
});
```

---
## 页面中如何使用路由
### 方式一：读取 search params（`Route.useSearch`）
```tsx
import { Route } from "@/routes/_layout/dictionary";

const searchParams = Route.useSearch();  // { create: true } 从 ?create=true 解析
```

### 方式二：导航跳转（`Route.useNavigate` / `useNavigate`）
```tsx
const routeNavigate = Route.useNavigate();

// 同页面内导航，更新 search params
routeNavigate({ to: ".", search: {} });           // 清除 query string

// 全局导航
import { useNavigate } from "@tanstack/react-router";
const navigate = useNavigate();
navigate({ to: "/dictionary", search: { create: true } });
```

### 方式三：带参数的导航（`useRouter`）
```tsx
import { useRouter } from "@tanstack/react-router";
const router = useRouter();

// 跳转到动态路由
router.navigate({ to: "/dictionary/$id", params: { id: entryId } });
```

### 方式四：获取当前路径（`useRouterState`）
```tsx
import { useRouterState } from "@tanstack/react-router";
const pathname = useRouterState().location.pathname;  // "/dictionary"
```

---
## search params 控制 UI 状态
本项目通过 URL query string 控制弹窗/抽屉的开关，而非组件内部 state：

```text
用户点击 [+] 按钮
  → navigate({ to: "/dictionary", search: { create: true } })
    → URL 变为 /dictionary?create=true
      → Route.useSearch() 返回 { create: true }
        → useEffect 检测到 → 打开 Dialog
          → 关闭时 → navigate({ to: ".", search: {} }) → URL 回到 /dictionary
```

优势：
- **可分享**：URL 直接复制给别人，打开就是同一状态
- **可回退**：浏览器的前进/后退按钮能控制弹窗开关
- **声明式**：组件不需要额外 state 管理弹窗可见性

---
## 布局路由（`_layout.tsx`）
```tsx
// routes/_layout.tsx
import { createFileRoute, Outlet } from "@tanstack/react-router";
import { AppLayout } from "@/components/AppLayout";

export const Route = createFileRoute("/_layout")({
  component: () => (
    <AppLayout>
      <Outlet />  {/* 子路由的内容渲染在这里 */}
    </AppLayout>
  ),
});
```

`_layout` 下的所有路由（`dictionary`、`architecture` 等）都包裹在 `AppLayout`（侧边栏 + 顶栏）中。

---
## 两种导航方式的选用
| 场景 | 使用 |
|------|------|
| 静态链接（侧边栏、导航菜单） | `<Link to="/dictionary">` |
| URL 需要 search params | `navigate({ to: "/x", search: {...} })` |
| 动态路由参数 | `navigate({ to: "/x/$id", params: { id } })` 或 `useRouter().navigate(...)` |
| 读取当前路径 | `useRouterState().location.pathname` |
| 读取 query string | `Route.useSearch()` |
