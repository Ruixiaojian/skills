# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过阿里云认证（AccessKey 或 STS [Token](../concepts/token.md)）调用，并遵循统一的计费与配额规则。

## 支持的模型与功能

当前 Qwen 系列支持以下主流接入协议：

- **OpenAI 兼容 Chat Completions**：适用于已使用 OpenAI SDK 的项目，可零代码迁移；支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等全部文本生成模型，但不原生支持工具调用（需自行封装）。详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **OpenAI 兼容-Responses**：在 Chat Completions 基础上增强，内置联网搜索、代码解释器和网页内容提取三类工具，自动维护对话历史与工具执行上下文；适合快速构建智能助手类应用。该能力仅限 `qwen-max` 和 `qwen-plus` 模型启用，具体限制见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **Anthropic 兼容-Messages**：完全兼容 Anthropic Messages API 规范，支持 `max_tokens`、`system` 消息、`tool_use` 与 `tool_result` 交互流程；适用于需要结构化思考链（Chain-of-Thought）或复杂工具编排的场景。注意：`qwen-turbo` 不支持此协议，详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **DashScope 原生接口**：百炼专属协议，提供最细粒度控制（如 `incremental_output`、`enable_search`、`top_p` 动态调整），并支持流式响应、[函数调用](../concepts/function-calling.md) schema 定义及异步任务提交；推荐用于生产环境高定制需求。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-max`、`qwen-plus`、`qwen-turbo`；不同协议下可用模型范围不同（见上节） |
| `messages` | array | 是（Chat/Anthropic/Messages） | 对话消息列表，格式为 `{"role": "user/system/assistant", "content": "..."}`；DashScope 还支持 `tool_calls` 字段 |
| `tools` | array | 否 | 工具定义列表（JSON Schema 格式），仅 DashScope 和 Anthropic Messages 支持；OpenAI Responses 的工具为预置且不可自定义 |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；所有协议均支持，但流式 chunk 结构略有差异 |

> **注意**：`temperature` 在 DashScope 中默认为 `0.8`，而在 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)中默认为 `1.0`；实际行为以 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中最新描述为准，旧文档可能未同步该差异。

## 使用方式

1. **认证**：使用阿里云 AccessKey ID/Secret 或短期 STS [Token](../concepts/token.md)，通过 `Authorization: Bearer <token>` 或 `X-DashScope-Authentication-Token`（DashScope 协议）传递；
2. **Endpoint**：
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`
   - Anthropic 兼容：`https://dashscope.aliyuncs.com/compatible-mode/v1/messages`
   - DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
3. **示例请求（DashScope）**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-max",
           "input": {"messages": [{"role":"user","content":"你好"}]},
           "parameters": {"temperature": 0.5}
         }'
   ```

## 限制和注意事项

- 所有接口单次请求 `messages` 总长度上限为 32768 token（含 system [prompt](../guides/prompt.md)），超出将返回 `400 Bad Request`；
- `qwen-turbo` 仅支持 DashScope 和 OpenAI Chat Completions 协议，不支持 Anthropic Messages 或 OpenAI Responses 的增强工具链；
- 流式响应中，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)返回 `delta` 字段，DashScope 返回 `output.text` 增量，二者解析逻辑不可混用；
- 超时时间统一为 120 秒，超时后连接关闭，不保证重试语义；
- 工具调用结果必须通过 `tool_result` 消息显式反馈给模型（Anthropic Messages）或由服务端自动注入（OpenAI Responses），手动拼接易导致上下文错乱。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


