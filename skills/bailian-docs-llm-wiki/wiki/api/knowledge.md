# knowledge

knowledge 是百炼平台提供的知识检索与问答能力，基于 RAG（[检索增强生成](../concepts/rag.md)）架构，支持跨知识库语义检索与流式智能问答。该能力通过 DashScope 应用网关提供 HTTP REST 接口，与底层 OpenAPI（如 `CreateIndex`、`Retrieve` 等）分离，面向业务集成场景设计。详细接口规范和行为定义见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索**：跨多个已接入知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于构建自定义检索链路。
- **知识问答**：端到端流式问答，输出包含规划（planning）、工具调用（tool calling）、生成（generation）三个阶段的 SSE 响应，需客户端支持流式解析。
- 不依赖特定大模型选型——底层模型由业务空间绑定的默认推理服务自动调度，开发者无需显式指定模型 ID。此行为与 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 一致。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `knowledgeIds` | string[] | 是（检索）/否（问答） | 检索时指定参与联合检索的知识库 ID 列表；问答时若未传，则使用应用绑定的默认知识库 |
| `query` | string | 是 | 用户原始查询文本，长度 ≤ 2048 字符 |
| `topK` | number | 否 | 检索返回切片数，默认 5，最大 20；问答中影响检索阶段召回数量 |
| `stream` | boolean | 否（默认 `true`） | 仅问答接口有效，设为 `false` 时返回完整 JSON 响应（非流式） |
| `workspaceId` | path variable | 是 | Base URL 中必需拼接的业务空间标识，非请求体参数 |

> **注意**：`maxTokens`、`temperature` 等 LLM 控制参数**不支持**在知识问答接口中透传。该限制已在 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 明确说明，与部分旧版文档中提及的“支持模型参数覆盖”存在矛盾，请以本页为准。

## 使用方式

1. **准备凭证**：从控制台 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 获取 API Key，从 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取 `workspaceId`；
2. **构造 URL**：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`；
3. **发起请求**：
   - 检索：`POST /api/v1/indices/knowledge/search`，Body 示例：
     ```json
     { "knowledgeIds": ["k-abc123", "k-def456"], "query": "百炼平台如何配置知识库？", "topK": 10 }
     ```
   - 问答：`POST /api/v2/apps/knowledge/chat`，Header 需含 `Authorization: Bearer <API-Key>`，Body 至少含 `query` 字段；
4. **处理响应**：检索返回 JSON 数组；问答默认 SSE 流式，每行一个 `data: {...}` 事件，需按 `event:` 字段区分阶段类型。

## 限制和注意事项

- **限流策略**：默认用户维度 25 QPS，超出将返回 `429 Too Many Requests`，需自行实现退避重试；
- **知识库状态依赖**：仅 `ACTIVE` 状态的知识库参与检索/问答，`PENDING` 或 `FAILED` 状态会被自动跳过；
- **字符限制**：`query` 超过 2048 字符将被截断，不报错但语义可能失真；
- **无异步轮询机制**：所有接口均为同步或流式响应，不提供 `job_id` + 轮询模式；
- **知识更新延迟**：新上传文档完成向量化后约 1–3 分钟生效，具体延迟取决于文档长度与向量维度。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


