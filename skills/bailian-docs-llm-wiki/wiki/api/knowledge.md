# knowledge

knowledge 是百炼平台提供的知识增强型 API 服务，用于在自有知识库基础上执行语义检索与多阶段智能问答。它属于 DashScope 应用网关体系，通过 RESTful 接口提供能力，不依赖底层 OpenAPI（如 `CreateIndex` 等 RPC 接口），开发者需使用业务空间 ID 构造 Base URL 并携带 API Key 鉴权。详细设计与行为请参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索**：跨多个知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于构建自定义 RAG 流程。  
- **知识问答**：端到端问答服务，支持流式响应（SSE），输出包含「规划 → 工具调用 → 生成」三阶段结果，适用于对话式知识交互场景。  
该能力不绑定特定大模型，底层由平台统一调度适配；具体模型选型与路由逻辑由应用网关自动完成，开发者无需显式指定模型名称。更多上下文见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `index_ids` | string[] | 是（检索）/否（问答） | 检索时指定知识库 ID 列表；问答时若未传则使用应用默认知识库 |
| `query` | string | 是 | 用户输入的自然语言查询语句 |
| `top_k` | integer | 否 | 检索返回切片数，默认 5，最大 20 |
| `stream` | boolean | 否（默认 false） | 仅问答接口支持；设为 `true` 时启用 SSE [流式输出](../concepts/streaming-output.md) |
| `workspace_id` | path variable | 是 | 构成 Base URL 的一部分，非请求体参数 |

> **注意**：`index_ids` 在问答接口中为可选字段，但若应用未配置默认知识库，则必须显式传入，否则返回 400 错误——这与 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中“问答接口自动关联默认知识库”的描述存在不一致，建议以实际接口返回错误码为准并显式传参。

## 使用方式

1. **构造请求 URL**：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`（检索）或 `/api/v2/apps/knowledge/chat`（问答）  
2. **设置请求头**：
   - `Authorization: Bearer <API-Key>`
   - `Content-Type: application/json`
3. **发送 POST 请求**，请求体为 JSON 格式（示例见原始文档）。  
所有调用均需通过业务空间 ID 和 API Key 鉴权，二者均需在控制台获取：[API Key 页面](https://rag.console.aliyun.com/settings/apikey) 与 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)。

## 限制和注意事项

- **限流策略**：默认用户维度 25 QPS，超出后返回 `429 Too Many Requests`，需客户端实现退避重试。  
- **知识库范围**：检索接口支持跨知识库联合查询，但所有 `index_ids` 必须归属同一业务空间（workspace），跨 workspace 调用将失败。  
- **流式问答兼容性**：`/api/v2/apps/knowledge/chat` 的 SSE 响应格式与标准 OpenAI-style 流式不兼容，需按平台定义的 `event: chunk` / `data: {...}` 解析，不可直接复用通用 SSE 客户端。  
- **鉴权隔离**：该服务不支持 RAM 子账号细粒度权限控制，API Key 具备 workspace 级别全读写权限，请妥善保管。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


