# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者可通过 OpenAI 兼容的 Responses API 或原生 DashScope API 两种方式发起同步或异步请求，支持文本、图像、文件等多模态输入，并可复用现有 SDK 生态。所有调用均需提供有效的 APP ID 及认证凭据。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **输入模态**：
  - 文本：单轮/多轮对话（`input` 字符串或 `messages` 数组）；
  - 图像：需选用通义千问 VL 系列模型，并在应用配置中启用自定义处理（智能体）或设置 `imageList` 入参（工作流），详见 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)；
  - 文件：仅智能体应用支持，需配置文件处理方式为“全文引用”或“切片检索”；
- **输出模式**：支持同步响应、[流式输出](../concepts/streaming-output.md)（仅同步调用）及异步任务（通过 `background=true` 触发）；
- **会话管理**：DashScope API 通过 `session_id` 维护上下文；Responses API 当前不支持 `pre_response_id` 或 `conversation_id`，需显式传递完整历史消息。

> **注意**：文档 4 和文档 5 均描述了 `/api/v1/apps/{APP_ID}/completion` 接口，但文档 4 明确限定为“新版智能体应用”，而文档 5 泛指“智能体与工作流应用”。实际调用时，请根据应用类型选择对应文档——新版智能体优先参考 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)，通用场景参考 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，从控制台[应用管理](https://bailian.console.aliyun.com/#/app-center)获取，详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` / `prompt` | string 或 array | 是 | 请求内容：Responses API 使用 `input`（支持字符串或 messages 数组）；DashScope API 使用 `prompt`（单轮）或 `messages`（多轮）。 |
| `stream` | boolean | 否 | 仅 Responses API 支持，设为 `true` 启用[流式输出](../concepts/streaming-output.md)；工作流应用需在结束节点启用“[流式输出](../concepts/streaming-output.md)”开关并重新发布。 |
| `background` | boolean | 否 | 仅 Responses API 支持，设为 `true` 触发异步调用，立即返回任务 ID；异步任务不支持 `stream=true`。 |
| `biz_params` | object | 否 | 仅异步调用支持，用于向工作流或智能体应用传递自定义参数（如 `{"city": "北京"}`），参数名须与应用内配置一致。 |
| `session_id` | string | 否 | 仅 DashScope API 支持，用于多轮对话上下文维护，首次调用不传，后续请求携带上一轮响应中的 `session_id`。 |

## 使用方式

- **OpenAI 兼容模式（Responses API）**：
  - 同步调用：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`，适用于实时交互；
  - 异步调用：在请求体中添加 `"background": true`，再通过 `GET /responses/{task_id}` 查询结果；
  - SDK 示例见 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md) 和 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。

- **原生 DashScope API**：
  - 统一入口：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`；
  - 支持 Python/Java/HTTP 等多种调用方式，含在线调试入口（应用卡片 → 发布 → API 调试）；
  - 多轮对话依赖 `session_id`，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)。

> **注意**：所有文档均强调“本文档仅适用于华北2（北京）地域”，但 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 明确指出：德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域下的模型调用必须包含 `Workspace ID`，且 `Workspace ID` 是这些地域 Base URL 的组成部分。因此，跨地域调用时务必确认是否需补充 `Workspace ID` 参数。

## 限制和注意事项

- **地域与凭证**：华北2（北京）为默认支持地域；其他支持地域（如德国、新加坡）调用时，必须同时提供 `APP ID` 和 `Workspace ID`，且 `Workspace ID` 需通过控制台手动获取，不支持 API 查询；
- **权限要求**：RAM 子账号需被授予 `AliyunBailianFullAccess` 或 `AliyunBailianControlFullAccess` 权限才能查询全部业务空间 ID；
- **功能限制**：
  - Responses API 的 `pre_response_id` 和 `conversation_id` 上下文功能尚未支持，需每次传递完整对话历史；
  - 异步调用不支持流式输出；
  - 文件输入仅限智能体应用，工作流暂不支持；
- **安全实践**：生产环境严禁硬编码 `DASHSCOPE_API_KEY`，应通过环境变量或密钥管理服务注入。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)


