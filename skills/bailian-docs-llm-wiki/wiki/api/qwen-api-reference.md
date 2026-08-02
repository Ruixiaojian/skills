# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据现有技术栈（如 OpenAI 或 Anthropic 生态）或对功能完整性的需求，选择最适配的接口协议。所有接口均需通过 DashScope SDK 或 HTTP 请求调用，并依赖有效的 API Key 认证。

## 支持的模型与功能

当前 Qwen 系列支持以下主流接入协议：

- **OpenAI 兼容 Chat Completions**：适用于已有 OpenAI 客户端的应用迁移，兼容 `openai>=1.0` SDK，支持 `messages` 输入格式及流式响应。详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **OpenAI 兼容 Responses**：在基础 Chat Completions 上增强，内置联网搜索、代码解释器和网页内容提取能力，自动维护对话上下文，适合需要自主工具调度的场景。该能力描述见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **Anthropic 兼容 Messages**：支持 `system` 消息、`tool_use` 块及思考过程输出（`content` 中含 `text` 与 `tool_use` 混合结构），适用于需显式控制工具调用流程的场景。具体字段定义参见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **DashScope 原生接口**：提供最全参数控制（如 `top_k`、`repetition_penalty`、`incremental_output`），支持长上下文、自定义 stop words 及细粒度 token 统计，是调试与高性能部署的首选。

> **注意**：OpenAI 兼容 Responses 的 `max_tokens` 行为与标准 OpenAI API 不一致——其实际限制为输出 token 总数（含工具调用返回内容），而非常规的 `completion_tokens`；此差异已在 DashScope 文档中明确，但 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 未作说明，建议以 DashScope 官方文档为准。

## 关键参数

| 参数名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `model` | string | 模型标识符，如 `qwen-max`、`qwen-plus`、`qwen-turbo` | 必填 |
| `temperature` | float | 控制输出随机性，范围 `[0.0, 2.0]` | `1.0` |
| `top_p` | float | 核采样阈值，范围 `[0.0, 1.0]` | `0.8` |
| `max_tokens` | integer | 最大生成 token 数（不含 [prompt](../guides/prompt.md)） | `1024`（部分接口上限不同） |
| `stream` | boolean | 是否启用流式响应 | `false` |

> **注意**：`max_tokens` 在 OpenAI 兼容 Responses 接口中实际限制总输出长度（含工具结果序列），而 DashScope 接口严格限制为模型生成部分；使用时请按所选协议查阅对应文档。

## 使用方式

1. **认证**：通过环境变量 `DASHSCOPE_API_KEY` 或请求头 `Authorization: Bearer <api_key>` 传入密钥；
2. **Endpoint 示例**：
   - DashScope：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/v1/chat/completions`
3. **SDK 调用（Python）**：
   ```python
   from dashscope import Generation
   response = Generation.call(model='qwen-max', messages=[{'role': 'user', 'content': '你好'}])
   ```

## 限制和注意事项

- 所有接口均受百炼平台配额与速率限制约束，具体额度可在控制台查看；
- `qwen-max` 和 `qwen-plus` 支持 32K 上下文，`qwen-turbo` 为 8K，超长输入将被截断；
- 工具调用（如联网搜索）仅在 OpenAI 兼容 Responses 和 Anthropic 兼容 Messages 中可用，DashScope 原生接口需自行集成工具调度逻辑；
- 流式响应中，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)返回 `delta.content`，而 DashScope 返回 `output.text` 字段，客户端需适配。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


