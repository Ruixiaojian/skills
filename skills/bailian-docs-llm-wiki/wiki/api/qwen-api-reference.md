# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接入方式，支持文本生成、多轮对话、工具调用等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过阿里云 AccessKey 进行身份认证，并遵循统一的配额与计费规则。

## 支持的模型/功能

当前支持的 Qwen 模型包括 `qwen-max`（旗舰版）、`qwen-plus`（均衡版）、`qwen-turbo`（轻量版）及 `qwen2.5` 系列（如 `qwen2.5-7b-instruct`）。各接口支持的功能略有差异：

- **OpenAI 兼容 Chat Completions**：支持标准 `chat/completions` 请求，适用于已有 OpenAI 生态的应用迁移；[原文标题](../../raw/model-api-reference/qwen-api-reference.md) 明确指出其“迁移成本最低”。
- **OpenAI 兼容-Responses**：内置联网搜索、代码解释器和网页内容提取工具，自动管理对话历史；该能力在 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中被强调为“无需手动维护”。
- **Anthropic 兼容-Messages**：支持 `tool_use` 和 `thinking` 模式，适用于需要结构化工具调用与推理链输出的场景；详见 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)。
- **DashScope 原生接口**：提供最完整的参数控制（如 `enable_search`、`max_output_tokens`、`top_p` 等），是调试与高阶定制的首选。

> **注意**：`qwen-max` 在 DashScope 接口中默认启用联网搜索，但在 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)中需显式传入 `tools=[{"type": "web_search"}]` 才生效——此行为差异未在 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中说明，实际以最新 DashScope SDK 文档为准。

## 关键参数

通用关键参数（跨接口适用）：
- `model`: 必填，模型标识符（如 `"qwen-plus"`）
- `messages`: 对话历史数组，格式为 `[{ "role": "user", "content": "..." }]`
- `temperature`: 控制随机性（0.0–2.0，默认 1.0）
- `max_tokens`: 最大输出 token 数（非严格上限，部分接口以 `max_output_tokens` 命名）

接口特有参数：
- [OpenAI 兼容接口](../concepts/openai-compatible-api.md)：支持 `stream`、`response_format`（`{ "type": "json_object" }`）、`tools`（需配合 `tool_choice`）
- DashScope 接口：额外支持 `incremental_output`（流式分块返回）、`seed`（确定性采样）、`repetition_penalty`

## 使用方式

1. **认证**：使用阿里云 `AccessKeyId` + `AccessKeySecret` 签名，或通过环境变量 `DASHSCOPE_API_KEY`（DashScope） / `OPENAI_API_KEY`（OpenAI 兼容）配置；
2. **Endpoint**：
   - DashScope：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/v1/chat/completions`
3. **示例请求（curl）**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/v1/chat/completions \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-plus",
           "messages": [{"role": "user", "content": "你好"}]
         }'
   ```

## 限制和注意事项

- 单次请求 `messages` 总长度上限为 32,768 tokens（DashScope 接口），[OpenAI 兼容接口](../concepts/openai-compatible-api.md)为 24,576 tokens；
- 流式响应（`stream=true`）下，OpenAI 兼容接口返回 `delta` 字段，DashScope 返回 `output.text` 分块，二者语义不完全对齐；
- `qwen-turbo` 不支持工具调用（`tools` 参数将被忽略），该限制未在 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中明确标注，需以控制台模型详情页为准；
- 跨区域调用（如华东1调用华北2模型）可能触发额外延迟与费用，建议就近部署。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


