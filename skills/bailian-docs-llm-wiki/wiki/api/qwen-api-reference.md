# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过阿里云认证（AccessKey 或 STS [Token](../concepts/token.md)）调用，并遵循统一的计费与配额规则。

## 支持的模型与功能

当前支持的 Qwen 模型包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 和 `qwen-vl`（多模态），具体能力因模型而异：

- **文本生成**：所有模型均支持基础 [prompt](../guides/prompt.md)-to-text 生成；
- **工具调用**：`qwen-max` 和 `qwen-plus` 支持[函数调用](../concepts/function-calling.md)（function calling）、联网搜索、代码解释器等扩展能力，需配合 [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference.md) 或 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference.md) 使用；
- **多模态理解**：`qwen-vl` 仅通过 [DashScope](../../raw/model-api-reference/qwen-api-reference.md) 原生接口支持图像输入，不兼容 OpenAI/Anthropic 标准协议。

> **注意**：文档中提及的“内置联网搜索”功能在 `qwen-turbo` 上默认不可用，实际支持情况以 [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference.md) 的最新说明为准；若调用失败，请确认模型版本与接口组合是否匹配。

## 关键参数

| 参数 | 说明 | 必填 | 示例值 |
|------|------|------|--------|
| `model` | 模型标识符 | 是 | `"qwen-max"` |
| `messages` | 对话历史（OpenAI/Anthropic 格式）或 `input`（DashScope 格式） | 是 | `[{"role":"user","content":"你好"}]` |
| `temperature` | 控制输出随机性（0.0–2.0） | 否 | `0.7` |
| `top_p` | 核采样阈值（0.0–1.0） | 否 | `0.8` |
| `max_tokens` | 最大生成长度 | 否 | `1024` |
| `tools` / `tool_choice` | 工具定义与调用策略（仅部分模型+接口支持） | 否 | 见 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference.md) 文档 |

## 使用方式

- **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**：使用标准 `openai` Python SDK，设置 `base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"` 并传入 DashScope API Key；
- **Anthropic 兼容接口**：需将 `Content-Type` 设为 `application/json`，并使用 `messages` 字段而非 `prompt`；
- **DashScope 原生接口**：推荐使用 `dashscope` SDK，支持更细粒度控制（如 `enable_search`、`enable_code_interpreter` 等布尔开关），详见 [DashScope](../../raw/model-api-reference/qwen-api-reference.md) 文档。

## 限制和注意事项

- 单次请求 `messages` 总 token 数上限为 32,768（`qwen-max`），其他模型略低；
- `qwen-vl` 图像输入仅支持 base64 编码或公网可访问 URL，不支持本地文件路径；
- 所有接口均不支持流式响应中的 `delta.tool_calls` 结构（仅返回完整 `tool_calls`），此行为与 OpenAI v1.0+ 不一致；
- 配额与计费按模型+输入/输出 token 分别统计，详细规则参见 [DashScope](../../raw/model-api-reference/qwen-api-reference.md) 官方说明。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


