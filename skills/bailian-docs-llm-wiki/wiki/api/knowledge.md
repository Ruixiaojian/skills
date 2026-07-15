# knowledge

knowledge 是百炼平台提供的知识检索与问答能力，通过统一的应用网关 API 提供语义检索和基于知识库的流式问答服务。该能力不依赖底层 OpenAPI（如 `CreateIndex` 等 RPC 接口），而是面向应用层提供标准化 HTTP REST 接口，适用于 RAG 场景下的快速集成。详细设计与行为请参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索**：跨多个知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于召回阶段。
- **知识问答**：端到端智能问答，支持 SSE 流式响应，输出包含规划（planning）、工具调用（tool calling）和生成（generation）三个逻辑阶段，需配合已部署的知识库与应用配置使用。  
  > **注意**：知识问答接口 `/api/v2/apps/knowledge/chat` 的三阶段输出行为与部分旧版文档描述的“单次生成”存在差异，以 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中的 SSE 分阶段说明为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `workspaceId` | string | 是 | 业务空间 ID，用于构造 Base URL（`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`），非用户 UID 或 Project ID。获取路径见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。 |
| `Authorization` | header | 是 | `Bearer <API-Key>`，API Key 需在控制台 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 申请。 |
| `top_k`（检索） | integer | 否 | 检索返回切片数量，默认 5，最大 100。 |
| `stream`（问答） | boolean | 否 | 是否启用 SSE 流式响应，默认 `true`；设为 `false` 将返回完整 JSON 响应（非流式）。 |

## 使用方式

1. **构造请求地址**：将 `workspaceId` 替换进 Base URL，例如 `https://my-workspace.cn-beijing.maas.aliyuncs.com`；
2. **发起请求**：
   - 知识检索：`POST /api/v1/indices/knowledge/search`，Body 包含 `query` 和可选 `indices`（知识库 ID 列表）；
   - 知识问答：`POST /api/v2/apps/knowledge/chat`，Body 需包含 `messages`（对话历史）及 `app_id`（对应知识问答应用 ID）；
3. **处理响应**：
   - 检索接口返回标准 JSON，含 `results` 数组；
   - 问答接口默认流式（SSE），需按 `event: chunk` 解析；若 `stream=false`，则响应为单次 JSON，结构与流式末尾 `event: done` payload 一致。

## 限制和注意事项

- **鉴权与域名强绑定**：Base URL 必须含 `workspaceId`，且 `Authorization` 头中的 API Key 必须属于该 workspace 下的有效密钥，否则返回 `401 Unauthorized`；
- **限流策略**：默认按用户维度限流 25 QPS，超限返回 `429 Too Many Requests`，不可通过增加并发绕过；
- **知识库依赖**：知识问答接口不接受裸知识库 ID，必须传入已绑定知识库的 `app_id`（即 Model Studio 中发布的“知识问答应用”ID），该约束未在所有前端文档中明确强调，实际行为以 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 为准；
- **地域固定**：当前仅支持 `cn-beijing` 地域，URL 路径中硬编码该 region，不支持切换。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


