# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接口，支持文本生成、多轮对话、工具调用等核心能力。开发者可根据技术栈兼容性、功能需求和部署场景选择 OpenAI 兼容、Anthropic 兼容或 DashScope 原生接口。所有接口均需通过阿里云百炼平台认证访问。

## 支持的模型与功能

当前 Qwen 系列支持以下主流调用方式（详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)）：

- **OpenAI 兼容 Chat Completions**：适配 `openai>=1.0.0` 客户端，支持 `messages` + `model` + `stream` 等标准参数，适用于快速迁移现有应用；  
- **OpenAI 兼容 Responses**：在 Chat Completions 基础上增强，**自动管理对话历史**，并内置联网搜索、代码解释器、网页内容提取等工具链（参见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)）；  
- **Anthropic 兼容 Messages**：支持 `system` 消息、`tool_use`、`thinking` 等结构化能力，适用于需要显式推理路径与工具协同的场景；  
- **DashScope 原生接口**：提供最细粒度控制，包括 `top_k`、`repetition_penalty`、`enable_search` 等专属参数，是功能最全的接入方式（详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)）。

> **注意**：OpenAI 兼容 Responses 接口的 `tools` 字段行为与标准 OpenAI v1 API 不完全一致——其工具调用由服务端自动触发并注入结果，不返回原始 tool_calls，开发者无需手动解析 `tool_calls` 或调用 `tool` 函数。该差异已在 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中明确说明，但易被误读为标准 OpenAI 行为。

## 关键参数

| 参数名 | 类型 | 说明 | DashScope 支持 | OpenAI 兼容 | Anthropic 兼容 |
|--------|------|------|----------------|-------------|----------------|
| `model` | string | 模型标识，如 `qwen-max`、`qwen-plus`、`qwen-turbo` | ✅ | ✅（需映射为对应别名） | ✅（需映射为 `claude-3-*` 风格别名） |
| `messages` | array | 对话消息列表，含 `role` 和 `content` | ✅（部分字段需转义） | ✅ | ✅（`system` 单独传入） |
| `stream` | boolean | 是否启用流式响应 | ✅ | ✅ | ✅ |
| `temperature` | number | 控制输出随机性（0.0–2.0） | ✅ | ✅ | ✅ |
| `max_tokens` | integer | 最大生成 token 数 | ✅ | ✅ | ✅（`max_tokens`） |
| `tools` | array | 工具定义列表 | ✅（`enable_search=true` 等隐式工具需额外开关） | ✅（仅 Responses 接口自动生效） | ✅（`tool_use` 显式声明） |

## 使用方式

1. **认证**：使用阿里云 AccessKey（推荐 RAM 子账号 + 最小权限策略）或 STS 临时凭证，通过 `Authorization: Bearer <api_key>` 或 `X-DashScope-Signature` 头传递；  
2. **Endpoint**：各接口 endpoint 不同，请严格按文档配置：
   - DashScope：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`  
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/v1/chat/completions`（Chat Completions）或 `/v1/responses`（Responses）  
   - Anthropic 兼容：`https://dashscope.aliyuncs.com/v1/messages`  
3. **示例请求（curl）**：  
   ```bash
   curl -X POST 'https://dashscope.aliyuncs.com/v1/chat/completions' \
     -H 'Authorization: Bearer YOUR_API_KEY' \
     -H 'Content-Type: application/json' \
     -d '{
           "model": "qwen-turbo",
           "messages": [{"role": "user", "content": "你好"}],
           "stream": false
         }'
   ```

## 限制和注意事项

- 所有接口默认单次请求最大 `messages` 长度为 32768 tokens（具体依模型而定），超长输入将被截断或报错 `400 Bad Request`；  
- DashScope 接口支持 `input` 字段直接传入 [prompt](../guides/prompt.md) 字符串（非 messages），但 OpenAI/Anthropic 兼容接口**仅接受 `messages` 格式**；  
- `qwen-max` 等高阶模型需单独开通权限，未授权调用将返回 `403 Forbidden`；  
- 流式响应中，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)返回 `data: {...}` SSE 格式，DashScope 返回 JSON Lines（每行一个 JSON 对象），二者解析逻辑不同；  
- 调用频率受百炼平台配额限制，可通过控制台查看实时用量与剩余额度。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


