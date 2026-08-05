# knowledge

knowledge 是百炼平台提供的知识检索与问答能力，面向开发者提供基于语义理解的跨知识库检索和流式问答服务。它通过 DashScope 应用网关暴露 RESTful API，不依赖 OpenAPI RPC 接口（如 `CreateIndex`），适用于快速集成 RAG 场景。该能力需配合业务空间 ID 和 API Key 使用，详见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索**：支持跨多个知识库联合语义检索，返回按相关性排序的文本切片（chunk），适用于召回增强场景。  
- **知识问答**：支持端到端流式问答（SSE），输出分三阶段：规划（query decomposition）、工具调用（retrieval）、生成（LLM response）。  
- 不提供独立模型选择参数；底层模型由应用网关自动调度，当前固定为百炼平台托管的 RAG 专用推理栈。具体实现细节参见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `workspaceId` | string | 是 | 业务空间 ID，用于构造 Base URL（`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`），非用户 UID 或租户 ID。须从 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取。 |
| `Authorization` | header | 是 | `Bearer <API-Key>`，API Key 需在 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 创建并复制。 |
| `top_k`（检索） | int | 否 | 检索返回切片数量，默认 5，取值范围 1–20。 |
| `stream`（问答） | boolean | 否 | 是否启用 SSE 流式响应，默认 `true`；设为 `false` 则返回完整 JSON 响应体。 |

> **注意**：文档中未定义 `model` 或 `llm_name` 类参数，与通用 `/v1/chat/completions` 接口不同，本能力不支持显式指定大模型——此设计与 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 一致，开发者不应尝试传入 `model` 字段，否则将被忽略或报错。

## 使用方式

1. 构造请求 URL：  
   - 检索：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`  
   - 问答：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat`  
2. 设置请求头：`Authorization: Bearer <your-api-key>`  
3. 请求体为 JSON，例如检索请求示例：
   ```json
   { "query": "阿里云百炼平台支持哪些知识库格式？", "top_k": 3 }
   ```
4. 问答接口响应为 SSE 流，需按 `data:` 行解析事件（`plan` / `tool_call` / `answer`），详见原始文档中的 [知识问答](https://help.aliyun.com/zh/model-studio/knowledgechat) 说明。

## 限制和注意事项

- **限流策略**：默认按用户维度限流 25 QPS，超限返回 `429 Too Many Requests`，需客户端退避重试。  
- **知识库前提**：知识检索与问答均要求知识库已通过 `CreateIndex` 等 OpenAPI 完成构建与发布，本接口不负责索引生命周期管理。  
- **地域约束**：Base URL 固定为 `cn-beijing` 区域，暂不支持跨 Region 调用。  
- **错误处理**：`401 Unauthorized` 表示 API Key 无效或过期；`404 Not Found` 多因 `workspaceId` 错误或知识库未发布。  
- **调试建议**：首次集成时，建议先用 `curl` 手动验证检索接口，再接入问答流式逻辑——参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中的路径与鉴权说明。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


