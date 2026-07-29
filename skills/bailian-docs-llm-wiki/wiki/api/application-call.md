# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者可通过 OpenAI 兼容的 Responses API 或原生 DashScope API 两种方式发起同步或异步请求，支持文本、图像、文件等多模态输入，并可选流式响应。调用前需明确应用类型、地域约束及凭证配置。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流三类应用，但不同 API 路径和参数要求存在差异。例如，[新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 明确限定仅适用于新版智能体，而 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md) 则覆盖所有类型。
- **多模态输入**：同步调用支持图像（`input_image`）和文件（`input_file`）输入，但文件输入**仅限智能体应用**，且需在应用内配置为“全文引用”或“切片检索”模式；图像输入则需选用通义千问 VL 系列模型并正确配置文件处理方式或模型节点入参 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
- **会话管理**：DashScope API 通过 `session_id` 实现多轮对话上下文维护（有效期 1 小时），而 Responses API 当前**不支持 `pre_response_id` 或 `conversation_id`**，必须在每次请求中显式传递完整消息历史 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。

> **注意**：文档 4 和文档 5 均描述了 `/api/v1/apps/{APP_ID}/completion` 接口，但文档 4 标题明确为“新版智能体应用 API”，文档 5 标题为“应用 DashScope API”且内容涵盖智能体与工作流。二者接口路径一致，但适用范围描述存在重叠与模糊。实际使用应以应用创建类型和控制台提示为准，建议优先参考 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md) 的通用说明。

## 关键参数

- **`app_id`**（必选）：应用唯一标识，在 [应用管理](https://bailian.console.aliyun.com/#/app-center) 页面获取。若应用位于子业务空间或特定地域（如德国法兰克福、华北2北京、新加坡、日本东京），还需提供 `workspace_id` [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **`input` / `prompt`**（必选）：
  - Responses API 使用 `input` 字段，支持字符串（单轮）或消息数组（多轮/多模态）；
  - DashScope API 使用 `prompt` 字段（单轮）或 `messages` 数组（多轮），结构更简洁。
- **`stream`**（可选，Responses API）：布尔值，启用[流式输出](../concepts/streaming-output.md)。**注意**：异步调用（`background=true`）不支持[流式输出](../concepts/streaming-output.md) [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **`background`**（可选，Responses API）：布尔值，设为 `true` 即发起[异步任务](../concepts/asynchronous-task.md)，立即返回任务 ID。
- **`biz_params`**（可选，Responses API 异步调用）：用于向工作流或智能体应用传递自定义参数（如城市名、索引值），需与应用内定义的参数名和类型严格匹配 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。

## 使用方式

- **同步调用（实时响应）**：
  - **Responses API**：Endpoint 为 `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`，推荐用于 OpenAI 生态迁移场景。
  - **DashScope API**：Endpoint 为 `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`，SDK 调用更简洁，支持 `session_id` 维护会话。
- **异步调用（长任务）**：
  - 仅 Responses API 支持，通过设置 `background=true` 发起，随后需轮询 `GET /responses/{task_id}` 获取状态与结果 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **[流式输出](../concepts/streaming-output.md)**：
  - 仅 Responses API 同步调用支持，需设置 `stream=true` 并在应用端（工作流结束节点/流程输出节点）启用流式开关后重新发布 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。

## 限制和注意事项

- **地域限制**：所有文档均强调“本文档仅适用于华北2（北京）地域”，但 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 明确指出 Workspace ID 在德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域下为必需。这意味着跨地域调用需严格匹配 Base URL 和 Workspace ID 配置。
- **凭证获取**：APP ID 和 Workspace ID **只能通过控制台手动获取**，不支持 API 或 CLI 查询 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **权限要求**：查询所有业务空间 ID 需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号，普通子账号仅能查看已加入的业务空间 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **API Key 安全**：所有示例均强调避免在生产代码中硬编码 `DASHSCOPE_API_KEY`，应优先使用环境变量配置。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)


