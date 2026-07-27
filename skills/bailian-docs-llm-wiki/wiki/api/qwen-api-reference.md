# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过阿里云 AccessKey 进行身份认证，并遵循统一的配额与计费规则。

## 支持的模型/功能

当前支持的 Qwen 模型包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 及 `qwen2.5-*` 系列（如 `qwen2.5-7b-instruct`），覆盖高性能、均衡型与轻量级场景。各接口支持的功能略有差异：

- **OpenAI 兼容 Chat Completions**：支持标准 `messages` 输入、`stream` 流式响应、`function calling`（需显式启用 `tools` 参数），但暂不支持 `response_format`（如 JSON Schema）强制约束 —— 该限制在 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中未明确说明，实际调用时会返回 `400` 错误。
- **OpenAI 兼容-Responses**：自动集成联网搜索、代码解释器等内置工具，无需配置 `tools` 即可触发，适合快速构建智能助手；其对话状态管理逻辑与标准 Chat Completions 不同，详见 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)。
- **Anthropic 兼容-Messages**：支持 `system` 角色、`tool_use` 块及 `max_tokens` 精确控制，但不支持 `temperature` 超出 `[0.0, 1.0]` 范围（超出将被截断），此行为与 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中“参数自由设置”的描述存在偏差。
- **DashScope 原生接口**：提供最全参数支持（如 `top_p`, `repetition_penalty`, `stop` 多值数组），并独占 `enable_search`、`enable_code_interpreter` 等高级开关，是调试与生产环境的首选。

> **注意**：`qwen-max` 在 DashScope 接口下支持 `output_format: "json"` 强制输出 JSON，但在 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)中该能力不可用，且文档未同步更新此限制。

## 关键参数

| 参数名 | 类型 | 说明 | 接口支持情况 |
|--------|------|------|--------------|
| `model` | string | 必填，如 `"qwen-max"` 或 `"qwen2.5-72b-instruct"` | 全部支持 |
| `messages` | array | 标准对话消息列表，含 `role`（`user`/`assistant`/`system`）和 `content` | Chat Completions / Anthropic / DashScope |
| `tools` | array | 工具定义列表（OpenAI 格式）或 `tool_choice` 控制策略 | Chat Completions / Anthropic / DashScope（后者用 `tool_list`） |
| `stream` | boolean | 是否启用流式响应 | 全部支持（Anthropic 接口需设 `stream: true` 且 `messages` 长度 ≤ 1） |
| `max_tokens` | integer | 最大输出 token 数 | 全部支持，但 Anthropic 接口实际生效值受模型最大上下文限制 |

## 使用方式

1. **认证**：使用阿里云 RAM 用户的 `AccessKeyId` 和 `AccessKeySecret`，通过 `Authorization: Bearer <api_key>`（OpenAI/Anthropic 接口）或 `X-DashScope-Access-Key`（DashScope 接口）传递；
2. **Endpoint**：
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/v1/chat/completions`
   - Anthropic 兼容：`https://dashscope.aliyuncs.com/v1/messages`
   - DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
3. **示例请求（DashScope）**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-max",
           "input": {"messages": [{"role": "user", "content": "你好"}]},
           "parameters": {"max_tokens": 512}
         }'
   ```

## 限制和注意事项

- 所有接口单次请求 `messages` 总长度（输入+输出）不得超过模型上下文窗口（如 `qwen-max` 为 32768 tokens），超长将被截断且不报错；
- [OpenAI 兼容接口](../concepts/openai-compatible-api.md)的 `functions` 参数已废弃，应改用 `tools`；旧版 `function_call` 字段在 `qwen2.5+` 模型中不再生效；
- 流式响应中，Anthropic 接口返回 `delta` 字段，而 OpenAI 接口返回 `choices[0].delta`，客户端需按协议解析；
- 跨区域调用（如华东1调用华北2的 endpoint）可能导致延迟升高或鉴权失败，建议 endpoint 与 AccessKey 所属地域一致。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


