# knowledge

知识检索与问答是百炼平台提供的核心 RAG 能力，通过统一的应用网关暴露 RESTful 接口，支持跨知识库语义检索与多阶段流式问答。该能力独立于底层 OpenAPI（如 `CreateIndex`、`Retrieve` 等 RPC 接口），面向业务应用层封装，适用于快速集成智能客服、文档助手等场景。详细设计与行为请参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索**：跨多个已发布知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），不涉及大模型生成。
- **知识问答**：基于知识库的端到端问答，采用三阶段流式响应（规划 → 工具调用 → 生成），通过 SSE 返回，支持上下文感知与引用溯源。
- 所有功能均运行在 DashScope 应用网关，**不直接暴露底层向量引擎或索引管理接口**。底层模型选型由平台自动匹配，开发者无需指定模型 ID；如需控制模型，请参见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中关于 `/api/v2/apps/knowledge/chat` 的说明。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `Authorization` | Header | 是 | `Bearer <API-Key>`，API Key 需在控制台 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 获取 |
| `workspaceId` | Base URL | 是 | 构成 Base URL 的路径前缀，例如 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，须在 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 中获取 |
| `knowledgeIds` | Body（search） | 否 | 检索时指定知识库 ID 列表；若为空，则检索当前 workspace 下所有已发布知识库 |
| `stream` | Body（chat） | 否 | 布尔值，默认 `true`；设为 `false` 将禁用 SSE，返回完整 JSON 响应 |

> **注意**：`knowledgeIds` 在 `/api/v1/indices/knowledge/search` 中为可选字段，但 `/api/v2/apps/knowledge/chat` 要求至少关联一个已发布的知识库（通过应用配置绑定，而非请求体传入）。此差异已在 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中明确，开发者需注意接口语义边界。

## 使用方式

1. **准备环境**：确认业务空间（workspace）已创建，并在其中发布至少一个知识库；
2. **构造请求**：
   - 检索：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`
   - 问答：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat`
3. **发送请求**：携带 `Authorization` 头与合法 JSON body（含 `query` 字段），问答接口建议启用 `Accept: text/event-stream` 并处理 SSE 流；
4. **解析响应**：检索返回 `chunks` 数组；问答返回按阶段划分的 `event` 类型消息（`plan` / `tool_call` / `answer`）。

## 限制和注意事项

- **限流策略**：默认按用户维度限流 25 QPS，超出将返回 `429 Too Many Requests`；如需提升配额，需提交工单申请。
- **知识库状态要求**：仅“已发布”状态的知识库参与检索与问答，草稿或停用状态不可见。
- **Base URL 区域固定**：当前仅支持 `cn-beijing` 地域，URL 中的地域标识不可替换，否则请求失败。
- **鉴权隔离**：API Key 与 workspace 绑定，跨 workspace 调用将被拒绝，即使 API Key 有效。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


