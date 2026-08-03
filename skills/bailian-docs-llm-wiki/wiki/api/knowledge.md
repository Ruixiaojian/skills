# knowledge

knowledge 是百炼平台提供的知识检索与问答能力，面向开发者提供基于语义理解的跨知识库联合检索（`/search`）和端到端知识增强问答（`/chat`）两类 RESTful 接口。所有接口均通过 DashScope 应用网关统一接入，采用 API Key Bearer 鉴权，不依赖 OpenAPI RPC 接口体系。详细设计与行为请参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索（Search）**：支持跨多个已发布知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于构建自定义 RAG 流程。
- **知识问答（Chat）**：支持流式知识问答，响应包含规划（planning）、[工具调用](../concepts/tool-use.md)（tool calling）、生成（generation）三阶段输出，通过 SSE 协议逐段返回；底层自动调度适配的知识模型与检索结果，无需显式指定 LLM。
- 两类功能均**不开放模型选择参数**，由平台根据知识库配置与请求上下文动态路由至最优模型。该行为与 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中“基于知识库的智能问答”描述一致。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `Authorization` | Header | 是 | `Bearer <API-Key>`，API Key 需从 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 获取 |
| `workspaceId` | Base URL 路径 | 是 | 构成 Base URL 的一部分：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，需在 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 中获取 |
| `knowledgeIds` | Body (search) | 否 | 指定参与检索的知识库 ID 列表；若为空，则检索当前 workspace 下所有已发布知识库 |
| `messages` | Body (chat) | 是 | 格式为 `[{"role": "user", "content": "..." }]`，暂不支持 system message 或多轮历史透传 |

> **注意**：`/chat` 接口不接受 `model` 字段，与通用 `/v1/chat/completions` 接口不同；若强行传入将被忽略。此限制已在 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 的接口描述中明确体现。

## 使用方式

1. **构造 Base URL**：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`
2. **发起请求**：
   - 知识检索：`POST /api/v1/indices/knowledge/search`，Body 示例：
     ```json
     { "query": "百炼平台如何配置向量模型？", "knowledgeIds": ["k-abc123"] }
     ```
   - 知识问答：`POST /api/v2/apps/knowledge/chat`，Body 示例：
     ```json
     { "messages": [{"role": "user", "content": "百炼平台如何配置向量模型？"}] }
     ```
3. **处理响应**：
   - `/search` 返回 JSON，含 `results: [{chunk, score, knowledgeId}]`
   - `/chat` 返回 SSE 流，每行以 `data:` 开头，事件类型包括 `planning`、`tool_calling`、`answer`，需按序解析

## 限制和注意事项

- **限流策略**：默认按用户维度限流 25 QPS，超限返回 `429 Too Many Requests`；无突发配额，不可降级绕过。
- **知识库状态要求**：仅 `已发布（Published）` 状态的知识库参与检索与问答；草稿或已下线知识库不可见。
- **地域硬编码**：Base URL 固定为 `cn-beijing` 地域，不支持切换；即使 workspace 创建于其他地域，仍须使用该 endpoint。
- **无异步批量能力**：当前不支持 `/search` 批量查询或多 query 并发合并，需客户端自行聚合。
- **SSE 连接稳定性**：`/chat` 接口依赖长连接，建议设置合理的超时（≥ 120s）并实现重连逻辑；网络中断后无法恢复会话上下文。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


