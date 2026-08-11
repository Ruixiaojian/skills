# knowledge

knowledge 是百炼平台提供的知识检索与问答能力，面向开发者提供基于语义理解的跨知识库联合检索（`/search`）和端到端知识增强问答（`/chat`）两类 RESTful 接口。所有接口均通过 DashScope 应用网关统一接入，采用 API Key Bearer 鉴权，不依赖 OpenAPI RPC 接口体系。详细设计与行为请参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索（Search）**：支持跨多个已发布知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于构建自定义 RAG 流程。
- **知识问答（Chat）**：支持流式知识问答，响应包含规划（planning）、工具调用（tool calling）、生成（generation）三阶段输出，通过 SSE 协议逐段返回；底层自动调度适配的知识模型（当前默认为 `qwen-max` 或 `qwen-plus`，具体以控制台配置为准）。该能力在 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中明确定义为应用网关专属接口，与 `CreateIndex` 等 OpenAPI RPC 接口无兼容性。

## 关键参数

| 参数 | 说明 | 示例值 | 是否必需 |
|------|------|--------|----------|
| `Authorization` | 请求头，Bearer + API Key | `Bearer ak-xxx` | 是 |
| `workspaceId` | 业务空间 ID，用于构造 Base URL | `ws-abc123` | 是（嵌入在 Base URL 中） |
| `query` | 检索或问答的用户输入文本 | `"如何申请发票？"` | 是 |
| `top_k` | 检索返回切片数（仅 `/search`） | `5` | 否，默认 3 |
| `stream` | 是否启用流式响应（仅 `/chat`） | `true` | 否，默认 `true` |

> **注意**：`/chat` 接口不接受 `model` 字段显式指定模型——模型由业务空间内知识应用的部署配置决定，强行传入将被忽略。此行为与部分旧版文档中“可选 model 参数”的描述矛盾，应以 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 的当前定义为准。

## 使用方式

1. 在控制台获取 API Key（见 [API Key 页面](https://rag.console.aliyun.com/settings/apikey)）和业务空间 ID（见 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)）；
2. 构造 Base URL：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`；
3. 发起请求：
   - 检索：`POST /api/v1/indices/knowledge/search`
   - 问答：`POST /api/v2/apps/knowledge/chat`
4. 所有请求必须携带 `Authorization: Bearer <API-Key>` 头。

## 限制和注意事项

- **限流策略**：默认按用户维度限流 25 QPS，超限返回 `429 Too Many Requests`，需客户端实现退避重试；
- **知识库状态要求**：仅已「发布」的知识库参与检索与问答，草稿或下线状态不可见；
- **Base URL 区域固定**：当前仅支持 `cn-beijing` 地域，URL 中地域字段不可替换；
- **SSE 兼容性**：`/chat` 接口强制使用 SSE，响应头含 `Content-Type: text/event-stream`，客户端须按 SSE 协议解析（如使用 `EventSource` 或流式 HTTP 客户端）；
- **调试建议**：首次调用前，请确认业务空间内至少有一个已发布的知识库，否则 `/search` 将返回空结果，`/chat` 可能因无可用知识源而降级为通用问答（非预期行为）。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


