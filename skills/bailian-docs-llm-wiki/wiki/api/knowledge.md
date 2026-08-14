# knowledge

knowledge 是百炼平台提供的知识检索与问答能力，面向开发者提供基于语义理解的跨知识库联合检索（`/search`）和端到端知识增强问答（`/chat`）两类 RESTful 接口。所有接口均通过 DashScope 应用网关统一接入，采用 API Key Bearer 鉴权，不依赖 OpenAPI RPC 接口体系。详细设计与行为请参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索（Search）**：支持跨多个已发布知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于构建自定义 RAG 流程。
- **知识问答（Chat）**：支持流式知识问答，响应包含规划（planning）、工具调用（tool calling）、生成（generation）三阶段输出，通过 SSE 协议逐段返回；底层自动调度适配的知识模型（当前默认为 `qwen-max` 或 `qwen-plus`，具体以控制台配置为准）。该能力在 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中明确定义为应用网关专属接口，与 `CreateIndex` 等 OpenAPI RPC 接口逻辑隔离。

## 关键参数

| 参数 | 说明 | 是否必需 | 示例 |
|------|------|----------|------|
| `Authorization` | 请求头，格式为 `Bearer <API-Key>` | 是 | `Bearer ak-xxxxxx` |
| `workspaceId` | 业务空间 ID，用于构造 Base URL（`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`） | 是（隐式） | `ws-abc123` |
| `top_k` | 检索返回切片数（仅 `/search`），默认 5，最大 20 | 否 | `10` |
| `stream` | 是否启用流式响应（仅 `/chat`），布尔值，默认 `true` | 否 | `false` |

> **注意**：`/chat` 接口的 `model` 参数**不可显式指定**——其调用模型由业务空间内绑定的知识应用配置决定，与通用 `/v1/chat/completions` 接口不同。若在测试中发现模型未按预期切换，请确认知识应用配置是否已生效，并参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中关于“应用网关”与“OpenAPI”的边界说明。

## 使用方式

1. 获取 API Key：前往 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 创建或复用密钥；
2. 获取 workspaceId：在 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 查看目标空间 ID；
3. 构造请求：
   - 检索示例（POST `https://<workspaceId>.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`）：
     ```json
     { "query": "百炼平台如何接入私有知识库？", "top_k": 3 }
     ```
   - 问答示例（POST `https://<workspaceId>.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat`）：
     ```json
     { "messages": [{"role": "user", "content": "简述RAG流程"}], "stream": true }
     ```

## 限制和注意事项

- **限流策略**：默认按用户维度限流 25 QPS，超限返回 `429 Too Many Requests`，需客户端实现退避重试；
- **知识库状态要求**：仅 `已发布` 的知识库参与检索与问答，草稿或下线状态不生效；
- **地域约束**：Base URL 固定为 `cn-beijing` 区域，暂不支持跨地域调用；
- **SSE 兼容性**：`/chat` 接口必须处理 `text/event-stream` 响应类型，建议使用标准 EventSource 或手动解析 `data:` 字段；
- **错误响应**：非 2xx 响应体中 `code` 字段为平台错误码（如 `InvalidParameter`、`ResourceNotFound`），非模型内部错误码。

> **注意**：原始文档中未明确说明 `/search` 接口是否支持过滤器（filter）或元数据条件查询，但实测当前版本（v202407）**不支持** `filter` 参数；若需细粒度筛选，请在客户端对返回切片做后处理。此行为与部分旧版 OpenAPI 文档描述存在差异，以 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 的接口列表和路径定义为准。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


