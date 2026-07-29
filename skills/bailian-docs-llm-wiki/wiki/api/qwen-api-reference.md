# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接口，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据技术栈兼容性、功能需求和部署场景选择合适的接入方式。所有接口均需通过百炼平台鉴权调用，并遵循统一的计费与配额规则。

## 支持的模型与功能

当前 Qwen 系列支持以下主流接口协议：

- **OpenAI 兼容 Chat Completions**：适用于已有 OpenAI 客户端的应用迁移，支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等模型，但不支持原生工具调用（需依赖客户端侧实现）。详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **OpenAI 兼容-Responses**：内置联网搜索、代码解释器与网页内容提取能力，自动维护对话上下文，适合快速构建智能助手类应用。该接口在 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中有完整说明。
- **Anthropic 兼容-Messages**：支持 `tool_use`、`thinking` 等结构化输出，适用于需要可控推理链路的场景；注意其 `max_tokens` 语义与 OpenAI 版本不同（指输出 token 上限，不含思考过程 token）。
- **DashScope 原生接口**：功能最全，支持流式响应、自定义 stop 字符串、logprobs、seed 固定等高级参数，是调试与生产环境的首选。具体能力请参阅 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

> **注意**：`qwen-vl`（多模态）和 `qwen-audio` 模型**不支持** [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，仅可通过 DashScope 原生接口调用，且输入格式（如 base64 图片/音频）与文本模型不同。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识，如 `qwen-max`、`qwen-plus`；不同接口协议下可选值略有差异，请以实际文档为准 |
| `messages` | array | 是（Chat Completions / Anthropic Messages） | 对话历史，格式为 `[{"role": "user", "content": "..."}]`；DashScope 接口还支持 `system` 角色 |
| `temperature` | number | 否 | 默认 `0.8`，范围 `0.0–2.0`；值越低输出越确定 |
| `top_p` | number | 否 | 默认 `0.8`，范围 `0.0–1.0`；控制核采样范围 |
| `max_tokens` | integer | 否 | 输出最大 token 数；DashScope 接口默认 `1024`，[OpenAI 兼容接口](../concepts/openai-compatible-api.md)默认 `2048` |

## 使用方式

1. **认证**：使用百炼平台颁发的 `API Key`，通过 `Authorization: Bearer <api_key>` 请求头传递；
2. **Endpoint**：
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/v1/chat/completions`
   - Anthropic 兼容：`https://dashscope.aliyuncs.com/v1/messages`
   - DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
3. **示例请求（curl）**：
   ```bash
   curl -X POST \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-plus",
           "messages": [{"role": "user", "content": "你好"}]
         }' \
     https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
   ```

## 限制和注意事项

- 单次请求 `messages` 总长度（含 system [prompt](../guides/prompt.md)）不得超过 32768 tokens（Qwen2/Qwen3 模型），超长将被截断或报错；
- [OpenAI 兼容接口](../concepts/openai-compatible-api.md)**不返回** `usage` 字段中的 `prompt_tokens` 和 `completion_tokens` 细粒度统计，仅 DashScope 接口提供完整 token 计数；
- 所有接口均**不支持**跨模型会话状态共享（如 `qwen-max` 的 history 不能用于 `qwen-turbo` 调用）；
- 流式响应中，OpenAI 兼容接口返回 `delta` 字段，DashScope 返回 `output.text` 字段，解析逻辑需区分处理。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


