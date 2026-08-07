# application call

`application call` 是指通过 API 调用阿里云百炼平台已发布的应用（包括新版智能体、旧版智能体、工作流等），向其提交输入并获取模型或流程执行结果的核心交互方式。调用需提供有效的 `APP ID`（必要）、`Workspace ID`（按地域与业务空间层级条件可选）及认证凭据（API Key），支持同步与异步两种模式，并兼容 DashScope 原生接口和 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体、工作流三类应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **多模态能力**：通过 OpenAI 兼容的 Responses API，支持图像（`input_image`）和文件（`input_file`）输入，但文件仅限智能体应用，且需在应用内配置为“全文引用”或“切片检索”[同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
- **会话管理**：DashScope API 通过 `session_id` 维护多轮对话上下文（有效期 1 小时）；OpenAI 兼容 API 则要求显式传递完整 `messages` 数组，当前不支持基于 `pre_response_id` 或 `conversation_id` 的隐式上下文延续。

> **注意**：文档 2 和文档 3 均声明“仅适用于华北2（北京）地域”，但文档 1 明确指出 Workspace ID 在德国（法兰克福）、华北2（北京）、新加坡、日本（东京）等多地均为必需。这意味着 DashScope API 的地域限制与 Workspace ID 的适用范围存在不一致，实际调用前请以控制台显示的 Base URL 和当前地域为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)中获取。所有调用均需此参数。 |
| `workspace_id` | string | 按需 | 业务空间唯一标识。当应用位于子业务空间，或部署在德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域时，必须提供。参见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` | string / array | 是 | 核心输入内容。DashScope API 使用 `input.prompt`（单轮）或 `input.messages`（多轮）；OpenAI 兼容 API 直接使用 `input` 字段，支持字符串或符合 OpenAI Messages 格式的数组。 |
| `stream` | boolean | 否（默认 false） | 仅 OpenAI 兼容 API 支持。设为 `true` 启用[流式输出](../concepts/streaming-output.md)，但工作流应用需在结束节点手动开启“[流式输出](../concepts/streaming-output.md)”开关并重新发布。 |
| `background` | boolean | 否（默认 false） | 仅 OpenAI 兼容 API 支持。设为 `true` 进入异步模式，立即返回任务 ID，后续通过 `retrieve` 查询结果。异步模式下 `stream=true` 不生效。 |
| `biz_params` | object | 否 | 仅 OpenAI 兼容 API 异步/同步调用中支持，用于向工作流或插件配置的自定义参数传值，参数名与类型须与应用内定义严格一致。 |

## 使用方式

### 接口地址
- **DashScope API（推荐）**：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
- **OpenAI 兼容 API（同步）**：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
- **OpenAI 兼容 API（异步）**：同上，仅需在请求体中设置 `"background": true`  

### 调用方式
- **HTTP 直连**：构造标准 POST 请求，携带 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 头及 JSON body。
- **SDK 调用**：
  - DashScope SDK（Python/Java 等）：直接调用 `Application.call()`，自动处理 endpoint。
  - OpenAI SDK（Python/Java 等）：初始化客户端时指定 `base_url` 为对应兼容模式地址，再调用 `client.responses.create()`。
- **在线调试**：在控制台应用卡片的 **发布 → API 调试** 页面中填写参数并运行，无需编码。

### 多轮对话示例（DashScope）
首次调用不传 `session_id`，响应中返回 `output.session_id`；后续请求在参数中传入该 `session_id` 即可延续上下文。

## 限制和注意事项

- **地域与 Workspace ID 强绑定**：调用非默认业务空间的应用，或在德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域调用任何应用，均**必须**同时提供 `APP ID` 和 `Workspace ID`，且 `Workspace ID` 是 Base URL 的组成部分之一 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **凭证获取方式受限**：`APP ID` 和 `Workspace ID` **仅支持通过控制台手动获取**，不支持 API 或 CLI 查询。
- **权限要求**：查询全部业务空间 ID 需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号；普通子账号仅能查看已加入的业务空间。
- **[异步任务](../concepts/asynchronous-task.md)约束**：异步调用（`background=true`）不支持[流式输出](../concepts/streaming-output.md)，且需主动轮询 `retrieve` 接口获取最终结果；任务状态终态为 `completed`、`failed` 或 `cancelled`。
- **SDK 版本依赖**：Java SDK 调用 DashScope API 时，建议版本 ≥ 2.12.0，否则可能缺少关键方法或参数支持。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


