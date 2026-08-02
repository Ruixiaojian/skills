# knowledge

knowledge 模块提供基于[知识库](../concepts/knowledge-base.md)的语义检索与智能问答能力，属于 DashScope 应用网关体系，通过 HTTP REST 接口调用，不依赖 OpenAPI RPC 接口（如 `CreateIndex` 等）。其核心能力分为知识检索与知识问答两类，适用于 RAG 场景下的结构化知识调用。详细接口定义与行为规范见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索**：跨多个[知识库](../concepts/knowledge-base.md)执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于召回阶段。
- **知识问答**：端到端问答流程，通过 SSE [流式输出](../concepts/streaming-output.md)，依次经历规划（planning）、工具调用（tool calling）、生成（generation）三个阶段，支持上下文感知与多轮交互。  
  > **注意**：该问答流程与传统单次 LLM 调用不同，需客户端正确处理 SSE event stream；具体阶段语义和事件格式详见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 关键参数

| 参数 | 说明 | 必填 | 示例 |
|------|------|------|------|
| `Authorization` | Bearer 鉴权头，值为 API Key | 是 | `Bearer ak-xxx` |
| `workspaceId` | 业务空间 ID，用于拼接 Base URL | 是 | `ws-abc123` → Base URL: `https://ws-abc123.cn-beijing.maas.aliyuncs.com` |
| `top_k`（检索） | 返回最相关的切片数量，默认 5，最大 20 | 否 | `10` |
| `stream`（问答） | 是否启用 SSE 流式响应，布尔值 | 否（默认 `true`） | `false`（禁用流式） |

所有请求必须使用业务空间 ID 构造专属 Base URL，不可复用通用域名；API Key 获取路径见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 使用方式

1. **准备环境**：在控制台获取 API Key 和 workspaceId（参见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)）；
2. **构造请求**：
   - 检索：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`
   - 问答：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat`
3. **发送请求**：携带 `Authorization` 头，Body 为 JSON（含 `query`、`knowledgeIds` 等字段）；
4. **处理响应**：
   - 检索返回标准 JSON 数组；
   - 问答默认返回 SSE 流，需按 `event: planning/data: {...}` 等格式解析各阶段事件。

## 限制和注意事项

- **限流策略**：默认用户维度 25 QPS，超限返回 `429 Too Many Requests`，需实现退避重试；
- **[知识库](../concepts/knowledge-base.md)范围**：检索与问答均仅作用于已发布（Published）状态的知识库，草稿或禁用状态不可见；
- **Base URL 动态性**：每个 workspaceId 对应唯一域名，不可硬编码通用地址（如 `maas.aliyuncs.com`），否则请求失败；
- > **注意**：文档中提及的 `api/v2/apps/knowledge/chat` 路径与部分旧版 SDK 示例中的 `/v1/knowledge/chat` 存在版本不一致，以 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中的路径为准。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


