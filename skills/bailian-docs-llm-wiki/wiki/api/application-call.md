# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者可使用 DashScope 原生 API 或 OpenAI 兼容的 Responses API 发起请求，支持单轮/多轮对话、多模态输入（文本、图像、文件）及会话状态管理。所有调用均需提供有效的 `APP ID`，部分场景还需 `Workspace ID` 和 `API Key`。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **多模态能力**：
  - 图像理解：需选用通义千问 VL 系列模型，并在应用中配置为「自定义处理」（智能体）或模型入参变量设为 `imageList`（工作流）[同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
  - 文件问答：仅智能体应用支持，需将[文件处理](../concepts/file-processing.md)方式设为「全文引用」或「切片检索」。
- **交互模式**：
  - 单轮/多轮对话（通过 `session_id` 或完整 `messages` 数组维护上下文）；
  - [流式输出](../concepts/streaming-output.md)（仅同步调用支持，且工作流应用需在结束节点启用流式开关）；
  - [异步任务](../concepts/asynchronous-task.md)（通过 `background=true` 触发，返回 `task_id` 后轮询结果）。

> **注意**：文档 2 和文档 3 均声明“仅适用于华北2（北京）地域”，但文档 1 明确指出德国（法兰克福）、华北2（北京）、新加坡、日本（东京）等地域调用子业务空间应用时**必须传入 `Workspace ID`**，且 `Workspace ID` 是这些地域 Base URL 的组成部分。这表明跨地域调用能力实际存在，文档 2/3 的地域限制描述可能已过时或仅针对特定 SDK 默认配置。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，从控制台 [应用管理](https://bailian.console.aliyun.com/#/app-center) 获取。详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `workspace_id` | string | 条件必填 | 子业务空间或特定地域（德/京/新/东京）下应用的业务空间 ID，需与 `app_id` 配合使用。 |
| `input` | string / array | 是 | 核心输入：<br>- 字符串：单轮纯文本；<br>- 消息数组：支持 `system`/`user`/`assistant` 角色，`user` 消息 `content` 可为字符串或含 `input_text`/`input_image`/`input_file` 的数组。 |
| `stream` | boolean | 否 | `true` 启用[流式输出](../concepts/streaming-output.md)（同步调用专属）。 |
| `background` | boolean | 否 | `true` 启用异步调用，立即返回 `task_id`。 |
| `biz_params` | object | 否 | 传递应用内定义的自定义参数（如城市名、索引值），需与应用配置严格一致。 |

## 使用方式

### 1. 接口地址
- **DashScope 原生 API**（推荐用于高性能/全功能场景）：  
  `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
- **OpenAI 兼容 Responses API**（便于迁移现有代码）：  
  - 同步：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  - 异步：同上，但请求体中 `background=true`

### 2. 认证方式
- Header 中携带 `Authorization: Bearer {DASHSCOPE_API_KEY}`，API Key 通过 [密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key) 获取并建议配置为环境变量。

### 3. 多轮对话实现
- **DashScope 方式**：首次请求不带 `session_id`，响应中返回 `output.session_id`；后续请求在参数中传入该 `session_id` 即可延续会话（有效期 1 小时）。
- **Responses API 方式**：直接在 `input` 数组中传入完整历史消息（`messages`），无需维护 `session_id`。

## 限制和注意事项

- **地域与 Workspace 限制**：调用位于子业务空间的应用，或在德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域的应用时，**必须提供 `Workspace ID`**，且其值需作为 Base URL 的一部分或独立参数传递 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **权限要求**：RAM 子账号默认只能查看其已加入的业务空间 ID；查询全部 Workspace ID 需主账号或具备 `AliyunBailianFullAccess` 权限的超级管理员 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **异步与流式互斥**：`background=true` 时 `stream` 参数无效，异步调用不支持[流式输出](../concepts/streaming-output.md) [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **凭证获取方式**：`APP ID` 和 `Workspace ID` **仅支持控制台手动获取**，不提供 API 或 CLI 查询接口 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **SDK 版本要求**：Java SDK 调用 DashScope API 时，建议版本 ≥ 2.12.0；OpenAI SDK 调用 Responses API 需安装对应语言的兼容版本。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


