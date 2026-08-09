# qwen api reference

Qwen 系列大模型通过百炼平台提供多种 API 接入方式，支持文本生成、多轮对话、工具调用等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过 DashScope SDK 或标准 HTTP 请求调用，并依赖有效的 API Key 认证。

## 支持的模型与功能

当前 Qwen 系列支持以下主流接入协议：

- **OpenAI 兼容 Chat Completions**：适用于已使用 OpenAI 客户端（如 `openai>=1.0`）的项目，可零代码修改迁移 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)  
- **OpenAI 兼容-Responses**：内置联网搜索、代码解释器及网页内容提取能力，自动维护对话上下文，适合快速构建智能助手 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)  
- **Anthropic 兼容 Messages**：支持 `tool_use`、`thinking` 等结构化输出，适用于需要可控推理链路的场景 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)  
- **DashScope 原生接口**：提供最全参数控制（如 `incremental_output`、`enable_search`）、细粒度流式响应及模型专属能力（如 Qwen2-VL 的[多模态](../concepts/multimodal.md)输入），推荐用于生产环境深度定制  

> **注意**：[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)中 `response_format` 参数在 DashScope 原生接口中对应为 `result_format`，且仅部分模型支持 JSON Schema 输出；实际行为请以 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中最新说明为准。

## 关键参数

| 参数名 | 类型 | 说明 | 备注 |
|--------|------|------|------|
| `model` | string | 模型标识符，如 `qwen-max`、`qwen-plus`、`qwen-turbo` | 必填，不同接口对取值范围要求不同 |
| `messages` | array | 对话历史，格式为 `[{"role": "user", "content": "..."}]` | OpenAI/Anthropic 接口强制要求；DashScope 支持 `prompt` 字段替代 |
| `stream` | boolean | 是否启用流式响应 | 所有接口均支持，但流式 chunk 结构存在差异 |
| `tools` | array | 工具定义列表（JSON Schema 格式） | Anthropic 和 DashScope 原生接口完整支持；[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)仅部分模型支持 |
| `max_tokens` | integer | 最大生成 token 数 | DashScope 接口默认值为 1024，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)默认为 4096 |

## 使用方式

1. **认证**：通过环境变量 `DASHSCOPE_API_KEY` 或请求头 `Authorization: Bearer <api_key>` 提供密钥  
2. **Endpoint 示例**：
   - DashScope：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`  
   - OpenAI 兼容：`POST https://dashscope.aliyuncs.com/v1/chat/completions`  
3. **SDK 调用（Python）**：
   ```python
   from dashscope import Generation
   response = Generation.call(model='qwen-max', messages=[{'role': 'user', 'content': '你好'}])
   ```

## 限制和注意事项

- 单次请求 `messages` 总长度（含 system [prompt](../guides/prompt.md)）不得超过 32768 tokens（Qwen2 系列）或 65536 tokens（Qwen3 系列），超长将被截断并返回 `400` 错误  
- OpenAI 兼容接口不支持 `logprobs` 和 `n > 1` 的并行采样；如需多候选输出，请改用 DashScope 原生接口  
- 所有接口均禁止在 `system` 角色中注入指令性内容（如“你必须回答…”），该行为可能触发安全拦截  
- 流式响应中，OpenAI 兼容接口返回 `delta` 字段，DashScope 返回 `output.text` 增量片段，客户端需按协议解析

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


