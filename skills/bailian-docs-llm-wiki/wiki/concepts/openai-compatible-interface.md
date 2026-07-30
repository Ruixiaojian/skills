# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 REST API 协议层，遵循 OpenAI 官方 Chat Completions 等核心接口规范（如 `/v1/chat/completions`），支持使用标准 OpenAI SDK（如 `openai==1.0+`）零代码迁移调用千问（Qwen）及第三方模型。该接口在保持语义一致性的前提下，对部分字段、参数范围和功能边界进行了平台级适配。

## 在百炼平台的不同场景中如何使用

- **快速迁移现有项目**：已有基于 OpenAI SDK 的应用（如 LangChain、LlamaIndex、FastAPI 服务）只需替换 `base_url` 和 `api_key`，无需修改业务逻辑即可接入 Qwen 系列模型（如 `qwen3.7-plus`、`qwen-max`）或 DeepSeek、Kimi 等第三方模型。
- **[多模态](multi-modal.md)与专用模型调用**：支持 `qwen-vl-plus`（视觉理解）、`text-embedding-v4`（向量嵌入）、`farui-plus`（法律）、`qwen-mt-plus`（机器翻译）等垂直模型，但需注意：`Qwen-Audio`、`qwen-deep-research` 等少数模型明确不支持该协议。
- **会话与批量任务管理**：
  - 通过 `Conversations API` + `Responses API` 实现自动上下文维护的多轮对话；
  - 使用 `completions` 接口专用于代码补全（仅限 `qwen-coder-turbo`）；
  - 支持两种 Batch 模式：异步文件式批处理（高吞吐）与同步 Batch Chat（保序、可控超时）。
- **开发工具集成**：可直接配置于 Cursor、Cherry Studio、Qoder、Dify HTTP 节点等主流 AI 工具，配合 `enable_thinking` 等扩展参数启用高级能力（如 qwen3.8-max-preview 的思考模式）。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `base_url` | string | 是 | 必须使用兼容域名：<br>• 生产推荐：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`<br>• 兼容旧版：`https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）或 `https://dashscope-us.aliyuncs.com/compatible-mode/v1`（美国）<br>• 试用：`https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（RPM 限 1000） |
| `model` | string | 是 | 模型标识符，大小写敏感，支持版本后缀（如 `qwen3.7-plus`、`qwen-max-20240718`）；不同子接口支持范围不同（`responses` 仅限 `qwen3-*` 系列，`completions` 仅限 `qwen-coder-turbo`） |
| `messages` | array | 是 | 标准 OpenAI 格式：`[{ "role": "user", "content": "..." }]`；`responses` 接口要求首条消息为 `user`，且 `system` 提示需作为顶层参数传入（非 `messages` 内） |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 启用流式响应（返回 `chat.completion.chunk`） |
| `stream_options` | object | 否 | 可选 `{ "include_usage": true }`，在末尾 chunk 中返回 token 统计 |
| `temperature` | number | 否 | 范围 `0.0–1.0`（OpenAI 兼容接口严格限制，DashScope 原生支持 `0.0–2.0`） |
| `tools` / `tool_choice` | array / string | 否 | **不支持自定义工具调用**；`responses` 接口内置联网搜索、代码解释器等预置工具，不可覆盖 |
| `response_format` | object | 否 | **不支持 JSON Schema 强约束输出**；如需结构化结果，请改用 DashScope 原生接口并设置 `output_format: "json"` |
| `extra_body` | object | 否 | 扩展参数载体，用于传递模型特有参数：<br>• `qwen-mt-plus`: `{"translation_options": {"source_lang": "zh", "target_lang": "en"}}`<br>• `qwen3.8-max-preview`: `{"enable_thinking": true}`（强制启用）<br>• `gui-plus`: `{"vl_high_resolution_images": true}` |

> ⚠️ 注意事项：
> - 不支持 `response_format`、`logprobs`、`top_logprobs` 等 OpenAI 高级字段；
> - 流式响应中 `delta.tool_calls` 字段可能缺失部分参数，建议非流式模式验证工具逻辑；
> - `system` 提示词在 `responses` 接口中需单独传入顶层，而非嵌入 `messages`；
> - 所有请求必须通过 `Authorization: Bearer <DASHSCOPE_API_KEY>` 认证。

## 面向开发者：简洁实用提示

- ✅ **起步最快**：`pip install -U openai` + 设置 `OPENAI_API_KEY` 环境变量 + 指定 `base_url`，3 行代码即可调通；
- ✅ **生产首选**：使用业务空间专属域名（含 `WorkspaceId`），获得更高 QPS、更低延迟与流量隔离；
- ✅ **调试技巧**：开启 `stream=False` + `stream_options={"include_usage": true}`，一次请求获取完整响应与 token 消耗；
- ❌ **避免踩坑**：
> - 不要尝试在 `messages` 中传 `system` 角色（`responses` 接口将忽略）；
> - 不要传 `response_format`（返回 `400 Unsupported parameter`）；
> - 不要跨地域混用 `WorkspaceId` 和 API Key（返回 `401 Unauthorized`）；
> - `qwen-deep-research`、`Qwen-Audio` 等模型不支持此协议，需切换至 DashScope 原生接口。

如需更细粒度控制（如自定义 stop words、增量输出、完整日志回溯），请优先选用 DashScope 原生接口。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [get started with models](../guides/get-started-with-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more models](../api/more-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


