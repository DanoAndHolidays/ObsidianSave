# Webhook
Webhook 是一种**由事件驱动的 HTTP 回调机制**——当某个事件在第三方系统中发生时，该系统会主动向你预先注册的 URL 发送一个 HTTP 请求（通常是 POST），将事件数据实时推送给你。

"第三方 Webhook"特指**外部服务/平台提供的 Webhook 能力**，即你的系统作为接收方，监听来自第三方的事件通知。

## 核心机制
```Plain
┌──────────────┐       事件发生       ┌──────────────────┐
│  第三方平台   │ ──── HTTP POST ──▶ │ 你的 Webhook 端点 │
│(GitHub/Stripe│     (携带事件数据)   │  (你的服务器)     │
│  /飞书/企微…) │                     │                  │
└──────────────┘                     └──────────────────┘
```

|                |                                         |
| -------------- | --------------------------------------- |
| 概念             | 说明                                      |
| **推模型 (Push)** | 第三方主动推送，区别于你定时去拉取数据的轮询模式 (Pull/Polling) |
| **注册/订阅**      | 你在第三方平台配置一个回调 URL，告诉它"事件发生时请通知这个地址"     |
| **Payload**    | 第三方推送过来的请求体，通常是 JSON 格式，包含事件类型和详细数据     |
| **签名/验签**      | 第三方在请求头中附带签名（HMAC 等），你的服务器需要验证签名以防伪造    |

## Webhook vs 轮询 (Polling)

|   |   |   |
|---|---|---|
|对比维度|Webhook（推）|轮询（拉）|
|**实时性**|事件发生后即时推送，近乎实时|取决于轮询间隔，存在延迟|
|**资源消耗**|只在有事件时才有请求，高效|不论是否有新数据都持续请求，浪费资源|
|**复杂度**|需要暴露一个公网可访问的端点|实现简单，不需要公网端口|
|**可靠性**|需自行处理重试、幂等、失败补偿|天然幂等，丢失数据可重新拉取|
|**适用场景**|事件驱动、对实时性要求高|数据变化频率低、或无法接收推送|

## 常见的第三方 Webhook 场景

|   |   |   |
|---|---|---|
|领域|平台|典型事件|
|**代码托管**|GitHub / GitLab|Push、PR 创建/合并、Issue 变更、CI 状态|
|**支付**|Stripe / 支付宝|支付成功、退款完成、订阅状态变化|
|**即时通讯**|飞书 / 企业微信 / Slack|消息接收、审批通过、机器人事件|
|**SaaS 工具**|Jira / Notion / Figma|任务状态变更、页面更新、设计评论|
|**CI/CD**|Jenkins / GitHub Actions|构建成功/失败通知|
|**监控告警**|Grafana / PagerDuty|告警触发、告警恢复|

---
## 接收 Webhook 的典型流程
### 1. 注册回调地址
在第三方平台的设置中填入你的端点 URL，例如：
```Plain
https://your-server.com/api/webhooks/github
```

### 2. 接收并验签
```TypeScript
import crypto from "crypto";
import express from "express";

const app = express();
app.post("/api/webhooks/github", express.json(), (req, res) => {
  // 1️⃣ 验证签名 — 防止伪造请求
  const signature = req.headers["x-hub-signature-256"];
  const expected = "sha256=" +
    crypto.createHmac("sha256", WEBHOOK_SECRET)
          .update(JSON.stringify(req.body))
          .digest("hex");

  if (signature !== expected) {
    return res.status(401).send("Invalid signature");
  }

  // 2️⃣ 处理事件
  const event = req.headers["x-github-event"];
  const payload = req.body;

  switch (event) {
    case "push":
      handlePush(payload);
      break;
    case "pull_request":
      handlePR(payload);
      break;
  }

  // 3️⃣ 快速响应 200（第三方通常要求在几秒内响应）
  res.status(200).send("OK");
});
```

### 3. 异步处理 + 幂等保障
```Plain
HTTP 请求进入 → 验签 → 快速返回 200 → 将事件投入消息队列 → 异步消费处理
                                         ↑
                                  避免处理耗时导致超时
```
