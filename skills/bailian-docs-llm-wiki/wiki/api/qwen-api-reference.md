# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过百炼平台鉴权访问，并遵循统一的计费与配额规则。

## 支持的模型与功能

当前 Qwen 系列支持以下主流接入协议：

- **OpenAI 兼容 Chat Completions**：完全兼容 OpenAI `chat/completions` 接口规范，适用于已有 OpenAI 客户端（如 `openai==1.0+`）的快速迁移。支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等全部公开模型，详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **OpenAI 兼容 Responses**：在标准 Chat Completions 基础上增强内置工具链（联网搜索、代码解释器、网页提取），自动维护对话上下文，适合无需手动管理 history 的轻量级应用。该模式的具体行为请参考 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **Anthropic 兼容 Messages**：适配 Anthropic `messages` 接口，支持 `tool_use`、`thinking` 等结构化输出，适用于需要显式控制工具调用流程的场景。注意其 `max_tokens` 含义与 OpenAI 版本不同（指输出 token 上限，不含输入），详情见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **DashScope 原生接口**：百炼专属协议，提供最细粒度参数控制（如 `enable_search`、`function_call`、`seed`）、完整流式响应字段及调试信息（`usage` 中含 input/output token 分项统计），推荐用于生产环境高可靠性要求场景。

> **注意**：`qwen-vl` 和 `qwen-audio` 等[多模态](../concepts/multi-modal.md)模型**不支持** OpenAI 或 Anthropic 兼容接口，仅可通过 DashScope 原生接口调用；相关限制未在 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中明确说明，需以 DashScope 文档为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-max`、`qwen-plus`；不同协议下可选值一致，但部分模型（如 `qwen2.5-72b`）仅 DashScope 支持 |
| `messages` | array | 是（除部分 streaming 场景外） | 对话历史列表，格式为 `[{"role": "user", "content": "..."}, ...]`；OpenAI/Anthropic 协议中 `content` 可为字符串或对象数组（含 `text`/`image_url`），DashScope 要求严格 JSON 结构 |
| `stream` | boolean | 否 | 是否启用流式响应；所有协议均支持，但 DashScope 返回 `event: message` + `data:` 格式，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)返回 `data: {...}` |
| `temperature` | number | 否 | 控制输出随机性（0.0–2.0），默认 0.8；DashScope 支持更宽范围（0.0–2.0），而 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)实际生效范围为 0.0–1.0（超出部分被截断） |
| `tools` / `functions` | array | 否 | 工具定义列表；[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)使用 `functions` 字段，Anthropic 使用 `tools`，DashScope 统一为 `tools` 且支持更多字段（如 `description` 必填） |

## 使用方式

1. **认证**：所有请求需携带 `Authorization: Bearer <api_key>`，API Key 在百炼控制台「API 密钥管理」中创建；
2. **Endpoint**：
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/v1/chat/completions`
   - Anthropic 兼容：`https://dashscope.aliyuncs.com/v1/messages`
   - DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
3. **示例（curl）**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/v1/chat/completions \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-max",
           "messages": [{"role": "user", "content": "你好"}],
           "stream": false
         }'
   ```

## 限制和注意事项

- 单次请求最大 `messages` 长度为 100 条，总 token 数上限依模型而定（`qwen-turbo`: 8K, `qwen-plus`: 32K, `qwen-max`: 64K）；
- 流式响应中，OpenAI 兼容接口的 `delta.content` 可能为空字符串（表示工具调用开始），需忽略空 content 判断；
- 所有协议均**不支持** `n > 1`（即并行生成多个候选结果），该参数被忽略；
- 错误码统一使用 HTTP 状态码 + JSON body 中 `code` 字段（如 `"InvalidParameter"`），具体映射关系请查阅 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 的错误码章节；
- `system` 角色消息仅 DashScope 原生接口原生支持；OpenAI/Anthropic 兼容接口中若传入 `system`，将被自动合并至首条 `user` 消息前（可能影响 [prompt](../guides/prompt.md) 效果）。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


