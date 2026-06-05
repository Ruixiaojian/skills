# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台对外暴露的一组与 OpenAI 官方 SDK 协议保持一致的 HTTP/SDK 端点，开发者只需替换 `api_key`、`base_url`、`model` 三个参数，即可将已有的 OpenAI 应用零改造迁移到百炼托管的模型上（千问、DeepSeek、Kimi、GLM、MiniMax、万相等）。该兼容层覆盖文本生成、多模态、嵌入、批处理、应用调用、模型调优等绝大多数场景，与百炼原生的 DashScope 接口并行存在。

## 通用接入：三要素

不论调用哪一类兼容接口，接入模型都只有三个必填配置项：

| 参数 | 取值 |
| --- | --- |
| `api_key` | 百炼 API Key（**各地域 Key 互不通用**，按量付费、Coding Plan、Token Plan 团队版各自独立） |
| `base_url` | 兼容模式根路径，见下方"服务地址"小节 |
| `model` | 百炼模型名（如 `qwen-plus`、`qwen3-vl-plus`、`text-embedding-v4`、`qwen3-livetranslate-flash` 等） |

> Base URL、API Key 与模型必须归属同一地域、同一计费方式，跨地域或跨套餐混搭会返回 `401 Incorrect API key` 或 `400 url error` / `404 status code`。

## 服务地址（base_url）

按地域与套餐选择正确端点：

| 场景 | base_url |
| --- | --- |
| 按量付费 · 华北 2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 按量付费 · 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 按量付费 · 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 按量付费 · 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |
| Batch（同步/文件输入） | `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`（中国内地） |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/compatible-mode/v1`（或 `/v1`） |
| Token Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| 语音/音视频翻译 · 北京 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 语音/音视频翻译 · 新加坡 | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` |

> 新加坡地域旧域名 `https://dashscope-intl.aliyuncs.com` 即将下线，需迁移到带 `WorkspaceId` 的新版域名；Responses / Conversations 旧版路径 `/api/v2/apps/protocols/compatible-mode/v1/...` 即将停止维护，请改用 `/compatible-mode/v1/...`。

## 覆盖的接口体系

百炼的 OpenAI 兼容层共有 8 类标准接口，端点与 OpenAI 官方一致：

| 接口 | 端点 | 主要用途 |
| --- | --- | --- |
| Chat Completions | `/v1/chat/completions` | 最常用的对话接口，支持千问商业版、开源版、QwQ、Vision、Speech Translation 非实时等 |
| Responses | `/v1/responses` | Chat Completions 的演进版，面向智能体场景，内置联网搜索/代码解释器/网页抓取等工具，支持通过 `previous_response_id` 自动管理对话历史 |
| Completions | `/v1/completions` | 前缀补全 / FIM 中间填充，目前仅 `qwen-coder-turbo`、仅北京地域 |
| Vision（多模态 Chat） | `/v1/chat/completions` | 同 Chat 端点，`messages.content` 改为数组，含 `image_url` / `input_audio` / `video_url` 等块 |
| Embedding | `/v1/embeddings` | 文本向量化，如 `text-embedding-v4` |
| Files | `/v1/files` | 文件上传，供 Batch、Vision、Audio 等引用 |
| Batch | `/v1/batches` | 异步批量推理，支持同步/文件输入两种入口 |
| Conversations | `/v1/conversations` | 会话状态管理（与 Responses 配合） |

## 在不同场景中的使用

### 1. 文本生成调用

- 适合**迁移现有 OpenAI 代码**的项目：直接使用 OpenAI 官方 SDK（Python / Node.js / curl），仅替换三要素即可。
- 不需要手动维护对话历史时优先选 Responses 接口（通过顶层 `id`，UUID 格式，有效期 7 天）。
- 需要使用百炼全部能力（多轮上下文 + Plugin + RAG + Function Calling 等完整功能集）应回退到 DashScope 原生接口。

### 2. 应用（智能体 / 工作流）调用

百炼应用调用提供 OpenAI 兼容的 Responses 端点：

```
POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses
```

- SDK：OpenAI 官方 SDK 的 `client.responses.create`。
- 请求结构：`{ "input": "..." }` 或消息数组。
- 多模态：支持 `input_text` / `input_image` / `input_file` 三种内容块。
- 异步：在请求体设置 `background=true`。
- 与 DashScope 原生 `Application.call` 相比，功能/性能略弱，但便于复用 OpenAI 生态工具。

### 3. 语音 / 音视频翻译（Qwen-LiveTranslate）

**非实时**音视频翻译必须走 OpenAI 兼容 `chat/completions` 路径（该模型族不支持 DashScope 原生 `multimodal-generation/generation` 协议）：

- 模型：`qwen3-livetranslate-flash`、`qwen3-livetranslate-flash-2025-12-01`。
- `stream` 必须为 `true`（仅支持流式输出）；建议 `stream_options.include_usage=true`。
- `messages.content` 放 `input_audio` 或 `video_url` 块；`translation_options` 至少携带 `target_lang`。Python SDK 中 `translation_options` 需通过 `extra_body` 透传。

> 实时流式翻译走原生 WebSocket，不属于 OpenAI 兼容范围。

### 4. 模型调优（Fine-tuning）

调优任务通过 OpenAI 兼容的 `/api/v1/fine-tunes` HTTP 接口发起（也可在控制台操作），覆盖文本、视觉、图像、视频、语音五种模态；当前仅北京地域可用，产出模型不支持下载。

### 5. 客户端 / IDE / 编码 Agent 接入

主流客户端（Cherry Studio、Chatbox、Cursor、Cline、Claude Code、Qwen Code、Codex、OpenCode、Kilo CLI、Hermes Agent、Qoder、Dify、OpenClaw 等）通常直接通过 OpenAI 兼容协议接入百炼。开发者只需要在客户端里填写三要素，按量付费、Coding Plan、Token Plan 团队版均通过这一协议落地（部分客户端如 Claude Code 走 Anthropic 兼容协议 `/apps/anthropic`，与 OpenAI 兼容协议路径不同）。

### 6. 框架集成

LangChain、LangChain4j 等主流编排框架已对接 OpenAI 兼容层，无需额外驱动包，只需把 `OpenAI` LLM 类的 `base_url` / `api_key` 指向百炼即可。

## 关键参数与配置约定

- **`api_key`**：放入 `Authorization: Bearer ...` Header 或 SDK 构造函数；按量付费 `sk-xxxxx`，Coding Plan / Token Plan 团队版均为 `sk-sp-xxxxx`，但**两套 `sk-sp-` Key 互不相通**。
- **`base_url`**：必须与套餐、地域严格匹配；Anthropic 兼容协议以 `/apps/anthropic` 结尾，OpenAI 兼容协议以 `/compatible-mode/v1` 或 `/v1` 结尾，路径不匹配会直接报错。
- **`model`**：必须是当前套餐 / 地域可见模型。例如 Coding Plan 不包含 `qwen3.7-max`、`qwen-image-2.0`、`wan2.7-image` 与 DeepSeek 系列；Token Plan 团队版与 Coding Plan 的模型白名单不一致，需逐字符匹配。
- **流式输出**：`stream=true` + 可选 `stream_options.include_usage` 拿到 Token 用量；Responses 接口默认非流式，可显式开启。
- **上下文管理**：Chat Completions 需要手动维护 `messages` 历史；Responses 通过 `previous_response_id` 自动串联，无需自行拼接。
- **多模态输入**：Vision 走 `image_url`；Speech Translation 走 `input_audio` / `video_url`；应用调用走 `input_text` / `input_image` / `input_file`。

## 注意事项

- 不同接口支持的参数范围不同，DashScope 原生接口覆盖最广；如需百炼全功能（如部分 Plugin、RAG、复杂 Function Calling 行为），优先选 DashScope。
- Responses 接口自动管理对话历史，状态机与 Chat Completions 不一致，迁移时需重写上下文逻辑。
- 地域 API Key 不通用：把北京 Key 用到新加坡 / 美国 / 德国端点会直接 401。
- `/compatible-mode/v1` 与 Coding Plan 的 `/v1` 路径并不等价，混用会触发 `404 status code`。
- Completions、CosyVoice 调优等部分能力**仅 API 可用、控制台不支持**，请按各能力页面的限制阅读。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)
- [fine tuning](../guides/fine-tuning.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [token plan guide](../guides/token-plan-guide.md)


