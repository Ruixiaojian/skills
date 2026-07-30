# knowledge

knowledge 是百炼平台提供的知识增强型 AI 服务模块，支持基于私有知识库的语义检索与多阶段智能问答。该能力通过 DashScope 应用网关提供 RESTful API，不依赖底层 OpenAPI RPC 接口（如 `CreateIndex`），适用于快速集成 RAG 场景。详细设计与行为请参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索**：跨多个已发布知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于召回阶段。
- **知识问答**：端到端问答流程，通过 SSE [流式输出](../concepts/streaming-output.md)，明确划分为「规划 → 工具调用 → 生成」三阶段，支持上下文感知与知识引用。  
  > **注意**：知识问答不等同于通用大模型调用，其输入必须绑定已发布的应用 ID（`app_id`），且仅作用于该应用关联的知识库；该约束在 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中明确，但部分旧版 SDK 示例未体现，实际调用时需严格校验。

## 关键参数

| 参数 | 说明 | 必填 | 示例 |
|------|------|------|------|
| `Authorization` | Bearer 鉴权头，值为 `Bearer <API-Key>` | 是 | `Bearer ak-xxx` |
| `workspaceId` | 业务空间 ID，用于构造 Base URL（`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`） | 是 | `ws-abc123` |
| `app_id` | 知识问答必需，对应控制台中已发布的知识应用 ID | 仅 `/api/v2/apps/knowledge/chat` 需要 | `app-xyz789` |
| `query` | 检索或问答的原始用户输入文本 | 是 | `"阿里云百炼支持哪些知识格式？"` |

## 使用方式

1. 在控制台获取 **API Key**（见 [API Key 页面](https://rag.console.aliyun.com/settings/apikey)）和 **workspaceId**（见 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)）；
2. 构造请求 URL：
   - 检索：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`
   - 问答：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat`
3. 设置 `Authorization` 请求头；
4. 发送 JSON body（检索含 `query`、`top_k`；问答含 `app_id`、`query`、`stream` 等）。  
   完整字段定义与示例见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 限制和注意事项

- **限流策略**：默认按用户维度限流 25 QPS，超限返回 `429 Too Many Requests`，需客户端实现退避重试；
- **知识库状态要求**：仅已「发布」的知识库参与检索/问答，草稿或下线状态不可见；
- **问答流式响应结构固定**：SSE event 类型依次为 `plan` → `tool_call` → `answer`，解析时须按序处理，不可假设单次响应即完成；
- **Base URL 区域固定**：当前仅支持 `cn-beijing` 地域，`{workspaceId}` 不可替换为其他地域标识。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)




