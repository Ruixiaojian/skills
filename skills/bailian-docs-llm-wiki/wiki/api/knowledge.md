# knowledge

knowledge 是百炼平台提供的知识检索与问答能力，通过统一的应用网关 API 提供语义检索和基于知识库的流式问答服务。该能力不依赖底层 OpenAPI（如 `CreateIndex` 等 RPC 接口），而是面向业务场景封装的 RESTful 接口，适用于快速集成 RAG 应用。详细设计与行为请参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索**：跨多个知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于构建搜索增强前端或预检模块。  
- **知识问答**：端到端智能问答，支持 SSE 流式响应，输出分三阶段：规划（query decomposition）、工具调用（retrieval + context injection）、生成（LLM 回答）。  
- 不提供独立模型选型参数；底层模型由业务空间绑定的默认推理引擎自动调度，开发者无需指定模型 ID。此行为与 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 一致。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `workspaceId` | string | 是 | 业务空间唯一标识，用于拼接 Base URL（如 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`）；需从 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取 |
| `Authorization` | string | 是 | 请求头字段，格式为 `Bearer <API-Key>`；API Key 需在 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 创建并复制 |
| `top_k`（仅 `/search`） | integer | 否 | 检索返回切片数量，默认 5，最大 20 |
| `stream`（仅 `/chat`） | boolean | 否 | 是否启用 SSE [流式输出](../concepts/streaming-output.md)，默认 `true` |

> **注意**：`/chat` 接口不支持 `model` 字段传参——这与部分旧版文档中提及的“可选模型切换”存在矛盾。实际调用时若携带 `model` 将被忽略，以 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 描述为准。

## 使用方式

1. 构造请求 URL：  
   - 检索：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`  
   - 问答：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat`  
2. 设置请求头：`Authorization: Bearer <your-api-key>`  
3. 发送 JSON body（示例）：  
   ```json
   { "query": "百炼支持哪些文件格式？", "top_k": 10 }
   ```
4. 处理响应：  
   - `/search` 返回标准 JSON 数组；  
   - `/chat` 响应为 SSE 流，需按 `data:` 行解析事件（`plan` / `tool_call` / `answer` 类型）。

## 限制和注意事项

- **鉴权强约束**：必须使用业务空间专属 Base URL + 对应 API Key，跨 workspace 或 key 复用将返回 `401 Unauthorized`。  
- **限流策略**：默认用户级 25 QPS，超限返回 `429 Too Many Requests`；无突发配额，需自行实现退避重试。  
- **知识库状态依赖**：检索与问答均要求目标知识库已发布（`status=Published`），草稿或禁用状态将导致空结果或 `404 Not Found`。  
- **路径版本差异**：`/search` 位于 `v1`，`/chat` 位于 `v2`，二者鉴权与错误码体系一致，但响应结构不同——详见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


