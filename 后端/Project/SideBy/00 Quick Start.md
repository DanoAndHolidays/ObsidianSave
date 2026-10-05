# 00 Quick Start
> Last Format Time：10/6/2026 02:27:25

我建议叫 **SideBy**，取自 _side by side_（并肩、一起）。

它表达的是：**来到新的城市，也能找到一起吃饭、运动、探索生活的人。** 名字简短，也方便后续拓展不同类型的活动。

- **英文名：** SideBy
- **宣传语：** _New city. Your people._（新的城市，同频的人。）
- **Git 仓库名：** `sideby`

它可以定位为：**面向异地实习、工作人群的同城活动平台，通过一起吃饭、运动、看展、周末出游，建立新的社交关系。** 产品围绕“活动”展开，用户带着具体目的参加，更容易迈出认识陌生人的第一步。

结合你选择的 **网页＋Android/iOS App**，我推荐：

**React + TypeScript + Capacitor，搭配 Spring Boot + MyBatis-Plus + MySQL + Redis；前后端放在同一个 Git 仓库，后端采用按业务划分的单体架构。**

下面是一套可以直接用于开工的方案。


先把第一版做成一个完整的活动闭环：**发现活动 → 查看详情 → 报名 → 活动内交流 → 参加活动。**

|模块|第一版功能|
|---|---|
|用户|注册登录、头像昵称、所在城市、兴趣标签|
|活动发现|按城市、分类、日期筛选；分页浏览|
|活动发布|标题、封面、介绍、地点、时间、人数限制、报名截止时间|
|报名|报名、退出、查看报名状态|
|活动管理|查看参与者、修改活动、取消活动|
|交流|活动留言、发起人公告|
|通知|报名结果、活动变更、活动取消的站内通知|
|基础管理|举报、管理员下架活动、封禁用户|

活动分类先固定为：吃饭、运动、看展、桌游、户外、学习交流。

第一版建议只做**免费活动、直接报名**。付款、报名审批、实时私聊、推荐算法、候补队列放到后续，先把用户能真正参加活动这件事做完整。

手机端可以采用四个主要入口：**发现、发布、消息、我的**；“我的”里区分我发起的活动和我参加的活动。


你要求的单体架构，可以这样组织：
 
这里的**单体**指：用户、活动、报名、通知等后端模块，都运行在同一个 Spring Boot 进程里，最终打成一个 JAR。

前端有自己的构建产物，数据库和 Redis 也独立运行。**同一个仓库、同一个后端应用、同一个部署产物，是三个不同的概念。**

具体技术栈我建议这样选：

|部分|选择|用途|
|---|---|---|
|前端|React + TypeScript + Vite|复用你现有的前端能力|
|路由|React Router|活动详情、个人中心等页面|
|服务端数据|TanStack Query|请求、分页、缓存、报名后的数据刷新|
|样式|CSS Modules|页面样式隔离、响应式布局|
|跨端|Capacitor|将前端打包为 Android/iOS App|
|后端|Java 21 + Spring Boot 4.1.x + Spring MVC|REST API、业务逻辑|
|数据访问|MyBatis-Plus|CRUD、分页；复杂操作写 SQL|
|数据库|MySQL|活动、报名和用户数据|
|Redis|Spring Data Redis|Token、限流；后期加热点缓存|
|数据库变更|Flyway|管理建表、加字段等 SQL 版本|
|构建部署|Maven、Docker Compose、Nginx|构建后端、启动服务、反向代理|

当前 Spring Boot 4.1 支持 Java 21，MyBatis-Plus 也提供对应的 Boot 4 Starter；起项目时按这套版本配依赖即可。你最近学的 Controller、Service、Mapper、事务等核心写法仍然能用。[docs.spring.io](https://docs.spring.io/spring-boot/system-requirements.html?utm_source=chatgpt.com)


前端跨端方面，**我推荐先用普通 React 做网页，再用 Capacitor 打包 App**。

Capacitor 会把网页资源放进原生容器，由 WebView 渲染界面，同时通过插件访问相机、定位等设备能力。这样你可以继续使用 HTML、CSS 和 React；它属于混合应用，界面渲染方式与 React Native 不同。[Capacitor](https://capacitorjs.com/docs/?utm_source=chatgpt.com)

对于活动列表、发布表单、个人中心这些页面，我判断这条路线很适合你现在起步。

从第一天开始，前端要注意三个设计点：

- **移动端优先，兼顾桌面布局。** 手机使用底部导航，桌面使用顶部或侧边导航；详情页在桌面可以增加右侧报名卡片。
- **平台能力集中封装。** 页面调用 `platform.share()`、`platform.pickImage()` 等统一接口，由内部决定使用浏览器能力还是 Capacitor 插件。
- **所有端使用同一套 API。** 网页可以请求同源的 `/api`；App 请求服务器的 HTTPS API 地址，通过环境配置切换。

业务组件里尽量少出现零散的 `if (isAndroid)`，把差异集中在平台适配层。

网页发布的是静态资源；Android 发布的是 APK/AAB；iOS 发布的是 IPA。App 内包含前端资源，联网请求后端。你目前使用 Windows，可以先完成网页和 Android；iOS 的本地构建需要 macOS 和 Xcode，也可以使用云端构建。[Capacitor Documentation](https://capacitorjs.com/docs/basics/workflow?utm_source=chatgpt.com)


Git 仓库建议保持简单，先用两个主要项目：

|路径|内容|
|---|---|
|`frontend/`|React 项目、依赖和前端构建配置|
|`frontend/android/`|Capacitor Android 工程|
|`frontend/ios/`|Capacitor iOS 工程|
|`backend/`|一个 Maven Spring Boot 项目|
|`deploy/`|Dockerfile、Compose、Nginx 配置|
|`docs/`|产品说明、数据库设计、API 约定|
|`.github/workflows/`|后续添加构建和检查流程|
|`README.md`|本地启动方式、环境变量说明|

**前端用自己的包管理器，后端用 Maven；它们共享仓库，但各自管理依赖。** 目前只有一个前端应用，不需要马上引入复杂的 workspace 或构建调度工具。

后端则按业务组织包：

```text
com.dano.tongpin
    auth
    user
    activity
    notification
    moderation
    common
    config
```

每个业务包内部再放 `controller`、`service`、`mapper`、`entity`、`dto`、`vo`。报名逻辑先放在 `activity` 内，因为它与活动容量、时间、状态关系非常紧密。

例如 `ActivityController` 接收请求，`ActivityService` 管发布与修改，`SignupService` 管报名与退出。它们都属于同一个应用，通过普通 Java 方法调用协作。


数据库第一版可以从这六张表开始：

|表|关键字段|
|---|---|
|`users`|`id`、账号、密码摘要、昵称、头像、城市、兴趣标签、角色、账号状态|
|`activities`|`id`、发起人、标题、介绍、封面、城市、分类、地址、开始结束时间、报名截止时间、容量、报名人数、状态|
|`activity_signups`|`id`、活动 ID、用户 ID、报名状态、报名时间、退出时间|
|`activity_comments`|`id`、活动 ID、作者 ID、内容、创建时间、删除状态|
|`notifications`|`id`、接收用户、通知类型、关联活动、内容、已读时间|
|`reports`|`id`、举报人、目标类型与 ID、原因、处理状态|

几个规则值得提前固定：

- `activity_signups` 对 **`(activity_id, user_id)` 建唯一约束**。退出后保留记录，再报名时更新原记录。
- 活动的“满员”由报名人数和容量计算，避免与单独的满员状态发生冲突。
- 活动状态先用：草稿、已发布、已取消；是否正在进行、已经结束，可以结合起止时间判断。
- 活动有报名者后，只允许调整受限字段；容量不能改到低于当前报名人数。
- 列表先展示城市、区域；详细集合地点和参与者信息按权限返回。

常用索引先围绕真实查询设置，例如活动列表的 `(city_code, status, start_time)`，我的报名的 `(user_id, status)`。ID 返回前端时统一使用字符串，避免 Java `Long` 与 JavaScript 数字精度产生问题。


**报名与退出，是最值得用你最近的后端知识认真做好的部分。**

第一版推荐一个容易理解的实现：**数据库事务＋活动行锁＋报名唯一约束**。

一次报名在 `SignupService` 的公开事务方法中完成：

1. 查询活动并使用 `SELECT ... FOR UPDATE` 锁住该活动行。
2. 检查活动状态、截止时间和剩余名额。
3. 查询当前用户的报名记录；已经报名就返回已有结果。
4. 新增报名记录，或者把已退出记录改回报名状态。
5. 报名人数加一，写入站内通知，然后提交事务。

退出报名同样先锁活动行：只有报名状态从“已报名”变为“已退出”时，人数才减一。重复退出不再次减人数。

修改容量、取消活动也遵循同样的活动行锁规则。这样同一场活动的关键修改会按顺序执行，报名名额更容易保持一致。

对小规模约搭子活动，这个方案足够直观。事务里只处理数据库操作；短信、上传、外部地图等网络调用放在事务之外，避免长时间占锁。

你最近遇到的事务代理问题，在这里可以直接规避：**由 Controller 调用 Spring 注入的 `SignupService` 事务方法**。写入之后发生失败要抛出异常触发回滚，不能仅返回 `Result.fail()` 就假设事务会回滚。


登录也可以沿用你刚学过的 Redis 思路：

**账号密码登录 → 校验密码 → 生成随机 Token → Redis 保存登录状态 → 后续请求携带 Token。**

密码用 BCrypt 存摘要；请求通过 `Authorization: Bearer ...` 携带 Token。登录拦截器恢复当前用户，退出登录时删除对应 Token。如果使用 `ThreadLocal` 保存当前用户，请求结束时必须清理。

权限要由后端判断：谁能编辑活动、谁能看参与者、谁能发公告，都不能只依赖前端隐藏按钮。

API 可以先这样约定：

|接口|用途|
|---|---|
|`POST /api/v1/auth/login`|登录|
|`GET /api/v1/activities`|筛选、分页查询|
|`POST /api/v1/activities`|发布活动|
|`GET /api/v1/activities/{id}`|活动详情|
|`PATCH /api/v1/activities/{id}`|修改活动|
|`PUT /api/v1/activities/{id}/signup`|报名，重复调用返回已有状态|
|`DELETE /api/v1/activities/{id}/signup`|退出报名|
|`POST /api/v1/activities/{id}/comments`|活动留言|
|`GET /api/v1/me/notifications`|我的通知|

请求和响应使用 DTO/VO，避免直接把数据库实体全部返回。未登录用 `401`，无权限用 `403`，满员等业务冲突可以用 `409`。


部署先采用**一台 Linux 服务器＋Docker Compose**，启动 Nginx、Spring Boot、MySQL、Redis。

Nginx 提供网页资源并转发 API；MySQL 数据和上传图片挂载持久化目录，Redis 登录数据按需要配置持久化。图片第一版存服务器磁盘，后端封装一个文件存储服务，之后再换对象存储。

开发环境用 Vite 代理连接后端；生产环境通过环境变量注入数据库密码和 API 地址。仓库里提交配置模板，不提交真实密钥。

建议按这个顺序实现：

1. **网页业务闭环：** 登录、发布活动、列表详情、报名与退出。
2. **可供真实用户使用：** 留言、通知、举报、上传、权限，以及并发报名和重复请求验证。
3. **Android 打包：** 返回键、键盘、安全区域、图片选择、真机网络测试。
4. **iOS 与后续增强：** iOS 适配；再根据实际需求增加推送、实时聊天和活动提醒。

这套项目最先值得打磨的是：**活动状态是否清楚、报名人数是否正确、跨端使用是否顺畅**。MQ 可以等到需要可靠发送大量提醒或推送时再加入，第一版的站内通知直接写 MySQL 就能完成闭环。
