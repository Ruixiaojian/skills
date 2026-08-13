# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者可通过 DashScope 原生 API 或 OpenAI 兼容的 Responses API 发起同步或异步请求，支持文本、图像、文件等[多模态](../concepts/multimodal.md)输入，并可维护会话上下文。所有调用均需提供有效的 `APP ID` 和（在特定场景下）`Workspace ID` 作为身份凭证 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流应用，但部分功能存在差异：
  - 文件输入（`input_file`）仅限**智能体应用**，且需在应用配置中启用“全文引用”或“切片检索”模式 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)；
  - 图像输入（`input_image`）要求应用选用通义千问 VL 系列模型，并按文档配置文件处理方式或模型入参变量；
  - [流式输出](../concepts/streaming-output.md)（`stream=true`）仅支持同步调用，**异步调用不支持流式** [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。

- **地域限制**：所有文档均明确标注“本文档仅适用于华北2（北京）地域”，但 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 指出德国（法兰克福）、新加坡、日本（东京）等地域调用时也必须传入 `Workspace ID`，且该 ID 是对应地域 Base URL 的组成部分。> **注意**：文档 2、4、5 均声明仅支持华北2（北京），而文档 1 明确列出其他地域需 `Workspace ID` —— 实际支持地域以控制台可用区域为准，建议优先查阅 [Regions 文档](https://help.aliyun.com/zh/model-studio/regions/)。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面获取。HTTP 调用时需嵌入 URL 路径；SDK 调用时作为显式参数传递。 |
| `input` | string / array | 是 | 核心输入内容：<br>- 字符串：单轮纯文本对话；<br>- 消息数组：支持多轮对话、[多模态](../concepts/multimodal.md)（文本+图像+文件）。消息对象需包含 `role`（`user`/`system`/`assistant`）与 `content`（文本字符串或含 `type`/`text`/`image_url`/`file_url` 的结构体）。 |
| `stream` | boolean | 否 | 默认 `false`。设为 `true` 启用流式响应（仅同步调用有效）。工作流应用需在结束节点启用“[流式输出](../concepts/streaming-output.md)”开关并重新发布。 |
| `background` | boolean | 否 | 默认 `false`。设为 `true` 切换为异步调用，立即返回任务 ID（`id`），后续通过 `retrieve` 查询结果。 |
| `session_id` | string | 否 | DashScope API 多轮对话专用。首次调用不传，响应中返回；后续请求携带该值即可延续上下文，有效期为最后一次请求后 1 小时。 |
| `biz_params` | object | 否 | 仅异步调用支持。用于向工作流或智能体应用传递自定义参数（如 `{"city": "北京"}`），参数名与应用内定义的开始节点参数严格一致。 |

## 使用方式

### 两种主流 API 风格
- **DashScope 原生 API**  
  Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  请求体结构简洁，`input.prompt` 为必填字段，适合快速集成。SDK（Python/Java）已内置 endpoint，HTTP 调用需手动构造 JSON。详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。

- **OpenAI 兼容 Responses API**  
  Endpoint（同步）：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  Endpoint（异步）：同上，但请求体含 `"background": true`  
  完全兼容 OpenAI SDK 接口（如 `client.responses.create`），支持 `messages` 数组格式、`stream`、`background` 等参数，便于复用现有代码库 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。

### 多轮对话实现
- **DashScope API**：依赖 `session_id` 字段，由服务端生成并返回，客户端需透传。
- **Responses API**：直接在 `input` 中传入完整消息历史数组（`messages`），无需维护 `session_id`；文档明确说明“基于 `pre_response_id` 或 `conversation_id` 的上下文功能将在后续支持”，当前必须传全量历史。

## 限制和注意事项

- **凭证获取**：`APP ID` 和 `Workspace ID` **仅支持控制台手动获取**，不提供 API 或 CLI 查询接口 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。RAM 子账号需被授予 `AliyunBailianFullAccess` 权限才能查看业务空间管理页面。
- **地域与 Workspace ID**：调用位于子业务空间的应用，或德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域的应用时，**必须提供 `Workspace ID`**（作为请求头或 URL 组成部分），否则返回权限错误。
- **异步调用约束**：`background=true` 时 `stream` 参数将被忽略，且不支持[流式输出](../concepts/streaming-output.md)；任务状态需轮询 `retrieve` 接口获取，无 Webhook 通知机制。
- **安全实践**：所有示例均强调 **禁止硬编码 `DASHSCOPE_API_KEY`**，应通过环境变量（如 `os.getenv("DASHSCOPE_API_KEY")`）注入，降低密钥泄露风险。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


