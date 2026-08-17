# qwen api reference

Qwen 系列大模型通过百炼平台提供多种 API 接入方式，支持文本生成、多轮对话、工具调用等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过阿里云 AccessKey 进行身份认证，并遵循统一的配额与计费规则。

## 支持的模型/功能

当前 Qwen 系列支持以下主流接口协议：
- **OpenAI 兼容 Chat Completions**：适用于已使用 OpenAI SDK 的应用，可零代码迁移；支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等模型 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)  
- **OpenAI 兼容 Responses**：在标准 Chat Completions 基础上增强，内置联网搜索、代码解释器、网页内容提取等工具链，自动维护对话历史 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)  
- **Anthropic 兼容 Messages**：支持 `tool_use`、`thinking` 等结构化输出能力，适用于需要可控推理路径的场景 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)  
- **DashScope 原生接口**：提供最全参数控制（如 `enable_search`、`max_output_tokens`、`top_p` 细粒度调节），是调试与高阶定制的首选

> **注意**：`qwen-vl`（多模态）和 `qwen-audio` 模型暂不支持 Anthropic Messages 协议，仅可通过 DashScope 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，该限制未在[文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)中明确说明，以最新控制台模型列表为准。

## 关键参数

| 参数名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `model` | string | 必填，模型标识符，如 `"qwen-max"`、`"qwen-plus"` | — |
| `messages` | array | 对话历史，格式为 `[{ "role": "user", "content": "..." }]` | — |
| `temperature` | number | 控制输出随机性，范围 `[0.0, 2.0]` | `0.8` |
| `top_p` | number | 核采样阈值，范围 `[0.0, 1.0]` | `0.8` |
| `max_tokens` | integer | 最大生成 token 数 | `2048`（部分模型上限不同） |

> **注意**：`max_tokens` 在 DashScope 接口中名为 `max_output_tokens`，而 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)统一使用 `max_tokens`；二者语义一致但字段名不兼容，需按所选协议严格匹配。

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <your_api_key>`（DashScope）或 `Authorization: Bearer <your_dashscope_api_key>`（OpenAI/Anthropic 兼容接口）  
2. **Endpoint**（以 `qwen-max` 为例）：
   - DashScope：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/v1/chat/completions`
3. **示例请求体**（OpenAI 兼容）：
   ```json
   {
     "model": "qwen-max",
     "messages": [{"role": "user", "content": "你好"}],
     "temperature": 0.5
   }
   ```

## 限制和注意事项

- 单次请求 `messages` 总长度（含 system [prompt](../guides/prompt.md)）不得超过 32768 tokens（具体依模型而定）  
- [OpenAI 兼容接口](../concepts/openai-compatible-api.md)不支持 `stream` 字段以外的流式响应元数据（如 usage、finish_reason），如需完整流控请使用 DashScope 接口  
- 所有接口均禁止用于生成违法、歧视、暴力等内容，违规调用将触发自动熔断  
- 配额与计费按模型实例独立计算，`qwen-max` 与 `qwen-plus` 不共享额度  

> **注意**：文档中提及的“自动管理对话历史”仅适用于 OpenAI 兼容 Responses 接口，而非标准 Chat Completions；该差异在[文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)中未作区分，实际开发中需确认所用子路径是否为 `/v1/responses`。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


