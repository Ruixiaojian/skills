# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据现有技术栈（如 OpenAI 或 Anthropic 生态）或对功能完整性的需求，选择最适配的接口协议。所有接口均需通过 DashScope SDK 或 HTTP 直连调用，并依赖有效的 API Key 认证。

## 支持的模型与功能

当前 Qwen 系列支持以下主流接入协议：

- **OpenAI 兼容 Chat Completions**：适用于已使用 `openai` Python SDK 的项目，可零代码修改迁移 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)；  
- **OpenAI 兼容 Responses**：内置联网搜索、代码解释器和网页内容提取能力，自动维护对话上下文，适合需要增强型推理的场景 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)；  
- **Anthropic 兼容 Messages**：支持 `tool_use`、`thinking` 等结构化输出，适用于需显式控制思维链与工具调用的流程 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)；  
- **DashScope 原生接口**：提供最全参数控制（如 `incremental_output`、`enable_search`、`max_input_tokens`），是调试与高阶定制的首选。

> **注意**：OpenAI 兼容 Responses 接口在 v2.0+ SDK 中已统一为 `chat/completions` 路径下的扩展模式，而非独立 endpoint；旧文档中描述的 `/v1/responses` 路径已弃用，请以 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中最新链接为准。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `model` | string | 模型标识符，如 `qwen-max`、`qwen-plus`、`qwen-turbo`；不同协议下命名规则一致 | 是 |
| `messages` | array | 对话历史，格式为 `[{ "role": "user", "content": "..." }]`；Anthropic 协议使用 `content` 数组并支持 `tool_result` | 是 |
| `tools` | array | 工具定义列表（JSON Schema），仅 DashScope 和 Anthropic Messages 支持完整工具声明 | 否 |
| `tool_choice` | string / object | 控制工具调用策略（`auto`/`none`/`{"type": "function", "name": "xxx"}`） | 否 |
| `stream` | boolean | 是否启用流式响应；[OpenAI 兼容接口](../concepts/openai-compatible-api.md)默认 `false`，DashScope 默认 `true` | 否 |

## 使用方式

1. **认证**：通过环境变量 `DASHSCOPE_API_KEY` 或请求头 `Authorization: Bearer <api_key>` 传入；
2. **Endpoint 示例**：
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/v1/chat/completions`
   - Anthropic 兼容：`https://dashscope.aliyuncs.com/v1/messages`
   - DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
3. **SDK 调用**（Python）：
   ```python
   from dashscope import Generation
   response = Generation.call(model='qwen-max', messages=[...], stream=False)
   ```

## 限制和注意事项

- 单次请求 `messages` 总长度（含 system [prompt](../guides/prompt.md)）不得超过模型 context window（如 `qwen-max` 为 32768 tokens）；
- [OpenAI 兼容接口](../concepts/openai-compatible-api.md)不支持 `system` role 的直接传递，需合并至首条 `user` message 或使用 `extra_body={"system": "..."}`（DashScope SDK v2.0+）；
- 工具调用返回的 `tool_calls` 在 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)中为非标准字段，需解析 `response.choices[0].message.tool_calls`（非 `function_call`）；
- 所有接口均按 token 数量计费，输入/输出 token 分开计量，详见 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中的计费说明。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


