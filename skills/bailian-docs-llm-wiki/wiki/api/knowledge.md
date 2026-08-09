# knowledge

knowledge 模块提供基于知识库的语义检索与智能问答能力，属于 DashScope 应用网关体系，通过 HTTP REST 接口调用，不依赖 OpenAPI RPC 接口（如 `CreateIndex` 等）。其核心能力分为知识检索与知识问答两类，适用于 RAG 场景下的结构化知识调用。详细接口定义与行为规范见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索**：跨多个知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于预检、摘要或下游模型输入。
- **知识问答**：端到端问答流程，通过 SSE [流式输出](../concepts/streaming-output.md)，依次经历规划（planning）、工具调用（tool calling）、生成（generation）三阶段，支持上下文感知与多跳推理。  
> **注意**：该问答流程与传统单次 LLM 生成不同，其分阶段机制在 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中明确定义，不可简化为普通 chat 接口。

## 关键参数

| 参数 | 说明 | 必填 | 示例 |
|------|------|------|------|
| `workspaceId` | 业务空间 ID，用于构造 Base URL（`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`） | 是 | `ws-abc123` |
| `Authorization` | 请求头中携带 `Bearer <API-Key>`，API Key 需从控制台 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 获取 | 是 | `Bearer ak-xxx` |
| `top_k`（检索） | 返回最相关的切片数量，默认 `5`，最大 `20` | 否 | `10` |
| `stream`（问答） | 是否启用 SSE 流式响应，布尔值，默认 `true` | 否 | `false` |

## 使用方式

1. 构造请求 URL：  
   - 检索：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`  
   - 问答：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat`  
2. 设置请求头：`Authorization: Bearer <API-Key>`，并确保 `Content-Type: application/json`。  
3. 发送 JSON body（以检索为例）：  
   ```json
   { "query": "什么是百炼平台？", "top_k": 5 }
   ```  
完整调用示例与错误码说明参见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 限制和注意事项

- **限流策略**：默认按用户维度限流 25 QPS；超出后返回 `429 Too Many Requests`，需客户端实现退避重试。  
- **知识库前提**：所有接口均要求知识库已通过 `CreateIndex` 等 OpenAPI 接口完成创建与向量化，但 knowledge 模块本身**不提供索引管理能力**——此属 OpenAPI 范畴，详见 [原文标题](../../raw/application-api-reference/knowledge.md)。  
- **地域绑定**：Base URL 固定为 `cn-beijing` 区域，暂不支持跨 Region 调用。  
- **鉴权隔离**：API Key 与 workspaceId 必须匹配，否则返回 `401 Unauthorized`；workspaceId 需在 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 中确认。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


