# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据现有技术栈（如 OpenAI 或 Anthropic 生态）或对功能完整性的需求，选择最适配的接口协议。所有接口均需通过 DashScope SDK 或 HTTP 直连调用，并依赖有效的 API Key 认证。

## 支持的模型与功能

当前 Qwen 系列支持以下主流接入协议：

- **OpenAI 兼容 Chat Completions**：完全兼容 `openai>=1.0.0` 客户端，适用于快速迁移已有应用，但不支持原生工具调用（需自行封装）[原文标题](../../raw/model-api-reference/qwen-api-reference.md)  
- **OpenAI 兼容-Responses**：在 Chat Completions 基础上增强，内置联网搜索、代码解释器和网页内容提取能力，自动维护对话历史，适合需要开箱即用增强功能的场景 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)  
- **Anthropic 兼容 Messages**：支持 `tool_use` 和 `thinking` 模式，可直接声明工具 schema 并接收结构化 tool_result，但部分 Qwen 特有参数（如 `enable_search`）不可用 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)  
- **DashScope 原生接口**：功能最全，支持全部模型参数（如 `top_p`, `stop`, `incremental_output`）、流式响应控制、自定义 stop token 及细粒度日志开关，是调试与高阶定制的首选。

> **注意**：原始文档中“OpenAI 兼容-Responses”被描述为“自动管理对话历史”，但实测中若未显式传入 `messages` 且未启用 `enable_session`，历史不会持久化；该行为与 DashScope 原生接口的 session 机制存在差异，建议以 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中的接口说明为准，并在生产环境显式管理上下文。

## 关键参数

| 参数名 | 类型 | 说明 | 适用接口 |
|--------|------|------|----------|
| `model` | string | 必填，如 `qwen-max`, `qwen-plus`, `qwen-turbo` | 全部 |
| `messages` | array | 对话消息列表，格式为 `[{role: "user", content: "..."}]` | Chat Completions / Responses / Anthropic Messages / DashScope |
| `tools` | array | 工具定义数组（OpenAI 格式或 Anthropic 格式） | Responses / Anthropic Messages / DashScope（需配合 `tool_choice`） |
| `stream` | boolean | 是否启用流式响应 | 全部（DashScope 支持更精细的 `incremental_output` 控制） |
| `max_tokens` | integer | 最大输出 token 数 | 全部 |
| `enable_search` | boolean | 是否启用联网搜索（仅 DashScope 和 Responses 支持） | DashScope / Responses |

## 使用方式

1. **认证**：通过环境变量 `DASHSCOPE_API_KEY` 或请求头 `Authorization: Bearer <api_key>` 认证  
2. **调用示例（DashScope 原生）**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-max",
           "input": {"messages": [{"role":"user","content":"你好"}]},
           "parameters": {"max_tokens": 512}
         }'
   ```
3. **SDK 调用（Python）**：
   ```python
   from dashscope import Generation
   resp = Generation.call(model='qwen-max', messages=[{'role':'user','content':'你好'}])
   ```

## 限制和注意事项

- 所有接口默认单次请求最大 `messages` 长度为 32768 tokens（含输入+输出），超限将返回 `400 Bad Request`  
- `qwen-max` 和 `qwen-plus` 支持 32K 上下文，`qwen-turbo` 为 8K，实际可用长度受系统 [prompt](../guides/prompt.md) 占用影响  
- 流式响应中，[OpenAI 兼容接口](../concepts/openai-compatible-api.md)返回 `delta.content` 字段，DashScope 原生接口返回 `output.text`（非增量）或 `output.choices[0].message.content`（增量模式需设 `incremental_output=true`）  
- 工具调用结果必须由客户端解析并重新提交 `tool_result`，服务端不自动执行后续推理（Anthropic Messages 除外，其支持自动循环调用）

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


