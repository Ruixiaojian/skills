# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接口，支持文本生成、多轮对话、工具调用等核心能力。开发者可根据技术栈兼容性、功能需求和部署场景选择合适的接入方式。所有接口均需通过百炼平台鉴权，并遵循统一的计费与配额规则。

## 支持的模型与功能

当前 Qwen 系列支持以下主流调用方式：

- **OpenAI 兼容 Chat Completions**：适用于已使用 OpenAI SDK 的项目，可零代码修改迁移；支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等全部公开模型，但部分高级参数（如 `tool_choice` 的细粒度控制）需参考 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中的兼容性说明。
- **OpenAI 兼容-Responses**：内置联网搜索、代码解释器与网页内容提取能力，自动维护对话历史；该模式不支持自定义 system [prompt](../guides/prompt.md) 的逐轮覆盖，详见 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)。
- **Anthropic 兼容-Messages**：支持 `max_tokens`、`temperature`、`tool_use` 等 Anthropic 标准参数，但 Qwen 模型对 `stop_sequences` 的处理逻辑与 Anthropic 原生实现存在差异，> **注意**：实际行为以 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中“Anthropic兼容-Messages”章节为准，而非 Anthropic 官方文档。
- **DashScope 原生接口**：功能最完整，支持流式响应、长上下文分块、自定义 stop words、logprobs 输出及模型专属参数（如 `enable_search`），推荐新项目优先采用。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `model` | string | 模型标识符，如 `qwen-max`、`qwen-plus`；必须与所选接口类型匹配 | 是 |
| `messages` | array | 对话消息列表，格式为 `[{ "role": "user", "content": "..." }]`；`system` 角色仅 DashScope 和 OpenAI Chat Completions 支持 | 是（除 Anthropic Messages 使用 `system` 字段） |
| `temperature` | number | 控制输出随机性，范围 `[0.0, 2.0]`，默认 `1.0` | 否 |
| `top_p` | number | 核采样阈值，范围 `[0.0, 1.0]`，默认 `1.0` | 否 |
| `max_tokens` | integer | 最大生成 token 数，不同模型上限不同（如 `qwen-turbo` 默认 8192） | 否 |
| `stream` | boolean | 是否启用流式响应；仅 DashScope 和 OpenAI Chat Completions 支持 | 否 |

> **注意**：`tools` 和 `tool_choice` 参数在 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)中仅部分生效，完整工具调用能力需通过 DashScope 或 Anthropic Messages 接口实现，具体约束见 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)。

## 使用方式

1. **认证**：所有请求需携带 `Authorization: Bearer <api_key>`，API Key 从百炼控制台「API 密钥管理」获取；
2. **Endpoint 示例**：
   - DashScope：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
   - OpenAI Chat Completions：`POST https://dashscope.aliyuncs.com/v1/chat/completions`
3. **SDK 调用**：推荐使用官方 `dashscope` Python SDK（v1.20.0+）或 `openai` SDK（v1.0+），初始化时指定 `base_url` 和 `api_key` 即可自动路由。

## 限制和注意事项

- 单次请求 `messages` 总长度（含 [prompt](../guides/prompt.md) + history）不得超过模型 context length（如 `qwen-max` 为 32768 tokens），超长输入将被截断且无警告；
- [OpenAI 兼容接口](../concepts/openai-compatible-api.md)不支持 `response_format`（如 JSON mode）和 `parallel_tool_calls`，此类功能仅 DashScope 原生接口支持；
- 所有接口均按实际输入 + 输出 token 计费，空格、换行符、标点均计入 token；
- 流式响应中 `delta.content` 可能为空字符串（表示中间 token 分片），客户端需忽略空 content 并持续拼接；
- 模型版本升级可能影响输出稳定性，生产环境建议锁定 `model` 版本号（如 `qwen-max-20240701`），而非使用别名 `qwen-max`。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


