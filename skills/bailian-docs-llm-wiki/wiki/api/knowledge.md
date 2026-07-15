# knowledge

knowledge 是百炼平台提供的知识增强型 AI 服务模块，支持基于私有知识库的语义检索与多阶段智能问答。其 API 位于 DashScope 应用网关体系下，采用 RESTful 接口设计，与 OpenAPI 的索引管理类 RPC 接口（如 `CreateIndex`）在调用方式、鉴权机制和 Base URL 上存在本质差异。开发者需通过业务空间 ID 构造专属域名，并使用 API Key 进行 Bearer 鉴权。

## 支持的模型/功能

- **知识检索**：跨多个已发布知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于构建自定义 RAG 流程。  
- **知识问答**：端到端的流式问答能力，通过 SSE 返回三阶段响应（规划 → 工具调用 → 生成），自动完成知识检索、上下文组装与大模型生成。  
该能力不依赖特定大模型选型，底层由平台统一调度适配；但需确保所绑定的知识库已完成发布（参见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)）。

## 关键参数

| 参数 | 说明 | 必填 | 示例 |
|------|------|------|------|
| `workspaceId` | 业务空间唯一标识，用于构造 Base URL（`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`） | 是 | `ws-abc123` |
| `Authorization` | 请求头中携带 `Bearer <API-Key>`，API Key 需在控制台 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 获取 | 是 | `Bearer ak-xxx` |
| `top_k`（检索接口） | 检索返回的最大切片数，默认 `5`，最大 `20` | 否 | `10` |
| `stream`（问答接口） | 是否启用 SSE 流式响应，默认 `true` | 否 | `false` |

> **注意**：`workspaceId` 与 OpenAPI 中的 `project_id` 或 `tenant_id` 无映射关系，不可混用；[知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 明确指出其 Base URL 与 OpenAPI 完全隔离，若错误复用 `https://dashscope.aliyuncs.com` 将导致 404。

## 使用方式

1. 在控制台完成知识库创建、上传、解析与发布（详见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)）；  
2. 获取业务空间 ID 与 API Key；  
3. 构造请求：
   - 知识检索：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`  
   - 知识问答：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat`  
4. 发送 JSON body（如检索需含 `query` 字段，问答需含 `messages` 数组）。

## 限制和注意事项

- **限流策略**：默认用户维度 25 QPS，超限返回 `429 Too Many Requests`；  
- **知识库状态**：仅已“发布”状态的知识库参与检索/问答，草稿或未发布状态不可见；  
- **SSE 兼容性**：知识问答接口强制要求客户端支持 EventSource 或手动解析 `text/event-stream` 响应体；  
- **路径差异**：`/api/v1/indices/knowledge/search` 与 `/api/v2/apps/knowledge/chat` 分属不同版本路径，v1 不支持问答，v2 不支持纯检索——二者功能正交，不可替代。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


