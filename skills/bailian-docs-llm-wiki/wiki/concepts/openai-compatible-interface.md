# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一套标准化 API 协议层，严格遵循 OpenAI REST API 的路径、请求/响应格式、参数命名与语义规范（如 `/v1/chat/completions`），使开发者能复用现有 OpenAI SDK（Python/Node.js 等）、工具链（Dify/Cursor/Postman）和业务代码，零改造接入百炼托管的千问（Qwen）及第三方模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **基础模型调用**：通过 `chat/completions`、`embeddings`、`files`、`batches` 等标准端点调用文本生成、向量检索、文档解析等能力，支持 `qwen3.8-max`、`qwen3.7-plus`、`deepseek-v4-flash`、`text-embedding-v3` 等数十种模型。
- **智能体（Agent）开发**：使用专为 Agent 设计的 `responses` 接口（路径 `/v1/responses`），自动管理上下文、内置工具调用（联网搜索/代码解释器）和多轮状态延续，无需手动拼接 `messages`。
- **应用集成**：在调用已发布的智能体或工作流时，可选用 OpenAI 兼容的 `application call` 模式（路径 `/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`），支持同步/异步、[流式输出](streaming-output.md)及自定义 `biz_params`。
- **多模态交互**：在 `chat/completions` 中传入含 `image_url` 或 Base64 图像的 `messages`，即可调用 `qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 等视觉模型（注意：Qwen-Audio 和多模态 Embedding 不支持该协议）。
- **开发工具对接**：直接配置第三方客户端（如 Cursor、Claude Code、Cherry Studio）或低代码平台（如 Dify），只需填入百炼的 OpenAI 兼容 `base_url` 和 `api_key`，即可开箱即用。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `base_url` | 必填。服务入口地址，格式为 `https://{domain}/compatible-mode/v1`。地域决定域名结构：<br>• 华北2（北京）、新加坡：需替换 `{WorkspaceId}`（如 `w-abc123.cn-beijing.maas.aliyuncs.com`）<br>• 美国（弗吉尼亚）、德国（法兰克福）、日本（东京）：使用固定域名（如 `dashscope-us.aliyuncs.com`），**不包含 WorkspaceId**<br>• 试用域名仅限测试（`trial.cn-beijing.maas.aliyuncs.com`），RPM=1000 | 必须与 `api_key` 所属地域、计费方案（[Token](token.md) Plan/Coding Plan/按量）严格匹配，否则返回 401 |
| `api_key` | 必填。通过 [百炼控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建，建议设为环境变量 `DASHSCOPE_API_KEY` | 不同计费方案（如 [Token](token.md) Plan 个人版 vs 按量计费）的 Key **不可混用** |
| `model` | 必填。模型 ID，严格区分大小写与版本后缀（如 `qwen3.8-max` ≠ `qwen3.7-max`）。部分模型有地域限制（如 DeepSeek 仅支持北京/新加坡） | 查看 [模型支持列表](https://help.aliyun.com/zh/model-studio/models) 确认可用性，跨地域调用将失败 |
| `stream` | 可选（默认 `false`）。设为 `true` 启用流式响应（SSE）。Vision 模型（如 QVQ）强制流式 | 流式响应中，最后一 chunk 可通过 `stream_options={"include_usage": true}` 获取 token 统计 |
| `previous_response_id` | Responses API 专用。传入上一轮响应的顶层 `id`（非 `output.msg_xxx`），用于自动关联上下文（有效期 7 天） | 仅 `responses` 接口支持，`chat/completions` 需显式维护完整 `messages` 数组 |
| `extra_body` | 可选。OpenAI 兼容接口扩展字段，用于传递协议未定义但模型需要的参数，如：<br>• `vl_high_resolution_images: true`（GUI-Plus）<br>• `translation_options: {...}`（Qwen-MT）<br>• `enable_thinking: true`（Qwen3 思考模式） | 需查阅对应模型文档确认支持字段，非法字段会被忽略 |

## 面向开发者，简洁实用

- ✅ **快速起步**：复制示例代码，仅需替换 `base_url`（填入你的 `WorkspaceId` 或固定域名）和 `DASHSCOPE_API_KEY` 环境变量，5 分钟完成首次调用。
- ✅ **无缝迁移**：已有 OpenAI 项目，只需修改 `client = OpenAI(...)` 初始化参数，其余代码（`messages` 结构、`model` 名称、`stream` 逻辑）完全兼容。
- ✅ **统一调试**：所有 OpenAI 兼容接口共用 `/compatible-mode/v1` 路径前缀，便于统一监控、日志采集和限流策略配置。
- ⚠️ **避坑提示**：
  - 不要混用地域：`api_key`（北京） + `base_url`（弗吉尼亚） → 401 错误；
  - 不要硬编码 `WorkspaceId`：推荐用环境变量或配置中心动态注入；
  - 不要忽略模型兼容性：`qwen3-vl-embedding`、`qwen-audio`、`qwen-deep-research` **不支持** OpenAI 兼容接口，必须用 DashScope 原生协议；
  - 异步调用需设 `"background": true`，此时 `stream` 自动失效，结果需轮询 `retrieve` 接口获取。

> 提示：最新地域域名、模型支持矩阵及完整参数参考，请查阅 [Base URL 总览](https://help.aliyun.com/zh/model-studio/base-url) 和 [OpenAI 兼容接口 API 参考](https://help.aliyun.com/zh/model-studio/openai-compatible-api-reference)。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application call](../api/application-call.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more models](../api/more-models.md)


