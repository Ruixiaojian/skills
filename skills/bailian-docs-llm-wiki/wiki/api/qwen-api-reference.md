# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适的接口协议。所有接口均需通过 DashScope SDK 或标准 HTTP 请求调用，并依赖有效的 API Key 进行鉴权。

## 支持的模型与功能

当前 Qwen 系列支持以下主流接入协议：

- **OpenAI 兼容 Chat Completions**：适用于已使用 OpenAI 客户端（如 `openai==1.0+`）的项目，可零代码修改迁移 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)；  
- **OpenAI 兼容 Responses**：在基础聊天能力上集成联网搜索、代码解释器、网页内容提取等内置工具，自动维护对话上下文，适合快速构建智能助手 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)；  
- **Anthropic 兼容 Messages**：支持 `tool_use`、`thinking` 等结构化输出能力，适用于需要显式推理链或可控工具调用的场景 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)；  
- **DashScope 原生接口**：提供最全参数控制（如 `enable_search`、`max_output_tokens`、`top_p`）、细粒度流式响应及模型专属能力（如 Qwen2-VL [多模态](../concepts/multi-modal.md)支持），是生产环境推荐方案。

> **注意**：OpenAI 兼容 Responses 的 `tools` 字段行为与 Anthropic Messages 的 `tool_choice` 语义不一致——前者为自动触发，后者需显式声明；实际调用前请以 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中最新示例为准。

## 关键参数

| 参数名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `model` | string | 模型标识，如 `qwen-max`、`qwen-plus`、`qwen-turbo` | 必填 |
| `messages` | array | 对话历史，格式为 `[{ "role": "user", "content": "..." }]` | — |
| `temperature` | float | 控制输出随机性（0.0–2.0） | `1.0` |
| `top_p` | float | 核采样阈值（0.0–1.0） | `0.8` |
| `max_output_tokens` | int | 最大生成 token 数 | `2048` |
| `stream` | bool | 是否启用流式响应 | `false` |

部分参数仅 DashScope 接口支持（如 `enable_search`、`seed`），OpenAI/Anthropic 兼容接口会忽略或静默转换。

## 使用方式

1. **安装 SDK**：`pip install dashscope`（推荐）或 `pip install openai`（仅限 OpenAI 兼容模式）；  
2. **设置认证**：通过环境变量 `DASHSCOPE_API_KEY` 或 `OPENAI_API_KEY`（兼容模式下）配置密钥；  
3. **发起请求**：  
   - DashScope 示例：`dashscope.Generation.call(model='qwen-max', messages=[...])`；  
   - OpenAI 兼容示例：`client.chat.completions.create(model='qwen-max', messages=[...])`；  
   - Anthropic 兼容示例：`client.messages.create(model='qwen-max', messages=[...], tools=[...])`。

## 限制和注意事项

- 单次请求 `messages` 总长度（含 system [prompt](../guides/prompt.md)）不得超过 32768 tokens；  
- 流式响应中，[OpenAI 兼容接口](../concepts/openai-compatible-api.md)返回 `delta.content`，DashScope 返回 `output.text`，字段命名不一致；  
- `qwen-vl` 等[多模态](../concepts/multi-modal.md)模型**仅支持 DashScope 原生接口**，OpenAI/Anthropic 兼容层暂不开放；  
- 所有接口均遵循百炼平台配额与计费规则，详见 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中的“计费说明”章节。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


