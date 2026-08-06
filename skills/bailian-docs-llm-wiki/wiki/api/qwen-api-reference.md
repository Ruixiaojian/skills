# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接口，支持文本生成、多轮对话、工具调用等核心能力。开发者可根据技术栈兼容性、功能需求和部署场景选择 OpenAI 兼容、Anthropic 兼容或 DashScope 原生接口。所有接口均需通过阿里云百炼平台认证访问。

## 支持的模型与功能

当前 Qwen 系列支持以下主流调用方式（详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)）：

- **OpenAI 兼容 Chat Completions**：适配 `openai>=1.0.0` 客户端，支持 `messages` + `model` + `stream` 等标准参数，适用于快速迁移现有应用；  
- **OpenAI 兼容 Responses**：在 Chat Completions 基础上增强，**自动管理对话历史**，并内置联网搜索、代码解释器、网页内容提取等工具链（参见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)）；  
- **Anthropic 兼容 Messages**：支持 `system` 消息、`tool_use`、`thinking` 等结构化输出，适用于需要可控推理路径的场景；  
- **DashScope 原生接口**：提供最全参数控制（如 `top_p`, `repetition_penalty`, `incremental_output`），支持长上下文、流式响应及高级日志调试（详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)）。

> **注意**：OpenAI 兼容 Responses 接口的 `tools` 字段行为与标准 OpenAI v1 API 不完全一致——其工具调用由服务端自动编排，不返回原始 tool_calls，开发者无需手动解析 `function_call`。该差异已在最新版文档中明确，旧版 SDK 示例可能未同步更新。

## 关键参数

| 参数名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `model` | string | 必填。支持 `qwen-max`, `qwen-plus`, `qwen-turbo` 等具体模型标识符 | — |
| `messages` | array | 对话历史，格式为 `[{ "role": "user/system/assistant", "content": "..."}]` | — |
| `stream` | boolean | 是否启用流式响应（SSE） | `false` |
| `max_tokens` | integer | 最大生成 token 数，受模型上下文长度限制 | `2048`（部分模型上限更高） |
| `temperature` | number | 控制输出随机性，范围 `[0.0, 2.0]` | `1.0` |
| `top_p` | number | 核采样阈值，范围 `[0.0, 1.0]` | `1.0` |

> **注意**：`repetition_penalty` 仅 DashScope 接口支持；[OpenAI 兼容接口](../concepts/openai-compatible-api.md)暂不支持该参数，若传入将被忽略。

## 使用方式

1. **认证**：使用阿里云 AccessKey ID / Secret 或 STS [Token](../concepts/token.md)，通过 `Authorization: Bearer <token>` 传递；  
2. **Endpoint**（示例）：
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`  
   - DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`  
3. **请求示例（curl）**：
   ```bash
   curl -X POST \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-max",
           "messages": [{"role":"user","content":"你好"}],
           "stream": true
         }' \
     https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
   ```

## 限制和注意事项

- 单次请求 `messages` 总长度（含 system [prompt](../guides/prompt.md)）不得超过模型上下文窗口（如 `qwen-max` 为 32768 tokens）；  
- 流式响应（`stream=true`）下，[OpenAI 兼容接口](../concepts/openai-compatible-api.md)返回 `data: {...}` SSE 格式，DashScope 返回 JSON Lines；  
- 工具调用能力仅在 **OpenAI 兼容 Responses** 和 **Anthropic 兼容 Messages** 接口中可用，Chat Completions 接口需自行实现工具调度逻辑；  
- 所有接口均遵循百炼平台配额与计费规则，详细用量统计请查阅控制台「用量中心」；  
- 模型版本升级可能导致默认 `temperature` 或 `top_p` 行为微调，建议显式指定关键采样参数以保证稳定性。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


