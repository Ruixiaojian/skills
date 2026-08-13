# knowledge

knowledge 是百炼平台提供的知识增强型 AI 服务模块，支持基于私有知识库的语义检索与多阶段智能问答。其核心能力通过 DashScope 应用网关暴露为 RESTful API，与底层 OpenAPI（如 `CreateIndex`、`Retrieve`）在调用方式、鉴权机制和路由结构上存在明确分层。开发者需按业务空间维度组织请求，并严格遵循鉴权与限流规则。

## 支持的模型/功能

- **知识检索**：跨多个已发布的知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于召回增强场景。  
- **知识问答**：端到端 RAG 流式问答，采用规划 → 工具调用（检索）→ 生成三阶段范式，响应通过 SSE 流式传输。  
该能力不依赖特定大模型选型，而是由应用网关统一调度底层检索与生成服务，具体模型版本由平台自动管理。详见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 关键参数

- `workspaceId`：必需，业务空间 ID，用于构造 Base URL（`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`）。  
- `Authorization: Bearer <API-Key>`：必需，API Key 需在控制台 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 获取。  
- 请求体中需指定 `knowledgeIds`（知识库 ID 列表）、`query`（用户问题）等语义参数；知识问答接口额外支持 `stream: true` 控制[流式输出](../concepts/streaming-output.md)。  
> **注意**：`workspaceId` 不同于项目 ID 或租户 ID，必须从 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 页面准确获取，否则将返回 404 或鉴权失败 —— 此细节在 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中明确强调，但部分旧版 SDK 文档误标为“可选”。

## 使用方式

1. 确保知识库已发布（未发布的知识库不可被检索或问答调用）；  
2. 构造请求 URL：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`（检索）或 `/api/v2/apps/knowledge/chat`（问答）；  
3. 设置请求头 `Authorization: Bearer <your-api-key>`；  
4. 发送 JSON body（检索示例含 `knowledgeIds`, `query`, `topK`；问答示例含 `messages`, `knowledgeIds`, `stream`）。  
完整请求示例与字段说明见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 限制和注意事项

- **限流策略**：默认按用户维度限流 25 QPS，超限返回 `429 Too Many Requests`，需客户端实现退避重试；  
- **知识库状态**：仅 `published` 状态的知识库参与检索与问答，草稿或已下线库将被忽略；  
- **Base URL 区域固定**：当前仅支持 `cn-beijing` 地域，URL 中硬编码该区域，不支持动态切换；  
- **SSE 兼容性**：知识问答接口强制使用 SSE，需客户端正确处理 `event: chunk`、`data:` 及连接中断重连逻辑。  
以上约束均以 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 为准，其他文档若提及更高 QPS 或多地域支持，属过时信息。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


