# knowledge

知识检索与问答是百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，通过语义检索与大模型协同实现精准、可溯源的智能问答。该能力基于 DashScope 应用网关提供 RESTful API，与 OpenAPI 体系（如 `CreateIndex`、`Retrieve` 等 RPC 接口）分离，适用于需快速集成、无需管理索引生命周期的业务场景。详细设计与行为请参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索**：跨多个已配置知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），不调用大模型，纯检索服务。
- **知识问答**：端到端问答流程，支持 SSE 流式响应，输出包含三个阶段：规划（planning）、工具调用（tool calling）、生成（generation），底层自动绑定知识检索结果与指定大模型（当前仅支持 `qwen-max` 和 `qwen-plus`，具体以 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中最新支持列表为准）。

> **注意**：部分旧文档提及支持 `qwen-turbo`，但根据 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 当前版本，该模型未列于知识问答可用模型列表中，实际调用将返回 `model_not_supported` 错误，请以该文档为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `knowledge_config.indices` | array of string | 是 | 知识库 ID 列表（如 `["idx-abc123", "idx-def456"]`），最多支持 5 个知识库联合检索 |
| `model` | string | 否（知识问答必填） | 指定问答所用大模型，当前仅支持 `qwen-max`、`qwen-plus`；知识检索接口不接受该参数 |
| `top_k` | integer | 否 | 检索返回切片数，默认 5，范围 1–20 |
| `stream` | boolean | 否 | 仅知识问答支持，设为 `true` 启用 SSE 流式响应 |

## 使用方式

1. **Base URL 构造**：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，其中 `{workspaceId}` 需从控制台 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取；
2. **鉴权**：所有请求头必须携带 `Authorization: Bearer <API-Key>`，API Key 从 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 获取；
3. **调用示例**：
   - 知识检索：`POST /api/v1/indices/knowledge/search`
   - 知识问答：`POST /api/v2/apps/knowledge/chat`

## 限制和注意事项

- **限流策略**：默认按用户维度限流 25 QPS，超限返回 `429 Too Many Requests`，需客户端实现退避重试；
- **知识库状态依赖**：仅 `ACTIVE` 状态的知识库参与检索，`PENDING` 或 `FAILED` 状态将被跳过且不报错；
- **无索引管理能力**：本接口不提供 `CreateIndex`、`DeleteIndex` 等索引操作，相关功能需调用 OpenAPI（参见 `raw/openapi-reference/indexing.md`）；
- **地域固定**：当前仅支持 `cn-beijing` 地域，URL 中的 region 不可替换。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


