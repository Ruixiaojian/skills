# knowledge

knowledge 是百炼平台提供的知识增强型 AI 服务模块，支持基于私有知识库的语义检索与多阶段智能问答。该能力通过 DashScope 应用网关提供 RESTful API，与底层 OpenAPI（如 `CreateIndex`、`Retrieve`）解耦，面向业务应用层封装，适用于 RAG 场景下的快速集成。详细设计与行为请参考 [知识检索与问答](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索**：跨多个已发布知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），不调用大模型，纯向量/关键词混合召回。  
- **知识问答**：端到端流式问答，内部自动完成「问题理解→知识检索→答案生成」三阶段，通过 SSE 返回结构化响应（含 `plan`、`tool_calls`、`response` 字段）。  
- 所有功能均依赖预构建并发布的知识库索引，不支持运行时上传或动态索引构建。具体能力边界详见 [知识检索与问答](../../raw/application-api-reference/knowledge.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `knowledge_ids` | string[] | 是（检索）/ 否（问答） | 检索时指定参与查询的知识库 ID 列表；问答时若未指定，则使用应用绑定的默认知识库 |
| `query` | string | 是 | 用户原始查询文本，长度 ≤ 2048 字符 |
| `top_k` | integer | 否（默认 5） | 检索返回切片数（范围 1–50）；问答中影响检索阶段召回数量 |
| `stream` | boolean | 否（默认 true） | 仅问答接口有效，设为 `false` 时返回完整 JSON 响应而非 SSE 流 |

> **注意**：`top_k` 在问答接口中实际生效值受后端策略限制，可能被截断至 ≤10，与 [知识检索与问答](../../raw/application-api-reference/knowledge.md) 中文档描述的“范围 1–50”存在不一致，以实际 API 响应为准。

## 使用方式

1. **准备环境**：在控制台获取业务空间 ID（workspaceId）和 API Key，构造 Base URL：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`  
2. **发起请求**：  
   - 知识检索：`POST /api/v1/indices/knowledge/search`，Body 示例：  
     ```json
     { "knowledge_ids": ["k1", "k2"], "query": "百炼平台如何接入知识库？", "top_k": 3 }
     ```  
   - 知识问答：`POST /api/v2/apps/knowledge/chat`，Header 需含 `Authorization: Bearer <API-Key>`，Body 同上（`stream` 可选）  
3. **处理响应**：检索返回标准 JSON；问答若启用 `stream=true`，需按 SSE 协议解析 `event: plan/data: {...}` 等事件流。完整调用示例见 [知识检索与问答](../../raw/application-api-reference/knowledge.md)。

## 限制和注意事项

- **鉴权与域名**：必须使用业务空间专属域名（含 workspaceId），不可复用通用 DashScope OpenAPI 域名；API Key 需在 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 单独创建。  
- **限流策略**：默认 25 QPS（用户维度），超限返回 `429 Too Many Requests`，需客户端实现退避重试。  
- **知识库状态**：仅 `published` 状态的知识库可被检索/问答调用；草稿或已下线知识库不参与计算。  
- **无状态设计**：问答接口不维护会话上下文，如需多轮对话，须由应用层自行管理历史消息并拼入 `query`。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


