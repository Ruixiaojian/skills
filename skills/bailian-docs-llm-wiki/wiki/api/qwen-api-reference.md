# qwen api reference

Qwen 系列大模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过阿里云 AccessKey 进行身份认证，并遵循统一的配额与计费规则。

## 支持的模型/功能

当前支持的 Qwen 模型包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 及 `qwen2.5-*` 系列（如 `qwen2.5-7b-instruct`），覆盖高性能、高性价比与轻量部署场景。各接口支持的功能略有差异：

- **OpenAI 兼容 Chat Completions**：支持标准 `chat/completions` 请求，适用于已有 OpenAI 生态的应用迁移；[原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中明确指出其“迁移成本最低”。
- **OpenAI 兼容-Responses**：内置联网搜索、代码解释器和网页内容提取三类工具，自动维护对话历史，适合需要增强推理能力的场景；该能力在 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中被强调为“无需手动维护”。
- **Anthropic 兼容-Messages**：支持 `tool_use`、`thinking` 等结构化输出，适用于需显式控制思考链与工具调用流程的场景；[原文标题](../../raw/model-api-reference/qwen-api-reference.md) 明确说明其“支持思考和工具调用”。

> **注意**：`qwen-vl`（[多模态](../concepts/multi-modal.md)）与 `qwen-audio` 模型**不**支持 Anthropic Messages 接口，仅可通过 DashScope 原生接口调用——此限制未在 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中说明，需以 DashScope 官方文档为准。

## 关键参数

通用关键参数（各接口基本一致）：
- `model`: 必填，指定模型 ID（如 `"qwen-plus"`）；
- `messages`: 必填，对话消息数组，格式为 `[{ "role": "user", "content": "..." }]`；
- `temperature`: 控制输出随机性（0.0–2.0，默认 1.0）；
- `max_tokens`: 输出最大 token 数（不同模型上限不同，`qwen-turbo` 默认 8192）；
- `tools`: 工具定义数组（仅 DashScope 和 Anthropic Messages 接口原生支持；[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)需通过 `tool_choice="auto"` 触发，但工具执行逻辑由服务端托管）。

## 使用方式

1. **认证**：使用阿里云 `AccessKeyId` 与 `AccessKeySecret` 签名，或通过 STS [Token](../concepts/token.md) 临时凭证；
2. **Endpoint**：
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/compatible-mode/v1`；
   - DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`；
3. **示例请求（curl）**：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model":"qwen-plus","messages":[{"role":"user","content":"你好"}]}'
   ```

## 限制和注意事项

- 单次请求 `messages` 总长度（含 system [prompt](../guides/prompt.md)）不得超过模型上下文窗口（如 `qwen-max` 为 32768 tokens）；
- [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**不支持**流式响应中的 `delta.tool_calls` 结构，工具调用结果始终以 `content` 字段返回（DashScope 原生接口支持完整 `tool_calls` 流式解析）；
- 所有接口默认启用安全过滤，敏感内容可能被拦截并返回 `400` 错误；如需调整策略，须通过百炼控制台申请白名单；
- 调用频率限制按项目（Project）维度统计，超出后返回 `429 Too Many Requests`。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


