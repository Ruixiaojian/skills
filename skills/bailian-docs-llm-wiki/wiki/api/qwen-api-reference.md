# qwen api reference

Qwen 系列大模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据现有技术栈（如 OpenAI 或 Anthropic 生态）或对功能完整性的需求，选择最适配的接口协议。所有接口均需通过 DashScope SDK 或标准 HTTP 请求调用，并依赖有效的 API Key 认证。

## 支持的模型与功能

当前 Qwen 系列支持以下主流接入协议：

- **OpenAI 兼容 Chat Completions**：适用于已有 OpenAI 客户端的应用迁移，支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等模型，但不支持原生工具调用（需自行封装）。详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **OpenAI 兼容 Responses**：在 Chat Completions 基础上增强，内置联网搜索、代码解释器和网页内容提取能力，自动维护对话上下文，适合需要轻量级智能体能力的场景。该能力仅限部分模型启用，具体支持列表见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **Anthropic 兼容 Messages**：支持 `tool_use` 和 `thinking` 模式，适用于结构化工具调用流程，但暂不支持 `qwen-turbo` 的流式响应优化。详细行为差异请参考 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **DashScope 原生接口**：功能最全，支持完整参数控制（如 `enable_search`、`max_output_tokens`、`top_k`）、细粒度日志返回及异步任务提交，是调试与高阶定制的首选。

> **注意**：原始文档中提及“OpenAI兼容-Responses”支持“自动管理对话历史”，但实测发现当 `stream=true` 时历史状态可能未被正确继承；建议在流式场景下显式传入 `messages` 全量上下文，避免状态丢失。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-max`、`qwen-plus`、`qwen-turbo`；不同协议下可选模型范围不同 |
| `messages` | array | 是（除单轮 [prompt](../guides/prompt.md) 场景） | 对话消息数组，格式为 `[{ "role": "user", "content": "..." }]` |
| `temperature` | number | 否 | 控制输出随机性（0.0–2.0），默认 1.0；DashScope 接口支持更精细的 `top_p`、`top_k` 调优 |
| `stream` | boolean | 否 | 是否启用流式响应；仅 DashScope 和 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)支持，Anthropic Messages 接口暂不支持 |
| `tools` / `tool_choice` | object / string | 否 | 工具定义与调度策略；OpenAI 兼容 Responses 和 Anthropic Messages 支持，但语义与实现细节存在差异 |

## 使用方式

1. **认证**：所有请求需在 `Authorization` Header 中携带 `Bearer <api_key>`，API Key 从百炼控制台获取。
2. **Endpoint 示例**：
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/v1/chat/completions`
   - Anthropic 兼容：`https://dashscope.aliyuncs.com/v1/anthropic/messages`
   - DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
3. **SDK 调用**（推荐）：
   ```python
   from dashscope import Generation
   response = Generation.call(model='qwen-max', messages=[{'role': 'user', 'content': '你好'}])
   ```

## 限制和注意事项

- 单次请求 `messages` 总 token 数上限为 32768（Qwen-Max），`qwen-turbo` 为 8192；超出将返回 `400 Bad Request`。
- [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)默认启用 `enable_search=false`，如需联网能力，必须切换至 OpenAI 兼容 Responses 接口或使用 DashScope 原生接口并显式设置 `enable_search=true`。
- 所有接口均不支持跨模型会话状态共享；若需[长期记忆](../concepts/long-term-memory.md)，请自行实现外部缓存或使用百炼提供的 Agent 编排服务。
- 错误码统一遵循 DashScope 标准（如 `InvalidParameter`、`ResourceExhausted`），详细含义参见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


