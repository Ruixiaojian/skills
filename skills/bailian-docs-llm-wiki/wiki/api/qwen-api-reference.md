# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过阿里云 AccessKey 或 STS 临时凭证鉴权。

## 支持的模型与功能

当前 Qwen 系列支持以下主流接入协议：

- **OpenAI 兼容 Chat Completions**：适用于已使用 OpenAI SDK 的项目，可零代码修改迁移；支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等模型，但不支持流式工具调用响应格式（详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)）。
- **OpenAI 兼容-Responses**：内置联网搜索、代码解释器、网页内容提取三类工具，自动维护对话历史与工具执行上下文；该模式下 `messages` 中无需显式传入 `tool_calls`，由服务端自动编排（参见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)）。
- **Anthropic 兼容 Messages**：支持 `system` 消息、`max_tokens` 精确控制、以及结构化 `tool_use` 声明；但暂不支持 Qwen 自研的 `retrieval` 工具类型（> **注意**：官方文档中称支持“工具调用”，但实际仅限 Anthropic 标准工具 schema，与 DashScope 原生工具体系不互通）。
- **DashScope 原生接口**：功能最完整，支持 `input_files` 文件上传、`incremental_output` 流式增量返回、`enable_search` 显式开关联网搜索等高级参数；是唯一支持 `qwen-vl` [多模态](../concepts/multi-modal.md)模型的入口（见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-max`、`qwen-plus`、`qwen-turbo`；DashScope 接口还支持 `qwen-vl`、`qwen-audio` |
| `messages` | array | 是 | 对话消息列表，格式为 `[{ "role": "user", "content": "..." }]`；Anthropic 接口要求首条消息 role 为 `user` 或 `assistant` |
| `tools` | array | 否 | 工具定义列表（OpenAI/Anthropic/DashScope 均支持，但 schema 不同） |
| `tool_choice` | string/object | 否 | 控制工具调用策略；DashScope 支持 `"auto"`、`"none"`、`{"type": "function", "function": {"name": "xxx"}}` |
| `stream` | boolean | 否 | 是否启用流式响应；仅 DashScope 和 OpenAI Chat Completions 支持 `true` |

> **注意**：`temperature` 在 DashScope 接口中范围为 `[0.01, 2.0]`，而 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)默认接受 `[0, 2]`，超出 `0.01` 下限将被静默截断——此行为差异未在 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中明确说明。

## 使用方式

1. **认证**：使用阿里云 `AccessKeyId` + `AccessKeySecret` 或 STS [Token](../concepts/token.md)，通过 `Authorization: Bearer <token>` 或 `X-DashScope-Authentication-Token` 传递；
2. **Endpoint**：
   - DashScope：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/v1/chat/completions`
   - Anthropic 兼容：`https://dashscope.aliyuncs.com/v1/messages`
3. **示例请求（DashScope）**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-max",
           "input": {"messages": [{"role":"user","content":"你好"}]},
           "parameters": {"temperature": 0.8}
         }'
   ```

## 限制和注意事项

- 单次请求 `messages` 总 token 数上限为 32768（Qwen-Max），其他模型请查阅对应规格文档；
- [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)不支持 `response_format`（如 JSON Schema 强约束），该能力仅 DashScope 原生接口提供；
- 所有接口均**不支持跨账号共享模型实例**，`model` 参数必须属于调用方所属的百炼工作空间；
- 流式响应中，DashScope 返回 `output.text` 字段为增量片段，而 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)返回 `choices[0].delta.content`，客户端需适配解析逻辑。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


