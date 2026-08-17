# knowledge

knowledge 是百炼平台提供的知识检索与问答能力，面向开发者提供基于语义理解的跨知识库联合检索（`/search`）和端到端知识增强问答（`/chat`）两类 RESTful 接口。所有接口均通过 DashScope 应用网关统一接入，采用 API Key Bearer 鉴权，不依赖 OpenAPI RPC 接口体系。详细设计与行为请参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索（Search）**：支持跨多个已配置知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于构建自定义 RAG 流程。
- **知识问答（Chat）**：支持流式知识问答，响应包含三个逻辑阶段（规划 → 工具调用 → 生成），通过 SSE 返回，适用于对话式应用集成。  
该能力底层不暴露具体模型名称，由平台根据知识库结构、查询意图及服务策略自动调度；开发者无需指定模型参数。更多能力边界说明见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `Authorization` | Header | 是 | `Bearer <API-Key>`，API Key 需在控制台 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 获取 |
| `workspaceId` | Base URL 路径 | 是 | 构成 Base URL 的一部分：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，需在 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 中获取 |
| `query` | JSON Body（`/search` 和 `/chat`） | 是 | 用户原始查询文本，长度 ≤ 2048 字符 |
| `top_k` | JSON Body（仅 `/search`） | 否 | 返回切片数量，默认 5，最大 20 |
| `stream` | JSON Body（仅 `/chat`） | 否 | 布尔值，控制是否启用 SSE 流式响应，默认 `true` |

> **注意**：`/chat` 接口不支持 `model` 字段传参——这与通用大模型聊天接口不同；其模型调度完全由知识上下文与系统策略隐式决定。此行为已在 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 明确说明，避免与 `/v1/services/aigc/text-generation/generation` 等 OpenAPI 接口混淆。

## 使用方式

1. **构造 Base URL**：将业务空间 ID（如 `ws-abc123`）代入 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`；
2. **设置请求头**：`Authorization: Bearer <your_api_key>`；
3. **发起请求**：
   - 检索：`POST /api/v1/indices/knowledge/search`，Body 示例：`{"query": "百炼如何配置知识库？", "top_k": 3}`；
   - 问答：`POST /api/v2/apps/knowledge/chat`，Body 示例：`{"query": "百炼如何配置知识库？", "stream": true}`；
4. **处理响应**：`/search` 返回 JSON 数组；`/chat` 在 `stream=true` 时需按 SSE 格式解析事件流（`event: chunk`, `data: {...}`）。

## 限制和注意事项

- **限流策略**：默认按用户维度限流 25 QPS，超限返回 `429 Too Many Requests`，需客户端实现退避重试；
- **知识库前提**：所有接口要求至少一个已发布且状态为“可用”的知识库，否则返回 `400 Bad Request` 或 `404 Not Found`；
- **地域约束**：Base URL 固定为 `cn-beijing` 区域，不支持切换地域；
- **无异步轮询机制**：`/chat` 接口不提供 `job_id` + `GET /status` 异步模式，必须使用 SSE 或同步阻塞等待完整响应（`stream=false` 时）；
- **输入长度限制**：`query` 字段严格限制 ≤ 2048 Unicode 字符，超长将被截断或报错（非静默处理）。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


