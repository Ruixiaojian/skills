# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过阿里云认证鉴权，并遵循统一的计费与配额规则。

## 支持的模型与功能

当前 Qwen 系列支持以下主流接入协议：

- **OpenAI 兼容 Chat Completions**：适用于已有 OpenAI SDK 的项目，可零代码迁移；支持 `qwen-plus`、`qwen-max`、`qwen-turbo` 等模型，但不支持流式工具调用响应解析（详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)）。
- **OpenAI 兼容-Responses**：内置联网搜索、代码解释器、网页内容提取三类工具，自动维护对话历史，适合快速构建智能助手；该模式下 `messages` 格式与标准 OpenAI 不完全一致，需参考 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中的字段说明。
- **Anthropic 兼容-Messages**：支持 `tool_use`、`thinking` 等结构化输出，适用于需要可控推理路径的场景；注意其 `system` 字段行为与 Anthropic 原生 API 存在差异（> **注意**：`system` 提示词在百炼 Anthropic 兼容接口中会被截断至 4096 token，而官方 Anthropic 文档未声明此限制，实际行为以 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 为准）。
- **DashScope 原生接口**：功能最全，支持细粒度参数控制（如 `incremental_output`、`enable_search`）、自定义 stop words 及完整日志回溯，推荐用于生产环境高可靠性场景。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-max`、`qwen-plus`；不同接口对模型命名略有差异，DashScope 接口要求全小写，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)接受 `qwen-max` 或 `qwen-max-20240718` 等版本后缀 |
| `messages` | array | 是 | 对话消息列表，格式为 `[{ "role": "user", "content": "..." }]`；Anthropic 兼容接口要求首条消息 `role` 为 `user`，且 `system` 字段必须单独传入顶层参数 |
| `temperature` | number | 否 | 采样温度，默认 `0.8`；DashScope 接口支持 `0.0–2.0`，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)仅接受 `0.0–1.0` |
| `tools` | array | 否 | 工具定义列表，仅 DashScope 和 Anthropic 兼容接口支持；OpenAI 兼容-Responses 的工具由平台预置，不可自定义 |

## 使用方式

1. **认证**：使用阿里云 AccessKey ID/Secret 或 STS [Token](../concepts/token.md)，通过 `Authorization: Bearer <api_key>`（OpenAI/Anthropic 兼容）或 `X-DashScope-Signature`（DashScope）传递；
2. **Endpoint**：
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/v1/chat/completions`
   - Anthropic 兼容：`https://dashscope.aliyuncs.com/v1/messages`
   - DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`；
3. **请求示例（DashScope）**：
```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
        "model": "qwen-max",
        "input": {"messages": [{"role":"user","content":"你好"}]},
        "parameters": {"temperature": 0.5}
      }'
```

## 限制和注意事项

- 单次请求 `messages` 总长度上限为 32768 token（Qwen-Max），`qwen-turbo` 为 8192 token；超出将返回 `400 Bad Request`；
- [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)不支持 `response_format`（如 JSON Schema 强约束），如需结构化输出，请改用 DashScope 接口并设置 `output_format: "json"`；
- 所有接口默认启用流式响应（`stream: true`），但 OpenAI 兼容-Responses 的流式 chunk 中 `delta.tool_calls` 字段可能缺失部分工具参数，建议在非流式模式下验证工具调用逻辑；
- 配额按 Project 维度隔离，可通过 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 查看各模型的 QPS 与并发限制。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)




