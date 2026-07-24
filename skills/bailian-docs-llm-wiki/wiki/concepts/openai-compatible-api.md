# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 API 协议，严格遵循 OpenAI REST API 的路径、请求/响应结构、字段命名与语义规范（如 `/chat/completions`、`messages` 数组、`choices[0].message.content`），使开发者能复用现有 OpenAI SDK（Python/Node.js 等）和框架（LangChain、LlamaIndex）零代码迁移调用百炼托管的各类模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移已有应用**：无需修改业务逻辑，仅需将 `openai.base_url` 指向百炼地域专属 endpoint（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`），并替换 `api_key` 为百炼 API Key，即可调用 `qwen-max`、`qwen-plus` 等全部公开文本模型。
- **[多模态](multi-modal.md)能力扩展**：通过同一兼容协议支持视觉理解（`qwen-vl-plus`）、文本补全（`qwen-coder-turbo`）、向量嵌入（`text-embedding-v4`）、长文档问答（`qwen-long`）及批量推理（Batch Chat / JSONL 文件驱动），统一客户端接入体验。
- **智能体与工作流集成**：使用 `Responses API`（路径 `/compatible-mode/v1/responses`）调用已发布的智能体或工作流应用，自动集成联网搜索、代码解释器等工具链，并维护完整对话状态，无需手动拼装消息历史。
- **跨地域与计费方案适配**：不同套餐（[Token](token.md) Plan 个人版、Coding Plan、按量计费）和地域（北京、新加坡、东京、法兰克福）均提供独立的 `base_url`，Key 与 URL 必须严格匹配，确保权限隔离与服务路由正确。
- **开发工具无缝接入**：支持 Postman、cURL、Cherry Studio、Qwen Code、Dify 等主流客户端，只需配置 `base_url` 和 `api_key`，即可启用[流式输出](streaming-output.md)、思考模式（`enable_thinking`）、自定义参数（`biz_params`）等高级能力。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `base_url` | string | 是 | 地域专属 endpoint，必须以 `/compatible-mode/v1` 结尾；北京用 `https://dashscope.aliyuncs.com/compatible-mode/v1`，新加坡/东京等需带 Workspace ID（如 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| `api_key` | string | 是 | 百炼 API Key，**按地域和计费方案隔离**，不可混用；推荐设为环境变量 `DASHSCOPE_API_KEY` | `sk-xxxxxxxxxxxxx` |
| `model` | string | 是 | 模型 ID，大小写敏感，必须在当前套餐支持列表内（如 `qwen3.7-plus`、`text-embedding-v4`、`qwen-vl-plus`） | `qwen3.7-max` |
| `messages` | array | 是（Chat/Responses） | OpenAI 标准格式，支持 `system`/`user`/`assistant`/`tool` 角色；`tool` 消息仅 Responses API 支持 | `[{"role":"user","content":"你好"}]` |
| `tools` + `tool_choice` | array / string/object | 否（Responses & Anthropic） | 替代已废弃的 `functions`，用于声明可用工具及调用策略（`auto`/`none`/`required`/`{"type":"function","name":"xxx"}`） | `{"type":"function","name":"search_web"}` |
| `stream` | boolean | 否 | 启用流式响应，默认 `false`；流式时响应字段为 `delta.content`（非 `output.text`） | `true` |
| `stream_options` | object | 否（流式时推荐） | 控制流式行为，如 `{"include_usage": true}` 可在最终 `done` chunk 中获取 token 统计 | `{"include_usage": true}` |
| `dimensions` | integer | 否（Embedding） | 仅 `text-embedding-v3/v4` 支持，指定输出向量维度（如 `256`、`1024`） | `1024` |
| `enable_thinking` | boolean | 否（部分模型必需） | 控制思考模式开关；`qwen3.8-max-preview` 等模型强制开启，需显式传入 | `true` |

> ⚠️ 注意事项：
> - `max_tokens` 在 Responses API 中限制的是**总上下文长度**（含 system [prompt](../guides/prompt.md)、tool definitions、messages），非纯 completion tokens；
> - `Responses API` 不支持 OpenAI 原生 `functions` 字段，必须使用 `tools` + `tool_choice`；
> - 流式响应字段路径为 `delta.content`（兼容模式） vs `output.text`（DashScope 原生），客户端需区分处理；
> - Qwen-Audio、私有调优模型、[多模态](multi-modal.md) Embedding（如 `qwen3-vl-embedding`）**不支持** OpenAI 兼容接口。

## 面向开发者，简洁实用

- ✅ **三步接入**：安装 `openai` SDK → 设置 `base_url` 和 `api_key` → 调用 `client.chat.completions.create()` 或 `client.embeddings.create()`。
- ✅ **一行切换模型**：只需改 `model="qwen-vl-plus"` 即可从文本切换到图文理解，无需改代码结构。
- ✅ **调试友好**：控制台「API 调试」页面支持直接填写 `messages` 和 `tools`，实时查看响应。
- ✅ **生产就绪**：支持连接池复用（Python `aiohttp.ClientSession` / Java `connectionPoolSize`）、临时 API Key（防泄露）、OSS 文件直传（`X-DashScope-OssResourceResolve: enable`）。
- ❌ **避坑提示**：不要复用 Anthropic 或 DashScope 原生的 `api_key`/`base_url`；不要在 `extra_body` 中传 `enable_thinking`（应为顶层字段）；不要对 `qwen-long` 使用 `completions` 接口（应走 `files` + `conversations`）。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more about models](../api/more-about-models.md)
- [application call](../api/application-call.md)


