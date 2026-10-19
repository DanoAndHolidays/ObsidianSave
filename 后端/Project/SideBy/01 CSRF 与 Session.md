# 认证流程解析与前端登录/退出实现记录  
  
> 适用读者：需要理解 SideBy 认证闭环，或接手、修改前端 auth 代码的开发者。  
>  
> 状态：2026-10-19 登录/退出闭环已实现，并通过 API 冒烟 + 浏览器端到端全链路验证。  
>  
> 相关文档：`docs/api.md`（API 契约）、`docs/auth-first-loop-plan.md`（阶段计划）、`docs/auth-guide/`（分步教程）。  
  
## 1. 总体架构  
  
**服务端 Session 认证 + CSRF 防护，不使用 JWT。**  
  
- 后端：Spring Boot 4.1.1（Spring Security 7）+ MyBatis + MySQL，登录状态保存在服务端 `HttpSession`；  
- 前端：Vite + React 19 + React Router 7 + TanStack Query，登录状态由 `AuthProvider` 统一管理；  
- 浏览器只被动持有 Cookie。前端不把用户数据或 Session ID 写进 `localStorage`。  
  
## 2. 三个"钥匙"  
  
| 名字 | 谁设置 | 谁能读 | 作用 |  
| --- | --- | --- | --- |  
| `JSESSIONID` Cookie（HttpOnly） | 后端，创建 Session 时 | 只有浏览器，JS 读不到 | 服务端 Session 的编号，是登录凭证 |  
| `XSRF-TOKEN` Cookie | 后端 CSRF 过滤器 | JS 可以读 | CSRF **原始** token |  
| `X-CSRF-TOKEN` 请求头 | 前端写请求时显式发送 | 后端校验 | 证明写请求来自本站页面 |  
  
浏览器每次请求自动带 Cookie，所以前端请求封装（`frontend/src/lib/http.ts`）必须设置 `credentials: 'include'`；CSRF 头必须由前端显式发送——攻击者的跨站表单伪造不出这个头，这正是 CSRF 防护的意义。  
  
## 3. 完整流程  
  
### 3.1 应用启动与登录态恢复  
  
```  
App 启动  
  └─ AuthProvider 挂载（features/auth/authStore.tsx）  
       └─ GET /api/users/me（自动携带 JSESSIONID Cookie）  
            ├─ 200 → status = authenticated            ├─ 401 → status = anonymous（游客是正常状态）  
            └─ 其他 → status = error（后端故障 ≠ 未登录，不能混淆）  
```  
  
后端：Spring Security 过滤器链从 Cookie 取出 `JSESSIONID`，找到 `HttpSession`，恢复其中保存的 `Authentication`。`UserController.me` 拿到 `authentication.getName()`（数据库 username）→ `UserQueryService.findCurrentUser` 查出最新资料 → 返回 `CurrentUserVO`（**id 是字符串，永不含 passwordHash**）。  
  
### 3.2 注册（写请求，需要 CSRF）  
  
```  
前端 authApi.register(registerCommand)  1. ensureCsrfToken() → GET /api/auth/csrf → 内存缓存 token  2. POST /api/auth/register     头: Content-Type: application/json + X-CSRF-TOKEN  
     体: { username, email, password, displayName }  
  
后端：  
  CsrfFilter 校验通过  
    → AuthController.register（@Valid 校验，400 VALIDATION_FAILED）  
      → AuthService.register          username/email 规范化（trim、邮箱转小写）  
          → 查重（重复 username/email → 409）  
          → passwordEncoder.encode(password)   ← BCrypt 哈希  
          → INSERT app_user（password_hash 列存哈希）  
          → CurrentUserVO → HTTP 201```  
  
### 3.3 登录  
  
```  
前端 LoginPage 提交 → authApi.login({ identifier, password })  POST /api/auth/login（JSON + X-CSRF-TOKEN）  
  
后端校验链（AuthController.login）：  
  1. CsrfFilter 校验通过  
  2. authenticationManager.authenticate(UsernamePasswordAuthenticationToken)       └─ DaoAuthenticationProvider            ├─ AppUserDetailsService.loadUserByUsername(identifier)            │    └─ AppUserMapper.findByIdentifier：  
            │        WHERE username = ? OR email = ?   ← 用户名和邮箱都能登录  
            └─ BCrypt.matches(明文, passwordHash)  
  3. 失败 → 401 { code: "INVALID_CREDENTIALS",       message: "Username/email or password is incorrect" }  4. 成功 → 创建 SecurityContext → saveContext(...)     → 服务端创建 HttpSession     → Set-Cookie: JSESSIONID=xxx; HttpOnly   ← 浏览器从此"记住"登录  
     → 200 + CurrentUserVO  
前端（authStore.login）：  
  currentUser = 返回的用户 → status = authenticated  LoginPage → navigate(returnTo, { replace: true })  ← 回到登录前想去的页面  
```  
  
**为什么登录失败永远是同一句话？** 区分"账号不存在"和"密码错误"会泄露哪些账号已注册。Spring Security 默认把 `UsernameNotFoundException` 隐藏为 `BadCredentialsException`，两种失败对调用方完全不可区分。  
  
### 3.4 维持登录（刷新恢复）  
  
```  
浏览器刷新 → 前端内存状态清零  
  └─ AuthProvider 重新挂载 → GET /api/users/me       └─ 浏览器自动带 JSESSIONID → 后端从 Session 恢复 Authentication            └─ 200 → status = authenticated，登录态"回来了"  
```  
  
真相来源只有服务端 Session。`loading` 与 `anonymous` 必须分开处理，否则刷新受保护页会出现"先跳登录页又跳回来"的闪烁。  
  
### 3.5 退出  
  
```  
前端点"退出" → authApi.logout()  
  POST /api/auth/logout + X-CSRF-TOKEN  
后端：请求到不了 Controller——  Spring Security 的 LogoutFilter（过滤器链，先于 DispatcherServlet）  
    → 销毁 HttpSession、清空 Authentication、删除 JSESSIONID Cookie    → 200 { code: "OK", data: null }  
前端：currentUser = null → status = anonymous → navigate('/login')  
之后访问 /me → /api/users/me 401 → 路由守卫再次跳登录页  
```  
  
退出必须先调后端销毁 Session；只在前端把 `currentUser` 置空是假退出。  
  
### 3.6 前端路由守卫（ProtectedRoute）  
  
| 状态 | 行为 |  
| --- | --- |  
| `loading` | 显示"正在恢复登录状态"，**不能**此时跳登录页 |  
| `authenticated` | 渲染受保护页面 |  
| `anonymous` | `Navigate` 到 `/login`，state 携带 `returnTo`（原目标地址） |  
| `error` | 提示后端问题 |  
  
受保护路由：`/activities/create`、`/me`、`/notifications`。`/login` 必须在守卫之外，否则未登录访问登录页会形成跳转循环。登录成功回跳时只接受站内路径（拒绝 `//evil.com` 这类值），避免开放重定向。  
  
## 4. Spring Security 7 的掩码 CSRF（最容易踩的坑）  
  
### 4.1 实测行为  
  
`GET /api/auth/csrf` 一次响应同时产生两个**不同的**值：  
  
```text  
响应头:  Set-Cookie: XSRF-TOKEN=621ab6b3-5180-454b-a9e4-152e414aa290   ← 36 位 UUID响应体:  { "token": "enWIKOMaFtY8CssqeU_5aJAmE2HOHmo7JQaKCTzOLAVDI..." }  ← 96 位 base64url  
```  
  
实测结论：  
  
- 用响应体里的 96 位 token 当 `X-CSRF-TOKEN` 头 → 注册/登录/退出全部通过；  
- 用 Cookie 里的 UUID 当请求头 → 校验失败（匿名 401 / 已登录 403）。  
  
### 4.2 机制解释  
  
Spring Security 7 默认对"暴露给应用"的 CSRF token 做掩码处理（BREACH 攻击防护，`XorCsrfTokenRequestAttributeHandler`）：  
  
```text  
Cookie 里保存原始 token（36 字节 UUID 字符串）  
暴露给应用的 token = base64url(随机数(36B) ‖ 原始token ⊕ 随机数(36B)) = 96 字符  
校验时：后端用 Cookie 里的原始值反解请求头  
```  
  
所以**请求头必须使用 `/api/auth/csrf` 返回的 96 位 token**，Cookie 里的原始值直接拿来用必失败。96 = 72×4/3（72 字节 = 36 字节随机数 + 36 字节掩码结果），与 UUID 字符串 36 字节完全吻合，可以互相印证。  
  
### 4.3 前端正确做法  
  
```ts  
let csrfToken: string | null = null  
  
async function ensureCsrfToken(): Promise<string> {  
  if (csrfToken) return csrfToken          // 内存缓存  
  const response = await getCsrfToken()    // 永远通过接口获取  
  return response.token}  
```  
  
**不要**读取 `XSRF-TOKEN` Cookie 当作请求头（教程 07 的旧写法在 Spring Security 7 下会 403）。  
  
### 4.4 本次踩坑与排查过程  
  
1. 现象：浏览器里登录成功、刷新恢复正常，但点退出必 403；  
2. Network 发现退出请求头是 36 位 UUID，而接口返回的是 96 位 token；  
3. curl 探针确认：JSON token 有效、Cookie 原始值无效；  
4. 根因：教程 07 的 `ensureCsrfToken` 优先读 Cookie。全新浏览器首次登录时 Cookie 尚不存在，侥幸走了接口所以成功；刷新后 Cookie 存在，退出时用了原始 UUID → 403；  
5. 修复：`frontend/src/lib/authApi.ts` 删除读 Cookie 逻辑，始终通过接口获取并内存缓存；  
6. 复验：刷新 → 退出 → 200 → 跳 `/login` → 访问 `/me` → 401 → 跳回 `/login` ✓。  
  
## 5. 前端实现记录（2026-10-19）  
  
### 5.1 新增文件  
  
| 文件 | 用途 |  
| --- | --- |  
| `frontend/src/features/auth/authTypes.ts` | `CurrentUser`、`LoginCommand`、`AuthStatus` 等类型 |  
| `frontend/src/features/auth/authStore.tsx` | `AuthProvider` / `useAuth()`：认证状态与登录、退出、恢复 |  
| `frontend/src/features/auth/ProtectedRoute.tsx` | 路由守卫 |  
| `frontend/src/lib/authApi.ts` | CSRF 获取与缓存、注册/登录/退出/当前用户请求 |  
| `frontend/src/pages/LoginPage.tsx` | 登录页 |  
| `frontend/src/pages/LoginPage.module.css` | 登录页样式 |  
  
### 5.2 修改文件  
  
| 文件 | 改动 |  
| --- | --- |  
| `frontend/src/lib/http.ts` | `credentials: 'include'`；用 `Headers` 合并请求头 |  
| `frontend/src/app/providers.tsx` | 包裹 `AuthProvider` |  
| `frontend/src/app/router.tsx` | 挂载 `/login`；三个受保护路由放进 `ProtectedRoute` |  
| `frontend/src/layouts/AppLayout.tsx` | 顶栏/侧栏显示登录态与退出按钮 |  
| `frontend/src/layouts/AppLayout.module.css` | 侧栏登录态样式 |  
| `frontend/src/styles/global.css` | 补充缺失的 `--color-background` 变量 |  
| `frontend/eslint.config.js` | 给 `authStore.tsx` 加 `allowExportNames: ['useAuth']` |  
  
### 5.3 相对教程 07/08 的偏差与原因  
  
1. **登录页不再直接渲染 `error` 对象**：教程 07 的 store 存的是 `Error | null`，教程 08 直接 `{formError ?? error}` 渲染会导致 React 崩溃（Error 不是合法子元素）。已改为渲染 `error.message`，`ProtectedRoute` 同样处理。  
2. **`login()` 签名采用教程 07 的对象形式** `login({ identifier, password })`：教程 08 的两参数写法与教程 07 的 store 实现不一致，按教程 07 为准。  
3. **`authStore` 的 `refresh` 改为 `.then` 回调形式**：react-hooks v7 的 `set-state-in-effect` 规则不识别 await 边界，教程 07 的 async 写法会在 lint（`--max-warnings 0`）下报错。  
4. **eslint 增加 `allowExportNames: ['useAuth']` 覆盖**：`react-refresh/only-export-components` 会告警 hook 与组件同文件导出，这是标准豁免。  
5. **CSRF 不再读 Cookie**（见第 4 节）。  
6. **桌面侧栏增加登录态与退出按钮**：教程 08 只在移动端 header 实现，桌面宽度（≥800px）下 header 隐藏，将看不到任何登录/退出入口。  
7. **`--color-background` 变量**：`LoginPage.module.css` 引用了它但 `global.css` 未定义，已补上（值 `#f7f6fb`）。  
  
## 6. 验证记录  
  
### 6.1 静态检查  
  
```text  
pnpm typecheck / lint / format:check / build  全部退出码 0  
```  
  
### 6.2 API 冒烟测试（curl + cookie jar，测试账号 fe_smoke_1792397425）  
  
| 步骤 | 请求 | 结果 |  
| --- | --- | --- |  
| 1 | `GET /api/auth/csrf` | 200，`headerName=X-CSRF-TOKEN` |  
| 2 | `POST /api/auth/register`（JSON + CSRF 头） | 201，id 为字符串，无 passwordHash |  
| 3 | `POST /api/auth/login` 无 CSRF 头 | 401（匿名用户的 CSRF 失败走认证入口，见第 7 节） |  
| 4 | `POST /api/auth/login` 错误密码 | 401 `INVALID_CREDENTIALS` |  
| 5 | `POST /api/auth/login` 正确密码 | 200，Set-Cookie JSESSIONID |  
| 6 | `GET /api/users/me` | 200，返回当前用户 |  
| 7 | `POST /api/auth/logout` | 200，`data: null` |  
| 8 | `GET /api/users/me` | 401 `UNAUTHENTICATED` |  
  
### 6.3 浏览器端到端验证（Playwright）  
  
| 步骤 | 预期 | 结果 |  
| --- | --- | --- |  
| 未登录访问 `/activities/create` | 跳转 `/login` | ✓ |  
| 登录成功 | 回到 `/activities/create` | ✓ |  
| 刷新页面 | 保持登录并停留原页 | ✓ |  
| 点击退出 | 200，跳转 `/login` | ✓（修复掩码 CSRF 后） |  
| 退出后访问 `/me` | 跳回 `/login` | ✓ |  
  
## 7. 遗留事项  
  
- **注册页前端未做**：本阶段范围刻意只做登录/退出，注册通过 API（教程 07 的浏览器 Console 脚本或 PowerShell）完成。  
- **`AuthController.logout()` 是死代码**：`LogoutFilter` 在过滤器链就拦截了 `/api/auth/logout`，Controller 里该方法永远不会执行（目前 return null），建议删除。  
- **匿名用户缺 CSRF 的写请求返回 401 而非 403**：Spring Security 标准行为——匿名用户的 `AccessDeniedException` 交给"未登录入口"处理；已登录用户缺 CSRF 才是 403。  
- **Session 固定防护**：登录由 Controller 手工调用 `AuthenticationManager`，未经过 Spring Security 的 `SessionAuthenticationStrategy`（登录时不更换 Session ID）。当前开发阶段风险低，后续可补 `ChangeSessionIdAuthenticationStrategy`。  
- **`docs/api.md` 的"当前实现状态"一节** 仍写着登录接口"正在实现中"，可更新为已验收。  
- 本地数据库留有冒烟测试账号 `fe_smoke_1792397425`，可继续用于手工测试。