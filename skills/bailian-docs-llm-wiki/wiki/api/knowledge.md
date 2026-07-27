# knowledge

knowledge 是百炼平台提供的知识增强型 AI 服务模块，支持基于私有知识库的语义检索与多阶段流式问答。该能力通过 DashScope 应用网关提供 RESTful API，与底层 OpenAPI（如 `CreateIndex`、`Retrieve`）解耦，面向业务应用层封装，适用于 RAG 场景下的快速集成。详细设计与行为请参考 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 支持的模型/功能

- **知识检索**：跨多个已发布知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），不调用大模型，纯向量+关键词混合召回。
- **知识问答**：端到端流式问答，内部自动完成问题理解→知识检索→推理规划→工具调用→答案生成，通过 SSE 返回三阶段事件（`plan`、`tool_call`、`answer`）。  
  > **注意**：知识问答接口不支持指定 LLM 模型，其底层模型由业务空间配置决定，与 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中描述一致；若需控制模型，请使用底层 OpenAPI 的 `Retrieve` + 自定义 LLM 调用组合方案，详见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | string | 是 | 用户原始查询文本 |
| `top_k` | integer | 否 | 检索/问答中返回的最大切片数，默认 5（检索）或 3（问答） |
| `indices` | array[string] | 否 | 指定参与检索的知识库 ID 列表；未传则使用当前业务空间默认知识库 |
| `stream` | boolean | 否 | 仅问答接口有效，设为 `true` 启用 SSE 流式响应（默认 `true`） |

## 使用方式

1. **Base URL 构造**：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，其中 `{workspaceId}` 需从 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取；
2. **鉴权**：所有请求必须携带 `Authorization: Bearer <API-Key>`，API Key 从 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 获取；
3. **调用示例（知识检索）**：
   ```bash
   curl -X POST "https://my-workspace.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search" \
     -H "Authorization: Bearer sk-xxx" \
     -H "Content-Type: application/json" \
     -d '{"query":"百炼平台如何接入知识库？","top_k":3}'
   ```

## 限制和注意事项

- **限流策略**：默认用户级 25 QPS，超限返回 `429 Too Many Requests`，需客户端实现退避重试；
- **知识库状态要求**：仅 `published` 状态的知识库可被检索或问答调用，草稿或已下线库将被忽略；
- **问答流式阶段不可跳过**：即使禁用工具调用，`plan` 和 `answer` 阶段仍会发出，无法跳过中间阶段直接获取最终答案；
- **跨区域访问限制**：Base URL 中的地域固定为 `cn-beijing`，不支持切换至其他地域 endpoint。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


