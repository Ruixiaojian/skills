# qwen api reference

Qwen 系列大模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过阿里云 AccessKey 进行身份认证，并遵循统一的配额与计费规则。

## 支持的模型/功能

当前 Qwen 系列支持以下主流 API 协议接入：
- **OpenAI 兼容 Chat Completions**：适用于已有 OpenAI 客户端（如 `openai>=1.0`）的项目，可零代码迁移 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)；
- **OpenAI 兼容 Responses**：在标准 Chat Completions 基础上增强，内置联网搜索、代码解释器与网页内容提取能力，并自动维护对话上下文，适合需要轻量级智能体能力的场景 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)；
- **Anthropic 兼容 Messages**：支持 `tool_use`、`thinking` 等结构化输出，适用于需显式控制推理链与工具调用流程的应用 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)；
- **DashScope 原生接口**：提供最全参数控制（如 `top_k`、`repetition_penalty`、`enable_search`）、细粒度流式响应及调试字段（`usage`、`finish_reason`），推荐用于生产环境高精度调优。

> **注意**：`OpenAI 兼容 Responses` 接口虽宣称“自动管理对话历史”，但实际仍要求客户端传入完整 `messages` 数组（非仅最新一轮），其“自动”仅体现在内部工具调用状态跟踪；该行为与 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中描述存在歧义，建议以 DashScope 文档为准。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `model` | string | 模型标识符，如 `qwen-max`、`qwen-plus`、`qwen-turbo`；不同协议下命名略有差异（如 Anthropic 接口使用 `claude-3-haiku-20240307` 风格别名） | 是 |
| `messages` | array | 对话消息列表，格式为 `[{ "role": "user/system/assistant", "content": "..." }]`；`system` 角色仅 DashScope 和 Anthropic 接口原生支持 | 是 |
| `temperature` | number | 控制输出随机性（0.0–2.0），默认 `0.8`；[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)默认值为 `1.0`，存在不一致 | 否 |
| `stream` | boolean | 是否启用流式响应；DashScope 和 OpenAI 接口均支持，但 Anthropic 接口需显式设置 `stream: true` 并处理 `event: message_start` 等 SSE 事件 | 否 |

## 使用方式

1. **认证**：所有请求需在 HTTP Header 中携带 `Authorization: Bearer <api_key>`（DashScope 接口）或 `Authorization: Bearer <dashscope_api_key>`（OpenAI/Anthropic 兼容接口）；
2. **Endpoint**：
   - DashScope：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/v1/chat/completions`
   - Anthropic 兼容：`https://dashscope.aliyuncs.com/v1/messages`
3. **示例（curl）**：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/v1/chat/completions" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-plus",
           "messages": [{"role": "user", "content": "你好"}]
         }'
   ```

## 限制和注意事项

- 单次请求 `messages` 总 token 数上限为 32,768（Qwen2/Qwen3 系列），超出将返回 `400 Bad Request`；
- `qwen-turbo` 不支持 `tool_use` 和 `system` 角色，调用时需显式降级至 `qwen-plus` 或更高版本；
- [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)暂不支持 `response_format`（如 JSON Schema 强约束），该能力仅 DashScope 原生接口提供；
- 所有接口均按输入 + 输出 token 总数计费，具体单价见 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中的定价说明。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


