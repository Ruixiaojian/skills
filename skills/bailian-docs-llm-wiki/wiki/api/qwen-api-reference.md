# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过阿里云 AccessKey 或 STS 临时凭证鉴权。

## 支持的模型与功能

当前 Qwen 系列支持以下主流接入协议：

- **OpenAI 兼容 Chat Completions**：适用于已有 OpenAI 客户端（如 `openai==1.0+`）的快速迁移，支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等模型，但不支持原生工具调用（需依赖 [OpenAI兼容-Responses](https://help.aliyun.com/zh/model-studio/openai-compatible-responses/) 的自动工具链）。详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

- **OpenAI兼容-Responses**：在 Chat Completions 基础上增强，内置联网搜索、代码解释器、网页内容提取等工具，并自动维护对话历史（`messages` 中无需显式传入历史），适合需要开箱即用智能体能力的场景。该能力仅在该接口中提供，DashScope 和 Anthropic 接口需自行实现历史管理。参见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

- **Anthropic兼容-Messages**：支持 `claude` 风格的 `system` 消息、`tool_use`/`tool_result` 分块响应及思考过程[流式输出](../concepts/streaming-output.md)，适用于需结构化工具调用与推理链控制的场景。注意其 `max_tokens` 含义与 OpenAI 不同（指输出 token 上限，不含输入），具体差异请查阅 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

- **DashScope 原生接口**：提供最全参数控制（如 `enable_search`、`enable_code_interpreter`、`incremental_output`）、细粒度流式响应（`event: message` / `event: tool_calls`）及模型专属能力（如 `qwen-vl` 多模态支持）。是调试与高阶定制的首选。

> **注意**：原始文档中提及的 “OpenAI兼容-Responses” 接口在最新 DashScope SDK v3.2.0+ 中已统一归入 `/v1/chat/completions` 路径并启用 `response_format={"type": "auto"}` 自动触发工具，但旧版文档仍按独立路径描述。实际使用请以 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中的最新 SDK 示例为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识，如 `qwen-max`、`qwen-plus`、`qwen-turbo`；不同接口对模型名大小写敏感性不同（DashScope 区分大小写，[OpenAI 兼容接口](../concepts/openai-compatible-api.md)通常忽略） |
| `messages` | array | 是 | 对话消息列表，格式为 `[{"role": "user", "content": "..."}, ...]`；`system` 角色仅 Anthropic 和 DashScope 支持 |
| `temperature` | number | 否 | 采样温度，默认 `0.8`；范围 `0.0–2.0`，值越低越确定 |
| `top_p` | number | 否 | 核采样阈值，默认 `0.8`；与 `temperature` 互斥推荐使用其一 |
| `stream` | boolean | 否 | 是否流式响应，默认 `false`；流式下响应格式依接口协议而异 |

## 使用方式

1. **认证**：使用阿里云主账号或 RAM 子账号的 `AccessKeyId`/`AccessKeySecret`，或通过 STS 获取临时 [Token](../concepts/token.md)；
2. **Endpoint**：
   - DashScope：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/v1/chat/completions`
   - Anthropic 兼容：`https://dashscope.aliyuncs.com/v1/messages`
3. **请求示例（curl）**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/v1/chat/completions \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-max",
           "messages": [{"role": "user", "content": "你好"}],
           "stream": true
         }'
   ```

## 限制和注意事项

- 单次请求最大 `input_tokens` + `output_tokens` 总和受模型限制（如 `qwen-turbo` 为 8K，`qwen-max` 为 32K），超出将返回 `400 Bad Request`；
- [OpenAI 兼容接口](../concepts/openai-compatible-api.md)默认禁用工具调用，如需启用需显式设置 `tools` 字段并配合 `tool_choice="auto"`（仅 DashScope 和 Anthropic 接口原生支持完整工具生命周期）；
- 所有接口均不支持跨会话状态共享，`messages` 必须包含完整上下文（除 OpenAI兼容-Responses 外）；
- 流式响应中，`data:` 行末尾必须含换行符（`\n`），否则客户端可能解析失败。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


