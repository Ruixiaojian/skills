# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者只需提供应用凭证（APP ID 及可选的 Workspace ID）、API Key 和输入内容，即可触发应用逻辑并获取结构化响应。该机制支持文本、图像、文件等多模态输入，并兼容 OpenAI SDK 调用习惯，适用于实时交互与长耗时任务两类场景。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **调用模式**：
  - **同步调用**：适用于即时响应场景（如聊天机器人），通过 Responses API 或 DashScope API 实现，支持[流式输出](../concepts/streaming-output.md)（`stream=true`）；但需注意 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md) 明确指出“异步任务暂不支持[流式输出](../concepts/streaming-output.md)”。
  - **异步调用**：适用于耗时较长任务（如报告生成、多步骤工具链执行），通过设置 `background=true` 触发，返回任务 ID 后轮询结果。
- **多模态能力**：
  - 图像输入：需选用通义千问 VL 系列模型，并在应用中配置[文件处理](../concepts/file-processing.md)方式为“自定义处理”（智能体）或模型入参变量为 `imageList`（工作流）。
  - 文件输入：仅智能体应用支持，需配置[文件处理](../concepts/file-processing.md)方式为“全文引用”或“切片检索”。

> **注意**：文档 2 和文档 3 均声明“本文档仅适用于华北2（北京）地域”，而文档 1 指出“在德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域下的模型时，API 请求中才必须包含 `Workspace ID`”。这意味着 Workspace ID 的强制性与地域强相关，但文档 2/3 未提及 Workspace ID 使用场景，存在信息缺失风险，实际调用前请务必按 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 文档确认凭证要求。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面复制。若应用位于子业务空间或特定地域（如法兰克福、北京、新加坡、东京），还需配合 `workspace_id` 使用。 |
| `workspace_id` | string | 条件必填 | 业务空间唯一标识，仅当应用部署于子业务空间或上述指定地域时必需。获取方式见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` | string \| array | 是 | 核心输入内容：<br>- 字符串：单轮纯文本对话（如 `"你好"`）；<br>- 消息数组：支持多轮对话、图像（`input_image`）、文件（`input_file`）等多模态输入。消息对象需含 `role`（`user`/`system`/`assistant`）和 `content`（文本字符串或含 `type`/`text`/`image_url`/`file_url` 的对象数组）。 |
| `stream` | boolean | 否（默认 `false`） | 是否启用[流式输出](../concepts/streaming-output.md)。仅同步调用有效；异步调用（`background=true`）下该参数被忽略。 |
| `background` | boolean | 否（默认 `false`） | 是否启用异步模式。设为 `true` 时立即返回任务 ID，需后续调用 `retrieve` 查询结果。 |
| `biz_params` | object | 否 | 用于传递应用内定义的自定义参数（如城市名、索引值等），键名需与应用配置完全一致。 |

## 使用方式

### 1. 凭证准备
- 获取 `APP ID` 和（条件性）`Workspace ID`：通过控制台手动复制，[不支持 API 或 CLI 查询](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- 获取 `DASHSCOPE_API_KEY`：在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建并配置至环境变量。

### 2. 接口选择与调用
- **DashScope API（推荐）**  
  Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  支持 Python/Java/Go 等 SDK 及 HTTP 直接调用，请求体结构简洁（`input.prompt` + `parameters` + `debug`）。适用于对性能和功能完整性要求较高的场景。

- **Responses API（OpenAI 兼容）**  
  - 同步：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  - 异步：同上，但请求体需含 `"background": true`  
  优势在于复用现有 OpenAI 代码库，支持更丰富的输入格式（如 `messages` 数组、`input_image`、`input_file`）。

### 3. 多轮对话实现
- **DashScope API**：通过 `session_id` 维护上下文。首次调用不传，响应中返回 `session_id`；后续请求携带该 ID 即可延续会话（有效期：最后一次请求后 1 小时）。
- **Responses API**：直接在 `input` 中传入完整消息历史数组（`messages`），无需维护 `session_id`。当前不支持基于 `pre_response_id` 或 `conversation_id` 的上下文管理。

## 限制和注意事项

- **地域限制**：所有文档（文档 2、3、4、5）均明确标注“本文档仅适用于华北2（北京）地域”。其他地域（如法兰克福、新加坡）虽支持调用，但需额外提供 `Workspace ID` 且 Base URL 不同，具体请参考 [Base URL 文档](https://help.aliyun.com/zh/model-studio/regions/)。
- **权限要求**：获取 `Workspace ID` 需主账号或具备 `AliyunBailianFullAccess`/`AliyunBailianControlFullAccess` 权限的 RAM 子账号；普通子账号仅能查看已加入的业务空间 ID。
- **异步限制**：异步调用不支持流式输出（`stream=true` 会被忽略），且需主动轮询任务状态（`retrieve` 接口），无 Webhook 回调机制。
- **安全实践**：禁止在生产代码中硬编码 `API Key`，应通过环境变量（如 `DASHSCOPE_API_KEY`）注入。SDK 示例中均包含此提醒，符合最小权限原则。
- **调试支持**：所有应用均提供控制台在线调试入口（应用卡片 → 发布 → API 调试），建议开发阶段优先使用。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


