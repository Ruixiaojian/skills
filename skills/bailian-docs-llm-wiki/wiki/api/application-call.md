# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者只需提供应用凭证（APP ID 及可选的 Workspace ID）、API Key 和输入内容，即可触发模型推理、工具调用与业务逻辑执行。该机制支持文本、图像、文件等多模态输入，并兼容 OpenAI 接口风格，便于快速迁移现有代码。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **调用模式**：
  - **同步调用**：适用于实时交互场景，立即返回完整响应；支持[流式输出](../concepts/streaming-output.md)（`stream=true`），但工作流需在结束节点启用流式开关并重新发布。
  - **异步调用**：适用于耗时较长任务（如复杂报告生成），通过 `background=true` 立即返回任务 ID，后续轮询查询结果；**异步模式不支持[流式输出](../concepts/streaming-output.md)**，详见 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **输入模态**：
  - 文本：单轮字符串或标准 Messages 数组（含 `system`/`user`/`assistant` 角色）。
  - 图像：仅限智能体应用（需选用通义千问 VL 模型并配置为“自定义处理”）或工作流应用（模型节点入参设为 `imageList`）。
  - 文件：仅限智能体应用（需选择“全文引用”或“切片检索”文件处理方式）。

> **注意**：文档 2 和文档 3 均声明“仅适用于华北2（北京）地域”，但文档 1 明确指出德国（法兰克福）、新加坡、日本（东京）等地域调用子业务空间应用时也必须传入 `Workspace ID`，且其 Base URL 已适配对应地域。因此，`application call` 实际支持多地域，但 DashScope API 的 endpoint 需按地域调整，而 Responses API 当前仍限定华北2（北京）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)中获取，详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `workspace_id` | string | 否（条件必填） | 业务空间唯一标识。当应用位于子业务空间，或部署在德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域时**必须提供**。 |
| `input` | string \| array | 是 | 核心输入。单轮对话可为字符串；多轮或含多媒体时为 Messages 数组，其中 `content` 支持 `input_text`/`input_image`/`input_file` 类型。 |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming-output.md)（默认 `false`）。仅同步调用有效，且工作流需提前发布时启用流式开关。 |
| `background` | boolean | 否 | 是否启用异步模式（默认 `false`）。设为 `true` 时返回任务 ID，不可与 `stream=true` 共存。 |
| `biz_params` | object | 否 | 自定义参数对象，用于向工作流或智能体传递插件/模型所需变量（如 `{"city": "北京"}`），需与应用内参数配置严格一致。 |

## 使用方式

### 1. 凭证准备
- 获取 `APP ID` 和（如需）`Workspace ID`：通过百炼控制台手动复制，**不支持 API 或 CLI 查询**，详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- 获取 `DASHSCOPE_API_KEY`：在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)中创建并配置至环境变量。

### 2. 接口选择与调用
- **DashScope API（推荐）**  
  Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  支持 Python/Java/Go/C#/Node.js/PHP SDK 及 HTTP 直连，内置 `session_id` 多轮会话管理（有效期 1 小时）。

- **OpenAI 兼容 Responses API（同步）**  
  Endpoint：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  适配 OpenAI SDK，支持 `input` 为字符串或 Messages 数组，`stream` 控制输出模式。

- **OpenAI 兼容 Responses API（异步）**  
  Endpoint：同上，但请求体中设置 `"background": true`，响应返回 `id` 字段作为任务 ID，后续通过 `GET /responses/{task_id}` 查询状态。

> **注意**：文档 4 和文档 5 均强调 Responses API “仅适用于华北2（北京）地域”，而文档 2 和文档 3 的 DashScope API 示例未明确地域限制，但实际调用需根据 `workspace_id` 所属地域选择对应 endpoint（如法兰克福地域应使用 `dashscope.eu-central-1.aliyuncs.com`）。开发者需依据 [Base URL 文档](https://help.aliyun.com/zh/model-studio/regions/) 配置正确域名。

## 限制和注意事项

- **地域与 Workspace ID 绑定**：调用德国（法兰克福）、新加坡、日本（东京）等非北京地域的应用时，`workspace_id` 是必需参数，且其值决定请求路由的 endpoint，详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **多轮会话**：DashScope API 通过 `session_id` 维护上下文（1 小时有效期）；Responses API **不支持 `pre_response_id` 或 `conversation_id`**，必须在每次请求中传入完整历史消息数组。
- **异步约束**：`background=true` 时 `stream` 参数将被忽略，且无法流式输出；任务状态需主动轮询（建议间隔 ≥2 秒）。
- **安全实践**：API Key **严禁硬编码**，务必通过环境变量（如 `DASHSCOPE_API_KEY`）注入；生产环境应结合 RAM 权限策略最小化授权。
- **调试支持**：所有应用均提供控制台内“API 调试”功能（路径：应用卡片 → 发布 → API 调试），可快速验证参数与响应。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


