# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组遵循 OpenAI REST API 规范（如 `/v1/chat/completions`、`/v1/embeddings` 等路径与请求/响应格式）的标准 HTTP 接口，使开发者能复用现有 OpenAI SDK（如 `openai==1.0+`）、工具链和代码逻辑，零改造或极小改造即可调用百炼托管的 Qwen 及第三方大模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型直调**：通过 `chat/completions` 接口调用 `qwen3.8-max`、`qwen3.7-plus` 等文本模型，或 `qwen3-vl-plus` 等多模态模型（需配合 `vision` 子路径），适用于对话、摘要、推理等通用任务；迁移成本最低，推荐新项目首选。
- **智能体与应用集成**：通过 `/responses` 接口调用已发布的**新版智能体（Agent 2.0）**，自动启用联网搜索、网页提取、代码解释器等内置工具，无需手动维护对话历史或工具调用循环；支持 `stream=true` [流式输出](streaming-output.md)和 `background=true` 异步执行。
- **多模态处理**：使用 `/vision` 子路径调用 `QVQ` 或 `qwen3-vl-plus`，支持图像理解、OCR、图文问答；注意 QVQ 模型强制要求 `stream=true`。
- **向量化与批量任务**：通过 `/embeddings` 接口生成文本向量（支持 `dimensions` 参数）；通过 `/batch` 接口提交 JSONL 文件进行低成本异步批量推理（文件模式）或同步批量 Chat 请求（Chat 模式）。
- **文件与会话管理**：使用 `/files` 接口上传文档用于后续分析（`purpose=file-extract`）或微调（`purpose=fine-tune`）；使用 `/conversations` 接口跨设备持久化对话状态，与 `/responses` 配合实现上下文自动注入。

> ⚠️ 注意：并非所有模型都支持全部 OpenAI 兼容子接口。例如：  
> - `qwen-turbo` / `qwen3.6-flash` 不支持 `tools`；  
> - `Qwen-Audio` 不支持 `chat/completions`；  
> - 多模态 Embedding 模型（如 `qwen3-vl-embedding`）不支持 OpenAI 兼容 `/embeddings`；  
> - `completions`（前缀补全）接口当前仅限 `qwen-coder-turbo`（华北2 地域）。

## 关键参数和配置

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `model` | string | 必填。模型 ID，必须与所选接口支持列表一致，且与地域、计费方案匹配。 | `"qwen3.8-max"`, `"qwen3-vl-plus"` |
| `base_url` | string | 必填。服务端点，**强烈推荐使用业务空间专属域名**（含 WorkspaceId），而非旧版 `dashscope.aliyuncs.com`。 | `"https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"` |
| `api_key` | string | 必填。必须使用与 `base_url` 所属地域和计费方案（Token Plan / Coding Plan / 按量付费）严格配套的 API Key。各地域、各方案 Key 相互隔离。 | `"sk-xxxxxxxxxxxxx"`（从对应控制台获取） |
| `stream` | boolean | 可选。启用流式响应（默认 `false`）。部分接口（如 Vision 的 QVQ）强制为 `true`。 | `true` |
| `stream_options` | object | 可选。当 `stream=true` 时，设 `{"include_usage": true}` 可在流末尾返回 token 统计。 | `{"include_usage": true}` |
| `tools` + `tool_choice` | array + string/object | 可选。启用工具调用（如 `web_search`）。需显式传入 `tools=[{"type": "web_search"}]`，否则不生效（与 DashScope 原生接口行为不同）。 | `{"type": "function", "function": {"name": "web_search"}}` |
| `response_format` | object | 可选。结构化输出控制，如 `{"type": "json_object"}` 要求模型返回合法 JSON。 | `{"type": "json_object"}` |
| `max_tokens` | integer | 可选。最大输出 token 数（语义与 OpenAI 一致，非严格硬上限）。部分接口也接受 `max_output_tokens`（DashScope 原生风格），但 OpenAI 兼容接口统一用 `max_tokens`。 | `1024` |

## 面向开发者，简洁实用

- ✅ **快速上手**：安装官方 OpenAI SDK（`pip install -U openai`），仅需替换 `base_url` 和 `api_key`，其余代码（如 `client.chat.completions.create(...)`）完全复用。
- ✅ **环境变量友好**：设置 `DASHSCOPE_API_KEY` 即可自动认证，无需硬编码密钥。
- ✅ **生产推荐配置**：
  - 使用业务空间专属 `base_url`（含 `{WorkspaceId}`），性能更稳、延迟更低；
  - 优先选用无日期后缀的稳定模型 ID（如 `qwen3.8-max`，而非 `qwen3.7-plus-2025-07-28`），避免限流突变；
  - 流式场景务必检查 `stream_options.include_usage` 是否开启，便于监控 token 消耗。
- ❌ **避坑提示**：
  - 切勿混用地域或计费方案的 `api_key` 与 `base_url`，否则返回 401；
  - `qwen-turbo` 等轻量模型忽略 `tools` 参数，调试时请换用 `qwen3.7-plus`；
  - Dify 等工具**不支持 Token Plan/Coding Plan**，仅允许按量付费 Key；
  - `/responses` 和 `/conversations` 的旧路径（含 `/api/v2/apps/protocols/...`）已标记为“即将停止维护”，请立即迁移到 `/compatible-mode/v1/...`。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [get started with models](../guides/get-started-with-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application call](../api/application-call.md)


