# knowledge

知识检索与问答是百炼平台面向 RAG 场景提供的核心能力，通过统一的应用网关 API 提供语义检索与端到端问答服务。该能力不依赖底层 OpenAPI（如 `CreateIndex` 等 RPC 接口），而是以 REST/SSE 方式暴露，适用于快速集成到业务应用中。详细设计与行为请参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索**：跨多个已配置知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于构建自定义召回链路。
- **知识问答**：端到端问答服务，内部自动完成查询改写、知识检索、上下文融合与大模型生成，并通过 SSE [流式输出](../concepts/streaming-output.md)三个阶段结果（规划 → 工具调用 → 生成）。  
  > **注意**：知识问答接口 `/api/v2/apps/knowledge/chat` 的阶段划分和流式结构与旧版 `/api/v1/knowledge/chat`（已下线）不兼容，迁移时需适配 SSE event type 解析逻辑；具体阶段语义详见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 关键参数

| 参数 | 说明 | 是否必需 |
|------|------|----------|
| `Authorization: Bearer <API-Key>` | 使用控制台 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 获取的密钥 | 是 |
| Base URL | `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，其中 `{workspaceId}` 需从 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取 | 是 |
| `top_k`（检索接口） | 返回切片数量，默认 5，最大支持 20 | 否 |
| `stream`（问答接口） | 布尔值，控制是否启用 SSE 流式响应，默认 `true` | 否 |

## 使用方式

1. **知识检索**：向 `POST /api/v1/indices/knowledge/search` 发送 JSON 请求体（含 `query` 字段），示例：
   ```json
   { "query": "百炼平台如何配置知识库？", "top_k": 3 }
   ```
2. **知识问答**：向 `POST /api/v2/apps/knowledge/chat` 发送请求，推荐启用 `stream=true` 以获取完整三阶段流式响应；非流式模式仅返回最终答案（丢失中间过程）。  
   全部调用细节与鉴权要求均以 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 为准。

## 限制和注意事项

- **限流策略**：默认按用户维度限制 25 QPS，超限返回 `429 Too Many Requests`，需自行实现退避重试。
- **地域约束**：Base URL 固定为 `cn-beijing` 区域，暂不支持其他地域部署的知识库接入。
- **知识库状态依赖**：检索与问答均要求目标知识库处于 `ACTIVE` 状态，若知识库正在构建或失败，将返回 `400 Bad Request` 并提示 `index not ready`。
- **问答接口无显式模型选择参数**：底层模型由平台统一分配（当前为 `qwen-max` 或 `qwen-plus`），不可在请求中指定；如需固定模型，请使用底层 OpenAPI 自建 RAG 流程。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


