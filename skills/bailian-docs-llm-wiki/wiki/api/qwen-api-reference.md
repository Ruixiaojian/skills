# qwen api reference

Qwen 系列大模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过阿里云认证（AccessKey 或 STS [Token](../concepts/token.md)）调用。

## 支持的模型与功能

当前 Qwen 系列支持以下主流接入协议：

- **OpenAI 兼容 Chat Completions**：适用于已有 OpenAI 客户端的应用迁移，支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等模型，但不支持原生工具调用（需自行封装）。详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **OpenAI 兼容-Responses**：内置联网搜索、代码解释器、网页内容提取三类工具，自动维护对话历史，适合快速构建智能助手。该接口对 `messages` 格式有特定约束，详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **Anthropic 兼容 Messages**：支持 `tool_use`、`thinking` 等结构化输出，适用于需要可控推理链路的场景；注意其 `max_tokens` 语义与 OpenAI 不同（指输出 token 上限，不含输入）。详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **DashScope 原生接口**：提供最全参数控制（如 `incremental_output`、`enable_search`、`tools` schema 注册），支持流式响应、[函数调用](../concepts/function-calling.md)、长上下文（最高 128K tokens）及私有模型部署。推荐新项目优先选用。

> **注意**：`qwen-vl`（多模态）和 `qwen-audio` 模型**不支持** [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，仅可通过 DashScope 原生接口调用，相关限制请参阅最新 [DashScope 文档](https://help.aliyun.com/zh/dashscope/developer-reference/quick-start)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-max`、`qwen-plus`、`qwen-turbo`；不同接口对取值范围要求不同（例如 Anthropic 接口仅支持 `qwen-max`） |
| `messages` | array | 是 | 对话消息列表，格式为 `[{"role": "user", "content": "..."}, ...]`；[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)中 `content` 可为字符串或数组（含 text/image_url），DashScope 接口支持更丰富的 content 结构 |
| `temperature` | number | 否 | 采样温度，默认 `0.8`；取值范围 `0.0–1.0`，`0` 表示确定性输出 |
| `top_p` | number | 否 | 核采样阈值，默认 `0.95`；与 `temperature` 互斥使用效果更佳 |
| `stream` | boolean | 否 | 是否启用流式响应；[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)默认 `false`，DashScope 默认 `true`（若未显式设置） |

## 使用方式

1. **认证**：使用阿里云 AccessKey ID/Secret 或 STS [Token](../concepts/token.md)，通过 `Authorization: Bearer <token>` 或 `X-DashScope-Signature` 头传递；
2. **Endpoint**：
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/v1/chat/completions`
   - Anthropic 兼容：`https://dashscope.aliyuncs.com/v1/messages`
   - DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`；
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

- 单次请求最大 `input` 长度受模型 context window 限制（`qwen-turbo`: 8K, `qwen-plus`: 32K, `qwen-max`: 128K），超出将返回 `400 Bad Request`；
- OpenAI 兼容接口**不支持** `system` 角色消息（会被忽略），需改用 `user` + 提示词前置方式模拟；
- 所有接口均按 `input_tokens + output_tokens` 计费，`output_tokens` 包含工具调用返回内容；
- 流式响应中，OpenAI 兼容接口返回 `delta.content` 字段，DashScope 返回 `output.text` 字段，解析逻辑需区分；
- 调用失败时优先检查 `X-DashScope-Request-ID` 响应头，便于问题定位。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


