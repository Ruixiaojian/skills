# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者可通过同步、异步或流式方式发起请求，支持文本、图像、文件等多模态输入，并可复用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或原生 DashScope SDK。调用前需准备 APP ID、Workspace ID（如适用）及有效的 API Key。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **多模态输入**：
  - 图像：需选用通义千问 VL 系列模型，并在应用中配置为“自定义处理”（智能体）或设置 `imageList` 入参（工作流）[同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)；
  - 文件：仅智能体应用支持，需启用“全文引用”或“切片检索”文件处理方式；
  - 音频/视频：当前仅支持作为 URL 传入（如 `file_url`），由模型节点解析内容。
- **会话管理**：
  - DashScope API 通过 `session_id` 维护上下文，有效期为最后一次请求后 1 小时；
  - OpenAI 兼容模式（Responses API）暂不支持 `pre_response_id` 或 `conversation_id`，需在每次请求中传递完整对话历史。

> **注意**：文档 3 和文档 5 均描述了 `/api/v1/apps/{APP_ID}/completion` 接口，但文档 3 明确限定为“新版智能体应用”，而文档 5 泛指“智能体与工作流应用”。实际调用时，工作流应用应优先参考文档 5；若使用新版智能体，文档 3 提供更精确的参数说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，从[应用管理](https://bailian.console.aliyun.com/#/app-center)页面获取。 |
| `workspace_id` | string | 否（按需） | 业务空间唯一标识，子业务空间或德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域下必须提供，详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` / `prompt` | string 或 array | 是 | 核心输入：<br>- DashScope API 使用 `prompt` 字符串（单轮）或 `messages` 数组（多轮）；<br>- Responses API 使用 `input`，支持字符串（单轮）或消息对象数组（含 `role`, `content`，支持 `input_text`/`input_image`/`input_file`）。 |
| `stream` | boolean | 否 | 仅 Responses API 支持。`true` 启用[流式输出](../concepts/streaming-output.md)；工作流应用需在结束节点启用“[流式输出](../concepts/streaming-output.md)”开关并重新发布。 |
| `background` | boolean | 否 | 仅 Responses API 支持。`true` 切换为异步模式，立即返回任务 ID；异步任务不支持 `stream=true`。 |
| `biz_params` | object | 否 | 仅 Responses API 异步调用支持，用于传递工作流/智能体中预设的自定义参数（如 `{"city": "北京"}`）。 |

## 使用方式

### 1. 接口地址
- **DashScope API（推荐用于新版智能体/工作流）**：  
  `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
- **Responses API（OpenAI 兼容，支持同步/异步/流式）**：  
  同步：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  异步：同上，但请求体含 `"background": true`

### 2. 认证方式
- 所有请求均需在 Header 中携带 `Authorization: Bearer ${DASHSCOPE_API_KEY}`。
- API Key 需通过[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)获取并配置为环境变量 `DASHSCOPE_API_KEY`。

### 3. 代码示例（核心场景）
- **同步调用（文本）**：见 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md) 的 Python/curl 示例。
- **多轮对话（DashScope）**：首次调用不传 `session_id`，后续请求携带响应中的 `output.session_id`。
- **异步调用**：设置 `background=true` 获取 `task_id`，再轮询 `GET /responses/{task_id}` 查询状态（详见 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)）。

## 限制和注意事项

- **地域限制**：所有文档均明确标注“仅适用于华北2（北京）地域”，其他地域（如德国、新加坡）需配合 `workspace_id` 使用对应 Base URL，且部分功能可能受限。
- **凭证获取**：APP ID 和 Workspace ID **仅支持控制台手动获取**，不提供 API 或 CLI 查询接口 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **权限要求**：查询全部 Workspace ID 需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号；普通子账号仅能查看已加入的业务空间。
- **超时与重试**：同步调用默认超时时间较短，耗时任务（如复杂工作流）务必使用异步模式；异步任务轮询间隔建议 ≥2 秒。
- **流式限制**：异步调用 (`background=true`) 与[流式输出](../concepts/streaming-output.md) (`stream=true`) **互斥**，二者不可同时启用。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)


