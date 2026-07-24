# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 API 协议，严格遵循 OpenAI REST API 的路径、请求/响应格式、参数命名与语义规范（如 `/v1/chat/completions`），使开发者能复用现有 OpenAI SDK（如 `openai==1.0+`）、LangChain、LlamaIndex 等生态工具，无需修改业务代码即可接入通义千问等百炼模型。

## 在百炼平台的不同场景中如何使用

- **模型调用**：适用于文本生成（`chat/completions`）、视觉理解（`vision`）、向量嵌入（`embeddings`）、代码补全（`completions`）、[文件处理](file-processing.md)（`files`）、批量任务（`batch`）及会话管理（`conversations`）等核心能力。不同接口支持的模型有明确限制（例如 `completions` 接口仅支持 `qwen-coder-turbo`，`vision` 接口仅支持 `qwen-vl-plus` 等 VL 系列模型）。
- **应用调用**：通过 OpenAI 兼容的 `responses` 接口（`/compatible-mode/v1/responses`）调用已发布的智能体或工作流应用，支持多轮对话（直接传入完整 `messages` 数组）、图像/文件输入（需按 OpenAI 格式封装 `content`），适合快速迁移已有 Agent 应用。
- **开发工具集成**：终端工具（Hermes Agent、Claude Code）、IDE 插件（Cursor、Qoder）、Agent 框架（OpenClaw、QwenPaw）及低代码平台（Dify）均可通过配置 `base_url` 和 `api_key` 直接对接，实现“零适配”接入。
- **跨方案迁移**：[Token](token.md) Plan、Coding Plan 等计费方案均提供专属 OpenAI 兼容 endpoint（如 `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），API Key 与 Base URL 必须同地域、同方案绑定，不可混用。

## 关键参数和配置

| 参数 | 类型 | 说明 | 注意事项 |
|------|------|------|----------|
| `base_url` | string | **必须配置**，指向业务空间专属域名（如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧全局域名 `dashscope.aliyuncs.com` 已不推荐 | 地域、计费方案、Workspace ID 三者必须严格匹配，否则返回 401 |
| `model` | string | 模型标识符（如 `qwen-max`、`qwen-vl-plus`、`text-embedding-v3`），需与接口类型一致 | `completions` 接口仅接受 `qwen-coder-turbo`；`embedding` 接口不支持多模态模型 |
| `messages` | array | 对话消息列表，格式为 `[{ "role": "user", "content": "..." }]`；支持 `image_url`（vision）、`file_id`（files）等扩展字段 | OpenAI 兼容接口**不原生支持 `system` role**，需合并至首条 `user` message 或通过 `extra_body={"system": "..."}`（DashScope SDK v2.0+）传递 |
| `stream` | boolean | 是否启用流式响应 | 默认 `false`；`QVQ` 等部分视觉模型强制流式；流式响应末 chunk 可含 `usage`（需 `stream_options={"include_usage": true}`） |
| `tools` / `tool_choice` | array / object | 工具定义与调用策略 | OpenAI 兼容接口支持 `tool_calls` 字段（非 `function_call`），需解析 `response.choices[0].message.tool_calls` |

> ⚠️ 注意：  
> - 所有 OpenAI 兼容接口均需 `Authorization: Bearer <DASHSCOPE_API_KEY>` 认证；  
> - `qwen-audio`、多模态 Embedding（如 `qwen3-vl-embedding`）**不支持** OpenAI 兼容协议，必须使用 DashScope 原生接口；  
> - `/v1/responses` 路径已弃用，统一归入 `/v1/chat/completions` 的扩展模式（v2.0+ SDK）。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application call](../api/application-call.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


