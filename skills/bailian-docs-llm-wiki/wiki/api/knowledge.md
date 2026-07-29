# knowledge

知识检索与问答是百炼平台提供的核心 RAG 能力，通过统一的应用网关 API 提供语义检索与基于知识库的流式问答服务。该能力不依赖底层 OpenAPI（如 `CreateIndex` 等 RPC 接口），而是面向业务场景封装的 RESTful 接口，适用于快速集成到应用中。详细设计与行为请参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索**：跨多个已发布知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），不涉及大模型生成。
- **知识问答**：端到端流式问答，内部自动完成查询规划、知识检索、答案生成三阶段，响应通过 SSE [流式输出](../concepts/streaming-output.md)，支持中断与增量渲染。  
  > **注意**：知识问答接口（`/api/v2/apps/knowledge/chat`）**不支持指定基础模型**，其底层模型由平台固定调度，与 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中描述一致；若需控制模型，请使用底层 OpenAPI + 自定义 LLM 编排，而非本接口。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `knowledgeIds` | string[] | 否 | 指定参与检索的知识库 ID 列表；未传则默认使用当前应用绑定的所有已发布知识库。详见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) |
| `query` | string | 是（仅检索） | 检索用自然语言查询语句 |
| `messages` | object[] | 是（仅问答） | 对话历史数组，格式同标准 Chat API（含 `role` 和 `content`），首条 `user` 消息即为问题 |
| `stream` | boolean | 否，默认 `true` | 是否启用 SSE 流式响应；设为 `false` 将返回完整 JSON 响应体 |

## 使用方式

1. 构造 Base URL：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，其中 `{workspaceId}` 需从控制台 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取；
2. 在请求头设置 `Authorization: Bearer <API-Key>`，API Key 来自 [API Key 页面](https://rag.console.aliyun.com/settings/apikey)；
3. 发送 POST 请求：
   - 检索：`POST /api/v1/indices/knowledge/search`
   - 问答：`POST /api/v2/apps/knowledge/chat`

## 限制和注意事项

- **限流策略**：默认按用户维度限流 25 QPS，超限返回 `429 Too Many Requests`，需客户端实现退避重试；
- **知识库状态要求**：仅 `已发布（Published）` 的知识库参与检索/问答，草稿或下线状态不可见；
- **鉴权隔离**：API Key 与 workspaceId 必须匹配同一租户，否则返回 `401 Unauthorized`；
- **问答流式阶段**：SSE 响应包含 `planning`、`retrieving`、`generating` 三类事件，客户端需按 `event` 字段区分处理，不可假设顺序或忽略中间事件。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


