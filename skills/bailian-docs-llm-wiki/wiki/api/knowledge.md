# knowledge

knowledge 是百炼平台提供的知识增强型 API 服务，用于在自有知识库基础上执行语义检索与多阶段智能问答。它属于 DashScope 应用网关体系，通过 RESTful 接口提供能力，不依赖底层 OpenAPI（如 `CreateIndex` 等 RPC 接口），开发者需使用业务空间 ID 构造 Base URL 并携带 API Key 鉴权。详细设计与行为请参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索**：跨多个知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于构建自定义 RAG 流程。  
- **知识问答**：端到端问答服务，支持流式响应（SSE），输出分三阶段：规划（planning）、工具调用（tool calling）、生成（generation）。该能力内嵌检索逻辑，无需显式调用检索接口。  
- 不支持直接指定 LLM 模型——问答阶段使用的模型由服务端固定配置，当前为 `qwen-max` 或 `qwen-plus`（具体以实际响应中 `model` 字段为准）。此实现细节与 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 一致。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `workspaceId` | Base URL 路径 | string | 是 | 业务空间 ID，用于构造 Base URL：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`；须从 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取 |
| `Authorization` | Header | string | 是 | `Bearer <API-Key>`，API Key 须从 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 获取 |
| `query` | Body（JSON） | string | 是 | 检索或问答的原始用户输入文本 |
| `top_k` | Body（JSON） | integer | 否 | 仅知识检索接口支持，默认为 `5`；知识问答接口不接受该参数 |
| `stream` | Body（JSON） | boolean | 否 | 仅知识问答接口支持，默认 `true`；设为 `false` 可获取完整 JSON 响应（非流式） |

> **注意**：知识问答接口 `/api/v2/apps/knowledge/chat` 的请求体结构与知识检索 `/api/v1/indices/knowledge/search` 不兼容，二者不可混用参数。详见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中“接口列表”章节。

## 使用方式

1. **构造请求地址**：  
   - 知识检索：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`  
   - 知识问答：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat`  

2. **设置请求头**：  
   ```http
   Authorization: Bearer <your-api-key>
   Content-Type: application/json
   ```

3. **发送 JSON Body**（示例）：  
   ```json
   { "query": "百炼平台如何接入私有知识库？" }
   ```

4. **处理响应**：  
   - 检索接口返回标准 JSON 数组，含 `chunks` 字段；  
   - 问答接口默认流式（SSE），需按 `data:` 行解析事件；若 `stream=false`，则返回单个 JSON 对象，含 `output.choices[0].message.content`。

## 限制和注意事项

- **限流策略**：默认按用户维度限流 25 QPS，超限返回 `429 Too Many Requests`，需客户端退避重试。  
- **知识库前提**：所有接口均要求对应业务空间下已成功创建并发布至少一个知识库，否则返回 `404 Not Found` 或 `400 Bad Request`。  
- **地域约束**：Base URL 固定为 `cn-beijing` 区域，不支持切换地域；若业务空间部署于其他 Region，当前接口不可用。  
- **鉴权隔离**：API Key 与业务空间 ID 必须匹配，跨空间调用将失败——此行为与 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 描述一致，但与部分旧版文档中“全局 API Key 可通用”的说法冲突，请以本页为准。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


