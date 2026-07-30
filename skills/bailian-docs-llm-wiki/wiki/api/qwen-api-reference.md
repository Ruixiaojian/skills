# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据现有技术栈（如 OpenAI 或 Anthropic 生态）或对功能完整性的需求，选择最适配的接口协议。所有接口均需通过 DashScope SDK 或 HTTP 请求调用，并依赖有效的 API Key 认证。

## 支持的模型与功能

当前 Qwen 系列支持以下主流接入协议：

- **OpenAI 兼容 Chat Completions**：适用于已有 OpenAI 客户端的应用迁移，兼容 `openai>=1.0` SDK，支持 `messages` 输入格式及流式响应。详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **OpenAI 兼容 Responses**：在基础聊天能力上集成联网搜索、代码解释器和网页内容提取等内置工具，自动维护对话上下文，无需手动传入 `history`。该模式细节请参见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **Anthropic 兼容 Messages**：遵循 Anthropic Messages API 规范，支持 `tool_use`、`thinking`（推理步骤显式输出）等高级能力，适用于需要可控推理链路的场景。具体字段语义参考 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **DashScope 原生接口**：百炼专属协议，提供最全参数控制（如 `incremental_output`、`enable_search` 细粒度开关）、最长上下文（最高 32K tokens）及模型专属能力（如 Qwen2.5-VL 的多模态输入）。> **注意**：部分 DashScope 参数（如 `top_p` 范围）在旧版文档中描述为 `[0,1]`，但实测 v3.14+ SDK 已支持 `0.0–1.0` 闭区间外的扩展值（如 `0.001`），以实际 SDK 文档为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，例如 `qwen-max`、`qwen-plus`、`qwen-turbo`；不同协议下命名规则一致。 |
| `messages` | array | 是（Chat Completions / Anthropic） | 对话消息列表，每项含 `role`（`system`/`user`/`assistant`/`tool`）和 `content`；Anthropic 协议额外支持 `tool_calls` 字段。 |
| `temperature` | number | 否 | 控制输出随机性，默认 `0.8`；取值范围 `0.0–2.0`（DashScope 实际支持更宽，但建议保持 ≤1.2 以保障稳定性）。 |
| `max_tokens` | integer | 否 | 最大生成 token 数，最大值依模型而异（如 `qwen-max` 为 8192）。 |
| `tools` | array | 否 | 工具定义列表（JSON Schema 格式），仅 DashScope 和 Anthropic Messages 支持原生工具注册；[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)需通过 `function_call` 或 `tool_choice` 显式启用。 |

## 使用方式

1. **认证**：所有请求需在 `Authorization` Header 中携带 `Bearer <api_key>`，API Key 可在百炼控制台「API 密钥管理」获取。
2. **Endpoint 示例**：
   - DashScope：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
   - OpenAI 兼容：`POST https://dashscope.aliyuncs.com/v1/chat/completions`（需设置 `Content-Type: application/json`）
3. **SDK 调用（Python）**：
   ```python
   from dashscope import Generation
   response = Generation.call(
       model='qwen-max',
       messages=[{'role': 'user', 'content': '你好'}],
       temperature=0.5,
       api_key='YOUR_API_KEY'
   )
   ```

## 限制和注意事项

- **速率限制**：免费试用额度为 1000 QPM（Queries Per Minute），商用需按量计费；不同模型有独立限流策略（如 `qwen-turbo` QPM 高于 `qwen-max`）。
- **上下文长度**：`qwen-turbo` 最高支持 16K tokens 输入，`qwen-plus` 和 `qwen-max` 支持 32K；超出部分将被截断且不报错，需自行校验 `usage.total_tokens`。
- **工具调用差异**：[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)返回的 `function_call` 字段在新版 DashScope SDK 中已统一映射为 `tool_calls`，但原始响应体仍保留旧字段名；建议优先使用 SDK 封装而非直接解析 raw JSON。> **注意**：[文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中关于工具调用返回格式的示例未同步更新，应以实际 API 响应或最新 SDK 文档为准。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


