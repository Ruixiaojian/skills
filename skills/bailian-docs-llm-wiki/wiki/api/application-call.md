# application call

`application call` 是阿里云百炼平台提供的核心 API 调用能力，用于以编程方式触发已发布的智能体（Agent）或工作流（Workflow）应用。它支持同步与异步两种模式，兼容 DashScope 原生协议和 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，适用于实时交互、长耗时任务及多模态场景。调用前需完成凭证配置（API Key + APP ID），并根据应用部署位置决定是否需附加 Workspace ID。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流三类应用，但功能覆盖存在差异：
  - 图像输入（`input_image`）仅在 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md) 中明确支持，且要求智能体应用选用通义千问 VL 系列模型并配置为“自定义处理”；
  - 文件输入（`input_file`）仅限智能体应用，需在应用内设置文件处理方式为“全文引用”或“切片检索”；
  - 工作流应用若需[流式输出](../concepts/streaming-output.md)，必须在结束节点或流程输出节点中显式启用“[流式输出](../concepts/streaming-output.md)”开关并重新发布。
- **地域限制**：所有文档均强调“本文档仅适用于华北2（北京）地域”，但 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 明确指出德国（法兰克福）、新加坡、日本（东京）等地域调用时也**必须提供 Workspace ID**，且该 ID 是对应地域 Base URL 的组成部分。> **注意**：DashScope API 文档（文档2、3）与 Responses API 文档（文档4、5）均未说明非北京地域的 endpoint 配置方式，实际调用需参考 [业务空间权限管理](https://help.aliyun.com/zh/model-studio/permission-management-overview#dac6676deelh2) 中的 Base URL 规则。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，从[应用管理](https://bailian.console.aliyun.com/#/app-center)页面复制。详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `workspace_id` | string | 条件必选 | 仅当应用位于子业务空间，或部署在德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域时必需。通过控制台右上角业务空间图标或[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)界面获取。 |
| `input` | string 或 array | 是 | 核心输入内容：<br>- 字符串：单轮纯文本对话；<br>- 消息数组：支持多轮对话、图像（`input_image`）、文件（`input_file`）等多模态输入。消息对象需包含 `role`（`user`/`system`/`assistant`）和 `content`（文本字符串或含 `type`/`text`/`image_url`/`file_url` 的对象）。 |
| `stream` | boolean | 否（默认 false） | 是否启用流式响应。**异步调用不支持[流式输出](../concepts/streaming-output.md)**（见 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)）。 |
| `background` | boolean | 否（默认 false） | 是否启用异步模式。设为 `true` 时立即返回任务 ID，需后续轮询查询结果。 |
| `biz_params` | object | 否 | 用于向工作流或智能体应用传递自定义参数（如城市名、索引值等），参数名与应用内定义严格一致。 |

## 使用方式

- **HTTP 调用**：
  - DashScope 原生接口：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`（文档2、3）；
  - [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（同步）：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`（文档4）；
  - [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（异步）：同上，但请求体需包含 `"background": true`（文档5）。
- **SDK 调用**：
  - DashScope SDK（Python/Java 等）：直接使用 `Application.call()` 方法，自动处理 endpoint（文档2、3）；
  - OpenAI SDK（Python/Java）：初始化客户端时指定 `base_url` 为 `https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/`，再调用 `client.responses.create()`（文档4、5）。
- **在线调试**：通过应用卡片 → 发布 → API 调试路径快速验证参数与响应（文档2、3）。

## 限制和注意事项

- **凭证获取**：APP ID 和 Workspace ID **仅支持通过控制台手动获取**，不提供 API 或 CLI 查询方式（见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)）。
- **会话管理**：DashScope API 的多轮对话依赖 `session_id`（首次响应返回，后续请求携带），有效期为最后一次请求后 1 小时；而 OpenAI 兼容接口**暂不支持基于 `pre_response_id` 或 `conversation_id` 的上下文管理**，必须在每次请求中传递完整对话历史（文档3、4）。
- **权限要求**：查询所有业务空间 ID 需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号；普通 RAM 子账号仅能查看其已加入的业务空间（文档1）。
- **错误处理**：所有示例代码均包含对 `status_code` 或 `response.status` 的检查，并建议参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code) 进行调试。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


