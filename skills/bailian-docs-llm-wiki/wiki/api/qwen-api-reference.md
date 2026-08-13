# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接口，支持文本生成、多轮对话、工具调用等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过 DashScope SDK 或 HTTP 请求调用，并依赖有效的 API Key 认证。

## 支持的模型与功能

当前支持的 Qwen 模型包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 和 `qwen-vl`（[多模态](../concepts/multimodal.md)），具体能力因模型而异：

- **OpenAI 兼容 Chat Completions**：适用于已有 OpenAI 生态的应用迁移，支持 `messages` 输入格式，但不原生支持工具调用或联网搜索 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)  
- **OpenAI 兼容-Responses**：自动集成联网搜索、代码解释器和网页内容提取，会话状态由服务端维护，适合快速构建智能助手 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)  
- **Anthropic 兼容-Messages**：支持 `tool_use`、`thinking` 等结构化输出，适用于需要可控推理链路的场景 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)  
- **DashScope 原生接口**：提供最全参数控制（如 `top_p`、`seed`、`enable_search`）、流式响应、[函数调用](../concepts/function-calling.md) schema 定义及[多模态](../concepts/multimodal.md)输入支持，是生产环境首选

> **注意**：`qwen-vl` 在 DashScope 接口中支持图像 URL 或 base64 输入，但在 [OpenAI 兼容接口](../concepts/openai-compatibility.md)中暂不支持[多模态](../concepts/multimodal.md)；该差异已在 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中未明确说明，建议以 DashScope 文档为准。

## 关键参数

| 参数名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `model` | string | 必填，模型 ID（如 `qwen-max`） | — |
| `messages` | array | 对话历史，每项含 `role`（`system`/`user`/`assistant`）和 `content` | — |
| `temperature` | number | 控制输出随机性，范围 0.0–2.0 | `1.0` |
| `max_tokens` | integer | 最大生成 token 数 | `1024` |
| `stream` | boolean | 是否启用流式响应 | `false` |
| `tools` | array | 工具定义列表（仅 DashScope 和 Anthropic 接口支持） | `[]` |
| `enable_search` | boolean | 启用联网搜索（仅 OpenAI 兼容-Responses 和 DashScope 支持） | `false` |

## 使用方式

1. **认证**：在请求头中携带 `Authorization: Bearer <your_api_key>`  
2. **Endpoint 示例**：
   - DashScope：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`  
   - OpenAI 兼容：`POST https://dashscope.aliyuncs.com/v1/chat/completions`（需配置 `base_url`）  
3. **SDK 调用（Python）**：
   ```python
   from dashscope import Generation
   response = Generation.call(
       model='qwen-max',
       messages=[{'role': 'user', 'content': '你好'}],
       stream=True
   )
   ```

## 限制和注意事项

- 单次请求 `messages` 总长度（含系统提示）不得超过 32768 tokens（`qwen-max`）或 8192 tokens（`qwen-turbo`）  
- 流式响应中，`delta.content` 可能为空（尤其在工具调用阶段），需检查 `delta.tool_calls` 字段  
- [OpenAI 兼容接口](../concepts/openai-compatibility.md)返回字段命名（如 `choices[0].message.content`）与标准 OpenAI API 一致，但部分字段（如 `usage.prompt_tokens`）可能为 `null`，实际计费以 DashScope 后台日志为准  
- 所有接口均不支持跨会话的[长期记忆](../concepts/memory.md)，如需持久化上下文，须自行实现 history 缓存或使用百炼工作流服务

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


