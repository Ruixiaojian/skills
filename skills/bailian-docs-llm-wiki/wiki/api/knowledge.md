# knowledge

knowledge 是百炼平台提供的知识增强型 API 服务，支持跨知识库的语义检索与基于知识的流式问答。该能力通过 DashScope 应用网关提供 RESTful 接口，不依赖底层 OpenAPI（如 `CreateIndex`），而是面向业务场景封装了更高层的抽象。开发者需使用业务空间 ID 构造 Base URL 并通过 API Key 进行 Bearer 鉴权。

## 支持的模型/功能

- **知识检索**：执行跨多个知识库的联合语义检索，返回按相关性排序的文本切片（chunk），适用于召回阶段；  
- **知识问答**：端到端的 RAG 流式问答，输出包含规划（planning）、工具调用（tool calling）和生成（generation）三个阶段的 SSE 响应，适用于对话式知识交互场景。  
两者均属于 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 所定义的应用网关能力，与底层索引管理类 RPC 接口（如 `Retrieve`）逻辑隔离。

## 关键参数

- `Authorization`: 请求头必须携带 `Bearer <API-Key>`，API Key 须从 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 获取；  
- `Base URL`: 格式为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，其中 `{workspaceId}` 为业务空间 ID，需在 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 中确认；  
- 知识检索接口（`POST /api/v1/indices/knowledge/search`）需传入 `query` 和 `index_ids`（可选多个知识库 ID）；  
- 知识问答接口（`POST /api/v2/apps/knowledge/chat`）需传入 `messages`（对话历史）及 `app_id`（绑定知识库的应用 ID）。  
详细字段说明请参见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 使用方式

1. 在控制台创建并发布知识库，获取对应 `index_id` 或绑定知识库的 `app_id`；  
2. 从控制台获取有效的 API Key 和业务空间 ID；  
3. 构造请求：  
   - 检索示例：`curl -X POST "https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search" \  
     -H "Authorization: Bearer <API-Key>" \  
     -H "Content-Type: application/json" \  
     -d '{"query":"如何申请发票","index_ids":["idx-xxx"]}'`；  
   - 问答示例：同上 Base URL，路径为 `/api/v2/apps/knowledge/chat`，Body 中 `messages` 为标准 ChatML 格式数组。  
完整调用流程与错误码定义详见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 限制和注意事项

- **限流策略**：默认按用户维度限制为 25 QPS，超限返回 `429 Too Many Requests`，需自行实现退避重试；  
- **地域硬编码**：Base URL 固定为 `cn-beijing` 区域，当前不支持跨 Region 调用，即使业务空间部署在其他地域；  
> **注意**：文档中提及的 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com` 与部分旧版 SDK 示例中使用的 `dashscope.aliyuncs.com` 域名不兼容，后者属于 OpenAPI 体系，**不可混用**；  
- 知识问答接口返回 SSE 流，客户端需正确处理 `event: planning` / `event: tool_call` / `event: message` 三类事件，且必须保持长连接；  
- `index_ids` 在检索接口中为可选字段，但若未指定，将默认检索当前 workspace 下所有已发布知识库，可能引发性能波动或权限越界风险。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


