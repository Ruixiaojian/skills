# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接入方式，支持文本生成、[工具调用](../concepts/tool-use.md)、多轮对话等核心能力。开发者可根据现有技术栈（如 OpenAI 或 Anthropic 客户端）或功能需求（如联网搜索、历史管理）选择合适接口。所有接口均需通过 DashScope SDK 或标准 HTTP 请求调用，并依赖有效的 API Key 认证。

## 支持的模型/功能

当前支持的 Qwen 模型包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 及 `qwen-vl`（[多模态](../concepts/multi-modal.md)），具体能力因模型而异：  
- `qwen-max` 和 `qwen-plus` 支持长上下文、复杂推理与[工具调用](../concepts/tool-use.md)；  
- `qwen-turbo` 适用于低延迟、高吞吐场景；  
- `qwen-vl` 支持图像理解与图文生成（需使用 [DashScope](https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope) 接口）。  
详细模型能力对比见 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)。

## 关键参数

通用参数（各接口共用）：
- `model`: 必填，指定模型 ID（如 `"qwen-plus"`）；
- `messages`: 对话历史数组，格式为 `[{ "role": "user", "content": "..." }]`；
- `temperature`: 控制输出随机性（0.0–2.0，默认 1.0）；
- `max_tokens`: 限制响应最大 token 数（非必填，但建议设置防超限）；
- `stream`: 布尔值，启用流式响应（仅部分接口支持，详见 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)）。

> **注意**：`top_p` 在 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)中默认为 `1.0`，但在 DashScope 原生接口中默认为 `0.8`，行为不一致，建议显式指定以避免歧义。

## 使用方式

推荐优先使用 DashScope SDK（Python/Java/Node.js）简化认证与请求封装：  
```python
from dashscope import Generation
Generation.call(model='qwen-plus', messages=[{'role': 'user', 'content': '你好'}])
```

若直接调用 HTTP 接口：
- [OpenAI 兼容接口](../concepts/openai-compatible-api.md)：`POST https://dashscope.aliyuncs.com/v1/chat/completions`（需 `Authorization: Bearer <api_key>`）；  
- Anthropic 兼容接口：`POST https://dashscope.aliyuncs.com/v1/messages`；  
- DashScope 原生接口：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`。  
完整请求示例与鉴权说明参见 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)。

## 限制和注意事项

- 单次请求 `messages` 总长度（含 system [prompt](../guides/prompt.md)）不得超过模型 context window（如 `qwen-plus` 为 32768 tokens）；  
- 流式响应（`stream=True`）在 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)中返回 `text/event-stream`，而 DashScope 原生接口返回 JSON Lines；  
- [工具调用](../concepts/tool-use.md)（function calling）仅在 `qwen-max`/`qwen-plus` + DashScope 或 Anthropic 兼容接口中可用，OpenAI 兼容接口暂不支持结构化工具定义；  
- 所有接口均受百炼配额与速率限制约束，超出将返回 `429 Too Many Requests`。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


