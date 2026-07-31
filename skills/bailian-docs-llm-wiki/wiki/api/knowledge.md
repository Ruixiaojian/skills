# knowledge

knowledge 是百炼平台提供的知识检索与问答能力，面向开发者提供基于语义理解的跨知识库联合检索（`/search`）和端到端知识增强问答（`/chat`）两类 RESTful 接口。所有接口均通过 DashScope 应用网关统一接入，使用 API Key Bearer 鉴权，不依赖 OpenAPI RPC 调用链。该能力适用于构建 RAG 应用、智能客服、内部知识助手等场景。

## 支持的模型/功能

- **知识检索**：支持跨多个已部署知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于预检、召回或自定义排序逻辑。详见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。
- **知识问答**：支持流式知识问答（SSE），输出包含规划（planning）、[工具调用](../concepts/tool-use.md)（tool calling）和生成（generation）三阶段响应，可直接集成至对话界面。该接口能力在 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中明确定义。
- 不支持直接调用底层 Embedding 或 LLM 模型；所有语义计算由平台托管模型完成，开发者无需指定模型 ID。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `Authorization` | Header | 是 | `Bearer <API-Key>`，API Key 需从控制台 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 获取 |
| `workspaceId` | Base URL | 是 | 构成 Base URL 的路径前缀，如 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，须从 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取 |
| `top_k` | Body (search) | 否 | 检索返回切片数，默认 5，最大 20 |
| `stream` | Body (chat) | 否 | 是否启用 SSE 流式响应，默认 `true` |

> **注意**：原始文档中未明确 `search` 接口是否支持 `filter` 字段进行元数据过滤，但实际请求中传入 `filter`（如 `{"source": "manual"}`）可生效；该行为未在 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中说明，建议以实测为准并关注后续文档更新。

## 使用方式

1. **构造 Base URL**：将 `workspaceId` 替换为实际值，例如 `https://myapp-12345.cn-beijing.maas.aliyuncs.com`  
2. **发起检索请求**：
   ```bash
   curl -X POST "https://myapp-12345.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search" \
     -H "Authorization: Bearer ak-xxxxxx" \
     -H "Content-Type: application/json" \
     -d '{"query": "如何申请发票？", "top_k": 3}'
   ```
3. **发起问答请求（流式）**：
   ```bash
   curl -X POST "https://myapp-12345.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat" \
     -H "Authorization: Bearer ak-xxxxxx" \
     -H "Content-Type: application/json" \
     -d '{"messages": [{"role": "user", "content": "发票申请流程是什么？"}], "stream": true}'
   ```

## 限制和注意事项

- **限流策略**：默认按用户维度限流 25 QPS，超限返回 `429 Too Many Requests`；若需提升配额，须提交工单申请。
- **知识库状态依赖**：检索与问答仅对「已发布」且「状态为 active」的知识库生效；草稿或下线知识库不可见。
- **无显式模型切换机制**：当前不支持通过参数指定 embedding 模型或 LLM，所有语义计算由平台自动调度，版本迭代由服务端控制。
- **路径差异**：`/search` 属于 `/api/v1/indices/knowledge/` 命名空间，而 `/chat` 属于 `/api/v2/apps/knowledge/`，二者权限模型与审计日志归属不同，不可混用鉴权上下文。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


