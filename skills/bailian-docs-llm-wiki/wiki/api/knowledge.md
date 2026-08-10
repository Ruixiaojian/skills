# knowledge

knowledge 是百炼平台提供的知识增强型 API 服务，支持跨知识库的语义检索与基于知识的流式问答。该能力通过 DashScope 应用网关提供 REST 接口，与底层 OpenAPI（如 `CreateIndex`、`Retrieve`）分离，面向业务集成场景设计。详细接口定义与行为规范请参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索**：跨多个已发布知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于召回阶段；
- **知识问答**：端到端 RAG 流式问答，输出包含规划（planning）、工具调用（tool calling）、生成（generation）三阶段结果，通过 SSE 协议逐块返回；
- 不依赖特定大模型选型，底层由平台统一调度适配的知识增强推理引擎执行，开发者无需显式指定模型 ID。具体能力边界详见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | string | 是 | 检索或问答的用户输入文本 |
| `top_k` | integer | 否 | 检索返回切片数，默认 5，最大 20；问答接口不支持该参数 |
| `indices` | array of string | 否 | 指定参与检索的知识库 ID 列表；未传则使用默认知识库（若已配置） |
| `stream` | boolean | 否 | 仅知识问答接口有效，设为 `true` 启用 SSE 流式响应（默认 `true`） |

> **注意**：`indices` 参数在 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中明确要求为字符串数组，但部分旧版 SDK 示例误传为逗号分隔字符串，实际请求将被拒绝。

## 使用方式

1. **Base URL 构造**：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，其中 `{workspaceId}` 需从控制台 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取；
2. **鉴权**：所有请求必须携带 `Authorization: Bearer <API-Key>`，API Key 请在 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 创建；
3. **调用示例**（知识检索）：
   ```bash
   curl -X POST "https://my-workspace.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search" \
     -H "Authorization: Bearer ak-xxx" \
     -H "Content-Type: application/json" \
     -d '{"query":"百炼平台如何接入知识库？","top_k":3}'
   ```

## 限制和注意事项

- **限流策略**：默认按用户维度限流 25 QPS，超出将返回 `429 Too Many Requests`；
- **知识库状态要求**：仅 `published` 状态的知识库参与检索与问答，草稿或已下线库不可见；
- **SSE 连接超时**：知识问答接口流式响应最长持续 60 秒，超时后连接关闭，需客户端重试；
- **不支持自定义 embedding 模型或 reranker**：所有[向量化与重排序](../concepts/embedding-rerank.md)逻辑由平台托管，暂不开放配置入口。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


