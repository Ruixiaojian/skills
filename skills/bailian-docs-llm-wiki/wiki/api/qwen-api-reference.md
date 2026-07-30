# qwen api reference

Qwen 系列大模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过阿里云 AccessKey 进行身份认证，并遵循统一的配额与计费规则。

## 支持的模型/功能

当前 Qwen 系列支持以下主流调用方式（按协议兼容性分类）：
- **OpenAI 兼容 Chat Completions**：完全兼容 OpenAI `chat/completions` 接口规范，适用于已有 OpenAI SDK 的项目快速迁移；支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等全部公开文本生成模型。详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **OpenAI 兼容-Responses**：在标准 Chat Completions 基础上增强，内置联网搜索、代码解释器、网页内容提取等工具链，自动维护对话历史，适合需要轻量级 RAG 或自动化执行的场景。该能力说明见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **Anthropic 兼容-Messages**：适配 Anthropic Messages API 协议，支持 `tool_use`、`thinking` 等结构化输出能力，适用于需显式控制推理路径或集成 Anthropic 生态工具的场景。具体参数与行为请参考 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **DashScope 原生接口**：百炼专属协议，提供最细粒度的参数控制（如 `incremental_output`、`enable_search`）、完整流式响应支持及调试字段（如 `usage` 细分 token 类型），推荐用于生产环境高可靠性要求场景。

> **注意**：`qwen-vl`（[多模态](../concepts/multi-modal.md)）和 `qwen-audio` 模型**不支持** [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，仅可通过 DashScope 原生接口调用；此限制未在 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中明确说明，以 DashScope 官方文档为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"qwen-max"`、`"qwen-plus"`；不同接口对取值范围有差异（例如 Anthropic 接口不支持 `qwen-turbo`） |
| `messages` | array | 是（Chat Completions / Anthropic） | 对话消息列表，格式为 `{"role": "user/system/assistant", "content": "..."}`
| `tools` | array | 否 | 工具定义数组（JSON Schema），仅 DashScope 和 Anthropic 接口支持完整工具声明 |
| `tool_choice` | string/object | 否 | 控制工具调用策略，DashScope 支持 `"auto"`/`"required"`/`{"type": "function", "name": "xxx"}`，OpenAI 接口仅支持字符串形式 |

## 使用方式

1. **认证**：所有请求需在 Header 中携带 `Authorization: Bearer <api_key>`，其中 `api_key` 为阿里云 DashScope API Key（非 AccessKey）；
2. **Endpoint**（示例）：
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/v1/chat/completions`
   - Anthropic 兼容：`https://dashscope.aliyuncs.com/v1/messages`
   - DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
3. **流式响应**：各接口均支持 `stream=true`，但字段结构不同（如 OpenAI 返回 `delta`，DashScope 返回 `output.text` 分段）；建议优先使用 DashScope 原生接口以获得一致的流式语义。

## 限制和注意事项

- 单次请求 `messages` 总长度（含 system [prompt](../guides/prompt.md)）不得超过模型上下文窗口（如 `qwen-max` 为 32768 tokens），超长将被截断且**不返回警告**；
- [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)的 `temperature` 取值范围为 `[0.0, 2.0]`，而 DashScope 原生接口为 `[0.0, 1.0]`，跨接口迁移时需归一化处理；
- 所有接口默认启用安全过滤，敏感内容可能被静默拦截或替换为占位符，如需关闭需单独申请白名单权限；
- `max_tokens` 在 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)中表示**响应上限**，在 DashScope 原生接口中表示**总 token 数上限（[prompt](../guides/prompt.md) + completion）**，行为差异显著。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


