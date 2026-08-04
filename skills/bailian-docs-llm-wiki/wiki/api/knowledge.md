# knowledge

knowledge 模块提供基于知识库的语义检索与智能问答能力，属于 DashScope 应用网关体系，通过 HTTP REST 接口调用，不依赖 OpenAPI RPC 接口（如 `CreateIndex` 等）。其核心能力分为知识检索与知识问答两类，适用于 RAG 场景下的结构化知识调用。详细接口定义与行为规范见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索**：跨多个知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于召回阶段。
- **知识问答**：端到端问答流程，支持 SSE 流式响应，输出包含规划（planning）、工具调用（tool calling）和生成（generation）三个阶段的结果，需配合已部署的知识应用 ID 使用。  
  > **注意**：该问答能力并非直接调用大语言模型，而是由应用网关编排知识检索、推理调度与 LLM 调用，具体行为以 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中定义为准，与底层模型无关。

## 关键参数

| 参数 | 说明 | 必填 | 示例 |
|------|------|------|------|
| `Authorization` | 请求头中携带 `Bearer <API-Key>`，API Key 需在控制台 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 获取 | 是 | `Bearer ak-xxx` |
| `workspaceId` | 业务空间 ID，用于拼接 Base URL（`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`），须在 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 中创建并获取 | 是 | `ws-abc123` |
| `app_id` | 知识问答必需，指向已发布的知识应用；知识检索无需此字段 | 仅问答 | `app-xyz789` |

## 使用方式

1. 构造 Base URL：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`  
2. 知识检索：向 `/api/v1/indices/knowledge/search` 发送 POST 请求，请求体为 JSON，含 `query` 字段（字符串）及可选 `top_k`（默认 5）等参数；参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中的完整字段列表。  
3. 知识问答：向 `/api/v2/apps/knowledge/chat` 发送 POST 请求，请求体需包含 `app_id` 和 `messages`（格式同标准 chat 接口），响应为 SSE 流，客户端需按 `event: message` 解析 data 字段。

## 限制和注意事项

- **鉴权与域名强绑定**：Base URL 必须含 `workspaceId`，且 `Authorization` 头必须使用对应 workspace 的 API Key；二者不匹配将返回 `401 Unauthorized`。  
- **限流策略**：默认用户维度 25 QPS，超限返回 `429 Too Many Requests`；暂不支持按应用或知识库粒度配置配额。  
- **问答流式阶段不可跳过**：即使未启用工具调用，SSE 响应仍会依次发出 `planning` → `tool_calling` → `generation` 事件，客户端需兼容空 `tool_calls` 字段。  
- > **注意**：文档中未说明知识检索是否支持过滤条件（如 metadata 过滤）或向量重排序（rerank），实际能力请以最新 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 为准；历史版本中部分参数（如 `filter`）已在 v1 接口中移除，但未在本文档中明确标注废弃。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


