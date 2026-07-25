# qwen api reference

Qwen 系列大模型通过百炼平台提供多种 API 接入方式，支持文本生成、多轮对话、工具调用等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过阿里云 AccessKey 认证，并遵循统一的配额与计费规则。

## 支持的模型/功能

当前 Qwen 系列支持以下主流调用方式，覆盖不同生态适配场景：

- **OpenAI 兼容 Chat Completions**：完全兼容 OpenAI `chat/completions` 接口规范，适用于已有 OpenAI SDK 的项目快速迁移。详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **OpenAI 兼容-Responses**：在标准 Chat Completions 基础上增强，内置联网搜索、代码解释器、网页内容提取等工具链，自动维护对话上下文，适合需要轻量级智能体能力的场景。该能力说明见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **Anthropic 兼容-Messages**：支持 Anthropic Messages API 标准，可启用 `tool_use`、`thinking` 等高级能力，适用于需结构化工具调用与推理过程显式控制的场景。具体参数与行为请参考 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **DashScope 原生接口**：百炼专属协议，提供最全参数控制（如 `enable_search`、`max_output_tokens`、`top_k`）、细粒度流式响应及调试字段（如 `usage` 中的 `prompt_tokens_details`），推荐用于生产环境高可控性需求。

> **注意**：OpenAI 兼容-Responses 与 DashScope 接口均支持联网搜索，但 Responses 的搜索结果默认经摘要处理并注入 system message，而 DashScope 需显式设置 `enable_search: true` 且返回原始搜索片段；二者行为不一致，建议以 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中 DashScope 文档为准进行关键路径开发。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `model` | string | 模型标识符，如 `qwen-max`、`qwen-plus`、`qwen-turbo`；不同接口对 model 命名格式要求不同（如 OpenAI 接口需前缀 `qwen-`） | 是 |
| `messages` | array | 对话消息列表，格式为 `[{ "role": "user", "content": "..." }]`；Anthropic 接口使用 `system` 字段而非 system message | 是（除部分单轮请求外） |
| `temperature` | number | 控制输出随机性，范围 0.0–2.0，默认 1.0 | 否 |
| `top_p` | number | 核采样阈值，范围 0.0–1.0，默认 0.8 | 否 |
| `max_tokens` | integer | 最大生成 token 数，不同模型有硬上限（如 qwen-turbo ≤ 8192） | 否 |

> **注意**：`max_tokens` 在 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)中实际对应 `max_completion_tokens`，而 DashScope 接口使用 `max_output_tokens`；若混用文档示例可能导致截断异常，请严格按所选接口的参数命名约定配置。

## 使用方式

1. **认证**：使用阿里云主账号或 RAM 子账号的 `AccessKeyId` 和 `AccessKeySecret`，通过 HTTP Header `Authorization: Bearer <api_key>`（OpenAI/Anthropic 兼容）或 `Authorization: Bearer <dashscope_api_key>`（DashScope）传递；
2. **Endpoint**：
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/v1/chat/completions`
   - Anthropic 兼容：`https://dashscope.aliyuncs.com/v1/messages`
   - DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
3. **调用示例（curl）**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/v1/chat/completions \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-max",
           "messages": [{"role": "user", "content": "你好"}]
         }'
   ```

## 限制和注意事项

- 单次请求 `messages` 总长度（含 [prompt](../guides/prompt.md) + history）不得超过模型 context window（如 `qwen-max` 为 32768 tokens），超长将被截断且不报错；
- 流式响应（`stream: true`）在 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)中返回 `text/event-stream`，DashScope 接口返回 JSON Lines（每行一个 `{"output": {...}}` 对象）；
- 所有接口均不支持跨模型 session 共享；若需长期对话状态管理，须由客户端自行缓存 `messages` 并完整传入每次请求；
- 免费调用量受百炼平台账户等级限制，超出后按 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中公示价格计费。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


