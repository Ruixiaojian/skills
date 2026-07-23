# knowledge

知识检索与问答是百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，通过语义检索与大模型协同实现精准、可溯源的智能问答。该能力基于 DashScope 应用网关提供 HTTP REST 接口，不依赖 OpenAPI RPC 调用链，适用于需快速集成知识增强能力的业务场景。详细设计与行为请参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索**：跨多个已构建的知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），不调用大模型，纯检索服务。  
- **知识问答**：端到端问答流程，支持 SSE 流式响应，输出包含「规划 → 工具调用（如 Retrieve）→ 生成」三阶段结果，底层自动调度检索与 LLM 生成。  
- 所有功能均运行于 DashScope 应用网关，与 `CreateIndex` 等 OpenAPI RPC 接口隔离，不可混用。详见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 关键参数

| 参数 | 说明 | 必填 | 示例 |
|------|------|------|------|
| `Authorization` | Bearer 鉴权头，值为 API Key | 是 | `Bearer ak-xxx` |
| `workspaceId` | 业务空间 ID，用于拼接 Base URL（`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`） | 是 | `ws-abc123` |
| `query` | 检索或问答的用户输入文本 | 是 | `"阿里云百炼平台支持哪些知识库格式？"` |
| `top_k` | 检索返回切片数（仅 `/search` 接口支持） | 否 | `5` |
| `stream` | 是否启用 SSE 流式（仅 `/chat` 接口有效） | 否，默认 `true` | `true` |

> **注意**：`/chat` 接口不接受 `model` 参数——模型由业务空间绑定的默认应用配置决定，无法在请求中覆盖。此行为与部分旧版文档描述不符，请以 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 为准。

## 使用方式

1. 在控制台获取 API Key（[API Key 页面](https://rag.console.aliyun.com/settings/apikey)）和业务空间 ID（[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)）；  
2. 构造 Base URL：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`；  
3. 发起 POST 请求：
   - 检索：`POST /api/v1/indices/knowledge/search`，Body 为 JSON `{ "query": "..." }`；  
   - 问答：`POST /api/v2/apps/knowledge/chat`，Body 同样为 JSON `{ "query": "..." }`，响应为 SSE 流；  
4. 所有请求必须携带 `Authorization: Bearer <API-Key>` 头。

## 限制和注意事项

- **限流策略**：默认按用户维度限流 25 QPS，超限返回 `429 Too Many Requests`，需客户端退避重试；  
- **知识库前提**：检索与问答均要求目标知识库已完成索引构建并处于 `ACTIVE` 状态，否则返回 `404 Not Found` 或 `400 Bad Request`；  
- **协议差异**：该能力**不兼容** OpenAPI 的 `Retrieve` RPC 接口（如 `dashscope.serving.Retrieve`），二者鉴权、Endpoint、参数结构完全不同；  
- **地域固定**：Base URL 中的 `cn-beijing` 为硬编码区域，暂不支持切换；  
- **调试建议**：首次调用前，务必确认业务空间已绑定至少一个有效知识库，否则 `/chat` 将静默返回空结果而非报错。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


