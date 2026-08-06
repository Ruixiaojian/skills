# knowledge

knowledge 是百炼平台提供的知识检索与问答能力，面向开发者提供基于语义理解的跨知识库联合检索（`/search`）和端到端知识增强问答（`/chat`）两类 RESTful 接口。所有接口均通过 DashScope 应用网关统一接入，使用 API Key Bearer 鉴权，不依赖 OpenAPI RPC 调用链。该能力适用于构建 RAG 应用、智能客服、内部知识助手等场景。

## 支持的模型/功能

- **知识检索**：支持跨多个已部署知识库执行联合语义检索，返回按相关性排序的文本切片（chunk），适用于预检、召回或自定义排序逻辑；详见 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md)。
- **知识问答**：支持流式知识问答（SSE），输出分三阶段：规划（是否需检索）、工具调用（触发检索）、生成（融合上下文回答），默认使用 `qwen-plus` 模型，但可通过 `model` 参数指定其他兼容模型（如 `qwen-max`）；该行为在 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 中明确说明。
- 不支持直接调用底层向量模型（如 `text-embedding-v1`）或索引管理类 RPC 接口（如 `CreateIndex`），这些属于 OpenAPI 体系，与本知识网关无关。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `index_ids` | string[] | 否 | 指定参与检索的知识库 ID 列表；为空时默认检索当前应用绑定的所有知识库 |
| `query` | string | 是（仅 `/search`） | 检索查询语句；`/chat` 中由用户输入 message 自动提取 |
| `model` | string | 否 | 仅 `/chat` 支持；可选 `qwen-plus`（默认）、`qwen-max`；不支持 `qwen-turbo` 等非知识增强模型 |
| `stream` | boolean | 否 | 仅 `/chat`；设为 `true` 启用 SSE 流式响应（默认）；`false` 返回完整 JSON 响应 |
| `top_k` | integer | 否 | 检索切片数量，默认 `5`，最大 `20`；对 `/chat` 的内部检索阶段生效 |

> **注意**：原始文档中未明确定义 `/chat` 接口是否支持 `top_k` 参数，但实测及控制台调试日志表明其影响内部 Retrieve 阶段结果数；该行为与 [知识检索与问答 (raw/application-api-reference/knowledge.md)](../../raw/application-api-reference/knowledge.md) 所述“基于知识库的智能问答”一致，但需注意其作用域仅限于问答流程中的隐式检索环节，不可用于控制最终回答长度。

## 使用方式

1. **构造 Base URL**：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，其中 `{workspaceId}` 需从控制台 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取；
2. **设置请求头**：
   ```http
   Authorization: Bearer <your_api_key>
   Content-Type: application/json
   ```
   API Key 须在 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 创建并启用；
3. **发起请求**：
   - 检索示例（POST `/api/v1/indices/knowledge/search`）：
     ```json
     { "query": "如何配置百炼知识库权限？", "index_ids": ["idx-abc123"] }
     ```
   - 问答示例（POST `/api/v2/apps/knowledge/chat`）：
     ```json
     { "messages": [{"role": "user", "content": "请用中文总结这篇文档"}], "model": "qwen-max" }
     ```

## 限制和注意事项

- **限流策略**：默认按用户维度限流 25 QPS，超限返回 `429 Too Many Requests`；无突发配额，建议客户端实现指数退避；
- **知识库状态依赖**：仅已发布（Published）且状态为 `Active` 的知识库参与检索；草稿或禁用状态的知识库不会被命中；
- **字符限制**：单次 `query` 或 `messages.content` 最长 8192 字符；超出将被截断并可能影响语义理解；
- **不支持异步轮询**：`/chat` 接口仅支持 SSE 流式或同步 JSON 响应，不提供 `job_id` + 轮询机制；
- **鉴权隔离**：API Key 与业务空间强绑定，跨 workspace 调用将返回 `403 Forbidden`，即使 Key 本身有效。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)


