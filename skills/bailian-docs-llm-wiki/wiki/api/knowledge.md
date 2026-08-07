# knowledge

knowledge 是百炼平台提供的知识检索与问答能力，通过应用网关 API 提供语义检索和基于知识库的流式问答服务。该能力不依赖底层 OpenAPI（如 `CreateIndex` 等 RPC 接口），而是以 RESTful 形式暴露，面向业务空间（workspace）进行隔离调用。所有请求需使用 API Key Bearer 鉴权，并通过业务空间 ID 构造专属 Base URL。

## 支持的模型/功能

- **知识检索**：跨多个知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于召回增强场景。  
- **知识问答**：端到端智能问答，支持 SSE 流式响应，输出包含规划（planning）、工具调用（tool calling）和生成（generation）三个阶段内容，适用于对话式 RAG 应用。  
这两项能力均属于 DashScope 应用网关体系，与底层索引管理类 OpenAPI 完全解耦，详见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 关键参数

- `Authorization`: 请求头必须携带 `Bearer <API-Key>`，API Key 须在控制台 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 获取。  
- Base URL: `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，其中 `{workspaceId}` 为业务空间 ID，需在 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 中获取。  
- 接口路径：  
  - 检索：`POST /api/v1/indices/knowledge/search`  
  - 问答：`POST /api/v2/apps/knowledge/chat`（注意版本号为 `v2`，非 `v1`）  
> **注意**：部分旧文档中误将问答接口路径写作 `/api/v1/apps/knowledge/chat`，实际应以 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中的 `v2` 路径为准。

## 使用方式

1. 确保已创建并启用至少一个知识库（知识库配置独立于本 API，需提前在控制台完成）；  
2. 获取有效 API Key 和业务空间 ID；  
3. 构造请求：  
   - 设置 `Authorization: Bearer <your-api-key>`；  
   - 使用 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com` 作为 Base URL；  
   - 向对应路径发送 JSON body（检索需传 `query` 字段，问答需传 `messages` 及可选 `app_id`）；  
4. 知识问答接口返回 SSE 流，客户端需按 `data:` 行解析事件（`planning`/`tool_calling`/`generation` 类型）。  
完整请求示例与字段说明请参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 限制和注意事项

- **限流策略**：默认按用户维度限流 25 QPS，超限返回 `429 Too Many Requests`，需自行实现退避重试；  
- **知识库范围**：检索接口自动覆盖当前 workspace 下所有已启用的知识库，不支持指定单个知识库 ID 过滤；  
- **问答上下文**：`/api/v2/apps/knowledge/chat` 不维护会话状态，每次请求均为无状态调用，如需多轮对话，需由客户端维护 `messages` 历史；  
- **地域约束**：Base URL 固定为 `cn-beijing` 地域，暂不支持其他 Region；  
- **鉴权隔离**：API Key 与 workspace ID 必须匹配，跨 workspace 使用将返回 `403 Forbidden`。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


