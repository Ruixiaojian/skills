# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过百炼平台申请 API Key 并配置鉴权。

## 支持的模型与功能

当前 Qwen 系列支持以下主流接入协议：

- **OpenAI 兼容 Chat Completions**：适用于已有 OpenAI 客户端（如 `openai>=1.0`）的项目，可零修改迁移；支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等模型，但不支持流式工具调用响应解析 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)  
- **OpenAI 兼容-Responses**：在 Chat Completions 基础上增强，内置联网搜索、代码解释器和网页内容提取能力，并自动维护对话历史；适合无需手动管理上下文的轻量级应用 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)  
- **Anthropic 兼容-Messages**：支持 `tool_use`、`thinking` 等结构化输出，适用于需要显式推理链或自主工具调度的场景；注意该接口暂不支持 `qwen-turbo` 模型 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)  
- **DashScope 原生接口**：提供最全参数控制（如 `incremental_output`、`enable_search`）、细粒度错误码及调试字段，是调试与高阶定制的首选  

> **注意**：原始文档中未明确说明各接口对 `qwen2.5` 系列模型的支持状态，实际调用时请以 [DashScope 文档](https://help.aliyun.com/zh/dashscope/developer-reference/quick-start) 中的模型列表为准，避免因模型别名不一致导致 404 错误。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-max`、`qwen-plus`；不同接口对模型命名规范要求不同（DashScope 区分大小写，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)通常忽略大小写） |
| `messages` | array | 是 | 对话消息数组，格式为 `[{ "role": "user", "content": "..." }]`；Anthropic 接口使用 `content` 字段嵌套 `text` 或 `tool_use` 对象 |
| `tools` | array | 否 | 工具定义列表（仅 Anthropic Messages 和 DashScope 支持）；[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)需通过 `functions`（已弃用）或 `tool_choice`（v1.3+）启用 |
| `stream` | boolean | 否 | 是否启用流式响应；DashScope 和 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)均支持，但 Anthropic Messages 的流式格式与前两者不兼容 |

## 使用方式

1. **认证**：所有请求需携带 `Authorization: Bearer <api_key>`，API Key 从百炼控制台「API 密钥管理」获取  
2. **Endpoint 示例**：
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`  
   - Anthropic 兼容：`https://dashscope.aliyuncs.com/compatible-mode/v1/messages`  
   - DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`  
3. **SDK 推荐**：  
   - OpenAI 兼容 → 使用官方 `openai` Python SDK（设置 `base_url`）  
   - DashScope → 使用 `dashscope` SDK（`pip install dashscope`），支持异步、重试策略与日志追踪  

## 限制和注意事项

- 单次请求 `messages` 总 token 数上限为 32768（`qwen-max`），其他模型按规格降低；超出将返回 `400 Bad Request`  
- OpenAI 兼容接口默认禁用工具调用，需显式设置 `tool_choice="auto"` 并传入 `tools`；DashScope 接口需启用 `enable_search=true` 或 `enable_code_interpreter=true`  
- 所有接口均不支持跨会话状态共享；若需[长期记忆](../concepts/long-term-memory.md)，请自行实现外部向量库 + RAG 逻辑  
- 错误码统一遵循 RFC 7807 标准，但 `error.message` 字段内容在不同协议间存在差异（如 Anthropic 返回 `validation_error`，DashScope 返回 `InvalidParameter`），建议优先解析 `error.code`

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


