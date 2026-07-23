# qwen api reference

Qwen API 提供多种调用方式，支持文本生成、工具调用、联网搜索等能力，开发者可根据技术栈兼容性与功能需求选择合适接口。所有接口均基于 Qwen 系列大模型（如 Qwen2、Qwen2.5、Qwen3）提供服务，需通过百炼平台鉴权访问。详细参数说明与行为差异请参考 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

## 支持的模型与功能

- **基础文本生成**：支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等多档位模型，适用于通用对话、摘要、创作等场景。
- **增强能力接口**：
  - OpenAI 兼容 Chat Completions：适合已有 OpenAI 生态集成的应用快速迁移；
  - OpenAI 兼容-Responses：自动启用联网搜索、代码解释器、网页提取等工具链，无需手动管理工具调用流程；
  - Anthropic 兼容 Messages：支持 `tool_use`、`thinking` 等结构化输出，适配 Anthropic 工作流；
  - DashScope 原生接口：提供最全参数控制（如 `top_k`、`repetition_penalty`、`enable_search`），是调试与高阶定制的首选。

> **注意**：`qwen-max` 在 DashScope 接口中默认启用思考模式（`enable_thinking=true`），但在 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)中该参数不可设；此行为差异已在 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中明确标注，使用时需注意一致性。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 | 备注 |
|--------|------|------|----------|------|
| `model` | string | 模型标识符，如 `qwen-max`、`qwen-plus` | 是 | 不同接口对模型命名格式要求一致，详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) |
| `messages` | array | 对话历史，格式为 `[{ "role": "...", "content": "..." }]` | 是（Chat Completions / Messages） | DashScope 接口额外支持 `system` 角色和 `tools` 字段 |
| `tools` | array | 工具定义列表（JSON Schema 格式） | 否 | 仅 DashScope 和 Anthropic Messages 接口原生支持；OpenAI 兼容-Responses 的工具由服务端自动注入，不开放显式传参 |
| `enable_search` | boolean | 是否启用联网搜索（DashScope 专属） | 否 | 默认 `false`；启用后将自动触发搜索并融合结果 |

## 使用方式

1. **认证**：使用百炼平台颁发的 `API Key`，通过 `Authorization: Bearer <api_key>` 请求头传递；
2. **Endpoint 示例**：
   - DashScope：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
   - OpenAI 兼容：`POST https://dashscope.aliyuncs.com/v1/chat/completions`
3. **SDK 调用**：推荐使用官方 `dashscope` Python SDK（v1.20.0+）或 `openai` 客户端（v1.0+），配置 `base_url` 指向百炼 OpenAI 兼容地址即可复用现有逻辑。

## 限制和注意事项

- 单次请求 `messages` 总长度（token 数）上限为 32768（Qwen3 模型）或 8192（旧版模型），具体以实际模型文档为准；
- 工具调用（如 `code_interpreter`）在 OpenAI 兼容-Responses 接口中为全自动模式，**不支持用户自定义工具函数**，与 DashScope 接口的可控性存在本质差异；
- 流式响应（`stream=true`）在所有接口中均支持，但字段结构不同：DashScope 返回 `output.text`，OpenAI 兼容返回 `choices[0].delta.content`；
- > **注意**：原始文档中 OpenAI 兼容-Responses 的“自动管理对话历史”描述与实际行为存在偏差——当启用 `enable_search` 时，历史会被截断以预留上下文空间，该限制未在 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中明示，建议在长对话场景下主动控制 `max_tokens` 与历史长度。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


