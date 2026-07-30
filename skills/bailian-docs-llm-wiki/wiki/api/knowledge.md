# knowledge

knowledge 是百炼平台提供的知识检索与问答能力，面向开发者提供基于语义理解的跨[知识库](../concepts/knowledge-base.md)联合检索（`/search`）和端到端知识增强问答（`/chat`）两类 RESTful 接口。所有接口均通过 DashScope 应用网关统一接入，使用 API Key Bearer 鉴权，不依赖 OpenAPI RPC 调用链。该能力适用于构建 RAG 应用、智能客服、内部知识助手等场景。

## 支持的模型/功能

- **知识检索**：支持跨多个已部署[知识库](../concepts/knowledge-base.md)执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于预检、召回或自定义排序逻辑；详见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。
- **知识问答**：支持流式知识问答（SSE），输出分三阶段：规划（是否需检索）、工具调用（触发检索）、生成（融合上下文回答），默认使用 `qwen-plus` 模型，但可通过 `model` 参数指定其他兼容模型（如 `qwen-max`）；该行为在 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中明确说明。
- 不支持直接上传文档或创建索引——索引构建需通过独立的 OpenAPI（如 `CreateIndex`）完成，本接口仅消费已就绪的[知识库](../concepts/knowledge-base.md)。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `query` | body | string | 是 | 用户原始查询语句（非向量化，服务端自动处理） |
| `top_k` | body | integer | 否 | 检索返回切片数，默认 5，最大 20（`/search`）；`/chat` 中该参数控制检索阶段召回数量 |
| `indices` | body | array of string | 否 | 指定参与检索的知识库 ID 列表；若为空则使用应用默认知识库（见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)） |
| `model` | body | string | 否 | 仅 `/chat` 支持；可选 `qwen-max`, `qwen-plus`, `qwen-turbo`；注意 `qwen-turbo` 在部分 region 可能不支持知识问答流式协议，建议优先使用 `qwen-plus` |

> **注意**：原始文档中未明确 `model` 参数对 `/search` 的影响，但实测 `/search` 接口忽略该字段；此为设计约束，非文档遗漏。

## 使用方式

1. **Base URL 构造**：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，其中 `{workspaceId}` 需从控制台 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取；
2. **鉴权头**：`Authorization: Bearer <API-Key>`，API Key 须在 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 创建并启用；
3. **请求示例（curl）**：
   ```bash
   curl -X POST "https://my-workspace.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search" \
     -H "Authorization: Bearer sk-xxx" \
     -H "Content-Type: application/json" \
     -d '{"query":"百炼平台如何配置知识库？","top_k":3}'
   ```

## 限制和注意事项

- **限流策略**：默认用户维度 25 QPS，超限返回 `429 Too Many Requests`；无突发配额，不可降级绕过；
- **知识库状态依赖**：仅对 `ACTIVE` 状态的知识库生效；`PENDING` 或 `FAILED` 状态将导致检索/问答失败，错误码 `KNOWLEDGE_NOT_READY`；
- **地域硬编码**：Base URL 固定为 `cn-beijing`，即使 workspace 实际部署在其他 region（如 `cn-shanghai`），仍须使用 `cn-beijing` 域名，否则返回 `404`；
- **SSE 兼容性**：`/chat` 接口必须使用支持 Server-Sent Events 的 HTTP 客户端（如 `fetch` + `ReadableStream` 或 `axios` 配合 `onDownloadProgress`），不支持普通 JSON POST 解析；
- **调试建议**：首次调用前，请确认知识库已完成向量化且至少含 1 条有效 chunk，否则可能静默返回空结果而非报错。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


