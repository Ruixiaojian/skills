# knowledge

knowledge 是百炼平台提供的知识检索与问答能力，通过 HTTP REST 接口实现跨知识库的语义检索和基于知识的流式问答。该能力运行在 DashScope 应用网关体系下，与底层 OpenAPI（如 `CreateIndex`、`Retrieve` 等 RPC 接口）逻辑隔离，面向业务应用层提供开箱即用的 RAG 服务。详细设计与行为请参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索**：支持跨多个知识库联合语义检索，返回按相关性排序的文本切片（chunk），适用于召回增强场景。  
- **知识问答**：支持端到端的智能问答流程，通过 SSE [流式输出](../concepts/streaming-output.md)，依次返回规划（planning）、工具调用（tool calling）、生成（generation）三个阶段结果，需配合已部署的知识应用 ID 使用。  
- 所有功能均基于 DashScope 应用网关提供，**不依赖用户自行托管模型或向量引擎**，底层模型由平台统一调度。具体能力边界详见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `workspaceId` | string | 是 | 业务空间 ID，用于构造 Base URL（`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`），非 AccessKey 或 Region ID |
| `Authorization` | header | 是 | `Bearer <API-Key>`，API Key 需在控制台 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 获取 |
| `app_id` | body（仅 `/chat`） | 是 | 已发布的知识应用 ID，对应控制台中“知识应用”模块下的唯一标识 |
| `query` | body | 是 | 检索或问答的原始用户输入文本 |

> **注意**：`workspaceId` 与百炼控制台中的“业务空间”ID 完全一致，**不可替换为 Project ID 或 UID**；部分旧文档误将 `workspaceId` 描述为“区域+实例ID”，该说法已过时，请以 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中定义为准。

## 使用方式

1. **构造请求地址**：  
   - 知识检索：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`  
   - 知识问答：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat`  

2. **设置请求头**：  
   ```http
   Authorization: Bearer <your-api-key>
   Content-Type: application/json
   ```

3. **发送 JSON Body（示例）**：  
   ```json
   {
     "query": "百炼平台如何配置知识库权限？",
     "top_k": 5
   }
   ```
   > 注意：`top_k` 仅对 `/search` 有效；`/chat` 接口不接受 `top_k`，其召回策略由绑定的知识应用配置决定。

## 限制和注意事项

- **限流策略**：默认按用户维度限流 25 QPS，超限返回 `429 Too Many Requests`，需客户端实现退避重试。  
- **鉴权隔离**：API Key 与 workspaceId 必须匹配同一业务空间，跨空间调用将返回 `403 Forbidden`。  
- **知识问答依赖部署状态**：`/chat` 接口要求 `app_id` 对应的知识应用已**发布成功且状态为“运行中”**，草稿或停用状态将返回 `404 Not Found`。  
- **无批量接口**：当前不支持单次请求多 query 批处理，需逐条调用。  
- **SSE 兼容性**：`/chat` 返回流式响应，需客户端正确处理 `text/event-stream` MIME 类型及 `data:` 前缀格式。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


