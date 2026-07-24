# application call

`application call` 是指通过 API 调用阿里云百炼平台已发布的应用（包括智能体、工作流等）的核心能力。开发者可使用 DashScope 原生 API 或 OpenAI 兼容模式的 Responses API，以同步或异步方式发起请求，支持单轮/多轮对话、[多模态](../concepts/multi-modal.md)输入（文本、图像、文件）及自定义参数传递。调用前需明确目标应用身份（APP ID）、运行环境（Workspace ID，如适用）和认证凭证（API Key）。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体、工作流三类应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **调用模式**：
  - **同步调用**：适用于实时交互场景，API 阻塞等待结果返回；支持[流式输出](../concepts/streaming-output.md)（`stream=true`），但仅对工作流应用生效（需在结束节点启用流式开关）[同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
  - **异步调用**：适用于耗时任务（如复杂工具链执行），立即返回任务 ID，后续通过轮询查询状态；**不支持[流式输出](../concepts/streaming-output.md)** [异步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **输入能力**：
  - 文本：单字符串或标准 OpenAI Messages 数组（含 `system`/`user`/`assistant` 角色）；
  - 图像：需选用通义千问 VL 系列模型，并在应用中配置为“自定义处理”（智能体）或模型入参变量设为 `imageList`（工作流）；
  - 文件：仅智能体应用支持，需配置[文件处理](../concepts/file-processing.md)方式为“全文引用”或“切片检索”。

> **注意**：文档 2 和文档 3 均声明“仅适用于华北2（北京）地域”，但文档 1 明确指出 Workspace ID 在德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域下为必需字段，且是 Base URL 的组成部分。这意味着实际支持地域不止北京，文档 2/3 的地域限制描述**过时或不完整**，应以文档 1 的地域列表为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面获取。 |
| `workspace_id` | string | 条件必填 | 业务空间唯一标识。当应用位于子业务空间，或部署在德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域时必须提供 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` | string \| array | 是 | 核心输入内容。单轮对话可为字符串（如 `"你是谁？"`）；多轮或[多模态](../concepts/multi-modal.md)需为 Messages 数组，其中 `content` 支持 `input_text`/`input_image`/`input_file` 类型。 |
| `session_id` | string | 否（多轮必需） | 用于维护会话上下文。首次调用不传，响应中返回；后续请求携带该值即可延续对话，有效期为最后一次请求后 1 小时。 |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming-output.md)（默认 `false`）。仅同步调用支持，且工作流应用需在发布前开启流式开关。 |
| `background` | boolean | 否 | 是否启用异步模式（默认 `false`）。设为 `true` 时立即返回任务 ID，后续需调用 `retrieve` 查询结果。 |
| `biz_params` | object | 否 | 传递应用内定义的自定义参数（如 `{"city": "北京"}`），参数名与类型须与应用配置严格一致。 |

## 使用方式

- **DashScope SDK（推荐）**：  
  Python 示例：`Application.call(api_key=..., app_id='xxx', prompt='...')`；Java 示例：`ApplicationParam.builder().apiKey(...).appId('xxx').prompt('...').build()`。SDK 默认配置正确 endpoint，无需手动拼接 URL。

- **HTTP 直连**：  
  - 同步（DashScope 模式）：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  - 同步（OpenAI 模式）：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  - 异步（OpenAI 模式）：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`（请求体含 `"background": true`）  
  > 所有 HTTP 请求均需携带 `Authorization: Bearer {DASHSCOPE_API_KEY}` 头。

- **在线调试**：在控制台应用卡片的 **发布 → API 调试** 页面直接填写参数并运行，无需编码。

## 限制和注意事项

- **地域与 Workspace ID**：调用子业务空间应用，或在德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域调用时，`workspace_id` 为必需参数，且需作为 Base URL 的一部分或独立请求头（具体依 SDK 版本而定）。
- **凭证安全**：API Key **严禁硬编码**在生产代码中，应通过环境变量（如 `DASHSCOPE_API_KEY`）注入。
- **权限要求**：获取 Workspace ID 需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号；普通子账号仅能查看已加入的业务空间 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **会话管理**：`session_id` 由服务端生成并返回，客户端负责透传；超时（1 小时无新请求）后失效，需新建会话。
- **异步任务生命周期**：创建后状态为 `queued` → `running` → 终态（`completed`/`failed`/`cancelled`）；终态后任务数据保留 7 天，之后自动清理。
- **错误处理**：所有调用均返回 `request_id`，用于问题排查；详细错误码请参考官方错误码文档。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)


