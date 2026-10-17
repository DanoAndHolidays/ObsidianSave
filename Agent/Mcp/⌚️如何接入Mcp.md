# ⌚️如何接入Mcp
> Last Format Time：9/16/2026 19:24:50

MCP（Model Context Protocol）可以理解为：给 AI / Agent 使用的一套标准化接口协议。传统 Web：
```text
用户
↓
React
↓
HTTP API
↓
Service
↓
数据库
```

MCP：
```text
用户
↓
LLM / Agent
↓
MCP Client
↓
MCP Server
↓
Service / API / DB
```

可以简单理解：
```text
MCP Tool ≈ 给 AI 使用的 API
```

---
## MCP Server 提供三种能力
```text
MCP Server
├── Tools
├── Resources
└── Prompts
```

##### Tools
让 AI **执行操作**，例如：
```text
get_user
create_user
send_email
create_order
delete_file
```

AI 根据 Tool 的：
```text
name
description
inputSchema
```

判断什么时候调用以及传什么参数。

##### Resources
给 AI **读取上下文和数据**，例如：
```text
docs://readme
users://123
logs://today
```

主要用于：
```text
查询文档
读取数据
获取日志
读取项目上下文
```

##### Prompts
提供预定义的 Prompt 模板，例如：
```text
review-code
summarize-project
analyze-bug
```

---
##  MCP Tool 的基本结构
一个 Tool 通常包括：
```text
名称
+
描述
+
输入 Schema
+
Handler
```

例如：
```ts
server.registerTool(
  "get-user",
  {
    description: "根据用户 ID 查询用户",

    inputSchema: {
      userId: z.string(),
    },
  },

  async ({ userId }) => {
    const user = await getUser(userId);

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(user),
        },
      ],
    };
  }
);
```

核心就是：
```text
Agent 调 Tool
↓
MCP Server 执行 Handler
↓
调用 Service / API / DB
↓
返回结果
↓
LLM 继续推理
```

### MCP 底层通信
MCP 底层使用类似：
```text
JSON-RPC
```

例如客户端查询工具：
```text
tools/list
```

调用工具：
```text
tools/call
```

逻辑：
```text
MCP Client
↓
tools/list
↓
获取可用工具

LLM 判断需要某工具
↓
tools/call
↓
MCP Server
↓
执行 Handler
↓
返回结果
```

SDK 帮我们封装了：

```text
JSON-RPC
Schema 校验
Tool 注册
协议能力协商
Transport 通信
```

### MCP 的通信方式
本地 MCP 常见：
```text
stdio
```

结构：
```text
MCP Client
↕ stdin / stdout
MCP Server Process
```

例如：
```text
Cursor
↓
启动 node mcp-server.js
↓
通过 stdin/stdout 通信
```

因此本地 MCP不一定需要 HTTP 端口，远程 MCP 一般使用：
```text
Streamable HTTP
```

给你整理成适合记笔记的版本：

---
## 企业中 MCP 的部门划分与使用
企业内部一般不会所有部门共用一个巨型 MCP Server，而是按照：
```text
业务域
+
权限边界
```

可以理解为：
```text
谁负责业务
↓
谁维护对应 MCP
```

例如：
```text
HR MCP
├── get_employee
├── get_attendance
└── create_leave_request

Finance MCP
├── get_budget
├── create_invoice
└── approve_payment

Engineering MCP
├── get_issue
├── query_logs
└── get_deployment
```


### Agent 可以同时使用多个 MCP
一个 MCP Client 可以连接多个 Server：
```text
Agent
↓
MCP Client
├── HR MCP
├── Finance MCP
├── Engineering MCP
└── Common MCP
```

LLM 根据用户需求决定调用哪个 Tool，例如：
```text
查询年假
↓
HR MCP

查询项目预算
↓
Finance MCP

查询线上日志
↓
Engineering MCP
```

### MCP Server 负责能力边界
例如：
```text
Finance MCP
```

代表这里提供的是财务领域能力而不是只有财务员工才能连接人员，权限应该由权限系统负责，因此：
```text
MCP Server
→ 控制能力属于哪个领域

权限系统
→ 控制谁能使用这些能力
```

### 权限需要多层控制
不能简单做到：
```text
能访问 Finance MCP
=
可以调用 Finance MCP 所有工具
```

实际一般会细分：
```text
Server 权限
↓
Tool 权限
↓
Resource 权限
↓
数据权限
```

例如：
```text
Finance MCP

get_budget
→ 普通员工可读

create_invoice
→ 财务员工可用

approve_payment
→ 财务主管可用

delete_invoice
→ 管理员可用
```

典型链路：
```text
用户
↓
SSO / OAuth
↓
RBAC / ABAC
↓
MCP Tool
↓
业务系统
```

### Common MCP
很多能力并不属于某个单独部门，可以抽成公共 MCP：
```text
Common MCP
├── search_company_docs
├── get_current_user
├── employee_directory
├── knowledge_search
└── company_calendar
```

供多个部门共同使用，最终可能形成：
```text
MCP
├── Common
│   ├── Docs
│   └── Search
│
├── HR
│   └── Employee
│
├── Finance
│   └── Budget
│
├── Engineering
│   ├── Git
│   └── Logs
│
└── Sales
    └── CRM
```

### 企业推荐使用 MCP Gateway
小规模可以：
```text
Agent
├── HR MCP
├── Finance MCP
└── Engineering MCP
```

规模变大以后更推荐：
```text
                Agent
                  ↓
             MCP Gateway
                  ↓
       ┌──────────┼──────────┐
       ↓          ↓          ↓
     HR MCP   Finance MCP   R&D MCP
```

Gateway 统一负责：
```text
身份认证
权限控制
Tool 路由
服务发现
限流
审计
监控
安全过滤
```

这样 Agent 只需要连接：
```text
company-mcp-gateway
```

而不是自己维护几十个 MCP Server。

### 一句话总结
```text
MCP Server
解决：能力怎么分

权限系统
解决：谁能用

MCP Gateway
解决：怎么统一管理和路由
```

企业里比较标准的做法是：业务团队维护各自领域 MCP，平台团队维护 MCP Gateway、统一鉴权、审计、注册发现和公共 MCP。
