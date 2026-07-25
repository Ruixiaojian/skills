# knowledge

knowledge 是百炼平台提供的知识增强型 API 服务，用于在自有知识库基础上执行语义检索与多阶段智能问答。它属于 DashScope 应用网关体系，通过 RESTful 接口提供能力，不依赖底层 OpenAPI（如 `CreateIndex` 等 RPC 接口），开发者需使用业务空间 ID 构造 Base URL 并携带 API Key 鉴权。详细设计与行为请参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索**：跨多个知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于构建自定义 RAG 流程。  
- **知识问答**：端到端问答接口，支持 SSE 流式响应，输出包含「规划 → 工具调用 → 生成」三阶段结果，适用于对话式知识交互场景。  
该能力不绑定特定大模型，由平台统一调度适配的知识增强推理引擎完成，具体模型选型对用户透明。更多上下文见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `workspaceId` | string | 是 | 业务空间 ID，用于构造 Base URL（`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`）；需从 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取 |
| `Authorization` | string | 是 | 请求头字段，格式为 `Bearer <API-Key>`；API Key 需从 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 获取 |
| `top_k`（检索接口） | integer | 否 | 返回切片数量，默认 5，最大 20 |
| `stream`（问答接口） | boolean | 否 | 是否启用 SSE [流式输出](../concepts/streaming-output.md)，默认 `true` |

> **注意**：文档中未明确 `knowledge/search` 接口是否支持 `stream=false` 模式，但根据 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 描述，该接口仅定义为 POST `/api/v1/indices/knowledge/search`，且未提及流式能力——因此 `stream` 参数**仅适用于 `/api/v2/apps/knowledge/chat`**，不可混用。

## 使用方式

1. 构造请求 URL：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`（检索）或 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat`（问答）  
2. 设置请求头：`Authorization: Bearer <your_api_key>`  
3. 发送 JSON body（示例为检索）：
   ```json
   {
     "query": "百炼平台如何配置知识库？",
     "top_k": 3
   }
   ```
4. 处理响应：检索接口返回同步 JSON；问答接口默认返回 SSE 流，需按 `data:` 行解析事件（`plan` / `tool_call` / `answer` 类型）。

## 限制和注意事项

- **鉴权与域名**：必须使用业务空间 ID 拼接 Base URL，不可使用通用域名（如 `dashscope.aliyuncs.com`）；否则返回 `404` 或 `401`。  
- **限流策略**：默认按用户维度限流 25 QPS，超限返回 `429 Too Many Requests`；无单独配额申请入口，需自行降频或联系技术支持。  
- **知识库前提**：调用前须已在控制台完成知识库创建、上传与发布；未发布的知识库不可被检索或问答命中。  
- **路径版本差异**：`/api/v1/.../search` 与 `/api/v2/.../chat` 版本号不一致，反映功能演进，二者**不共享参数规范或错误码体系**，需分别查阅对应文档。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


