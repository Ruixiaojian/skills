# DashScope SDK 与原生 API

DashScope 是阿里云百炼平台提供的**原生 API 协议族**，统一封装大模型与应用调用的 HTTP 端点、鉴权机制和 SDK；与之并行的还有 OpenAI 兼容、Anthropic 兼容等第三方生态接口。DashScope 通常具备**最完整的功能集与最优性能**，是优先推荐的接入方式。

## 在百炼平台中的角色

百炼对外暴露的所有大模型与应用调用，本质上都通过 `dashscope.aliyuncs.com` 域名提供服务。在此之上分化出四类调用方式：

| 接口类型 | 端点路径示例 | 选择建议 |
| --- | --- | --- |
| DashScope（原生） | `/api/v1/...`、`/api/v2/...` | 功能最完整、参数最全，需要平台全部能力时首选 |
| OpenAI 兼容 Chat Completions | `/compatible-mode/v1/chat/completions` | 已有 OpenAI 代码迁移成本最低 |
| OpenAI 兼容 Responses | `/compatible-mode/v1/responses` | 需要内置工具（联网、代码解释器）且不想手动维护对话历史 |
| Anthropic 兼容 Messages | `/anthropic/v1/messages` | 复用 Anthropic 生态 |

兼容接口可以视为 DashScope 之上的一层适配；某些参数（流式细节、Plugin/RAG、Function Calling、`biz_params`、`session_id` 等）只在 DashScope 原生协议下可用。

## 典型使用场景

### 1. 模型调用（Qwen 文本/多模态）

DashScope 接口覆盖 Qwen 全系：

```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"model":"qwen-plus","input":{"prompt":"你是谁?"}}'
```

Python SDK 等价写法 `dashscope.Generation.call(...)`。

### 2. 视频生成（异步任务模式）

通义万相 / 爱诗 / 可灵 / Vidu 等视频模型都遵循"先创建任务返回 `task_id`，再轮询 `/api/v1/tasks/{task_id}` 拉结果"的异步流程；结果 URL 默认 24 小时有效，需自行转存。

### 3. 实时多模态对话（WebSocket）

Qwen-Omni-Realtime 走 WebSocket 通道：

- 华北 2（北京）：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`
- 新加坡：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`

模型双向流式传输音频/图像/文本，由 `session.update`、`response.create`、`input_audio_buffer.append` 等客户端事件驱动。

### 4. 长期记忆（新）

应用级 REST 服务，Base URL 为 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`，提供 `AddMemory` / `SearchMemory` / `ListMemory` 等 11 个接口，支持 cURL 与 Python SDK。

### 5. 应用调用（智能体 / 工作流）

百炼应用统一入口为 `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`：

```python
from dashscope import Application
Application.call(api_key=..., app_id='YOUR_APP_ID', prompt='你好')
```

请求体根字段为 `input` / `parameters` / `debug`，支持 `messages`（自管多轮）、`session_id`（云端托管多轮，1 小时、≤50 轮）、`biz_params.user_defined_params`（工作流节点/插件透传）。同一端点上还有 OpenAI Responses 兼容路径 `/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`。

### 6. 周边运维能力

- **临时 API Key**：`POST /api/v1/tokens` 由后端换取以 `st-` 开头的临时 Key，默认 60 秒，最长 1800 秒，到期自动失效，避免在浏览器/移动端泄露永久 Key。
- **异步任务管理**：`GET /api/v1/tasks/{task_id}` 查询、`GET /api/v1/tasks/` 批量查询、`POST /api/v1/tasks/{task_id}/cancel` 取消，共享 20 QPS 限流，结果保留 24 小时。
- **完成事件推送**：异步任务接入事件总线 EventBridge，`dashscope:System:AsyncTaskFinish` 事件可通过 HTTP 回调或 RocketMQ 通知业务侧，避免高频轮询。
- **本地文件上传**：上传后获得临时 URL 供模型读取。

## 鉴权与请求约定

- **API Key**：通过环境变量 `DASHSCOPE_API_KEY` 注入；HTTP 请求 Header `Authorization: Bearer $DASHSCOPE_API_KEY`。
- **APP ID**：仅应用调用需要，从百炼控制台应用卡片复制。
- **Workspace ID**：子业务空间或部分海外地域必须携带，控制台手动获取。
- **Content-Type**：`application/json`。
- **地域隔离**：北京、新加坡、弗吉尼亚、法兰克福等地域的 API Key 与端点互相独立，**不可跨地域混用**；新加坡旧域名 `dashscope-intl.aliyuncs.com` 即将下线，请迁移到带 `WorkspaceId` 的新版域名。

## DashScope SDK 与连接复用

官方 SDK 覆盖 Python、Java、Node.js、Go、C#、PHP，对应包名：

- Python：`pip install -U dashscope`（自定义参数透传场景需 ≥ 1.14.0）。
- Java：`com.alibaba:dashscope-sdk-java`（建议 ≥ 2.12.0）。

高并发场景应显式开启连接池复用：

| 语言 | 配置方式 |
| --- | --- |
| Java | `Constants.connectionConfigurations = ConnectionConfigurations.builder()...build();`，可调 `connectionPoolSize`（默认 32）、`maximumAsyncRequests`、`connectionIdleTimeout`（默认 300 秒）等 |
| Python（异步） | 复用 `aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=..., limit_per_host=...))` |
| HTTP 客户端 | 自行启用 Keep-Alive 与连接池 |

> Java SDK 默认 `connectTimeout=120s`、`readTimeout=300s`、`writeTimeout=60s`；低延迟场景应调小，并保证 `maximumAsyncRequestsPerHost ≤ maximumAsyncRequests ≤ connectionPoolSize`。

## 选型与注意事项

- **要功能最全 / 性能最优** → 选 DashScope 原生接口。
- **已有 OpenAI 代码、追求迁移成本最低** → 选 OpenAI 兼容 Chat Completions。
- **需要联网搜索 / 代码解释器等内置工具，且不想自管历史** → 选 OpenAI 兼容 Responses。
- **使用 Anthropic 生态工具链** → 选 Anthropic 兼容 Messages。
- 同一应用可以通过 DashScope 与 OpenAI 兼容两路并行调用，但新版智能体（Agent 2.0）请求字段与旧版智能体/工作流不完全一致，需按实际应用版本对照文档。
- 异步任务的取消操作只对 `PENDING` 状态有效，其它状态返回 `UnsupportedOperation`。
- 事件总线规则的**地域必须与任务地域一致**，否则收不到完成事件。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [video generation api](../api/video-generation-api.md)
- [long term memory new](../api/long-term-memory-new.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [more about models](../api/more-about-models.md)
- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)


