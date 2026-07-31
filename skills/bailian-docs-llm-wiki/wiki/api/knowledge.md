# knowledge

knowledge 是百炼平台提供的知识检索与问答能力，面向开发者提供基于语义理解的跨知识库联合检索（`/search`）和端到端知识增强问答（`/chat`）两类 RESTful 接口。所有接口均通过 DashScope 应用网关统一接入，采用 API Key Bearer 鉴权，不依赖 OpenAPI RPC 接口体系。详细设计与行为请参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索（Search）**：支持跨多个已发布知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于构建自定义 RAG 流程。
- **知识问答（Chat）**：支持流式知识问答，响应包含规划（planning）、工具调用（tool calling）、生成（generation）三阶段输出，通过 SSE 协议逐段返回；底层自动调度适配的知识模型（当前默认为 `qwen-max` 或 `qwen-plus`，具体以控制台配置为准）。该能力在 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中明确定义为应用网关专属接口，与 `CreateIndex` 等 OpenAPI RPC 接口逻辑隔离。

## 关键参数

| 参数 | 说明 | 是否必需 | 示例 |
|------|------|----------|------|
| `Authorization` | 请求头，格式为 `Bearer <API-Key>` | 是 | `Bearer ak-xxxxxx` |
| `workspaceId` | 业务空间 ID，用于构造 Base URL（`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`） | 是（隐式） | `ws-abc123` |
| `top_k` | 检索返回切片数（仅 `/search`），默认 5，最大 20 | 否 | `10` |
| `stream` | 是否启用流式响应（仅 `/chat`），布尔值，默认 `true` | 否 | `false` |

> **注意**：`/chat` 接口的 `model` 参数**不可显式指定**——其调用模型由业务空间内绑定的知识应用配置决定，而非请求体传入。这与部分旧版文档中暗示可传 `model` 的描述存在冲突；请以 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 的权威说明为准。

## 使用方式

1. 在百炼控制台获取 API Key（[API Key 页面](https://rag.console.aliyun.com/settings/apikey)）和业务空间 ID（[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)）；
2. 构造 Base URL：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`；
3. 发起请求：
   - 检索：`POST /api/v1/indices/knowledge/search`，Body 为 JSON，含 `query` 字段；
   - 问答：`POST /api/v2/apps/knowledge/chat`，Body 为 JSON，含 `messages`（标准 chat 格式）及可选 `app_id`（若业务空间下存在多个知识应用）。

## 限制和注意事项

- **限流策略**：默认按用户维度限流 25 QPS，超限返回 `429 Too Many Requests`，需客户端实现退避重试；
- **知识库状态要求**：仅 `已发布` 状态的知识库参与检索与问答，草稿或下线库不可见；
- **地域约束**：Base URL 固定为 `cn-beijing` 区域，暂不支持跨地域调用；
- **SSE 兼容性**：`/chat` 接口强制使用 SSE，响应头必须包含 `Content-Type: text/event-stream`，客户端需按事件流解析（如 `data: {...}` 块）；
- **错误处理**：所有错误响应均为标准 HTTP 状态码 + JSON body（含 `code` 和 `message`），无重定向或 HTML fallback。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


