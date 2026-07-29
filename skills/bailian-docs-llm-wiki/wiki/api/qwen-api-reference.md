# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过百炼平台鉴权访问，并遵循统一的配额与计费规则。

## 支持的模型与功能

当前 Qwen 系列支持以下主流接入协议：

- **OpenAI 兼容 Chat Completions**：适用于已有 OpenAI 客户端（如 `openai==1.0+`）的快速迁移，支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等模型，但不支持原生工具调用（需依赖 [OpenAI兼容-Responses](https://help.aliyun.com/zh/model-studio/openai-compatible-responses/) 的增强能力）。详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

- **OpenAI兼容-Responses**：在 Chat Completions 基础上扩展联网搜索、代码解释器、网页内容提取等内置工具，自动维护对话历史，适合需要轻量级智能体能力的场景。该模式下 `messages` 格式与标准 OpenAI 一致，但 `tool_choice` 和 `tools` 字段行为以 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 为准。

- **Anthropic兼容-Messages**：完全兼容 Anthropic Messages API 规范，支持 `system` 消息、分步思考（`max_tokens` 控制推理深度）、结构化工具调用（`tool_use`），适用于对可控推理链有明确要求的场景。参数语义与 Anthropic 文档一致，但模型列表仅限 Qwen 系列已发布的版本，具体请参阅 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

- **DashScope 原生接口**：百炼专属协议，提供最细粒度控制（如 `incremental_output`、`enable_search`、`top_k` 等），支持流式响应、长上下文截断策略、自定义 stop words 等高级特性，是生产环境推荐使用的接口。

> **注意**：原始文档中提及的 “OpenAI兼容-Responses” 支持“自动管理对话历史”，但实际使用中若启用 `stream: true`，需自行处理 `delta` 中的 `tool_calls` 分片；该行为与标准 OpenAI 流式响应不完全一致，建议在非流式模式下使用工具调用功能。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-max`、`qwen-plus`；不同接口支持的模型范围略有差异，DashScope 接口支持最全 |
| `messages` | array | 是 | 对话消息列表，格式为 `[{ "role": "user/system/assistant", "content": "..." }]`；Anthropic 接口额外支持 `tool_result` 角色 |
| `temperature` | number | 否 | 采样温度，默认 `0.8`；DashScope 接口支持 `0.0–2.0`，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)限制为 `0.0–2.0`（部分旧版 SDK 可能截断为 `0.0–1.0`） |
| `max_tokens` | integer | 否 | 最大生成 token 数，DashScope 默认 `1024`，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)默认 `4096`（实际受模型 context length 限制） |
| `tools` / `tool_choice` | object / string | 否 | 工具定义与调用策略；仅 DashScope 和 OpenAI兼容-Responses 支持完整工具调用，Anthropic 接口使用 `tools` + `tool_choice: "auto"` 或 `"any"` |

## 使用方式

1. **认证**：所有请求需携带 `Authorization: Bearer <api_key>`，API Key 从百炼控制台「API 密钥管理」获取；
2. **Endpoint**：
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`
   - OpenAI兼容-Responses：`https://dashscope.aliyuncs.com/compatible-mode/v1/responses`
   - Anthropic 兼容：`https://dashscope.aliyuncs.com/compatible-mode/v1/messages`
   - DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
3. **示例（curl）**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-max",
           "messages": [{"role": "user", "content": "你好"}]
         }'
   ```

## 限制和注意事项

- 单次请求 `messages` 总长度（含 system [prompt](../guides/prompt.md)）不得超过模型 context length（如 `qwen-max` 为 32768 tokens），超长时 DashScope 接口支持 `truncate` 策略，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)默认静默截断；
- 工具调用返回的 `tool_calls` 在流式响应中可能跨 chunk 分片，需按 `index` 和 `id` 合并（DashScope 接口保证单次调用原子性，OpenAI兼容-Responses 需自行聚合）；
- `qwen-turbo` 不支持 `system` 消息（Anthropic 和 DashScope 接口均忽略该字段），此限制未在 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中明确说明，实际调用时应避免传入；
- 所有接口均不支持 `logprobs` 输出，且 `n > 1`（多候选生成）仅 DashScope 接口支持。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


