# qwen api reference

Qwen 系列大模型通过百炼平台提供多种 API 接入方式，支持文本生成、多轮对话、工具调用等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过阿里云 AccessKey 认证，并遵循统一的配额与计费规则。

## 支持的模型/功能

当前 Qwen 系列支持以下主流调用方式，覆盖不同生态适配场景：

- **OpenAI 兼容 Chat Completions**：完全兼容 OpenAI `chat/completions` 接口规范，适用于已有 OpenAI SDK 的项目快速迁移。详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **OpenAI 兼容-Responses**：在标准 Chat Completions 基础上增强，内置联网搜索、代码解释器和网页内容提取三类工具，自动维护对话历史与工具调用状态。该能力文档见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **Anthropic 兼容 Messages**：支持 `messages` 接口，兼容 Anthropic 的 `system` 消息、`tool_use` 和 `tool_result` 机制，适用于需要结构化思考链与工具协同的场景。具体参数与行为请参考 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **DashScope 原生接口**：百炼原生协议，提供最细粒度的控制能力（如流式响应开关、token 统计开关、自定义 stop 字符串等），是调试与高阶定制的首选。

> **注意**：OpenAI 兼容-Responses 接口虽自动管理对话历史，但其 `max_tokens` 行为与标准 OpenAI 接口存在差异（实际限制包含系统提示与工具调用 token），而 DashScope 接口对此有明确分离控制。建议生产环境优先使用 DashScope 接口以避免歧义。

## 关键参数

通用关键参数（各接口均支持，语义一致）：

- `model`: 必填，如 `qwen-max`、`qwen-plus`、`qwen-turbo`；模型列表以控制台实时为准。
- `messages`: 对话消息数组，格式为 `[{ "role": "user" | "assistant" | "system", "content": string }]`；部分接口（如 Anthropic 兼容）额外支持 `tool_use` 类型 message。
- `temperature`: 控制输出随机性，范围 0.0–2.0，默认 1.0。
- `top_p`: 核采样阈值，范围 0.0–1.0，默认 0.8。
- `stream`: 布尔值，启用流式响应（`true` 时返回 SSE 流）。
- `max_tokens`: 限制模型生成的最大 token 数（不含输入 tokens）；**注意**：该参数在 OpenAI 兼容-Responses 接口中实际生效值受工具调用上下文影响，推荐改用 DashScope 接口的 `max_output_tokens` 实现精确控制。

## 使用方式

1. **认证**：所有请求需在 `Authorization` Header 中携带 `Bearer <your_api_key>`（DashScope 接口）或 `Bearer <your_dashscope_api_key>`（OpenAI/Anthropic 兼容接口）；API Key 从 [百炼控制台 → API 密钥管理](https://dashscope.console.aliyun.com/) 获取。
2. **Endpoint 示例**：
   - DashScope：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
   - OpenAI 兼容：`POST https://dashscope.aliyuncs.com/v1/chat/completions`
3. **SDK 调用**：推荐使用官方 `dashscope` Python SDK（v1.20.0+）或 `openai` SDK（v1.0+），后者需配置 `base_url="https://dashscope.aliyuncs.com/v1"`。

## 限制和注意事项

- 单次请求 `messages` 总长度（含 system [prompt](../guides/prompt.md)）不得超过模型 context window（如 `qwen-max` 为 32768 tokens），超长将被截断并返回 `400` 错误。
- 流式响应中，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)返回 `delta.content` 字段，DashScope 接口返回 `output.text` 字段，二者字段名不一致，集成时需适配。
- 工具调用（tool use）仅在 OpenAI 兼容-Responses 和 Anthropic 兼容 Messages 接口中原生支持；DashScope 接口需通过 `tools` + `tool_choice` 参数显式启用，且返回格式为独立 `tool_calls` 数组。
- 所有接口均不支持跨请求的长期会话状态保存；若需持久化对话历史，须由应用层自行缓存与拼接 `messages`。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


