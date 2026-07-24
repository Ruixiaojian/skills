# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接入方式，支持文本生成、多工具协同、对话状态管理等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过阿里云认证（AccessKey 或 STS [Token](../concepts/token.md)）调用。

## 支持的模型与功能

当前 Qwen 系列支持以下主流接入协议：

- **OpenAI 兼容 Chat Completions**：适用于已使用 `openai` Python SDK 或类似客户端的应用，零代码改造即可迁移。支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等全部公开模型 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。  
- **OpenAI 兼容-Responses**：在标准 Chat Completions 基础上，自动集成联网搜索、代码解释器、网页内容提取三类工具，并维护完整对话历史，适合需要增强推理能力的场景 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。  
- **Anthropic 兼容-Messages**：支持 `tool_use`、`thinking` 等结构化输出，适用于需显式控制工具调用链路或分步推理的业务逻辑 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。  
- **DashScope 原生接口**：提供最细粒度参数控制（如 `incremental_output`、`enable_search`）、流式响应优化及私有模型部署支持，是高级定制场景的首选。

> **注意**：`OpenAI 兼容-Responses` 的 `max_tokens` 行为与标准 OpenAI API 不一致——其实际限制包含系统提示词与工具调用上下文总长度，而非常规的 `completion_tokens`；该差异未在 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中明确说明，建议以 DashScope 文档为准。

## 关键参数

| 参数名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `model` | string | 模型标识符，如 `qwen-max`、`qwen-plus` | 必填 |
| `messages` | array | 对话消息列表，格式同 OpenAI；`role` 支持 `system`/`user`/`assistant`/`tool` | — |
| `tools` | array | 工具定义列表（仅 Responses 和 Anthropic Messages 支持） | `[]` |
| `tool_choice` | string / object | 控制工具调用策略（`auto`/`none`/`required`/`{"type": "function", "name": "xxx"}`） | `auto` |
| `stream` | boolean | 是否启用流式响应 | `false` |

## 使用方式

1. **认证**：使用阿里云 AccessKey ID/Secret 或短期 STS [Token](../concepts/token.md)，通过 `Authorization: Bearer <token>` 或 `X-DashScope-Signature` 头传递。  
2. **Endpoint**：各协议对应独立 endpoint（例如 DashScope 为 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`）。  
3. **示例请求（DashScope）**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-max",
           "input": {"messages": [{"role": "user", "content": "你好"}]},
           "parameters": {"temperature": 0.8}
         }'
   ```

## 限制和注意事项

- 所有接口单次请求 `messages` 总 token 数上限为 32768（Qwen2/Qwen3 系列），超出将返回 `400 Bad Request`。  
- `OpenAI 兼容-Responses` 不支持 `functions` 字段（已废弃），必须改用 `tools` + `tool_choice`；该变更未在原始文档中同步更新。  
- 流式响应中，`OpenAI 兼容` 接口返回 `delta.content`，而 `DashScope` 返回 `output.text`，客户端需适配不同字段路径。  
- 免费额度仅适用于 `qwen-turbo` 和 `qwen-plus` 的非流式调用；`qwen-max` 及流式请求均计费。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


